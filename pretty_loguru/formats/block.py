"""
區塊格式化模組

此模組提供用於創建格式化日誌區塊的功能，可以為日誌消息添加邊框、
標題和特定樣式，增強日誌的可讀性和視覺效果。
"""

from typing import List, Optional, Any, Union

from rich.panel import Panel
from rich.console import Console
from rich import box as rich_box
from ..core.base import get_console

from ..types import EnhancedLogger
from ..core.target_formatter import add_target_methods, ensure_target_parameters


# Box style mapping
BOX_STYLES = {
    # Basic styles
    "ascii": rich_box.ASCII,
    "ascii2": rich_box.ASCII2,
    "square": rich_box.SQUARE,
    "rounded": rich_box.ROUNDED,
    "double": rich_box.DOUBLE,
    "heavy": rich_box.HEAVY,
    "minimal": rich_box.MINIMAL,
    "simple": rich_box.SIMPLE,
    
    # Header variations
    "heavy_head": rich_box.HEAVY_HEAD,
    "double_edge": rich_box.DOUBLE_EDGE,
    "ascii_double_head": rich_box.ASCII_DOUBLE_HEAD,
    "minimal_double_head": rich_box.MINIMAL_DOUBLE_HEAD,
    "minimal_heavy_head": rich_box.MINIMAL_HEAVY_HEAD,
    "simple_head": rich_box.SIMPLE_HEAD,
    "simple_heavy": rich_box.SIMPLE_HEAVY,
    "square_double_head": rich_box.SQUARE_DOUBLE_HEAD,
    
    # Edge styles
    "heavy_edge": rich_box.HEAVY_EDGE,
    
    # Special styles
    "horizontals": rich_box.HORIZONTALS,
    "markdown": rich_box.MARKDOWN,
    
    # Aliases for common variations
    "thick": rich_box.HEAVY,  # Alias for heavy
}


def get_box_style(box_name: Optional[str] = None):
    """
    獲取 box 樣式對象
    
    Args:
        box_name: box 樣式名稱，如 "double", "rounded" 等
        
    Returns:
        對應的 box 樣式對象，如果名稱無效則返回默認樣式
    """
    if box_name is None:
        return rich_box.ROUNDED  # 默認使用圓角樣式
    
    return BOX_STYLES.get(box_name.lower(), rich_box.ROUNDED)


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
    border_style: Union[str, None] = "cyan",
    box: Union[str, None] = None,
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
        border_style: 區塊邊框顏色（如 "cyan", "red" 等）或 box 樣式名稱（如 "double", "rounded" 等）
                     為了向後兼容，如果傳入的是 box 樣式名稱，會自動識別
        box: 明確指定的 box 樣式名稱，會覆蓋 border_style 中的 box 樣式
        log_level: 日誌級別，預設為 "INFO"
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
    """
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = get_console()
    
    # 處理 border_style 參數的向後兼容
    # 如果 border_style 是 box 樣式名稱，則轉換為 box 參數
    actual_border_style = border_style
    actual_box = box
    
    if border_style and border_style.lower() in BOX_STYLES and not box:
        # border_style 是 box 樣式名稱
        actual_box = border_style
        actual_border_style = "cyan"  # 使用默認顏色
    
    # 獲取 box 樣式對象
    box_style = get_box_style(actual_box)
    
    # 構造區塊內容，將多行訊息合併為單一字串
    message = "\n".join(message_list)
    panel = Panel(
        message,
        title=title,  # 設定區塊標題
        title_align="left",  # 標題靠左對齊
        border_style=actual_border_style,  # 設定邊框顏色
        box=box_style,  # 設定 box 樣式
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
        console = get_console()
    
    @ensure_target_parameters
    def block_method(
        title: str,
        message_list: List[str],
        border_style: Union[str, None] = "cyan",
        box: Union[str, None] = None,
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
            border_style: 邊框顏色（如 "cyan", "red" 等）或 box 樣式名稱（如 "double", "rounded" 等）
                         為了向後兼容，如果傳入的是 box 樣式名稱，會自動識別
            box: 明確指定的 box 樣式名稱，會覆蓋 border_style 中的 box 樣式
            log_level: 日誌級別，預設為 "INFO"
            to_console_only: 是否僅輸出到控制台，預設為 False
            to_log_file_only: 是否僅輸出到日誌文件，預設為 False
            _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        """
        # 直接傳遞明確參數
        print_block(
            title,
            message_list,
            border_style=border_style,
            box=box,
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth
        )
    
    # 將方法添加到 logger 實例
    logger_instance.block = block_method
    
    # 添加目標特定方法
    add_target_methods(logger_instance, "block", block_method)