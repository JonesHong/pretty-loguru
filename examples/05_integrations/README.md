# FastAPI 整合範例

這個目錄包含了 Pretty-Loguru 與 FastAPI 框架整合的完整演示範例，展示如何在 FastAPI 應用中實現專業級的日誌記錄。

## 📁 檔案列表

### 1. simple_api.py
**基本整合範例**
- FastAPI 與 Pretty-Loguru 的基本整合
- 自動請求/響應日誌記錄
- API 路由中的日誌使用
- 錯誤處理和狀態記錄

```bash
python simple_api.py
# 訪問 http://localhost:8012
```

### 2. middleware_demo.py
**中間件完整功能**
- LoggingMiddleware 的完整展示
- 自動請求/響應記錄
- 性能監控和分析
- 錯誤追蹤和處理

```bash
python middleware_demo.py
# 訪問 http://localhost:8001
```

### 3. dependency_injection.py
**依賴注入範例**
- Logger 依賴注入模式
- 不同服務使用不同 logger
- Logger 重用和管理
- 微服務架構最佳實踐

```bash
python dependency_injection.py
# 訪問 http://localhost:8002
```

### 4. simple_one_liner.py
**一行程式碼整合**
- 最簡單的整合方式
- 快速開始模板
- 最小配置範例

### 5. test_uvicorn_logging.py
**Uvicorn 日誌整合**
- Uvicorn 服務器日誌配置
- 生產環境日誌設置
- 日誌輪轉和管理

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install fastapi uvicorn
```

### 2. 基本使用
```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

app = FastAPI()
logger = create_logger("my_api", log_dir="./logs")
integrate_fastapi(app, logger)

@app.get("/")
async def root():
    logger.info("處理首頁請求")
    return {"message": "Hello World"}
```

### 3. 啟動應用
```python
import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000)
```

## 🔧 核心功能

### 自動請求記錄
- 請求方法和路徑
- 客戶端 IP 和端口
- 請求頭部資訊
- 請求體內容（可選）

### 自動響應記錄
- 響應狀態碼
- 處理時間統計
- 響應頭部資訊
- 響應體內容（可選）

### 錯誤追蹤
- 異常詳細資訊
- 錯誤發生時間
- 錯誤上下文
- 錯誤分類和處理

### 性能監控
- 請求處理時間
- 響應時間分析
- 慢請求檢測
- 性能瓶頸識別

## 🎯 整合方式

### 1. 自動中間件整合
```python
from pretty_loguru.integrations.fastapi import integrate_fastapi

# 完整自動整合
integrate_fastapi(app, logger)
```

### 2. 手動中間件配置
```python
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

setup_fastapi_logging(
    app=app,
    logger_instance=logger,
    middleware=True,
    exclude_paths=["/health", "/metrics"]
)
```

### 3. 依賴注入模式
```python
from pretty_loguru.integrations.fastapi import get_logger_dependency
from pretty_loguru import create_logger

logger = create_logger("my_api")
logger_dep = get_logger_dependency(logger)

@app.get("/items/")
async def get_items(logger: PrettyLogger = Depends(logger_dep)):
    logger.info("Getting items")
    return {"items": []}
```

## ⚙️ 配置選項

### 排除路徑
排除不需要記錄的端點：
```python
integrate_fastapi(
    app, logger,
    exclude_paths=["/health", "/metrics", "/docs"]
)
```

### 排除方法
排除特定 HTTP 方法：
```python
integrate_fastapi(
    app, logger,
    exclude_methods=["OPTIONS", "HEAD"]
)
```

### 請求體記錄
啟用請求體記錄（謹慎使用）：
```python
setup_fastapi_logging(
    app, logger,
    log_request_body=True,
    log_response_body=False
)
```

## 📊 日誌格式

### 請求日誌
```
2024-01-15 10:30:45 | INFO | Request [1705123445.123]: GET /users/123 from 127.0.0.1:12345
```

### 響應日誌
```
2024-01-15 10:30:45 | INFO | Response [1705123445.123]: 200 in 0.045s
```

### 錯誤日誌
```
2024-01-15 10:30:45 | ERROR | Response [1705123445.123]: Exception after 0.023s - HTTPException: User not found
```

## 🏗️ 實際應用場景

### 1. API 網關
- 所有請求統一日誌記錄
- 流量分析和監控
- 安全審計記錄

### 2. 微服務架構
- 服務間調用追蹤
- 分散式日誌收集
- 服務健康監控

### 3. 生產環境監控
- 性能指標收集
- 錯誤率統計
- 使用者行為分析

## 🔒 安全考量

### 敏感資訊保護
- 自動過濾敏感頭部
- 請求體敏感資料遮蔽
- 日誌存取權限控制

### 預設排除的敏感頭部
- `authorization`
- `cookie`
- `set-cookie`

## 📈 性能最佳化

### 1. 生產環境建議
- 關閉請求體記錄
- 設置適當的日誌等級
- 配置日誌輪轉

### 2. 排除健康檢查
- 排除 `/health` 端點
- 排除 `/metrics` 端點
- 排除 `/docs` 和 `/openapi.json`

### 3. 非同步處理
- 所有日誌操作都是非同步的
- 不會阻塞請求處理
- 最小性能影響

## 🔧 故障排除

### 常見問題

1. **FastAPI 未安裝**
   ```bash
   pip install fastapi uvicorn
   ```

2. **日誌檔案權限問題**
   確保日誌目錄有寫入權限

3. **中間件順序問題**
   確保 LoggingMiddleware 在其他中間件之前添加

## 📚 相關文檔

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [Uvicorn 配置](https://www.uvicorn.org/)
- [中間件開發指南](https://fastapi.tiangolo.com/tutorial/middleware/)

---

**注意**: 這些範例適合開發和測試環境，生產環境請根據實際需求調整配置。
