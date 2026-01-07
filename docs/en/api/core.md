# Core Module API

This page documents the **latest** core contract of pretty-loguru.

## `LoggerConfig`

`LoggerConfig` is the canonical configuration object used by `create_logger(...)` and `LoggerConfig.apply_to(...)`.

Key idea: **one config can manage many loggers** — once attached, future `update(...)` calls stay synchronized.

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

### Common fields

- `level`: minimum log level
- `log_dir`: directory for log files (`None` means console-only)
- `rotation`, `retention`, `compression`, `compression_format`: loguru-style file rotation/retention/compression
- `format`, `component_name`, `subdirectory`: formatting and naming controls
- `serialize`: write JSON lines to file (recommended for ELK/Filebeat/Promtail)
- `loki_enabled` + `loki_*`: optional Loki direct push (best-effort; no retries/offline buffer/backpressure)

Notes:
- `name` is a legacy field (kept only for older configs); use `create_logger("name", ...)` instead.

### Updating config

`update(...)` uses explicit fields (IDE-friendly). For dynamic dict overrides (JSON/ENV), use `update_from_dict(...)`:

```python
config.update_from_dict({"level": "DEBUG", "serialize": True})
```

## `configure_logger(logger_instance, config, reset_handlers=False)`

Configures a loguru logger instance using a `LoggerConfig`.

By default, it only removes **pretty-loguru managed** handlers; pass `reset_handlers=True` to also remove sinks you added via that logger instance (`logger.add(...)`).

## Destination filters (console/file routing)

pretty-loguru routes per-message output using record extras:

- `to_console_only=True`: console only
- `to_file_only=True`: file only

Use the convenience helper:

```python
from pretty_loguru.addons import log_to_targets

log_to_targets(logger, "both")
log_to_targets(logger, "console only", console_only=True)
log_to_targets(logger, "file only", file_only=True)
```

