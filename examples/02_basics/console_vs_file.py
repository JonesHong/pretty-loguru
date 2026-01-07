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
from pretty_loguru.addons import log_to_targets

def main():
    print("=== 控制台 vs 檔案輸出範例 ===\n")
    
    # 創建有檔案輸出的 logger
    logger = create_logger("demo_app", log_dir="./logs")
    
    print("1. 正常日誌 - 同時輸出到控制台和檔案")
    logger.info("用戶登入：user123")
    logger.warning("API 響應時間較慢：2.5秒")
    
    print("\n2. 僅控制台輸出 - 開發除錯資訊")
    log_to_targets(logger, "除錯：檢查變數值 x=42, y=24", level="DEBUG", console_only=True)
    log_to_targets(logger, "開發提示：記得檢查快取", level="INFO", console_only=True)
    
    print("\n3. 僅檔案輸出 - 敏感或詳細資訊")
    log_to_targets(logger, "檔案處理完成：/data/export_20240627.csv", level="INFO", file_only=True)
    log_to_targets(logger, "記憶體使用率：87% (檔案記錄)", level="WARNING", file_only=True)
    
    print("\n4. 實際應用場景示範")
    
    # 模擬用戶操作
    user_id = "user123"
    operation = "export_data"
    
    # 給用戶看的簡單訊息
    log_to_targets(logger, "開始匯出資料...", level="INFO", console_only=True)
    
    # 詳細的系統記錄
    log_to_targets(logger, f"用戶 {user_id} 開始操作 {operation}", level="INFO", file_only=True)
    log_to_targets(logger, "操作參數：format=csv, date_range=30days", level="DEBUG", file_only=True)
    
    # 處理完成
    logger.success("資料匯出完成")  # 同時記錄到控制台和檔案
    log_to_targets(logger, "檔案已下載到您的下載資料夾", level="SUCCESS", console_only=True)
    log_to_targets(logger, f"操作 {operation} 完成，耗時 1.2秒", level="INFO", file_only=True)
    
    print("\n檢查 './logs' 目錄中的檔案，對比控制台輸出")
    print("您會發現檔案中包含更多詳細資訊！")

if __name__ == "__main__":
    main()
