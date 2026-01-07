from __future__ import annotations

import importlib
import sys
from contextlib import contextmanager
from types import ModuleType

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


def test_formats_init_importerror_branch(monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.formats as formats

    # 強制 pyfiglet import 失敗，覆蓋 except ImportError 分支
    saved = {k: v for k, v in list(sys.modules.items()) if k == "pyfiglet" or k.startswith("pyfiglet.")}
    for k in saved:
        sys.modules.pop(k, None)

    with _block_import("pyfiglet"):
        importlib.reload(formats)
        assert formats.has_figlet() is False

    # restore
    sys.modules.update(saved)
    importlib.reload(formats)


def test_formats_init_figlet_import_exception_branch(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch):
    import pretty_loguru.formats as formats

    # 模擬 `from .figlet import ...` 失敗，覆蓋 except Exception 分支（57-59）
    dummy = ModuleType("pretty_loguru.formats.figlet")
    sys.modules["pretty_loguru.formats.figlet"] = dummy

    with pytest.warns(UserWarning, match="Failed to initialize FIGlet features"):
        formats = importlib.reload(formats)
        assert formats.has_figlet() is False

    # restore：刪除 dummy，重新載入讓 module 回到正常狀態
    monkeypatch.delitem(sys.modules, "pretty_loguru.formats.figlet", raising=False)
    importlib.reload(formats)
