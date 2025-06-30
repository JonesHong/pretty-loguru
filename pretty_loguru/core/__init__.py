"""
核心模組入口

此模組提供 Pretty Loguru 的核心功能，包括基本日誌操作、
配置管理、處理器管理和日誌清理機制。
"""

# 導入基本配置
from .config import (
    LoggerConfig
)

# 導入基本日誌功能
from .base import (
    configure_logger,
    get_console,
)

# 導入處理器功能
from .handlers import (
    create_destination_filters,
    format_filename
)

# 導入清理功能
from .cleaner import LoggerCleaner

# 導入目標導向格式化工具
from .target_formatter import (
    create_target_method,
    add_target_methods,
    ensure_target_parameters
)

# 導入註冊表
from .registry import (
    register_logger,
    get_logger,
    unregister_logger,
    list_loggers,
    update_logger
)

# 導入事件系統
from .event_system import (
    subscribe,
    unsubscribe,
    post_event,
    list_events,
    clear_events
)

# 導入擴展系統
from .extension_system import (
    register_extension_method
)

# 定義對外可見的功能
__all__ = [
    # 配置
    "LoggerConfig",
    
    # 基本功能
    "configure_logger",
    "get_console",
    
    # 處理器功能
    "create_destination_filters",
    "format_filename",
    
    # 日誌清理
    "LoggerCleaner",
    
    # 目標導向格式化工具
    "create_target_method",
    "add_target_methods",
    "ensure_target_parameters",
    
    # 註冊表功能
    "register_logger",
    "get_logger",
    "unregister_logger",
    "list_loggers",
    "update_logger",
    
    # 事件系統功能
    "subscribe",
    "unsubscribe", 
    "post_event",
    "list_events",
    "clear_events",
    
    # 擴展系統功能
    "register_extension_method"
]