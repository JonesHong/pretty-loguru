# FastAPI 應用範例

pretty-loguru 與 FastAPI 完美整合，提供美觀且實用的 API 日誌記錄功能。本頁面展示如何在 FastAPI 應用中充分利用 pretty-loguru 的視覺化功能。

## 🚀 基本整合

### 簡單的 FastAPI 應用

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pretty_loguru import create_logger
import time
import uvicorn

# 初始化日誌系統
logger = create_logger(
    name="fastapi_demo",
    log_path="fastapi_logs", preset="development",
    level="INFO"
)

app = FastAPI(title="Pretty Loguru API Demo", version="1.0.1")

@app.on_event("startup")
async def startup_event():
    """應用啟動事件"""
    logger.ascii_header("API START", font="slant", border_style="blue")
    
    logger.block(
        "FastAPI 應用啟動",
        [
            "🚀 應用名稱: Pretty Loguru API Demo",
            "📦 版本: 1.0.1",
            "🌐 環境: Development",
            "📝 日誌系統: pretty-loguru",
            "⚡ 狀態: 準備就緒"
        ],
        border_style="green",
        log_level="SUCCESS"
    )

@app.on_event("shutdown")
async def shutdown_event():
    """應用關閉事件"""
    logger.ascii_header("SHUTDOWN", font="standard", border_style="yellow")
    logger.warning("FastAPI 應用正在關閉...")

