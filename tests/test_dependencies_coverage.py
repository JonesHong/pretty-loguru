from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from pretty_loguru.utils import dependencies


def test_ensure_pyfiglet_dependency_success_branch():
    assert dependencies.ensure_pyfiglet_dependency() is True


def test_check_availability_import_error_branches(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(dependencies, "art", lambda: (_ for _ in ()).throw(ImportError("no art")))
    assert dependencies.check_art_availability() is False

    monkeypatch.setattr(dependencies, "pyfiglet", lambda: (_ for _ in ()).throw(ImportError("no pyfiglet")))
    assert dependencies.check_pyfiglet_availability() is False

