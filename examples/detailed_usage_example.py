"""
Pretty-Loguru 詳細使用範例
展示新版 Pretty-Loguru 的所有主要功能
"""
import os
import time
import random
from datetime import datetime
# 確保本地路徑優先
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')
from pretty_loguru import logger, logger_start, print_block, print_ascii_header, print_ascii_block


def show_standard_logs():
    """展示標準日誌功能"""
    print_ascii_header("Stander System Log ", font="big")
    
    # 基本日誌級別
    logger.debug("這是一條 DEBUG 級別的日誌")
    logger.info("這是一條 INFO 級別的日誌")
    logger.success("這是一條 SUCCESS 級別的日誌")
    logger.warning("這是一條 WARNING 級別的日誌")
    logger.error("這是一條 ERROR 級別的日誌")
    logger.critical("這是一條 CRITICAL 級別的日誌")
    
    # 帶參數的日誌
    user_id = 12345
    action = "login"
    logger.info(f"用戶 {user_id} 執行了 {action} 操作")
    
    # 結構化參數
    data = {"user": "admin", "ip": "192.168.1.1", "action": "delete", "target": "file.txt"}
    logger.info(f"用戶操作: {data}")


def show_destination_specific_logs():
    """展示目標特定日誌功能"""
    print_ascii_header("Destination Specific Logs", font="slant")
    
    # 僅控制台輸出
    logger.console("INFO", "這條日誌只會顯示在控制台，不會寫入日誌檔案")
    logger.console_debug("調試資訊 - 僅顯示在控制台")
    logger.console_info("一般資訊 - 僅顯示在控制台")
    logger.console_success("成功資訊 - 僅顯示在控制台")
    logger.console_warning("警告資訊 - 僅顯示在控制台")
    logger.console_error("錯誤資訊 - 僅顯示在控制台")
    logger.console_critical("嚴重錯誤資訊 - 僅顯示在控制台")
    
    # 開發模式 (別名，同樣僅控制台輸出)
    logger.dev("DEBUG", "開發模式 - 自定義級別")
    logger.dev_debug("開發模式 - 調試資訊")
    logger.dev_info("開發模式 - 一般資訊")
    logger.dev_success("開發模式 - 成功資訊")
    logger.dev_warning("開發模式 - 警告資訊")
    logger.dev_error("開發模式 - 錯誤資訊")
    logger.dev_critical("開發模式 - 嚴重錯誤資訊")
    
    # 僅檔案輸出
    logger.file("INFO", "這條日誌只會寫入日誌檔案，不會在控制台顯示")
    logger.file_debug("調試資訊 - 僅寫入檔案")
    logger.file_info("一般資訊 - 僅寫入檔案")
    logger.file_success("成功資訊 - 僅寫入檔案")
    logger.file_warning("警告資訊 - 僅寫入檔案")
    logger.file_error("錯誤資訊 - 僅寫入檔案")
    logger.file_critical("嚴重錯誤資訊 - 僅寫入檔案")


