"""
Logger 創建模組 - 改進版

此模組提供創建和管理 Logger 實例的功能，
實現了單例模式、工廠模式和延遲初始化，確保 Logger 實例的有效隔離和管理。
"""

import inspect
import os
import warnings
import uuid
from pathlib import Path
from typing import Dict, Optional, Union, Literal, List, Any, cast

from loguru import logger as _base_logger
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from rich.console import Console

from ..types import (
    EnhancedLogger, LogLevelType, LogPathType, LogNameFormatType, 
    LogRotationType, LogConfigType
)
from ..core.config import LOG_NAME_FORMATS
from ..core.base import configure_logger, get_console
from ..core.cleaner import LoggerCleaner
from .methods import add_custom_methods

# 全局 logger 實例註冊表
# 用於保存、查找和管理已創建的 logger 實例
_logger_registry: Dict[str, EnhancedLogger] = {}

# 保存 logger 實例的文件路徑
_logger_file_paths: Dict[str, str] = {}

# 保存是否已啟動清理器的標誌
_cleaner_started = False

# 默認 console 實例，用於共享視覺輸出
_console = get_console()

# 保存延遲初始化的 default_logger
_default_logger_instance = None


def create_logger(
    name: Optional[str] = None,
    service_tag: Optional[str] = None,
    subdirectory: Optional[str] = None, 
    log_name_format: LogNameFormatType = None,
    log_name_preset: Optional[Literal["default", "daily", "hourly", "minute", "simple", "detailed"]] = None,
    timestamp_format: Optional[str] = None,
    log_path: Optional[LogPathType] = None,
    log_file_settings: Optional[LogConfigType] = None,
    custom_config: Optional[LogConfigType] = None,
    reuse_existing: bool = False,
    start_cleaner: bool = False,
    force_new_instance: bool = True,
    console: Optional[Console] = None,
    level: LogLevelType = "INFO",
    rotation: LogRotationType = "20 MB",
) -> EnhancedLogger:
    """
    創建有效隔離的 logger 實例
    
    Args:
        name: logger 實例的名稱，如果不提供則自動生成
        service_tag: 服務或模組名稱，用於標識日誌來源
        subdirectory: 日誌子目錄，用於分類不同模組或功能的日誌
        log_name_format: 日誌檔案名稱格式，可包含變數如 {component_name}, {timestamp}, {date}, {time} 等
        log_name_preset: 預設的日誌檔案名格式，可選值為 "default", "daily", "hourly" 等
        timestamp_format: 時間戳格式，用於自定義時間顯示方式
        log_path: 日誌基礎路徑，覆蓋預設的 log_path
        log_file_settings: 日誌檔案的其他設定，如壓縮、保留時間等
        custom_config: 自定義日誌配置，可包含任意 configure_logger 支援的參數
        reuse_existing: 是否重用同名的既有實例，預設為 False
        start_cleaner: 是否啟動日誌清理器，預設為 False
        force_new_instance: 是否強制創建新實例，預設為 True
        console: 要使用的 Rich Console 實例，預設為全局共享的實例
        level: 日誌級別，預設為 INFO
        rotation: 日誌輪換設置，預設為 20 MB

    Returns:
        EnhancedLogger: 已配置的日誌實例
        
    Examples:
        >>> # 創建基本 logger
        >>> logger = create_logger("my_app")
        >>> 
        >>> # 創建帶有子目錄的 logger
        >>> logger = create_logger("api", subdirectory="api_logs")
        >>> 
        >>> # 使用預設文件名格式
        >>> logger = create_logger("db", log_name_preset="daily")
        >>> 
        >>> # 自定義日誌文件配置
        >>> logger = create_logger(
        ...     "worker", 
        ...     service_tag="background_tasks",
        ...     log_file_settings={"compression": "zip", "retention": "1 week"}
        ... )
    """
    global _cleaner_started
    
    # 取得調用者資訊，用於自動生成名稱
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename if caller_frame else "unknown"
    
    # 確定 component_name 的值 (用於日誌文件名)
    if service_tag is not None:
        component_name = service_tag
    else:
        file_name = os.path.splitext(os.path.basename(caller_file))[0]
        component_name = file_name

    # 若未提供 name 參數，使用 component_name 作為 name
    if name is None:
        name = component_name
    
    # 創建唯一的 logger 標識
    logger_id = f"{name}_{service_tag}"
    
    # 如果想重用實例且不是強制創建新的
    if reuse_existing and not force_new_instance:
        if name in _logger_registry:
            return _logger_registry[name]
        
        # 查找已存在的實例 (基於名稱和服務名稱但不包括唯一ID部分)
        base_id = f"{name}_{service_tag}"
        for existing_id, logger_instance in _logger_registry.items():
            if existing_id.startswith(base_id):
                return logger_instance
    
    # 處理預設日誌名稱格式
    if log_name_preset and not log_name_format:
        if log_name_preset in LOG_NAME_FORMATS:
            log_name_format = LOG_NAME_FORMATS[log_name_preset]
        else:
            warnings.warn(
                f"Unknown log_name_preset '{log_name_preset}'. Using 'default' instead.",
                UserWarning,
                stacklevel=2
            )
            log_name_format = LOG_NAME_FORMATS["default"]
    
    # 創建新的 logger 實例
    new_logger = _Logger(
        core=_Core(),
        exception=None,
        depth=0,
        record=False,
        lazy=False,
        colors=False,
        raw=False,
        capture=True,
        patchers=[],
        extra={},
    ).patch(lambda record: record.update(
        logger_name=name,
        logger_id=logger_id,
        folder=component_name,
        service_tag=service_tag
    ))
    
    # 使用相同的 console 實例
    if console is None:
        console = _console
    
    # 準備日誌初始化參數
    logger_config = {
        "level": level,
        "component_name": component_name,
        "rotation": rotation,
        "log_path": log_path,
        "subdirectory": subdirectory,
        "log_name_format": log_name_format,
        "timestamp_format": timestamp_format,
        "log_file_settings": log_file_settings,
        "service_tag": service_tag,
        "isolate_handlers": True,
    }
    
    # 合併自定義配置
    if custom_config:
        logger_config.update(custom_config)
    
    # 配置 logger 實例
    log_file_path = configure_logger(
        logger_instance=new_logger, 
        **logger_config
    )
    
    # 保存文件路徑
    _logger_file_paths[logger_id] = log_file_path
    
    # 加入自定義方法到新的 logger 實例
    add_custom_methods(new_logger, console)
    
    # 只有在被明確要求時才啟動日誌清理器，而且只啟動一次
    if start_cleaner and not _cleaner_started:
        logger_cleaner = LoggerCleaner(
            logger_instance=new_logger,
            log_path=log_path
        )
        logger_cleaner.start()
        _cleaner_started = True
    
    # 將新實例註冊到全局註冊表
    _logger_registry[name] = cast(EnhancedLogger, new_logger)
    
    # 記錄創建信息
    new_logger.debug(f"Logger instance '{name}' (ID: {logger_id}) has been created, log file: {log_file_path}")
    
    return cast(EnhancedLogger, new_logger)


