#!/usr/bin/env python3
"""
Time Rotation - 時間輪替

學習如何基於時間進行日誌輪替，
掌握不同時間間隔的設定和時間基礎的檔案管理。

運行方式：
    python time_rotation.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
from datetime import datetime, timedelta

def basic_time_rotation():
    """基本時間輪替"""
    print("🕐 基本時間輪替")
    print("-" * 30)
    
    # 使用分鐘輪替來快速演示
    logger = create_logger(
        "time_basic",
        log_path="./logs/rotation/time",
        preset="minute",  # 每分鐘輪替
        retention=10
    )
    
    logger.info("開始時間輪替演示")
    logger.info("使用分鐘輪替預設，每分鐘會創建新檔案")
    
    # 記錄一些日誌
    for i in range(20):
        current_time = datetime.now().strftime("%H:%M:%S")
        logger.info(f"[{current_time}] 第 {i+1} 條時間輪替日誌")
        
        if i % 5 == 4:
            logger.success(f"[{current_time}] 已完成第 {i+1} 個階段")
            time.sleep(2)  # 稍微等待一下
    
    logger.success("時間輪替演示完成")
    print("✅ 基本時間輪替演示完成")

def different_time_intervals():
    """不同時間間隔演示"""
    print("\n⏰ 不同時間間隔演示")
    print("-" * 30)
    
    # 不同時間間隔的配置
    time_configs = [
        {
            "name": "second",
            "rotation": "10 seconds",
            "description": "10秒輪替（演示用）",
            "retention": 20
        },
        {
            "name": "minute", 
            "rotation": "1 minute",
            "description": "每分鐘輪替",
            "retention": 10
        },
        {
            "name": "hourly",
            "preset": "hourly",
            "description": "每小時輪替（使用預設）",
            "retention": 24
        },
        {
            "name": "daily",
            "preset": "daily", 
            "description": "每日輪替（使用預設）",
            "retention": 30
        }
    ]
    
    loggers = {}
    
    for config in time_configs:
        if "preset" in config:
            # 使用預設配置
            logger = create_logger(
                f"time_{config['name']}",
                log_path=f"./logs/rotation/time/{config['name']}",
                preset=config["preset"],
                retention=config["retention"]
            )
        else:
            # 使用自定義輪替時間
            logger = create_logger(
                f"time_{config['name']}", 
                log_path=f"./logs/rotation/time/{config['name']}",
                rotation=config["rotation"],
                retention=config["retention"]
            )
        
        loggers[config["name"]] = logger
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"初始化 {config['description']} - {current_time}")
        
        print(f"  📅 {config['description']} 已配置")
    
    # 持續記錄一段時間來觀察輪替
    print("  🔄 開始持續記錄日誌...")
    
    start_time = time.time()
    iteration = 0
    
    while time.time() - start_time < 30:  # 運行30秒
        iteration += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        for name, logger in loggers.items():
            logger.info(f"[{current_time}] 第 {iteration} 次記錄")
            
            if iteration % 10 == 0:
                logger.success(f"[{current_time}] 完成第 {iteration} 次記錄")
        
        time.sleep(1)  # 每秒記錄一次
        
        if iteration % 10 == 0:
            print(f"    已記錄 {iteration} 次")
    
    print("✅ 不同時間間隔演示完成")

def rotation_at_specific_times():
    """特定時間輪替"""
    print("\n🎯 特定時間輪替")
    print("-" * 30)
    
    # 特定時間的輪替配置
    specific_configs = [
        {
            "name": "midnight",
            "rotation": "00:00",  # 每天午夜
            "description": "每日午夜輪替"
        },
        {
            "name": "noon",
            "rotation": "12:00",  # 每天中午
            "description": "每日中午輪替"
        },
        {
            "name": "weekly",
            "rotation": "monday",  # 每週一
            "description": "每週一輪替"
        },
        {
            "name": "hourly_15",
            "rotation": "15 minutes",  # 每15分鐘（演示用）
            "description": "每15分鐘輪替"
        }
    ]
    
    for config in specific_configs:
        logger = create_logger(
            f"specific_{config['name']}",
            log_path=f"./logs/rotation/time/specific/{config['name']}",
            rotation=config["rotation"],
            retention=20
        )
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"配置 {config['description']} - {current_time}")
        logger.info(f"輪替設定：{config['rotation']}")
        
        # 記錄一些日誌來測試
        for i in range(5):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{timestamp}] {config['description']} 測試日誌 {i+1}")
            time.sleep(0.5)
        
        logger.success(f"{config['description']} 配置完成")
        print(f"  ⏰ {config['description']} 已配置")

def time_based_log_analysis():
    """基於時間的日誌分析"""
    print("\n📈 基於時間的日誌分析")
    print("-" * 30)
    
    # 創建分析用的 logger
    analysis_logger = create_logger(
        "time_analysis",
        log_path="./logs/rotation/time/analysis",
        preset="minute",  # 使用分鐘輪替便於觀察
        retention=30
    )
    
    # 模擬不同時間段的活動
    activities = [
        {"time": "morning", "level": "info", "message": "系統啟動，開始處理請求"},
        {"time": "morning", "level": "success", "message": "所有服務初始化完成"},
        {"time": "noon", "level": "warning", "message": "請求量增加，資源使用率上升"},
        {"time": "afternoon", "level": "info", "message": "穩定運行中"},
        {"time": "evening", "level": "success", "message": "每日備份完成"},
        {"time": "night", "level": "info", "message": "進入維護模式"}
    ]
    
    analysis_logger.info("開始時間基礎的日誌分析演示")
    
    for round_num in range(3):
        current_time = datetime.now()
        
        for activity in activities:
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{activity['time'].upper()}] {activity['message']} - 輪次 {round_num + 1}"
            
            # 根據等級記錄日誌
            if activity["level"] == "info":
                analysis_logger.info(f"[{timestamp}] {log_message}")
            elif activity["level"] == "success":
                analysis_logger.success(f"[{timestamp}] {log_message}")
            elif activity["level"] == "warning":
                analysis_logger.warning(f"[{timestamp}] {log_message}")
            
            time.sleep(0.5)  # 模擬時間間隔
        
        # 每輪之間暫停
        analysis_logger.info(f"第 {round_num + 1} 輪分析完成，等待下一輪...")
        time.sleep(2)
    
    analysis_logger.success("時間基礎日誌分析演示完成")
    print("✅ 時間基礎日誌分析完成")

def rotation_retention_strategies():
    """輪替保留策略"""
    print("\n🗂️ 輪替保留策略")
    print("-" * 30)
    
    # 不同保留策略的配置
    retention_strategies = [
        {
            "strategy": "short_term",
            "rotation": "1 minute",
            "retention": "5 files",
            "description": "短期保留 - 快速輪替，只保留最近的檔案"
        },
        {
            "strategy": "medium_term",
            "rotation": "1 minute",
            "retention": "1 day",
            "description": "中期保留 - 按時間保留"
        },
        {
            "strategy": "long_term",
            "rotation": "1 minute", 
            "retention": "1 week",
            "description": "長期保留 - 歷史歸檔"
        },
        {
            "strategy": "file_count",
            "rotation": "1 minute",
            "retention": "20 files",
            "description": "檔案數量保留 - 固定檔案數量"
        }
    ]
    
    for strategy in retention_strategies:
        logger = create_logger(
            f"retention_{strategy['strategy']}",
            log_path=f"./logs/rotation/time/retention/{strategy['strategy']}",
            rotation=strategy["rotation"],
            retention=strategy["retention"]
        )
        
        logger.info(f"初始化保留策略：{strategy['description']}")
        logger.info(f"輪替：{strategy['rotation']}, 保留：{strategy['retention']}")
        
        # 生成一些測試日誌
        for i in range(10):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{timestamp}] {strategy['strategy']} 策略測試日誌 {i+1}")
            
            if i % 3 == 2:
                logger.success(f"[{timestamp}] {strategy['strategy']} 階段完成")
            
            time.sleep(0.3)
        
        logger.success(f"{strategy['description']} 測試完成")
        print(f"  📋 {strategy['description']} 已配置")

def monitor_time_rotation_files():
    """監控時間輪替檔案"""
    print("\n📊 監控時間輪替檔案")
    print("-" * 30)
    
    def analyze_time_rotation_directory(dir_path, description):
        """分析時間輪替目錄"""
        path = Path(dir_path)
        if not path.exists():
            print(f"  ❌ {description} 目錄不存在：{dir_path}")
            return
        
        log_files = list(path.glob("*.log*"))
        if not log_files:
            print(f"  📁 {description} 目錄為空")
            return
        
        print(f"  📁 {description} ({len(log_files)} 個檔案):")
        
        # 按修改時間排序
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for i, file_path in enumerate(log_files[:8]):  # 顯示前8個
            size = file_path.stat().st_size
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            size_str = f"{size:,} bytes"
            if size > 1024:
                size_str = f"{size/1024:.1f} KB"
            
            # 計算檔案年齡
            age = datetime.now() - mtime
            age_str = f"{age.total_seconds():.0f} 秒前"
            if age.total_seconds() > 60:
                age_str = f"{age.total_seconds()/60:.0f} 分鐘前"
            if age.total_seconds() > 3600:
                age_str = f"{age.total_seconds()/3600:.1f} 小時前"
            
            # 判斷檔案狀態
            status = "📄 當前" if i == 0 else f"📦 歸檔({age_str})"
            
            print(f"    {status} {file_path.name} - {size_str}")
        
        if len(log_files) > 8:
            print(f"    ... 還有 {len(log_files) - 8} 個檔案")
    
    # 檢查各個時間輪替目錄
    directories = [
        ("./logs/rotation/time", "基本時間輪替"),
        ("./logs/rotation/time/second", "秒級輪替"),
        ("./logs/rotation/time/minute", "分鐘輪替"),
        ("./logs/rotation/time/hourly", "小時輪替"),
        ("./logs/rotation/time/daily", "每日輪替"),
        ("./logs/rotation/time/analysis", "時間分析"),
    ]
    
    for dir_path, description in directories:
        analyze_time_rotation_directory(dir_path, description)

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 時間輪替範例")
    print("=" * 50)
    
    # 1. 基本時間輪替
    basic_time_rotation()
    
    # 2. 不同時間間隔演示
    different_time_intervals()
    
    # 3. 特定時間輪替
    rotation_at_specific_times()
    
    # 4. 基於時間的日誌分析
    time_based_log_analysis()
    
    # 5. 輪替保留策略
    rotation_retention_strategies()
    
    # 6. 監控時間輪替檔案
    monitor_time_rotation_files()
    
    print("\n" + "=" * 50)
    print("✅ 時間輪替範例完成！")
    print("💡 時間輪替最佳實踐：")
    print("   - 根據業務節奏選擇合適的輪替間隔")
    print("   - 平衡輪替頻率和系統性能")
    print("   - 為不同重要性的日誌設定不同保留期")
    print("   - 考慮磁碟空間和合規要求")

if __name__ == "__main__":
    main()