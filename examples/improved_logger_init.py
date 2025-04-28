"""
更改後的 logger_start() 函數用法示例
展示如何設定日誌系統來實現按模組分資料夾和每天生成一個檔案
"""
# 確保本地路徑優先
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')
from pretty_loguru import logger, logger_start, print_ascii_header

def setup_modular_logging():
    """
    設定模組化日誌系統
    """
    # 範例1：API 服務，使用每日一檔模式
    api_log_path = logger_start(
        service_name="api_service",   # 指定服務名稱（也是 process_id）
        subdirectory="api",           # 子目錄，日誌將存儲在 logs/api/ 目錄下
        log_name_preset="daily",      # 使用每日一檔模式，檔案名格式為 {date}_{process_id}.log
    )
    logger.info(f"API 服務日誌系統已初始化: {api_log_path}")
    logger.dev_info("這是開發用資訊，只會在控制台顯示")
    
    # 範例2：資料庫服務，自定義日誌檔案名格式
    db_log_path = logger_start(
        service_name="db_service",
        subdirectory="database",      # 子目錄，日誌將存儲在 logs/database/ 目錄下
        log_name_format="{date}_database.log", # 自定義檔案名格式
    )
    logger.info(f"資料庫服務日誌系統已初始化: {db_log_path}")
    
    # 範例3：使用者介面服務，含更多自定義配置
    ui_log_path = logger_start(
        service_name="ui_service",
        subdirectory="ui",            # 子目錄，日誌將存儲在 logs/ui/ 目錄下
        log_name_preset="daily",      # 使用每日一檔模式
        log_file_settings={
            "rotation": "1 day",      # 日誌檔案輪換時間
            "retention": "1 week",    # 保留日誌的時間
            "compression": "zip",     # 舊日誌壓縮格式
        }
    )
    logger.info(f"使用者介面服務日誌系統已初始化: {ui_log_path}")
    
    # 在不同服務中使用日誌
    simulate_api_logs()
    simulate_db_logs()
    simulate_ui_logs()


def simulate_api_logs():
    """模擬 API 服務的日誌輸出"""
    print_ascii_header("API Logs", font="standard")
    
    # 標準日誌 - 同時輸出到控制台和檔案
    logger.info("處理 API 請求 GET /users")
    logger.success("API 請求處理成功，耗時: 45ms")
    
    # 僅用於開發的日誌 - 只顯示在控制台
    logger.dev_debug("API 請求參數: ?page=1&limit=20")
    logger.dev_info("API 請求頭: Content-Type: application/json")
    
    # 審計日誌 - 僅寫入檔案
    logger.file_info("用戶 admin 訪問了 /users 接口")


def simulate_db_logs():
    """模擬資料庫服務的日誌輸出"""
    print_ascii_header("Database Logs", font="standard")
    
    # 標準日誌
    logger.info("執行資料庫查詢: SELECT * FROM users LIMIT 10")
    logger.success("查詢成功，返回 10 條記錄")
    
    # 僅用於開發的日誌
    logger.dev_debug("SQL 參數綁定: {user_id: 123}")
    logger.dev_info("查詢耗時: 32ms, 緩存狀態: miss")
    
    # 審計日誌
    logger.file_info("資料庫查詢: users 表，條件: id=123")


def simulate_ui_logs():
    """模擬使用者介面服務的日誌輸出"""
    print_ascii_header("UI Log", font="standard")
    
    # 標準日誌
    logger.info("渲染用戶管理頁面")
    logger.success("頁面載入完成，耗時: 125ms")
    
    # 僅用於開發的日誌
    logger.dev_debug("頁面元素計數: buttons=12, inputs=8, tables=1")
    logger.dev_info("用戶設備: Chrome 85.0, Windows 10")
    
    # 審計日誌
    logger.file_info("管理員訪問了用戶管理頁面")


if __name__ == "__main__":
    setup_modular_logging()
