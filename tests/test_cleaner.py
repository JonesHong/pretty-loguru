import os
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from pretty_loguru.core.cleaner import LoggerCleaner


def _touch(path: Path, *, mtime: datetime) -> None:
    path.write_text("x", encoding="utf-8")
    ts = mtime.timestamp()
    os.utime(path, (ts, ts))


def test_parse_retention_accepts_int_days():
    cleaner = LoggerCleaner(log_retention=7, log_dir=".")
    assert cleaner.retention_delta == timedelta(days=7)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("10 days", timedelta(days=10)),
        ("1 week", timedelta(weeks=1)),
        ("2 months", timedelta(days=61)),  # 30.5 * 2
        ("1 year", timedelta(days=365.25)),
        ("30 seconds", timedelta(seconds=30)),
        ("15 minutes", timedelta(minutes=15)),
        ("2 hours", timedelta(hours=2)),
    ],
)
def test_parse_retention_accepts_string_units(value, expected):
    cleaner = LoggerCleaner(log_retention=value, log_dir=".")
    assert cleaner.retention_delta == expected


def test_parse_retention_rejects_invalid_format():
    cleaner = LoggerCleaner(log_retention="30 days", log_dir=".")
    with pytest.raises(ValueError):
        cleaner._parse_retention("days 30")


def test_should_consider_file_include_exclude(tmp_path: Path):
    cleaner = LoggerCleaner(
        log_retention="30 days",
        log_dir=tmp_path,
        include_patterns=["*.log"],
        exclude_patterns=["*.tmp.log"],
    )
    assert cleaner._should_consider_file(tmp_path / "a.log") is True
    assert cleaner._should_consider_file(tmp_path / "a.txt") is False
    assert cleaner._should_consider_file(tmp_path / "a.tmp.log") is False


def test_clean_old_logs_deletes_expired_files(tmp_path: Path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    old_log = log_dir / "old.log"
    recent_log = log_dir / "recent.log"
    hidden_log = log_dir / ".hidden.log"
    ignored_tmp = log_dir / "ignore.tmp"

    now = datetime.now()
    _touch(old_log, mtime=now - timedelta(days=2))
    _touch(recent_log, mtime=now)
    _touch(hidden_log, mtime=now - timedelta(days=2))
    _touch(ignored_tmp, mtime=now - timedelta(days=2))

    cleaner = LoggerCleaner(
        log_retention="1 day",
        log_dir=log_dir,
        recursive=False,
        include_patterns=["*.log"],
    )
    cleaner._clean_old_logs()

    assert old_log.exists() is False
    assert recent_log.exists() is True
    assert hidden_log.exists() is True  # 隱藏檔案一律略過
    assert ignored_tmp.exists() is True  # include_patterns 限制只處理 *.log


def test_clean_old_logs_creates_directory_when_missing(tmp_path: Path):
    missing = tmp_path / "missing_logs_dir"
    cleaner = LoggerCleaner(log_retention="1 day", log_dir=missing)
    assert missing.exists() is False
    cleaner._clean_old_logs()
    assert missing.exists() is True

