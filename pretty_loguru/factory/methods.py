"""
Logger 方法擴展模組

此模組提供各種方法，用於擴展 Logger 實例的功能，
包括自定義輸出方法和格式化方法。
"""

from typing import Any, Callable, Optional

from rich.console import Console

from pretty_loguru.formats import has_figlet

from ..types import PrettyLogger

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

    # 注意（最新版）：不再注入 console_*/file_* 等「目標導向日誌方法」。
    #
    # 目標導向的 canonical 做法是使用 loguru 原生的 bind + filters：
    # - logger.opt(depth=...).bind(to_console_only=True).info(...)
    # - logger.opt(depth=...).bind(to_file_only=True).info(...)
    #
    # 對外教學與 examples 以 pretty_loguru.addons.log_to_targets() 作為最簡單入口。

    setattr(logger_instance, "_pretty_loguru_addons_injected", True)
    _install_bind_addons_injection(logger_instance, console)


def _install_bind_addons_injection(logger_instance: Any, console: Optional[Console]) -> None:
    """
    讓 `logger.bind(...)` 回傳的 logger 也具備 formats 方法。

    注意：只包裝 `bind()`（不包裝 `opt()`），避免每次記錄 event 都付出額外成本。
    """
    if getattr(logger_instance, "_pretty_loguru_bind_addons_installed", False):
        return

    original_bind = getattr(logger_instance, "bind", None)
    if not callable(original_bind):
        return

    setattr(logger_instance, "_pretty_loguru_original_bind", original_bind)

    def _bind_wrapper(**kwargs: Any) -> Any:
        child = original_bind(**kwargs)
        try:
            if not getattr(child, "_pretty_loguru_addons_injected", False):
                add_custom_methods(child, console)
        except Exception:
            pass
        return child

    setattr(logger_instance, "bind", _bind_wrapper)
    setattr(logger_instance, "_pretty_loguru_bind_addons_installed", True)
