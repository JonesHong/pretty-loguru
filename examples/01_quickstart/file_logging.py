#!/usr/bin/env python3
"""
File Logging - 檔案日誌輸出

學習如何使用 Pretty-Loguru 進行檔案日誌輸出。
了解基本的檔案日誌配置和使用方式。

運行方式：
    python file_logging.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger

def basic_file_logging():
    """基本檔案日誌輸出"""
    print("📁 基本檔案日誌輸出")
    print("-" * 30)
    
    # 創建一個檔案 logger
    logger = create_logger(
        "file_demo",
        log_path="./logs/quickstart"  # 日誌會儲存在 logs/quickstart/ 目錄
    )
    
    # 寫入各種日誌等級
    logger.info("這是一個資訊日誌，會儲存到檔案中")
    logger.success("檔案日誌設定成功！")
    logger.warning("這是一個警告日誌")
    logger.error("這是一個錯誤日誌")
    
    print("✅ 日誌已儲存到 logs/quickstart/ 目錄")

def separate_file_logging():
    """分離的檔案日誌"""
    print("\n🎯 分離的檔案日誌")
    print("-" * 30)
    
    # 創建不同模組的 logger，分別寫入不同檔案
    error_logger = create_logger("error_log", log_path="./logs/quickstart")
    access_logger = create_logger("access_log", log_path="./logs/quickstart")
    
    # 記錄不同類型的事件
    access_logger.info("用戶訪問了首頁")
    access_logger.success("用戶成功登入")
    error_logger.warning("API 響應時間較長")
    error_logger.error("數據庫查詢失敗")
    
    print("✅ 分離日誌已儲存")

def custom_file_logging():
    """自定義檔案日誌"""
    print("\n⚙️ 自定義檔案日誌")
    print("-" * 30)
    
    # 使用自定義檔案名稱
    logger = create_logger(
        "custom_demo",
        log_path="./logs/quickstart",
        preset="simple"  # 使用簡單預設
    )
    
    # 記錄一些業務操作
    logger.info("用戶登入系統")
    logger.success("數據庫連接成功")
    logger.warning("記憶體使用率較高")
    logger.error("API 調用失敗")
    
    print("✅ 自定義日誌已儲存")

def check_log_files():
    """檢查生成的日誌檔案"""
    print("\n📋 檢查生成的日誌檔案")
    print("-" * 30)
    
    log_dir = Path("./logs/quickstart")
    if log_dir.exists():
        log_files = list(log_dir.glob("*.log"))
        if log_files:
            print(f"找到 {len(log_files)} 個日誌檔案：")
            for log_file in log_files:
                size = log_file.stat().st_size
                print(f"  📄 {log_file.name} ({size} bytes)")
                
                # 顯示檔案最後幾行
                if size > 0:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if lines:
                            print(f"     最後一行：{lines[-1].strip()}")
        else:
            print("❌ 沒有找到日誌檔案")
    else:
        print("❌ 日誌目錄不存在")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 檔案日誌範例")
    print("=" * 40)
    
    # 1. 基本檔案日誌
    basic_file_logging()
    
    # 2. 分離的檔案日誌
    separate_file_logging()
    
    # 3. 自定義檔案日誌
    custom_file_logging()
    
    # 4. 檢查日誌檔案
    check_log_files()
    
    print("\n" + "=" * 40)
    print("✅ 檔案日誌範例完成！")
    print("💡 接下來可以學習：")
    print("   - ../02_basics/：更多基礎功能")
    print("   - ../03_configuration/：進階配置")

if __name__ == "__main__":
    main()