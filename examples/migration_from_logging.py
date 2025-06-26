"""
Pretty Loguru vs 標準 logging 對比範例

展示如何從標準 logging 遷移到 pretty-loguru，
包括功能對比和遷移指南
"""

import logging
import time
from pretty_loguru import create_logger

print("=== Pretty Loguru vs 標準 logging 對比 ===\n")

# === 對比1: 基本設置 ===
print("--- 對比1: 基本設置 ---")

print("\n【標準 logging 設置】:")
print("""
import logging

# 需要多行配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('my_app')
""")

# 標準 logging 實際設置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('standard_app.log'),
        logging.StreamHandler()
    ]
)
std_logger = logging.getLogger('my_app')

print("\n【Pretty Loguru 設置】:")
print("""
from pretty_loguru import create_logger

# 一行即可完成相同配置
logger = create_logger("my_app", log_path="./logs")
""")

# Pretty Loguru 設置
pretty_logger = create_logger("my_app", log_path="./logs")

print("\n測試日誌輸出:")
std_logger.info("標準 logging 的信息")
pretty_logger.info("Pretty Loguru 的信息")

# === 對比2: 日誌級別 ===
print("\n--- 對比2: 日誌級別對比 ---")

print("\n【標準 logging】:")
std_logger.debug("Debug 信息")
std_logger.info("Info 信息") 
std_logger.warning("Warning 信息")
std_logger.error("Error 信息")
std_logger.critical("Critical 信息")

print("\n【Pretty Loguru】:")
pretty_logger.debug("Debug 信息")
pretty_logger.info("Info 信息")
pretty_logger.warning("Warning 信息") 
pretty_logger.error("Error 信息")
pretty_logger.critical("Critical 信息")
pretty_logger.success("Success 信息")  # 額外的級別！

# === 對比3: 結構化日誌 ===
print("\n--- 對比3: 結構化日誌 ---")

print("\n【標準 logging - 需要手動格式化】:")
user_id = "12345"
action = "login"
std_logger.info(f"用戶操作: user_id={user_id}, action={action}")

print("\n【Pretty Loguru - 使用 bind】:")
user_logger = pretty_logger.bind(user_id=user_id, action=action)
user_logger.info("用戶操作")

# === 對比4: 異常處理 ===
print("\n--- 對比4: 異常處理 ---")

def divide_numbers_std(a, b):
    """使用標準 logging 的異常處理"""
    try:
        result = a / b
        std_logger.info(f"計算結果: {result}")
        return result
    except Exception as e:
        std_logger.error(f"計算錯誤: {str(e)}", exc_info=True)  # 需要 exc_info=True
        return None

def divide_numbers_pretty(a, b):
    """使用 Pretty Loguru 的異常處理"""
    try:
        result = a / b
        pretty_logger.info(f"計算結果: {result}")
        return result
    except Exception as e:
        pretty_logger.opt(exception=True).error(f"計算錯誤: {str(e)}")  # 自動包含堆疊追蹤
        return None

print("\n【標準 logging 異常】:")
divide_numbers_std(10, 0)

print("\n【Pretty Loguru 異常】:")
divide_numbers_pretty(10, 0)

# === 對比5: 多個日誌器管理 ===
print("\n--- 對比5: 多個日誌器管理 ---")

print("\n【標準 logging - 需要手動管理多個 logger】:")
# 標準 logging 需要為每個模塊單獨配置
db_std_logger = logging.getLogger('database')
api_std_logger = logging.getLogger('api')

