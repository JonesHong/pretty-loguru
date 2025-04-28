from typing import List, Optional, cast
from rich.panel import Panel
from .logger_base import _logger, console
from .logger_types import EnhancedLogger


def print_block(
    title: str,
    message_list: List[str],
    border_style: str = "cyan",
    log_level: str = "INFO",  # 可選層級
    logger_instance = None,
) -> None:
    """
    打印區塊樣式的日誌，並寫入到日誌文件
    
    Args:
        title: 區塊的標題
        message_list: 日誌的內容列表
        border_style: 區塊邊框顏色
        log_level: 日誌級別
        logger_instance: 要使用的 logger 實例，預設為全局 _logger
    """
    # 確定要使用的 logger 實例
    target_logger = _logger if logger_instance is None else logger_instance
    
    # 將日誌寫入到終端，僅顯示在終端中
    target_logger.opt(ansi=True, depth=1).bind(to_console_only=True).log(
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
    target_logger.opt(ansi=True, depth=1).bind(to_log_file_only=True).log(
        log_level, f"\n{formatted_message}"
    )


# 不再將 print_block 函數直接添加到 _logger
# 這將由 logger_factory.py 中的 _add_custom_methods 函數處理
# _logger.block = print_block