"""
日誌系統基礎模組

此模組提供 Pretty Loguru 的基本功能，包括核心初始化、
日誌實例的配置和管理等基礎功能。
"""

import sys
import warnings
from pathlib import Path
from typing import Dict, Any, Optional, Union, Callable, cast

from loguru import logger as _logger
from rich.console import Console

from ..types import (
    EnhancedLogger, LogLevelType, LogPathType, LogNameFormatType, 
    LogRotationType, LogHandlerIdType, LogFilterType, LogConfigType
)
from .config import LOG_LEVEL, LOGGER_FORMAT
from .handlers import create_destination_filters, format_filename

log_path_global: Optional[Path] = None  # 全域變數，用於儲存日誌路徑
# Rich Console 實例，用於美化輸出
_console = Console()

def get_console() -> Console:
    """獲取 Rich Console 實例
    
    Returns:
        Console: Rich Console 實例，用於美化輸出
    """
    return _console


def configure_logger(
    level: LogLevelType = LOG_LEVEL,
    log_path: Optional[LogPathType] = None,
    process_id: str = "",
    rotation: LogRotationType = "20 MB",
    subdirectory: Optional[str] = None,
    log_name_format: LogNameFormatType = None,
    timestamp_format: Optional[str] = None,
    log_file_settings: Optional[LogConfigType] = None,
    logger_instance: Any = None,
    service_name: Optional[str] = None,
    isolate_handlers: bool = True,
    # unique_id: Optional[str] = None,
    logger_format: str = LOGGER_FORMAT,
) -> str:
    """
    配置日誌系統，確保每個 logger 實例的處理器完全隔離

    Args:
        level: 日誌級別，預設為全域變數 LOG_LEVEL。
        log_path: 日誌儲存路徑，若為 None 則使用預設路徑。
        process_id: 處理程序 ID，用於標記日誌檔案。
        rotation: 日誌輪換大小，單位為 MB。
        subdirectory: 子目錄名稱，用於分類不同類型的日誌。
        log_name_format: 日誌檔案名稱格式。
        timestamp_format: 時間戳格式，用於自定義時間顯示方式。
        log_file_settings: 日誌檔案的其他設定。
        logger_instance: 要初始化的日誌實例，如果為None則使用全局的_logger
        service_name: 服務名稱，用於在日誌檔案名中使用 {service_name} 變數
        isolate_handlers: 是否隔離不同 logger 實例的處理器，預設為 True
        # unique_id: 唯一ID，用於確保每個logger實例完全獨立
        logger_format: 日誌格式字符串，預設使用 LOGGER_FORMAT

    Returns:
        str: 日誌檔案的完整路徑
    """
    # 決定要使用的logger實例
    target_logger = _logger if logger_instance is None else logger_instance
    
    # 1. 決定最終要用的資料夾
    if log_path is None:
        base = Path.cwd() / "logs"  # 預設日誌資料夾
    else:
        base = Path(log_path)
    
    # 如果指定了子目錄，將其添加到基礎路徑中
    if subdirectory:
        base = base / subdirectory
    
    global log_path_global
    log_path_global = base  # 更新全域變數
    
    # 確保資料夾存在
    base.mkdir(parents=True, exist_ok=True)

    # 2. 移除所有現有的處理器 - 這是一種激進但有效的方法
    if isolate_handlers and hasattr(target_logger, "_core"):
        handler_ids = list(target_logger._core.handlers.keys())
        for handler_id in handler_ids:
            try:
                target_logger.remove(handler_id)
            except Exception as e:
                print(f"Warning: Failed to remove handler {handler_id}: {str(e)}")
    
    # 3. 設定附加資訊
    # 生成唯一的 logger_id，結合 process_id, service_name 和 unique_id
    # logger_id = f"{process_id}_{service_name}_{unique_id}" if unique_id else f"{process_id}_{service_name}"
    logger_id = f"{process_id}_{service_name}" 
    
    extra_config = {
        "folder": process_id,      # 額外資訊：處理程序 ID
        "logger_id": logger_id,    # 唯一的 logger 識別碼
        "to_console_only": False,  # 是否僅輸出到控制台
        "to_log_file_only": False, # 是否僅輸出到日誌檔案
    }
    
    # 如果提供了 service_name，將其添加到額外資訊中
    if service_name:
        extra_config["service_name"] = service_name
    
    # 更新 logger 的額外資訊
    target_logger.configure(extra=extra_config)

    # 4. 生成日誌檔案名
    log_filename = format_filename(process_id, log_name_format, timestamp_format, service_name)
    
    # 如果提供了唯一ID，將其添加到檔案名中以確保唯一性
    # if unique_id:
    #     base_name, ext = log_filename.rsplit(".", 1) if "." in log_filename else (log_filename, "log")
    #     log_filename = f"{base_name}_{unique_id}.{ext}"
    
    logfile = base / log_filename
    
    # 輸出調試信息
    print(f"Logger '{service_name or process_id}' (ID: {logger_id}): 設置日誌文件路徑為 {logfile}")
    
    # 5. 創建目標過濾器
    filters = create_destination_filters()
    
    # 處理輪換大小格式
    rotation_value = rotation
    if isinstance(rotation, (int, float)) or (isinstance(rotation, str) and rotation.isdigit()):
        # 如果是數字或純數字字符串，添加空格和單位
        rotation_value = f"{rotation} MB"
    elif isinstance(rotation, str):
        # 如果是字符串但不是純數字，檢查是否已經包含單位
        if any(unit in rotation.lower() for unit in ["kb", "mb", "gb", "b", "day", "month", "week", "hour", "minute", "second"]):
            rotation_value = rotation  # 已經有單位，保持不變
        else:
            # 嘗試轉換為數字，如果成功則添加 MB 單位
            try:
                float(rotation)
                rotation_value = f"{rotation} MB"  # 添加空格和單位
            except ValueError:
                rotation_value = rotation  # 不是數字，保持不變
    
    # 6. 準備日誌檔案設置
    file_settings = {
        "rotation": rotation_value,  # 設定日誌輪換大小，修正後的格式
        "encoding": "utf-8",         # 檔案編碼
        "enqueue": True,             # 使用多線程安全的方式寫入
        "filter": filters["file"],   # 文件過濾器
    }
    
    # 合併自定義設置
    if log_file_settings:
        file_settings.update(log_file_settings)
    
    # 7. 新增檔案 handler - 確保檔案處理器綁定到正確的文件
    file_handler_id = target_logger.add(
        str(logfile),
        format=logger_format,  # 使用定義的日誌格式
        level=level,           # 設定日誌級別
        **file_settings
    )
    
    # 8. 新增 console handler - 確保控制台處理器不會干擾其他實例
    console_handler_id = target_logger.add(
        sys.stderr,
        format=logger_format,     # 使用相同的日誌格式
        level=level,              # 設定日誌級別
        filter=filters["console"], # 控制台過濾器
    )
    
    # 保存處理器 ID，以便將來需要更新或移除
    if not hasattr(target_logger, "_handler_ids"):
        target_logger._handler_ids = {}
    target_logger._handler_ids["file"] = file_handler_id
    target_logger._handler_ids["console"] = console_handler_id
    
    # 返回完整的日誌文件路徑，方便外部使用
    return str(logfile)


