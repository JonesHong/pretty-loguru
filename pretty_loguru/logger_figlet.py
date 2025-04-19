"""
這個模塊提供了使用 pyfiglet 替代 art 庫的實現。
要使用這些功能，請取消註釋並安裝 pyfiglet 庫:
pip install pyfiglet
"""

from typing import List, Optional
import re
# import pyfiglet  # 取消註釋以啟用 pyfiglet
from rich.panel import Panel
from .logger_base import _logger, console
from .logger_block import print_block
from .logger_ascii import is_ascii_only


def print_figlet_header(
    text: str,
    font: str = "standard",
    log_level: str = "INFO",
    border_style: str = "cyan",
    to_console_only: bool = False,
    to_log_file_only: bool = False,
):
    """
    使用 pyfiglet 打印 FIGlet 文本藝術標題
    
    Args:
        text: 要轉換為 FIGlet 的文本
        font: FIGlet 字體
        log_level: 日誌級別
        border_style: 邊框樣式
        to_console_only: 是否僅輸出到控制台
        to_log_file_only: 是否僅輸出到日誌文件
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
        ImportError: 如果 pyfiglet 未安裝
    """
    try:
        import pyfiglet  # 動態導入 pyfiglet，避免未安裝時出錯
    except ImportError:
        # 如果未安裝 pyfiglet，記錄錯誤並拋出異常
        _logger.error("pyfiglet 未安裝。請使用以下命令安裝: pip install pyfiglet")
        raise ImportError("pyfiglet 未安裝。請使用以下命令安裝: pip install pyfiglet")
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(text):
        _logger.warning(f"FIGlet 僅支持 ASCII 字符。文本 '{text}' 包含非 ASCII 字符。")
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # 移除非 ASCII 字符
        _logger.warning(f"已移除非 ASCII 字符。使用: '{text}'")
        if not text:  # 如果移除後為空
            raise ValueError("文本僅包含非 ASCII 字符，無法生成 FIGlet 藝術。")
    
    # 使用 pyfiglet 生成 FIGlet 藝術
    try:
        figlet_art = pyfiglet.figlet_format(text, font=font)
    except Exception as e:
        # 捕獲生成 FIGlet 藝術時的異常
        _logger.error(f"生成 FIGlet 藝術失敗: {str(e)}")
        raise
    
    # 創建一個帶有邊框的 Panel
    panel = Panel(
        figlet_art,
        border_style=border_style,
    )
    
    # 控制台輸出
    if not to_log_file_only:
        console.print(panel)
    
    # 日誌文件輸出
    if not to_console_only:
        _logger.opt(ansi=True, depth=1).bind(to_log_file_only=True).log(
            log_level, f"\n{figlet_art}\n{'=' * 50}"
        )


def print_figlet_block(
    title: str,
    message_list: List[str],
    figlet_header: Optional[str] = None,
    figlet_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
):
    """
    打印帶有 FIGlet 藝術標題的區塊樣式日誌
    
    Args:
        title: 區塊的標題
        message_list: 日誌的內容列表
        figlet_header: FIGlet 藝術標題文本 (如果不提供，則使用 title)
        figlet_font: FIGlet 藝術字體
        border_style: 區塊邊框顏色
        log_level: 日誌級別
        
    Raises:
        ValueError: 如果 FIGlet 標題包含非 ASCII 字符
        ImportError: 如果 pyfiglet 未安裝
    """
    try:
        import pyfiglet  # 動態導入 pyfiglet，避免未安裝時出錯
    except ImportError:
        # 如果未安裝 pyfiglet，記錄錯誤並拋出異常
        _logger.error("pyfiglet 未安裝。請使用以下命令安裝: pip install pyfiglet")
        raise ImportError("pyfiglet 未安裝。請使用以下命令安裝: pip install pyfiglet")
    
    # 如果沒有提供 FIGlet 標題，則使用普通標題
    header_text = figlet_header if figlet_header is not None else title
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(header_text):
        _logger.warning(f"FIGlet 僅支持 ASCII 字符。文本 '{header_text}' 包含非 ASCII 字符。")
        header_text = re.sub(r'[^\x00-\x7F]+', '', header_text)  # 移除非 ASCII 字符
        _logger.warning(f"已移除非 ASCII 字符。使用: '{header_text}'")
        if not header_text:  # 如果移除後為空
            raise ValueError("FIGlet 標題僅包含非 ASCII 字符，無法生成 FIGlet 藝術。")
    
    # 生成 FIGlet 藝術
    try:
        figlet_art = pyfiglet.figlet_format(header_text, font=figlet_font)
    except Exception as e:
        # 捕獲生成 FIGlet 藝術時的異常
        _logger.error(f"生成 FIGlet 藝術失敗: {str(e)}")
        raise
    
    # 將 FIGlet 藝術添加到消息列表的開頭
    full_message_list = [figlet_art] + message_list
    
    # 使用現有的 print_block 函數
    print_block(title, full_message_list, border_style, log_level)


# 以下函數需要取消註釋才能使用
# # 添加到 _logger
# _logger.figlet_header = print_figlet_header
# _logger.figlet_block = print_figlet_block


def get_figlet_fonts():
    """
    獲取所有可用的 FIGlet 字體
    
    Returns:
        List[str]: 可用字體列表
        
    Raises:
        ImportError: 如果 pyfiglet 未安裝
    """
    try:
        from pyfiglet import FigletFont  # 動態導入 FigletFont 類
        return FigletFont.getFonts()  # 返回所有可用字體
    except ImportError:
        # 如果未安裝 pyfiglet，記錄錯誤並拋出異常
        _logger.error("pyfiglet 未安裝。請使用以下命令安裝: pip install pyfiglet")
        raise ImportError("pyfiglet 未安裝。請使用以下命令安裝: pip install pyfiglet")