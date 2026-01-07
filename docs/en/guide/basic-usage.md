# Basic Usage

This page covers the core usage patterns of pretty-loguru.

## 🚀 Quick start

### Console-only logger (no files)

```python
from pretty_loguru import create_logger

logger = create_logger("my_app", level="INFO")
logger.info("Hello from pretty-loguru")
```

### File logging (log_dir is a directory)

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="my_app",
    level="INFO",
    log_dir="logs/my_app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
)
logger.success("File logging enabled")
```

## ✅ Semantic consistency (core contract)

- One API call emits **one Loguru event** (no side-channel `console.print(...)` inside logging methods).
- Console/file are different renderers of the **same event**.
- Pretty methods (e.g. `block/table/tree/...`) put `pretty_kind` + `pretty_payload` + `pretty_text` into `record["extra"]`.

## 🔁 Reinitializing an existing logger

Use `reinit_logger()` when you want to update the existing registered logger instance:

```python
from pretty_loguru import create_logger, reinit_logger

logger = create_logger("service", log_dir="logs/service", level="INFO")
reinit_logger("service", level="DEBUG", rotation="10 MB")
logger.debug("Now DEBUG is enabled")
```

By default (`reset_handlers=False`), pretty-loguru keeps sinks you added via `logger.add(...)`.  
Pass `reset_handlers=True` to remove those sinks as well (explicit choice).

## 🧩 Using LoggerConfig and templates

`LoggerConfig` is a reusable configuration template. `apply_to()` applies the config to named loggers and attaches them so future `update()` calls are synchronized.  
In the latest version, `create_if_missing=True` by default: missing loggers are created automatically.

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(level="INFO", log_dir="logs/app", rotation="00:00", retention="14 days")

create_logger("api", config=config)
create_logger("worker", config=config)
config.apply_to("api", "worker")

config.update(level="DEBUG")
```

Built-in templates:

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

prod = ConfigTemplates.production()
create_logger("my_app", config=prod)
prod.apply_to("my_app")
```

## 🎯 Console-only vs file-only per message

Use `log_to_targets()` to route specific messages:

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets", log_dir="logs/targets")

log_to_targets(logger, "This goes to both", level="INFO")
log_to_targets(logger, "Console only", level="INFO", console_only=True)
log_to_targets(logger, "File only", level="INFO", file_only=True)
```

## 📦 Shipping logs to ELK/Loki (recommended approach)

- ELK: set `serialize=True` and ship JSON logs via Filebeat/Fluent Bit
- Loki: ship via Promtail/Grafana Agent (or enable `loki_enabled=True` direct push; best-effort: no retries, no offline buffer, no backpressure; failures are dropped)

### Minimal examples

#### 1) Semantic consistency (pretty methods)

```python
from pretty_loguru import create_logger

logger = create_logger("demo", log_dir="logs/demo", level="INFO")

# One call -> one Loguru event
logger.block("BOOT", ["step=1", "step=2"])
logger.table("Users", [{"name": "Alice", "age": 30}])
```

#### 2) JSON file logs (ELK/Filebeat)

```python
from pretty_loguru import create_logger

logger = create_logger("json_demo", log_dir="logs/json_demo", level="INFO", serialize=True)
logger.block("STRUCTURED", ["this line is also inside record.extra.pretty_text"])
```

#### 3) Loki direct push (optional)

```python
from pretty_loguru import create_logger

logger = create_logger(
    "loki_demo",
    log_dir="logs/loki_demo",
    level="INFO",
    serialize=True,
    loki_enabled=True,
    loki_base_url="http://localhost:3100",
    loki_labels={"app": "loki_demo"},
)
logger.info("hello loki")
```
