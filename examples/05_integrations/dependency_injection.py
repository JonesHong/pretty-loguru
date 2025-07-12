#!/usr/bin/env python3
"""
Dependency Injection - Logger 依賴注入範例

這個範例展示：
1. 如何在 FastAPI 中使用 logger 依賴注入
2. 不同服務使用不同的 logger
3. logger 的重用和管理
4. 最佳實踐

運行方式：
    pip install fastapi uvicorn
    python dependency_injection.py
    
測試 API：
    curl http://localhost:8002/auth/login
    curl http://localhost:8002/users/profile
    curl http://localhost:8002/orders/create
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from fastapi import FastAPI, Depends, HTTPException
    import uvicorn
except ImportError:
    print("請先安裝依賴：pip install fastapi uvicorn")
    exit(1)

from pretty_loguru import create_logger, EnhancedLogger,configure_uvicorn
from typing import Dict, Any
configure_uvicorn()
# 創建主應用 logger
main_logger = create_logger("dependency_app", log_path="./logs/fastapi")

# 創建不同服務的 logger 實例
auth_logger = create_logger("auth_service", log_path="./logs/fastapi") 
user_logger = create_logger("user_service", log_path="./logs/fastapi")
order_logger = create_logger("order_service", log_path="./logs/fastapi")

# 創建 logger 依賴函數
def get_auth_logger() -> EnhancedLogger:
    return auth_logger

def get_user_logger() -> EnhancedLogger:
    return user_logger

def get_order_logger() -> EnhancedLogger:
    return order_logger

# 創建 FastAPI 應用
app = FastAPI(
    title="Logger Dependency Injection Demo",
    description="展示 Pretty Loguru 依賴注入模式",
    version="1.0.1"
)

# === 認證服務路由 ===
@app.get("/auth/status")
async def auth_status(logger: EnhancedLogger = Depends(get_auth_logger)):
    """檢查認證服務狀態 - 使用認證服務 logger"""
    logger.info("檢查認證服務狀態")
    logger.file_info("認證服務狀態檢查")
    
    return {"status": "ok", "message": "認證服務運行正常"}
@app.post("/auth/login")
async def login(
    credentials: Dict[str, str] = {"username": "demo", "password": "123456"},
    logger: EnhancedLogger = Depends(get_auth_logger)
):
    """用戶登入 - 使用認證服務 logger"""
    username = credentials.get("username", "unknown")
    
    logger.info(f"用戶登入嘗試：{username}")
    logger.file_info(f"登入嘗試 - 用戶名：{username}, IP: client_ip")
    
    # 模擬認證邏輯
    if username == "demo" and credentials.get("password") == "123456":
        logger.success(f"用戶 {username} 登入成功")
        logger.file_success(f"成功登入 - 用戶：{username}")
        
        return {
            "status": "success",
            "message": "登入成功",
            "token": "demo_token_12345"
        }
    else:
        logger.warning(f"用戶 {username} 登入失敗")
        logger.file_warning(f"登入失敗 - 用戶：{username}, 原因：密碼錯誤")
        
        raise HTTPException(status_code=401, detail="用戶名或密碼錯誤")

@app.post("/auth/logout")
async def logout(logger: EnhancedLogger = Depends(get_auth_logger)):
    """用戶登出"""
    logger.info("用戶登出")
    logger.file_info("用戶登出操作")
    
    return {"status": "success", "message": "已成功登出"}

# === 用戶服務路由 ===
@app.get("/users/profile")
async def get_profile(
    user_id: str = "demo_user",
    logger: EnhancedLogger = Depends(get_user_logger)
):
    """獲取用戶資料 - 使用用戶服務 logger"""
    logger.info(f"查詢用戶資料：{user_id}")
    logger.file_info(f"資料查詢 - 用戶ID：{user_id}")
    
    # 模擬資料庫查詢
    profile = {
        "user_id": user_id,
        "name": "Demo User",
        "email": "demo@example.com",
        "created_at": "2024-01-01"
    }
    
    logger.success(f"成功獲取用戶 {user_id} 的資料")
    logger.file_success(f"資料查詢成功 - 用戶：{user_id}")
    
    return profile

@app.put("/users/profile")
async def update_profile(
    profile_data: Dict[str, Any],
    logger: EnhancedLogger = Depends(get_user_logger)
):
    """更新用戶資料"""
    user_id = profile_data.get("user_id", "unknown")
    
    logger.info(f"更新用戶資料：{user_id}")
    logger.file_info(f"資料更新 - 用戶ID：{user_id}, 更新欄位：{list(profile_data.keys())}")
    
    # 模擬更新邏輯
    logger.success(f"用戶 {user_id} 資料更新成功")
    logger.file_success(f"資料更新成功 - 用戶：{user_id}")
    
    return {"status": "success", "message": "資料更新成功"}

# === 訂單服務路由 ===
@app.post("/orders/create")
async def create_order(
    order_data: Dict[str, Any] = {"product": "demo_product", "quantity": 1, "price": 99.99},
    logger: EnhancedLogger = Depends(get_order_logger)
):
    """創建訂單 - 使用訂單服務 logger"""
    product = order_data.get("product", "unknown")
    quantity = order_data.get("quantity", 0)
    price = order_data.get("price", 0)
    
    logger.info(f"創建新訂單：{product} x {quantity}")
    logger.file_info(f"訂單創建 - 產品：{product}, 數量：{quantity}, 金額：${price}")
    
    # 模擬訂單處理
    order_id = f"ORDER_{hash(str(order_data)) % 10000:04d}"
    
    logger.success(f"訂單創建成功：{order_id}")
    logger.file_success(f"訂單處理成功 - 訂單ID：{order_id}, 總金額：${price * quantity}")
    
    return {
        "order_id": order_id,
        "status": "created",
        "total": price * quantity,
        "items": [{"product": product, "quantity": quantity, "price": price}]
    }

@app.get("/orders/{order_id}")
async def get_order(
    order_id: str,
    logger: EnhancedLogger = Depends(get_order_logger)
):
    """查詢訂單"""
    logger.info(f"查詢訂單：{order_id}")
    logger.file_info(f"訂單查詢 - 訂單ID：{order_id}")
    
    # 模擬訂單查詢
    if order_id.startswith("ORDER_"):
        order = {
            "order_id": order_id,
            "status": "completed",
            "total": 99.99,
            "created_at": "2024-06-28"
        }
        
        logger.success(f"訂單 {order_id} 查詢成功")
        logger.file_success(f"訂單查詢成功 - 訂單ID：{order_id}")
        
        return order
    else:
        logger.warning(f"訂單 {order_id} 不存在")
        logger.file_warning(f"訂單查詢失敗 - 訂單ID：{order_id} 不存在")
        
        raise HTTPException(status_code=404, detail="訂單不存在")

# === 主應用路由 ===
@app.get("/")
async def root():
    """首頁 - 使用主應用 logger"""
    main_logger.info("收到首頁請求")
    main_logger.console_info("歡迎使用依賴注入示範 API")
    
    return {
        "message": "Logger 依賴注入示範 API",
        "services": ["auth", "users", "orders"],
        "endpoints": {
            "auth": ["/auth/login", "/auth/logout","/auth/status"],
            "users": ["/users/profile"],
            "orders": ["/orders/create", "/orders/{order_id}"]
        }
    }

@app.get("/logs/stats")
async def get_log_stats():
    """日誌統計 - 展示不同 logger 的使用情況"""
    main_logger.info("查詢日誌統計")
    
    from pretty_loguru import list_loggers
    
    loggers = list_loggers()
    stats = {
        "total_loggers": len(loggers),
        "logger_names": loggers,
        "services": ["dependency_app", "auth_service", "user_service", "order_service"]
    }
    
    main_logger.success("日誌統計查詢完成")
    return stats

@app.on_event("startup")
async def startup():
    """啟動事件"""
    main_logger.success("依賴注入示範 API 啟動成功")
    main_logger.console_success("🔧 Logger 依賴注入已配置完成")
    
    print("\n" + "="*60)
    print("服務架構：")
    print("├── 主應用 (dependency_app)")
    print("├── 認證服務 (auth_service) - /auth/*")
    print("├── 用戶服務 (user_service) - /users/*")
    print("└── 訂單服務 (order_service) - /orders/*")
    print()
    print("每個服務都有獨立的 logger，記錄在不同的日誌檔案中")
    print("檢查 ./logs/ 目錄查看各服務的日誌檔案")
    print("="*60)

def main():
    """啟動應用"""
    host = "localhost"
    port = 8002
    print("=== FastAPI + Pretty Loguru 依賴注入範例 ===")
    print("正在啟動服務...")
    main_logger.info(f"FastAPI 服務啟動中: http://{host}:{port}")
    uvicorn.run(
        "dependency_injection:app",
        host=host,
        port=port,
        reload=False,
        log_level="warning"
    )

if __name__ == "__main__":
    main()