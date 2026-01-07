# Target Logging

Sometimes you want a message to go to console only (developer-facing), or file only (audit/forensics).

pretty-loguru provides `log_to_targets()` to route messages per target.

## ✅ `log_to_targets()`

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets", log_dir="logs/targets", level="INFO")

log_to_targets(logger, "both", level="INFO")
log_to_targets(logger, "console only", level="INFO", console_only=True)
log_to_targets(logger, "file only", level="INFO", file_only=True)
```

## ✅ Recommended

Use `log_to_targets()` for per-message routing (single, explicit API).
