from __future__ import annotations

import logging
from typing import Any

import pytest


def test_intercept_handler_uses_default_logger_when_none(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.integrations.uvicorn as uv
    import pretty_loguru.factory.creator as creator

    sentinel = object()
    monkeypatch.setattr(creator, "default_logger", lambda: sentinel)
    handler = uv.InterceptHandler()
    assert handler.logger is sentinel


def test_build_uvicorn_log_config_uses_default_logger_when_none(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.integrations.uvicorn as uv
    import pretty_loguru.factory.creator as creator

    sentinel = object()
    monkeypatch.setattr(creator, "default_logger", lambda: sentinel)

    cfg = uv.build_uvicorn_log_config()
    assert cfg["handlers"]["pretty_loguru_intercept"]["logger_instance"] is sentinel


def test_configure_uvicorn_logging_removes_handlers(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.integrations.uvicorn as uv
    import pretty_loguru.factory.creator as creator

    class DummyLogger:
        def __init__(self) -> None:
            self.debugs: list[str] = []

        def debug(self, msg: str) -> None:
            self.debugs.append(msg)

    dummy = DummyLogger()
    monkeypatch.setattr(creator, "default_logger", lambda: dummy)

    logger_name = "uvicorn.error"
    logging_logger = logging.getLogger(logger_name)
    dummy_handler = logging.StreamHandler()
    logging_logger.addHandler(dummy_handler)

    root = logging.getLogger()
    saved_root_handlers = list(root.handlers)
    saved_root_level = root.level
    saved = {}
    for n in ["uvicorn.asgi", "uvicorn.access", "uvicorn", "uvicorn.error"]:
        lg = logging.getLogger(n)
        saved[n] = (list(lg.handlers), lg.propagate, lg.level)

    try:
        uv._configure_uvicorn_logging(logger_instance=None, log_level="INFO")
        assert dummy.debugs
        assert dummy_handler not in logging_logger.handlers
    finally:
        root.handlers[:] = saved_root_handlers
        root.setLevel(saved_root_level)
        for n, (handlers, propagate, level) in saved.items():
            lg = logging.getLogger(n)
            lg.handlers[:] = handlers
            lg.propagate = propagate
            lg.setLevel(level)


def test_setup_uvicorn_logging_calls_integrate(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.integrations.uvicorn as uv
    import pretty_loguru.factory.creator as creator

    sentinel = object()
    monkeypatch.setattr(creator, "default_logger", lambda: sentinel)

    called: dict[str, Any] = {}

    def fake_integrate(logger_instance: Any, log_level: Any = None, **kwargs: Any):
        called["logger"] = logger_instance
        called["log_level"] = log_level

    monkeypatch.setattr(uv, "integrate_uvicorn", fake_integrate)
    uv.setup_uvicorn_logging()
    assert called["logger"] is sentinel


def test_integrate_uvicorn_monkeypatch_executes_patched_configure_logging(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.integrations.uvicorn as uv
    import uvicorn.config

    sentinel = object()
    calls: list[str] = []

    def fake_original(self) -> None:
        calls.append("original")

    def fake_configure(*args: Any, **kwargs: Any) -> None:
        calls.append("configure")

    original = uvicorn.config.Config.configure_logging
    had_attr = hasattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging")
    if had_attr:
        saved_attr = uvicorn.config.Config._pretty_loguru_original_configure_logging
    else:
        saved_attr = None

    try:
        monkeypatch.setattr(uv, "_configure_uvicorn_logging", fake_configure)
        monkeypatch.setattr(uvicorn.config.Config, "configure_logging", fake_original)
        if hasattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging"):
            delattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging")

        uv.integrate_uvicorn(logger=sentinel, monkeypatch=True)
        uvicorn.config.Config.configure_logging(object())
        assert calls == ["configure", "original", "configure"]
    finally:
        uvicorn.config.Config.configure_logging = original
        if had_attr:
            setattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging", saved_attr)
        else:
            if hasattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging"):
                delattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging")
