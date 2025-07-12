#!/usr/bin/env python3
"""
調試 monthly preset 問題
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pretty_loguru import create_logger
import time

def test_monthly_preset():
    print("=== 調試 Monthly Preset ===\n")
    
    # 創建 monthly logger
    logger = create_logger(
        "debug_monthly",
        log_path="./logs/debug",
        preset="monthly"
    )
    
    print("1. 寫入第一條日誌...")
    logger.info("這是第一條 monthly 測試日誌")
    
    print("2. 強制 flush...")
    # 嘗試強制 flush loguru 緩衝區
    import logging
    logging.shutdown()
    
    print("3. 等待1秒...")
    time.sleep(1)
    
    print("4. 寫入第二條日誌...")
    logger.info("這是第二條 monthly 測試日誌")
    
    print("5. 再次 flush...")
    time.sleep(1)
    
    print("6. 寫入第三條日誌...")
    logger.info("這是第三條 monthly 測試日誌")
    
    # 檢查文件
    log_file = Path("./logs/debug/[debug_monthly]monthly_latest.temp.log")
    if log_file.exists():
        size = log_file.stat().st_size
        print(f"\n檔案大小: {size} bytes")
        if size > 0:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"檔案內容:\n{content}")
        else:
            print("檔案是空的！")
    else:
        print("檔案不存在！")

if __name__ == "__main__":
    test_monthly_preset()