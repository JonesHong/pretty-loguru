from typing import List, cast
from rich.panel import Panel
from .logger_base import _logger, console
from .logger_types import EnhancedLogger


def print_block(
    title: str,
    message_list: List[str],
    border_style: str = "cyan",
    log_level: str = "INFO",  # 可選層級
) -> None:
    """
    打印區塊樣式的日誌，並寫入到日誌文件
    
    Args:
        title: 區塊的標題
        message_list: 日誌的內容列表
        border_style: 區塊邊框顏色
        log_level: 日誌級別
    """
    _logger.opt(ansi=True, depth=1).bind(to_console_only=True).log(
        log_level, "CustomBlock"
    )
    # 構造區塊內容
    message = "\n".join(message_list)
    panel = Panel(
        message,
        title=title,
        title_align="left",
        border_style=border_style,
    )
    # 打印到終端
    console.print(panel)

    formatted_message = f"{title}\n{'=' * 50}\n{message}\n{'=' * 50}"

    _logger.opt(ansi=True, depth=1).bind(to_log_file_only=True).log(
        log_level, f"\n{formatted_message}"
    )  # 僅寫入文件


# 將 block 函數添加到 _logger 並註解其類型
# 這只是動態添加，實際類型檢查需要借助 logger_types.py 中的類型標註
_logger.block = print_block