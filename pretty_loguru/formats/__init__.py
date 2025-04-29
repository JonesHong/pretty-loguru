"""
格式化模組入口

此模組提供 Pretty Loguru 的所有格式化功能，包括區塊格式化、
ASCII 藝術和 FIGlet 文本等。這些功能豐富了日誌的視覺呈現效果。
"""

# 導入區塊格式化功能
from .block import (
    print_block,
    format_block_message,
)

# 導入 ASCII 藝術功能
from .ascii_art import (
    print_ascii_header,
    print_ascii_block,
    is_ascii_only,
)

# 導入 FIGlet 功能 (可選)
try:
    from .figlet import (
        print_figlet_header,
        print_figlet_block,
        get_figlet_fonts,
    )
    _has_figlet = True
except ImportError:
    _has_figlet = False

# 定義對外可見的功能
__all__ = [
    # 區塊格式化
    "print_block",
    "format_block_message",
    
    # ASCII 藝術
    "print_ascii_header",
    "print_ascii_block",
    "is_ascii_only",
]

# 如果 FIGlet 可用，則添加相關功能
if _has_figlet:
    __all__.extend([
        "print_figlet_header",
        "print_figlet_block",
        "get_figlet_fonts",
    ])

# 提供檢查 FIGlet 是否可用的函數
def has_figlet() -> bool:
    """
    檢查 FIGlet 功能是否可用
    
    Returns:
        bool: 如果 FIGlet 功能可用則返回 True，否則返回 False
    """
    return _has_figlet
