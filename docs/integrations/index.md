# 整合指南

pretty-loguru 設計為與現代 Python 框架無縫整合。本章節將展示如何將 pretty-loguru 整合到各種 Web 框架和應用中。

## 🌐 支援的框架

### Web 框架
- **[FastAPI](./fastapi)** - 現代、快速的 Web 框架
- **[Uvicorn](./uvicorn)** - 高效能 ASGI 伺服器

### 即將支援
- **Flask** - 輕量級 Web 框架
- **Django** - 全功能 Web 框架
- **Starlette** - 輕量級 ASGI 框架

## 🚀 快速開始

### FastAPI 基本整合

```python
from fastapi import FastAPI
from pretty_loguru import logger, logger_start

# 初始化日誌
logger_start(folder="api_logs")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.ascii_header("API STARTUP", font="slant", border_style="blue")
    logger.success("FastAPI 應用啟動完成")

@app.get("/")
async def root():
    logger.info("收到根路徑請求")
    return {"message": "Hello World"}
```

### Uvicorn 日誌統一

```python
from pretty_loguru import uvicorn_init_config

# 統一 Uvicorn 日誌到 pretty-loguru
uvicorn_init_config()

# 啟動時所有 Uvicorn 日誌都會使用 pretty-loguru 格式
```

## 🎯 整合模式

### 1. 基本整合
最簡單的整合方式，替換預設的日誌系統。

### 2. 中介軟體整合
在請求處理中間添加日誌記錄。

### 3. 依賴注入整合
使用框架的依賴注入系統管理 logger。

### 4. 完全客製化
完全控制日誌行為和格式。

## 📊 整合效果展示

### 請求日誌

```python
# 中介軟體記錄每個請求
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.console_info(f"→ {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    status_color = "green" if response.status_code < 400 else "red"
    
    logger.block(
        "請求完成",
        [
            f"方法: {request.method}",
            f"路徑: {request.url.path}",
            f"狀態: {response.status_code}",
            f"處理時間: {process_time:.3f}s"
        ],
        border_style=status_color
    )
    
    return response
```

### 啟動日誌

```python
@app.on_event("startup")
async def startup():
    logger.ascii_header("WEB API", font="block", border_style="cyan")
    
    logger.block(
        "服務資訊",
        [
            f"應用名稱: {settings.app_name}",
            f"版本: {settings.version}",
            f"環境: {settings.environment}",
            f"除錯模式: {'開啟' if settings.debug else '關閉'}"
        ],
        border_style="blue"
    )
    
    logger.success("🚀 Web API 已成功啟動")
```

## 🔧 進階配置

### 環境別配置

```python
import os
from pretty_loguru import logger_start

def setup_logging():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return logger_start(
            folder="prod_logs",
            level="INFO",
            rotation="100MB",
            retention="30 days"
        )
    elif env == "staging":
        return logger_start(
            folder="staging_logs", 
            level="DEBUG",
            rotation="50MB",
            retention="14 days"
        )
    else:  # development
        return logger_start(
            folder="dev_logs",
            level="DEBUG",
            rotation="10MB",
            retention="7 days"
        )
```

### 多重日誌目標

```python
from pretty_loguru import create_logger

# API 專用 logger
api_logger = create_logger("api", log_path="logs/api")

# 資料庫專用 logger  
db_logger = create_logger("database", log_path="logs/db")

# 背景任務專用 logger
task_logger = create_logger("tasks", log_path="logs/tasks")

# 在不同模組中使用
class APIService:
    def process_request(self):
        api_logger.info("處理 API 請求")
        
class DatabaseService:
    def connect(self):
        db_logger.success("資料庫連接成功")
```

## 🎮 實際範例

### 完整的 FastAPI 應用

```python
from fastapi import FastAPI, Request, HTTPException
from pretty_loguru import logger, logger_start, uvicorn_init_config
import time
import uvicorn

# 初始化日誌系統
logger_start(folder="webapp_logs")
uvicorn_init_config()

app = FastAPI(title="Demo API", version="1.0.0")

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # 請求開始
    logger.console_info(f"→ {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # 成功響應
        logger.block(
            "請求成功",
            [
                f"📍 路徑: {request.url.path}",
                f"⚡ 方法: {request.method}",
                f"✅ 狀態: {response.status_code}",
                f"⏱️  時間: {process_time:.3f}s"
            ],
            border_style="green"
        )
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        
        # 錯誤響應
        logger.block(
            "請求失敗",
            [
                f"📍 路徑: {request.url.path}",
                f"⚡ 方法: {request.method}",
                f"❌ 錯誤: {str(e)}",
                f"⏱️  時間: {process_time:.3f}s"
            ],
            border_style="red",
            log_level="ERROR"
        )
        raise

@app.on_event("startup")
async def startup_event():
    logger.ascii_header("WEBAPP START", font="slant", border_style="blue")
    
    logger.block(
        "應用配置",
        [
            "🌐 名稱: Demo API",
            "📦 版本: 1.0.0",
            "🔧 環境: Development",
            "🚀 狀態: 啟動中"
        ],
        border_style="cyan"
    )
    
    logger.success("✨ 應用啟動完成")

@app.on_event("shutdown")
async def shutdown_event():
    logger.ascii_header("SHUTDOWN", font="standard", border_style="magenta")
    logger.info("應用正在關閉...")

@app.get("/")
async def root():
    logger.info("處理根路徑請求")
    return {"message": "Hello Pretty Loguru!"}

@app.get("/health")
async def health_check():
    logger.success("健康檢查通過")
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/error")
async def trigger_error():
    logger.error("故意觸發錯誤進行測試")
    raise HTTPException(status_code=500, detail="測試錯誤")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 💡 最佳實踐

### 1. 日誌分層
不同類型的日誌使用不同的 logger：

```python
# 按功能分層
api_logger = create_logger("api")      # API 相關
auth_logger = create_logger("auth")    # 認證相關  
db_logger = create_logger("db")        # 資料庫相關
```

### 2. 結構化日誌
使用 Rich 區塊記錄結構化資訊：

```python
logger.block(
    "用戶操作",
    [
        f"用戶 ID: {user_id}",
        f"操作: {action}",
        f"IP 地址: {ip_address}",
        f"時間戳: {timestamp}"
    ]
)
```

### 3. 錯誤追蹤
詳細記錄錯誤資訊：

```python
try:
    # 業務邏輯
    pass
except Exception as e:
    logger.ascii_block(
        "錯誤報告",
        [
            f"錯誤類型: {type(e).__name__}",
            f"錯誤訊息: {str(e)}",
            f"發生位置: {__file__}:{inspect.currentframe().f_lineno}",
            f"用戶 ID: {current_user.id}",
            f"請求 ID: {request_id}"
        ],
        ascii_header="ERROR",
        border_style="red",
        log_level="ERROR"
    )
```

## 🚀 下一步

選擇你使用的框架開始整合：

- **[FastAPI 整合](./fastapi)** - 詳細的 FastAPI 整合指南
- **[Uvicorn 整合](./uvicorn)** - Uvicorn 伺服器日誌統一
- **[查看範例](../examples/fastapi/)** - 完整的實際應用範例

準備好將 pretty-loguru 整合到你的專案中了嗎？ 🎯