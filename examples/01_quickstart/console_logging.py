#!/usr/bin/env python3
"""
Console Logging - 控制台日誌輸出

學習如何使用 Pretty-Loguru 進行控制台日誌輸出。
了解不同的日誌等級和目標導向方法。

運行方式：
    python console_logging.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger

def basic_console_logging():
    """基本控制台日誌輸出"""
    print("📟 基本控制台日誌輸出")
    print("-" * 30)
    
    # 創建一個 logger
    logger = create_logger("console_demo")
    
    # 各種日誌等級
    logger.debug("這是除錯訊息")
    logger.info("這是資訊訊息")
    logger.success("這是成功訊息")
    logger.warning("這是警告訊息")
    logger.error("這是錯誤訊息")
    logger.critical("這是嚴重錯誤訊息")

def target_console_logging():
    """不同 logger 的控制台日誌"""
    print("\n🎯 不同 logger 的控制台日誌")
    print("-" * 30)
    
    # 創建不同用途的 logger
    auth_logger = create_logger("auth")
    api_logger = create_logger("api")
    db_logger = create_logger("database")
    
    # 模擬不同模組的日誌
    auth_logger.info("用戶登入成功")
    api_logger.success("API 調用完成")
    db_logger.warning("數據庫連接池使用率較高")
    api_logger.error("API 調用失敗")

def formatted_console_logging():
    """格式化控制台日誌"""
    print("\n✨ 格式化控制台日誌")
    print("-" * 30)
    
    logger = create_logger("formatted_demo")
    
    # 使用變數格式化
    user_name = "張三"
    user_age = 25
    
    logger.info(f"用戶 {user_name} 已登入，年齡：{user_age}")
    
    # 使用字典格式化
    data = {"action": "登入", "status": "成功", "time": "2025-07-07 14:00:00"}
    logger.success(f"操作完成：{data}")
    
    # 長訊息換行
    long_message = "這是一個很長的日誌訊息，用來演示 Pretty-Loguru 如何處理長文本。即使訊息很長，也能保持良好的可讀性。"
    logger.info(long_message)

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 控制台日誌範例")
    print("=" * 40)
    
    # 1. 基本控制台日誌
    basic_console_logging()
    
    # 2. 目標導向日誌
    target_console_logging()
    
    # 3. 格式化日誌
    formatted_console_logging()
    
    print("\n" + "=" * 40)
    print("✅ 控制台日誌範例完成！")
    print("💡 接下來可以學習：")
    print("   - file_logging.py：檔案輸出")
    print("   - ../02_basics/：更多基礎功能")

if __name__ == "__main__":
    main()