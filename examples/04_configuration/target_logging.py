#!/usr/bin/env python3
"""
Target Logging - 目標導向日誌方法

這個範例展示 pretty-loguru 的目標導向功能：
1. `log_to_targets()` - 每則訊息選擇輸出目的地
2. 實際使用場景和最佳實踐
3. 實際使用場景和最佳實踐

運行方式：
    python target_logging.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets
import time

def simulate_user_registration():
    """模擬用戶註冊流程"""
    logger = create_logger("user_service", log_dir="./logs")
    
    print("=== 用戶註冊流程範例 ===")
    
    # 1. 用戶開始註冊
    log_to_targets(logger, "開始註冊流程...", level="INFO", console_only=True)
    log_to_targets(logger, "用戶註冊開始 - IP: 192.168.1.100, UserAgent: Chrome/91.0", level="INFO", file_only=True)
    
    # 2. 驗證階段
    log_to_targets(logger, "驗證輸入資料...", level="INFO", console_only=True)
    log_to_targets(logger, "驗證 email 格式：user@example.com", level="DEBUG", file_only=True)
    log_to_targets(logger, "檢查密碼強度：符合要求", level="DEBUG", file_only=True)
    log_to_targets(logger, "檢查用戶名是否重複：可用", level="DEBUG", file_only=True)
    
    # 3. 資料庫操作
    log_to_targets(logger, "開始資料庫操作", level="INFO", file_only=True)
    time.sleep(0.1)  # 模擬處理時間
    log_to_targets(logger, "用戶資料插入成功 - UserID: 12345", level="SUCCESS", file_only=True)
    
    # 4. 用戶看到的結果
    log_to_targets(logger, "註冊成功！歡迎加入我們的平台", level="SUCCESS", console_only=True)
    
    # 5. 系統記錄
    log_to_targets(logger, "註冊流程完成 - 總耗時: 0.1秒", level="INFO", file_only=True)

def simulate_error_handling():
    """模擬錯誤處理"""
    logger = create_logger("payment_service", log_dir="./logs")
    
    print("\n=== 錯誤處理範例 ===")
    
    try:
        # 模擬支付處理
        log_to_targets(logger, "處理支付請求...", level="INFO", console_only=True)
        log_to_targets(logger, "支付請求 - 金額: $99.99, 卡號: ****1234", level="INFO", file_only=True)
        
        # 模擬錯誤
        raise ValueError("信用卡已過期")
        
    except ValueError as e:
        # 用戶看到的友善訊息
        log_to_targets(logger, "支付失敗，請檢查您的信用卡資訊", level="ERROR", console_only=True)
        
        # 系統記錄詳細錯誤
        logger.opt(exception=True, depth=1).bind(to_file_only=True).error(f"支付錯誤 - {str(e)}")

def demonstrate_all_levels():
    """展示所有日誌級別的目標導向方法"""
    logger = create_logger("demo_service", log_dir="./logs")
    
    print("\n=== 所有目標導向方法展示 ===")
    
    print("\n控制台專用 (console_only=True):")
    log_to_targets(logger, "除錯訊息 - 僅顯示在控制台", level="DEBUG", console_only=True)
    log_to_targets(logger, "資訊訊息 - 僅顯示在控制台", level="INFO", console_only=True)
    log_to_targets(logger, "警告訊息 - 僅顯示在控制台", level="WARNING", console_only=True)
    log_to_targets(logger, "錯誤訊息 - 僅顯示在控制台", level="ERROR", console_only=True)
    log_to_targets(logger, "成功訊息 - 僅顯示在控制台", level="SUCCESS", console_only=True)
    
    print("\n檔案專用 (file_only=True) - 這些訊息只寫入檔案:")
    log_to_targets(logger, "詳細除錯資訊 - 僅寫入檔案", level="DEBUG", file_only=True)
    log_to_targets(logger, "系統資訊 - 僅寫入檔案", level="INFO", file_only=True)
    log_to_targets(logger, "系統警告 - 僅寫入檔案", level="WARNING", file_only=True)
    log_to_targets(logger, "系統錯誤 - 僅寫入檔案", level="ERROR", file_only=True)
    log_to_targets(logger, "系統成功 - 僅寫入檔案", level="SUCCESS", file_only=True)
    
    print("\n檢查日誌檔案，您會發現更多詳細資訊！")

def main():
    print("=== Pretty Loguru 目標導向日誌範例 ===\n")
    
    # 1. 用戶註冊流程
    simulate_user_registration()
    
    # 2. 錯誤處理
    simulate_error_handling()
    
    # 3. 展示所有方法
    demonstrate_all_levels()
    
    print("\n" + "="*50)
    print("範例完成！")
    print("提示：檢查 './logs' 目錄中的檔案")
    print("您會發現檔案中記錄了更多詳細資訊")

if __name__ == "__main__":
    main()
