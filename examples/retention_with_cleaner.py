import time
import os
import shutil
import tempfile
from pathlib import Path

# 確保本地路徑優先
import sys

sys.path.insert(0, r"C:\work\pretty-loguru")


from pretty_loguru import create_logger
from pretty_loguru.core.cleaner import LoggerCleaner
from pretty_loguru.types.protocols import LogConfigType

def test_minimum_log_retention():
    """測試日誌清理功能的最小保留時間（使用臨時文件）"""
    # 創建一個監控 logger
    monitor_logger = create_logger(
        name="monitor_logger",
        service_tag="monitor",
        log_path=Path.cwd() / "logs" / "monitor",
        log_file_settings= {"rotation": "5 seconds", "retention": "10 seconds"}
    )
    
    # 創建測試目錄
    test_log_path = Path.cwd() / "logs" / "retention_test"
    if test_log_path.exists():
        shutil.rmtree(test_log_path)
    test_log_path.mkdir(parents=True, exist_ok=True)
    
    # 創建測試文件（模擬日誌文件，但不是真正的日誌）
    monitor_logger.info("創建測試文件...")
    for i in range(5):
        test_file = test_log_path / f"test_log_{i}.log"
        with open(test_file, "w") as f:
            f.write(f"測試日誌內容 {i}\n")
            f.write(f"這不是真正的日誌文件，只是用來測試清理功能\n")
        
        monitor_logger.info(f"已創建測試文件: {test_file}")
    
    # 檢查初始文件
    initial_files = list(test_log_path.glob("*.log"))
    monitor_logger.info(f"初始測試文件數: {len(initial_files)}")
    for file in initial_files:
        monitor_logger.info(f"初始測試文件: {file.name}")
    
    # 創建一個非常短的清理間隔
    min_retention = 0.001  # 0.001天 = 86.4秒
    
    cleaner = LoggerCleaner(
        log_retention=min_retention,
        log_path=test_log_path,
        check_interval=10,  # 每10秒檢查一次
        logger_instance=monitor_logger,
        recursive=True,
    )
    
    # 啟動清理器
    monitor_logger.info(f"啟動日誌清理器，保留時間: {min_retention} 天 (約 {min_retention*24*60*60:.2f} 秒)")
    cleaner.start()
    
    # 等待略長於保留時間再檢查
    wait_seconds = min_retention * 24 * 60 * 60 * 1.5  # 保留時間的1.5倍
    monitor_logger.info(f"等待 {wait_seconds:.2f} 秒後檢查...")
    time.sleep(wait_seconds)
    
    # 檢查剩餘文件
    remaining_files = list(test_log_path.glob("*.log"))
    monitor_logger.info(f"清理後剩餘文件數: {len(remaining_files)}")
    for file in remaining_files:
        created_time = os.path.getctime(file)
        age_seconds = time.time() - created_time
        monitor_logger.info(f"剩餘文件: {file.name}, 存在時間: {age_seconds:.2f} 秒")
    
    # 查看是否有文件被清理
    monitor_logger.info(f"初始文件數: {len(initial_files)}, 剩餘文件數: {len(remaining_files)}")
    if len(remaining_files) < len(initial_files):
        monitor_logger.success(f"文件清理成功! 已清理 {len(initial_files) - len(remaining_files)} 個文件")
    else:
        monitor_logger.warning("文件未被清理，可能需要更長的等待時間或更短的保留時間")
    
    # 再創建一些新文件看看是否能即時清理
    monitor_logger.info("創建新的測試文件...")
    for i in range(5, 10):
        test_file = test_log_path / f"test_log_{i}.log"
        with open(test_file, "w") as f:
            f.write(f"新測試日誌內容 {i}\n")
        
        monitor_logger.info(f"已創建新測試文件: {test_file}")
    
    # 再次等待查看清理效果
    monitor_logger.info("等待兩分鐘以觀察即時清理效果...")
    time.sleep(120)
    
    # 最終檢查
    final_files = list(test_log_path.glob("*.log"))
    monitor_logger.info(f"最終剩餘文件數: {len(final_files)}")
    for file in final_files:
        created_time = os.path.getctime(file)
        age_seconds = time.time() - created_time
        monitor_logger.info(f"最終剩餘文件: {file.name}, 存在時間: {age_seconds:.2f} 秒")
    
    return monitor_logger

if __name__ == "__main__":
    logger = test_minimum_log_retention()
    logger.info("測試完成")