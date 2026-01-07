# 目標導向日誌（Target Logging）

有些訊息你希望「只在控制台看得到」（例如開發除錯），有些則希望「只寫入檔案」（例如稽核）。

pretty-loguru 提供 `log_to_targets()` 來做到「每則訊息選擇輸出目的地」。

## ✅ 使用 `log_to_targets()`

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets", log_dir="logs/targets", level="INFO")

log_to_targets(logger, "同時輸出", level="INFO")
log_to_targets(logger, "只到控制台", level="INFO", console_only=True)
log_to_targets(logger, "只到檔案", level="INFO", file_only=True)
```

## ✅ 建議用法

建議統一使用 `log_to_targets()` 來做「每則訊息選擇輸出目的地」（單一且明確的 API）。
