"""
Pretty Loguru 日誌系統包入口

此模組提供了增強型的 Loguru 日誌系統，包含區塊式日誌、ASCII 藝術標題
以及與各種框架的集成功能，使日誌記錄變得更加直觀和美觀。
"""

import sys
from typing import cast, Optional, Dict, Any, Union, Literal, List, Set
from pathlib import Path

# 導入類型標註
from .types import EnhancedLogger

from .core.base import (
    configure_logger,
    get_console,
)

# 導入核心配置和功能
from .core.config import (
    LoggerConfig
)

# 日誌預設參數
from .core.presets import (
    PresetType,
    PresetFactory
)


# 導入目標導向格式化工具
from .core.target_formatter import (
    create_target_method,
    add_target_methods,
    ensure_target_parameters
)

# 導入工廠功能 - 注意這裡使用新的 default_logger 函數
from .factory.creator import (
    create_logger,
    default_logger,
    get_logger,
    set_logger,
    unregister_logger,
    list_loggers,
    reinit_logger
)

# 導入格式化功能
from .formats.block import print_block
from .formats.ascii_art import print_ascii_header, print_ascii_block, is_ascii_only
from .formats.rich_components import print_table, print_tree, print_columns, LoggerProgress

# 導入集成功能
from .integrations import has_uvicorn

if has_uvicorn():
    from .integrations.uvicorn import configure_uvicorn, InterceptHandler

# 嘗試導入 FastAPI 集成
try:
    from .integrations.fastapi import setup_fastapi_logging

    _has_fastapi = True
except ImportError:
    _has_fastapi = False

    
from .formats import has_figlet

# 如果 FIGlet 可用，則導入相關功能
if has_figlet():
    from .formats import (
        print_figlet_header,
        print_figlet_block,
        get_figlet_fonts
    )


# 定義對外可見的功能
__all__ = [
    # 日誌預設參數
    "PresetType", 
    "PresetFactory",
    # 類型和配置
    "EnhancedLogger",
    "LoggerConfig",
    # 核心功能
    "configure_logger",
    # 目標導向格式化工具
    "create_target_method",
    "add_target_methods",
    "ensure_target_parameters",
    # 工廠函數與管理
    "create_logger",
    "default_logger",
    "get_logger",
    "set_logger",
    "unregister_logger", 
    "list_loggers",
    "reinit_logger",
    # 格式化功能
    "print_block",
    "print_ascii_header",
    "print_ascii_block",
    "is_ascii_only",
    # Rich 組件
    "print_table",
    "print_tree",
    "print_columns",
    "LoggerProgress"
]

# 如果 Uvicorn 可用，添加相關功能
if has_uvicorn():
    __all__.extend(
        [
            "configure_uvicorn",
            "InterceptHandler"
        ]
    )

# 如果 FastAPI 可用，添加相關功能
if _has_fastapi:
    __all__.append("setup_fastapi_logging")

# 如果 FIGlet 可用，添加相關功能
if has_figlet():
    __all__.extend(
        [
            "print_figlet_header",
            "print_figlet_block",
            "get_figlet_fonts"
        ]
    )

# 嘗試導入 Advanced 模組（為進階用戶提供底層庫直接訪問）
try:
    from . import advanced
    _has_advanced = True
except ImportError:
    _has_advanced = False

# 如果 Advanced 模組可用，添加到導出列表
if _has_advanced:
    __all__.append("advanced")

# 版本信息
__version__ = "0.2.14"
