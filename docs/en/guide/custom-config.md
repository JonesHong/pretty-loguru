# Custom Configuration

This page shows how to customize pretty-loguru beyond the defaults.

## ✅ Prefer `LoggerConfig` for reusable configs

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(
    level="INFO",
    log_dir="logs/app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
    serialize=True,
)

logger = create_logger("my_app", config=config, component_name="my_app")
config.apply_to("my_app")
```

## 📦 JSON logs for ELK/Filebeat (recommended)

The simplest way is `serialize=True`:

```python
from pretty_loguru import create_logger

logger = create_logger(
    "json_app",
    log_dir="logs/json_app",
    serialize=True,
)
logger.info("structured message: user_id={user_id}", user_id=123)
```

## 🔧 Adding extra sinks (loguru-native)

pretty-loguru returns a loguru logger, so you can still call `logger.add(...)` to add extra sinks:

```python
from pretty_loguru import create_logger

logger = create_logger("app", log_dir="logs/app")

# Extra file (separate from pretty-loguru's managed file handler)
logger.add("logs/app/extra.log", level="WARNING")
```

Note: by default (`reset_handlers=False`), `reinit_logger()` only rebuilds pretty-loguru managed handlers and keeps sinks you added via `logger.add(...)`. Pass `reset_handlers=True` to remove those sinks too (explicit choice).

## 🧩 Loki direct push (optional)

This is a convenience option for simple setups where you cannot deploy an agent. It is **best-effort**:

- No retries
- No offline buffering
- No backpressure control
- Failures are silently dropped

```python
from pretty_loguru import create_logger

logger = create_logger(
    "loki_app",
    log_dir="logs/loki_app",
    serialize=True,
    loki_enabled=True,
    loki_base_url="http://localhost:3100",
    loki_labels={"app": "loki_app"},
)
logger.info("hello loki")
```