def show_real_world_application():
    """展示實際應用場景"""
    print_ascii_header("Real World Application", font="bubble")
    
    # 模擬 API 請求
    request_data = {
        "user_id": "user_123",
        "timestamp": datetime.now().isoformat(),
        "action": "get_data",
        "parameters": {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "filters": ["status=active", "type=premium"],
            "page": 1,
            "limit": 100
        }
    }
    
    # 一般日誌 - 記錄到檔案和控制台
    logger.info(f"收到來自用戶 {request_data['user_id']} 的 {request_data['action']} 請求")
    
    # 開發模式日誌 - 僅顯示在控制台，方便調試時查看詳細請求內容
    logger.dev_debug(f"請求詳情: {request_data}")
    logger.dev_info(f"請求參數: {request_data['parameters']}")
    
    # 模擬處理請求
    time.sleep(0.5)
    
    # 檔案日誌 - 僅記錄到檔案，作為審計追蹤
    logger.file_info(f"用戶 {request_data['user_id']} 查詢了 {request_data['parameters']['start_date']} 至 {request_data['parameters']['end_date']} 的資料")
    
    # 模擬處理結果
    results = {
        "total_count": 1250,
        "page_count": 13,
        "results": [f"item_{i}" for i in range(10)]  # 簡化的範例項目
    }
    
    # 控制台日誌 - 用於開發時監控
    logger.console_info(f"查詢返回 {results['total_count']} 條記錄，分 {results['page_count']} 頁")
    
    # 標準日誌 - 記錄關鍵資訊
    logger.success(f"成功處理用戶 {request_data['user_id']} 的請求，返回 {len(results['results'])} 條記錄")
    
    # 模擬偶爾出現的警告
    if random.random() < 0.3:
        logger.warning("查詢執行時間超過預期閾值")
    
    # 模擬罕見的錯誤
    if random.random() < 0.1:
        error_msg = "資料庫連接超時"
        
        # 錯誤日誌 - 同時發送到檔案和控制台
        logger.error(f"處理請求時發生錯誤: {error_msg}")
        
        # 開發日誌 - 僅記錄在控制台的詳細錯誤資訊
        logger.dev_error(f"詳細錯誤: 連接到 db_cluster_03 失敗，嘗試次數: 3，超時: 5s")


def show_block_logs():
    """展示區塊日誌功能"""
    print_ascii_header("Block Log Features", font="standard")
    
    # 基本區塊
    logger.block(
        "系統狀態摘要", 
        [
            "CPU 使用率: 45%",
            "記憶體使用率: 62%",
            "磁碟使用率: 78%",
            "網路流量: 25MB/s",
            "活動連接數: 143"
        ],
        border_style="green",
        log_level="INFO"
    )
    
    # 使用獨立函數的區塊
    print_block(
        "資料庫連接池", 
        [
            "總連接數: 50",
            "活動連接: 12",
            "等待連接: 3",
            "最大等待時間: 120ms",
            "平均響應時間: 45ms"
        ],
        border_style="blue",
        log_level="INFO"
    )
    
    # ASCII 藝術風格區塊
    logger.ascii_block(
        "重要通知", 
        [
            "系統將於 2023-09-15 02:00 進行維護",
            "預計停機時間: 30 分鐘",
            "影響範圍: 所有用戶",
            "請提前做好準備"
        ],
        ascii_header="NOTICE",
        ascii_font="banner3-D",
        border_style="red",
        log_level="WARNING"
    )


def show_ascii_headers():
    """展示 ASCII 藝術標題功能"""
    print_ascii_header("ASCII Art Headers", font="banner")
    time.sleep(0.5)
    
    # 不同字體的標題
    print_ascii_header("Warning", font="banner3-D", border_style="yellow", log_level="WARNING")
    time.sleep(0.5)
    print_ascii_header("Error", font="doom", border_style="red", log_level="ERROR")
    time.sleep(0.5)
    print_ascii_header("Success", font="bubble", border_style="green", log_level="SUCCESS")
    time.sleep(0.5)
    
    # 只顯示在控制台或檔案的標題
    print_ascii_header(
        "Console Only", 
        font="small", 
        border_style="cyan", 
        log_level="INFO",
        to_console_only=True
    )
    
    print_ascii_header(
        "File Only", 
        font="mini", 
        border_style="blue", 
        log_level="INFO",
        to_log_file_only=True
    )


def main():
    """主函數"""
    # 初始化日誌系統
    log_file_path = logger_start(
        service_name="LogDemo",
        subdirectory="demos",
        log_name_preset="detailed"
    )
    
    # 顯示初始化資訊
    logger.info(f"日誌系統已初始化，日誌檔案路徑: {log_file_path}")
    
    # 展示各種日誌功能
    show_standard_logs()
    time.sleep(1)
    
    show_destination_specific_logs()
    time.sleep(1)
    
    show_block_logs()
    time.sleep(1)
    
    show_ascii_headers()
    time.sleep(1)
    
    show_real_world_application()
    
    # 結束演示
    logger.success("日誌功能演示完成！")
    print_ascii_header("THE END", font="banner3-D", border_style="green")


if __name__ == "__main__":
    main()
