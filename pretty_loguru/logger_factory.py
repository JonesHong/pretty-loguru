"""
修訂後的日誌工廠模組 - 提供有效隔離的日誌實例創建與管理
"""

import inspect
import os
import warnings
import sys
import uuid
import threading
from pathlib import Path
from typing import cast, Optional, Dict, Any, Union, Literal, List

from loguru import logger as _base_logger

from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger


from .logger_base import init_logger, _logger, LoggerClear, LOG_NAME_FORMATS
from .logger_block import print_block
from .logger_ascii import print_ascii_header, print_ascii_block, is_ascii_only
from .logger_types import EnhancedLogger

# 保存已創建的日誌實例和它們對應的文件路徑
_logger_instances: Dict[str, EnhancedLogger] = {}
_logger_file_paths: Dict[str, str] = {}
_logger_handler_ids: Dict[str, Dict[str, int]] = {}
_cleaner_started = False

def create_logger(
    name: Optional[str] = None,
    file: Optional[str] = None, 
    service_name: Optional[str] = None,
    subdirectory: Optional[str] = None, 
    log_name_format: Optional[str] = None,
    log_name_preset: Optional[Literal["default", "daily", "hourly", "minute", "simple", "detailed"]] = None,
    timestamp_format: Optional[str] = None,
    log_base_path: Optional[Union[str, Path]] = None,
    log_file_settings: Optional[Dict[str, Any]] = None,
    custom_config: Optional[Dict[str, Any]] = None,
    reuse_existing: bool = False,  # 默認不重用，確保獨立性
    start_cleaner: bool = False,
    force_new_instance: bool = True  # 默認總是強制創建新實例
) -> EnhancedLogger:
    """
    創建有效隔離的 logger 實例
    
    Args:
        name (str, optional): logger 實例的名稱，如果不提供則自動生成
        file (str, optional): 指定的文件路徑，若提供則使用該文件名作為 process_id
        service_name (str, optional): 服務或模組名稱，用於標識日誌來源
        subdirectory (str, optional): 日誌子目錄，用於分類不同模組或功能的日誌
        log_name_format (str, optional): 日誌檔案名稱格式，可包含變數如 {process_id}, {timestamp}, {date}, {time} 等
        log_name_preset (str, optional): 預設的日誌檔案名格式，可選值為 "default", "daily", "hourly" 等
        timestamp_format (str, optional): 時間戳格式，用於自定義時間顯示方式
        log_base_path (Union[str, Path], optional): 日誌基礎路徑，覆蓋預設的 log_path
        log_file_settings (Dict[str, Any], optional): 日誌檔案的其他設定，如壓縮、保留時間等
        custom_config (Dict[str, Any], optional): 自定義日誌配置，可包含任意 init_logger 支援的參數
        reuse_existing (bool): 是否重用同名的既有實例，預設為 False
        start_cleaner (bool): 是否啟動日誌清理器，預設為 False
        force_new_instance (bool): 是否強制創建新實例，預設為 True

    Returns:
        EnhancedLogger: 已配置的日誌實例
    """
    # 取得調用者資訊
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename if caller_frame else "unknown"
    
    # 確定 process_id 的值 (用於日誌文件名)
    if file is not None:
        process_id = os.path.splitext(os.path.basename(file))[0]
    elif service_name is not None:
        process_id = service_name
    else:
        file_name = os.path.splitext(os.path.basename(caller_file))[0]
        process_id = file_name

    # 若未提供 name 參數，使用 process_id 作為 name
    if name is None:
        name = process_id
    
    # 創建唯一的 logger 標識 - 結合 name 和 service_name，並添加唯一ID
    # 這確保每次調用都創建新的 logger 實例，即使在同一函數內
    unique_id = str(uuid.uuid4())[:8]
    logger_id = f"{name}_{service_name or process_id}_{unique_id}"
    
    # 如果想重用實例且不是強制創建新的
    if reuse_existing and not force_new_instance:
        # 查找已存在的實例 (基於名稱和服務名稱但不包括唯一ID部分)
        base_id = f"{name}_{service_name or process_id}"
        for existing_id in _logger_instances:
            if existing_id.startswith(base_id):
                return _logger_instances[existing_id]
    
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

    # 創建新的 logger 實例 - 使用 bind() 方法
    
    # 先透過 patch 創建獨立的 logger
    
    new_logger  = _Logger(
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
        folder=process_id,
        service_name=service_name or process_id
    ))
    # new_logger = _base_logger.patch(lambda record: record.update(
    #     logger_name=name,
    #     logger_id=logger_id,
    #     folder=process_id,
    #     service_name=service_name or process_id
    # ))

    # 移除目前所有 handlers
    # new_logger.remove()

    # 準備日誌初始化參數
    logger_config = {
        "process_id": process_id,
        "log_path": log_base_path,
        "subdirectory": subdirectory,
        "log_name_format": log_name_format,
        "timestamp_format": timestamp_format,
        "log_file_settings": log_file_settings,
        "service_name": service_name,
        "isolate_handlers": True,  # 始終隔離處理器
        "unique_id": unique_id    # 傳遞唯一 ID 到初始化函數
    }
    
    # 明確為此 logger 添加新的 handler
    log_file_path = init_logger(
        logger_instance=new_logger, 
        **logger_config
    )
    
    # 合併自定義配置
    if custom_config:
        logger_config.update(custom_config)
    
    # 初始化新的 logger 實例
    log_file_path = init_logger(
        logger_instance=new_logger, 
        **logger_config
    )
    
    # 保存文件路徑
    _logger_file_paths[logger_id] = log_file_path
    
    # 保存處理器 ID
    if hasattr(new_logger, "_handler_ids"):
        _logger_handler_ids[logger_id] = new_logger._handler_ids
    
    # 加入自定義方法到新的 logger 實例
    _add_custom_methods(new_logger)
    
    # 只有在被明確要求時才啟動日誌清理器，而且只啟動一次
    global _cleaner_started
    if start_cleaner and not _cleaner_started:
        logger_cleaner = LoggerClear(logger_instance=new_logger)
        logger_cleaner.start()
        _cleaner_started = True
    
    # 將新實例保存到字典中
    _logger_instances[logger_id] = cast(EnhancedLogger, new_logger)
    
    # 記錄創建信息
    new_logger.debug(f"Logger 實例 '{name}' (ID: {logger_id}) 已創建，日誌文件: {log_file_path}")
    
    return cast(EnhancedLogger, new_logger)

