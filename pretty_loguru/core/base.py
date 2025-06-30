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

from ..types import EnhancedLogger
from .config import LoggerConfig, NATIVE_LOGGER_FORMAT
from .handlers import create_destination_filters, format_filename

# Rich Console 實例，用於美化輸出
_console = Console()

def get_console() -> Console:
    """獲取 Rich Console 實例"""
    return _console

def configure_logger(logger_instance: EnhancedLogger, config: LoggerConfig) -> None:
    """
    根據 LoggerConfig 配置日誌實例。
    """
    # 1. 移除所有現有的處理器以確保隔離
    if hasattr(logger_instance, "_core"):
        handler_ids = list(logger_instance._core.handlers.keys())
        for handler_id in handler_ids:
            try:
                logger_instance.remove(handler_id)
            except Exception as e:
                warnings.warn(f"Failed to remove handler {handler_id}: {e}")

    # 2. 根據 use_native_format 決定格式和 extra 配置
    if config.use_native_format:
        # 使用原生格式時，minimal extra 配置，不影響 loguru 的 file.name
        extra_config = {
            "to_console_only": False,
            "to_log_file_only": False,
        }
        actual_format = NATIVE_LOGGER_FORMAT
    else:
        # 使用自定義格式時，保持原有行為
        extra_config = {
            "folder": config.component_name or config.name,
            "logger_id": config.name,
            "to_console_only": False,
            "to_log_file_only": False,
        }
        actual_format = config.logger_format
    
    logger_instance.configure(extra=extra_config)

    # 3. 創建目標過濾器
    filters = create_destination_filters()

    # 4. 新增 console handler
    logger_instance.add(
        sys.stderr,
        format=actual_format,
        level=config.level,
        filter=filters["console"],
    )

    # 5. 如果需要，新增 file handler
    if config.log_path:
        log_path = Path(config.log_path)
        if config.subdirectory:
            log_path = log_path / config.subdirectory
        
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 決定檔案名稱
        if config.use_native_format:
            # 使用原生格式時，檔案名使用 logger 名稱，不使用自定義格式
            log_filename = f"{config.name}.log"
        else:
            # 使用自定義格式時，保持原有行為
            from ..core.presets import get_preset_config
            preset_conf = get_preset_config(config.preset) if config.preset else {}
            log_name_format = preset_conf.get('name_format')
            log_filename = format_filename(config.component_name or config.name, log_name_format)
        logfile = log_path / log_filename

        # 處理自定義壓縮格式
        compression_function = config.compression
        if config.compression_format and compression_function:
            # 如果有自定義格式且有壓縮函數，創建包含自定義格式的新函數
            from ..core.presets import create_custom_compression_function
            compression_function = create_custom_compression_function(config.compression_format)
        elif config.compression_format and not compression_function:
            # 如果只有自定義格式沒有壓縮函數，創建新的函數
            from ..core.presets import create_custom_compression_function
            compression_function = create_custom_compression_function(config.compression_format)

        file_settings = {
            "rotation": config.rotation,
            "retention": config.retention,
            "compression": compression_function,
            "encoding": "utf-8",
            "enqueue": True,
            "filter": filters["file"],
        }
        # 過濾掉值為 None 的設置
        file_settings = {k: v for k, v in file_settings.items() if v is not None}

        logger_instance.add(
            str(logfile),
            format=actual_format,
            level=config.level,
            **file_settings
        )
        print(f"Logger '{config.name}' (ID: {config.name}): Log file path set to {logfile}")
    else:
        print(f"Logger '{config.name}' (ID: {config.name}): Console only mode")