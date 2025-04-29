"""
Pretty Loguru 日誌系統包入口

此模組提供了增強型的 Loguru 日誌系統，包含區塊式日誌、ASCII 藝術標題
以及與各種框架的集成功能，使日誌記錄變得更加直觀和美觀。
"""
from typing import cast, Optional, Dict, Any, Union, Literal, List, Set
from pathlib import Path

# 導入類型標註
from .types import EnhancedLogger

from .core.base import (
    log_path_global,
    configure_logger,
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
    LoggerConfig,
)

# 導入工廠功能 - 注意這裡使用新的 default_logger 函數
from .factory.creator import (
    create_logger,
    default_logger,
    get_logger,
    set_logger,
    unregister_logger,
    list_loggers,
)

# 導入格式化功能
from .formats.block import print_block
from .formats.ascii_art import print_ascii_header, print_ascii_block, is_ascii_only

# 嘗試導入 FIGlet 功能 (可選)
try:
    from .formats.figlet import print_figlet_header, print_figlet_block, get_figlet_fonts
    _has_figlet = True
except ImportError:
    _has_figlet = False

# 導入集成功能
from .integrations import has_uvicorn
if has_uvicorn():
    from .integrations.uvicorn import configure_uvicorn, InterceptHandler
try:
    from .integrations.fastapi import setup_fastapi_logging
    _has_fastapi = True
except ImportError:
    _has_fastapi = False


# 定義對外可見的功能
__all__ = [
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
    "is_ascii_only",
    
]

# 如果 Uvicorn 可用，添加相關功能
if has_uvicorn():
    __all__.extend([
        "configure_uvicorn",
        "InterceptHandler",
    ])

# 如果 FastAPI 可用，添加相關功能
if _has_fastapi:
    __all__.append("setup_fastapi_logging")

# 如果 FIGlet 可用，添加相關功能
if _has_figlet:
    __all__.extend([
        "print_figlet_header",
        "print_figlet_block",
        "get_figlet_fonts",
    ])

# 版本信息
__version__ = "0.2.2"