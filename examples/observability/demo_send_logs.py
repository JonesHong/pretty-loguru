"""
Loki 直推示範程式。

用途：
- 用最小程式展示 `create_logger(..., serialize=True, loki_enabled=True, ...)` 的效果
- 適合用於本機環境快速驗證 Loki/Grafana 是否串通
"""

import time
import sys
from pathlib import Path

# 此檔案位於 examples/observability/，因此 repo root 在 parents[2]。
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pretty_loguru import create_logger


def main() -> None:
    """建立 logger 並送出數筆日誌到 Loki（best-effort）。"""
    logger = create_logger(
        "demo",
        log_dir="logs",
        serialize=True,
        loki_enabled=True,
        loki_base_url="http://localhost:3100",
        loki_labels={"app": "pretty-loguru-demo", "env": "local"},
        loki_batch_size=1,
        loki_timeout_seconds=1.0,
        verbose=True,
    )

    logger.bind(demo=True).info("Hello Loki from pretty-loguru")
    for i in range(3):
        logger.bind(i=i).info(f"demo log line {i}")
        time.sleep(0.2)

    if hasattr(logger, "complete"):
        logger.complete()


if __name__ == "__main__":
    main()
