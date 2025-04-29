"""
Logger 方法擴展模組

此模組提供各種方法，用於擴展 Logger 實例的功能，
包括自定義輸出方法和格式化方法。
"""

from typing import Any, Optional

from rich.console import Console

from ..types import EnhancedLogger
from ..core.base import _console_only, _file_only
from ..formats.block import create_block_method
from ..formats.ascii_art import create_ascii_methods
from ..formats.figlet import create_figlet_methods, _has_pyfiglet


def add_output_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例添加輸出目標相關方法
    
    Args:
        logger_instance: 要擴展的 logger 實例
        console: 要使用的 console 實例，如果為 None 則使用新創建的
    """
    # 為 logger_instance 新增只輸出到控制台的方法
    
    # 控制台專用方法
    logger_instance.console = lambda level, message, *args, **kwargs: _console_only(logger_instance, level, message, *args, **kwargs)
    logger_instance.console_debug = lambda message, *args, **kwargs: _console_only(logger_instance, "DEBUG", message, *args, **kwargs)
    logger_instance.console_info = lambda message, *args, **kwargs: _console_only(logger_instance, "INFO", message, *args, **kwargs)
    logger_instance.console_success = lambda message, *args, **kwargs: _console_only(logger_instance, "SUCCESS", message, *args, **kwargs)
    logger_instance.console_warning = lambda message, *args, **kwargs: _console_only(logger_instance, "WARNING", message, *args, **kwargs)
    logger_instance.console_error = lambda message, *args, **kwargs: _console_only(logger_instance, "ERROR", message, *args, **kwargs)
    logger_instance.console_critical = lambda message, *args, **kwargs: _console_only(logger_instance, "CRITICAL", message, *args, **kwargs)

    # 文件專用方法
    logger_instance.file = lambda level, message, *args, **kwargs: _file_only(logger_instance, level, message, *args, **kwargs)
    logger_instance.file_debug = lambda message, *args, **kwargs: _file_only(logger_instance, "DEBUG", message, *args, **kwargs)
    logger_instance.file_info = lambda message, *args, **kwargs: _file_only(logger_instance, "INFO", message, *args, **kwargs)
    logger_instance.file_success = lambda message, *args, **kwargs: _file_only(logger_instance, "SUCCESS", message, *args, **kwargs)
    logger_instance.file_warning = lambda message, *args, **kwargs: _file_only(logger_instance, "WARNING", message, *args, **kwargs)
    logger_instance.file_error = lambda message, *args, **kwargs: _file_only(logger_instance, "ERROR", message, *args, **kwargs)
    logger_instance.file_critical = lambda message, *args, **kwargs: _file_only(logger_instance, "CRITICAL", message, *args, **kwargs)

    # 開發模式方法 (別名為控制台方法)
    logger_instance.dev = logger_instance.console
    logger_instance.dev_debug = logger_instance.console_debug
    logger_instance.dev_info = logger_instance.console_info
    logger_instance.dev_success = logger_instance.console_success
    logger_instance.dev_warning = logger_instance.console_warning
    logger_instance.dev_error = logger_instance.console_error
    logger_instance.dev_critical = logger_instance.console_critical


def add_format_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例添加格式化相關方法
    
    Args:
        logger_instance: 要擴展的 logger 實例
        console: 要使用的 console 實例，如果為 None 則使用新創建的
    """
    # 添加區塊格式化方法
    create_block_method(logger_instance, console)
    
    # 添加 ASCII 藝術方法
    create_ascii_methods(logger_instance, console)
    
    # 如果 pyfiglet 可用，添加 FIGlet 方法
    if _has_pyfiglet:
        create_figlet_methods(logger_instance, console)


def add_custom_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例添加所有自定義方法
    
    這是一個綜合函數，它會添加所有的輸出和格式化方法。
    
    Args:
        logger_instance: 要擴展的 logger 實例
        console: 要使用的 console 實例，如果為 None 則使用新創建的
    """
    # 添加輸出目標相關方法
    add_output_methods(logger_instance, console)
    
    # 添加格式化相關方法
    add_format_methods(logger_instance, console)


def register_extension_method(
    logger_instance: Any,
    method_name: str,
    method_function: Any,
    overwrite: bool = False
) -> bool:
    """
    註冊自定義擴展方法到 logger 實例
    
    此函數允許用戶動態地擴展 logger 的功能。
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        method_name: 方法名稱
        method_function: 方法函數
        overwrite: 如果方法已存在，是否覆蓋，預設為 False
        
    Returns:
        bool: 如果成功註冊則返回 True，否則返回 False
        
    Examples:
        >>> def my_custom_log(self, message, *args, **kwargs):
        ...     self.info(f"CUSTOM: {message}", *args, **kwargs)
        >>> 
        >>> register_extension_method(logger, "custom", my_custom_log)
        >>> logger.custom("Hello, world!")  # 輸出: "CUSTOM: Hello, world!"
    """
    # 檢查方法是否已存在
    if hasattr(logger_instance, method_name) and not overwrite:
        if hasattr(logger_instance, "warning"):
            logger_instance.warning(f"方法 '{method_name}' 已存在，未註冊。若要覆蓋，請使用 overwrite=True。")
        return False
    
    # 設置方法到 logger 實例
    setattr(logger_instance, method_name, method_function.__get__(logger_instance, type(logger_instance)))
    
    # 記錄註冊信息
    if hasattr(logger_instance, "debug"):
        logger_instance.debug(f"已註冊自定義方法: {method_name}")
    
    return True