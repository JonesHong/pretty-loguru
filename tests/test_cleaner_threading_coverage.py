from __future__ import annotations

import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pretty_loguru.core.cleaner import LoggerCleaner


def _touch(path: Path, *, mtime: datetime) -> None:
    path.write_text("x", encoding="utf-8")
    ts = mtime.timestamp()
    os.utime(path, (ts, ts))


def test_cleaner_invalid_retention_falls_back_and_logs_warning(tmp_path: Path):
    mock_logger = MagicMock()
    cleaner = LoggerCleaner(log_retention="not a retention", log_dir=tmp_path, logger_instance=mock_logger)
    assert cleaner.retention_str == "30 days"
    mock_logger.warning.assert_called()


def test_cleaner_start_stop_and_already_running(tmp_path: Path):
    mock_logger = MagicMock()
    cleaner = LoggerCleaner(log_retention="1 day", log_dir=tmp_path, logger_instance=mock_logger, check_interval=0.01)

    cleaner.start()
    assert cleaner._is_running is True

    # 已在運行中分支
    cleaner.start()
    assert cleaner._is_running is True

    cleaner.stop()
    assert cleaner._is_running is False


def test_cleaner_loop_handles_exceptions(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    # 沒有 logger，verbose=True 時會走 print() 分支，方便驗證
    cleaner = LoggerCleaner(log_retention="1 day", log_dir=tmp_path, logger_instance=None, verbose=True, check_interval=0.01)

    def boom():
        raise RuntimeError("boom")

    cleaner._clean_old_logs = boom  # type: ignore[method-assign]
    cleaner.start()
    time.sleep(0.05)
    cleaner.stop()

    out = capsys.readouterr().out
    assert "清理日誌時發生錯誤" in out


def test_cleaner_permission_error_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    old_log = log_dir / "old.log"
    _touch(old_log, mtime=datetime.now() - timedelta(days=10))

    mock_logger = MagicMock()
    cleaner = LoggerCleaner(log_retention="1 day", log_dir=log_dir, logger_instance=mock_logger, recursive=False, verbose=True)

    # 讓 unlink 產生 PermissionError，覆蓋 WARNING 分支
    monkeypatch.setattr(Path, "unlink", lambda self: (_ for _ in ()).throw(PermissionError("nope")))
    cleaner._clean_old_logs()

    assert mock_logger.warning.called

