from __future__ import annotations

import json
import subprocess
import sys


def _run(code: str) -> str:
    return subprocess.check_output([sys.executable, "-c", code], text=True).strip()


def test_import_pretty_loguru_does_not_import_formats():
    loaded = json.loads(
        _run(
            r"""
import json, sys
import pretty_loguru
mods = [m for m in sys.modules.keys() if m == "pretty_loguru.formats" or m.startswith("pretty_loguru.formats.")]
print(json.dumps(sorted(mods)))
"""
        )
    )
    assert loaded == []


def test_create_logger_without_addons_does_not_import_formats(tmp_path):
    tmp_path_str = str(tmp_path)
    loaded = json.loads(
        _run(
            rf"""
import json, sys
from pathlib import Path
from pretty_loguru import create_logger

tmp = Path({tmp_path_str!r})
create_logger("no_addons", log_dir=str(tmp/"logs"), enable_addons=False)
mods = [m for m in sys.modules.keys() if m == "pretty_loguru.formats" or m.startswith("pretty_loguru.formats.")]
print(json.dumps(sorted(mods)))
"""
        )
    )
    assert loaded == []
