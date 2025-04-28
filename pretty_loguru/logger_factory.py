"""
日誌工廠模組 - 提供日誌實例的創建與管理
"""

import inspect
import os
import warnings
from pathlib import Path
from typing import cast, Optional, Dict, Any, Union, Literal, List

from loguru import logger as _base_logger

from .logger_base import init_logger, _logger, LoggerClear, LOG_NAME_FORMATS
from .logger_block import print_block
from .logger_ascii import print_ascii_header, print_ascii_block, is_ascii_only
from .logger_types import EnhancedLogger

# 保存已創建的日誌實例
_logger_instances: Dict[str, EnhancedLogger] = {}

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
    reuse_existing: bool = True,
    start_cleaner: bool = False  # 新增參數控制是否啟動清理器
) -> EnhancedLogger:
    """
    創建新的 logger 實例或返回既有實例
    
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
        reuse_existing (bool): 是否重用同名的既有實例，預設為 True

    Returns:
        EnhancedLogger: 已配置的日誌實例

    用法:
        1. logger = create_logger() - 自動創建具有唯一名稱的日誌實例
        2. logger = create_logger(name="api") - 創建名為 "api" 的日誌實例或返回既有實例
        3. logger = create_logger(file=__file__) - 使用文件名作為 process_id
        4. logger = create_logger(service_name="auth_service") - 指定服務名稱
        5. logger = create_logger(name="api", reuse_existing=False) - 強制創建新實例
    """
    # 取得調用者資訊
    caller_frame = inspect.currentframe().f_back  # 獲取上一層調用的堆疊幀
    caller_file = caller_frame.f_code.co_filename  # 獲取調用文件的完整路徑
    
    # 確定 process_id 的值 (用於日誌文件名)
    process_id = None

    # 若提供 file 參數，使用該文件名作為 process_id
    if file is not None:
        process_id = os.path.splitext(os.path.basename(file))[0]
    # 若提供 service_name 參數，使用該服務名稱作為 process_id
    elif service_name is not None:
        process_id = service_name
    # 若都未提供，則從調用文件推斷
    else:
        file_name = os.path.splitext(os.path.basename(caller_file))[0]  # 獲取文件名（無副檔名）
        process_id = file_name

    # 若未提供 name 參數，使用 process_id 作為 name
    if name is None:
        name = process_id
    
    # 檢查是否已有同名實例
    if name in _logger_instances and reuse_existing:
        return _logger_instances[name]
    
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

    # 準備日誌初始化參數
    logger_config = {
        "process_id": process_id,
        "log_path": log_base_path,
        "subdirectory": subdirectory,
        "log_name_format": log_name_format,
        "timestamp_format": timestamp_format,
        "log_file_settings": log_file_settings,
        "service_name": service_name,  # 傳遞 service_name 參數
    }
    
    # 合併自定義配置
    if custom_config:
        logger_config.update(custom_config)
    
    # 建立 logger 實例 (從 _base_logger 複製)
    new_logger = _base_logger.bind(
        logger_name=name,
        folder=process_id,
        to_console_only=False,
        to_log_file_only=False
    )
    
    # 初始化新的 logger 實例
    log_file_path = init_logger(
        logger_instance=new_logger, 
        **logger_config
    )
    
    # 加入自定義方法到新的 logger 實例
    _add_custom_methods(new_logger)
    
    # 只有在被明確要求時才啟動日誌清理器，而且只啟動一次
    global _cleaner_started
    if start_cleaner and not _cleaner_started:
        logger_cleaner = LoggerClear(logger_instance=new_logger)  # 傳遞 logger 實例
        logger_cleaner.start()
        _cleaner_started = True
    
    # 將新實例保存到字典中
    _logger_instances[name] = cast(EnhancedLogger, new_logger)
    
    return cast(EnhancedLogger, new_logger)

