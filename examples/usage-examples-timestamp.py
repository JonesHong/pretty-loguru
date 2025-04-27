"""
日誌檔名格式和時間戳配置範例
"""

# 確保本地路徑優先
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')

# 驗證一下導入的是哪個模組
import pretty_loguru
print(pretty_loguru.__file__)

        
def demonstrate_log_file_formats():
    """展示不同的日誌檔案名稱格式和時間戳配置"""
    from pretty_loguru import logger, logger_start
    
    # 1. 使用預設的日誌檔案格式
    process_id = logger_start(
        service_name="default_example"
    )
    logger.info(f"使用預設日誌格式，進程ID: {process_id}")
    
    # 2. 使用預定義的 "daily" 格式 - 每日一個日誌檔
    process_id = logger_start(
        service_name="daily_logs",
        log_name_preset="daily",
        subdirectory="daily_logs"
    )
    logger.info(f"使用每日一檔格式，進程ID: {process_id}")
    
    # 3. 使用預定義的 "hourly" 格式 - 每小時一個日誌檔
    process_id = logger_start(
        service_name="hourly_logs",
        log_name_preset="hourly",
        subdirectory="hourly_logs"
    )
    logger.info(f"使用每小時一檔格式，進程ID: {process_id}")
    
    # 4. 使用自定義格式 - 帶有年月日的結構
    process_id = logger_start(
        service_name="custom_format",
        log_name_format="{year}/{month}/{day}/{process_id}.log",
        subdirectory="structured_logs"
    )
    logger.info(f"使用自定義年月日結構格式，進程ID: {process_id}")
    
    # 5. 使用自定義時間戳格式 - ISO 8601 格式
    process_id = logger_start(
        service_name="iso_date",
        log_name_format="log_{timestamp}_{process_id}.log",
        timestamp_format="%Y-%m-%dT%H:%M:%S",
        subdirectory="iso_logs"
    )
    logger.info(f"使用 ISO 時間格式，進程ID: {process_id}")
    
    # 6. 按應用模組分類的日誌 - 使用服務名稱和日期
    process_id = logger_start(
        service_name="auth_service",
        log_name_format="{date}_{process_id}.log",
        subdirectory="services/auth"
    )
    logger.info(f"按應用模組分類 - 認證服務，進程ID: {process_id}")
    
    process_id = logger_start(
        service_name="payment_service",
        log_name_format="{date}_{process_id}.log",
        subdirectory="services/payment"
    )
    logger.info(f"按應用模組分類 - 支付服務，進程ID: {process_id}")
    
    # 7. 輪換和壓縮配置
    process_id = logger_start(
        service_name="web_service",
        log_name_preset="daily",
        subdirectory="web_logs",
        log_file_settings={
            "rotation": "10 MB",  # 每 10MB 輪換一次
            "compression": "zip",  # 輪換時壓縮為 zip
            "retention": "1 month",  # 保留 1 個月
        }
    )
    logger.info(f"輪換和壓縮配置示例，進程ID: {process_id}")
    
    # 8. 生產環境配置示例
    process_id = logger_start(
        service_name="production_api",
        log_name_format="api_{date}.log",
        subdirectory="production/api",
        custom_config={
            "level": "WARNING",  # 生產環境只記錄警告及以上級別
            "rotation": "50 MB",
            "log_file_settings": {
                "compression": "gz",
                "retention": "3 months",
                "backtrace": True,  # 包含回溯信息
                "diagnose": True,   # 增強診斷信息
            }
        }
    )
    logger.warning(f"生產環境配置示例，進程ID: {process_id}")
    
    # 9. 特殊場景 - 按小時和級別分類日誌
    process_id = logger_start(
        service_name="error_tracking", 
        log_name_format="errors_{date}_{hour}.log",
        subdirectory="error_logs",
        custom_config={"level": "ERROR"}  # 只記錄錯誤
    )
    logger.error(f"按級別分類 - 只記錄錯誤，進程ID: {process_id}")
    
    logger.info("日誌檔名格式和時間戳配置示例完成")


if __name__ == "__main__":
    demonstrate_log_file_formats()