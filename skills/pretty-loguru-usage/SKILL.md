---
name: pretty-loguru-usage
description: Implement and troubleshoot Python logging with pretty-loguru (Loguru + Rich). Use when you need to set up application logging, configure console/file outputs (rotation/retention/compression), enable/disable addons (pretty block/table/tree/panel/code/diff rendering), control per-message targets (console-only/file-only), manage multiple named loggers, push logs to Grafana Loki, or integrate with FastAPI/Uvicorn logging.
---

# Pretty Loguru Usage

## Workflow

1) Confirm requirements
- Ask whether they need console-only or file logging.
- Ask for rotation/retention expectations and whether JSON serialization is needed (ELK/Filebeat/Promtail).
- Ask whether Loki push is required (and whether agent-based shipping is acceptable).
- Ask whether they use FastAPI/Uvicorn and want to unify standard logging.

2) Prefer stable public API first
- Import from `pretty_loguru` for core usage: `create_logger`, `default_logger`, `reinit_logger`, `cleanup_loggers`, `LoggerConfig`.
- Use `pretty_loguru.addons` for optional “nice-to-have” helpers (targets, presets/templates, visual prints).

3) Create a logger (recommended)
- Use `create_logger(name, ...)` to create/register a named logger (shared loguru core; isolated by `logger_id` internally).
- Use `default_logger()` for a quick drop-in logger.
- Avoid binding custom `logger_id`: it is reserved and will be overwritten.

4) Configure outputs
- Console-only: leave `log_dir=None` (default).
- File logging: set `log_dir`, optionally `subdirectory`, `rotation`, `retention`, `compression` or `compression_format`.
- Set `serialize=True` when you want NDJSON-friendly file logs.
- Enable Loki push with `loki_enabled=True` and `loki_base_url=...` (best-effort; no retry/offline buffer).

5) Use addons (pretty render methods)
- Addons are enabled by default.
- Disable addons by:
  - `create_logger(..., enable_addons=False)`, or
  - setting env `PRETTY_LOGURU_ENABLE_ADDONS_DEFAULT=0/false/no` (global default).
- When enabled, the logger gains convenience methods like `block`, `table`, `tree`, `columns`, `panel`, `code`, `diff`, `render`, plus optional `figlet_*` if `pyfiglet` is installed.

6) Control per-message targets (single-event path)
- Prefer loguru-native flags (works with pretty-loguru filters):
  - console-only: `logger.opt(depth=1).bind(to_console_only=True).info("...")`
  - file-only: `logger.opt(depth=1).bind(to_file_only=True).info("...")`
- Or use helper: `pretty_loguru.addons.log_to_targets(logger, "...", console_only=True)` / `file_only=True`.

7) Update existing loggers carefully
- Use `reinit_logger(name, ...)` to reconfigure an existing logger.
- Treat unspecified parameters as “may revert to defaults” (pass a full configuration when you want to preserve file logging / retention / rotation).
- For “config + overrides” flows, prefer `create_logger(name, config=LoggerConfig(...), ...)` and use `clear_fields=[...]` when you must explicitly clear fields (set them to `None`).

## Examples

### Minimal console logger
```python
from pretty_loguru import create_logger

logger = create_logger("app")
logger.info("hello")
```

### File logging with rotation/retention + cleaner
```python
from pretty_loguru import create_logger

logger = create_logger(
    "app",
    log_dir="logs",
    rotation="20 MB",
    retention="30 days",
    compression="gz",
    start_cleaner=True,
)
logger.info("write to console + file")
```

### JSON-serialized file logs (ELK/Promtail-friendly)
```python
from pretty_loguru import create_logger

logger = create_logger("app", log_dir="logs/elk", serialize=True)
logger.info("this file sink becomes JSON lines")
```

### Pretty output (addons) + file-safe rendering
```python
from pretty_loguru import create_logger

logger = create_logger("app")  # addons enabled by default
logger.block("Startup", ["env=prod", "version=1.2.3"])
logger.table("metrics", [{"k": "cpu", "v": 0.7}, {"k": "mem", "v": 0.4}])
```

### Per-message target routing
```python
from pretty_loguru import create_logger

logger = create_logger("app", log_dir="logs")
logger.opt(depth=1).bind(to_console_only=True).info("console only")
logger.opt(depth=1).bind(to_file_only=True).info("file only")
```

### Loki push (best-effort)
```python
from pretty_loguru import create_logger

logger = create_logger(
    "app",
    loki_enabled=True,
    loki_base_url="http://localhost:3100",
    loki_labels={"service": "app"},
    serialize=True,
)
logger.info("pushed to loki (best-effort)")
```

### Uvicorn integration (non-monkeypatch)
```python
from pretty_loguru import default_logger
from pretty_loguru.integrations.uvicorn import build_uvicorn_log_config
import uvicorn

logger = default_logger()
log_config = build_uvicorn_log_config(logger_instance=logger, log_level="INFO")
uvicorn.run("app:app", log_config=log_config)
```

### FastAPI middleware
```python
from fastapi import FastAPI
from pretty_loguru.integrations.fastapi import LoggingMiddleware
from pretty_loguru import create_logger

app = FastAPI()
logger = create_logger("api", log_dir="logs/api")
app.add_middleware(LoggingMiddleware, logger_instance=logger)
```

## Guidelines

- Prefer `create_logger(..., config=LoggerConfig(...))` for reusable configs; pass overrides explicitly.
- Keep Loki labels low-cardinality (avoid user_id/request_id); put dynamic data in message/body fields instead.
- Use env `PRETTY_LOGURU_SKIP_REMOVE_DEFAULT_HANDLER=1` if you need to keep loguru’s default handler (otherwise pretty-loguru tries to remove handler id=0 on first use to avoid duplicate logs).
- Use env `PRETTY_LOGURU_WARNINGS_SUPPRESS=1` to silence warnings (or `PRETTY_LOGURU_WARNINGS_DEBUG=1` to route through `warnings.warn` for external filtering).
- When diagnosing handler state, inspect `pretty_loguru.core.diagnostics.get_handler_status()` and `get_cleaner_status()` during runtime.