def _add_custom_methods(logger_instance):
    """
    將自定義方法添加到 logger 實例
    
    Args:
        logger_instance: 要擴展的 logger 實例
    """
    # 將 block, ascii_header, ascii_block 等方法添加到實例
    logger_instance.block = lambda *args, **kwargs: print_block(*args, **kwargs)
    logger_instance.ascii_header = lambda *args, **kwargs: print_ascii_header(*args, **kwargs)
    logger_instance.ascii_block = lambda *args, **kwargs: print_ascii_block(*args, **kwargs)
    logger_instance.is_ascii_only = lambda *args, **kwargs: is_ascii_only(*args, **kwargs)
    
    # 以下為目標特定方法,需要綁定當前實例 (此處需修改 print_block 等函數來接收 logger 實例)
    
    # 控制台專用方法
    def _console_only(level, message, *args, **kwargs):
        return logger_instance.bind(to_console_only=True).log(level, message, *args, **kwargs)
    
    # 文件專用方法    
    def _file_only(level, message, *args, **kwargs):
        return logger_instance.bind(to_log_file_only=True).log(level, message, *args, **kwargs)
    
    # 控制台專用的各級別日誌方法
    def _console_debug(message, *args, **kwargs):
        return _console_only("DEBUG", message, *args, **kwargs)

    def _console_info(message, *args, **kwargs):
        return _console_only("INFO", message, *args, **kwargs)

    def _console_success(message, *args, **kwargs):
        return _console_only("SUCCESS", message, *args, **kwargs)

    def _console_warning(message, *args, **kwargs):
        return _console_only("WARNING", message, *args, **kwargs)

    def _console_error(message, *args, **kwargs):
        return _console_only("ERROR", message, *args, **kwargs)

    def _console_critical(message, *args, **kwargs):
        return _console_only("CRITICAL", message, *args, **kwargs)
    
    # 文件專用的各級別日誌方法
    def _file_debug(message, *args, **kwargs):
        return _file_only("DEBUG", message, *args, **kwargs)

    def _file_info(message, *args, **kwargs):
        return _file_only("INFO", message, *args, **kwargs)

    def _file_success(message, *args, **kwargs):
        return _file_only("SUCCESS", message, *args, **kwargs)

    def _file_warning(message, *args, **kwargs):
        return _file_only("WARNING", message, *args, **kwargs)

    def _file_error(message, *args, **kwargs):
        return _file_only("ERROR", message, *args, **kwargs)

    def _file_critical(message, *args, **kwargs):
        return _file_only("CRITICAL", message, *args, **kwargs)
    
    # 開發模式方法 (同控制台方法)
    def _dev_debug(message, *args, **kwargs):
        return _console_debug(message, *args, **kwargs)

    def _dev_info(message, *args, **kwargs):
        return _console_info(message, *args, **kwargs)

    def _dev_success(message, *args, **kwargs):
        return _console_success(message, *args, **kwargs)

    def _dev_warning(message, *args, **kwargs):
        return _console_warning(message, *args, **kwargs)

    def _dev_error(message, *args, **kwargs):
        return _console_error(message, *args, **kwargs)

    def _dev_critical(message, *args, **kwargs):
        return _console_critical(message, *args, **kwargs)
    
    # 添加到 logger 實例
    logger_instance.console = _console_only
    logger_instance.console_debug = _console_debug
    logger_instance.console_info = _console_info
    logger_instance.console_success = _console_success
    logger_instance.console_warning = _console_warning
    logger_instance.console_error = _console_error
    logger_instance.console_critical = _console_critical

    logger_instance.file = _file_only
    logger_instance.file_debug = _file_debug
    logger_instance.file_info = _file_info
    logger_instance.file_success = _file_success
    logger_instance.file_warning = _file_warning
    logger_instance.file_error = _file_error
    logger_instance.file_critical = _file_critical

    logger_instance.dev = _console_only
    logger_instance.dev_debug = _dev_debug
    logger_instance.dev_info = _dev_info
    logger_instance.dev_success = _dev_success
    logger_instance.dev_warning = _dev_warning
    logger_instance.dev_error = _dev_error
    logger_instance.dev_critical = _dev_critical


# 添加全局標記
_cleaner_started = False

# 默認 logger 實例 (與原程式碼兼容)
default_logger = create_logger(name="default", start_cleaner=True)