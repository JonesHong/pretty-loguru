"""
FIGlet 藝術模組

此模組提供用於生成 FIGlet 文本藝術的功能，
是 ASCII 藝術的替代選項，支援更多的字體和樣式。
需要安裝 pyfiglet 庫：pip install pyfiglet
"""

import re
from typing import List, Optional, Any, Set

from rich.panel import Panel
from rich.console import Console

try:
    import pyfiglet
    from pyfiglet import FigletFont
    _has_pyfiglet = True
    # print("Debug: pyfiglet successfully imported")
except ImportError:
    _has_pyfiglet = False
    pyfiglet = None
    FigletFont = None
    print("Debug: pyfiglet import failed")

from ..types import EnhancedLogger
from ..core.target_formatter import add_target_methods, ensure_target_parameters
from .block import print_block
from .ascii_art import is_ascii_only


@ensure_target_parameters
def print_figlet_header(
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
    打印 FIGlet 藝術標題
    
    Args:
        text: 要轉換為 FIGlet 藝術的文本
        font: FIGlet 藝術字體
        log_level: 日誌級別
        border_style: 邊框樣式
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
        ImportError: 如果未安裝 pyfiglet 庫
    """
    # 檢查 pyfiglet 庫是否已安裝
    if not _has_pyfiglet:
        error_msg = "The 'pyfiglet' library is not installed. Please install it using 'pip install pyfiglet'."
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(text):
        warning_msg = f"FIGlet only supports ASCII characters. The text '{text}' contains non-ASCII characters."
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        if logger_instance:
            logger_instance.warning(f"Non-ASCII characters have been removed. Using: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("The text contains only non-ASCII characters and cannot create FIGlet art.")
        
        text = cleaned_text
    
    # 使用 pyfiglet 生成 FIGlet 藝術
    try:
        figlet_art = pyfiglet.figlet_format(text, font=font)
    except Exception as e:
        error_msg = f"Failed to generate FIGlet art: {str(e)}"
        if logger_instance:
            logger_instance.error(error_msg)
        raise
    
    # 創建一個帶有邊框的 Panel
    panel = Panel(
        figlet_art,
        border_style=border_style,
    )
    
    # 控制台輸出 - 僅當非僅文件模式時
    if not to_log_file_only:
        console.print(panel)
    
    # 日誌文件輸出 - 僅當非僅控制台模式時
    if logger_instance and not to_console_only:
        # 使用動態設置的 depth 來捕獲實際調用者的位置
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{figlet_art}\n{'=' * 50}"
        )


@ensure_target_parameters
def print_figlet_block(
    title: str,
    message_list: List[str],
    figlet_header: Optional[str] = None,
    figlet_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    打印帶有 FIGlet 藝術標題的區塊樣式日誌
    
    Args:
        title: 區塊的標題
        message_list: 日誌的內容列表
        figlet_header: FIGlet 藝術標題文本 (如果不提供，則使用 title)
        figlet_font: FIGlet 藝術字體
        border_style: 區塊邊框顏色
        log_level: 日誌級別
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果 FIGlet 標題包含非 ASCII 字符
        ImportError: 如果未安裝 pyfiglet 庫
    """
    # 檢查 pyfiglet 庫是否已安裝
    if not _has_pyfiglet:
        error_msg = "The 'pyfiglet' library is not installed. Please install it using 'pip install pyfiglet'."
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = Console()
    
    # 如果沒有提供 FIGlet 標題，則使用普通標題
    header_text = figlet_header if figlet_header is not None else title
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(header_text):
        warning_msg = f"FIGlet only supports ASCII characters. The text '{header_text}' contains non-ASCII characters."
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', header_text)
        
        if logger_instance:
            logger_instance.warning(f"Non-ASCII characters have been removed. Using: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("The FIGlet header contains only non-ASCII characters and cannot create FIGlet art.")
        
        header_text = cleaned_text
    
    # 生成 FIGlet 藝術
    try:
        figlet_art = pyfiglet.figlet_format(header_text, font=figlet_font)
    except Exception as e:
        error_msg = f"Failed to generate FIGlet art: {str(e)}"
        if logger_instance:
            logger_instance.error(error_msg)
        raise
    
    # 將 FIGlet 藝術添加到消息列表的開頭
    full_message_list = [figlet_art] + message_list
    
    # 構造區塊內容
    message = "\n".join(full_message_list)
    panel = Panel(
        message,
        title=title,
        title_align="left",
        border_style=border_style,
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


def get_figlet_fonts() -> Set[str]:
    """
    獲取所有可用的 FIGlet 字體
    
    Returns:
        Set[str]: 可用字體名稱的集合
        
    Raises:
        ImportError: 如果未安裝 pyfiglet 庫
    """
    if not _has_pyfiglet:
        raise ImportError("The 'pyfiglet' library is not installed. Please install it using 'pip install pyfiglet'.")
    
    return set(FigletFont.getFonts())


def create_figlet_methods(logger_instance: Any, console: Optional[Console] = None) -> bool:
    """
    為 logger 實例創建 FIGlet 藝術相關方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 rich console 實例，如果為 None 則使用新創建的
        
    Returns:
        bool: 如果成功添加方法則返回 True，否則返回 False
    """
    # 檢查 pyfiglet 庫是否已安裝
    if not _has_pyfiglet:
        if hasattr(logger_instance, "warning"):
            logger_instance.warning("'pyfiglet' library is not installed. Skipping adding FIGlet methods.")
        return False
    
    if console is None:
        console = Console()
    
    # 添加 figlet_header 方法
    @ensure_target_parameters
    def figlet_header_method(
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        """
        logger 實例的 FIGlet 藝術標題方法
        
        Args:
            text: 要轉換為 FIGlet 藝術的文本
            font: FIGlet 藝術字體
            log_level: 日誌級別
            border_style: 邊框樣式
            to_console_only: 是否僅輸出到控制台，預設為 False
            to_log_file_only: 是否僅輸出到日誌文件，預設為 False
            _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        """
        # 使用 kwargs 傳遞參數，避免參數重複
        kwargs = {
            "font": font,
            "log_level": log_level,
            "border_style": border_style,
            "logger_instance": logger_instance,
            "console": console,
            "_target_depth": _target_depth,  # 傳遞深度
        }
        
        # 使用當前方法的 to_console_only 和 to_log_file_only
        print_figlet_header(text, **kwargs, to_console_only=to_console_only, to_log_file_only=to_log_file_only)
    
    # 添加 figlet_block 方法
    @ensure_target_parameters
    def figlet_block_method(
        title: str,
        message_list: List[str],
        figlet_header: Optional[str] = None,
        figlet_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        """
        logger 實例的 FIGlet 藝術區塊方法
        
        Args:
            title: 區塊的標題
            message_list: 日誌的內容列表
            figlet_header: FIGlet 藝術標題文本 (如果不提供，則使用 title)
            figlet_font: FIGlet 藝術字體
            border_style: 區塊邊框顏色
            log_level: 日誌級別
            to_console_only: 是否僅輸出到控制台，預設為 False
            to_log_file_only: 是否僅輸出到日誌文件，預設為 False
            _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        """
        # 使用 kwargs 傳遞參數，避免參數重複
        kwargs = {
            "figlet_header": figlet_header,
            "figlet_font": figlet_font,
            "border_style": border_style,
            "log_level": log_level,
            "logger_instance": logger_instance,
            "console": console,
            "_target_depth": _target_depth,  # 傳遞深度
        }
        
        # 使用當前方法的 to_console_only 和 to_log_file_only
        print_figlet_block(title, message_list, **kwargs, to_console_only=to_console_only, to_log_file_only=to_log_file_only)
    
    # 添加 get_figlet_fonts 方法
    def get_fonts_method() -> Set[str]:
        """
        獲取所有可用的 FIGlet 字體
        """
        return get_figlet_fonts()
    
    # 將方法添加到 logger 實例
    logger_instance.figlet_header = figlet_header_method
    logger_instance.figlet_block = figlet_block_method
    logger_instance.get_figlet_fonts = get_fonts_method
    
    # 添加目標特定方法
    add_target_methods(logger_instance, "figlet_header", figlet_header_method)
    add_target_methods(logger_instance, "figlet_block", figlet_block_method)
    
    return True