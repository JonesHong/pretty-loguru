# Integrations Module API

The `pretty-loguru` integrations module is designed to work seamlessly with popular Python frameworks (such as FastAPI and Uvicorn), allowing you to easily introduce powerful logging functionality into existing projects.

**Note:** Before using integrations, ensure dependencies are installed. Recommended: `uv add "pretty-loguru[integrations]"` (or `pip install "pretty-loguru[integrations]"`).

---

## FastAPI Integration

This module provides a complete solution for logging HTTP requests, injecting loggers, and unified log management in FastAPI applications.

### `integrate_fastapi()`

This is the recommended quick integration method. It automatically sets up logging middleware and optionally configures Uvicorn logging as well.

```python
def integrate_fastapi(
    app: FastAPI,
    logger: PrettyLogger,
    enable_uvicorn: bool = True,
    exclude_health_checks: bool = True,
    exclude_paths: Optional[List[str]] = None,
    exclude_methods: Optional[List[str]] = None,
    # Middleware configuration
    middleware: bool = True,
    custom_routes: bool = False,
    log_request_body: bool = False,
    log_response_body: bool = False,
    log_headers: bool = True,
    sensitive_headers: Optional[Set[str]] = None
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `app` | `FastAPI` | - | Your FastAPI application instance. |
| `logger` | `PrettyLogger` | - | An already created `pretty-loguru` logger instance. |
| `enable_uvicorn` | `bool` | `True` | If `True`, will also call `integrate_uvicorn` to unify logging. |
| `exclude_health_checks` | `bool` | `True` | If `True`, automatically excludes common non-business paths like `/health`, `/metrics`, `/docs`. |

**Path and Method Control:**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `exclude_paths` | `Optional[List[str]]` | `None` | Additional paths to exclude from logging |
| `exclude_methods` | `Optional[List[str]]` | `None` | HTTP methods to exclude from logging |

**Middleware Configuration:**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `middleware` | `bool` | `True` | Whether to add logging middleware |
| `custom_routes` | `bool` | `False` | Whether to use custom LoggingRoute |
| `log_request_body` | `bool` | `False` | Whether to log request body |
| `log_response_body` | `bool` | `False` | Whether to log response body |
| `log_headers` | `bool` | `True` | Whether to log request and response headers |
| `sensitive_headers` | `Optional[Set[str]]` | `None` | Sensitive header fields whose values will be masked |

**Examples:**

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

# 1. Create FastAPI app and logger
app = FastAPI()
logger = create_logger("my_api", log_dir="logs/")

# 2. Basic integration
integrate_fastapi(app, logger)

# 3. Full configuration integration
integrate_fastapi(
    app,
    logger,
    log_request_body=True,        # Log request body
    log_response_body=False,      # Don't log response body
    log_headers=True,             # Log header information
    exclude_paths=["/metrics"],   # Additional excluded paths
    sensitive_headers={"x-api-key", "authorization"}  # Sensitive headers
)

@app.get("/")
async def root():
    logger.info("Processing root path request")
    return {"message": "Hello World"}
```

### `LoggingMiddleware`

A FastAPI middleware that automatically logs detailed information for each incoming request, including request method, path, client IP, processing time, and status code.

```python
class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        logger_instance: Optional[PrettyLogger] = None,
        exclude_paths: Optional[List[str]] = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
        sensitive_headers: Optional[Set[str]] = None
    ):
        ...
```

**Main Parameters:**

| Parameter | Type | Description |
| --- | --- | --- |
| `logger_instance` | `PrettyLogger` | Logger instance used for logging. |
| `exclude_paths` | `List[str]` | List of paths where matching requests won't be logged. |
| `log_request_body` | `bool` | Whether to log request body content. |
| `log_response_body` | `bool` | Whether to log response body content. |
| `sensitive_headers` | `Set[str]` | Set of sensitive header names whose values will be masked, defaults include `authorization`. |

### `get_logger_dependency()`

Creates a FastAPI dependency that allows you to easily inject logger instances into route functions.

```python
def get_logger_dependency(
    logger_instance: PrettyLogger
) -> Callable[[], PrettyLogger]:
    ...
```

**Examples:**

