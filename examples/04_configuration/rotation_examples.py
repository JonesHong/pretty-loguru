#!/usr/bin/env python3
"""
Rotation Examples - 檔案輪替策略範例

展示不同的日誌輪替策略：
1. 按大小輪替 - 適合流量不均的應用
2. 按時間輪替 - 適合定期分析的應用  
3. 生產環境策略 - 兼顧兩者優勢
4. 極端客製化輪轉情境 - 1KB輪轉 + ZIP壓縮 + 1秒檢查10秒清理 (持續運行)

運行方式：
    python rotation_examples.py
    
特色功能：
- 互動式選單系統
- 極端輪轉演示 (1KB檔案 + ZIP壓縮 + 1秒檢查快速清理)
- 持續運行模式 (Ctrl+C 停止)
- 即時狀態顯示
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
import signal
import sys
from datetime import datetime

def demo_size_rotation():
    """演示按大小輪替"""
    print("📁 按大小輪替 - 適合流量不均的應用")
    print("-" * 40)
    
    # 小檔案快速輪替（演示用）
    logger = create_logger(
        "size_demo",
        log_dir="./logs/rotation_demo",
        rotation="1 KB",  # 小檔案用於演示
        retention="10 seconds"
    )
    
    print("   生成日誌觸發輪替...")
    for i in range(20):
        logger.info(f"[{i:02d}] 按大小輪替測試 - 當檔案達到1KB時會自動輪替到新檔案")
        time.sleep(0.1)
    
    print("   ✅ 檔案已按大小輪替")
    print()

def demo_time_rotation():
    """演示按時間輪替"""
    print("⏰ 按時間輪替 - 適合定期分析的應用")
    print("-" * 40)
    
    # 使用預設配置
    presets = [
        ("daily", "每日輪替", "適合 Web 應用"),
        ("hourly", "每小時輪替", "適合高頻系統"),
        ("minute", "每分鐘輪替", "適合測試演示")
    ]
    
    for preset, name, use_case in presets:
        logger = create_logger(
            f"{preset}_demo",
            log_dir="./logs/rotation_demo",
            preset=preset,
            retention="30 seconds"  # 短保留期用於演示
        )
        
        print(f"   {name}: {use_case}")
        for i in range(5):
            logger.info(f"[{i:02d}] {name}測試")
            time.sleep(0.2)
    
    print("   ✅ 各種時間輪替策略已演示")
    print()

def demo_production_strategies():
    """演示生產環境策略"""
    print("🏭 生產環境建議策略")
    print("-" * 40)
    
    strategies = [
        {
            "name": "Web 應用",
            "logger": create_logger("web_app", log_dir="./logs/rotation_demo", 
                                   preset="daily", retention="30 days"),
            "description": "每日歸檔，保留30天"
        },
        {
            "name": "API 服務", 
            "logger": create_logger("api_service", log_dir="./logs/rotation_demo",
                                   rotation="50 MB", retention="7 days"),
            "description": "按50MB輪替，保留7天"
        },
        {
            "name": "數據管道",
            "logger": create_logger("data_pipeline", log_dir="./logs/rotation_demo",
                                   preset="hourly", retention="14 days"),
            "description": "每小時歸檔，保留14天"
        }
    ]
    
    for strategy in strategies:
        print(f"   {strategy['name']}: {strategy['description']}")
        for i in range(3):
            strategy['logger'].info(f"[{i:02d}] {strategy['name']} 運行日誌")
    
    print("   ✅ 生產環境策略已演示")
    print()

def demo_extreme_rotation():
    """演示極端客製化輪轉情境"""
    print("🚀 極端客製化輪轉情境 - 超快速輪轉和清理")
    print("-" * 50)
    print("設定：1KB立即輪轉 + ZIP壓縮 + 10秒自動刪除舊檔案")
    print("特點：每條日誌約100字元，約10條觸發輪轉")
    print("壓縮：輪轉時自動壓縮為 ZIP 格式（節省70-80%空間）")
    print("清理：LoggerCleaner 自動刪除超過10秒的檔案")
    print("效果：持續生成檔案，ZIP壓縮，同時自動清理10秒前的檔案")
    print("按 Ctrl+C 停止運行...")
    print()
    
    # 創建帶有真正 ZIP 壓縮的極端配置 logger
    def extreme_compression(file_path):
        """自定義壓縮函數：真正壓縮為 ZIP 檔案"""
        import os
        import zipfile
        from pathlib import Path
        from datetime import datetime
        
        path = Path(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"{path.stem}_compressed_{timestamp}.zip"
        zip_path = path.parent / zip_name
        
        # 創建 ZIP 檔案
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, path.name)
        
        # 刪除原始檔案
        try:
            os.remove(file_path)
            print(f"   📦 ZIP壓縮完成: {path.name} → {zip_name}")
        except OSError as e:
            print(f"   ⚠️  無法刪除原始檔案 {path.name}: {e}")
        return str(zip_path)
    
    # 創建極端配置的 logger
    logger = create_logger(
        "extreme_demo",
        log_dir="./logs/extreme_demo", 
        rotation="4 KB",        # 1KB 立即輪轉
        retention="3 seconds", # 10秒後刪除所有舊檔案
        compression=extreme_compression  # 自定義 ZIP 壓縮
        
    )
    
    # 手動創建快速檢查的清理器（每1秒檢查一次）
    # 由於 LoggerCleaner 只支援天數，我們需要修改它來支援秒數
    from pretty_loguru.core.cleaner import LoggerCleaner
    
    # 創建自定義的快速清理器類
    class FastCleaner(LoggerCleaner):
        def __init__(self, log_dir, retention_seconds=10, check_interval=1):
            super().__init__(log_dir=log_dir, log_retention=30, check_interval=check_interval)
            self.retention_seconds = retention_seconds  # 保留秒數
            
        def _clean_old_logs(self):
            """重寫清理邏輯，使用秒數而不是天數"""
            import os
            import time
            from pathlib import Path
            
            if not os.path.exists(self.log_dir):
                return
                
            # 計算截止時間戳（當前時間 - 保留秒數）
            cutoff_timestamp = time.time() - self.retention_seconds
            
            # 搜尋要檢查的檔案路徑
            paths_to_check = []
            
            if self.recursive:
                for root, dirs, files in os.walk(self.log_dir):
                    for file in files:
                        paths_to_check.append(os.path.join(root, file))
            else:
                for file_path in Path(self.log_dir).iterdir():
                    if file_path.is_file():
                        paths_to_check.append(str(file_path))
            
            # 清理過期檔案
            deleted_count = 0
            for file_path in paths_to_check:
                try:
                    # 忽略隱藏文件
                    if os.path.basename(file_path).startswith('.'):
                        continue
                    
                    # 檢查檔案的修改時間是否早於截止時間
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime < cutoff_timestamp:
                        # 刪除過期檔案
                        try:
                            os.remove(file_path)
                            deleted_count += 1
                            print(f"   🗑️  已刪除過期檔案: {os.path.basename(file_path)} (年齡: {time.time() - file_mtime:.1f}秒)")
                        except OSError as e:
                            print(f"   ⚠️  無法刪除檔案 {os.path.basename(file_path)}: {e}")
                        
                except FileNotFoundError:
                    # 檔案可能已被壓縮程序刪除，忽略即可
                    continue
                except (PermissionError, OSError) as e:
                    print(f"   ❌ 無法刪除檔案 {file_path}: {e}")
            
            if deleted_count > 0:
                print(f"   ✅ 本次清理共刪除 {deleted_count} 個過期檔案")
    
    fast_cleaner = FastCleaner(
        log_dir="./logs/extreme_demo",
        retention_seconds=10,  # 10秒保留期
        check_interval=1  # 每1秒檢查一次
    )
    fast_cleaner.start()
    print("   ⚡ 快速清理器已啟動：每1秒檢查並刪除超過10秒的檔案")
    
    # 設置中斷處理
    def signal_handler(sig, frame):
        print("\n\n🛑 使用者中斷程序")
        print("🛑 正在停止快速清理器...")
        fast_cleaner.stop()
        print("📊 查看 ./logs/extreme_demo/ 目錄觀察檔案變化")
        print("💡 注意：ZIP檔案和清理效果已演示完成")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # 計數器
    message_count = 0
    start_time = time.time()
    
    try:
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # 生成日誌訊息
            message_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            logger.info(f"[{message_count:04d}] {timestamp} - 極端輪轉測試訊息，這是一個較長的訊息用於快速達到1KB限制並觸發檔案輪轉")
            
            # 每5秒顯示狀態
            if message_count % 50 == 0:
                print(f"   📝 已生成 {message_count} 條日誌 | 運行時間: {elapsed:.1f}秒")
                print(f"   🔄 預期已輪轉檔案數: ~{message_count // 10}")
                print(f"   📦 ZIP壓縮: 輪轉時自動壓縮為 .zip 檔案")
                print(f"   🗑️  自動清理: LoggerCleaner 每秒檢查並刪除超過10秒的檔案")
                print(f"   📊 當前速度: 每秒約10條日誌，每1KB輪轉一次")
                print(f"   💾 壓縮比: ZIP格式可節省約70-80%儲存空間")
                print()
            
            # 控制生成速度（每秒約10條訊息）
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 接收到中斷信號")
        print("🛑 正在停止快速清理器...")
        fast_cleaner.stop()
        print("📊 查看 ./logs/extreme_demo/ 目錄觀察檔案變化")
        print("💡 注意：ZIP檔案和清理效果已演示完成")

def interactive_demo():
    """互動式演示選單"""
    print("🎯 Pretty Loguru 檔案輪替策略範例")
    print("=" * 50)
    print()
    
    while True:
        print("請選擇演示模式：")
        print("1. 📁 按大小輪替演示")
        print("2. ⏰ 按時間輪替演示") 
        print("3. 🏭 生產環境策略演示")
        print("4. 🚀 極端客製化輪轉情境 (1KB輪轉+ZIP壓縮+10秒清理，持續運行)")
        print("5. 🔄 運行所有標準演示")
        print("0. ❌ 退出")
        print()
        
        try:
            choice = input("請輸入選項 (0-5): ").strip()
            print()
            
            if choice == "0":
                print("👋 感謝使用 Pretty Loguru 演示！")
                break
            elif choice == "1":
                demo_size_rotation()
            elif choice == "2":
                demo_time_rotation()
            elif choice == "3":
                demo_production_strategies()
            elif choice == "4":
                demo_extreme_rotation()
            elif choice == "5":
                demo_size_rotation()
                demo_time_rotation()  
                demo_production_strategies()
                print("📋 標準演示總結")
                print("=" * 50)
                print("✅ 按大小輪替：適合流量不均的應用")
                print("✅ 按時間輪替：適合定期分析的應用") 
                print("✅ 生產策略：根據業務需求選擇合適策略")
                print()
                print("📁 檢查 ./logs/rotation_demo/ 查看生成的檔案")
            else:
                print("❌ 無效選項，請重新選擇")
            
            if choice in ["1", "2", "3", "5"]:
                input("\n按 Enter 繼續...")
                print()
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已中斷，感謝使用！")
            break
        except EOFError:
            print("\n\n👋 程序已結束，感謝使用！")
            break

def auto_demo():
    """自動運行所有演示"""
    print("🎯 Pretty Loguru 檔案輪替策略範例")
    print("=" * 50)
    print("🔄 自動運行所有標準演示")
    print()
    
    demo_size_rotation()
    demo_time_rotation()  
    demo_production_strategies()
    
    print("📋 標準演示總結")
    print("=" * 50)
    print("✅ 按大小輪替：適合流量不均的應用")
    print("✅ 按時間輪替：適合定期分析的應用") 
    print("✅ 生產策略：根據業務需求選擇合適策略")
    print()
    print("📁 檢查 ./logs/rotation_demo/ 查看生成的檔案")
    print("✅ 輪替範例完成！")

def main():
    """主函數"""
    # 檢查是否有命令行參數
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        auto_demo()

if __name__ == "__main__":
    main()