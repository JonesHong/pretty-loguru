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
    log_path_global
)
# 導入核心配置和功能
from .core.config import (
    LOG_LEVEL,
    LOG_ROTATION,
    LOG_PATH,
    LOG_NAME_FORMATS,
    OUTPUT_DESTINATIONS,
    LogLevelEnum,
    LoggerConfig,
)

# 導入工廠功能
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

# 提供向後兼容性的別名
# 將全局 logger 標記為擴展類型 (向後兼容)
logger = cast(EnhancedLogger, default_logger)

# 舊函數名的別名 (向後兼容)
def logger_start(
    file: Optional[str] = None, 
    folder: Optional[str] = None,
    **kwargs
) -> str:
    """
    初始化 logger 並開始記錄日誌。(向後兼容函數)
    
    此函數是 create_logger 的簡化版本，提供與舊版本相同的介面。
    新代碼應該直接使用 create_logger 函數。
    
    Args:
        file: 日誌文件的名稱，預設為 None
        folder: 日誌文件的資料夾，預設為 None
        **kwargs: 其他傳遞給 create_logger 的參數
        
    Returns:
        str: 日誌文件的完整路徑
    """
    if folder is not None and 'service_name' not in kwargs:
        kwargs['service_name'] = folder
    
    logger_instance = create_logger(
        file=file,
        start_cleaner=True,
        **kwargs
    )
    
    # 取得進程 ID 或服務名稱
    process_id = None
    if file is not None:
        import os
        process_id = os.path.splitext(os.path.basename(file))[0]
    elif 'service_name' in kwargs:
        process_id = kwargs['service_name']
    elif folder is not None:
        process_id = folder
    
    return process_id or "default"

# 提供 uvicorn_init_config 別名 (向後兼容)
if has_uvicorn():
    def uvicorn_init_config(**kwargs):
        """
        初始化 uvicorn 的配置。(向後兼容函數)
        
        Args:
            **kwargs: 傳遞給 configure_uvicorn 的參數
        """
        return configure_uvicorn(**kwargs)
else:
    def uvicorn_init_config(**kwargs):
        """
        初始化 uvicorn 的配置。(向後兼容函數)
        
        當 uvicorn 未安裝時，此函數將引發 ImportError。
        
        Raises:
            ImportError: 當 uvicorn 未安裝時
        """
        raise ImportError("未安裝 uvicorn 套件，此功能不可用。可使用 'pip install uvicorn' 安裝。")

# 定義對外可見的功能
__all__ = [
    # 類型和配置
    "EnhancedLogger",
    "LOG_LEVEL",
    "LOG_ROTATION",
    "LOG_PATH",
    "LOG_NAME_FORMATS",
    "OUTPUT_DESTINATIONS",
    "LogLevelEnum",
    "LoggerConfig",
    
    # 全局 logger (向後兼容)
    "logger", 
    
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
    
    # 初始化函數 (向後兼容)
    "logger_start",
    "log_path_global",  # 全域變數，用於儲存日誌路徑
]

# 如果 Uvicorn 可用，添加相關功能
if has_uvicorn():
    __all__.extend([
        "configure_uvicorn",
        "InterceptHandler",
        "uvicorn_init_config",  # 向後兼容
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
__version__ = "1.0.0"