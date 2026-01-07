"""
Grafana Loki 整合模組（直接 Push）

設計目標（使用層面）：
- 以 LoggerConfig 開關啟用，不影響現有使用方式
- 預設送出 JSON line（loguru serialize=True），方便在 Grafana 端解析/查詢
- 批次送出降低 HTTP 開銷；失敗時不中斷主流程（best-effort：失敗即丟棄，不重試）

注意：
- 生產環境更建議使用 promtail 讀取檔案再送 Loki（更穩定、可離線緩衝）
  但此模組提供「程式內直推」的選項，適合簡單場景或無法部署 agent 的環境。
- 此模組不提供離線緩衝/重試/backpressure 控制；若你需要可靠性，請優先採用 agent 方式。
"""

from __future__ import annotations

import atexit
import base64
import json
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from urllib.request import Request, urlopen


def _normalize_loki_push_url(url: str) -> str:
    """將 base URL 正規化成 Loki push endpoint（`/loki/api/v1/push`）。"""
    u = url.strip()
    if not u:
        raise ValueError("loki_base_url is empty")
    if u.endswith("/"):
        u = u[:-1]
    if u.endswith("/loki/api/v1/push"):
        return u
    return u + "/loki/api/v1/push"


@dataclass
class LokiSinkConfig:
    """
    Loki sink 設定（直推 / best-effort）。

    注意：此設定不提供重試、離線緩衝、或 backpressure 控制；失敗會被吞掉以避免影響主流程。
    """
    url: str
    labels: Dict[str, str] = field(default_factory=dict)
    batch_size: int = 50
    flush_interval_seconds: float = 1.0
    timeout_seconds: float = 2.0
    tenant_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)


class LokiSink:
    """
    Loguru sink：將 log line 推送到 Loki。

    - 建議搭配 logger.add(..., serialize=True, enqueue=True) 使用。
    - 本 sink 會盡量不拋出例外以免影響主流程。
    """

    def __init__(self, config: LokiSinkConfig) -> None:
        """
        建立 Loki sink。

        使用者通常不需要直接呼叫，請使用 `create_loki_sink(...)`。
        """
        self._url = _normalize_loki_push_url(config.url)
        self._labels = dict(config.labels or {})
        self._batch_size = max(int(config.batch_size), 1)
        self._flush_interval = max(float(config.flush_interval_seconds), 0.0)
        self._timeout = max(float(config.timeout_seconds), 0.1)
        self._tenant_id = config.tenant_id
        self._username = config.username
        self._password = config.password
        self._headers = dict(config.headers or {})

        self._lock = threading.Lock()
        self._values: List[Tuple[str, str]] = []
        self._last_flush = time.time()
        self._closed = False

        atexit.register(self.close)

    def __call__(self, message: Any) -> None:
        """
        Loguru sink entrypoint：接收一筆 message 並加入緩衝，必要時觸發 flush。

        注意：任何例外都會被吞掉（best-effort）。
        """
        if self._closed:
            return

        try:
            record = getattr(message, "record", None) or {}
            record_time = record.get("time")
            if record_time is not None:
                ts_ns = int(record_time.timestamp() * 1_000_000_000)
            else:
                ts_ns = int(time.time() * 1_000_000_000)

            line = str(message)  # serialize=True 時會是 JSON（含 text/record）
            ts_str = str(ts_ns)

            should_flush = False
            with self._lock:
                self._values.append((ts_str, line))
                if len(self._values) >= self._batch_size:
                    should_flush = True
                elif self._flush_interval > 0 and (time.time() - self._last_flush) >= self._flush_interval:
                    should_flush = True

            if should_flush:
                self.flush()
        except Exception:
            # sink 內部錯誤不應影響主流程
            return

    def flush(self) -> None:
        """
        立即送出目前緩衝的 log lines。

        - 若沒有任何待送出內容則直接返回。
        - 送出失敗會被吞掉（best-effort）。
        """
        if self._closed:
            return

        with self._lock:
            if not self._values:
                self._last_flush = time.time()
                return
            values = self._values
            self._values = []
            self._last_flush = time.time()

        payload = {
            "streams": [
                {
                    "stream": self._labels,
                    "values": values,
                }
            ]
        }

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "pretty-loguru-loki-sink",
            **self._headers,
        }

        if self._tenant_id:
            headers["X-Scope-OrgID"] = self._tenant_id

        if self._username and self._password:
            token = base64.b64encode(f"{self._username}:{self._password}".encode("utf-8")).decode("ascii")
            headers["Authorization"] = f"Basic {token}"

        req = Request(self._url, data=body, headers=headers, method="POST")
        try:
            with urlopen(req, timeout=self._timeout) as resp:
                # 204/200 都算成功；其他不拋例外也不重試（KISS）
                _ = resp.read()
        except Exception:
            # 不中斷主流程：掉了就掉了（生產建議用 promtail）
            return

    def close(self) -> None:
        """
        關閉 sink 並嘗試做最後一次 flush。

        重複呼叫是安全的；任何例外都會被吞掉（best-effort）。
        """
        if self._closed:
            return
        self._closed = True
        try:
            self.flush()
        except Exception:
            return


def create_loki_sink(
    url: str,
    labels: Optional[Dict[str, str]] = None,
    batch_size: int = 50,
    flush_interval_seconds: float = 1.0,
    timeout_seconds: float = 2.0,
    tenant_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
) -> LokiSink:
    """
    建立可直接傳給 `logger.add(...)` 的 Loki sink。

    Args:
        url: Loki base URL 或 push endpoint（會自動補成 `/loki/api/v1/push`）。
        labels: Loki stream labels。
        batch_size: 累積到多少筆後 flush。
        flush_interval_seconds: 距離上次 flush 超過此秒數也會 flush（0 表示不靠時間觸發）。
        timeout_seconds: HTTP timeout（秒）。
        tenant_id: 多租戶 header（`X-Scope-OrgID`）。
        username: Basic auth username（可選）。
        password: Basic auth password（可選）。
        headers: 額外 HTTP headers（可選）。

    Returns:
        `LokiSink` callable（可作為 loguru sink）。
    """
    return LokiSink(
        LokiSinkConfig(
            url=url,
            labels=labels or {},
            batch_size=batch_size,
            flush_interval_seconds=flush_interval_seconds,
            timeout_seconds=timeout_seconds,
            tenant_id=tenant_id,
            username=username,
            password=password,
            headers=headers or {},
        )
    )