# 需要單獨配置每個 logger
for logger in [db_std_logger, api_std_logger]:
    logger.setLevel(logging.INFO)
    if not logger.handlers:  # 避免重複添加
        handler = logging.FileHandler(f'{logger.name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

print("\n【Pretty Loguru - 簡單的多 logger 管理】:")
db_pretty_logger = create_logger("database", log_path="./logs", subdirectory="db")
api_pretty_logger = create_logger("api", log_path="./logs", subdirectory="api")

db_pretty_logger.info("數據庫連接成功")
api_pretty_logger.info("API 服務啟動")

# === 對比6: 日誌輪轉 ===
print("\n--- 對比6: 日誌輪轉配置 ---")

print("\n【標準 logging - 需要額外配置】:")
print("""
from logging.handlers import RotatingFileHandler

# 需要手動設置輪轉
rotating_handler = RotatingFileHandler(
    'app.log', 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
logger.addHandler(rotating_handler)
""")

print("\n【Pretty Loguru - 內建支持】:")
print("""
# 內建輪轉支持
rotating_logger = create_logger(
    "rotating_app", 
    log_path="./logs",
    preset="daily",          # 每日輪轉
    rotation="10 MB",        # 或按大小輪轉
    retention="7 days"       # 保留7天
)
""")

rotating_logger = create_logger(
    "rotating_app",
    log_path="./logs", 
    preset="daily",
    rotation="10 MB",
    retention="7 days"
)
rotating_logger.info("支持自動輪轉的日誌")

# === 對比7: 性能 ===
print("\n--- 對比7: 性能對比 ---")

def performance_test():
    """簡單的性能測試"""
    import time
    
    # 測試標準 logging
    start = time.time()
    for i in range(1000):
        std_logger.info(f"測試消息 {i}")
    std_time = time.time() - start
    
    # 測試 Pretty Loguru
    start = time.time()
    for i in range(1000):
        pretty_logger.info(f"測試消息 {i}")
    pretty_time = time.time() - start
    
    print(f"\n性能測試結果 (1000 條日誌):")
    print(f"標準 logging: {std_time:.3f} 秒")
    print(f"Pretty Loguru: {pretty_time:.3f} 秒")

# performance_test()  # 取消註釋以運行性能測試

# === 遷移指南 ===
print("\n--- 遷移指南 ---")

migration_guide = """
🚀 從標準 logging 遷移到 Pretty Loguru:

1. 基本替換:
   logging.getLogger('name') → create_logger('name')

2. 配置簡化:
   複雜的 handler/formatter 配置 → 簡單的參數設置

3. 新功能利用:
   - 使用 bind() 添加上下文
   - 使用 block() 和 ascii_header() 美化輸出
   - 使用預設配置快速設置

4. 最佳實踐:
   - 為不同模塊創建專用 logger
   - 使用 subdirectory 組織日誌文件
   - 在生產環境使用 proxy 模式

5. 逐步遷移策略:
   - 從新模塊開始使用 Pretty Loguru
   - 保持舊模塊的 logging 不變
   - 逐步替換關鍵模塊
"""

print(migration_guide)

# === 示例: 遷移前後對比 ===
print("\n--- 實際遷移示例 ---")

class DatabaseService:
    """數據庫服務示例"""
    
    def __init__(self, use_pretty_loguru=False):
        if use_pretty_loguru:
            self.logger = create_logger(
                "database_service",
                log_path="./logs",
                preset="daily",
                subdirectory="services"
            )
        else:
            self.logger = logging.getLogger("database_service")
    
    def connect(self, host: str, port: int):
        """連接數據庫"""
        if hasattr(self.logger, 'bind'):  # Pretty Loguru
            conn_logger = self.logger.bind(host=host, port=port)
            conn_logger.info("正在連接數據庫")
            conn_logger.success("數據庫連接成功")
        else:  # 標準 logging
            self.logger.info(f"正在連接數據庫: {host}:{port}")
            self.logger.info("數據庫連接成功")

print("\n【使用標準 logging】:")
db_service_std = DatabaseService(use_pretty_loguru=False)
db_service_std.connect("localhost", 5432)

print("\n【使用 Pretty Loguru】:")
db_service_pretty = DatabaseService(use_pretty_loguru=True)
db_service_pretty.connect("localhost", 5432)

print("\n=== 對比示例完成 ===")
print("建議: 從新項目開始使用 Pretty Loguru，舊項目可逐步遷移")