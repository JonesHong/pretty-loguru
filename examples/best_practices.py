"""
Pretty Loguru 最佳實踐和常見陷阱

展示正確的使用方式，避免常見錯誤，提供生產環境的最佳實踐
"""

import os
import time
from pathlib import Path
from pretty_loguru import create_logger

print("=== Pretty Loguru 最佳實踐指南 ===\n")

# === 最佳實踐1: 模塊級別的 logger 管理 ===
print("--- 最佳實踐1: 模塊級別的 logger 管理 ---")

# ✅ 好的做法: 每個模塊一個 logger
class UserService:
    def __init__(self):
        self.logger = create_logger(
            "user_service",
            log_path="./logs",
            preset="daily",
            subdirectory="services"
        )
    
    def create_user(self, email: str):
        # ✅ 使用 bind 添加上下文
        user_logger = self.logger.bind(email=email, operation="create_user")
        user_logger.info("開始創建用戶")
        
        # 模擬業務邏輯
        if "@" not in email:
            user_logger.error("無效的電子郵件地址")
            return False
            
        user_logger.success("用戶創建成功")
        return True

# ❌ 錯誤做法: 全局共享一個 logger
# global_logger = create_logger("global")  # 不要這樣做！

user_service = UserService()
user_service.create_user("test@example.com")
user_service.create_user("invalid-email")

# === 最佳實踐2: 敏感信息處理 ===
print("\n--- 最佳實踐2: 敏感信息處理 ---")

class AuthService:
    def __init__(self):
        self.logger = create_logger("auth_service", log_path="./logs")
    
    def login(self, username: str, password: str):
        # ✅ 好的做法: 不記錄敏感信息
        self.logger.info(f"用戶登錄嘗試: {username}")
        
        # ❌ 錯誤做法: 記錄密碼
        # self.logger.info(f"登錄: {username}, 密碼: {password}")  # 絕對不要這樣做！
        
        # ✅ 好的做法: 只記錄必要的審計信息
        login_logger = self.logger.bind(
            username=username,
            ip_address="192.168.1.100",  # 從請求獲取
            user_agent="Mozilla/5.0..."   # 從請求獲取
        )
        
        # 模擬登錄邏輯
        if password == "correct_password":
            login_logger.success("登錄成功")
        else:
            login_logger.warning("登錄失敗: 密碼錯誤")

auth_service = AuthService()
auth_service.login("john_doe", "correct_password")
auth_service.login("john_doe", "wrong_password")

# === 最佳實踐3: 性能優化 ===
print("\n--- 最佳實踐3: 性能優化 ---")

performance_logger = create_logger("performance", log_path="./logs")

# ✅ 好的做法: 避免昂貴的字符串操作
def process_data_good(items):
    """性能優化的日誌記錄"""
    start_time = time.time()
    
    # ✅ 只在需要時格式化字符串
    if performance_logger._core.min_level <= 10:  # DEBUG 級別
        performance_logger.debug(f"開始處理 {len(items)} 個項目")
    
    # 業務邏輯...
    time.sleep(0.1)  # 模擬處理時間
    
    execution_time = time.time() - start_time
    performance_logger.bind(
        item_count=len(items),
        execution_time=f"{execution_time:.3f}s"
    ).info("數據處理完成")

# ❌ 錯誤做法: 昂貴的字符串操作
def process_data_bad(items):
    """性能較差的日誌記錄"""
    # ❌ 總是執行昂貴的字符串格式化，即使不會記錄
    expensive_debug_info = "\n".join([f"項目 {i}: {item}" for i, item in enumerate(items)])
    performance_logger.debug(f"詳細信息:\n{expensive_debug_info}")

process_data_good(["item1", "item2", "item3"])

# === 最佳實踐4: 錯誤處理和重試邏輯 ===
print("\n--- 最佳實踐4: 錯誤處理和重試邏輯 ---")

class ApiClient:
    def __init__(self):
        self.logger = create_logger("api_client", log_path="./logs")
        self.max_retries = 3
    
    def call_api(self, endpoint: str):
        """帶重試的 API 調用"""
        for attempt in range(self.max_retries):
            try:
                # ✅ 為每次嘗試創建專用 logger
                attempt_logger = self.logger.bind(
                    endpoint=endpoint,
                    attempt=attempt + 1,
                    max_retries=self.max_retries
                )
                
                attempt_logger.info("API 調用開始")
                
                # 模擬 API 調用
                import random
                if random.random() < 0.7:  # 70% 失敗率
                    raise Exception("API 暫時不可用")
                
                attempt_logger.success("API 調用成功")
                return True
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    attempt_logger.warning(f"API 調用失敗，將重試: {str(e)}")
                    time.sleep(0.1)  # 等待後重試
                else:
                    # ✅ 最後一次失敗時記錄完整錯誤
                    attempt_logger.opt(exception=True).error(f"API 調用最終失敗: {str(e)}")
                    return False

