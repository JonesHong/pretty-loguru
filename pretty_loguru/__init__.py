"""
日誌系統包入口
"""
from typing import cast

# 導入類型標註 (使用簡化版)
from .logger_types import EnhancedLogger

# 導入基礎日誌組件
from .logger_base import _logger, log_path

# 導入區塊日誌功能
from .logger_block import print_block 

# 導入 ASCII 藝術日誌功能
from .logger_ascii import print_ascii_header, print_ascii_block, is_ascii_only

# 導入初始化相關功能
from .logger_init import logger_start, uvicorn_init_config, InterceptHandler

# 將 _logger 標記為擴展類型
logger = cast(EnhancedLogger, _logger)

# 定義對外可見的功能
__all__ = [
    "logger", 
    "print_block", 
    "print_ascii_header", 
    "print_ascii_block",
    "is_ascii_only",
    "logger_start",
    "uvicorn_init_config",
    "log_path"
]