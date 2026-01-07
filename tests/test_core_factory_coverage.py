from __future__ import annotations

import json
import platform
from pathlib import Path

import pytest
from loguru import logger as _base_logger

import pretty_loguru
from pretty_loguru import LoggerConfig, create_logger
from pretty_loguru.core import event_system, registry
from pretty_loguru.core.handlers import adapt_rotation_value, format_filename
from pretty_loguru.core.templates import ConfigTemplates, create_config
from pretty_loguru.factory.updater import update_logger_config, update_logger_level


def test_top_level_lazy_modules():
    assert pretty_loguru.__version__
    assert hasattr(pretty_loguru, "create_logger")

    addons = pretty_loguru.addons
    integrations = pretty_loguru.integrations
    assert addons is not None
    assert integrations is not None

    with pytest.raises(AttributeError):
        getattr(pretty_loguru, "not_exist")


def test_event_system_subscribe_unsubscribe_and_error(capsys: pytest.CaptureFixture[str]):
    event_system.clear_events()

    called = []

    def ok_handler(*args, **kwargs):
        called.append(("ok", args, kwargs))

    def bad_handler(*args, **kwargs):
        raise RuntimeError("boom")

    event_system.subscribe("e1", ok_handler)
    event_system.subscribe("e1", bad_handler)
    assert "e1" in event_system.list_events()
    assert event_system.listener_count("e1") == 2

    event_system.post_event("e1", 1, a=2)
    assert called and called[0][0] == "ok"

    out = capsys.readouterr().out
    assert "Error in event listener" in out

    assert event_system.unsubscribe("e1", ok_handler) is True
    assert event_system.unsubscribe("e1", ok_handler) is False
    event_system.clear_events()
    assert event_system.event_count() == 0


def test_registry_register_update_clear_triggers_events():
    event_system.clear_events()
    events = []

    def on_registered(name, logger):
        events.append(("registered", name))

    def on_updated(name, logger):
        events.append(("updated", name))

    def on_cleared(count: int):
        events.append(("cleared", count))

    event_system.subscribe("logger_registered", on_registered)
    event_system.subscribe("logger_updated", on_updated)
    event_system.subscribe("registry_cleared", lambda **kw: on_cleared(kw["count"]))

    logger = _base_logger.bind(test=1)
    registry.register_logger("a", logger)
    assert registry.get_logger("a") is logger
    assert "a" in registry.list_loggers()

    assert registry.update_logger("a", logger) is True
    assert registry.update_logger("missing", logger) is False
    assert registry.unregister_logger("a") is True
    assert registry.unregister_logger("a") is False

    registry.register_logger("b", logger)
    assert registry.get_registry_size() == 1
    assert registry.clear_registry() == 1

    assert ("registered", "a") in events
    assert ("updated", "a") in events
    assert ("cleared", 1) in events


def test_handlers_format_filename_and_rotation_adapter():
    name = format_filename("svc", "[{component_name}]daily_latest.temp.log")
    assert name.startswith("[svc]daily_latest.temp.log")

    with pytest.raises(KeyError):
        format_filename("svc", "{missing}.log")

    assert adapt_rotation_value(10) == "10 MB"
    assert adapt_rotation_value("20") == "20 MB"
    assert adapt_rotation_value("1 day") == "1 day"
    assert adapt_rotation_value("weird") == "weird"


def test_templates_builtin_custom_and_create_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    dev = ConfigTemplates.development()
    assert dev.level == "DEBUG"
    assert dev.use_native_format is True

    # 覆蓋 Windows/Unix 分支（只驗證路徑規則，不在測試中寫入該目錄）
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    prod_win = ConfigTemplates.production()
    assert "AppData" in str(prod_win.log_dir)

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    prod_unix = ConfigTemplates.production()
    assert ".local" in str(prod_unix.log_dir)

    custom = LoggerConfig(level="INFO", log_dir=str(tmp_path / "logs"))
    ConfigTemplates.register("my_template", custom)
    got = ConfigTemplates.get("my_template")
    assert got is not None and got.level == "INFO"
    assert ConfigTemplates.unregister("my_template") is True
    assert ConfigTemplates.unregister("my_template") is False

    cfg = create_config(level="WARNING", log_dir=str(tmp_path / "x"), rotation="1 day", serialize=True)
    cfg.validate_strict()


