from __future__ import annotations

import warnings
from datetime import datetime
from pathlib import Path

import pytest
from rich.table import Table

from pretty_loguru import create_logger
from pretty_loguru.core.extension_system import (
    apply_extensions,
    clear_extensions,
    get_extension_method,
    list_extensions,
    register_extension_method,
)
from pretty_loguru.core.presets import (
    _create_rename_function,
    _subtract_one_month,
    get_preset_config,
    list_available_presets,
)
from pretty_loguru.core.pretty_event import (
    build_renderable,
    render_renderable_to_text,
    validate_pretty_payload,
)
from pretty_loguru.core.target_formatter import ensure_target_parameters, log_to_targets
from pretty_loguru.core.templates import ConfigTemplates
from tests.conftest import capture_loguru_messages


def test_target_formatter_log_to_targets_and_decorator(tmp_path: Path):
    logger = create_logger("targets", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        log_to_targets(logger, "both", level="INFO")
        log_to_targets(logger, "console_only", level="INFO", console_only=True)
        log_to_targets(logger, "file_only", level="INFO", file_only=True)

    assert any(r["message"] == "both" for r in records)
    assert any(r["message"] == "console_only" and r["extra"].get("to_console_only") is True for r in records)
    assert any(r["message"] == "file_only" and r["extra"].get("to_file_only") is True for r in records)

    with pytest.raises(ValueError):
        log_to_targets(logger, "bad", console_only=True, file_only=True)

    @ensure_target_parameters
    def f(*, to_console_only: bool = False, to_file_only: bool = False, _target_depth: int = 0):
        return (to_console_only, to_file_only, _target_depth)

    assert f() == (False, False, 2)


def test_extension_system_register_apply_list_clear():
    clear_extensions()

    class Obj:
        pass

    obj = Obj()

    def hello(self):
        return "hi"

    register_extension_method(obj, "hello", hello)
    assert callable(getattr(obj, "hello"))
    assert obj.hello() == "hi"
    assert get_extension_method("hello") is hello
    assert "hello" in list_extensions()

    with pytest.raises(ValueError):
        register_extension_method(obj, "hello", hello)

    register_extension_method(obj, "hello", hello, overwrite=True)
    apply_extensions(obj)
    assert obj.hello() == "hi"

    clear_extensions()
    assert list_extensions() == {}


def test_presets_list_and_core_behaviors(tmp_path: Path):
    presets = list_available_presets()
    assert "daily" in presets and "detailed" in presets

    for name in presets:
        conf = get_preset_config(name)
        assert {"rotation", "retention", "compression", "name_format"}.issubset(conf.keys())

    # _subtract_one_month：處理月底（例如 3/31 -> 2/28 或 2/29）
    assert _subtract_one_month(datetime(2025, 3, 31)).month == 2

    # loguru_suffix 解析：詳細模式會嘗試從檔名中解析時間戳
    renamer = _create_rename_function(pattern="[{name}].{timestamp}", time_source="loguru_suffix")

    src = tmp_path / "[app]20250101-000000.log.2025-05-05_23-29-33_084163.log"
    src.write_text("x", encoding="utf-8")
    new_path_str = renamer(str(src))
    new_path = Path(new_path_str)
    assert src.exists() is False
    assert new_path.exists() is True
    assert new_path.name.startswith("[app].20250505-232933")

    # suffix 缺失時會 warnings.warn 並使用 current time
    renamer2 = _create_rename_function(pattern="[{name}].{timestamp}", time_source="loguru_suffix")
    src2 = tmp_path / "[app]no_suffix.log"
    src2.write_text("x", encoding="utf-8")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = renamer2(str(src2))
        assert any("Loguru suffix not found" in str(x.message) for x in w)


def test_pretty_event_build_renderable_and_render_to_text():
    validate_pretty_payload("block", {"title": "T", "lines": ["a"], "border_style": "cyan"})
    with pytest.raises(ValueError):
        validate_pretty_payload("", {})
    with pytest.raises(ValueError):
        validate_pretty_payload("block", "not a dict")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_pretty_payload("block", {"title": "T"})
    with pytest.raises(ValueError):
        validate_pretty_payload("block", {"title": "T", "lines": "nope"})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_pretty_payload("ascii_header", {"text": "x"})
    with pytest.raises(ValueError):
        validate_pretty_payload("table", {"rows": []})
    with pytest.raises(ValueError):
        validate_pretty_payload("tree", {"title": "t"})
    with pytest.raises(ValueError):
        validate_pretty_payload("columns", {"title": "t"})
    with pytest.raises(ValueError):
        validate_pretty_payload("code", {})
    with pytest.raises(ValueError):
        validate_pretty_payload("diff", {"old_code": "a"})
    with pytest.raises(ValueError):
        validate_pretty_payload("panel", {})
    with pytest.raises(ValueError):
        validate_pretty_payload("renderable", {})

    renderables = [
        build_renderable("block", {"title": "T", "lines": ["a"], "border_style": "cyan", "box": "rounded"}),
        build_renderable(
            "panel",
            {"content": "c", "title": "t", "subtitle": "s", "border_style": "cyan", "box_style": "ascii"},
        ),
        build_renderable(
            "table",
            # headers=None 時會從第一列 rows 推導（覆蓋該分支）
            {"title": "Users", "headers": None, "rows": [{"name": "Alice"}], "show_header": True},
        ),
        build_renderable(
            "tree",
            {
                "title": "Root",
                "data": {"k": ["a", {"x": 1}]},  # 覆蓋 _tree_add 的 list 分支
                "style": "tree",
                "guide_style": "tree.line",
            },
        ),
        build_renderable("columns", {"title": "Cols", "items": ["a", "b"], "padding": (0, 1), "expand": False}),
        build_renderable(
            "code",
            {"code": "print('x')\n", "language": "python", "theme": "monokai", "line_numbers": True},
        ),
        build_renderable(
            "diff",
            {
                "old_title": "old",
                "new_title": "new",
                "old_code": "a\n",
                "new_code": "b\n",
                "language": "python",
                "theme": "monokai",
            },
        ),
        build_renderable("renderable", {"title": "R", "text": "hello"}),
        build_renderable("ascii_header", {"text": "t", "font": "standard", "art": "ASCII", "border_style": "cyan"}),
        build_renderable("ascii_block", {"title": "T", "lines": ["ASCII", "x"], "border_style": "cyan"}),
        build_renderable("figlet_header", {"text": "t", "font": "standard", "art": "FIG", "border_style": "cyan"}),
        build_renderable("figlet_block", {"title": "T", "lines": ["FIG", "x"], "border_style": "cyan"}),
        build_renderable("unknown_kind", {"x": 1}),  # fallback Panel
    ]

    for r in renderables:
        text = render_renderable_to_text(r)
        assert isinstance(text, str)
        assert text.strip()

    # 確保也能處理「使用者自行建立的 renderable」
    t = Table(title="T")
    t.add_column("a")
    t.add_row("1")
    assert "1" in render_renderable_to_text(t)


def test_templates_cover_all_builtins():
    # 只要求能建立，不測寫入（避免污染 repo）
    for name in ConfigTemplates.list_all():
        cfg = ConfigTemplates.get(name)
        assert cfg is not None
