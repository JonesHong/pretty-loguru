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
    log_path_global,
    configure_logger
)

# 導入核心配置和功能
from .core.config import (
    LOG_LEVEL,
    LOG_ROTATION,
    LOG_PATH,
    LOG_NAME_FORMATS,
    LOGGER_FORMAT,
    OUTPUT_DESTINATIONS,
    LogLevelEnum,
    LoggerConfig
)

# 日誌預設參數
from .core.presets import (
    PresetType,
    LogPreset,
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
    list_loggers
)

# 導入格式化功能
from .formats.block import print_block
from .formats.ascii_art import print_ascii_header, print_ascii_block, is_ascii_only

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

# 檢查 pyfiglet 可用性 - 但不要讓導入失敗影響整個模組的加載
_has_figlet = False
try:
    # 嘗試導入 figlet 模組本身，而不是其中的函數
    from . import formats

    # 檢查 figlet 功能是否可用
    _has_figlet = formats.has_figlet()

    # 如果 figlet 可用，則導入相關功能
    if _has_figlet:
        from .formats.figlet import (
            print_figlet_header,
            print_figlet_block,
            get_figlet_fonts
        )
except ImportError as e:
    # 忽略導入錯誤，但將 _has_figlet 設為 False
    _has_figlet = False
    print(f"Warning: Failed to import figlet features: {str(e)}", file=sys.stderr)


# 定義對外可見的功能
__all__ = [
    # 日誌預設參數
    "PresetType",
    "LogPreset",
    "PresetFactory",
    # 類型和配置
    "EnhancedLogger",
    "LOG_LEVEL",
    "LOG_ROTATION",
    "LOG_PATH",
    "LOGGER_FORMAT",
    "LOG_NAME_FORMATS",
    "OUTPUT_DESTINATIONS",
    "LogLevelEnum",
    "LoggerConfig",
    # 核心功能
    "log_path_global",
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
    # 格式化功能
    "print_block",
    "print_ascii_header",
    "print_ascii_block",
    "is_ascii_only"
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
if _has_figlet:
    __all__.extend(
        [
            "print_figlet_header",
            "print_figlet_block",
            "get_figlet_fonts"
        ]
    )

# 版本信息
__version__ = "0.2.11"
