# API Reference (Overview)

This page is a high-level overview of the public pretty-loguru API. For the latest full signature list, use the repository root `snapshot.md` as the source of truth.

## ✅ Key rule

- `log_dir` is a **directory** where log files are stored (not a file path)
- If `log_dir` is not set, you get console-only output (rotation/retention/compression won’t apply)

## 🚀 Core API

### `create_logger()`

Create (or fetch) a registered logger instance:

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="my_app",
    component_name="my_app",
    level="INFO",
    log_dir="logs/my_app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
)
```

**Parameter note:**

- `enable_addons` (default `True`): inject addons (targets / Rich / ASCII, etc.). Set to `False` if you want core-only behavior (or want to avoid importing Rich/art dependencies).

### `reinit_logger()`

Update an existing logger (keeps the same registered instance):

```python
from pretty_loguru import create_logger, reinit_logger

logger = create_logger("service", log_dir="logs/service", level="INFO")
reinit_logger("service", level="DEBUG", rotation="10 MB")
logger.debug("DEBUG enabled")
```

**Handler behavior (important):**

- Default (`reset_handlers=False`) only rebuilds pretty-loguru managed handlers, and keeps sinks you added via `logger.add(...)`
- Pass `reset_handlers=True` to also remove sinks added via that logger instance (explicit choice)

### Get/list/cleanup loggers

```python
from pretty_loguru import get_logger, list_loggers, cleanup_loggers

logger = get_logger("service")
names = list_loggers()
cleanup_loggers()
```

## 🧩 Configuration

### `LoggerConfig`

`apply_to()` applies the config to the named loggers and attaches them so future `update()` calls are synchronized.  
In the latest version, `create_if_missing=True` by default: missing loggers are created automatically. Set `create_if_missing=False` to require that loggers already exist.

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(level="INFO", log_dir="logs/app", rotation="00:00", retention="14 days")

create_logger("api", config=config)
create_logger("worker", config=config)
config.apply_to("api", "worker")

config.update(level="DEBUG")
```

### `ConfigTemplates`

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

prod = ConfigTemplates.production()
create_logger("my_app", config=prod)
prod.apply_to("my_app")
```

## 🎯 Target routing per message

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets", log_dir="logs/targets")
log_to_targets(logger, "both")
log_to_targets(logger, "console only", console_only=True)
log_to_targets(logger, "file only", file_only=True)
```

## 🔌 Integrations

- FastAPI: `pretty_loguru.integrations.fastapi.integrate_fastapi()` / `setup_fastapi_logging()` / `get_logger_dependency()`
- Uvicorn: `pretty_loguru.integrations.uvicorn.integrate_uvicorn()`

## 📦 ELK / Loki (observability)

- ELK: `serialize=True` (JSON logs) + Filebeat/Fluent Bit shipping
- Loki: prefer Promtail/Grafana Agent, or enable `loki_enabled=True` direct push (best-effort: no retries, no offline buffer, no backpressure; failures are dropped)
