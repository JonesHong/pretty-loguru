# 簡單用法

這是使用 pretty-loguru 的最小範例，展示如何快速開始記錄日誌（console + file）。

## 💻 最簡單的開始

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="simple_demo",
    log_dir="logs/simple_demo",  # 注意：log_dir 是「目錄」
    level="INFO",
)

logger.debug("debug")
logger.info("info")
logger.success("success")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```

## 🎯 每筆訊息控制輸出去向（console/file）

使用 `log_to_targets()` 做最直覺的 routing：

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets_demo", log_dir="logs/targets_demo", level="INFO")

log_to_targets(logger, "both (default)", level="INFO")
log_to_targets(logger, "console only", level="INFO", console_only=True)
log_to_targets(logger, "file only", level="INFO", file_only=True)
```

## 📦 想接 ELK/Loki（建議）

- ELK：`serialize=True`（JSON 檔案）+ Filebeat/Fluent Bit
- Loki：建議 Promtail/Grafana Agent；或 `loki_enabled=True` 直推（best-effort：不重試、無離線緩衝、無 backpressure；失敗即丟棄）

```python
from pretty_loguru import create_logger

logger = create_logger(
    "json_demo",
    log_dir="logs/json_demo",
    level="INFO",
    serialize=True,
)
logger.info("hello", user_id=123)
```

