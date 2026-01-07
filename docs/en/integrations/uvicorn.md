# Uvicorn Integration

pretty-loguru can intercept Uvicorn’s standard `logging` output and forward it into your pretty-loguru logger.

## 🚀 Basic usage

```python
# main.py
from fastapi import FastAPI
import uvicorn

from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

app = FastAPI()

logger = create_logger(
    name="my_app",
    component_name="my_app",
    log_dir="logs/my_app",   # log_dir is a directory
    level="INFO",
)

# Build uvicorn log_config (non-monkeypatch, recommended)
log_config = integrate_uvicorn(logger)

@app.get("/health")
def health():
    logger.info("health check")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
```

## ⚙️ Options

- `integrate_uvicorn(logger, log_level="INFO")`: set interception level (returns log_config)
- `integrate_uvicorn(logger, logger_names=[...])`: customize which `logging` loggers to intercept (returns log_config)
- `integrate_uvicorn(logger, monkeypatch=True)`: explicitly enable monkeypatch (no need to pass log_config, but modifies uvicorn internals)

