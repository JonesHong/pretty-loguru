"""
核心模組入口

此模組提供 Pretty Loguru 的核心功能，包括基本日誌操作、
配置管理、處理器管理和日誌清理機制。
"""

# 導入基本配置
from .config import (
    LOG_LEVEL,
    LOG_ROTATION,
    LOG_PATH,
    LOG_NAME_FORMATS,
    OUTPUT_DESTINATIONS,
    LOGGER_FORMAT,
    LogLevelEnum,
)

# 導入基本日誌功能
from .base import (
    configure_logger,
    get_console,
    log_path_global
)

# 導入處理器功能
from .handlers import (
    create_destination_filters,
    format_filename,
)

# 導入清理功能
from .cleaner import LoggerCleaner

# 定義對外可見的功能
__all__ = [
    # 配置常數
    "LOG_LEVEL",
    "LOG_ROTATION",
    "LOG_PATH",
    "LOG_NAME_FORMATS",
    "OUTPUT_DESTINATIONS",
    "LOGGER_FORMAT",
    "LogLevelEnum",
    
    # 基本功能
    "configure_logger",
    "get_console",
    
    # 處理器功能
    "create_destination_filters",
    "format_filename",
    
    # 日誌清理
    "LoggerCleaner",
    "log_path_global"  # 全域變數，用於儲存日誌路徑
]