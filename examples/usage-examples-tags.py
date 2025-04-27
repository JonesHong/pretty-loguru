"""
標籤過濾系統使用範例
展示如何使用標籤來控制日誌的輸出目標
"""

# 確保本地路徑優先
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')

# 驗證一下導入的是哪個模組
# import pretty_loguru
# print(pretty_loguru.__file__)

def demonstrate_tag_filtering():
    """展示標籤過濾系統的功能"""
    from pretty_loguru import logger, logger_start
    
    # 1. 基本標籤用法 - 不設置過濾規則
    process_id = logger_start(
        service_name="tag_demo",
        subdirectory="tags/basic"
    )
    
    # 使用不同的標籤記錄日誌
    logger.info_t(message="這是一個帶有 'info' 標籤的消息", tags="info")
    logger.debug_t("這是一個帶有 'debug' 標籤的消息", tags="debug")
    logger.warning_t("這是一個帶有 'warning' 標籤的消息", tags="warning")
    logger.error_t("這是一個帶有多個標籤的錯誤消息", tags=["error", "important"])
    logger.success_t("這是一個沒有標籤的成功消息")  # 不提供標籤也可以
    
    # 2. 使用標籤過濾 - 只在控制台顯示某些標籤
    tag_config = {
        "console_only": ["dev", "debug"],  # 僅在控制台顯示的標籤
        "file_only": ["prod", "error"],    # 僅寫入文件的標籤
    }
    
    process_id = logger_start(
        service_name="dev_console",
        subdirectory="tags/filtered",
        tag_filter_config=tag_config
    )
    
    # 這條日誌只會顯示在控制台，不會寫入文件
    logger.debug_t("這條日誌只會顯示在控制台", tags="dev")
    
    # 這條日誌只會寫入文件，不會顯示在控制台
    logger.error_t("這條日誌只會寫入文件", tags="prod")
    
    # 這條日誌既會顯示在控制台，也會寫入文件（因為有兩個標籤分別符合兩種條件）
    logger.warning_t("這條日誌會同時顯示在控制台和文件中", tags=["dev", "error"])
    
    # 這條日誌沒有符合任何過濾條件，但因為沒有明確排除，也會顯示（取決於設置）
    logger.info_t("這條日誌沒有明確的過濾條件", tags="general")

    # 3. 使用排除標籤 - 不顯示或不寫入某些標籤
    exclude_config = {
        "console_exclude": ["verbose", "trace"],  # 不在控制台顯示的標籤
        "file_exclude": ["temporary", "debug"]    # 不寫入文件的標籤
    }
    
    process_id = logger_start(
        service_name="exclude_demo",
        subdirectory="tags/exclude",
        tag_filter_config=exclude_config
    )
    
    # 這條日誌不會顯示在控制台
    logger.debug_t("這條日誌不會顯示在控制台", tags="verbose")
    
    # 這條日誌不會寫入文件
    logger.info_t("這條日誌不會寫入文件", tags="temporary")
    
    # 這條日誌正常顯示和寫入（沒有被排除）
    logger.warning_t("這條日誌正常顯示和寫入", tags="important")
    
    # 4. 實際應用場景 - API 日誌過濾
    api_tag_config = {
        "console_only": ["api_debug", "performance"],  # 開發時需要在控制台查看的標籤
        "file_only": ["api_request", "api_response"],  # 只需要寫入文件存檔的標籤
        "console_exclude": ["sensitive"],              # 敏感資訊不顯示在控制台
    }
    
    process_id = logger_start(
        service_name="api_logger",
        subdirectory="api/logs",
        tag_filter_config=api_tag_config
    )
    
    # 模擬 API 請求日誌（只寫入文件）
    request_data = {"user_id": 12345, "action": "get_profile"}
    logger.info_t(f"收到 API 請求: {request_data}", tags="api_request")
    
    # 敏感資訊（只寫入文件，不顯示在控制台）
    user_data = {"name": "測試用戶", "email": "test@example.com", "password_hash": "abc123"}
    logger.info_t(f"用戶資料: {user_data}", tags=["api_response", "sensitive"])
    
    # 調試資訊（只顯示在控制台，不寫入文件）
    logger.debug_t("API 調用耗時: 125ms", tags="api_debug")
    logger.debug_t("數據庫查詢耗時: 45ms", tags="performance")
    
    # 錯誤資訊（同時顯示在控制台和文件中）
    try:
        # 模擬錯誤
        raise ValueError("資料庫連接失敗")
    except Exception as e:
        logger.error_t(f"API 錯誤: {str(e)}", tags=["api_debug", "api_request", "error"])
    
    # 5. 組合標籤的使用
    combo_tag_config = {
        "console_only": ["dev"],
        "file_only": ["audit"],
        "console_exclude": ["verbose"],
        "file_exclude": ["temp"]
    }
    
    process_id = logger_start(
        service_name="combo_tags",
        subdirectory="tags/combined",
        tag_filter_config=combo_tag_config
    )
    
    # 多標籤組合的各種情況
    logger.info_t("只在開發時顯示在控制台的消息", tags="dev")
    logger.info_t("只記錄到審計日誌文件的消息", tags="audit")
    logger.info_t("同時在控制台顯示和寫入文件的消息", tags=["dev", "audit"])
    logger.debug_t("此消息不會顯示在控制台", tags=["verbose", "dev"])  # dev 被 verbose 覆蓋
    logger.info_t("此消息不會寫入文件", tags=["audit", "temp"])  # audit 被 temp 覆蓋
    
    logger.info("標籤過濾演示完成")


if __name__ == "__main__":
    demonstrate_tag_filtering()