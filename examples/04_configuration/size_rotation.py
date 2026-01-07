#!/usr/bin/env python3
"""
Size Rotation - 大小輪替

學習如何基於檔案大小進行日誌輪替，
掌握不同大小閾值的設定和檔案管理策略。

運行方式：
    python size_rotation.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
import os

def basic_size_rotation():
    """基本大小輪替"""
    print("📏 基本大小輪替")
    print("-" * 30)
    
    # 創建一個小文件大小輪替的 logger
    logger = create_logger(
        "size_basic",
        log_dir="./logs/rotation",
        rotation="1 KB",  # 很小的大小以便演示
        retention=5  # 保留5個檔案
    )
    
    logger.info("開始大小輪替演示")
    
    # 生成一些日誌來觸發輪替
    for i in range(50):
        long_message = f"這是第 {i+1:03d} 條日誌訊息，包含一些額外的內容來增加檔案大小。" + "X" * 50
        logger.info(long_message)
        
        if i % 10 == 9:  # 每10條訊息檢查一次
            time.sleep(0.1)  # 給 loguru 時間處理
            print(f"  已寫入 {i+1} 條訊息")
    
    print("✅ 大小輪替演示完成")

def different_size_thresholds():
    """不同大小閾值演示"""
    print("\n📐 不同大小閾值演示")
    print("-" * 30)
    
    # 不同大小閾值的配置
    size_configs = [
        {"name": "tiny", "size": "500 B", "description": "極小檔案"},
        {"name": "small", "size": "2 KB", "description": "小檔案"},
        {"name": "medium", "size": "10 KB", "description": "中等檔案"},
        {"name": "large", "size": "50 KB", "description": "大檔案"}
    ]
    
    for config in size_configs:
        logger = create_logger(
            f"size_{config['name']}",
            log_dir="./logs/rotation/sizes",
            rotation=config["size"],
            retention=3
        )
        
        logger.info(f"開始 {config['description']} 輪替測試")
        logger.info(f"輪替大小設定為：{config['size']}")
        
        # 生成足夠的內容觸發輪替
        base_message = f"{config['description']} - "
        for i in range(20):
            padding = "日誌內容填充 " * 10  # 增加內容長度
            logger.info(f"{base_message}第 {i+1} 條訊息 - {padding}")
        
        logger.success(f"{config['description']} 輪替測試完成")
        print(f"  ✅ {config['description']} ({config['size']}) 測試完成")

def rotation_with_compression():
    """帶壓縮的輪替"""
    print("\n🗜️ 帶壓縮的輪替")
    print("-" * 30)
    
    # 使用預設配置，會自動處理壓縮
    logger = create_logger(
        "size_compressed",
        log_dir="./logs/rotation/compressed",
        preset="detailed",  # detailed 預設包含壓縮邏輯
        rotation="5 KB",
        retention=10
    )
    
    logger.info("開始壓縮輪替演示")
    
    # 生成大量內容
    for i in range(100):
        # 創建比較長的日誌訊息
        data_content = {
            "序號": i + 1,
            "操作": "數據處理",
            "狀態": "進行中" if i % 3 != 0 else "完成",
            "詳情": "這是一個包含大量資訊的日誌訊息，用來演示壓縮輪替功能。" + "詳細資訊 " * 20,
            "時間戳": time.time()
        }
        
        logger.info(f"處理記錄：{data_content}")
        
        if i % 20 == 19:
            time.sleep(0.1)
            print(f"  已處理 {i+1} 條記錄")
    
    logger.success("壓縮輪替演示完成")
    print("✅ 壓縮輪替測試完成")

def custom_rotation_logic():
    """自定義輪替邏輯"""
    print("\n⚙️ 自定義輪替邏輯")
    print("-" * 30)
    
    # 不同類型日誌的輪替策略
    rotation_strategies = [
        {
            "type": "error_logs",
            "rotation": "1 KB",  # 錯誤日誌快速輪替
            "retention": 20,  # 保留更多錯誤日誌
            "description": "錯誤日誌 - 快速輪替，長期保存"
        },
        {
            "type": "access_logs", 
            "rotation": "10 KB",  # 訪問日誌中等輪替
            "retention": 10,
            "description": "訪問日誌 - 中等輪替"
        },
        {
            "type": "debug_logs",
            "rotation": "2 KB",  # 除錯日誌快速輪替
            "retention": 5,  # 短期保存
            "description": "除錯日誌 - 快速輪替，短期保存"
        }
    ]
    
    loggers = {}
    
    for strategy in rotation_strategies:
        logger = create_logger(
            strategy["type"],
            log_dir=f"./logs/rotation/custom/{strategy['type']}",
            rotation=strategy["rotation"],
            retention=strategy["retention"]
        )
        loggers[strategy["type"]] = logger
        
        logger.info(f"初始化 {strategy['description']}")
        print(f"  📋 {strategy['description']} 已配置")
    
    # 模擬不同類型的日誌產生
    print("  🔄 開始模擬日誌產生...")
    
    for round_num in range(5):
        print(f"    第 {round_num + 1} 輪日誌產生")
        
        # 錯誤日誌（較少但重要）
        loggers["error_logs"].error(f"第 {round_num + 1} 輪：發生系統錯誤")
        loggers["error_logs"].critical(f"第 {round_num + 1} 輪：嚴重錯誤，需要立即處理")
        
        # 訪問日誌（中等頻率）
        for i in range(10):
            loggers["access_logs"].info(f"第 {round_num + 1} 輪：用戶 {i+1} 訪問頁面 /api/data")
            loggers["access_logs"].success(f"第 {round_num + 1} 輪：用戶 {i+1} 操作成功")
        
        # 除錯日誌（高頻率）
        for i in range(30):
            loggers["debug_logs"].debug(f"第 {round_num + 1} 輪：除錯資訊 {i+1}")
            loggers["debug_logs"].info(f"第 {round_num + 1} 輪：詳細處理步驟 {i+1}")
        
        time.sleep(0.1)  # 給輪替一些時間
    
    print("✅ 自定義輪替邏輯演示完成")

def monitor_rotation_files():
    """監控輪替檔案"""
    print("\n📊 監控輪替檔案")
    print("-" * 30)
    
    def check_rotation_directory(dir_path, description):
        """檢查輪替目錄中的檔案"""
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
        
        total_size = 0
        for i, file_path in enumerate(log_files[:10]):  # 只顯示前10個
            size = file_path.stat().st_size
            total_size += size
            
            size_str = f"{size:,} bytes"
            if size > 1024:
                size_str = f"{size/1024:.1f} KB"
            if size > 1024*1024:
                size_str = f"{size/(1024*1024):.1f} MB"
            
            # 判斷檔案類型
            file_type = "📄 當前" if i == 0 and not any(ext in file_path.name for ext in ['.1', '.2', '.gz', '.zip']) else "📦 歸檔"
            
            print(f"    {file_type} {file_path.name} - {size_str}")
        
        if len(log_files) > 10:
            print(f"    ... 還有 {len(log_files) - 10} 個檔案")
        
        total_size_str = f"{total_size:,} bytes"
        if total_size > 1024:
            total_size_str = f"{total_size/1024:.1f} KB"
        if total_size > 1024*1024:
            total_size_str = f"{total_size/(1024*1024):.1f} MB"
            
        print(f"    📊 總大小：{total_size_str}")
    
    # 檢查各個輪替目錄
    directories = [
        ("./logs/rotation", "基本輪替"),
        ("./logs/rotation/sizes", "不同大小閾值"),
        ("./logs/rotation/compressed", "壓縮輪替"),
        ("./logs/rotation/custom/error_logs", "錯誤日誌"),
        ("./logs/rotation/custom/access_logs", "訪問日誌"),
        ("./logs/rotation/custom/debug_logs", "除錯日誌")
    ]
    
    for dir_path, description in directories:
        check_rotation_directory(dir_path, description)

def rotation_best_practices():
    """輪替最佳實踐"""
    print("\n💡 輪替最佳實踐")
    print("-" * 30)
    
    # 最佳實踐配置示例
    best_practices = [
        {
            "scenario": "Web 應用",
            "config": {
                "rotation": "100 MB",
                "retention": 30,
                "description": "平衡存儲空間和歷史保存"
            }
        },
        {
            "scenario": "微服務",
            "config": {
                "rotation": "50 MB", 
                "retention": 20,
                "description": "快速輪替，適度保存"
            }
        },
        {
            "scenario": "批次處理",
            "config": {
                "rotation": "200 MB",
                "retention": 50, 
                "description": "大容量處理，長期歷史"
            }
        },
        {
            "scenario": "除錯環境",
            "config": {
                "rotation": "10 MB",
                "retention": 5,
                "description": "快速輪替，短期保存"
            }
        }
    ]
    
    for practice in best_practices:
        logger = create_logger(
            f"bp_{practice['scenario'].lower().replace(' ', '_')}",
            log_dir="./logs/rotation/best_practices",
            rotation=practice["config"]["rotation"],
            retention=practice["config"]["retention"]
        )
        
        logger.info(f"最佳實踐配置：{practice['scenario']}")
        logger.info(f"輪替策略：{practice['config']['description']}")
        logger.success(f"配置完成 - 輪替：{practice['config']['rotation']}, 保留：{practice['config']['retention']}")
        
        print(f"  ✅ {practice['scenario']} - {practice['config']['description']}")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 大小輪替範例")
    print("=" * 50)
    
    # 1. 基本大小輪替
    basic_size_rotation()
    
    # 2. 不同大小閾值演示
    different_size_thresholds()
    
    # 3. 帶壓縮的輪替
    rotation_with_compression()
    
    # 4. 自定義輪替邏輯
    custom_rotation_logic()
    
    # 5. 監控輪替檔案
    monitor_rotation_files()
    
    # 6. 輪替最佳實踐
    rotation_best_practices()
    
    print("\n" + "=" * 50)
    print("✅ 大小輪替範例完成！")
    print("💡 大小輪替最佳實踐：")
    print("   - 根據應用類型選擇合適的輪替大小")
    print("   - 平衡存儲空間和歷史保存需求")
    print("   - 為不同類型日誌設定不同策略")
    print("   - 定期監控輪替檔案的數量和大小")

if __name__ == "__main__":
    main()