# FastAPI Integration

pretty-loguru provides ready-to-use helpers for FastAPI request/response logging and Uvicorn log unification.

## 🚀 Quick start (recommended)

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

app = FastAPI(title="My API")

logger = create_logger(
    name="api",
    component_name="my_api",
    log_dir="logs/api",
    level="INFO",
    rotation="50 MB",
    retention="30 days",
    serialize=True,
)

integrate_fastapi(app, logger, enable_uvicorn=True)
```

## 🧩 Dependency injection (per-route logger)

```python
from fastapi import FastAPI, Depends
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import get_logger_dependency

app = FastAPI()

logger = create_logger("api_route", log_dir="logs/api", level="INFO")
get_logger = get_logger_dependency(logger)

@app.get("/health")
def health(logger=Depends(get_logger)):
    logger.info("health check")
    return {"status": "ok"}
```

## ⚙️ Controlling what gets logged

`integrate_fastapi()` and `setup_fastapi_logging()` support common controls:

- `exclude_paths` / `exclude_methods`: skip noisy endpoints (e.g. `/health`)
- `log_headers`: log request headers (default True)
- `sensitive_headers`: mask sensitive headers
- `log_request_body` / `log_response_body`: opt-in body logging (default False)
- `max_body_bytes`: cap body size (bytes) to avoid huge logs

## 🔒 Security / Privacy / Performance notes (important)

- **General logging (recommended)**: log method/path/status/latency/headers (mask sensitive headers). Lowest risk.
- **Body logging (high risk, opt-in)**: `log_request_body/log_response_body=True` may write passwords, tokens, PII, or file contents into logs.
- **Request size & memory**: even with `max_body_bytes`, upstream servers may deliver a large chunk at once; prefer limiting request size at server/proxy level.
- **Unknown content-length**: request body is skipped by default; if you enable `log_request_body_if_unknown_length=True`, it will only peek the first `max_body_bytes` and keep the original body for downstream handlers.

## 🧱 Composable building blocks

If you want fine-grained control, use these lower-level helpers directly:

- `install_fastapi_middleware(...)`: install `LoggingMiddleware` only
- `install_fastapi_route_class(...)`: set `LoggingRoute` via `app.router.route_class` only

## 📦 Loki / ELK note

- For ELK pipelines: use `serialize=True` and ship JSON logs via Filebeat/Fluent Bit.
- For Loki: prefer Promtail/Grafana Agent, or enable direct push via `loki_enabled=True` (best-effort: no retries, no offline buffer, no backpressure; failures are dropped).
