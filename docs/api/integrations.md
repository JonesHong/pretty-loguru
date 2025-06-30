# 整合模組 API

`pretty-loguru` 的整合模組旨在與流行的 Python 框架（如 FastAPI 和 Uvicorn）無縫協作，讓你可以在現有專案中輕鬆地引入強大的日誌功能。

**注意：** 使用特定的整合功能前，請確保已安裝對應的函式庫（例如 `pip install fastapi uvicorn`）。

---

## FastAPI 整合

此模組提供了在 FastAPI 應用中記錄 HTTP 請求、注入 logger 以及統一日誌管理的完整解決方案。

### `integrate_fastapi()`

這是最推薦的快速整合方法。它會自動設定日誌中間件，並可選擇性地一併設定 Uvicorn 日誌。

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

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `app` | `FastAPI` | 你的 FastAPI 應用實例。 |
| `logger` | `EnhancedLogger` | 一個已創建的 `pretty-loguru` logger 實例。 |
| `enable_uvicorn` | `bool` | 若為 `True`，會同時呼叫 `integrate_uvicorn` 來統一日誌。 |
| `exclude_health_checks` | `bool` | 若為 `True`，會自動排除 `/health`, `/metrics`, `/docs` 等常見的非業務路徑。 |
| `**kwargs` | `Any` | 其他要傳遞給 `LoggingMiddleware` 的參數，如 `log_request_body=True`。 |

**範例：**

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

# 1. 創建 FastAPI 應用和 logger
app = FastAPI()
logger = create_logger("my_api", log_path="logs/")

# 2. 一行代碼完成整合
integrate_fastapi(app, logger)

@app.get("/")
async def root():
    logger.info("處理根路徑請求")
    return {"message": "Hello World"}
```

### `LoggingMiddleware`

一個 FastAPI 中間件，用於自動記錄每個傳入請求的詳細資訊，包括請求方法、路徑、客戶端 IP、處理時間和狀態碼。

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

**主要參數：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `logger_instance` | `EnhancedLogger` | 用於記錄日誌的 logger 實例。 |
| `exclude_paths` | `List[str]` | 一個路徑列表，符合的請求將不會被記錄。 |
| `log_request_body` | `bool` | 是否記錄請求的 body 內容。 |
| `log_response_body` | `bool` | 是否記錄回應的 body 內容。 |
| `sensitive_headers` | `Set[str]` | 一組敏感的標頭名稱，其值將被遮蔽，預設包含 `authorization`。 |

### `get_logger_dependency()`

創建一個 FastAPI 依賴，讓你可以在路由函數中輕鬆地注入 logger 實例。

```python
def get_logger_dependency(
    name: Optional[str] = None,
    **kwargs: Any
) -> Callable[[], EnhancedLogger]:
    ...
```

**範例：**

```python
from fastapi import FastAPI, Depends
from pretty_loguru.types import EnhancedLogger
from pretty_loguru.integrations.fastapi import get_logger_dependency

app = FastAPI()

# 創建一個 logger 依賴
api_logger_dependency = get_logger_dependency(name="api_route", log_path="logs/api.log")

@app.get("/users/{user_id}")
async def get_user(user_id: str, logger: EnhancedLogger = Depends(api_logger_dependency)):
    logger.info(f"正在獲取使用者 {user_id} 的資料")
    # ... 業務邏輯 ...
    return {"user_id": user_id}
```

---

## Uvicorn 整合

此模組可以攔截 Uvicorn 的標準日誌，並將其重導向到 `pretty-loguru`，從而讓 ASGI 伺服器的日誌與你的應用日誌擁有統一的格式和輸出目標。

### `integrate_uvicorn()`

推薦使用此函數來設定 Uvicorn 日誌。它會處理所有必要的底層配置。

```python
def integrate_uvicorn(
    logger: Any,
    level: LogLevelType = "INFO"
) -> None:
    ...
```

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `logger` | `Any` | 你希望 Uvicorn 使用的 `pretty-loguru` logger 實例。 |
| `level` | `LogLevelType` | Uvicorn 要記錄的最低日誌級別。 |

**範例：**

```python
import uvicorn
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

app = FastAPI()
logger = create_logger("main_app", log_path="logs/")

# 在啟動 uvicorn 前進行整合
integrate_uvicorn(logger)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### `InterceptHandler`

這是一個繼承自 `logging.Handler` 的類別，是實現 Uvicorn 日誌攔截的核心。它會捕獲由 Python 標準 `logging` 模組發出的日誌，並將其轉換為 `loguru` 格式。

通常你不需要直接使用此類別，`integrate_uvicorn` 函數已經為你處理好了。

---

[返回 API 總覽](./index.md)
