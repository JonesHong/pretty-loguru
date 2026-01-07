import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from pretty_loguru.core.presets import get_preset_config
from pretty_loguru.integrations.loki import _normalize_loki_push_url, create_loki_sink


def test_daily_preset_name_format_and_compression(tmp_path: Path):
    conf = get_preset_config("daily")
    assert conf["name_format"] == "[{component_name}]daily_latest.temp.log"

    original = tmp_path / "[my_app]daily_latest.temp.log"
    original.write_text("x", encoding="utf-8")

    # 模擬「歸檔檔名」已存在時會自動加上序號
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    expected_base = tmp_path / f"[my_app]{yesterday}.log"
    expected_base.write_text("occupied", encoding="utf-8")

    new_path_str = conf["compression"](str(original))
    new_path = Path(new_path_str)

    assert original.exists() is False
    assert new_path.exists() is True
    assert new_path.name == f"[my_app]{yesterday}.1.log"


def test_normalize_loki_push_url():
    with pytest.raises(ValueError):
        _normalize_loki_push_url("   ")
    assert _normalize_loki_push_url("http://localhost:3100") == "http://localhost:3100/loki/api/v1/push"
    assert _normalize_loki_push_url("http://localhost:3100/") == "http://localhost:3100/loki/api/v1/push"
    assert (
        _normalize_loki_push_url("http://localhost:3100/loki/api/v1/push")
        == "http://localhost:3100/loki/api/v1/push"
    )


def test_loki_sink_builds_request_and_payload(monkeypatch):
    captured = {}

    def fake_urlopen(req, timeout=None):
        captured["url"] = req.full_url
        captured["timeout"] = timeout
        captured["data"] = req.data
        captured["headers"] = dict(req.headers)

        class Resp:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b""

        return Resp()

    # loki.py 是 `from urllib.request import Request, urlopen`，所以 patch module-level 名稱
    monkeypatch.setattr("pretty_loguru.integrations.loki.urlopen", fake_urlopen)

    sink = create_loki_sink(
        url="http://localhost:3100",
        labels={"service": "svc"},
        batch_size=1,  # 立即 flush
        flush_interval_seconds=999,
        timeout_seconds=1.5,
        tenant_id="t1",
        username="u",
        password="p",
        headers={"X-Custom": "1"},
    )

    record_time = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    class Msg:
        record = {"time": record_time}

        def __str__(self) -> str:
            return '{"hello":"world"}'

    sink(Msg())

    assert captured["url"].endswith("/loki/api/v1/push")
    assert captured["timeout"] == 1.5

    headers = {k.lower(): v for k, v in captured["headers"].items()}
    assert headers["content-type"] == "application/json"
    assert headers["x-scope-orgid"] == "t1"
    assert headers["x-custom"] == "1"
    assert "authorization" in headers

    payload = json.loads(captured["data"].decode("utf-8"))
    assert payload["streams"][0]["stream"] == {"service": "svc"}

    values = payload["streams"][0]["values"]
    assert len(values) == 1

    expected_ts_ns = int(record_time.timestamp() * 1_000_000_000)
    assert values[0][0] == str(expected_ts_ns)
    assert values[0][1] == '{"hello":"world"}'


def test_loki_sink_is_best_effort_on_network_error(monkeypatch):
    def raising_urlopen(req, timeout=None):
        raise RuntimeError("boom")

    monkeypatch.setattr("pretty_loguru.integrations.loki.urlopen", raising_urlopen)
    sink = create_loki_sink(url="http://localhost:3100", batch_size=1, flush_interval_seconds=999)

    class Msg:
        record = {"time": datetime.now(timezone.utc)}

        def __str__(self) -> str:
            return "x"

    # best-effort：不應往外拋出例外
    sink(Msg())


def test_loki_sink_close_and_empty_flush_paths(monkeypatch):
    # 不需要真的打網路：讓 urlopen 永遠成功
    def fake_urlopen(req, timeout=None):
        class Resp:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b""

        return Resp()

    monkeypatch.setattr("pretty_loguru.integrations.loki.urlopen", fake_urlopen)

    sink = create_loki_sink(url="http://localhost:3100", batch_size=999, flush_interval_seconds=999)

    # 空 flush 分支
    sink.flush()

    class Msg:
        record = {}  # no time -> uses time.time branch

        def __str__(self) -> str:
            return "x"

    # close 後 __call__ 應直接 return（不拋錯）
    sink.close()
    sink(Msg())
    sink.close()  # 重複 close 也要安全