def test_logger_config_validate_strict_errors(tmp_path: Path):
    bad_rotation = LoggerConfig(log_dir=str(tmp_path), rotation="not a rotation")
    with pytest.raises(ValueError):
        bad_rotation.validate_strict()

    bad_retention = LoggerConfig(log_dir=str(tmp_path), retention="nonsense")
    with pytest.raises(ValueError):
        bad_retention.validate_strict()

    bad_loki = LoggerConfig(log_dir=None, loki_enabled=True, loki_base_url=None)
    with pytest.raises(ValueError):
        bad_loki.validate_strict()


def test_logger_config_apply_update_from_dict_save_load(tmp_path: Path):
    log_dir = tmp_path / "logs"
    cfg = LoggerConfig(level="INFO", log_dir=str(log_dir), rotation="20 MB", retention="7 days")

    with pytest.raises(ValueError):
        cfg.apply_to("a", create_if_missing=False)

    logger = cfg.apply_to("a")
    assert logger is not None
    assert LoggerConfig.logger_exists("a") is True
    assert "a" in cfg.get_attached_loggers()

    cfg.update(level="DEBUG")
    cfg.update_from_dict({"retention": "3 days"})

    with pytest.raises(TypeError):
        cfg.update_from_dict("not a dict")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        cfg.update_from_dict({"_private": 1})
    with pytest.raises(ValueError):
        cfg.update_from_dict({"not_a_field": 1})

    cfg.detach("a")
    assert "a" not in cfg.get_attached_loggers()
    cfg.detach_all()
    assert not cfg.get_attached_loggers()

    cloned = cfg.clone(level="ERROR")
    assert cloned.level == "ERROR"

    parent = LoggerConfig(level="WARNING", log_dir=str(tmp_path / "p"))
    child = LoggerConfig(level="INFO", log_dir=None).inherit_from(parent, level="DEBUG")
    assert child.level == "DEBUG"
    assert child.log_dir == parent.log_dir

    path = tmp_path / "cfg.json"
    cfg.save_to_file(path)
    loaded = LoggerConfig.from_file(path)
    assert loaded.to_dict()["level"] == cfg.to_dict()["level"]

    with pytest.raises(FileNotFoundError):
        LoggerConfig.from_file(tmp_path / "missing.json")


def test_factory_create_logger_force_new_instance_and_config_override(tmp_path: Path):
    base = create_logger("svc", log_dir=str(tmp_path / "logs"), enable_addons=False)
    again = create_logger("svc", enable_addons=False)
    assert base is again

    with pytest.warns(UserWarning):
        new_one = create_logger("svc", force_new_instance=True, enable_addons=False)
    assert new_one is not base

    cfg = LoggerConfig(level="INFO", log_dir=str(tmp_path / "x"), rotation="20 MB")
    overridden = create_logger("cfg_logger", config=cfg, level="ERROR", enable_addons=False)
    stored = getattr(overridden, "_pretty_loguru_config", None)
    assert stored is not None
    assert getattr(stored, "level") == "ERROR"


def test_updater_update_logger_level_and_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    logger = create_logger("lvl", log_dir=str(tmp_path / "logs"), enable_addons=False)
    assert update_logger_level("lvl", "ERROR") is True

    # 沒有 stored config 的 logger 會被拒絕（避免操作 shared core 造成副作用）
    raw = _base_logger.bind(raw=True)
    registry.register_logger("raw", raw)
    with pytest.warns(UserWarning):
        assert update_logger_level("raw", "INFO") is False

    called = {}

    def fake_restart(path: str, **kwargs):
        called["path"] = path

    monkeypatch.setattr("pretty_loguru.factory.creator._restart_cleaner_for_path", fake_restart)

    cfg = LoggerConfig(level="INFO", log_dir=str(tmp_path / "logs2"), start_cleaner=True)
    assert update_logger_config("lvl", cfg, restart_cleaner=True) is True
    assert "logs2" in str(called["path"])


def test_config_validate_log_dir_must_be_directory(tmp_path: Path):
    cfg = LoggerConfig(log_dir=str(tmp_path / "app.log"))
    with pytest.raises(ValueError):
        cfg.validate()
