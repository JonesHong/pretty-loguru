from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from pretty_loguru.core.base import configure_logger
from pretty_loguru.core.config import LoggerConfig


class FakeLogger:
    def __init__(self) -> None:
        self._core = object()
        self.add_calls: list[tuple[Any, dict[str, Any]]] = []
        self.remove_calls: list[Any] = []
        self.messages: list[tuple[str, str]] = []
        self._next_handler_id = 1

    def add(self, sink: Any, **kwargs: Any) -> int:
        self.add_calls.append((sink, dict(kwargs)))
        handler_id = self._next_handler_id
        self._next_handler_id += 1
        return handler_id

    def remove(self, handler_id: Any = None) -> None:
        self.remove_calls.append(handler_id)

    def info(self, msg: str) -> None:
        self.messages.append(("info", msg))

    def debug(self, msg: str) -> None:
        self.messages.append(("debug", msg))


def test_configure_logger_clone_failure_falls_back(monkeypatch: pytest.MonkeyPatch):
    logger = FakeLogger()
    config = LoggerConfig(name="svc", strict_validation=False)
    monkeypatch.setattr(config, "clone", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    configure_logger(logger, config)
    assert getattr(logger, "_pretty_loguru_config") is config


def test_configure_logger_remove_managed_handler_warns(monkeypatch: pytest.MonkeyPatch):
    logger = FakeLogger()
    setattr(logger, "_pretty_loguru_managed_handler_ids", [123])

    def raising_remove(_handler_id: Any = None) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(logger, "remove", raising_remove)
    config = LoggerConfig(name="svc", strict_validation=False)
    with pytest.warns(UserWarning):
        configure_logger(logger, config)


def test_configure_logger_log_dir_validation_errors(tmp_path: Path):
    logger = FakeLogger()
    file_path = tmp_path / "not_a_dir.log"
    file_path.write_text("x", encoding="utf-8")
    config = LoggerConfig(name="svc", log_dir=file_path, strict_validation=False)
    with pytest.raises(ValueError):
        configure_logger(logger, config)


def test_configure_logger_file_paths_and_compression_warnings(tmp_path: Path):
    logger = FakeLogger()
    log_dir = tmp_path / "logs"

    config_true = LoggerConfig(
        name="svc",
        log_dir=log_dir,
        use_native_format=True,
        compression=True,
        verbose=True,
        strict_validation=False,
    )
    with pytest.warns(DeprecationWarning):
        configure_logger(logger, config_true)

    file_sink, file_kwargs = logger.add_calls[2]
    assert isinstance(file_sink, str)
    assert file_sink.endswith("svc.log")
    assert file_kwargs["compression"] == "gz"

    logger2 = FakeLogger()
    config_false = replace(config_true, compression=False, name="svc2")
    with pytest.warns(DeprecationWarning):
        configure_logger(logger2, config_false)
    _, file_kwargs2 = logger2.add_calls[2]
    assert "compression" not in file_kwargs2 or file_kwargs2["compression"] is None


def test_configure_logger_custom_compression_format_overrides(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.core.presets as presets

    logger = FakeLogger()
    log_dir = tmp_path / "logs"

    sentinel = object()
    monkeypatch.setattr(presets, "create_custom_compression_function", lambda _fmt: sentinel)
    config = LoggerConfig(
        name="svc",
        log_dir=log_dir,
        compression="gz",
        compression_format="[{time}]_{file}",
        serialize=True,
        strict_validation=False,
    )
    configure_logger(logger, config)

    _, file_kwargs = logger.add_calls[2]
    assert file_kwargs["compression"] is sentinel
    assert file_kwargs["serialize"] is True


def test_pretty_console_sink_branches(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path):
    import pretty_loguru.core.base as base
    import pretty_loguru.core.pretty_event as pretty_event

    logger = FakeLogger()
    config = LoggerConfig(name="svc", log_dir=None, strict_validation=False)
    configure_logger(logger, config)

    pretty_sink = logger.add_calls[1][0]
    assert callable(pretty_sink)

    class Message:
        def __init__(self, record: dict[str, Any], text: str = "HEADER\n") -> None:
            self.record = record
            self._text = text

        def __str__(self) -> str:
            return self._text

    pretty_sink(Message({"extra": {}}))
    assert "HEADER" in capsys.readouterr().err

    class StubConsole:
        def __init__(self) -> None:
            self.print_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

        def print(self, *args: Any, **kwargs: Any) -> None:
            self.print_calls.append((args, kwargs))

    stub_console = StubConsole()
    monkeypatch.setattr(base, "get_console", lambda: stub_console)
    monkeypatch.setattr(pretty_event, "validate_pretty_payload", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))

    pretty_sink(
        Message(
            {
                "extra": {
                    "pretty_kind": "x",
                    "pretty_payload": {"title": "t", "version": 1},
                    "pretty_text": "FALLBACK",
                }
            }
        )
    )
    assert stub_console.print_calls
    assert stub_console.print_calls[-1][0][0] == "FALLBACK"
    assert stub_console.print_calls[-1][1].get("markup") is False

    class MessageBadRecord:
        @property
        def record(self) -> Any:
            raise RuntimeError("boom")

        def __str__(self) -> str:
            return "HEADER2\n"

    pretty_sink(MessageBadRecord())
    assert "HEADER2" in capsys.readouterr().err


def test_configure_logger_loki_enabled_adds_sink(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.core.base as base

    logger = FakeLogger()
    seen: dict[str, Any] = {}
    sentinel_sink = object()

    def fake_create_loki_sink(**kwargs: Any) -> Any:
        seen.update(kwargs)
        return sentinel_sink

    monkeypatch.setattr(base, "get_console", lambda: None)
    monkeypatch.setattr("pretty_loguru.integrations.loki.create_loki_sink", fake_create_loki_sink)

    config = LoggerConfig(
        name="svc",
        component_name="comp",
        loki_enabled=True,
        loki_base_url="http://127.0.0.1:3100",
        strict_validation=False,
    )
    configure_logger(logger, config)

    loki_sink, loki_kwargs = logger.add_calls[-1]
    assert loki_sink is sentinel_sink
    assert loki_kwargs["format"] == "{message}"
    assert loki_kwargs["serialize"] is True
    assert seen["labels"]["logger"] == "svc"
    assert seen["labels"]["component"] == "comp"

