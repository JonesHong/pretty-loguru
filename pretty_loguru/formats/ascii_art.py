"""
ASCII 藝術模組

此模組提供用於生成 ASCII 藝術標題和區塊的功能，
增強日誌的視覺效果和結構化呈現。
"""

import re
from typing import List, Optional, Any

from rich.panel import Panel
from rich.console import Console

try:
    from art import text2art
    _has_art = True
except ImportError:
    _has_art = False
    # 定義一個空的 text2art 函數，避免引用錯誤
    def text2art(text, **kwargs):
        return f"[Art library not installed: {text}]"

from ..types import EnhancedLogger
from .block import print_block, format_block_message


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
    # 使用正則表達式檢查文本是否符合 ASCII 範圍
    return bool(ASCII_PATTERN.match(text))


def print_ascii_header(
    text: str,
    font: str = "standard",
    log_level: str = "INFO",
    border_style: str = "cyan",
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    logger_instance: Any = None,
    console: Optional[Console] = None,
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
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
        ImportError: 如果未安裝 art 庫
    """
    # 檢查 art 庫是否已安裝
    if not _has_art:
        error_msg = "未安裝 'art' 庫。請使用 'pip install art' 安裝。"
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(text):
        warning_msg = f"ASCII art 只支持 ASCII 字符。文本 '{text}' 包含非 ASCII 字符。"
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        if logger_instance:
            logger_instance.warning(f"已移除非 ASCII 字符。使用: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("文本僅包含非 ASCII 字符，無法創建 ASCII 藝術。")
        
        text = cleaned_text
    
    # 使用 art 庫生成 ASCII 藝術
    try:
        ascii_art = text2art(text, font=font)
    except Exception as e:
        error_msg = f"生成 ASCII 藝術失敗: {str(e)}"
        if logger_instance:
            logger_instance.error(error_msg)
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
    if logger_instance and not to_console_only:
        logger_instance.opt(ansi=True, depth=2).bind(to_log_file_only=True).log(
            log_level, f"\n{ascii_art}\n{'=' * 50}"
        )


def print_ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = None,
    ascii_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
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
        
    Raises:
        ValueError: 如果 ASCII 標題包含非 ASCII 字符
        ImportError: 如果未安裝 art 庫
    """
    # 檢查 art 庫是否已安裝
    if not _has_art:
        error_msg = "未安裝 'art' 庫。請使用 'pip install art' 安裝。"
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
        warning_msg = f"ASCII art 只支持 ASCII 字符。文本 '{header_text}' 包含非 ASCII 字符。"
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', header_text)
        
        if logger_instance:
            logger_instance.warning(f"已移除非 ASCII 字符。使用: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("ASCII 標題僅包含非 ASCII 字符，無法創建 ASCII 藝術。")
        
        header_text = cleaned_text
    
    # 生成 ASCII 藝術
    try:
        ascii_art = text2art(header_text, font=ascii_font)
    except Exception as e:
        error_msg = f"生成 ASCII 藝術失敗: {str(e)}"
        if logger_instance:
            logger_instance.error(error_msg)
        raise
    
    # 將 ASCII 藝術添加到消息列表的開頭
    full_message_list = [ascii_art] + message_list
    
    # 使用 print_block 函數打印區塊，確保傳遞正確的 logger 實例
    # print_block(title, full_message_list, border_style, log_level, logger_instance, console)
      # 如果提供了 logger 實例，我們應該通過調整 depth 來確保捕獲正確的調用位置
    if logger_instance is not None:
        # print_block 會添加額外的堆棧深度，所以直接在這裡實現，而不是調用 print_block
        # 將日誌寫入到終端，僅顯示在終端中
        logger_instance.opt(ansi=True, depth=2).bind(to_console_only=True).log(
            log_level, f"CustomBlock: {title}"
        )
        
        # 構造區塊內容，將多行訊息合併為單一字串
        message = "\n".join(full_message_list)
        
        # 創建 Rich Panel
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
        logger_instance.opt(ansi=True, depth=2).bind(to_log_file_only=True).log(
            log_level, f"\n{formatted_message}"
        )
    else:
        # 如果沒有提供 logger 實例，則使用 print_block 函數
        print_block(title, full_message_list, border_style, log_level, logger_instance, console)


def create_ascii_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例創建 ASCII 藝術相關方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 rich console 實例，如果為 None 則使用新創建的
    """
    if console is None:
        console = Console()
    
    # 為 logger 添加 is_ascii_only 方法
    logger_instance.is_ascii_only = is_ascii_only
   
    # 添加 ascii_header 方法
    def ascii_header_method(
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None:
        """
        logger 實例的 ASCII 藝術標題方法
        """
        # 直接實現，而不是調用 print_ascii_header，以便正確捕獲調用位置
        if not _has_art:
            logger_instance.error("未安裝 'art' 庫。請使用 'pip install art' 安裝。")
            return
        
        # 檢查是否包含非 ASCII 字符
        if not is_ascii_only(text):
            logger_instance.warning(f"ASCII art 只支持 ASCII 字符。文本 '{text}' 包含非 ASCII 字符。")
            
            # 移除非 ASCII 字符
            cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
            
            logger_instance.warning(f"已移除非 ASCII 字符。使用: '{cleaned_text}'")
            
            if not cleaned_text:  # 如果移除後為空，則返回，避免錯誤
                logger_instance.error("文本僅包含非 ASCII 字符，無法創建 ASCII 藝術。")
                return
            
            text = cleaned_text
        
        # 使用 art 庫生成 ASCII 藝術
        try:
            ascii_art = text2art(text, font=font)
        except Exception as e:
            logger_instance.error(f"生成 ASCII 藝術失敗: {str(e)}")
            return
        
        # 創建一個帶有邊框的 Panel
        panel = Panel(
            ascii_art,
            border_style=border_style,
        )
        
        # 控制台輸出
        if not to_log_file_only:
            console.print(panel)
        
        # 日誌文件輸出 - 使用 depth=1 捕獲正確的調用位置
        if not to_console_only:
            logger_instance.opt(ansi=True, depth=1).bind(to_log_file_only=True).log(
                log_level, f"\n{ascii_art}\n{'=' * 50}"
            )
    
    # 添加 ascii_block 方法
    def ascii_block_method(
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = None,
        ascii_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        logger 實例的 ASCII 藝術區塊方法
        """
        # 直接實現，而不是調用 print_ascii_block，以便正確捕獲調用位置
        if not _has_art:
            logger_instance.error("未安裝 'art' 庫。請使用 'pip install art' 安裝。")
            return
        
        # 如果沒有提供 ASCII 標題，則使用普通標題
        header_text = ascii_header if ascii_header is not None else title
        
        # 檢查是否包含非 ASCII 字符
        if not is_ascii_only(header_text):
            logger_instance.warning(f"ASCII art 只支持 ASCII 字符。文本 '{header_text}' 包含非 ASCII 字符。")
            
            # 移除非 ASCII 字符
            cleaned_text = re.sub(r'[^\x00-\x7F]+', '', header_text)
            
            logger_instance.warning(f"已移除非 ASCII 字符。使用: '{cleaned_text}'")
            
            if not cleaned_text:  # 如果移除後為空，則返回，避免錯誤
                logger_instance.error("ASCII 標題僅包含非 ASCII 字符，無法創建 ASCII 藝術。")
                return
            
            header_text = cleaned_text
        
        # 生成 ASCII 藝術
        try:
            ascii_art = text2art(header_text, font=ascii_font)
        except Exception as e:
            logger_instance.error(f"生成 ASCII 藝術失敗: {str(e)}")
            return
        
        # 將 ASCII 藝術添加到消息列表的開頭
        full_message_list = [ascii_art] + message_list
        
        # 直接實現區塊輸出，而不是調用 print_block
        # 將日誌寫入到終端，僅顯示在終端中 - 使用 depth=1 捕獲正確的調用位置
        logger_instance.opt(ansi=True, depth=1).bind(to_console_only=True).log(
            log_level, f"CustomBlock: {title}"
        )
        
        # 構造區塊內容，將多行訊息合併為單一字串
        message = "\n".join(full_message_list)
        
        # 創建 Rich Panel
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
    logger_instance.ascii_header = ascii_header_method
    logger_instance.ascii_block = ascii_block_method