# 新增目標導向日誌方法 - 只輸出到控制台
def _console_only(logger_instance: Any, level: str, message: str, *args: Any, **kwargs: Any) -> None:
    """
    僅在控制台顯示的日誌記錄方法
    
    Args:
        logger_instance: 日誌實例
        level: 日誌級別
        message: 日誌訊息
        *args: 其他位置參數
        **kwargs: 其他關鍵字參數
    """
    return logger_instance.opt(ansi=True, depth=2).bind(to_console_only=True).log(level, message, *args, **kwargs)


# 新增目標導向日誌方法 - 只輸出到文件
def _file_only(logger_instance: Any, level: str, message: str, *args: Any, **kwargs: Any) -> None:
    """
    僅寫入文件的日誌記錄方法
    
    Args:
        logger_instance: 日誌實例
        level: 日誌級別
        message: 日誌訊息
        *args: 其他位置參數
        **kwargs: 其他關鍵字參數
    """
    return logger_instance.bind(to_log_file_only=True).log(level, message, *args, **kwargs)


def add_custom_output_methods(logger_instance: Any) -> None:
    """
    為日誌實例添加自定義輸出方法
    
    Args:
        logger_instance: 要擴展的日誌實例
    """
    # 控制台專用方法
    logger_instance.console = lambda level, message, *args, **kwargs: _console_only(logger_instance, level, message, *args, **kwargs)
    logger_instance.console_debug = lambda message, *args, **kwargs: _console_only(logger_instance, "DEBUG", message, *args, **kwargs)
    logger_instance.console_info = lambda message, *args, **kwargs: _console_only(logger_instance, "INFO", message, *args, **kwargs)
    logger_instance.console_success = lambda message, *args, **kwargs: _console_only(logger_instance, "SUCCESS", message, *args, **kwargs)
    logger_instance.console_warning = lambda message, *args, **kwargs: _console_only(logger_instance, "WARNING", message, *args, **kwargs)
    logger_instance.console_error = lambda message, *args, **kwargs: _console_only(logger_instance, "ERROR", message, *args, **kwargs)
    logger_instance.console_critical = lambda message, *args, **kwargs: _console_only(logger_instance, "CRITICAL", message, *args, **kwargs)

    # 文件專用方法
    logger_instance.file = lambda level, message, *args, **kwargs: _file_only(logger_instance, level, message, *args, **kwargs)
    logger_instance.file_debug = lambda message, *args, **kwargs: _file_only(logger_instance, "DEBUG", message, *args, **kwargs)
    logger_instance.file_info = lambda message, *args, **kwargs: _file_only(logger_instance, "INFO", message, *args, **kwargs)
    logger_instance.file_success = lambda message, *args, **kwargs: _file_only(logger_instance, "SUCCESS", message, *args, **kwargs)
    logger_instance.file_warning = lambda message, *args, **kwargs: _file_only(logger_instance, "WARNING", message, *args, **kwargs)
    logger_instance.file_error = lambda message, *args, **kwargs: _file_only(logger_instance, "ERROR", message, *args, **kwargs)
    logger_instance.file_critical = lambda message, *args, **kwargs: _file_only(logger_instance, "CRITICAL", message, *args, **kwargs)

    # 開發模式方法 (別名為控制台方法)
    logger_instance.dev = logger_instance.console
    logger_instance.dev_debug = logger_instance.console_debug
    logger_instance.dev_info = logger_instance.console_info
    logger_instance.dev_success = logger_instance.console_success
    logger_instance.dev_warning = logger_instance.console_warning
    logger_instance.dev_error = logger_instance.console_error
    logger_instance.dev_critical = logger_instance.console_critical