@app.get("/")
async def root():
    logger.info("收到根路徑請求")
    return {"message": "Hello World", "status": "success"}

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    logger.info("執行健康檢查")
    
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.1"
    }
    
    logger.block(
        "健康檢查結果",
        [
            "✅ 應用狀態: 正常",
            "✅ 資料庫: 連接正常",
            "✅ 快取: 運行正常",
            f"⏰ 檢查時間: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        ],
        border_style="green"
    )
    
    return health_status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔧 中間件整合

### 請求日誌中間件

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import json

class PrettyLoguruMiddleware(BaseHTTPMiddleware):
    """Pretty Loguru 日誌中間件"""
    
    async def dispatch(self, request: Request, call_next):
        # 記錄請求開始
        start_time = time.time()
        
        # 獲取請求資訊
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        logger.ascii_header("REQUEST", font="small", border_style="cyan")
        
        logger.block(
            "新的 API 請求",
            [
                f"🌐 方法: {method}",
                f"📍 URL: {url}",
                f"💻 客戶端 IP: {client_ip}",
                f"🖥️  User-Agent: {user_agent[:50]}...",
                f"⏰ 時間: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            ],
            border_style="blue"
        )
        
        # 處理請求
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # 根據響應狀態選擇顏色
            if response.status_code < 300:
                color = "green"
                level = "SUCCESS"
            elif response.status_code < 400:
                color = "yellow" 
                level = "WARNING"
            else:
                color = "red"
                level = "ERROR"
            
            logger.block(
                "請求處理完成",
                [
                    f"📊 狀態碼: {response.status_code}",
                    f"⏱️  處理時間: {process_time:.3f}s",
                    f"📦 響應大小: {len(response.body) if hasattr(response, 'body') else 'N/A'} bytes",
                    f"✅ 狀態: {'成功' if response.status_code < 400 else '失敗'}"
                ],
                border_style=color,
                log_level=level
            )
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            
            logger.ascii_block(
                "請求處理失敗",
                [
                    f"❌ 錯誤: {str(e)}",
                    f"⏱️  處理時間: {process_time:.3f}s",
                    f"🔍 請求: {method} {url}",
                    f"💻 客戶端: {client_ip}"
                ],
                ascii_header="ERROR",
                ascii_font="doom",
                border_style="red",
                log_level="ERROR"
            )
            
            raise

# 應用中間件
app = FastAPI()
app.add_middleware(PrettyLoguruMiddleware)
```

### 錯誤處理中間件

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 例外處理器"""
    
    logger.ascii_block(
        "HTTP 例外處理",
        [
            f"❌ 狀態碼: {exc.status_code}",
            f"📝 詳細訊息: {exc.detail}",
            f"🌐 請求路徑: {request.url.path}",
            f"📊 請求方法: {request.method}",
            f"💻 客戶端 IP: {request.client.host if request.client else 'unknown'}"
        ],
        ascii_header="HTTP ERROR",
        ascii_font="standard",
        border_style="red",
        log_level="ERROR"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """一般例外處理器"""
    
    logger.ascii_block(
        "系統例外處理",
        [
            f"💥 例外類型: {type(exc).__name__}",
            f"📝 錯誤訊息: {str(exc)}",
            f"🌐 請求路徑: {request.url.path}",
            f"📊 請求方法: {request.method}",
            f"🔍 需要檢查: 程式碼邏輯"
        ],
        ascii_header="EXCEPTION", 
        ascii_font="doom",
        border_style="red",
        log_level="CRITICAL"
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )
```

## 📊 業務邏輯日誌

### 用戶認證系統

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
import hashlib

security = HTTPBearer()

class AuthService:
    """認證服務"""
    
    def __init__(self):
        self.secret_key = "your-secret-key"
        self.algorithm = "HS256"
    
    async def login(self, username: str, password: str):
        """用戶登入"""
        logger.ascii_header("LOGIN", font="standard", border_style="blue")
        
        logger.block(
            "用戶登入嘗試",
            [
                f"👤 用戶名: {username}",
                f"🕐 時間: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"🔐 密碼雜湊: {hashlib.md5(password.encode()).hexdigest()[:8]}...",
                f"🌐 請求來源: 登入端點"
            ],
            border_style="cyan"
        )
        
        # 模擬認證邏輯
        if username == "admin" and password == "password":
            # 成功登入
            token = jwt.encode(
                {"username": username, "exp": time.time() + 3600}, 
                self.secret_key, 
                algorithm=self.algorithm
            )
            
            logger.ascii_block(
                "登入成功",
                [
                    f"✅ 用戶: {username}",
                    f"🎫 Token 已生成",
                    f"⏰ 有效期: 1 小時",
                    f"🔒 算法: {self.algorithm}",
                    f"🎯 狀態: 認證成功"
                ],
                ascii_header="SUCCESS",
                ascii_font="slant",
                border_style="green",
                log_level="SUCCESS"
            )
            
            return {"access_token": token, "token_type": "bearer"}
        else:
            # 登入失敗
            logger.ascii_block(
                "登入失敗",
                [
                    f"❌ 用戶: {username}",
                    f"🚫 原因: 認證資訊無效",
                    f"⚠️  風險等級: 中",
                    f"🔍 建議: 檢查用戶名和密碼",
                    f"📊 失敗次數: 需要追蹤"
                ],
                ascii_header="FAILED",
                ascii_font="doom",
                border_style="red",
                log_level="WARNING"
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認證失敗"
            )
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """驗證 Token"""
        try:
            payload = jwt.decode(
                credentials.credentials,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            username = payload.get("username")
            
            logger.debug(f"Token 驗證成功: {username}")
            return username
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token 已過期")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 已過期"
            )
        except jwt.InvalidTokenError:
            logger.error("無效的 Token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="無效的 Token"
            )

auth_service = AuthService()

@app.post("/login")
async def login_endpoint(username: str, password: str):
    return await auth_service.login(username, password)

@app.get("/protected")
async def protected_route(current_user: str = Depends(auth_service.verify_token)):
    logger.info(f"受保護路由訪問: {current_user}")
    return {"message": f"Hello {current_user}", "status": "authorized"}
```

### 資料庫操作日誌

```python
from typing import List, Optional
import asyncio

class UserService:
    """用戶服務"""
    
    async def create_user(self, user_data: dict):
        """創建用戶"""
        logger.ascii_header("CREATE USER", font="standard", border_style="green")
        
        logger.block(
            "創建用戶請求",
            [
                f"👤 用戶名: {user_data.get('username')}",
                f"📧 郵箱: {user_data.get('email')}",
                f"🏷️  角色: {user_data.get('role', 'user')}",
                f"🕐 創建時間: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            ],
            border_style="blue"
        )
        
        try:
            # 模擬資料庫操作
            await asyncio.sleep(0.1)  # 模擬資料庫延遲
            
            # 模擬驗證
            if not user_data.get('username'):
                raise ValueError("用戶名不能為空")
            
            if not user_data.get('email'):
                raise ValueError("郵箱不能為空")
            
            # 模擬成功創建
            user_id = hash(user_data['username']) % 10000
            
            logger.ascii_block(
                "用戶創建成功",
                [
                    f"✅ 用戶 ID: {user_id}",
                    f"👤 用戶名: {user_data['username']}",
                    f"📧 郵箱: {user_data['email']}",
                    f"🎯 狀態: 已激活",
                    f"📊 資料庫: 已同步"
                ],
                ascii_header="CREATED",
                ascii_font="slant",
                border_style="green",
                log_level="SUCCESS"
            )
            
            return {"user_id": user_id, "status": "created"}
            
        except Exception as e:
            logger.ascii_block(
                "用戶創建失敗",
                [
                    f"❌ 錯誤: {str(e)}",
                    f"📝 用戶資料: {user_data}",
                    f"🔍 需要檢查: 輸入驗證",
                    f"💾 資料庫狀態: 未變更"
                ],
                ascii_header="FAILED",
                ascii_font="doom", 
                border_style="red",
                log_level="ERROR"
            )
            
            raise HTTPException(
                status_code=400,
                detail=f"創建用戶失敗: {str(e)}"
            )
    
    async def get_users(self, limit: int = 10, offset: int = 0):
        """獲取用戶列表"""
        logger.info(f"查詢用戶列表: limit={limit}, offset={offset}")
        
        # 模擬資料庫查詢
        await asyncio.sleep(0.05)
        
        users = [
            {"id": i, "username": f"user{i}", "email": f"user{i}@example.com"}
            for i in range(offset, offset + limit)
        ]
        
        logger.block(
            "用戶查詢結果",
            [
                f"📊 查詢條件: limit={limit}, offset={offset}",
                f"📈 返回數量: {len(users)}",
                f"⏱️  查詢時間: 0.05s",
                f"💾 快取狀態: 未使用"
            ],
            border_style="blue"
        )
        
        return users

user_service = UserService()

@app.post("/users")
async def create_user_endpoint(user_data: dict):
    return await user_service.create_user(user_data)

@app.get("/users")
async def get_users_endpoint(limit: int = 10, offset: int = 0):
    return await user_service.get_users(limit, offset)
```

## 📈 性能監控

### API 性能追蹤

```python
import asyncio
from functools import wraps
from time import perf_counter

def performance_monitor(func):
    """性能監控裝飾器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = perf_counter()
        
        try:
            result = await func(*args, **kwargs)
            end_time = perf_counter()
            execution_time = end_time - start_time
            
            # 根據執行時間決定警告級別
            if execution_time > 1.0:
                color = "red"
                level = "WARNING"
                status = "⚠️  緩慢"
            elif execution_time > 0.5:
                color = "yellow"
                level = "WARNING" 
                status = "⚠️  偏慢"
            else:
                color = "green"
                level = "INFO"
                status = "✅ 正常"
            
            logger.block(
                f"函數執行監控: {func.__name__}",
                [
                    f"⏱️  執行時間: {execution_time:.3f}s",
                    f"📊 狀態: {status}",
                    f"🎯 函數: {func.__name__}",
                    f"📈 效能等級: {'優秀' if execution_time < 0.1 else '良好' if execution_time < 0.5 else '需優化'}"
                ],
                border_style=color,
                log_level=level
            )
            
            return result
            
        except Exception as e:
            end_time = perf_counter()
            execution_time = end_time - start_time
            
            logger.ascii_block(
                "函數執行異常",
                [
                    f"❌ 函數: {func.__name__}",
                    f"💥 異常: {str(e)}",
                    f"⏱️  執行時間: {execution_time:.3f}s",
                    f"🔍 需要調查: 異常原因"
                ],
                ascii_header="EXCEPTION",
                ascii_font="doom",
                border_style="red",
                log_level="ERROR"
            )
            
            raise
    
    return wrapper

@app.get("/slow-endpoint")
@performance_monitor
async def slow_endpoint():
    """模擬緩慢的端點"""
    logger.info("開始執行緩慢操作...")
    await asyncio.sleep(2)  # 模擬緩慢操作
    return {"message": "操作完成", "duration": "2 seconds"}

@app.get("/fast-endpoint")
@performance_monitor
async def fast_endpoint():
    """模擬快速的端點"""
    logger.info("執行快速操作")
    return {"message": "快速響應", "duration": "immediate"}
```

## 🔧 配置管理

### 環境配置

```python
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    """應用設定"""
    
    app_name: str = "Pretty Loguru FastAPI"
    app_version: str = "1.0.1"
    debug: bool = False
    log_level: str = "INFO"
    log_folder: str = "api_logs"
    
    # 資料庫設定
    database_url: str = "postgresql://localhost/mydb"
    
    # Redis 設定
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()

@app.on_event("startup")
async def startup_with_config():
    """使用配置啟動"""
    
    # 根據環境配置日誌
    if settings.debug:
        create_logger(preset="debug", folder=settings.log_folder)
    else:
        create_logger(preset="production", folder=settings.log_folder)
    
    logger.ascii_header("CONFIG LOADED", font="standard", border_style="cyan")
    
    logger.block(
        "應用配置",
        [
            f"📱 應用名稱: {settings.app_name}",
            f"📦 版本: {settings.app_version}",
            f"🔧 除錯模式: {'啟用' if settings.debug else '停用'}",
            f"📊 日誌級別: {settings.log_level}",
            f"📁 日誌目錄: {settings.log_folder}",
            f"🗄️  資料庫: {settings.database_url.split('@')[0]}@***",
            f"🔴 Redis: {settings.redis_url}"
        ],
        border_style="green"
    )

@app.get("/config")
async def get_config():
    """獲取應用配置"""
    logger.info("請求應用配置資訊")
    
    config_info = {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "log_level": settings.log_level
    }
    
    logger.block(
        "配置資訊請求",
        [f"{key}: {value}" for key, value in config_info.items()],
        border_style="blue"
    )
    
    return config_info
```

## 🚀 完整應用範例

結合所有功能的完整 FastAPI 應用：

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pretty_loguru import create_logger
import uvicorn
import time
import asyncio

# 初始化應用
app = FastAPI(
    title="Pretty Loguru FastAPI Demo",
    description="展示 pretty-loguru 與 FastAPI 整合的完整範例",
    version="1.0.1"
)

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加日誌中間件
app.add_middleware(PrettyLoguruMiddleware)

@app.on_event("startup")
async def startup():
    """應用啟動"""
    create_logger(preset="development", folder="fastapi_complete_logs")
    
    logger.ascii_block(
        "FastAPI 應用啟動完成",
        [
            "🚀 服務名稱: Pretty Loguru FastAPI Demo",
            "📦 版本: 1.0.1",
            "🌐 CORS: 已啟用",
            "📝 日誌中間件: 已載入",
            "🔧 認證系統: 已初始化",
            "💾 服務連接: 準備就緒",
            "⚡ 狀態: 完全啟動"
        ],
        ascii_header="ONLINE",
        ascii_font="block",
        border_style="green",
        log_level="SUCCESS"
    )

@app.on_event("shutdown")
async def shutdown():
    """應用關閉"""
    logger.ascii_block(
        "FastAPI 應用關閉",
        [
            "🛑 正在關閉服務...",
            "💾 清理資源連接",
            "📝 保存日誌狀態",
            "🔒 關閉認證系統",
            "✅ 優雅關閉完成"
        ],
        ascii_header="SHUTDOWN",
        ascii_font="standard",
        border_style="yellow",
        log_level="WARNING"
    )

# 包含所有路由
app.include_router(auth_router, prefix="/auth", tags=["認證"])
app.include_router(user_router, prefix="/users", tags=["用戶"])
app.include_router(monitor_router, prefix="/monitor", tags=["監控"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None  # 使用 pretty-loguru 而不是 uvicorn 的日誌
    )
```

這個完整的 FastAPI 範例展示了 pretty-loguru 在實際 Web 應用中的強大功能，提供專業級的日誌記錄和監控能力！