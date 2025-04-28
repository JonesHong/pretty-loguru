"""
簡單可靠的隔離日誌測試範例

此範例展示如何確保每個日誌都寫入到正確的文件中，不會混合在一起
"""
import time
import random
import sys
from pathlib import Path

# 確保本地路徑優先
sys.path.insert(0, r'C:\work\pretty-loguru')
from pretty_loguru import create_logger

def test_multiple_loggers():
    """
    測試多個 logger 實例的完全隔離
    """
    print("\n=== 測試多個完全隔離的 logger 實例 ===\n")
    
    # 每個 logger 都有唯一的名稱、服務名稱和文件
    auth_logger = create_logger(
        name="auth_service",
        service_name="auth_service", 
        subdirectory="test/auth"
    )
    
    db_logger = create_logger(
        name="db_service",
        service_name="db_service", 
        subdirectory="test/db"
    )
    
    api_logger = create_logger(
        name="api_service",
        service_name="api_service", 
        subdirectory="test/api"
    )
    
    # 寫入測試訊息
    auth_logger.info("【AUTH】這條訊息應該只出現在 auth_service 日誌中")
    db_logger.info("【DB】這條訊息應該只出現在 db_service 日誌中")
    api_logger.info("【API】這條訊息應該只出現在 api_service 日誌中")
    
    # 寫入多條訊息以確認隔離
    for i in range(3):
        auth_logger.debug(f"【AUTH {i}】認證服務調試資訊")
        db_logger.debug(f"【DB {i}】數據庫服務調試資訊")
        api_logger.debug(f"【API {i}】API服務調試資訊")
    
    # 故意觸發一個錯誤
    try:
        db_logger.info("【DB】嘗試執行數據庫操作...")
        if random.random() > 0.2:  # 80% 的機率會出錯
            raise ValueError("模擬的數據庫錯誤")
        db_logger.success("【DB】操作成功")
    except Exception as e:
        db_logger.error(f"【DB】操作失敗: {str(e)}")
        api_logger.error(f"【API】因數據庫錯誤無法處理請求: {str(e)}")
    
    # 測試其他日誌級別
    auth_logger.warning("【AUTH】認證警告")
    db_logger.warning("【DB】數據庫警告")
    api_logger.warning("【API】API警告")
    
    return auth_logger, db_logger, api_logger


def test_same_function_loggers():
    """
    特別測試同一函數中創建的多個 logger
    """
    print("\n=== 測試同一函數內的多個 logger ===\n")
    
    # 創建兩個不同的 logger
    advanced_logger = create_logger(
        name="advanced_features",
        service_name="advanced", 
        subdirectory="test/advanced"
    )
    
    new_logger = create_logger(
        name="new_features",
        service_name="new", 
        subdirectory="test/new"
    )
    
    # 寫入測試訊息
    advanced_logger.info("【ADV】這條訊息應該只出現在 advanced 日誌中")
    new_logger.info("【NEW】這條訊息應該只出現在 new 日誌中")
    
    # 交替寫入以測試隔離性
    for i in range(3):
        advanced_logger.debug(f"【ADV {i}】進階功能調試訊息")
        new_logger.debug(f"【NEW {i}】新功能調試訊息")
    
    # 測試錯誤處理
    try:
        advanced_logger.info("【ADV】嘗試進階操作...")
        result = 100 / 0  # 故意製造錯誤
    except Exception as e:
        advanced_logger.error(f"【ADV】操作失敗: {str(e)}")
        new_logger.info("【NEW】幸好我使用的是另一個 logger")
    
    return advanced_logger, new_logger


def main():
    """主函數，運行所有測試"""
    print("\n===== 隔離日誌系統測試 =====\n")
    
    # 運行測試
    auth_logger, db_logger, api_logger = test_multiple_loggers()
    advanced_logger, new_logger = test_same_function_loggers()
    
    # 額外的交叉測試 - 確保不同函數之間的 logger 也是隔離的
    print("\n=== 跨函數 logger 測試 ===\n")
    
    auth_logger.critical("【AUTH】重要認證訊息")
    db_logger.critical("【DB】重要數據庫訊息")
    api_logger.critical("【API】重要API訊息")
    advanced_logger.critical("【ADV】重要進階訊息")
    new_logger.critical("【NEW】重要新功能訊息")
    
    # 使用區塊輸出
    auth_logger.block(
        title="認證系統狀態", 
        message_list=[
            "【AUTH】用戶登入: 50",
            "【AUTH】登入失敗: 3",
            "【AUTH】令牌生成: 47"
        ],
        border_style="green"
    )
    
    db_logger.block(
        title="數據庫系統狀態", 
        message_list=[
            "【DB】總連接數: 10",
            "【DB】活躍查詢: 5",
            "【DB】響應時間: 45ms"
        ],
        border_style="blue"
    )
    
    print("\n\n===== 測試完成 =====")
    print("請檢查以下目錄中的日誌文件，確認每個訊息都在正確的文件中:")
    print("- logs/test/auth/")
    print("- logs/test/db/")
    print("- logs/test/api/")
    print("- logs/test/advanced/")
    print("- logs/test/new/")
    
    print("\n每個文件中應該只有對應服務的訊息，標記為【SERVICE】")


if __name__ == "__main__":
    main()
