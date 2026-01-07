#!/usr/bin/env python3
"""
Simple Usage - Pretty Loguru 最基本使用範例

這個範例展示 pretty-loguru 的核心功能：
1. 創建 logger
2. 基本日誌輸出
3. 不同日誌級別

運行方式：
    python simple_usage.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger

def main():
    print("=== Pretty Loguru 基本使用範例 ===\n")
    
    # 1. 最簡單的使用方式 - 只有控制台輸出
    print("1. 創建基本 logger（僅控制台輸出）")
    logger = create_logger(
        # format="{time} {level} {message}",  # 自定義日誌格式
    )
    
    # 2. 基本日誌輸出
    logger.info("應用程式啟動")
    logger.success("連接資料庫成功")
    logger.warning("記憶體使用率 85%")
    logger.error("找不到配置檔案")
    logger.debug("除錯資訊：變數 x = 42")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 添加檔案輸出
    print("2. 創建有檔案輸出的 logger")
    file_logger = create_logger("file_app", log_dir="./logs")
    
    file_logger.info("這條訊息會同時出現在控制台和檔案中")
    file_logger.success("檔案日誌設定完成")
    
    print("\n檢查 './logs' 目錄，您會看到生成的日誌檔案")
    
    print("\n" + "="*50 + "\n")
    
    # 4. 使用原生格式
    print("3. 使用原生 loguru 格式")
    native_logger = create_logger(
        "native_app", 
        use_native_format=True,  # 使用接近 loguru 原生的格式
        log_dir="./logs"
    )
    
    native_logger.info("這是原生格式的日誌訊息")
    native_logger.warning("注意格式差異：使用 file:function:line")
    
    print("\n💡 比較兩種格式：")
    print("  - Pretty(預設): {自定義名稱}:{function}:{line}")  
    print("  - Native: {file.name}:{function}:{line}")
    
    print("\n範例完成！接下來可以嘗試其他範例。")

if __name__ == "__main__":
    main()
