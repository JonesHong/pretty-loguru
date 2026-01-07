from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from rich.table import Table

from pretty_loguru import create_logger
from pretty_loguru.formats import ascii_art, rich_components
from tests.conftest import capture_loguru_messages


def test_rich_components_functions_emit_single_pretty_event(tmp_path: Path):
    logger = create_logger("rich", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        rich_components.print_table(
            title="Users",
            data=[{"name": "Alice", "age": 30}],
            logger_instance=logger,
        )
        rich_components.print_tree(
            title="Root",
            tree_data={"a": {"b": 1}},
            logger_instance=logger,
        )
        rich_components.print_columns(
            title="Cols",
            items=["a", "b"],
            logger_instance=logger,
        )
        rich_components.print_panel(
            content="hello",
            title="Panel",
            logger_instance=logger,
        )
        rich_components.print_code(
            code="print('x')\n",
            language="python",
            logger_instance=logger,
        )
        rich_components.print_diff(
            old_code="a\n",
            new_code="b\n",
            old_title="old",
            new_title="new",
            logger_instance=logger,
        )

        t = Table(title="T")
        t.add_column("a")
        t.add_row("1")
        rich_components.print_renderable(t, title="T", logger_instance=logger)

    kinds = [r["extra"].get("pretty_kind") for r in records if "pretty_kind" in r.get("extra", {})]
    assert {"table", "tree", "columns", "panel", "code", "diff", "renderable"}.issubset(set(kinds))

    for r in records:
        extra = r.get("extra", {})
        if extra.get("pretty_kind"):
            assert isinstance(extra.get("pretty_payload"), dict)
            assert isinstance(extra.get("pretty_text"), str)
            assert extra["pretty_text"].strip()


def test_rich_components_edge_cases(tmp_path: Path):
    logger = create_logger("rich_edge", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        rich_components.print_table("Empty", [], logger_instance=logger)
        rich_components.print_columns("Empty", [], logger_instance=logger)
        rich_components.print_table("NoLogger", [{"a": 1}], logger_instance=None)

    assert any("has no data" in r["message"] for r in records)
    assert any("has no items" in r["message"] for r in records)


def test_logger_progress_context(tmp_path: Path):
    logger = create_logger("progress", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    prog = rich_components.LoggerProgress(logger)
    with capture_loguru_messages(logger, formatter=str) as msgs:
        with prog.progress_context("Work", total=3) as update:
            update(1)
            update(2)
    assert any("Starting progress" in m for m in msgs)
    assert any("Completed progress" in m for m in msgs)


def test_create_rich_methods_injects_logger_methods(tmp_path: Path):
    logger = create_logger("inject", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    rich_components.create_rich_methods(logger)
    assert hasattr(logger, "table")
    assert hasattr(logger, "tree")
    assert hasattr(logger, "columns")
    assert hasattr(logger, "code")
    assert hasattr(logger, "diff")
    assert hasattr(logger, "panel")

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        logger.table("Users", [{"name": "A"}])
        logger.tree("Root", {"a": 1})
        logger.columns("Cols", ["a"])
        logger.code("x=1\n", language="python")
        logger.diff("a\n", "b\n", old_title="o", new_title="n")
        logger.panel("c", title="t")

    assert any(r["extra"].get("pretty_kind") == "table" for r in records)


def test_rich_components_code_from_file_and_track_list(tmp_path: Path):
    logger = create_logger("rich_file", log_dir=str(tmp_path / "logs"), level="DEBUG", enable_addons=False)
    logger.remove()

    code_file = tmp_path / "example.py"
    code_file.write_text("a=1\nb=2\nc=3\n", encoding="utf-8")

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        rich_components.print_code_from_file(
            file_path=str(code_file),
            language=None,  # 讓函式自行推導
            start_line=2,
            end_line=3,
            logger_instance=logger,
        )
        rich_components.print_code_from_file(
            file_path=str(tmp_path / "missing.py"),
            logger_instance=logger,
        )

        prog = rich_components.LoggerProgress(logger)
        items = list(prog.track_list([1, 2], description="Items"))
        assert items == [1, 2]

    assert any(r["extra"].get("pretty_kind") == "code" for r in records)
    assert any("File not found" in r["message"] for r in records)
    assert any("Completed tracking" in r["message"] for r in records)

    # methods：code_file + render + progress property
    rich_components.create_rich_methods(logger)
    with capture_loguru_messages(logger, formatter=str) as msgs:
        logger.code_file(str(code_file), start_line=1, end_line=1)
        t = Table(title="T")
        t.add_column("a")
        t.add_row("1")
        logger.render(t, title="T")
        with logger.progress.progress_context("Work", total=1) as update:
            update(1)
    assert any("Starting progress" in m for m in msgs)


def test_ascii_art_emits_pretty_payload(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    logger = create_logger("ascii", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    monkeypatch.setattr(ascii_art, "text2art", lambda text, **kw: "ASCII")

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        ascii_art.print_ascii_header("test", logger_instance=logger)
        ascii_art.print_ascii_block("TITLE", ["line1"], logger_instance=logger)

    assert any(r["extra"].get("pretty_kind") == "ascii_header" for r in records)
    assert any(r["extra"].get("pretty_kind") == "ascii_block" for r in records)


def test_formats_init_has_figlet_true_via_reload(monkeypatch: pytest.MonkeyPatch):
    # 模擬 pyfiglet 存在，覆蓋 formats/__init__.py 的 _has_figlet 分支
    fake = ModuleType("pyfiglet")

    def figlet_format(text: str, font: str = "standard") -> str:
        return f"FIGLET:{text}:{font}"

    class _FF:
        @staticmethod
        def getFonts():
            return ["standard"]

    fake.figlet_format = figlet_format  # type: ignore[attr-defined]
    sys.modules["pyfiglet"] = fake

    # figlet.py 內部 also imports FigletFont；提供 pyfiglet.FigletFont
    fake.FigletFont = _FF  # type: ignore[attr-defined]

    import pretty_loguru.formats as formats

    formats = importlib.reload(formats)
    assert formats.has_figlet() is True
    assert "print_figlet_header" in formats.__all__

    # 清理
    monkeypatch.delitem(sys.modules, "pyfiglet", raising=False)
    importlib.reload(formats)


def test_figlet_module_with_patching(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # 直接 import 模組（即使沒裝 pyfiglet 也要能跑），再用 patch 走主要路徑
    import pretty_loguru.formats.figlet as figlet

    logger = create_logger("figlet", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    class DummyFiglet:
        @staticmethod
        def figlet_format(text: str, font: str = "standard") -> str:
            return f"FIG:{text}:{font}"

    class DummyFigletFont:
        @staticmethod
        def getFonts():
            return ["standard", "slant"]

    monkeypatch.setattr(figlet, "_has_pyfiglet", True)
    monkeypatch.setattr(figlet, "pyfiglet", DummyFiglet)
    monkeypatch.setattr(figlet, "FigletFont", DummyFigletFont)
    monkeypatch.setattr(figlet, "ensure_pyfiglet_dependency", lambda *a, **k: True)

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        figlet.print_figlet_header("hi世界", logger_instance=logger)  # 會清理非 ASCII
        figlet.print_figlet_block("T", ["x"], figlet_header="ok", logger_instance=logger)

    assert any(r["extra"].get("pretty_kind") == "figlet_header" for r in records)
    assert any(r["extra"].get("pretty_kind") == "figlet_block" for r in records)

    fonts = figlet.get_figlet_fonts()
    assert "standard" in fonts

    # create_figlet_methods：_has_pyfiglet=True 分支
    assert figlet.create_figlet_methods(logger) is True
    assert hasattr(logger, "figlet_header")
    assert hasattr(logger, "get_figlet_fonts")

    # create_figlet_methods：_has_pyfiglet=False 分支（warn_missing_dependency）
    monkeypatch.setattr(figlet, "_has_pyfiglet", False)
    assert figlet.create_figlet_methods(logger) is False
