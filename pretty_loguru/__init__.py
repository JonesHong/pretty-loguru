"""
日誌系統包入口
"""
from typing import cast, Optional, Dict, Any, Union, Literal, List
from pathlib import Path

# 導入類型標註
from .logger_types import EnhancedLogger

# 導入基礎日誌組件
from .logger_base import _logger, log_path

# 導入區塊日誌功能
from .logger_block import print_block 

# 導入 ASCII 藝術日誌功能
from .logger_ascii import print_ascii_header, print_ascii_block, is_ascii_only

# 導入初始化相關功能
from .logger_init import logger_start, uvicorn_init_config, InterceptHandler

# 導入新的日誌工廠功能
from .logger_factory import create_logger, default_logger

# 將全局 logger 標記為擴展類型 (向後兼容)
logger = cast(EnhancedLogger, _logger)

# 定義對外可見的功能
__all__ = [
    # 全局 logger (向後兼容)
    "logger", 
    
    # 工廠函數與默認實例
    "create_logger",
    "default_logger",
    
    # 功能函數
    "print_block", 
    "print_ascii_header", 
    "print_ascii_block",
    "is_ascii_only",
    
    # 初始化函數 (向後兼容)
    "logger_start",
    "uvicorn_init_config",
    
    # 其他變數
    "log_path"
]