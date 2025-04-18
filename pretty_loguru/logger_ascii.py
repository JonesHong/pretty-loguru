from typing import List, Optional, cast
import re
from art import text2art
from rich.panel import Panel
from .logger_base import _logger, console
from .logger_block import print_block
from .logger_types import EnhancedLogger


# ASCII 字符檢查的正則表達式
# 僅匹配英文、數字和標準 ASCII 符號
ASCII_PATTERN = re.compile(r'^[\x00-\x7F]+$')


def is_ascii_only(text: str) -> bool:
    """
    檢查文本是否只包含 ASCII 字符
    
    Args:
        text: 要檢查的文本
        
    Returns:
        bool: 如果只包含 ASCII 字符則返回 True，否則返回 False
    """
    return bool(ASCII_PATTERN.match(text))


def print_ascii_header(
    text: str,
    font: str = "standard",
    log_level: str = "INFO",
    border_style: str = "cyan",
    to_console_only: bool = False,
    to_log_file_only: bool = False,
) -> None:
    """
    打印 ASCII 藝術標題
    
    Args:
        text: 要轉換為 ASCII 藝術的文本
        font: ASCII 藝術字體
        log_level: 日誌級別
        border_style: 邊框樣式
        to_console_only: 是否僅輸出到控制台
        to_log_file_only: 是否僅輸出到日誌文件
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
    """
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(text):
        _logger.warning(f"ASCII art only supports ASCII characters. Text '{text}' contains non-ASCII characters.")
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # 移除非 ASCII 字符
        _logger.warning(f"Non-ASCII characters removed. Using: '{text}'")
        if not text:  # 如果移除後為空
            raise ValueError("Text contains only non-ASCII characters. Cannot create ASCII art.")
    
    # 使用 art 庫生成 ASCII 藝術
    try:
        ascii_art = text2art(text, font=font)
    except Exception as e:
        _logger.error(f"Failed to create ASCII art: {str(e)}")
        raise
    
    # 創建一個帶有邊框的 Panel
    panel = Panel(
        ascii_art,
        border_style=border_style,
    )
    
    # 控制台輸出
    if not to_log_file_only:
        console.print(panel)
    
    # 日誌文件輸出
    if not to_console_only:
        _logger.opt(ansi=True, depth=1).bind(to_log_file_only=True).log(
            log_level, f"\n{ascii_art}\n{'=' * 50}"
        )


def print_ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = None,
    ascii_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
) -> None:
    """
    打印帶有 ASCII 藝術標題的區塊樣式日誌
    
    Args:
        title: 區塊的標題
        message_list: 日誌的內容列表
        ascii_header: ASCII 藝術標題文本 (如果不提供，則使用 title)
        ascii_font: ASCII 藝術字體
        border_style: 區塊邊框顏色
        log_level: 日誌級別
        
    Raises:
        ValueError: 如果 ASCII 標題包含非 ASCII 字符
    """
    # 如果沒有提供 ASCII 標題，則使用普通標題
    header_text = ascii_header if ascii_header is not None else title
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(header_text):
        _logger.warning(f"ASCII art only supports ASCII characters. Text '{header_text}' contains non-ASCII characters.")
        header_text = re.sub(r'[^\x00-\x7F]+', '', header_text)  # 移除非 ASCII 字符
        _logger.warning(f"Non-ASCII characters removed. Using: '{header_text}'")
        if not header_text:  # 如果移除後為空
            raise ValueError("ASCII header contains only non-ASCII characters. Cannot create ASCII art.")
    
    # 生成 ASCII 藝術
    try:
        ascii_art = text2art(header_text, font=ascii_font)
    except Exception as e:
        _logger.error(f"Failed to create ASCII art: {str(e)}")
        raise
    
    # 將 ASCII 藝術添加到消息列表的開頭
    full_message_list = [ascii_art] + message_list
    
    # 使用現有的 print_block 函數
    print_block(title, full_message_list, border_style, log_level)


# 添加到 _logger 並註解其類型
# 這只是動態添加，實際類型檢查需要借助 logger_types.py 中的類型標註
_logger.ascii_header = print_ascii_header
_logger.ascii_block = print_ascii_block
_logger.is_ascii_only = is_ascii_only