#!/usr/bin/env python3
"""
Preset Comparison - 預設配置對比

簡單對比所有可用預設的差異和適用場景。

運行方式：
    python examples/04_configuration/preset_comparison.py

注意：
    - `daily/hourly/minute/weekly/monthly` 這些預設的「當前寫入檔名」會是 `*_latest.temp.log`
      （用於維持固定的最新檔名，避免一天/一小時內產生大量檔案）。
    - 到達 rotation 條件時，才會依各預設的壓縮/重命名策略把輪替檔案改成「歸檔檔名」
      （例如 `[component]YYYYMMDD.log`）。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time

def compare_all_presets():
    """對比所有預設配置"""
    print("📊 Pretty Loguru 預設配置對比")
    print("=" * 40)
    
    # 基本預設資訊
    presets = [
        {"name": "simple", "rotation": "20 MB", "retention": "30 days", "use_case": "開發測試"},
        {"name": "detailed", "rotation": "20 MB", "retention": "30 days", "use_case": "完整功能"},
        {"name": "daily", "rotation": "00:00", "retention": "30 days", "use_case": "Web 應用"},
        {"name": "hourly", "rotation": "1 hour", "retention": "7 days", "use_case": "高頻系統"},
        {"name": "minute", "rotation": "1 minute", "retention": "24 hours", "use_case": "調試演示"},
        {"name": "weekly", "rotation": "monday", "retention": "12 weeks", "use_case": "週報系統"},
        {"name": "monthly", "rotation": "1 month", "retention": "12 months", "use_case": "月度歸檔"}
    ]
    
    for preset in presets:
        print(f"\n📋 {preset['name']} 預設")
        print(f"   輪替: {preset['rotation']}")
        print(f"   保留: {preset['retention']}")
        print(f"   適用: {preset['use_case']}")
        
        # 測試每個預設
        logger = create_logger(
            f"test_{preset['name']}", 
            log_dir="./logs/comparison_demo",
            preset=preset['name'],
            retention="30 seconds"  # 演示用短保留期
        )
        
        logger.info(f"{preset['name']} 預設測試日誌")
        
        # pretty-loguru 內部使用 enqueue=True（非同步），用 complete() 等待佇列清空更可靠。
        if hasattr(logger, "complete"):
            logger.complete()
        
        print(f"   ✅ {preset['name']} 測試完成")

def show_compression_strategies():
    """展示壓縮策略差異"""
    print("\n🗜️ 壓縮檔名策略")
    print("=" * 40)
    
    strategies = [
        {"preset": "detailed", "active": "[component]YYYYMMDD-HHMMSS.log", "rotated": "[component].YYYYMMDD-HHMMSS.log"},
        {"preset": "simple", "active": "component.log", "rotated": "component_rot_YYYYMMDD-HHMMSS.log"},
        {"preset": "daily", "active": "[component]daily_latest.temp.log", "rotated": "[component]YYYYMMDD.log"},
        {"preset": "hourly", "active": "[component]hourly_latest.temp.log", "rotated": "[component]YYYYMMDD_HH.log"},
        {"preset": "minute", "active": "[component]minute_latest.temp.log", "rotated": "[component]YYYYMMDD_HHMM.log"},
        {"preset": "weekly", "active": "[component]weekly_latest.temp.log", "rotated": "[component]week_2025W26.log"},
        {"preset": "monthly", "active": "[component]monthly_latest.temp.log", "rotated": "[component]202506.log"}
    ]
    
    for strategy in strategies:
        print(f"\n📄 {strategy['preset']}")
        print(f"   當前寫入: {strategy['active']}")
        print(f"   輪替歸檔: {strategy['rotated']}")

def scenario_recommendations():
    """場景建議"""
    print("\n💡 場景選擇建議")
    print("=" * 40)
    
    scenarios = [
        {"scenario": "Web 應用開發", "recommended": "daily", "reason": "每日歸檔便於分析"},
        {"scenario": "數據處理管道", "recommended": "hourly", "reason": "高頻處理需按小時分割"},
        {"scenario": "微服務系統", "recommended": "daily", "reason": "多服務統一管理"},
        {"scenario": "開發測試", "recommended": "simple", "reason": "簡單配置快速上手"},
        {"scenario": "調試分析", "recommended": "minute", "reason": "快速輪替便於測試"},
        {"scenario": "長期歸檔", "recommended": "monthly", "reason": "節省空間長期保存"}
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['scenario']}")
        print(f"   建議: {scenario['recommended']}")
        print(f"   原因: {scenario['reason']}")

def main():
    """主函數"""
    print("🎯 Pretty Loguru 預設配置對比")
    print("=" * 50)
    
    # 1. 對比所有預設
    compare_all_presets()
    
    # 2. 壓縮策略說明
    show_compression_strategies()
    
    # 3. 場景建議
    scenario_recommendations()
    
    print("\n" + "=" * 50)
    print("📁 檢查 ./logs/comparison_demo/ 查看測試檔案")
    print("💡 根據您的需求選擇合適的預設配置")

if __name__ == "__main__":
    main()
