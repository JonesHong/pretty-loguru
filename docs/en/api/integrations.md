# Integrations Module API

The `pretty-loguru` integrations module is designed to work seamlessly with popular Python frameworks (such as FastAPI and Uvicorn), allowing you to easily introduce powerful logging functionality into existing projects.

**Note:** Before using specific integration features, ensure the corresponding libraries are installed (e.g., `pip install fastapi uvicorn`).

---

## FastAPI Integration

This module provides a complete solution for logging HTTP requests, injecting loggers, and unified log management in FastAPI applications.

### `integrate_fastapi()`

This is the recommended quick integration method. It automatically sets up logging middleware and optionally configures Uvicorn logging as well.

```python
def integrate_fastapi(
    app: FastAPI,
    logger: EnhancedLogger,
    enable_uvicorn: bool = True,
    exclude_health_checks: bool = True,
    **kwargs: Any
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `app` | `FastAPI` | Your FastAPI application instance. |
| `logger` | `EnhancedLogger` | An already created `pretty-loguru` logger instance. |
| `enable_uvicorn` | `bool` | If `True`, will also call `integrate_uvicorn` to unify logging. |
| `exclude_health_checks` | `bool` | If `True`, automatically excludes common non-business paths like `/health`, `/metrics`, `/docs`. |
| `**kwargs` | `Any` | Other parameters to pass to `LoggingMiddleware`, such as `log_request_body=True`. |

**Examples:**

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

# 1. Create FastAPI app and logger
app = FastAPI()
logger = create_logger("my_api", log_path="logs/")

# 2. Complete integration with one line
integrate_fastapi(app, logger)

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
        logger_instance: Optional[EnhancedLogger] = None,
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
| `logger_instance` | `EnhancedLogger` | Logger instance used for logging. |
| `exclude_paths` | `List[str]` | List of paths where matching requests won't be logged. |
| `log_request_body` | `bool` | Whether to log request body content. |
| `log_response_body` | `bool` | Whether to log response body content. |
| `sensitive_headers` | `Set[str]` | Set of sensitive header names whose values will be masked, defaults include `authorization`. |

### `get_logger_dependency()`

Creates a FastAPI dependency that allows you to easily inject logger instances into route functions.

```python
def get_logger_dependency(
    name: Optional[str] = None,
    **kwargs: Any
) -> Callable[[], EnhancedLogger]:
    ...
```

**Examples:**

```python
from fastapi import FastAPI, Depends
from pretty_loguru.types import EnhancedLogger
from pretty_loguru.integrations.fastapi import get_logger_dependency

app = FastAPI()

# Create a logger dependency
api_logger_dependency = get_logger_dependency(name="api_route", log_path="logs/api.log")

@app.get("/users/{user_id}")
async def get_user(user_id: str, logger: EnhancedLogger = Depends(api_logger_dependency)):
    logger.info(f"Fetching data for user {user_id}")
    # ... business logic ...
    return {"user_id": user_id}
```

---

## Uvicorn Integration

This module can intercept Uvicorn's standard logs and redirect them to `pretty-loguru`, providing unified format and output destinations for both ASGI server logs and your application logs.

### `integrate_uvicorn()`

Use this function to configure Uvicorn logging. It handles all necessary underlying configuration.

```python
def integrate_uvicorn(
    logger: Any,
    level: LogLevelType = "INFO"
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `logger` | `Any` | The `pretty-loguru` logger instance you want Uvicorn to use. |
| `level` | `LogLevelType` | Minimum log level for Uvicorn to record. |

**Examples:**

```python
import uvicorn
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

app = FastAPI()
logger = create_logger("main_app", log_path="logs/")

# Integrate before starting uvicorn
integrate_uvicorn(logger)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### `InterceptHandler`

This is a class that inherits from `logging.Handler` and is the core of implementing Uvicorn log interception. It captures logs emitted by Python's standard `logging` module and converts them to `loguru` format.

Usually you don't need to use this class directly, as the `integrate_uvicorn` function already handles it for you.

---

[Back to API Overview](./index.md)