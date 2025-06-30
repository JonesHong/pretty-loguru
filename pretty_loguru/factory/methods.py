"""
Logger 方法擴展模組

此模組提供各種方法，用於擴展 Logger 實例的功能，
包括自定義輸出方法和格式化方法。
"""

from typing import Any, Callable, Optional

from rich.console import Console

from pretty_loguru.formats import has_figlet
from pretty_loguru.core.extension_system import register_extension_method

from ..types import EnhancedLogger
from ..core.target_formatter import add_target_methods

# 直接導入格式化方法模組
from ..formats.block import create_block_method
from ..formats.ascii_art import create_ascii_methods

# 這裡的導入方式需要修改
# 我們直接在 add_format_methods 函數中處理 FIGlet 相關功能
# 避免導入錯誤


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
    
    # 添加 Rich 組件方法
    from ..formats import create_rich_methods
    create_rich_methods(logger_instance, console)
    
    # 嘗試添加 FIGlet 方法
    if has_figlet():
        try:
            from ..formats import create_figlet_methods
            create_result = create_figlet_methods(logger_instance, console)
            if create_result and hasattr(logger_instance, "debug"):
                # logger_instance.debug("Successfully added FIGlet-related methods")
                pass
        except Exception as e:
            if hasattr(logger_instance, "warning"):
                logger_instance.warning(f"An error occurred while adding FIGlet methods: {str(e)}")
    else:
        if hasattr(logger_instance, "debug"):
            # logger_instance.debug("The pyfiglet library is not installed, skipping the addition of FIGlet methods")
            pass


def add_custom_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例添加所有自定義方法
    
    這是一個綜合函數，它會添加所有的輸出和格式化方法。
    
    Args:
        logger_instance: 要擴展的 logger 實例
        console: 要使用的 console 實例，如果為 None 則使用新創建的
    """
    # 添加格式化相關方法
    add_format_methods(logger_instance, console)
    
    # 檢查 figlet_block 方法是否被正確添加
    if not hasattr(logger_instance, "figlet_block"):
        try:
            # 再次嘗試直接添加 FIGlet 方法
            from ..formats.figlet import create_figlet_methods
            create_figlet_methods(logger_instance, console)
        except ImportError:
            # 如果無法導入 pyfiglet，則不添加相關方法
            pass
        except Exception as e:
            # 記錄其他錯誤（如果可能）
            if hasattr(logger_instance, "warning"):
                logger_instance.warning(f"An error occurred while attempting to add FIGlet methods again: {str(e)}")

    # Add targeted logging methods (console-only, file-only)
    def _create_targeted_log_method(target_type: str, level: str):
        """創建針對特定目標的日誌方法的工廠函數"""
        bind_key = f"to_{target_type}_only"
        def method(self, message: str, *args, **kwargs):
            self.opt(depth=1).bind(**{bind_key: True}).log(level, message, *args, **kwargs)
        return method

    # 支援的日誌級別
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "SUCCESS", "CRITICAL"]
    
    # 添加 console-only 方法
    for level in log_levels:
        method_name = f"console_{level.lower()}"
        method = _create_targeted_log_method("console", level)
        register_extension_method(logger_instance, method_name, method, overwrite=True)
    
    # 添加 file-only 方法
    for level in log_levels:
        method_name = f"file_{level.lower()}"
        method = _create_targeted_log_method("log_file", level)
        register_extension_method(logger_instance, method_name, method, overwrite=True)
    
    # 添加通用的 console 和 file 方法
    def console_method(self, level: str, message: str, *args, **kwargs):
        """通用的僅輸出到控制台的日誌方法"""
        self.opt(depth=1).bind(to_console_only=True).log(level, message, *args, **kwargs)
    
    def file_method(self, level: str, message: str, *args, **kwargs):
        """通用的僅輸出到文件的日誌方法"""
        self.opt(depth=1).bind(to_log_file_only=True).log(level, message, *args, **kwargs)
    
    register_extension_method(logger_instance, "console", console_method, overwrite=True)
    register_extension_method(logger_instance, "file", file_method, overwrite=True)
    
    # 添加開發模式方法（與 console 方法相同，但語義更明確）
    def dev_info_method(self, message: str, *args, **kwargs):
        """開發模式資訊日誌方法（僅輸出到控制台）"""
        self.opt(depth=1).bind(to_console_only=True).info(message, *args, **kwargs)
    
    def dev_debug_method(self, message: str, *args, **kwargs):
        """開發模式除錯日誌方法（僅輸出到控制台）"""
        self.opt(depth=1).bind(to_console_only=True).debug(message, *args, **kwargs)
    
    register_extension_method(logger_instance, "dev_info", dev_info_method, overwrite=True)
    register_extension_method(logger_instance, "dev_debug", dev_debug_method, overwrite=True)


