# 框架整合範例

展示如何將 Pretty-Loguru 整合到各種 Python 框架中，特別是 FastAPI 和 Uvicorn。

## FastAPI 基本整合

最簡單的 FastAPI 整合方式：

```python
from fastapi import FastAPI
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

# 創建 FastAPI 應用
app = FastAPI(title="My API")

# 設定日誌
setup_fastapi_logging(
    app,
    log_path="logs/api",
    level="INFO"
)

@app.get("/")
async def root():
    # 自動記錄請求和響應
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # 錯誤會自動被捕獲和記錄
    if item_id == 0:
        raise ValueError("Invalid item ID")
    return {"item_id": item_id}

# 運行：uvicorn main:app --reload
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/simple_api.py)

## 中間件日誌

使用中間件記錄所有請求：

```python
from fastapi import FastAPI, Request
from pretty_loguru import create_logger
import time

app = FastAPI()
logger = create_logger("api", log_path="logs/api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """記錄所有 HTTP 請求"""
    start_time = time.time()
    
    # 記錄請求資訊
    logger.info(f"📥 {request.method} {request.url.path}")
    
    # 處理請求
    response = await call_next(request)
    
    # 計算處理時間
    process_time = time.time() - start_time
    
    # 記錄響應資訊
    logger.info(
        f"📤 {request.method} {request.url.path} "
        f"- {response.status_code} ({process_time:.3f}s)"
    )
    
    # 為響應添加處理時間標頭
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/slow")
async def slow_endpoint():
    """模擬慢速端點"""
    import asyncio
    await asyncio.sleep(2)
    return {"message": "Finally done!"}
```

輸出範例：
```
2024-01-20 15:30:00 | INFO | 📥 GET /slow
2024-01-20 15:30:02 | INFO | 📤 GET /slow - 200 (2.003s)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/middleware_demo.py)

## 依賴注入

使用 FastAPI 的依賴注入系統管理 logger：

```python
from fastapi import FastAPI, Depends
from typing import Annotated
from pretty_loguru import create_logger, EnhancedLogger

app = FastAPI()

# 創建不同的 logger
api_logger = create_logger("api", level="INFO")
db_logger = create_logger("database", level="DEBUG")
auth_logger = create_logger("auth", level="WARNING")

# 依賴注入函數
def get_api_logger() -> EnhancedLogger:
    return api_logger

def get_db_logger() -> EnhancedLogger:
    return db_logger

def get_auth_logger() -> EnhancedLogger:
    return auth_logger

# 使用依賴注入
@app.post("/users/")
async def create_user(
    user_data: dict,
    logger: Annotated[EnhancedLogger, Depends(get_api_logger)],
    db_logger: Annotated[EnhancedLogger, Depends(get_db_logger)]
):
    logger.info(f"Creating user: {user_data.get('username')}")
    
    # 模擬資料庫操作
    db_logger.debug(f"INSERT INTO users VALUES {user_data}")
    
    logger.success("User created successfully")
    return {"id": 123, **user_data}

@app.post("/auth/login")
async def login(
    credentials: dict,
    logger: Annotated[EnhancedLogger, Depends(get_auth_logger)]
):
    logger.warning(f"Login attempt for: {credentials.get('username')}")
    
    # 驗證邏輯...
    
    logger.info("Login successful")
    return {"token": "xxx"}
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/dependency_injection.py)

## Uvicorn 整合

配置 Uvicorn 使用 Pretty-Loguru：

```python
import uvicorn
from fastapi import FastAPI
from pretty_loguru.integrations.uvicorn import configure_uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # 配置 Uvicorn 日誌
    configure_uvicorn(
        log_path="logs/uvicorn",
        level="INFO",
        intercept_levels=["INFO", "WARNING", "ERROR"]
    )
    
    # 運行伺服器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None  # 重要：禁用預設配置
    )
```

Uvicorn 配置選項：
```python
from pretty_loguru import LoggerConfig, ConfigTemplates

# 使用配置模板
config = ConfigTemplates.production()
configure_uvicorn(config=config)

# 自定義配置
custom_config = LoggerConfig(
    level="DEBUG",
    log_path="logs/server",
    rotation="100 MB",
    retention="30 days"
)
configure_uvicorn(config=custom_config)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/test_uvicorn_logging.py)

## 完整的 Web 應用範例

結合所有功能的完整範例：

```python
from fastapi import FastAPI, Request, HTTPException
from pretty_loguru import create_logger, ConfigTemplates
from pretty_loguru.integrations.fastapi import setup_fastapi_logging
import time

# 創建應用
app = FastAPI(title="完整範例")

# 使用生產環境配置
config = ConfigTemplates.production()
logger = create_logger("webapp", config=config)

# 設定 FastAPI 日誌
setup_fastapi_logging(app, config=config)

# 全局異常處理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"未處理的異常: {type(exc).__name__}: {str(exc)}")
    logger.error(f"請求路徑: {request.url.path}")
    
    # 錯誤報告
    logger.block(
        "❌ 錯誤詳情",
        [
            f"錯誤類型: {type(exc).__name__}",
            f"錯誤訊息: {str(exc)}",
            f"請求方法: {request.method}",
            f"請求路徑: {request.url.path}",
        ],
        border_style="red",
        log_level="ERROR"
    )
    
    return {"error": "Internal server error"}

# 啟動事件
@app.on_event("startup")
async def startup_event():
    logger.ascii_header("API START", font="small", border_style="green")
    logger.block(
        "🚀 服務啟動",
        [
            "環境: Production",
            "版本: v1.0.0",
            "配置: 生產環境預設",
            f"日誌路徑: {config.log_path}"
        ],
        border_style="green"
    )

# 健康檢查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

# 業務端點
@app.post("/process")
async def process_data(data: dict):
    logger.info(f"處理請求: {data.get('id')}")
    
    # 模擬處理
    with logger.progress("處理數據") as progress:
        task = progress.add_task("分析", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            await asyncio.sleep(0.01)
    
    logger.success("處理完成")
    return {"result": "processed"}
```

## 單行整合

最簡單的整合方式：

```python
from fastapi import FastAPI
from pretty_loguru import create_logger

app = FastAPI()
logger = create_logger("api")  # 一行搞定！

@app.get("/")
async def root():
    logger.info("Hello endpoint called")
    return {"message": "Hello World"}
```

## 環境特定配置

根據環境使用不同配置：

```python
import os
from fastapi import FastAPI
from pretty_loguru import create_logger, ConfigTemplates

app = FastAPI()

# 根據環境變數選擇配置
env = os.getenv("ENV", "development")

if env == "production":
    config = ConfigTemplates.production()
elif env == "testing":
    config = ConfigTemplates.testing()
else:
    config = ConfigTemplates.development()

logger = create_logger("api", config=config)
logger.info(f"Running in {env} mode")
```

## 下一步

- [生產環境](./production.md) - 部署和監控
- [進階功能](./advanced.md) - 自定義和擴展
- [配置管理](./configuration.md) - 深入配置選項