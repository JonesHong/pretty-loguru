import time
import os
from pathlib import Path
import datetime
import shutil

# 確保本地路徑優先
import sys
sys.path.insert(0, r"C:\work\pretty-loguru")
from pretty_loguru import create_logger

def test_pretty_loguru_retention_carefully():
    """嚴謹測試 pretty_loguru 的 retention 機制"""
    
    # 清理和創建測試目錄
    test_log_path = Path.cwd() / "logs" / "pretty_retention_test"
    if test_log_path.exists():
        shutil.rmtree(test_log_path)
    test_log_path.mkdir(parents=True, exist_ok=True)
    
    # 創建一個用於監控的 logger
    monitor_logger = create_logger(
        name="monitor",
        service_tag="monitor",
        log_path=Path.cwd() / "logs" / "monitor",
    )
    
    # 使用固定的時間戳記
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    test_logger_name = f"retention_test_{timestamp}"
    
    # 創建測試 logger，設置極小的輪換大小和極短的保留時間
    test_logger = create_logger(
        name=test_logger_name,
        service_tag="retention_test",
        log_path=test_log_path,
        log_file_settings={
            "rotation": "1 KB",      # 極小的輪換大小，更容易觸發
            "retention": "2 seconds", # 極短的保留時間
            "compression": None,      # 不壓縮，方便觀察
        }
    )
    
    # 記錄初始狀態
    monitor_logger.info(f"嚴謹測試開始 - logger名稱: {test_logger_name}, 輪換大小: 1 KB, 保留時間: 1 seconds")
    monitor_logger.info(f"預期行為: 輪換後的日誌檔案應在 1 seconds 後被刪除 (當有新的輪換發生時)")
    
    # 確認初始檔案
    base_log_file = list(test_log_path.glob(f"*{timestamp}*.log"))
    if base_log_file:
        monitor_logger.info(f"初始日誌檔案: {base_log_file[0].name}")
    else:
        monitor_logger.warning("未找到初始日誌檔案")
    
    # 寫入第一條日誌確保文件被創建
    test_logger.info("初始測試日誌")
    
    # 記錄初始狀態
    initial_files = list(test_log_path.glob(f"*{timestamp}*.log"))
    initial_files_info = {}
    
    monitor_logger.info(f"初始狀態: {len(initial_files)} 個檔案")
    for file in initial_files:
        size = os.path.getsize(file)
        ctime = os.path.getctime(file)
        initial_files_info[file.name] = {"path": file, "size": size, "ctime": ctime}
        monitor_logger.info(f"  - {file.name} ({size / 1024:.2f} KB, 創建於 {time.time() - ctime:.2f}秒前)")
    
    # 第一輪寫入，觸發輪換
    monitor_logger.info("開始第一輪寫入以觸發輪換...")
    for i in range(30):
        test_logger.file_info(f"日誌條目 {i}: " + "x" * 50)  # 寫入較長的內容以快速增加文件大小
    
    # 等待短暫時間讓輪換完成
    time.sleep(0.5)
    
    # 收集第一輪寫入後的檔案
    first_round_files = list(test_log_path.glob(f"*{timestamp}*.log"))
    first_round_info = {}
    
    monitor_logger.info(f"第一輪寫入後: {len(first_round_files)} 個檔案")
    for file in first_round_files:
        size = os.path.getsize(file)
        ctime = os.path.getctime(file)
        first_round_info[file.name] = {"path": file, "size": size, "ctime": ctime}
        
        # 判斷是新文件還是原有文件
        if file.name in initial_files_info:
            size_diff = size - initial_files_info[file.name]["size"]
            monitor_logger.info(f"  - 原有: {file.name} (大小變化: {size_diff / 1024:.2f} KB)")
        else:
            monitor_logger.info(f"  - 新增: {file.name} ({size / 1024:.2f} KB, 創建於 {time.time() - ctime:.2f}秒前)")
    
    # 等待略長於保留時間
    wait_time = 5  # 秒，略長於設定的保留時間
    monitor_logger.info(f"等待 {wait_time} 秒...")
    time.sleep(wait_time)
    
    # 第二輪寫入，再次觸發輪換和可能的清理
    monitor_logger.info("開始第二輪寫入，這應該會觸發輪換和清理...")
    for i in range(30, 60):
        test_logger.file_info(f"日誌條目 {i}: " + "y" * 50)
    
    # 等待短暫時間讓輪換和清理完成
    time.sleep(wait_time)
    
    # 收集第二輪寫入後的文件
    second_round_files = list(test_log_path.glob(f"*{timestamp}*.log"))
    
    # 分析哪些文件保留，哪些文件被刪除
    retained_files = []
    deleted_files = []
    new_files = []
    
    for file_name in first_round_info:
        file_path = first_round_info[file_name]["path"]
        if file_path.exists():
            retained_files.append(file_name)
        else:
            deleted_files.append(file_name)
            ctime = first_round_info[file_name]["ctime"]
            age = time.time() - ctime
            monitor_logger.info(f"  - 已刪除: {file_name} (存在時間: {age:.2f} 秒)")
    
    for file in second_round_files:
        if file.name not in first_round_info:
            size = os.path.getsize(file)
            ctime = os.path.getctime(file)
            new_files.append(file.name)
            monitor_logger.info(f"  - 新增: {file.name} ({size / 1024:.2f} KB, 創建於 {time.time() - ctime:.2f}秒前)")
    
    # 第三輪寫入，再次觸發輪換和清理
    monitor_logger.info("開始第三輪寫入...")
    for i in range(60, 90):
        test_logger.file_info(f"日誌條目 {i}: " + "z" * 50)
    
    # 等待短暫時間
    time.sleep(wait_time)
    
    # 收集最終文件狀態
    final_files = list(test_log_path.glob(f"*{timestamp}*.log"))
    
    # 總結測試結果
    monitor_logger.info("\n=== 測試結果 ===")
    monitor_logger.info(f"初始檔案數: {len(initial_files)}")
    monitor_logger.info(f"第一輪寫入後檔案數: {len(first_round_files)}")
    monitor_logger.info(f"最終檔案數: {len(final_files)}")
    monitor_logger.info(f"被刪除的檔案數: {len(deleted_files)}")
    
    # 列出目錄中的所有檔案
    monitor_logger.info("\n目錄中的所有檔案:")
    for file in test_log_path.glob("*"):
        size = os.path.getsize(file)
        ctime = os.path.getctime(file)
        age = time.time() - ctime
        monitor_logger.info(f"  - {file.name} ({size / 1024:.2f} KB, 存在時間: {age:.2f} 秒)")
    
    # 關閉測試 logger 以釋放文件
    if hasattr(test_logger, "_core") and hasattr(test_logger._core, "handlers"):
        handler_ids = list(test_logger._core.handlers.keys())
        for handler_id in handler_ids:
            try:
                test_logger.remove(handler_id)
            except Exception as e:
                monitor_logger.warning(f"無法移除處理器 {handler_id}: {str(e)}")
    
    # 結論
    if deleted_files:
        monitor_logger.success(f"✓ 測試成功 - 有 {len(deleted_files)} 個舊日誌檔案被刪除!")
        return "測試完成 - retention參數有效! 舊日誌被成功刪除"
    else:
        monitor_logger.error("✗ 測試失敗 - 沒有檔案被刪除!")
        return "測試完成 - retention參數無效，沒有檔案被刪除"

if __name__ == "__main__":
    result = test_pretty_loguru_retention_carefully()
    print("\n" + result)