def get_logger(name: str) -> Optional[EnhancedLogger]:
    """
    根據名稱獲取已註冊的 logger 實例
    
    Args:
        name: logger 實例的名稱
        
    Returns:
        Optional[EnhancedLogger]: 如果找到則返回 logger 實例，否則返回 None
    """
    return _logger_registry.get(name)


def set_logger(name: str, logger_instance: EnhancedLogger) -> None:
    """
    手動註冊 logger 實例
    
    Args:
        name: logger 實例的名稱
        logger_instance: 要註冊的 logger 實例
    """
    _logger_registry[name] = logger_instance


def unregister_logger(name: str) -> bool:
    """
    取消註冊 logger 實例
    
    Args:
        name: 要取消註冊的 logger 實例名稱
        
    Returns:
        bool: 如果成功取消註冊則返回 True，否則返回 False
    """
    if name in _logger_registry:
        del _logger_registry[name]
        return True
    return False


def list_loggers() -> List[str]:
    """
    列出所有已註冊的 logger 名稱
    
    Returns:
        List[str]: 註冊的 logger 名稱列表
    """
    return list(_logger_registry.keys())


def default_logger() -> EnhancedLogger:
    """
    獲取默認的 logger 實例（延遲初始化）
    
    只有在首次呼叫這個函數時，才會創建默認的 logger 實例，
    避免在導入模組時就立即創建日誌文件。
    
    Returns:
        EnhancedLogger: 默認的 logger 實例
    """
    global _default_logger_instance
    if _default_logger_instance is None:
        _default_logger_instance = create_logger(
            name="default", 
            service_tag="default_service",
            start_cleaner=False, 
            force_new_instance=False
        )
    return _default_logger_instance