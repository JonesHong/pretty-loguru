from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from pretty_loguru import create_logger
from tests.conftest import capture_loguru_messages


def test_advanced_module_exports_and_availability():
    import pretty_loguru.advanced as adv

    available = adv.get_available_libraries()
    assert set(available.keys()) == {"loguru", "rich", "art", "pyfiglet"}
    assert available is not adv.AVAILABLE_LIBRARIES

    assert isinstance(adv.check_library("rich"), bool)
    assert adv.check_library("not_a_lib") is False


def test_advanced_helpers_create_rich_table_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pretty_loguru.advanced import helpers

    logger = create_logger("adv_table", log_dir=str(tmp_path / "logs"), level="DEBUG", enable_addons=False)
    logger.remove()

    # HAS_RICH=False 分支
    monkeypatch.setattr(helpers, "HAS_RICH", False)
    with capture_loguru_messages(logger, formatter=str) as msgs:
        helpers.create_rich_table_log(logger, "T", [{"a": 1}])
    assert any("Rich library not available" in m for m in msgs)

    # 恢復並覆蓋 get_console 避免真的印出 table
    monkeypatch.setattr(helpers, "HAS_RICH", True)
    fake_console = SimpleNamespace(print=lambda *a, **k: None)
    monkeypatch.setattr(helpers, "get_console", lambda: fake_console)

    with capture_loguru_messages(logger, formatter=str) as msgs2:
        helpers.create_rich_table_log(logger, "Empty", [])
        helpers.create_rich_table_log(logger, "Scores", [{"name": "A", "score": 1}])

    assert any("has no data" in m for m in msgs2)
    assert any("Displaying table" in m for m in msgs2)
    assert any("Table:" in m for m in msgs2)  # file-only text 版本


def test_advanced_helpers_create_mixed_ascii_panel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pretty_loguru.advanced import helpers

    logger = create_logger("adv_panel", log_dir=str(tmp_path / "logs"), level="DEBUG", enable_addons=False)
    logger.remove()

    fake_console = SimpleNamespace(print=lambda *a, **k: None)
    monkeypatch.setattr(helpers, "get_console", lambda: fake_console)

    # HAS_ART=False 分支
    monkeypatch.setattr(helpers, "HAS_ART", False)
    monkeypatch.setattr(helpers, "HAS_RICH", True)
    with capture_loguru_messages(logger, formatter=str) as msgs:
        helpers.create_mixed_ascii_panel(logger, "OK", panel_title="P")
    assert any("Art library not available" in m for m in msgs)

    # HAS_RICH=False 分支（fallback to plain logging）
    monkeypatch.setattr(helpers, "HAS_RICH", False)
    with capture_loguru_messages(logger, formatter=str) as msgs2:
        helpers.create_mixed_ascii_panel(logger, "OK", panel_title="P2")
    assert any("ASCII Art" in m or "P2" in m for m in msgs2)

    # HAS_ART=True 但 text2art 失敗 -> warning branch
    monkeypatch.setattr(helpers, "HAS_RICH", True)
    monkeypatch.setattr(helpers, "HAS_ART", True)
    import pretty_loguru.advanced as adv

    monkeypatch.setattr(adv, "text2art", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    with capture_loguru_messages(logger, formatter=str) as msgs3:
        helpers.create_mixed_ascii_panel(logger, "OK", panel_title="P3")
    assert any("ASCII art generation failed" in m for m in msgs3)


def test_advanced_helpers_create_loguru_rich_sink(monkeypatch: pytest.MonkeyPatch):
    from pretty_loguru.advanced import helpers

    # HAS_RICH=False -> ImportError
    monkeypatch.setattr(helpers, "HAS_RICH", False)
    with pytest.raises(ImportError):
        helpers.create_loguru_rich_sink()

    # HAS_RICH=True -> return Console
    monkeypatch.setattr(helpers, "HAS_RICH", True)
    c = helpers.create_loguru_rich_sink(console=None)
    assert hasattr(c, "print")


def test_advanced_helpers_quick_figlet_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pretty_loguru.advanced import helpers

    logger = create_logger("adv_figlet", log_dir=str(tmp_path / "logs"), level="DEBUG", enable_addons=False)
    logger.remove()

    # HAS_PYFIGLET=False 分支
    monkeypatch.setattr(helpers, "HAS_PYFIGLET", False)
    with capture_loguru_messages(logger, formatter=str) as msgs:
        helpers.quick_figlet_log(logger, "READY")
    assert any("PyFiglet library not available" in m for m in msgs)
    assert any("FIGlet text" in m for m in msgs)

    # HAS_PYFIGLET=True 分支 + 正常 render
    class DummyFiglet:
        def __init__(self, font: str):
            self.font = font

        def renderText(self, text: str) -> str:  # noqa: N802 (match pyfiglet API)
            return f"{self.font}:{text}"

    import pretty_loguru.advanced as adv

    monkeypatch.setattr(helpers, "HAS_PYFIGLET", True)
    monkeypatch.setattr(adv, "Figlet", DummyFiglet)
    with capture_loguru_messages(logger, formatter=str) as msgs2:
        helpers.quick_figlet_log(logger, "GO", font="big")
    assert any("big:GO" in m for m in msgs2)

    # render 失敗 -> warning branch
    class BadFiglet(DummyFiglet):
        def renderText(self, text: str) -> str:  # noqa: N802
            raise RuntimeError("boom")

    monkeypatch.setattr(adv, "Figlet", BadFiglet)
    with capture_loguru_messages(logger, formatter=str) as msgs3:
        helpers.quick_figlet_log(logger, "GO", font="big")
    assert any("FIGlet generation failed" in m for m in msgs3)

