#!/usr/bin/env python3
"""
Ultra Simple FastAPI Integration - 超簡單 FastAPI 整合
一行代碼搞定所有日誌配置！

對比：
    舊版本需要：用戶自己創建 logger、配置中間件、設置 uvicorn、處理生命週期等
    新版本只需：一行 enable_pretty_logging(app) 即可

運行方式：
    pip install fastapi uvicorn
    python simple_one_liner.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    import uvicorn
    from fastapi import FastAPI
    from pretty_loguru import create_logger
    from pretty_loguru.integrations.fastapi import integrate_fastapi
except ImportError as e:
    print(f"請先安裝依賴：pip install fastapi uvicorn")
    print(f"錯誤詳情：{e}")
    exit(1)

# 創建 FastAPI 應用
app = FastAPI(title="簡化整合示例")

# 兩行代碼搞定所有日誌配置！包括：
# ✅ 創建 logger (用戶控制)
# ✅ 配置 FastAPI 中間件
# ✅ 配置 uvicorn 日誌攔截
# ✅ 排除健康檢查路徑
# ✅ 設置合理的默認值
logger = create_logger("simple_app", log_path="./logs")
integrate_fastapi(app, logger)

@app.get("/")
async def root():
    """首頁"""
    logger.info("用戶訪問首頁")
    return {"message": "Hello, World!", "status": "success"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """獲取用戶信息"""
    logger.info(f"查詢用戶 ID: {user_id}")
    if user_id == 404:
        logger.warning(f"用戶 {user_id} 不存在")
        return {"error": "User not found"}, 404
    
    logger.success(f"成功返回用戶 {user_id} 的信息")
    return {"user_id": user_id, "name": f"User{user_id}", "active": True}

@app.get("/health")
async def health():
    """健康檢查 (此路徑會被自動排除在日誌之外)"""
    return {"status": "healthy"}

if __name__ == "__main__":
    print("=== 一行代碼搞定 FastAPI + Pretty Loguru ===")
    print("啟動服務中...")
    
    # uvicorn 日誌已經被自動配置，無需額外設置
    uvicorn.run(app, host="127.0.0.1", port=8012)