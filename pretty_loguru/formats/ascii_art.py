"""
ASCII 藝術模組

此模組提供用於生成 ASCII 藝術標題和區塊的功能，
增強日誌的視覺效果和結構化呈現。
"""

import re
from typing import List, Optional, Any

from rich.panel import Panel
from rich.console import Console

from pretty_loguru.core.extension_system import register_extension_method

try:
    from art import text2art
    _has_art = True
except ImportError:
    _has_art = False
    # 定義一個空的 text2art 函數，避免引用錯誤
    def text2art(text, **kwargs):
        return f"[Art library not installed: {text}]"

from ..types import EnhancedLogger
from ..core.target_formatter import add_target_methods, ensure_target_parameters
from .block import print_block, format_block_message


# ASCII 字符檢查的正則表達式
# 僅匹配英文、數字和標準 ASCII 符號
ASCII_PATTERN = re.compile(r'^[\x00-\x7F]+$')

def is_ascii_only(text: str) -> bool:
    """檢查文本是否只包含 ASCII 字符"""
    return ASCII_PATTERN.match(text) is not None





@ensure_target_parameters
def print_ascii_header(
    text: str,
    font: str = "standard",
    log_level: str = "INFO",
    border_style: str = "cyan",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    打印 ASCII 藝術標題
    
    Args:
        text: 要轉換為 ASCII 藝術的文本
        font: ASCII 藝術字體
        log_level: 日誌級別
        border_style: 邊框樣式
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
        ImportError: 如果未安裝 art 庫
    """
    # 檢查 art 庫是否已安裝
    if not _has_art:
        error_msg = "The 'art' library is not installed. Please install it using 'pip install art'."
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(text):
        warning_msg = f"ASCII art only supports ASCII characters. The text '{text}' contains non-ASCII characters."
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        if logger_instance:
            logger_instance.warning(f"Removed non-ASCII characters. Using: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("The text contains only non-ASCII characters and cannot create ASCII art.")
        
        text = cleaned_text
    
    # 使用 art 庫生成 ASCII 藝術
    try:
        ascii_art = text2art(text, font=font)
    except Exception as e:
        error_msg = f"Failed to generate ASCII art: {str(e)}"
        if logger_instance:
            logger_instance.error(error_msg)
        raise
    
    # 創建一個帶有邊框的 Panel
    panel = Panel(
        ascii_art,
        border_style=border_style,
    )
    
    # 控制台輸出 - 僅當非僅文件模式時
    if not to_log_file_only:
        console.print(panel)
    
    # 日誌文件輸出 - 僅當非僅控制台模式時
    if logger_instance and not to_console_only:
        # 使用動態設置的 depth 來捕獲實際調用者的位置
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{ascii_art}\n{'=' * 50}"
        )


@ensure_target_parameters
def print_ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = None,
    ascii_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
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
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果 ASCII 標題包含非 ASCII 字符
        ImportError: 如果未安裝 art 庫
    """
    # 檢查 art 庫是否已安裝
    if not _has_art:
        error_msg = "The 'art' library is not installed. Please install it using 'pip install art'."
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 如果沒有提供 ASCII 標題，則使用普通標題
    header_text = ascii_header if ascii_header is not None else title
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(header_text):
        warning_msg = f"ASCII art only supports ASCII characters. The text '{header_text}' contains non-ASCII characters."
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', header_text)
        
        if logger_instance:
            logger_instance.warning(f"Removed non-ASCII characters. Using: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("The ASCII header contains only non-ASCII characters and cannot create ASCII art.")
        
        header_text = cleaned_text
    
    # 生成 ASCII 藝術
    try:
        ascii_art = text2art(header_text, font=ascii_font)
    except Exception as e:
        error_msg = f"Failed to generate ASCII art: {str(e)}"
        if logger_instance:
            logger_instance.error(error_msg)
        raise
    
    # 將 ASCII 藝術添加到消息列表的開頭
    full_message_list = [ascii_art] + message_list
    
    # 構造區塊內容，將多行訊息合併為單一字串
    message = "\n".join(full_message_list)
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



def create_ascii_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例創建 ASCII 藝術相關方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 rich console 實例，如果為 None 則使用新創建的
    """
    if console is None:
        console = Console()
   
    # 定義 ascii_header 的實現
    @ensure_target_parameters
    def _ascii_header_impl(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_ascii_header(text, font=font, log_level=log_level, border_style=border_style,
                           logger_instance=self, console=console,
                           to_console_only=to_console_only, to_log_file_only=to_log_file_only,
                           _target_depth=_target_depth)

    # 定義 ascii_block 的實現
    @ensure_target_parameters
    def _ascii_block_impl(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = None,
        ascii_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_ascii_block(title, message_list, ascii_header=ascii_header, ascii_font=ascii_font,
                          border_style=border_style, log_level=log_level,
                          logger_instance=self, console=console,
                          to_console_only=to_console_only, to_log_file_only=to_log_file_only,
                          _target_depth=_target_depth)

    # 註冊方法
    register_extension_method(logger_instance, "ascii_header", _ascii_header_impl, overwrite=True)
    register_extension_method(logger_instance, "ascii_block", _ascii_block_impl, overwrite=True)