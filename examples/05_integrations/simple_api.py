#!/usr/bin/env python3
"""
Simple FastAPI Integration - 基本 FastAPI 整合

這個範例展示：
1. FastAPI 與 pretty-loguru 的基本整合
2. API 路由中的日誌記錄
3. 真實可運行的 Web 應用

運行方式：
    pip install fastapi uvicorn
    python simple_api.py
    
然後訪問：
    http://localhost:8000
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/users/123
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from fastapi import FastAPI, HTTPException
    import uvicorn
except ImportError:
    print("請先安裝依賴：pip install fastapi uvicorn")
    exit(1)

from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

# 創建 FastAPI 應用
app = FastAPI(
    title="Pretty Loguru Demo API",
    description="展示 pretty-loguru 與 FastAPI 整合的簡單範例",
    version="1.1.2"
)

# 創建 logger 並與 FastAPI 集成
logger = create_logger("simple_api", log_path="./logs/fastapi")
integrate_fastapi(app, logger)

# 模擬資料
users_db = {
    "123": {"name": "Alice", "email": "alice@example.com"},
    "456": {"name": "Bob", "email": "bob@example.com"},
}

@app.get("/")
async def root():
    """首頁 - 歡迎訊息"""
    logger.info("收到首頁請求")
    logger.info("用戶訪問了首頁")
    
    return {
        "message": "歡迎使用 Pretty Loguru Demo API!",
        "docs": "/docs",
        "endpoints": ["/users/{user_id}", "/health"]
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    logger.debug("健康檢查請求")
    logger.debug("系統狀態：正常運行")
    
    return {"status": "healthy", "service": "pretty-loguru-demo"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """獲取用戶資訊"""
    logger.info(f"請求用戶資訊：{user_id}")
    logger.info(f"查詢用戶 - ID: {user_id}")
    
    if user_id not in users_db:
        logger.warning(f"用戶不存在：{user_id}")
        logger.warning(f"404 錯誤 - 用戶 {user_id} 不存在")
        raise HTTPException(status_code=404, detail="用戶不存在")
    
    user = users_db[user_id]
    logger.success(f"成功返回用戶資訊：{user['name']}")
    logger.success(f"成功查詢用戶 {user_id} - {user['name']}")
    
    return {"user_id": user_id, **user}

@app.post("/users")
async def create_user(user_data: dict):
    """創建新用戶"""
    name = user_data.get("name")
    email = user_data.get("email")
    
    if not name or not email:
        logger.error("創建用戶失敗：缺少必要欄位")
        logger.error(f"創建用戶失敗 - 數據：{user_data}")
        raise HTTPException(status_code=400, detail="缺少 name 或 email 欄位")
    
    # 生成新用戶 ID
    new_id = str(len(users_db) + 1000)
    users_db[new_id] = {"name": name, "email": email}
    
    logger.success(f"創建新用戶成功：{name}")
    logger.success(f"新用戶創建 - ID: {new_id}, Name: {name}, Email: {email}")
    
    return {"user_id": new_id, "name": name, "email": email}

def main():
    """啟動應用"""
    print("=== FastAPI + Pretty Loguru 基本整合範例 ===")
    print("啟動服務中...")
    
    # 使用 uvicorn 啟動應用
    uvicorn.run(
        "simple_api:app",
        host="127.0.0.1",
        port=8012,
        reload=False,  # 生產環境建議設為 False
        log_level="warning"  # 降低 uvicorn 的日誌輸出
    )

if __name__ == "__main__":
    main()