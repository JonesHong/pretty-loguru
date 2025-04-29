"""
類型存根文件 (.pyi)，提供精確的類型標註
IDE 會優先參考這個文件進行類型檢查和自動完成提示
"""
from typing import Any, Callable, Dict, List, Optional, Set, Union, overload, TypeVar
from pathlib import Path
import logging

from loguru import logger as _logger

# 導入重構後的類型定義
from .types import (
    EnhancedLogger,
    LogLevelType,
    LogPathType,
    LogNameFormatType,
    LogRotationType,
    LogConfigType,
)

# 基本類型別名 (向後兼容)
T = TypeVar('T', bound='EnhancedLogger')

# 重構後的全局 logger 實例
logger: EnhancedLogger

# 核心配置常數
LOG_LEVEL: LogLevelType
LOG_ROTATION: LogRotationType
LOG_PATH: Path
LOG_NAME_FORMATS: Dict[str, str]
OUTPUT_DESTINATIONS: Dict[str, str]

class LogLevelEnum:
    """日誌級別枚舉類別"""
    TRACE: str
    DEBUG: str
    INFO: str
    SUCCESS: str
    WARNING: str
    ERROR: str
    CRITICAL: str

# 工廠函數與管理
def create_logger(
    name: Optional[str] = None,
    file: Optional[str] = None, 
    service_name: Optional[str] = None,
    subdirectory: Optional[str] = None, 
    log_name_format: Optional[str] = None,
    log_name_preset: Optional[str] = None,
    timestamp_format: Optional[str] = None,
    log_base_path: Optional[Union[str, Path]] = None,
    log_file_settings: Optional[Dict[str, Any]] = None,
    custom_config: Optional[Dict[str, Any]] = None,
    reuse_existing: bool = False,
    start_cleaner: bool = False,
    force_new_instance: bool = True,
    level: LogLevelType = "INFO",
    rotation: LogRotationType = "20 MB",
) -> EnhancedLogger: ...

def default_logger() -> EnhancedLogger: ...
def get_logger(name: str) -> Optional[EnhancedLogger]: ...
def set_logger(name: str, logger_instance: EnhancedLogger) -> None: ...
def unregister_logger(name: str) -> bool: ...
def list_loggers() -> List[str]: ...

# 格式化功能
def print_block(
    title: str,
    message_list: List[str],
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
) -> None: ...

def print_ascii_header(
    text: str,
    font: str = "standard",
    log_level: str = "INFO",
    border_style: str = "cyan",
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    logger_instance: Any = None,
) -> None: ...

def print_ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = None,
    ascii_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
) -> None: ...

def is_ascii_only(text: str) -> bool: ...

# FIGlet 功能 (可選)
def print_figlet_header(
    text: str,
    font: str = "standard",
    log_level: str = "INFO",
    border_style: str = "cyan",
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    logger_instance: Any = None,
) -> None: ...

def print_figlet_block(
    title: str,
    message_list: List[str],
    figlet_header: Optional[str] = None,
    figlet_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO",
    logger_instance: Any = None,
) -> None: ...

def get_figlet_fonts() -> Set[str]: ...

# 向後兼容函數
def logger_start(
    file: Optional[str] = None, 
    folder: Optional[str] = None,
    **kwargs: Any
) -> str: ...

# Uvicorn 集成 (可選)
class InterceptHandler(logging.Handler):
    def __init__(self, logger_instance: Optional[Any] = None) -> None: ...
    def emit(self, record: logging.LogRecord) -> None: ...

def configure_uvicorn(
    logger_instance: Optional[Any] = None,
    level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None
) -> None: ...

def uvicorn_init_config(
    logger_instance: Optional[Any] = None,
    level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None
) -> None: ...

# FastAPI 集成 (可選)
def setup_fastapi_logging(
    app: Any,
    logger_instance: Optional[EnhancedLogger] = None,
    middleware: bool = True,
    custom_routes: bool = False,
    exclude_paths: Optional[List[str]] = None,
    exclude_methods: Optional[List[str]] = None,
    log_request_body: bool = False,
    log_response_body: bool = False,
) -> None: ...

# 配置類
class LoggerConfig:
    level: LogLevelType
    rotation: LogRotationType
    log_path: Path
    format: str
    
    def __init__(
        self,
        level: Optional[LogLevelType] = None,
        rotation: Optional[LogRotationType] = None,
        log_path: Optional[LogPathType] = None,
        logger_format: Optional[str] = None,
        env_prefix: str = "PRETTY_LOGURU_"
    ) -> None: ...
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'LoggerConfig': ...
    
    @classmethod
    def from_file(cls, file_path: Union[str, Path], format: str = "json") -> 'LoggerConfig': ...
    
    def to_dict(self) -> Dict[str, Any]: ...
    
    def save_to_file(self, file_path: Union[str, Path], format: str = "json") -> None: ...

# 版本信息
__version__: str