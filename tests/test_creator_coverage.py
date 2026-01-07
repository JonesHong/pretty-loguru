from __future__ import annotations
from types import SimpleNamespace
from typing import Any

import pytest


def test_ensure_base_logger_prepared_swallow_remove_failure(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.creator as creator

    class DummyBaseLogger:
        def remove(self, _handler_id: int) -> None:
            raise RuntimeError("boom")

    monkeypatch.setattr(creator, "_base_logger_prepared", False)
    monkeypatch.setattr(creator, "_base_logger", DummyBaseLogger())
    creator._ensure_base_logger_prepared()
    assert creator._base_logger_prepared is True


def test_install_user_handler_tracking_early_return_branches(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.creator as creator

    wrapped = SimpleNamespace(_pretty_loguru_add_wrapped=True, add=lambda *a, **k: 1)
    creator._install_user_handler_tracking(wrapped)

    no_add = SimpleNamespace()
    creator._install_user_handler_tracking(no_add)


def test_install_user_handler_tracking_wrapper_swallow_errors(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.creator as creator

    class DummyLogger:
        def add(self, *args: Any, **kwargs: Any) -> int:
            return 123

        def __getattribute__(self, name: str) -> Any:
            if name == "_pretty_loguru_user_handler_ids":
                raise RuntimeError("boom")
            return super().__getattribute__(name)

    dummy = DummyLogger()
    creator._install_user_handler_tracking(dummy)
    assert dummy.add("sink") == 123


def test_emit_cleaner_message_warns_when_no_logger():
    import pretty_loguru.factory.creator as creator

    with pytest.warns(UserWarning):
        creator._emit_cleaner_message(None, "warn", level="WARNING")


def test_create_logger_from_config_requires_name():
    import pretty_loguru.factory.creator as creator
    from pretty_loguru.core.config import LoggerConfig

    with pytest.raises(ValueError):
        creator._create_logger_from_config(LoggerConfig(name=None), enable_addons=False)


def test_create_logger_from_config_start_cleaner_without_log_dir_emits_warning():
    import pretty_loguru.factory.creator as creator
    from pretty_loguru.core.config import LoggerConfig
    from tests.conftest import capture_loguru_messages

    cfg = LoggerConfig(name="svc", start_cleaner=True, log_dir=None)
    logger = creator._create_logger_from_config(cfg, enable_addons=False)
    with capture_loguru_messages(logger, formatter=lambda m: m.record["message"]) as items:
        creator._create_logger_from_config(LoggerConfig(name="svc2", start_cleaner=True, log_dir=None), enable_addons=False)
    assert any("start_cleaner=True" in str(x) for x in items)


def test_cleaner_start_stop_restart_paths(monkeypatch: pytest.MonkeyPatch, tmp_path):
    import pretty_loguru.factory.creator as creator

    class DummyLogger:
        def __init__(self) -> None:
            self.messages: list[tuple[str, str]] = []

        def info(self, msg: str) -> None:
            self.messages.append(("info", msg))

        def error(self, msg: str) -> None:
            self.messages.append(("error", msg))

    class DummyCleaner:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs
            self.started = False
            self.stopped = False

        def start(self) -> None:
            self.started = True

        def stop(self) -> None:
            self.stopped = True

    logger = DummyLogger()

    monkeypatch.setattr(creator, "_active_cleaners", {})
    monkeypatch.setattr(creator, "LoggerCleaner", DummyCleaner)

    with pytest.warns(UserWarning):
        creator._start_cleaner_for_path("", logger_instance=None, verbose=False)

    creator._start_cleaner_for_path(str(tmp_path), logger_instance=logger, verbose=True)
    creator._start_cleaner_for_path(str(tmp_path), logger_instance=logger, verbose=True)
    assert any("啟動清理器" in msg for _lvl, msg in logger.messages)
    assert any("已有活躍的清理器" in msg for _lvl, msg in logger.messages)

    class RaisingCleaner(DummyCleaner):
        def __init__(self, **kwargs: Any) -> None:
            raise RuntimeError("boom")

    monkeypatch.setattr(creator, "LoggerCleaner", RaisingCleaner)
    creator._start_cleaner_for_path(str(tmp_path / "x"), logger_instance=logger, verbose=False)
    assert any("無法為路徑" in msg for _lvl, msg in logger.messages if _lvl == "error")

    class StopRaisingCleaner(DummyCleaner):
        def stop(self) -> None:
            raise RuntimeError("boom-stop")

    monkeypatch.setattr(
        creator,
        "_active_cleaners",
        {
            str((tmp_path / "a").resolve()): StopRaisingCleaner(),
            str((tmp_path / "b").resolve()): DummyCleaner(),
        },
    )
    with pytest.warns(UserWarning):
        creator._stop_all_cleaners()
    assert creator._active_cleaners == {}

    ok_cleaner = DummyCleaner()
    bad_cleaner = StopRaisingCleaner()
    monkeypatch.setattr(
        creator,
        "_active_cleaners",
        {
            str((tmp_path / "c").resolve()): ok_cleaner,
            str((tmp_path / "d").resolve()): bad_cleaner,
        },
    )
    creator._stop_cleaner_for_path("")
    creator._stop_cleaner_for_path(str(tmp_path / "c"), logger_instance=logger, verbose=True)
    assert ok_cleaner.stopped is True
    creator._stop_cleaner_for_path(str(tmp_path / "d"), logger_instance=logger, verbose=True)
    assert any("停止路徑" in msg for _lvl, msg in logger.messages if _lvl == "error")

    calls: list[str] = []
    monkeypatch.setattr(creator, "_stop_cleaner_for_path", lambda *a, **k: calls.append("stop"))
    monkeypatch.setattr(creator, "_start_cleaner_for_path", lambda *a, **k: calls.append("start"))
    creator._restart_cleaner_for_path("x", logger_instance=logger)
    assert calls == ["stop", "start"]


def test_create_logger_name_inference_branches(monkeypatch: pytest.MonkeyPatch, tmp_path):
    import pretty_loguru.factory.creator as creator

    def make_frame(globals_: dict[str, Any]):
        return SimpleNamespace(f_back=SimpleNamespace(f_globals=globals_))

    monkeypatch.setattr(
        creator.inspect,
        "currentframe",
        lambda: make_frame({"__file__": str(tmp_path / "app.py"), "__name__": "x"}),
    )
    logger1 = creator.create_logger(None, enable_addons=False)
    assert creator.get_logger("app") is logger1

    monkeypatch.setattr(
        creator.inspect,
        "currentframe",
        lambda: make_frame({"__name__": "pkg.mod"}),
    )
    logger2 = creator.create_logger(None, enable_addons=False, force_new_instance=True)
    assert creator.get_logger("pkg.mod") is logger2

    monkeypatch.setattr(
        creator.inspect,
        "currentframe",
        lambda: make_frame({"__name__": "__main__"}),
    )
    logger3 = creator.create_logger(None, enable_addons=False, force_new_instance=True)
    assert creator.get_logger("interactive") is logger3


def test_create_logger_unknown_preset_warns(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.creator as creator

    with pytest.warns(UserWarning):
        logger = creator.create_logger("unknown_preset", preset="__nope__", enable_addons=False)
    assert logger is not None


def test_creator_registry_wrapper_functions():
    import pretty_loguru.factory.creator as creator

    dummy = object()
    creator.set_logger("x", dummy)  # type: ignore[arg-type]
    assert creator.get_logger("x") is dummy  # type: ignore[comparison-overlap]
    assert "x" in creator.list_loggers()
    assert creator.unregister_logger("x") is True


def test_reinit_logger_warns_when_logger_missing():
    import pretty_loguru.factory.creator as creator

    with pytest.warns(UserWarning):
        assert creator.reinit_logger("missing") is None


def test_reinit_logger_unknown_preset_and_update_paths(monkeypatch: pytest.MonkeyPatch, tmp_path):
    import pretty_loguru.factory.creator as creator
    import pretty_loguru.factory.updater as updater

    creator.create_logger("svc", enable_addons=False)

    monkeypatch.setattr(updater, "update_logger_config", lambda *a, **k: True)
    with pytest.warns(UserWarning):
        updated = creator.reinit_logger("svc", preset="__nope__")
    assert updated is not None

    monkeypatch.setattr(updater, "update_logger_config", lambda *a, **k: False)
    with pytest.warns(UserWarning):
        assert creator.reinit_logger("svc") is None

    called: dict[str, Any] = {}
    monkeypatch.setattr(updater, "update_logger_config", lambda *a, **k: True)
    monkeypatch.setattr(creator, "_restart_cleaner_for_path", lambda path, **k: called.setdefault("path", path))
    creator.reinit_logger("svc", log_dir=str(tmp_path), start_cleaner=True)
    assert "path" in called


def test_default_logger_lazy_init(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.creator as creator

    monkeypatch.setattr(creator, "_default_logger_instance", None)

    created: list[str] = []

    def fake_create(name: str, **kwargs: Any):
        created.append(name)
        return object()

    monkeypatch.setattr(creator, "create_logger", fake_create)
    a = creator.default_logger()
    b = creator.default_logger()
    assert a is b
    assert created == ["default_service"]


def test_get_preset_unknown_fallback_warns():
    import pretty_loguru.factory.creator as creator

    with pytest.warns(UserWarning):
        cfg = creator._get_preset("__nope__")
    assert isinstance(cfg, dict)
    assert cfg


def test_cleanup_loggers_handles_missing_and_remove_errors(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.creator as creator

    class BadLogger:
        def remove(self, *a: Any, **k: Any) -> None:
            raise RuntimeError("boom")

    monkeypatch.setattr(creator, "_stop_all_cleaners", lambda: None)
    monkeypatch.setattr(creator.registry, "list_loggers", lambda: ["a", "b"])
    monkeypatch.setattr(creator.registry, "get_logger", lambda name: None if name == "a" else BadLogger())
    monkeypatch.setattr(creator.registry, "clear_registry", lambda: 2)

    assert creator.cleanup_loggers() == 2
