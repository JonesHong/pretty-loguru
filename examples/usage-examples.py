"""
多層目錄支援使用範例
"""

# 確保本地路徑優先
from pathlib import Path
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')

# 驗證一下導入的是哪個模組
import pretty_loguru
print(pretty_loguru.__file__)


def demonstrate_multi_directory():
    """展示多層目錄支援功能"""
    from pretty_loguru import logger, logger_start
    
    # 1. 基本用法 - 使用子目錄
    process_id = logger_start(
        service_name="api_service",
        subdirectory="api_logs"
    )
    logger.info(f"基本子目錄示例 - 日誌將保存在 logs/api_logs/ 目錄下，進程ID: {process_id}")
    
    # 2. 按模塊分類的多層目錄
    process_id = logger_start(
        service_name="database",
        subdirectory="db/queries",
        log_name_format="{date}_{process_id}.log"  # 每日一個日誌文件
    )
    logger.info(f"多層目錄示例 - 日誌將保存在 logs/db/queries/ 目錄下，使用日期作為文件名，進程ID: {process_id}")
    
    # 3. 使用完全自定義路徑
    custom_path = Path.home() / "custom_logs"
    process_id = logger_start(
        service_name="user_service",
        log_base_path=custom_path,
        subdirectory="auth/login",
        log_name_format="login_activity_{date}.log"
    )
    logger.info(f"自定義路徑示例 - 日誌將保存在 {custom_path}/auth/login/ 目錄下，進程ID: {process_id}")
    
    # 4. 高級配置 - 使用自定義配置
    process_id = logger_start(
        service_name="analytics",
        subdirectory="reports/daily",
        custom_config={
            "level": "DEBUG",
            "rotation": "50",  # 50MB 輪換
            "log_name_format": "analytics_{date}.log"
        }
    )
    logger.debug("高級配置示例 - 使用自定義配置參數")
    logger.info(f"高級配置進程ID: {process_id}")
    
    # 5. 實際應用場景 - 區分不同模塊的日誌
    # 模擬 API 服務日誌
    api_process_id = logger_start(
        service_name="api",
        subdirectory="services/external_api"
    )
    logger.info(f"[API] 初始化外部 API 服務，進程ID: {api_process_id}")
    logger.success("[API] 連接外部 API 成功")
    
    # 切換到數據庫日誌
    db_process_id = logger_start(
        service_name="database",
        subdirectory="transactions"
    )
    logger.info(f"[DB] 初始化數據庫連接，進程ID: {db_process_id}")
    logger.error("[DB] 數據庫查詢超時")
    
    logger.info("多層目錄支援演示完成")


if __name__ == "__main__":
    demonstrate_multi_directory()