#!/usr/bin/env python3
"""
快速日誌輪轉演示

展示如何使用短時間間隔來測試和觀察日誌輪轉效果。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
from datetime import datetime

def main():
    print("=== 快速日誌輪轉演示 ===\n")
    
    # 創建一個每5秒輪轉的 logger
    logger = create_logger(
        "rotation_test",
        log_path="./logs/quick_rotation",
        rotation="5 seconds",    # 每5秒輪轉
        retention="30 seconds",  # 保留30秒
        compression="zip"        # 壓縮舊文件
    )
    
    print("🔄 每5秒輪轉一次，運行20秒")
    print("📁 查看 ./logs/quick_rotation/ 目錄")
    print()
    
    # 運行20秒，每2秒寫一條日誌
    for i in range(10):
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        logger.info(f"輪轉測試日誌 #{i+1} - {current_time}")
        print(f"✏️  日誌 #{i+1} 已寫入 ({current_time})")
        
        if i < 9:
            time.sleep(2)
    
    print("\n📂 檢查生成的文件：")
    
    # 檢查生成的文件
    rotation_dir = Path("./logs/quick_rotation")
    if rotation_dir.exists():
        files = list(rotation_dir.glob("*"))
        files.sort(key=lambda x: x.stat().st_mtime)
        
        for file in files:
            size = file.stat().st_size
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            print(f"   📄 {file.name} ({size} bytes)")
    
    print("\n✅ 輪轉演示完成！")
    print("💡 可以看到多個文件被創建，這就是時間輪轉的效果")

if __name__ == "__main__":
    main()