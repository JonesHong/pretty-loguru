#!/usr/bin/env python3
"""
Target Logging - 目標導向日誌方法

這個範例展示 pretty-loguru 的目標導向功能：
1. console_* 方法 - 僅控制台輸出
2. file_* 方法 - 僅檔案輸出  
3. 實際使用場景和最佳實踐

運行方式：
    python target_logging.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time

def simulate_user_registration():
    """模擬用戶註冊流程"""
    logger = create_logger("user_service", log_path="./logs")
    
    print("=== 用戶註冊流程範例 ===")
    
    # 1. 用戶開始註冊
    logger.console_info("開始註冊流程...")
    logger.file_info("用戶註冊開始 - IP: 192.168.1.100, UserAgent: Chrome/91.0")
    
    # 2. 驗證階段
    logger.console_info("驗證輸入資料...")
    logger.file_debug("驗證 email 格式：user@example.com")
    logger.file_debug("檢查密碼強度：符合要求")
    logger.file_debug("檢查用戶名是否重複：可用")
    
    # 3. 資料庫操作
    logger.file_info("開始資料庫操作")
    time.sleep(0.1)  # 模擬處理時間
    logger.file_success("用戶資料插入成功 - UserID: 12345")
    
    # 4. 用戶看到的結果
    logger.console_success("註冊成功！歡迎加入我們的平台")
    
    # 5. 系統記錄
    logger.file_info("註冊流程完成 - 總耗時: 0.1秒")

def simulate_error_handling():
    """模擬錯誤處理"""
    logger = create_logger("payment_service", log_path="./logs")
    
    print("\n=== 錯誤處理範例 ===")
    
    try:
        # 模擬支付處理
        logger.console_info("處理支付請求...")
        logger.file_info("支付請求 - 金額: $99.99, 卡號: ****1234")
        
        # 模擬錯誤
        raise ValueError("信用卡已過期")
        
    except ValueError as e:
        # 用戶看到的友善訊息
        logger.console_error("支付失敗，請檢查您的信用卡資訊")
        
        # 系統記錄詳細錯誤
        logger.file_error(f"支付錯誤 - {str(e)}")
        logger.file_debug("錯誤堆疊追蹤", exc_info=True)

def demonstrate_all_levels():
    """展示所有日誌級別的目標導向方法"""
    logger = create_logger("demo_service", log_path="./logs")
    
    print("\n=== 所有目標導向方法展示 ===")
    
    print("\n控制台專用方法 (console_*):")
    logger.console_debug("除錯訊息 - 僅顯示在控制台")
    logger.console_info("資訊訊息 - 僅顯示在控制台") 
    logger.console_warning("警告訊息 - 僅顯示在控制台")
    logger.console_error("錯誤訊息 - 僅顯示在控制台")
    logger.console_success("成功訊息 - 僅顯示在控制台")
    
    print("\n檔案專用方法 (file_*) - 這些訊息只寫入檔案:")
    logger.file_debug("詳細除錯資訊 - 僅寫入檔案")
    logger.file_info("系統資訊 - 僅寫入檔案")
    logger.file_warning("系統警告 - 僅寫入檔案") 
    logger.file_error("系統錯誤 - 僅寫入檔案")
    logger.file_success("系統成功 - 僅寫入檔案")
    
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