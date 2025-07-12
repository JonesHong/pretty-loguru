# FastAPI 整合

pretty-loguru 與 FastAPI 的深度整合，提供自動化的請求日誌記錄、中間件支援和依賴注入功能。

## 🚀 快速開始

### 基本整合

```python
from fastapi import FastAPI
from pretty_loguru import create_logger, setup_fastapi_logging

# 建立 FastAPI 應用
app = FastAPI(title="My API", version="1.0.0")

# 建立日誌記錄器
logger = create_logger(
    name="fastapi_app",
    level="INFO",
    log_path="logs/fastapi.log",
    rotation="daily",
    retention="30 days"
)

# 設定 FastAPI 日誌整合
setup_fastapi_logging(
    app=app,
    logger_instance=logger,
    middleware=True,
    custom_routes=True
)

@app.get("/")
async def root():
    logger.info("根路徑被訪問")
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info(f"獲取用戶資訊", extra={"user_id": user_id})
    return {"user_id": user_id, "name": f"User {user_id}"}
```

## 🔧 中間件配置

### 自動請求日誌

```python
from fastapi import FastAPI, Request, HTTPException
from pretty_loguru import create_logger, setup_fastapi_logging
import time
import json

app = FastAPI()

# 建立專用的訪問日誌記錄器
access_logger = create_logger(
    name="fastapi_access",
    level="INFO",
    log_path="logs/access.log",
    rotation="daily",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    serialize=True
)

# 建立應用日誌記錄器
app_logger = create_logger(
    name="fastapi_app",
    level="INFO",
    log_path="logs/app.log",
    rotation="100 MB"
)

# 設定進階中間件配置
setup_fastapi_logging(
    app=app,
    logger_instance=access_logger,
    middleware=True,
    # 自訂配置
    exclude_paths=["/health", "/metrics"],  # 排除健康檢查和指標端點
    exclude_methods=["OPTIONS"],            # 排除 OPTIONS 請求
    log_request_body=True,                 # 記錄請求體（小心敏感資料）
    log_response_body=False,               # 不記錄回應體（避免過大）
    log_headers=True,                      # 記錄請求標頭
    sensitive_headers={"authorization", "cookie", "x-api-key"}  # 敏感標頭會被遮蔽
)

@app.middleware("http")
async def custom_logging_middleware(request: Request, call_next):
    """自訂日誌中間件"""
    start_time = time.time()
    
    # 提取用戶資訊（如果有認證）
    user_id = request.headers.get("x-user-id", "anonymous")
    request_id = request.headers.get("x-request-id", "unknown")
    
    # 處理請求
    response = await call_next(request)
    
    # 計算處理時間
    process_time = time.time() - start_time
    
    # 記錄詳細的訪問日誌
    app_logger.info(
        f"{request.method} {request.url.path} - {response.status_code}",
        extra={
            "request_id": request_id,
            "user_id": user_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    # 添加處理時間到回應標頭
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
```

### 錯誤處理日誌

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pretty_loguru import create_logger
import traceback

app = FastAPI()

