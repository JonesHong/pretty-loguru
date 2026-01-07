from __future__ import annotations

import re
import warnings
from datetime import datetime
from pathlib import Path

import pytest

from pretty_loguru.core import presets as p


def test_subtract_one_month_handles_january_rollover():
    dt = datetime(2025, 1, 15)
    out = p._subtract_one_month(dt)
    assert out.year == 2024 and out.month == 12


def test_rename_function_parsing_and_time_sources(tmp_path: Path):
    # 1) loguru_suffix parse failure -> warnings.warn
    renamer = p._create_rename_function(pattern="[{name}].{timestamp}", time_source="loguru_suffix")
    src = tmp_path / "[app]x.log.not-a-ts.log"
    src.write_text("x", encoding="utf-8")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        new_path = Path(renamer(str(src)))
        assert new_path.exists() is True
        assert any("Could not parse timestamp" in str(x.message) for x in w)

    # 2) 沒有 [component] 的檔名 -> regex match 失敗分支
    renamer2 = p._create_rename_function(pattern="{name}_rot_{timestamp}", time_source="current")
    src2 = tmp_path / "plain.log"
    src2.write_text("x", encoding="utf-8")
    out2 = Path(renamer2(str(src2)))
    assert out2.exists() is True
    assert out2.name.startswith("plain_rot_")

    # 3) time_source 分支（只驗證能產生檔案且命名符合 pattern）
    for ts in ["yesterday", "last_hour", "last_minute", "last_week", "last_month"]:
        ren = p._create_rename_function(pattern="[{name}]{date}", time_source=ts)  # type: ignore[arg-type]
        f = tmp_path / f"[svc]{ts}.log"
        f.write_text("x", encoding="utf-8")
        out = Path(ren(str(f)))
        assert out.exists() is True
        assert re.match(r"\[svc\]\d{8}(\.\d+)?\.log", out.name) is not None


def test_rename_function_missing_format_variable_raises(tmp_path: Path):
    renamer = p._create_rename_function(pattern="{missing}", time_source="current")
    src = tmp_path / "[x]a.log"
    src.write_text("x", encoding="utf-8")
    with pytest.raises(KeyError):
        renamer(str(src))


def test_register_custom_preset_and_factory():
    name = "custom_x"
    cfg = {
        "rotation": "1 day",
        "retention": "7 days",
        "compression": p.create_custom_compression_function("backup_{name}_{date}"),
        "name_format": "{component_name}.log",
    }
    p.register_custom_preset(name, cfg)
    assert p.get_preset_config(name)["rotation"] == "1 day"

    # required keys 缺失
    with pytest.raises(ValueError):
        p.register_custom_preset("bad", {"rotation": "1 day"})  # type: ignore[arg-type]

    assert name in p.PresetFactory.list_presets()
    assert p.PresetFactory.get_preset(name)["retention"] == "7 days"

    with pytest.raises(ValueError):
        p.get_preset_config("not-exist")  # type: ignore[arg-type]