```python
from fastapi import FastAPI, Depends
from pretty_loguru.types import PrettyLogger
from pretty_loguru.integrations.fastapi import get_logger_dependency
from pretty_loguru import create_logger

app = FastAPI()

# Create a logger dependency
logger = create_logger("api_route", log_dir="logs/api")
api_logger_dependency = get_logger_dependency(logger)

@app.get("/users/{user_id}")
async def get_user(user_id: str, logger: PrettyLogger = Depends(api_logger_dependency)):
    logger.info(f"Fetching data for user {user_id}")
    # ... business logic ...
    return {"user_id": user_id}
```

---

## Uvicorn Integration

This module can intercept Uvicorn's standard logs and redirect them to `pretty-loguru`, providing unified format and output destinations for both ASGI server logs and your application logs.

### `build_uvicorn_log_config()`

This is the **recommended** approach: it only builds the `dict` required by `uvicorn.run(..., log_config=...)` with minimal side effects and best predictability.

```python
def build_uvicorn_log_config(
    logger_instance: Any = None,
    log_level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None,
) -> Dict[str, Any]:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `logger_instance` | `Any` | The `pretty-loguru` logger instance you want Uvicorn to use. |
| `log_level` | `LogLevelType` | Minimum log level for Uvicorn to record (aligned with `uvicorn.run(..., log_level=...)`). |
| `logger_names` | `Optional[List[str]]` | List of standard `logging` logger names to intercept (defaults to Uvicorn-related loggers). |

### `integrate_uvicorn()`

Convenient integration helper:

- `monkeypatch=False` (default): equivalent to calling `build_uvicorn_log_config()` and returning `log_config`
- `monkeypatch=True`: patches Uvicorn's logging initialization (bigger side effects; only use when you understand the impact)

```python
def integrate_uvicorn(
    logger: Any = None,
    log_level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None,
    *,
    monkeypatch: bool = False,
) -> Optional[Dict[str, Any]]:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `logger` | `Any` | The `pretty-loguru` logger instance you want Uvicorn to use. |
| `log_level` | `LogLevelType` | Minimum log level for Uvicorn to record (aligned with `uvicorn.run(..., log_level=...)`). |
| `logger_names` | `Optional[List[str]]` | List of `logging` logger names to intercept (defaults to Uvicorn-related loggers). |
| `monkeypatch` | `bool` | Whether to monkeypatch Uvicorn's internal logging setup (default False; prefer passing `log_config`). |

**Examples:**

```python
import uvicorn
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import build_uvicorn_log_config

app = FastAPI()
logger = create_logger("main_app", log_dir="logs/")

# Build log_config before starting Uvicorn (non-monkeypatch, recommended)
log_config = build_uvicorn_log_config(logger_instance=logger)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
```

### `InterceptHandler`

This is a class that inherits from `logging.Handler` and is the core of implementing Uvicorn log interception. It captures logs emitted by Python's standard `logging` module and converts them to `loguru` format.

Usually you don't need to use this class directly, as the `integrate_uvicorn` function already handles it for you.

---

## Loki Integration

This module provides an in-process Grafana Loki sink (best-effort): failures are swallowed, no retries, no offline buffering. For reliability, prefer `promtail`/`grafana-agent` to ship logs from files to Loki.

### `LokiSinkConfig`

```python
@dataclass
class LokiSinkConfig:
    url: str
    labels: Dict[str, str] = ...
    batch_size: int = 50
    flush_interval_seconds: float = 1.0
    timeout_seconds: float = 2.0
    tenant_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    headers: Dict[str, str] = ...
```

### `create_loki_sink()`

```python
def create_loki_sink(
    url: str,
    labels: Optional[Dict[str, str]] = None,
    batch_size: int = 50,
    flush_interval_seconds: float = 1.0,
    timeout_seconds: float = 2.0,
    tenant_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
) -> LokiSink:
    ...
```

**Example (direct push)**:

```python
from pretty_loguru import create_logger
from pretty_loguru.integrations.loki import create_loki_sink

logger = create_logger("app", log_dir="logs/", serialize=True)

logger.add(
    create_loki_sink(
        "http://localhost:3100",
        labels={"app": "demo", "env": "local"},
    ),
    level="INFO",
    serialize=True,
    enqueue=True,
)
```

[Back to API Overview](./index.md)
