from __future__ import annotations

import importlib
import sys
from contextlib import contextmanager
from types import ModuleType
from typing import Any

import pytest


@contextmanager
def _block_import(prefix: str):
    from importlib.abc import MetaPathFinder
    from importlib.machinery import ModuleSpec

    class Blocker(MetaPathFinder):
        def find_spec(self, fullname: str, path, target=None) -> ModuleSpec | None:  # type: ignore[override]
            if fullname == prefix or fullname.startswith(prefix + "."):
                raise ImportError(f"blocked: {fullname}")
            return None

    blocker = Blocker()
    sys.meta_path.insert(0, blocker)
    try:
        yield
    finally:
        sys.meta_path = [x for x in sys.meta_path if x is not blocker]


class DummyLogger:
    def __init__(self) -> None:
        self.warnings: list[str] = []
        self.debugs: list[str] = []

    def warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def debug(self, msg: str) -> None:
        self.debugs.append(msg)


def test_add_format_methods_figlet_exception_warns(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.methods as methods
    import pretty_loguru.formats as formats

    monkeypatch.setattr(methods, "create_block_method", lambda *a, **k: None)
    monkeypatch.setattr(methods, "create_ascii_methods", lambda *a, **k: None)
    monkeypatch.setattr(formats, "create_rich_methods", lambda *a, **k: None)

    monkeypatch.setattr(methods, "has_figlet", lambda: True)
    monkeypatch.setattr(formats, "create_figlet_methods", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))

    logger = DummyLogger()
    methods.add_format_methods(logger)
    assert logger.warnings


def test_add_format_methods_figlet_unavailable_debug_branch(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.methods as methods
    import pretty_loguru.formats as formats

    monkeypatch.setattr(methods, "create_block_method", lambda *a, **k: None)
    monkeypatch.setattr(methods, "create_ascii_methods", lambda *a, **k: None)
    monkeypatch.setattr(formats, "create_rich_methods", lambda *a, **k: None)
    monkeypatch.setattr(methods, "has_figlet", lambda: False)

    logger = DummyLogger()
    methods.add_format_methods(logger)


def test_add_custom_methods_second_figlet_attempt_importerror(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.methods as methods

    monkeypatch.setattr(methods, "add_format_methods", lambda *a, **k: None)

    saved = {k: v for k, v in list(sys.modules.items()) if k == "pretty_loguru.formats.figlet" or k.startswith("pretty_loguru.formats.figlet.")}
    for k in saved:
        sys.modules.pop(k, None)

    with _block_import("pretty_loguru.formats.figlet"):
        logger = DummyLogger()
        methods.add_custom_methods(logger)

    sys.modules.update(saved)


def test_add_custom_methods_second_figlet_attempt_exception_warns(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.methods as methods

    monkeypatch.setattr(methods, "add_format_methods", lambda *a, **k: None)

    dummy = ModuleType("pretty_loguru.formats.figlet")

    def raising(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("boom")

    dummy.create_figlet_methods = raising  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "pretty_loguru.formats.figlet", dummy)

    logger = DummyLogger()
    methods.add_custom_methods(logger)
    assert logger.warnings


def test_install_bind_addons_injection_early_returns(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.methods as methods

    logger = DummyLogger()
    setattr(logger, "_pretty_loguru_bind_addons_installed", True)
    methods._install_bind_addons_injection(logger, None)

    logger2 = DummyLogger()
    setattr(logger2, "bind", None)
    methods._install_bind_addons_injection(logger2, None)


def test_install_bind_addons_injection_wrapper_swallow_exceptions(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.factory.methods as methods

    child = DummyLogger()

    class Parent(DummyLogger):
        def bind(self, **kwargs: Any) -> Any:
            return child

    parent = Parent()
    monkeypatch.setattr(methods, "add_custom_methods", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    methods._install_bind_addons_injection(parent, None)
    assert parent.bind(x=1) is child
