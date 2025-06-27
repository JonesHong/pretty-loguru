"""
Pretty Loguru 真實業務場景範例

展示在實際開發中的常見使用場景和最佳實踐
"""

import time
import random
from pathlib import Path
from pretty_loguru import create_logger
from pretty_loguru.factory.proxy import LoggerProxy

print("=== 真實業務場景範例 ===\n")

# === 場景1: Web API 服務日誌 ===
print("--- 場景1: Web API 服務 ---")
api_logger = create_logger(
    "api_service",
    log_path="./logs",
    preset="daily",
    subdirectory="api",
    level="INFO"
)

def simulate_api_request(endpoint: str, user_id: str = None):
    """模擬 API 請求處理"""
    request_id = f"req_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # 使用 bind 添加請求上下文
    request_logger = api_logger.bind(
        request_id=request_id,
        endpoint=endpoint,
        user_id=user_id
    )
    
    request_logger.info(f"收到請求: {endpoint}")
    
    # 模擬處理時間
    process_time = random.uniform(0.1, 2.0)
    time.sleep(0.1)  # 實際中這是業務邏輯處理時間
    
    # 模擬不同的響應結果
    status_code = random.choices([200, 201, 400, 404, 500], weights=[70, 10, 10, 5, 5])[0]
    
    if status_code >= 500:
        request_logger.error(f"服務器錯誤 - Status: {status_code}, 處理時間: {process_time:.2f}s")
    elif status_code >= 400:
        request_logger.warning(f"客戶端錯誤 - Status: {status_code}, 處理時間: {process_time:.2f}s")
    else:
        request_logger.success(f"請求成功 - Status: {status_code}, 處理時間: {process_time:.2f}s")

# 模擬一些 API 請求
simulate_api_request("/api/users", "user123")
simulate_api_request("/api/orders", "user456")
simulate_api_request("/api/products")

# === 場景2: 數據處理管道 ===
print("\n--- 場景2: 數據處理管道 ---")
data_logger = create_logger(
    "data_pipeline",
    log_path="./logs", 
    preset="hourly",
    subdirectory="etl",
    level="DEBUG"
)

def process_data_batch(batch_id: str, size: int):
    """模擬數據批次處理"""
    batch_logger = data_logger.bind(batch_id=batch_id, batch_size=size)
    
    batch_logger.info(f"開始處理數據批次，大小: {size}")
    
    # 階段1: 數據驗證
    batch_logger.debug("執行數據驗證...")
    invalid_records = random.randint(0, size // 10)
    if invalid_records > 0:
        batch_logger.warning(f"發現 {invalid_records} 條無效記錄")
    
    # 階段2: 數據轉換
    batch_logger.debug("執行數據轉換...")
    
    # 階段3: 數據載入
    batch_logger.debug("載入到目標系統...")
    
    success_rate = (size - invalid_records) / size * 100
    batch_logger.success(f"批次處理完成，成功率: {success_rate:.1f}%")

process_data_batch("batch_001", 1000)
process_data_batch("batch_002", 2500)

# === 場景3: 錯誤監控和告警 ===
print("\n--- 場景3: 錯誤監控和告警 ---")
monitor_logger = create_logger(
    "system_monitor",
    log_path="./logs",
    preset="daily",
    subdirectory="monitoring",
    use_proxy=True
)

def check_system_health():
    """模擬系統健康檢查"""
    services = ["database", "redis", "elasticsearch", "message_queue"]
    
    monitor_logger.ascii_header("HEALTH CHECK", font="standard", border_style="blue")
    print(f"Type of monitor_logger: {type(monitor_logger)}")
    print(f"Is monitor_logger an instance of LoggerProxy: {isinstance(monitor_logger, LoggerProxy)}")
    
    for service in services:
        # 模擬服務檢查
        is_healthy = random.choice([True, True, True, False])  # 75% 正常
        response_time = random.uniform(10, 500)
        
        service_logger = monitor_logger.bind(service=service, response_time=f"{response_time:.1f}ms")
        print(f"Type of service_logger: {type(service_logger)}")
        print(f"Is service_logger an instance of LoggerProxy: {isinstance(service_logger, LoggerProxy)}")
        
        if is_healthy:
            service_logger.success(f"{service} 服務正常")
        else:
            service_logger.error(f"{service} 服務異常！需要立即處理")
            
            # 記錄詳細錯誤信息到檔案
            service_logger.file_error(f"詳細錯誤報告: {service} 連接超時，響應時間: {response_time:.1f}ms")

check_system_health()

# === 場景4: 用戶行為追蹤 ===
print("\n--- 場景4: 用戶行為追蹤 ---")
behavior_logger = create_logger(
    "user_behavior",
    log_path="./logs",
    preset="daily", 
    subdirectory="analytics"
)

def track_user_action(user_id: str, action: str, metadata: dict = None):
    """追蹤用戶行為"""
    user_logger = behavior_logger.bind(
        user_id=user_id,
        action=action,
        timestamp=time.time()
    )
    
    if metadata:
        for key, value in metadata.items():
            user_logger = user_logger.bind(**{key: value})
    
    user_logger.info(f"用戶行為: {action}")

# 模擬用戶行為
track_user_action("user123", "login", {"device": "mobile", "location": "Taiwan"})
track_user_action("user123", "view_product", {"product_id": "P001", "category": "electronics"})
track_user_action("user123", "add_to_cart", {"product_id": "P001", "quantity": 2})
track_user_action("user123", "checkout", {"order_total": 299.99, "payment_method": "credit_card"})

# === 場景5: 性能監控 ===
print("\n--- 場景5: 性能監控 ---")
perf_logger = create_logger(
    "performance",
    log_path="./logs",
    preset="hourly",
    subdirectory="performance"
)

def monitor_function_performance(func_name: str):
    """性能監控裝飾器範例"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            perf_logger.debug(f"開始執行 {func_name}")
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                perf_logger.bind(
                    function=func_name,
                    execution_time=f"{execution_time:.3f}s"
                ).info(f"{func_name} 執行完成")
                
                # 如果執行時間過長，記錄警告
                if execution_time > 1.0:
                    perf_logger.warning(f"{func_name} 執行時間過長: {execution_time:.3f}s")
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                perf_logger.error(f"{func_name} 執行失敗: {str(e)}, 耗時: {execution_time:.3f}s")
                raise
        return wrapper
    return decorator

@monitor_function_performance("database_query")
def slow_database_query():
    """模擬慢查詢"""
    time.sleep(random.uniform(0.5, 1.5))
    return "查詢結果"

@monitor_function_performance("fast_cache_lookup")
def fast_cache_lookup():
    """模擬快速緩存查找"""
    time.sleep(random.uniform(0.01, 0.1))
    return "緩存數據"

# 執行性能監控
slow_database_query()
fast_cache_lookup()

print("\n=== 真實場景示例完成 ===")
print("這些範例展示了在生產環境中的實際使用方式")