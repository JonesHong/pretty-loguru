#!/usr/bin/env python3
"""
時間輪轉模擬演示

這個範例展示：
1. 如何模擬不同時間的日誌輪轉
2. loguru 的時間輪轉機制
3. 如何測試和觀察輪轉效果
4. 不同時間格式的輪轉策略

運行方式：
    python time_rotation_simulation.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
from datetime import datetime, timedelta
import os

def explain_rotation_mechanism():
    """解釋輪轉機制"""
    print("=== Loguru 時間輪轉機制說明 ===\n")
    
    explanations = [
        "📅 時間輪轉只在時間間隔到達時觸發",
        "⏰ 'monthly' preset 需要跨月才會輪轉",
        "📄 當前文件：[component]monthly_latest.temp.log",
        "🔄 輪轉後文件：[component]YYYYMM.log",
        "🚀 可以通過修改系統時間或使用較短間隔測試"
    ]
    
    for i, explanation in enumerate(explanations, 1):
        print(f"{i}. {explanation}")
    
    print()

def demonstrate_quick_rotation():
    """演示快速輪轉（使用秒級間隔）"""
    print("=== 快速輪轉演示（每10秒輪轉一次） ===\n")
    
    # 創建一個每10秒輪轉的 logger
    logger = create_logger(
        "quick_rotation",
        log_path="./logs/rotation_demo",
        rotation="10 seconds",  # 每10秒輪轉一次
        retention="1 minute",   # 保留1分鐘
        compression="zip"       # 壓縮舊文件
    )
    
    print("🔄 開始快速輪轉演示...")
    print("📝 每5秒寫入一條日誌，觀察輪轉效果")
    print("📁 檢查 ./logs/rotation_demo/ 目錄")
    print()
    
    for i in range(6):  # 運行30秒
        current_time = datetime.now().strftime("%H:%M:%S")
        logger.info(f"快速輪轉測試 - 第 {i+1} 條日誌 ({current_time})")
        print(f"✏️  已寫入第 {i+1} 條日誌 - {current_time}")
        
        if i < 5:  # 最後一次不等待
            print("⏱️  等待5秒...")
            time.sleep(5)
    
    print("\n🎯 輪轉演示完成！")
    print("📂 檢查 ./logs/rotation_demo/ 目錄查看生成的文件")

def demonstrate_minute_rotation():
    """演示分鐘輪轉"""
    print("\n=== 分鐘輪轉演示 ===\n")
    
    logger = create_logger(
        "minute_rotation",
        log_path="./logs/rotation_demo",
        rotation="1 minute",
        retention="5 minutes"
    )
    
    print("⏰ 分鐘輪轉演示（運行2分鐘）")
    print("📝 每15秒寫入一條日誌")
    
    start_time = datetime.now()
    log_count = 0
    
    while (datetime.now() - start_time).total_seconds() < 120:  # 運行2分鐘
        log_count += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        logger.info(f"分鐘輪轉測試 - 第 {log_count} 條日誌 ({current_time})")
        print(f"✏️  第 {log_count} 條日誌 - {current_time}")
        
        time.sleep(15)  # 每15秒寫一條
    
    print("\n🎯 分鐘輪轉演示完成！")

def show_rotation_files():
    """顯示輪轉後的文件"""
    print("\n=== 檢查輪轉文件 ===\n")
    
    rotation_dir = Path("./logs/rotation_demo")
    if rotation_dir.exists():
        files = list(rotation_dir.glob("*"))
        files.sort(key=lambda x: x.stat().st_mtime)
        
        if files:
            print("📁 輪轉演示生成的文件：")
            for file in files:
                size = file.stat().st_size
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                print(f"   📄 {file.name} ({size} bytes, {mtime.strftime('%H:%M:%S')})")
        else:
            print("📂 目錄存在但沒有文件")
    else:
        print("📂 輪轉目錄不存在")

def explain_preset_rotation_times():
    """解釋各種 preset 的輪轉時機"""
    print("\n=== Preset 輪轉時機說明 ===\n")
    
    rotation_info = {
        "minute": {
            "間隔": "1 分鐘",
            "輪轉時機": "每分鐘的00秒",
            "文件格式": "[component]YYYYMMDD_HHMM.log",
            "適用場景": "快速測試、調試"
        },
        "hourly": {
            "間隔": "1 小時", 
            "輪轉時機": "每小時的00分00秒",
            "文件格式": "[component]YYYYMMDD_HH.log",
            "適用場景": "高頻應用、實時系統"
        },
        "daily": {
            "間隔": "1 天",
            "輪轉時機": "每天的00:00:00",
            "文件格式": "[component]YYYYMMDD.log", 
            "適用場景": "Web應用、一般服務"
        },
        "weekly": {
            "間隔": "1 週",
            "輪轉時機": "每週一的00:00:00",
            "文件格式": "[component]week_YYYYWWW.log",
            "適用場景": "週報系統、統計分析"
        },
        "monthly": {
            "間隔": "1 個月",
            "輪轉時機": "每月1號的00:00:00", 
            "文件格式": "[component]YYYYMM.log",
            "適用場景": "長期歸檔、合規需求"
        }
    }
    
    for preset, info in rotation_info.items():
        print(f"📋 {preset.upper()} Preset:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        print()

def create_time_simulation_example():
    """創建時間模擬範例"""
    print("=== 時間模擬建議 ===\n")
    
    print("🛠️  如果要測試長時間輪轉，可以：")
    print()
    
    simulation_methods = [
        "1. 使用較短的輪轉間隔（如上面的演示）",
        "2. 修改系統時間（需要管理員權限）",
        "3. 使用 loguru 的測試工具",
        "4. 創建自訂輪轉函數"
    ]
    
    for method in simulation_methods:
        print(f"   {method}")
    
    print()
    print("💡 建議使用方法1（較短間隔）進行測試")

def main():
    """主函數"""
    print("=== Pretty Loguru 時間輪轉模擬演示 ===\n")
    
    # 1. 解釋輪轉機制
    explain_rotation_mechanism()
    
    # 2. 解釋各種 preset 的輪轉時機
    explain_preset_rotation_times()
    
    # 3. 時間模擬建議
    create_time_simulation_example()
    
    # 詢問用戶是否要運行演示
    print("🎯 是否要運行輪轉演示？")
    print("1. 快速輪轉演示（10秒間隔）")
    print("2. 分鐘輪轉演示（1分鐘間隔）") 
    print("3. 只查看現有文件")
    print("0. 跳過演示")
    
    try:
        choice = input("\n請選擇 (0-3): ").strip()
        
        if choice == "1":
            demonstrate_quick_rotation()
            show_rotation_files()
        elif choice == "2": 
            demonstrate_minute_rotation()
            show_rotation_files()
        elif choice == "3":
            show_rotation_files()
        else:
            print("👋 跳過演示")
            
    except KeyboardInterrupt:
        print("\n\n👋 演示已取消")
    except EOFError:
        print("\n👋 演示已結束")
    
    print("\n" + "="*50)
    print("時間輪轉演示完成！")
    print("\n💡 重點回顧：")
    print("• 時間輪轉只在指定時間間隔到達時觸發")
    print("• monthly preset 需要跨月才會輪轉")
    print("• 可以使用較短間隔測試輪轉效果")
    print("• 輪轉文件會自動重命名和壓縮")

if __name__ == "__main__":
    main()