# 建立錯誤日誌記錄器
error_logger = create_logger(
    name="fastapi_errors",
    level="ERROR",
    log_path="logs/errors.log",
    rotation="50 MB",
    retention="90 days",
    backtrace=True,
    diagnose=True
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """處理 HTTP 例外"""
    error_logger.warning(
        f"HTTP 例外: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """處理請求驗證錯誤"""
    error_logger.error(
        f"請求驗證失敗: {exc.errors()}",
        extra={
            "validation_errors": exc.errors(),
            "path": request.url.path,
            "method": request.method,
            "body": exc.body if hasattr(exc, 'body') else None
        }
    )
    
    return JSONResponse(
        status_code=422,
        content={"detail": "請求驗證失敗", "errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """處理一般例外"""
    error_logger.critical(
        f"未處理的例外: {type(exc).__name__}: {str(exc)}",
        extra={
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc(),
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "內部伺服器錯誤"}
    )
```

## 🎯 依賴注入

### 日誌記錄器注入

```python
from fastapi import FastAPI, Depends, HTTPException
from pretty_loguru import create_logger
from typing import Annotated

app = FastAPI()

# 建立不同用途的日誌記錄器
def get_app_logger():
    """獲取應用日誌記錄器"""
    return create_logger(
        name="app",
        level="INFO",
        log_path="logs/app.log"
    )

def get_business_logger():
    """獲取業務日誌記錄器"""
    return create_logger(
        name="business",
        level="INFO",
        log_path="logs/business.log",
        serialize=True
    )

def get_audit_logger():
    """獲取審計日誌記錄器"""
    return create_logger(
        name="audit",
        level="INFO",
        log_path="logs/audit.log",
        retention="7 years"  # 審計日誌長期保留
    )

# 依賴注入類型別名
AppLogger = Annotated[object, Depends(get_app_logger)]
BusinessLogger = Annotated[object, Depends(get_business_logger)]
AuditLogger = Annotated[object, Depends(get_audit_logger)]

@app.post("/users/")
async def create_user(
    user_data: dict,
    app_logger: AppLogger,
    business_logger: BusinessLogger,
    audit_logger: AuditLogger
):
    """建立用戶 - 使用多種日誌記錄器"""
    
    try:
        app_logger.info("開始建立用戶", extra={"user_data": user_data})
        
        # 模擬業務邏輯
        user_id = "user_123"
        
        # 記錄業務事件
        business_logger.info(
            "用戶建立成功",
            extra={
                "event": "user_created",
                "user_id": user_id,
                "email": user_data.get("email"),
                "registration_source": "api"
            }
        )
        
        # 記錄審計事件
        audit_logger.info(
            "用戶資料建立",
            extra={
                "action": "create",
                "resource": "user",
                "resource_id": user_id,
                "actor": "system",
                "changes": user_data
            }
        )
        
        return {"user_id": user_id, "status": "created"}
        
    except Exception as e:
        app_logger.error(f"建立用戶失敗: {e}", extra={"user_data": user_data})
        raise HTTPException(status_code=500, detail="建立用戶失敗")

@app.put("/users/{user_id}")
async def update_user(
    user_id: str,
    user_data: dict,
    audit_logger: AuditLogger
):
    """更新用戶 - 審計日誌範例"""
    
    # 獲取更新前的狀態（模擬）
    before_state = {"name": "舊名稱", "email": "old@example.com"}
    
    # 執行更新（模擬）
    after_state = user_data
    
    # 記錄審計日誌
    audit_logger.info(
        "用戶資料更新",
        extra={
            "action": "update",
            "resource": "user",
            "resource_id": user_id,
            "actor": "user",  # 實際應用中從認證資訊獲取
            "before_state": before_state,
            "after_state": after_state,
            "changed_fields": list(user_data.keys())
        }
    )
    
    return {"user_id": user_id, "status": "updated"}
```

### 上下文感知日誌

```python
from fastapi import FastAPI, Request, Depends
from contextvars import ContextVar
from pretty_loguru import create_logger
import uuid

app = FastAPI()

# 上下文變數
request_id_var: ContextVar[str] = ContextVar('request_id')
user_id_var: ContextVar[str] = ContextVar('user_id', default='anonymous')

# 建立上下文感知的日誌記錄器
logger = create_logger(
    name="context_aware",
    level="INFO",
    log_path="logs/context.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {extra[user_id]} | {message}",
    serialize=True
)

def get_context_logger():
    """獲取包含上下文的日誌記錄器"""
    class ContextLogger:
        def info(self, message, **kwargs):
            extra = kwargs.get('extra', {})
            extra.update({
                'request_id': request_id_var.get('unknown'),
                'user_id': user_id_var.get('anonymous')
            })
            kwargs['extra'] = extra
            logger.info(message, **kwargs)
        
        def error(self, message, **kwargs):
            extra = kwargs.get('extra', {})
            extra.update({
                'request_id': request_id_var.get('unknown'),
                'user_id': user_id_var.get('anonymous')
            })
            kwargs['extra'] = extra
            logger.error(message, **kwargs)
    
    return ContextLogger()

@app.middleware("http")
async def context_middleware(request: Request, call_next):
    """設定請求上下文"""
    # 生成或提取請求 ID
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request_id_var.set(request_id)
    
    # 提取用戶 ID（從認證中獲取）
    user_id = request.headers.get("x-user-id", "anonymous")
    user_id_var.set(user_id)
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response

@app.get("/orders/{order_id}")
async def get_order(
    order_id: str,
    context_logger=Depends(get_context_logger)
):
    """獲取訂單 - 上下文日誌範例"""
    
    context_logger.info(
        "開始處理訂單查詢",
        extra={"order_id": order_id, "action": "query"}
    )
    
    # 模擬業務邏輯
    try:
        # 模擬資料庫查詢
        order_data = {"order_id": order_id, "status": "shipped"}
        
        context_logger.info(
            "訂單查詢成功",
            extra={"order_id": order_id, "status": order_data["status"]}
        )
        
        return order_data
        
    except Exception as e:
        context_logger.error(
            "訂單查詢失敗",
            extra={"order_id": order_id, "error": str(e)}
        )
        raise HTTPException(status_code=404, detail="訂單不存在")
```

## 📊 效能監控

### API 效能日誌

```python
from fastapi import FastAPI, Request
from pretty_loguru import create_logger
import time
import psutil

app = FastAPI()

# 建立效能監控日誌記錄器
perf_logger = create_logger(
    name="performance",
    level="INFO",
    log_path="logs/performance.log",
    rotation="hourly",
    serialize=True
)

@app.middleware("http")
async def performance_monitoring(request: Request, call_next):
    """效能監控中間件"""
    
    # 記錄開始時間和系統資源
    start_time = time.time()
    start_cpu = psutil.cpu_percent()
    start_memory = psutil.virtual_memory().percent
    
    # 處理請求
    response = await call_next(request)
    
    # 計算處理時間和資源使用
    end_time = time.time()
    process_time = end_time - start_time
    end_cpu = psutil.cpu_percent()
    end_memory = psutil.virtual_memory().percent
    
    # 記錄效能指標
    perf_data = {
        "endpoint": f"{request.method} {request.url.path}",
        "process_time_ms": round(process_time * 1000, 2),
        "status_code": response.status_code,
        "cpu_usage_start": start_cpu,
        "cpu_usage_end": end_cpu,
        "memory_usage_start": start_memory,
        "memory_usage_end": end_memory,
        "timestamp": start_time
    }
    
    # 根據效能表現選擇日誌級別
    if process_time > 5.0:
        perf_logger.error("API 回應時間過長", extra=perf_data)
    elif process_time > 1.0:
        perf_logger.warning("API 回應時間較慢", extra=perf_data)
    else:
        perf_logger.info("API 效能正常", extra=perf_data)
    
    return response
```

## 🔧 進階配置

### 多環境配置

```python
import os
from fastapi import FastAPI
from pretty_loguru import create_logger, setup_fastapi_logging

def create_environment_logger(env: str = None):
    """根據環境建立日誌配置"""
    
    env = env or os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return create_logger(
            name="fastapi_prod",
            level="INFO",
            log_path="/var/log/fastapi/app.log",
            rotation="100 MB",
            retention="30 days",
            compression="gzip",
            serialize=True,
            enqueue=True
        )
    elif env == "staging":
        return create_logger(
            name="fastapi_staging",
            level="DEBUG",
            log_path="logs/staging.log",
            rotation="50 MB",
            retention="14 days",
            compression="gzip"
        )
    else:  # development
        return create_logger(
            name="fastapi_dev",
            level="DEBUG",
            log_path="logs/development.log",
            rotation="10 MB",
            retention="7 days",
            colorize=True  # 開發環境使用彩色輸出
        )

app = FastAPI()
logger = create_environment_logger()

setup_fastapi_logging(
    app=app,
    logger_instance=logger,
    middleware=True,
    log_request_body=os.getenv("ENVIRONMENT") != "production"  # 生產環境不記錄請求體
)
```

### 自訂日誌格式化器

```python
from fastapi import FastAPI, Request
from pretty_loguru import create_logger
import json
from datetime import datetime

class FastAPILogFormatter:
    """FastAPI 專用日誌格式化器"""
    
    def __init__(self, service_name: str, version: str):
        self.service_name = service_name
        self.version = version
    
    def format_access_log(self, request: Request, response, process_time: float):
        """格式化訪問日誌"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "version": self.version,
            "log_type": "access",
            "request": {
                "method": request.method,
                "path": request.url.path,
                "query": dict(request.query_params),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else None
            },
            "response": {
                "status_code": response.status_code,
                "headers": dict(response.headers)
            },
            "metrics": {
                "process_time_ms": round(process_time * 1000, 2)
            }
        }
    
    def format_error_log(self, error: Exception, request: Request = None):
        """格式化錯誤日誌"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "version": self.version,
            "log_type": "error",
            "error": {
                "type": type(error).__name__,
                "message": str(error)
            }
        }
        
        if request:
            log_data["request"] = {
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None
            }
        
        return log_data

# 使用自訂格式化器
app = FastAPI(title="My API", version="2.0.0")
formatter = FastAPILogFormatter("my-api", "2.0.0")

logger = create_logger(
    name="formatted_api",
    level="INFO",
    log_path="logs/formatted.log",
    rotation="daily"
)

@app.middleware("http")
async def formatted_logging(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # 使用自訂格式化器
    log_data = formatter.format_access_log(request, response, process_time)
    logger.info("API 訪問", extra=log_data)
    
    return response
```

## 🔗 相關資源

- [基本用法](../guide/basic-usage) - 日誌記錄基礎
- [自定義配置](../guide/custom-config) - 進階配置選項
- [生產環境部署](../guide/production) - 生產環境最佳實踐
- [範例集合](../examples/integrations/) - FastAPI 整合範例