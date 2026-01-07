# Console vs File

pretty-loguru defaults:

- No `log_dir`: console-only
- With `log_dir` (directory): console + file

## 🖥️ Console-only

```python
from pretty_loguru import create_logger

logger = create_logger("console_demo", level="INFO")
logger.info("console only")
```

## 📁 File logging (and console)

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="file_demo",
    log_dir="logs/file_demo",  # log_dir is a directory
    level="INFO",
    rotation="100 MB",
    retention="14 days",
    compression="gz",
)
logger.info("this goes to both console and file")
```

## 🎯 Route per message

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets_demo", log_dir="logs/targets_demo", level="INFO")

log_to_targets(logger, "both", level="INFO")
log_to_targets(logger, "console only", level="INFO", console_only=True)
log_to_targets(logger, "file only", level="INFO", file_only=True)
```