api_client = ApiClient()
api_client.call_api("/api/users")

# === 最佳實踐5: 資源管理 ===
print("\n--- 最佳實踐5: 資源管理 ---")

# ✅ 好的做法: 適當的資源管理
class DatabaseManager:
    def __init__(self):
        self.logger = create_logger(
            "database_manager",
            log_path="./logs",
            preset="daily",
            rotation="100 MB",  # 避免日誌文件過大
            retention="7 days"   # 自動清理舊日誌
        )
    
    def __enter__(self):
        self.logger.info("數據庫連接開啟")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"數據庫操作異常: {exc_val}")
        else:
            self.logger.info("數據庫連接正常關閉")

# 使用上下文管理器
with DatabaseManager() as db:
    db.logger.info("執行數據庫操作")

# === 常見陷阱1: 日誌級別混亂 ===
print("\n--- 常見陷阱1: 日誌級別使用不當 ---")

trap_logger = create_logger("trap_demo", log_path="./logs")

# ❌ 錯誤: 級別使用不當
# trap_logger.error("用戶登錄成功")  # 成功事件不應該用 error 級別
# trap_logger.info("系統崩潰")      # 嚴重問題不應該用 info 級別

# ✅ 正確: 適當的級別使用
trap_logger.info("用戶登錄成功")     # 正常事件用 info
trap_logger.success("訂單提交成功")  # 成功事件用 success  
trap_logger.warning("磁碟空間不足")  # 警告用 warning
trap_logger.error("數據庫連接失敗")  # 錯誤用 error
trap_logger.critical("系統內存耗盡") # 嚴重問題用 critical

# === 常見陷阱2: 過度日誌記錄 ===
print("\n--- 常見陷阱2: 過度日誌記錄 ---")

# ❌ 錯誤: 過度記錄
def bad_logging_example():
    trap_logger.debug("進入函數")
    trap_logger.debug("初始化變量")
    x = 10
    trap_logger.debug(f"x = {x}")
    y = 20
    trap_logger.debug(f"y = {y}")
    result = x + y
    trap_logger.debug(f"計算結果: {result}")
    trap_logger.debug("退出函數")
    return result

# ✅ 正確: 適度記錄關鍵信息
def good_logging_example():
    trap_logger.debug("開始計算操作")
    result = 10 + 20
    trap_logger.info(f"計算完成，結果: {result}")
    return result

good_logging_example()

# === 最佳實踐6: 測試友好的日誌 ===
print("\n--- 最佳實踐6: 測試友好的日誌 ---")

class TestableService:
    def __init__(self, logger=None):
        # ✅ 允許注入 logger，便於測試
        self.logger = logger or create_logger("testable_service", log_path="./logs")
    
    def process(self, data):
        self.logger.info(f"處理數據: {len(data)} 項")
        return len(data) * 2

# 在測試中可以注入 mock logger
service = TestableService()
result = service.process([1, 2, 3, 4, 5])

# === 最佳實踐總結 ===
print("\n--- 最佳實踐總結 ---")

best_practices_summary = """
🎯 Pretty Loguru 最佳實踐總結:

✅ 應該做的:
1. 每個模塊/類使用專用的 logger
2. 使用 bind() 添加結構化上下文
3. 適當選擇日誌級別
4. 避免記錄敏感信息（密碼、令牌等）
5. 使用預設配置簡化設置
6. 在生產環境設置適當的輪轉和保留策略
7. 使用 subdirectory 組織日誌文件
8. 為關鍵操作添加性能監控日誌

❌ 不應該做的:
1. 全局共享一個 logger 實例
2. 記錄敏感信息
3. 過度記錄調試信息
4. 在性能敏感路徑中進行昂貴的字符串操作
5. 忽略日誌文件的大小和清理
6. 混亂使用日誌級別
7. 在異常處理中丟失堆疊追蹤信息

🚀 生產環境建議:
1. 使用 WARNING 或 ERROR 級別減少日誌量
2. 設置適當的 rotation 和 retention
3. 使用 proxy 模式支持動態配置
4. 監控日誌文件大小和磁碟使用
5. 定期審查日誌內容，確保不包含敏感信息
"""

print(best_practices_summary)

print("\n=== 最佳實踐指南完成 ===")
print("遵循這些實踐可以讓你的日誌系統更加健壯和高效！")