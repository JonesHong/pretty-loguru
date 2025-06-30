# 04_fastapi - 真實 Web 應用範例

這個目錄展示 pretty-loguru 與 FastAPI 的深度整合，提供真實可運行的 Web 應用範例。

## 🎯 學習目標

- 掌握 FastAPI 與 pretty-loguru 的整合
- 理解中間件的自動日誌記錄功能
- 學會使用 logger 依賴注入模式
- 了解 Web 應用的日誌最佳實踐

## 📋 前置準備

安裝必要依賴：
```bash
pip install fastapi uvicorn
# 或
pip install -r requirements.txt
```

## 📚 範例列表

### 1. simple_api.py - 基本 FastAPI 整合
**學習重點**: FastAPI 與 pretty-loguru 的基本結合

```bash
python simple_api.py
```

**功能展示**:
- 基本的 API 路由日誌記錄
- 啟動/關閉事件記錄
- 錯誤處理和日誌記錄
- 用戶友善的控制台訊息 vs 詳細的檔案記錄

**測試方式**:
```bash
# 啟動服務後，在新終端中測試
curl http://localhost:8000/
curl http://localhost:8000/users/123
curl http://localhost:8000/users/999  # 測試 404 錯誤
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com"}'
```

### 2. middleware_demo.py - 完整中間件功能
**學習重點**: LoggingMiddleware 的自動請求/響應記錄

```bash
python middleware_demo.py
```

**功能展示**:
- 自動記錄所有 API 請求和響應
- 性能監控（響應時間）
- 請求體和響應體記錄
- 錯誤追蹤和異常處理

**測試方式**:
```bash
# 服務運行在 http://localhost:8001
curl http://localhost:8001/
curl http://localhost:8001/slow        # 測試慢速請求
curl http://localhost:8001/error       # 測試錯誤處理
curl -X POST http://localhost:8001/data -H "Content-Type: application/json" -d '{"test":"data"}'
```

### 3. dependency_injection.py - Logger 依賴注入
**學習重點**: 微服務架構中的 logger 管理

```bash
python dependency_injection.py
```

**功能展示**:
- 不同服務使用獨立的 logger
- Logger 依賴注入模式
- 服務間日誌隔離
- 多服務架構的日誌管理

**測試方式**:
```bash
# 服務運行在 http://localhost:8002
curl -X POST http://localhost:8002/auth/login
curl http://localhost:8002/users/profile
curl -X POST http://localhost:8002/orders/create
curl http://localhost:8002/logs/stats
```

## 🔧 核心功能

### 基本整合
```python
from pretty_loguru import create_logger
from fastapi import FastAPI

logger = create_logger("my_api", log_path="./logs")
app = FastAPI()

@app.get("/")
async def root():
    logger.info("處理首頁請求")
    return {"message": "Hello World"}
```

### 中間件設置
```python
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

setup_fastapi_logging(
    app,
    logger_instance=logger,
    middleware=True,
    log_request_body=True,
    log_response_body=True,
    exclude_paths=["/health"]
)
```

### 依賴注入
```python
from pretty_loguru.integrations.fastapi import get_logger_dependency

user_logger_dep = get_logger_dependency(name="user_service")

@app.get("/users")
async def get_users(logger: EnhancedLogger = Depends(user_logger_dep)):
    logger.info("查詢用戶列表")
    return {"users": []}
```

## 📁 生成的日誌檔案

運行範例後，您會看到：
```
logs/
├── simple_api_YYYYMMDD-HHMMSS.log          # 基本 API 日誌
├── middleware_demo_YYYYMMDD-HHMMSS.log     # 中間件示範日誌
├── dependency_app_YYYYMMDD-HHMMSS.log      # 主應用日誌
├── auth_service_YYYYMMDD-HHMMSS.log        # 認證服務日誌
├── user_service_YYYYMMDD-HHMMSS.log        # 用戶服務日誌
└── order_service_YYYYMMDD-HHMMSS.log       # 訂單服務日誌
```

## 🌟 最佳實踐

### 1. 分層日誌記錄
```python
# 用戶看到的簡潔訊息
logger.console_info("處理您的請求...")

# 系統記錄的詳細資訊
logger.file_info(f"API 請求 - 端點: {request.url}, 用戶: {user_id}")
```

### 2. 錯誤處理
```python
try:
    result = process_data()
    logger.success("資料處理完成")
except Exception as e:
    logger.error(f"處理失敗: {str(e)}")
    logger.file_error("詳細錯誤資訊", exc_info=True)
    raise HTTPException(status_code=500, detail="處理失敗")
```

### 3. 性能監控
```python
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"請求處理完成 - 耗時: {process_time:.3f}秒")
    return response
```

## 🚀 快速啟動指南

1. **安裝依賴**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **運行基本範例**:
   ```bash
   python simple_api.py
   ```

3. **查看 Swagger 文檔**:
   ```
   http://localhost:8000/docs
   ```

4. **檢查日誌輸出**:
   ```bash
   ls ./logs/
   tail -f ./logs/*.log
   ```

## 🔗 相關範例

- **01_basics/** - 了解基本概念
- **03_presets/** - 日誌檔案管理和輪替
- **05_production/** - 生產環境配置

## ❓ 常見問題

**Q: 如何自訂中間件的記錄內容？**
A: 使用 `setup_fastapi_logging` 的參數控制，如 `log_request_body`, `exclude_paths` 等。

**Q: 如何在不同環境使用不同的日誌配置？**
A: 可以根據環境變數選擇不同的 preset 或配置參數。

**Q: 微服務架構下如何管理多個 logger？**
A: 使用依賴注入模式，每個服務使用獨立的 logger 實例，便於追蹤和分析。