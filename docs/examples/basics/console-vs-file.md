# 控制台 vs 檔案

pretty-loguru 的預設行為：

- 不指定 `log_dir`：只輸出到控制台（console-only）
- 指定 `log_dir`（目錄）：同時輸出到控制台 + 檔案

## 🖥️ 只輸出控制台

```python
from pretty_loguru import create_logger

logger = create_logger("console_demo", level="INFO")
logger.info("只會出現在控制台")
```

## 📁 輸出到檔案（同時保留控制台）

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="file_demo",
    log_dir="logs/file_demo",  # 注意：log_dir 是目錄
    level="INFO",
    rotation="100 MB",
    retention="14 days",
    compression="gz",
)
logger.info("會出現在控制台，也會寫入檔案")
```

## 🎯 每則訊息選擇輸出目標

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets_demo", log_dir="logs/targets_demo", level="INFO")

log_to_targets(logger, "同時輸出", level="INFO")
log_to_targets(logger, "只到控制台", level="INFO", console_only=True)
log_to_targets(logger, "只到檔案", level="INFO", file_only=True)
```
