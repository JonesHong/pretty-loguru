"""
Pretty-Loguru 改進版應用範例
- 按模組分資料夾存儲日誌
- 設定每天產生一個日誌檔案
- 開發日誌僅顯示在控制台
"""
import os
import time
from datetime import datetime
from pathlib import Path
import random
import json
from typing import Dict, List, Optional

# 確保本地路徑優先
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')
# 導入 pretty_loguru
from pretty_loguru import logger, logger_start, print_ascii_header


def init_module_logger(module_name):
    """
    為每個模組初始化獨立的日誌配置
    
    Args:
        module_name: 模組名稱，將作為子目錄名稱
    
    Returns:
        str: 日誌檔案路徑
    """
    log_file_path = logger_start(
        service_name=module_name,     # 指定服務名稱
        subdirectory=module_name,     # 指定子目錄，實現按模組分資料夾
        log_name_preset="daily",      # 使用每日一檔模式，檔名格式為 {date}_{process_id}.log
    )
    
    # 記錄初始化訊息
    logger.info(f"模組 {module_name} 日誌系統已初始化")
    logger.dev_info(f"開發模式: 日誌檔案路徑 {log_file_path}")
    
    return log_file_path


class UserService:
    """用戶服務模組"""
    
    def __init__(self):
        # 初始化模組專用的日誌配置
        self.log_path = init_module_logger("user_service")
        print_ascii_header("User Service", font="standard")
        
        # 模擬用戶資料庫
        self.users = {}
    
    def register_user(self, username: str, email: str, password: str):
        """註冊新用戶"""
        # 開發日誌 - 僅顯示在控制台，不寫入檔案
        logger.dev_info(f"收到註冊請求 - 用戶名: {username}, 電子郵件: {email}")
        logger.dev_debug(f"註冊詳情 - 密碼長度: {len(password)}, 時間: {datetime.now().isoformat()}")
        
        # 檢查用戶是否已存在
        if username in self.users:
            logger.warning(f"註冊失敗 - 用戶名 {username} 已存在")
            return {"success": False, "error": "用戶名已存在"}
        
        # 模擬註冊處理
        time.sleep(0.2)
        
        # 創建用戶（實際應用中應對密碼進行加密）
        user_data = {
            "username": username,
            "email": email,
            "password": "****",  # 記錄中不保存實際密碼
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.users[username] = user_data
        
        # 標準日誌 - 同時記錄到控制台和檔案
        logger.success(f"用戶 {username} 註冊成功")
        
        # 審計日誌 - 僅寫入檔案，不顯示在控制台
        logger.file_info(f"新用戶註冊: {username}, 電子郵件: {email}, IP: 192.168.1.1")
        
        return {"success": True, "user": {k: v for k, v in user_data.items() if k != "password"}}
    
    def login(self, username: str, password: str):
        """用戶登入"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"收到登入請求 - 用戶名: {username}")
        
        # 檢查用戶是否存在
        if username not in self.users:
            logger.warning(f"登入失敗 - 用戶名 {username} 不存在")
            return {"success": False, "error": "用戶名或密碼錯誤"}
        
        # 模擬密碼驗證（實際應用中應使用安全的密碼驗證方法）
        if password != "password":  # 簡化示例
            logger.warning(f"登入失敗 - 用戶 {username} 密碼錯誤")
            
            # 審計日誌 - 僅寫入檔案
            logger.file_warning(f"登入失敗: 用戶 {username}, 原因: 密碼錯誤, IP: 192.168.1.1")
            
            return {"success": False, "error": "用戶名或密碼錯誤"}
        
        # 登入成功
        logger.success(f"用戶 {username} 登入成功")
        
        # 審計日誌 - 僅寫入檔案
        logger.file_info(f"用戶登入: {username}, IP: 192.168.1.1, 時間: {datetime.now().isoformat()}")
        
        return {"success": True, "user": {k: v for k, v in self.users[username].items() if k != "password"}}
    
    def get_all_users(self):
        """獲取所有用戶"""
        # 開發日誌 - 僅顯示在控制台
        user_count = len(self.users)
        logger.dev_info(f"請求獲取所有用戶 - 共 {user_count} 個用戶")
        
        # 準備用戶資料（移除敏感資訊）
        safe_users = {}
        for username, user_data in self.users.items():
            safe_users[username] = {k: v for k, v in user_data.items() if k != "password"}
        
        # 標準日誌
        logger.info(f"返回所有用戶資料 - 共 {user_count} 個用戶")
        
        return safe_users


class ProductService:
    """產品服務模組"""
    
    def __init__(self):
        # 初始化模組專用的日誌配置
        self.log_path = init_module_logger("product_service")
        print_ascii_header("Product Service", font="standard")
        
        # 模擬產品資料庫
        self.products = {
            f"prod_{i}": {
                "id": f"prod_{i}",
                "name": f"測試產品 {i}",
                "category": random.choice(["電子", "服飾", "食品", "書籍"]),
                "price": round(random.uniform(100, 10000), 2),
                "stock": random.randint(0, 100),
                "created_at": datetime.now().isoformat()
            } for i in range(1, 50)
        }
    
    def search_products(self, keyword: str, category: Optional[str] = None, max_results: int = 10, page: int = 1):
        """搜索產品"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"產品搜索請求 - 關鍵字: {keyword}, 類別: {category}, 頁碼: {page}, 每頁數量: {max_results}")
        
        # 執行搜索
        start_time = time.time()
        
        # 模擬搜索操作
        results = []
        for product_id, product in self.products.items():
            if keyword.lower() in product["name"].lower():
                if category is None or product["category"] == category:
                    results.append(product)
        
        # 分頁
        start_idx = (page - 1) * max_results
        end_idx = start_idx + max_results
        paged_results = results[start_idx:end_idx]
        
        # 計算搜索時間
        search_time = time.time() - start_time
        
        # 開發日誌 - 詳細搜索資訊
        logger.dev_debug(f"搜索詳情 - 總結果數: {len(results)}, 返回結果數: {len(paged_results)}, 耗時: {search_time:.4f}秒")
        
        # 標準日誌
        logger.info(f"產品搜索完成 - 關鍵字: '{keyword}', 找到 {len(results)} 個結果, 耗時: {search_time:.4f}秒")
        
        # 性能監控 (僅控制台)
        if search_time > 0.5:
            logger.console_warning(f"搜索性能警告 - 耗時: {search_time:.4f}秒，超過閾值 0.5秒")
        
        # 審計日誌 (僅文件)
        logger.file_info(f"產品搜索: 關鍵字='{keyword}', 類別='{category}', 結果數={len(results)}, 頁={page}, 耗時={search_time:.4f}秒")
        
        return {
            "total": len(results),
            "page": page,
            "page_size": max_results,
            "results": paged_results
        }
    
    def get_product(self, product_id: str):
        """獲取產品詳情"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"請求產品詳情 - 產品ID: {product_id}")
        
        # 檢查產品是否存在
        if product_id not in self.products:
            logger.warning(f"產品不存在 - 產品ID: {product_id}")
            return {"success": False, "error": "產品不存在"}
        
        # 獲取產品資訊
        product_data = self.products[product_id]
        
        # 標準日誌
        logger.info(f"返回產品詳情 - 產品: {product_data['name']}")
        
        return {"success": True, "product": product_data}
    
    def create_product(self, name: str, category: str, price: float, stock: int):
        """創建新產品"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"創建產品請求 - 名稱: {name}, 類別: {category}, 價格: {price}, 庫存: {stock}")
        
        # 生成產品ID
        product_id = f"prod_{len(self.products) + 1}"
        
        # 模擬產品創建
        product_data = {
            "id": product_id,
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "created_at": datetime.now().isoformat()
        }
        
        self.products[product_id] = product_data
        
        # 標準日誌
        logger.success(f"產品創建成功 - ID: {product_id}, 名稱: {name}")
        
        # 審計日誌 - 僅寫入檔案
        logger.file_info(f"新產品創建: ID={product_id}, 名稱='{name}', 類別='{category}', 價格={price}, 庫存={stock}")
        
        return {"success": True, "product": product_data}


class OrderService:
    """訂單服務模組"""
    
    def __init__(self, product_service):
        # 初始化模組專用的日誌配置
        self.log_path = init_module_logger("order_service")
        print_ascii_header("Order Service", font="standard")
        
        # 產品服務依賴
        self.product_service = product_service
        
        # 模擬訂單資料庫
        self.orders = {}
    
    def create_order(self, user_id: str, items: List[Dict]):
        """創建訂單"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"創建訂單請求 - 用戶ID: {user_id}, 商品數量: {len(items)}")
        logger.dev_debug(f"訂單詳情 - 商品: {json.dumps(items, ensure_ascii=False)}")
        
        # 生成訂單ID
        order_id = f"order_{len(self.orders) + 1}"
        
        # 計算總金額並檢查庫存
        total_amount = 0
        order_items = []
        
        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            
            # 獲取產品資訊
            product_result = self.product_service.get_product(product_id)
            if not product_result["success"]:
                logger.error(f"創建訂單失敗 - 產品不存在: {product_id}")
                return {"success": False, "error": f"產品不存在: {product_id}"}
            
            product = product_result["product"]
            
            # 檢查庫存
            if product["stock"] < quantity:
                logger.warning(f"創建訂單失敗 - 產品 {product_id} 庫存不足: 需要 {quantity}, 實際 {product['stock']}")
                return {"success": False, "error": f"產品 {product['name']} 庫存不足"}
            
            # 計算金額
            item_total = product["price"] * quantity
            total_amount += item_total
            
            # 添加到訂單項目
            order_items.append({
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "item_total": item_total
            })
            
            # 更新庫存（實際應用中應使用事務保證一致性）
            self.product_service.products[product_id]["stock"] -= quantity
        
        # 創建訂單
        order_data = {
            "id": order_id,
            "user_id": user_id,
            "items": order_items,
            "total_amount": total_amount,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
        
        self.orders[order_id] = order_data
        
        # 標準日誌
        logger.success(f"訂單創建成功 - ID: {order_id}, 用戶: {user_id}, 金額: {total_amount}")
        
        # 審計日誌 - 僅寫入檔案
        logger.file_info(f"新訂單: ID={order_id}, 用戶ID={user_id}, 商品數={len(items)}, 總金額={total_amount}")
        
        return {"success": True, "order": order_data}
    
    def get_order(self, order_id: str):
        """獲取訂單詳情"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"請求訂單詳情 - 訂單ID: {order_id}")
        
        # 檢查訂單是否存在
        if order_id not in self.orders:
            logger.warning(f"訂單不存在 - 訂單ID: {order_id}")
            return {"success": False, "error": "訂單不存在"}
        
        # 獲取訂單資訊
        order_data = self.orders[order_id]
        
        # 標準日誌
        logger.info(f"返回訂單詳情 - 訂單ID: {order_id}, 用戶: {order_data['user_id']}")
        
        return {"success": True, "order": order_data}
    
    def get_user_orders(self, user_id: str):
        """獲取用戶所有訂單"""
        # 開發日誌 - 僅顯示在控制台
        logger.dev_info(f"請求用戶訂單 - 用戶ID: {user_id}")
        
        # 查找用戶訂單
        user_orders = [order for order in self.orders.values() if order["user_id"] == user_id]
        
        # 標準日誌
        logger.info(f"返回用戶訂單 - 用戶ID: {user_id}, 訂單數: {len(user_orders)}")
        
        return {"success": True, "orders": user_orders}


def simulate_application():
    """模擬完整應用流程"""
    print_ascii_header("E-Commerce System Simulation", font="big", border_style="green")
    
    # 初始化各服務
    user_service = UserService()
    product_service = ProductService()
    order_service = OrderService(product_service)
    
    # 模擬用戶註冊和登入
    print("\n1. 用戶註冊和登入:")
    
    # 註冊用戶
    register_result = user_service.register_user(
        "john_doe", 
        "john@example.com", 
        "password123"
    )
    
    # 模擬登入
    login_result = user_service.login("john_doe", "password")
    
    # 模擬搜索產品
    print("\n2. 搜索產品:")
    
    # 搜索所有產品
    all_products = product_service.search_products(
        keyword="測試", 
        max_results=5
    )
    
    # 搜索特定類別
    category_products = product_service.search_products(
        keyword="測試", 
        category="電子",
        max_results=3
    )
    
    # 模擬創建訂單
    print("\n3. 創建訂單:")
    
    # 選擇商品
    cart_items = [
        {"product_id": list(product_service.products.keys())[0], "quantity": 2},
        {"product_id": list(product_service.products.keys())[1], "quantity": 1}
    ]
    
    # 創建訂單
    order_result = order_service.create_order(
        user_id="john_doe",
        items=cart_items
    )
    
    # 查詢訂單
    print("\n4. 查詢訂單:")
    
    # 獲取訂單詳情
    if order_result["success"]:
        order_details = order_service.get_order(order_result["order"]["id"])
    
    # 獲取用戶所有訂單
    user_orders = order_service.get_user_orders("john_doe")
    
    # 系統運行摘要
    print("\n5. 系統運行摘要:")
    
    logger.block(
        "系統運行摘要", 
        [
            f"運行時間: {datetime.now().isoformat()}",
            f"用戶總數: {len(user_service.users)}",
            f"產品總數: {len(product_service.products)}",
            f"訂單總數: {len(order_service.orders)}",
            f"--------------------",
            f"用戶服務日誌: {user_service.log_path}",
            f"產品服務日誌: {product_service.log_path}",
            f"訂單服務日誌: {order_service.log_path}"
        ],
        border_style="blue",
        log_level="INFO"
    )
    
    print_ascii_header("Simulation Complete", font="banner3-D", border_style="green")


if __name__ == "__main__":
    simulate_application()
