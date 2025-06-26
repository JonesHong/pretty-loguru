"""
區塊格式化模組

此模組提供用於創建格式化日誌區塊的功能，可以為日誌消息添加邊框、
標題和特定樣式，增強日誌的可讀性和視覺效果。
"""

from typing import List, Optional, Any

from rich.panel import Panel
from rich.console import Console

from ..types import EnhancedLogger
from ..core.target_formatter import add_target_methods, ensure_target_parameters


def format_block_message(
    title: str,
    message_list: List[str],
    separator: str = "=",
    separator_length: int = 50,
) -> str:
    """
    格式化區塊消息為單一字符串
    
    Args:
        title: 區塊的標題
        message_list: 消息列表
        separator: 分隔線字符，預設為 "="
        separator_length: 分隔線長度，預設為 50
        
    Returns:
        str: 格式化後的消息字符串
    """
    # 合併消息列表為單一字符串
    message = "\n".join(message_list)
    
    # 創建分隔線
    separator_line = separator * separator_length
    
    # 格式化為帶有標題和分隔線的區塊
    return f"{title}\n{separator_line}\n{message}\n{separator_line}"


@ensure_target_parameters
def print_block(
    title: str,
    message_list: List[str],
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    打印區塊樣式的日誌，並寫入到日誌文件
    
    Args:
        title: 區塊的標題
        message_list: 日誌的內容列表
        border_style: 區塊邊框顏色，預設為 "cyan"
        log_level: 日誌級別，預設為 "INFO"
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
    """
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 構造區塊內容，將多行訊息合併為單一字串
    message = "\n".join(message_list)
    panel = Panel(
        message,
        title=title,  # 設定區塊標題
        title_align="left",  # 標題靠左對齊
        border_style=border_style,  # 設定邊框樣式
    )
    
    # 只有當非僅文件模式時，才輸出到控制台
    if not to_log_file_only and logger_instance is not None:
        # 將日誌寫入到終端，僅顯示在終端中
        # 使用動態設置的 depth 來捕獲實際調用者的位置
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, f"CustomBlock: {title}"
        )
        
        # 打印區塊到終端
        console.print(panel)

    # 只有當非僅控制台模式時，才輸出到文件
    if not to_console_only and logger_instance is not None:
        # 格式化訊息，方便寫入日誌文件
        formatted_message = f"{title}\n{'=' * 50}\n{message}\n{'=' * 50}"

        # 將格式化後的訊息寫入日誌文件，僅寫入文件中
        # 使用動態設置的 depth 來捕獲實際調用者的位置
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{formatted_message}"
        )


def create_block_method(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例創建 block 方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 rich console 實例，如果為 None 則使用新創建的
    """
    if console is None:
        console = Console()
    
    @ensure_target_parameters
    def block_method(
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        """
        logger 實例的區塊日誌方法
        
        Args:
            title: 區塊的標題
            message_list: 區塊內的內容列表
            border_style: 邊框樣式，預設為 "cyan"
            log_level: 日誌級別，預設為 "INFO"
            to_console_only: 是否僅輸出到控制台，預設為 False
            to_log_file_only: 是否僅輸出到日誌文件，預設為 False
            _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        """
        # 使用 kwargs 傳遞參數，避免參數重複
        kwargs = {
            "border_style": border_style,
            "log_level": log_level,
            "logger_instance": logger_instance,
            "console": console,
            "_target_depth": _target_depth,  # 傳遞深度
        }
        
        # 使用當前方法的 to_console_only 和 to_log_file_only
        print_block(title, message_list, **kwargs, to_console_only=to_console_only, to_log_file_only=to_log_file_only)
    
    # 將方法添加到 logger 實例
    logger_instance.block = block_method
    
    # 添加目標特定方法
    add_target_methods(logger_instance, "block", block_method)