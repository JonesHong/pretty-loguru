"""
工廠模組入口

此模組提供 Logger 實例的創建和管理功能，包括各種自定義方法的添加。
工廠模式使得創建和配置 Logger 實例變得簡單和一致。
"""

from .creator import (
    create_logger,
    default_logger,
    get_logger,
    set_logger,
    unregister_logger,
    list_loggers,
)

from .methods import (
    add_custom_methods,
    add_output_methods,
    add_format_methods,
)

# 定義對外可見的功能
__all__ = [
    # Logger 創建和管理
    "create_logger",
    "default_logger",
    "get_logger",
    "set_logger",
    "unregister_logger",
    "list_loggers",
    
    # 方法擴展
    "add_custom_methods",
    "add_output_methods",
    "add_format_methods",
]