def _add_custom_methods(logger_instance):
    """
    將自定義方法添加到 logger 實例
    
    Args:
        logger_instance: 要擴展的 logger 實例
    """
    # 為自定義方法創建封閉作用域以避免相互干擾
    def create_method_wrapper(method, instance):
        def wrapper(*args, **kwargs):
            # 傳遞 logger_instance 作為參數
            return method(*args, **kwargs, logger_instance=instance)
        return wrapper
    
    # 將 block, ascii_header, ascii_block 等方法添加到實例，並傳入當前實例
    logger_instance.block = create_method_wrapper(print_block, logger_instance)
    logger_instance.ascii_header = create_method_wrapper(print_ascii_header, logger_instance)
    logger_instance.ascii_block = create_method_wrapper(print_ascii_block, logger_instance)
    logger_instance.is_ascii_only = is_ascii_only  # 這是靜態函數，不需要綁定
    
    # 控制台專用方法
    def _console_only(level, message, *args, **kwargs):
        return logger_instance.bind(to_console_only=True).log(level, message, *args, **kwargs)
    
    # 文件專用方法    
    def _file_only(level, message, *args, **kwargs):
        return logger_instance.bind(to_log_file_only=True).log(level, message, *args, **kwargs)
    
    # 添加所有級別的控制台方法
    logger_instance.console = _console_only
    logger_instance.console_debug = lambda msg, *args, **kwargs: _console_only("DEBUG", msg, *args, **kwargs)
    logger_instance.console_info = lambda msg, *args, **kwargs: _console_only("INFO", msg, *args, **kwargs)
    logger_instance.console_success = lambda msg, *args, **kwargs: _console_only("SUCCESS", msg, *args, **kwargs)
    logger_instance.console_warning = lambda msg, *args, **kwargs: _console_only("WARNING", msg, *args, **kwargs)
    logger_instance.console_error = lambda msg, *args, **kwargs: _console_only("ERROR", msg, *args, **kwargs)
    logger_instance.console_critical = lambda msg, *args, **kwargs: _console_only("CRITICAL", msg, *args, **kwargs)

    # 添加所有級別的文件方法
    logger_instance.file = _file_only
    logger_instance.file_debug = lambda msg, *args, **kwargs: _file_only("DEBUG", msg, *args, **kwargs)
    logger_instance.file_info = lambda msg, *args, **kwargs: _file_only("INFO", msg, *args, **kwargs)
    logger_instance.file_success = lambda msg, *args, **kwargs: _file_only("SUCCESS", msg, *args, **kwargs)
    logger_instance.file_warning = lambda msg, *args, **kwargs: _file_only("WARNING", msg, *args, **kwargs)
    logger_instance.file_error = lambda msg, *args, **kwargs: _file_only("ERROR", msg, *args, **kwargs)
    logger_instance.file_critical = lambda msg, *args, **kwargs: _file_only("CRITICAL", msg, *args, **kwargs)

    # 添加開發模式方法
    logger_instance.dev = _console_only
    logger_instance.dev_debug = logger_instance.console_debug
    logger_instance.dev_info = logger_instance.console_info
    logger_instance.dev_success = logger_instance.console_success
    logger_instance.dev_warning = logger_instance.console_warning
    logger_instance.dev_error = logger_instance.console_error
    logger_instance.dev_critical = logger_instance.console_critical


# 默認 logger 實例
default_logger = create_logger(name="default", start_cleaner=True)