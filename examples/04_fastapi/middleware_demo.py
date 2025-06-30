#!/usr/bin/env python3
"""
Middleware Demo - Pretty Loguru 中間件完整功能展示

這個範例展示：
1. LoggingMiddleware 的完整功能
2. 請求/響應自動記錄
3. 性能監控
4. 錯誤追蹤

運行方式：
    pip install fastapi uvicorn
    python middleware_demo.py
    
測試 API：
    curl http://localhost:8001/
    curl http://localhost:8001/slow
    curl http://localhost:8001/error
    curl -X POST http://localhost:8001/data -H "Content-Type: application/json" -d '{"test": "data"}'
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from fastapi import FastAPI, HTTPException, Request
    import uvicorn
except ImportError:
    print("請先安裝依賴：pip install fastapi uvicorn")
    exit(1)

from pretty_loguru import create_logger
import time
import asyncio

# 創建專用的 logger
logger = create_logger("middleware_demo", log_path="./logs")

# 創建 FastAPI 應用
app = FastAPI(
    title="Pretty Loguru Middleware Demo",
    description="展示 Pretty Loguru 中間件的完整功能",
    version="1.0.1"
)

# 添加自定義中間件進行日誌記錄
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """自定義請求日誌中間件"""
    # 排除健康檢查
    if request.url.path == "/health":
        return await call_next(request)
    
    start_time = time.time()
    client_host = request.client.host if request.client else "unknown"
    
    # 記錄請求
    logger.info(f"請求: {request.method} {request.url.path} from {client_host}")
    
    # 處理請求
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # 記錄響應
        logger.info(f"響應: {response.status_code} in {process_time:.3f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"請求處理失敗: {str(e)} after {process_time:.3f}s")
        raise

@app.get("/")
async def root():
    """首頁"""
    logger.info("處理首頁請求")
    return {"message": "中間件示範 API", "features": ["request_logging", "response_logging", "performance_monitoring"]}

@app.get("/slow")
async def slow_endpoint():
    """慢速端點 - 測試性能監控"""
    logger.info("開始處理慢速請求")
    
    # 模擬慢速處理
    await asyncio.sleep(2)
    
    logger.success("慢速請求處理完成")
    return {"message": "這是一個慢速端點", "processing_time": "2 seconds"}

@app.get("/error")
async def error_endpoint():
    """錯誤端點 - 測試錯誤追蹤"""
    logger.warning("即將產生錯誤")
    
    # 故意產生錯誤
    raise HTTPException(status_code=500, detail="這是一個示範錯誤")

@app.post("/data")
async def post_data(request: Request):
    """POST 端點 - 測試請求體記錄"""
    # 取得請求資料
    body = await request.json()
    
    logger.info(f"收到 POST 資料：{len(str(body))} 字符")
    logger.file_debug(f"POST 資料內容：{body}")
    
    # 處理資料
    result = {"received": body, "status": "processed", "timestamp": time.time()}
    
    logger.success("POST 資料處理完成")
    return result

@app.get("/health")
async def health():
    """健康檢查 - 不會被中間件記錄"""
    return {"status": "ok"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """用戶查詢 - 測試路徑參數記錄"""
    logger.info(f"查詢用戶：{user_id}")
    
    if user_id == "404":
        logger.warning(f"用戶 {user_id} 不存在")
        raise HTTPException(status_code=404, detail="用戶不存在")
    
    # 模擬用戶資料
    user_data = {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }
    
    logger.success(f"成功返回用戶 {user_id} 的資料")
    return user_data

@app.on_event("startup")
async def startup():
    """啟動事件"""
    logger.success("中間件示範 API 啟動成功")
    logger.console_success("🎯 中間件功能已啟用，所有 API 請求都會被自動記錄")
    print("\n" + "="*60)
    print("測試建議：")
    print("1. 訪問 http://localhost:8001/ - 正常請求")
    print("2. 訪問 http://localhost:8001/slow - 慢速請求 (2秒)")
    print("3. 訪問 http://localhost:8001/error - 錯誤請求")
    print("4. POST 到 http://localhost:8001/data - 測試請求體記錄")
    print("5. 檢查 ./logs/ 目錄中的詳細日誌")
    print("="*60)

def main():
    """啟動應用"""
    print("=== FastAPI + Pretty Loguru 中間件完整功能展示 ===")
    print("正在啟動服務...")
    
    # 使用 uvicorn 啟動
    uvicorn.run(
        "middleware_demo:app",
        host="127.0.0.1", 
        port=8001,
        reload=False,
        log_level="warning"  # 減少 uvicorn 自身的日誌輸出
    )

if __name__ == "__main__":
    main()