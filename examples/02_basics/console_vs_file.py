#!/usr/bin/env python3
"""
Console vs File - 控制台與檔案輸出對比

這個範例展示：
1. 同時輸出到控制台和檔案
2. 僅輸出到控制台
3. 僅輸出到檔案
4. 實際應用場景

運行方式：
    python console_vs_file.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger

def main():
    print("=== 控制台 vs 檔案輸出範例 ===\n")
    
    # 創建有檔案輸出的 logger
    logger = create_logger("demo_app", log_path="./logs")
    
    print("1. 正常日誌 - 同時輸出到控制台和檔案")
    logger.info("用戶登入：user123")
    logger.warning("API 響應時間較慢：2.5秒")
    
    print("\n2. 僅控制台輸出 - 開發除錯資訊")
    logger.console_debug("除錯：檢查變數值 x=42, y=24")
    logger.console_info("開發提示：記得檢查快取")
    
    print("\n3. 僅檔案輸出 - 敏感或詳細資訊")
    logger.file_info("檔案處理完成：/data/export_20240627.csv")
    logger.file_warning("記憶體使用率：87% (檔案記錄)")
    
    print("\n4. 實際應用場景示範")
    
    # 模擬用戶操作
    user_id = "user123"
    operation = "export_data"
    
    # 給用戶看的簡單訊息
    logger.console_info(f"開始匯出資料...")
    
    # 詳細的系統記錄
    logger.file_info(f"用戶 {user_id} 開始操作 {operation}")
    logger.file_debug(f"操作參數：format=csv, date_range=30days")
    
    # 處理完成
    logger.success("資料匯出完成")  # 同時記錄到控制台和檔案
    logger.console_success("檔案已下載到您的下載資料夾")
    logger.file_info(f"操作 {operation} 完成，耗時 1.2秒")
    
    print("\n檢查 './logs' 目錄中的檔案，對比控制台輸出")
    print("您會發現檔案中包含更多詳細資訊！")

if __name__ == "__main__":
    main()