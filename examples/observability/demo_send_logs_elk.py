"""
ELK（檔案收集）示範程式。

用途：
- 產生 JSON serialize 日誌到檔案，方便用 Filebeat / Logstash 收集
- 適合用於本機快速驗證 ELK pipeline 是否可解析 pretty-loguru 的 JSON
"""

import time
import sys
from pathlib import Path

# 此檔案位於 examples/observability/，因此 repo root 在 parents[2]。
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pretty_loguru import create_logger


def main() -> None:
    """建立 logger 並寫入數筆 JSON 日誌（供 ELK 收集）。"""
    log_dir = Path("logs") / "elk-demo"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = create_logger(
        "elk_demo",
        log_dir=log_dir,
        serialize=True,
        verbose=False,
    )

    logger.bind(demo=True, stack="elk").info("Hello ELK from pretty-loguru")
    for i in range(5):
        logger.bind(i=i).info("elk demo line")
        time.sleep(0.2)

    if hasattr(logger, "complete"):
        logger.complete()


if __name__ == "__main__":
    main()
