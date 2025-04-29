"""
區塊格式化模組

此模組提供用於創建格式化日誌區塊的功能，可以為日誌消息添加邊框、
標題和特定樣式，增強日誌的可讀性和視覺效果。
"""

from typing import List, Optional, Any

from rich.panel import Panel
from rich.console import Console

from ..types import EnhancedLogger


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


def print_block(
    title: str,
    message_list: List[str],
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
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
    """
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 將日誌寫入到終端，僅顯示在終端中
    if logger_instance is not None:
        logger_instance.opt(ansi=True, depth=2).bind(to_console_only=True).log(
            log_level, f"CustomBlock: {title}"
        )
    
    # 構造區塊內容，將多行訊息合併為單一字串
    message = "\n".join(message_list)
    panel = Panel(
        message,
        title=title,  # 設定區塊標題
        title_align="left",  # 標題靠左對齊
        border_style=border_style,  # 設定邊框樣式
    )
    
    # 打印區塊到終端
    console.print(panel)

    # 格式化訊息，方便寫入日誌文件
    formatted_message = f"{title}\n{'=' * 50}\n{message}\n{'=' * 50}"

    # 將格式化後的訊息寫入日誌文件，僅寫入文件中
    if logger_instance is not None:
        logger_instance.opt(ansi=True, depth=2).bind(to_log_file_only=True).log(
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
    
    def block_method(
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        logger 實例的區塊日誌方法
        """
        # 直接實現，而不是調用 print_block 函數，以便正確捕獲調用位置
        # 將日誌寫入到終端，僅顯示在終端中 - 使用 depth=1 捕獲正確的調用位置
        logger_instance.opt(ansi=True, depth=1).bind(to_console_only=True).log(
            log_level, f"CustomBlock: {title}"
        )
        
        # 構造區塊內容，將多行訊息合併為單一字串
        message = "\n".join(message_list)
        panel = Panel(
            message,
            title=title,  # 設定區塊標題
            title_align="left",  # 標題靠左對齊
            border_style=border_style,  # 設定邊框樣式
        )
        
        # 打印區塊到終端
        console.print(panel)

        # 格式化訊息，方便寫入日誌文件
        formatted_message = f"{title}\n{'=' * 50}\n{message}\n{'=' * 50}"

        # 將格式化後的訊息寫入日誌文件，僅寫入文件中 - 使用 depth=1 捕獲正確的調用位置
        logger_instance.opt(ansi=True, depth=1).bind(to_log_file_only=True).log(
            log_level, f"\n{formatted_message}"
        )
    
    # 將方法添加到 logger 實例
    logger_instance.block = block_method
