#!/usr/bin/env python3
"""
Error Handling - 錯誤處理最佳實踐

學習如何使用 Pretty-Loguru 進行錯誤處理和異常記錄。
了解錯誤日誌等級策略和堆疊追蹤優化。

運行方式：
    python error_handling.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import traceback

def basic_error_handling():
    """基本錯誤處理"""
    print("🚨 基本錯誤處理")
    print("-" * 30)
    
    logger = create_logger("error_demo", log_path="./logs/basics")
    
    try:
        # 模擬一個可能出錯的操作
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"除法錯誤：{e}")
        logger.debug(f"錯誤詳情：{traceback.format_exc()}")
    
    try:
        # 模擬另一個錯誤
        data = {"name": "張三"}
        age = data["age"]  # KeyError
    except KeyError as e:
        logger.error(f"鍵值錯誤：缺少必要的鍵 {e}")
        logger.warning("建議檢查輸入數據的完整性")

def exception_logging_with_context():
    """帶上下文的異常記錄"""
    print("\n📝 帶上下文的異常記錄")
    print("-" * 30)
    
    logger = create_logger("context_error", log_path="./logs/basics")
    
    def process_user_data(user_id, user_data):
        """處理用戶資料"""
        logger.info(f"開始處理用戶 {user_id} 的資料")
        
        try:
            # 驗證必要欄位
            required_fields = ["name", "email", "age"]
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"缺少必要欄位：{field}")
            
            # 驗證資料類型
            if not isinstance(user_data["age"], int):
                raise TypeError("年齡必須是整數")
            
            if user_data["age"] < 0:
                raise ValueError("年齡不能為負數")
            
            logger.success(f"用戶 {user_id} 資料驗證成功")
            return True
            
        except (ValueError, TypeError) as e:
            logger.error(f"用戶 {user_id} 資料驗證失敗：{e}")
            logger.debug(f"用戶資料：{user_data}")
            return False
        except Exception as e:
            logger.critical(f"用戶 {user_id} 處理時發生未預期錯誤：{e}")
            logger.debug(f"完整錯誤資訊：{traceback.format_exc()}")
            return False
    
    # 測試不同的錯誤情況
    test_cases = [
        (1, {"name": "張三", "email": "zhang@example.com", "age": 25}),  # 正常
        (2, {"name": "李四", "email": "li@example.com"}),  # 缺少 age
        (3, {"name": "王五", "email": "wang@example.com", "age": "二十五"}),  # 年齡類型錯誤
        (4, {"name": "趙六", "email": "zhao@example.com", "age": -5}),  # 年齡為負數
    ]
    
    for user_id, user_data in test_cases:
        process_user_data(user_id, user_data)

def error_classification():
    """錯誤分類和等級策略"""
    print("\n📊 錯誤分類和等級策略")
    print("-" * 30)
    
    logger = create_logger("error_classification", log_path="./logs/basics")
    
    def classify_and_log_error(error_type, error_msg, severity="error"):
        """分類並記錄錯誤"""
        prefix = {
            "user_error": "用戶操作錯誤",
            "system_error": "系統錯誤",
            "network_error": "網絡錯誤",
            "data_error": "數據錯誤",
            "auth_error": "認證錯誤"
        }
        
        full_msg = f"[{prefix.get(error_type, '未知錯誤')}] {error_msg}"
        
        if severity == "warning":
            logger.warning(full_msg)
        elif severity == "error":
            logger.error(full_msg)
        elif severity == "critical":
            logger.critical(full_msg)
        else:
            logger.info(full_msg)
    
    # 演示不同類型的錯誤
    classify_and_log_error("user_error", "用戶輸入了無效的郵箱格式", "warning")
    classify_and_log_error("system_error", "數據庫連接失敗", "error")
    classify_and_log_error("network_error", "API 調用超時", "error")
    classify_and_log_error("data_error", "數據格式不正確", "error")
    classify_and_log_error("auth_error", "認證令牌已過期", "critical")

def retry_with_logging():
    """帶日誌的重試機制"""
    print("\n🔄 帶日誌的重試機制")
    print("-" * 30)
    
    logger = create_logger("retry_demo", log_path="./logs/basics")
    
    def unreliable_function():
        """模擬不穩定的函數"""
        import random
        if random.random() < 0.7:  # 70% 機率失敗
            raise ConnectionError("網絡連接不穩定")
        return "操作成功"
    
    def retry_operation(operation, max_retries=3):
        """重試操作並記錄過程"""
        logger.info(f"開始執行操作，最大重試次數：{max_retries}")
        
        for attempt in range(max_retries + 1):
            try:
                result = operation()
                if attempt > 0:
                    logger.success(f"操作在第 {attempt + 1} 次嘗試時成功")
                else:
                    logger.success("操作首次嘗試成功")
                return result
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"第 {attempt + 1} 次嘗試失敗：{e}，將在 1 秒後重試")
                    import time
                    time.sleep(1)
                else:
                    logger.error(f"操作失敗，已達到最大重試次數 {max_retries}")
                    logger.critical(f"最終錯誤：{e}")
                    raise
    
    # 測試重試機制
    try:
        result = retry_operation(unreliable_function)
        logger.info(f"最終結果：{result}")
    except Exception as e:
        logger.error(f"操作最終失敗：{e}")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 錯誤處理範例")
    print("=" * 40)
    
    # 1. 基本錯誤處理
    basic_error_handling()
    
    # 2. 帶上下文的異常記錄
    exception_logging_with_context()
    
    # 3. 錯誤分類和等級策略
    error_classification()
    
    # 4. 帶日誌的重試機制
    retry_with_logging()
    
    print("\n" + "=" * 40)
    print("✅ 錯誤處理範例完成！")
    print("💡 錯誤處理最佳實踐：")
    print("   - 使用適當的日誌等級")
    print("   - 記錄足夠的上下文資訊")
    print("   - 分類不同類型的錯誤")
    print("   - 在重試機制中記錄過程")

if __name__ == "__main__":
    main()