"""
日誌系統初始化相關函數

此模組提供與日誌系統相關的初始化功能，包括與 Uvicorn 的整合以及自定義日誌處理器的設置。
"""

import inspect
import logging
import os
import warnings
from pathlib import Path
from types import FrameType
from typing import cast, Optional, Dict, Any, Union, Literal, List

from .logger_base import _logger, LoggerClear, init_logger, LOG_NAME_FORMATS


def uvicorn_init_config():
    """
    配置 Uvicorn 日誌以使用 Loguru 格式化輸出

    此函數用於將 Uvicorn 的日誌輸出格式改為 Loguru 的格式，適合需要統一日誌格式的應用場景。
    """
    LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")  # Uvicorn 預設的日誌記錄器名稱

    # 先移除所有現有的處理器，避免重複輸出
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    root_logger.addHandler(InterceptHandler())  # 添加自定義的處理器以攔截日誌

    # 設定 Uvicorn 特定日誌的處理器
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        if logging_logger.handlers:
            for handler in logging_logger.handlers[:]:
                logging_logger.removeHandler(handler)
        logging_logger.addHandler(InterceptHandler())  # 使用相同的處理器攔截日誌


def logger_start(
    file=None, 
    service_name=None, 
    folder=None,  # 為了向後兼容
    subdirectory=None, 
    log_name_format=None,
    log_name_preset: Optional[Literal["default", "daily", "hourly", "minute", "simple", "detailed"]] = None,
    timestamp_format=None,
    log_base_path=None,
    log_file_settings: Optional[Dict[str, Any]] = None,
    tag_filter_config: Optional[Dict[str, List[str]]] = None,
    custom_config: Optional[Dict[str, Any]] = None
):
    """
    初始化 Loguru 日誌系統並啟動日誌清理器

    Args:
        file (str, optional): 指定的文件路徑，若提供則使用該文件名作為 process_id。
        service_name (str, optional): 服務或模組名稱，用於標識日誌來源。
        folder (str, optional): [已棄用] 使用 service_name 替代。
        subdirectory (str, optional): 日誌子目錄，用於分類不同模組或功能的日誌。
        log_name_format (str, optional): 日誌檔案名稱格式，可包含變數如 {process_id}, {timestamp}, {date}, {time} 等。
        log_name_preset (str, optional): 預設的日誌檔案名格式，可選值為：
            - "default": "[{process_id}]{timestamp}.log"
            - "daily": "{date}_{process_id}.log"
            - "hourly": "{date}_{hour}_{process_id}.log"
            - "minute": "{date}_{hour}{minute}_{process_id}.log"
            - "simple": "{process_id}.log"
            - "detailed": "[{process_id}]_{date}_{time}.log"
        timestamp_format (str, optional): 時間戳格式，用於自定義時間顯示方式，默認為 "%Y%m%d-%H%M%S"。
        log_base_path (Union[str, Path], optional): 日誌基礎路徑，覆蓋預設的 log_path。
        log_file_settings (Dict[str, Any], optional): 日誌檔案的其他設定，如壓縮、保留時間等。
        tag_filter_config (Dict[str, List[str]], optional): 標籤過濾配置，可包含下列鍵：
            - console_only: 僅顯示在控制台的標籤列表
            - file_only: 僅寫入文件的標籤列表
            - console_exclude: 不顯示在控制台的標籤列表
            - file_exclude: 不寫入文件的標籤列表
        custom_config (Dict[str, Any], optional): 自定義日誌配置，可包含任意 init_logger 支援的參數。

    Returns:
        str: 初始化的 process_id，用於標識當前日誌的來源。

    用法:
        1. logger_start() - 自動獲取調用文件和文件夾作為 process_id，使用預設日誌格式。
        2. logger_start(file=__file__) - 指定文件作為 process_id。
        3. logger_start(service_name="api_service") - 指定服務名稱作為 process_id。
        4. logger_start(subdirectory="api_logs") - 將日誌保存在 logs/api_logs/ 子目錄中。
        5. logger_start(log_name_preset="daily") - 使用每日一檔的命名方式。
        6. logger_start(log_name_format="{date}_{process_id}.log") - 自定義日誌檔案名格式。
        7. logger_start(timestamp_format="%Y-%m-%d") - 自定義時間戳格式。
        8. logger_start(tag_filter_config={"console_only": ["dev", "debug"]}) - 設置標籤過濾規則。
    """
    # 處理向後兼容性: 如果提供了 folder 參數但沒有提供 service_name，則使用 folder
    if folder is not None and service_name is None:
        warnings.warn(
            "The 'folder' parameter is deprecated and will be removed in a future version. "
            "Use 'service_name' instead.",
            DeprecationWarning,
            stacklevel=2
        )
        service_name = folder
    
    # 獲取調用該函數的文件資訊
    caller_frame = inspect.currentframe().f_back  # 獲取上一層調用的堆疊幀
    caller_file = caller_frame.f_code.co_filename  # 獲取調用文件的完整路徑

    # 確定 process_id 的值
    process_id = None

    # 如果提供了 file 參數，使用該文件名作為 process_id
    if file is not None:
        process_id = os.path.splitext(os.path.basename(file))[0]
    # 如果提供了 service_name 參數，使用該服務名稱作為 process_id
    elif service_name is not None:
        process_id = service_name
    # 如果都未提供，則嘗試從調用文件中推斷
    else:
        file_name = os.path.splitext(os.path.basename(caller_file))[0]  # 獲取文件名（無副檔名）
        folder_name = os.path.basename(os.path.dirname(caller_file))  # 獲取文件所在的文件夾名稱

        # 優先使用文件名作為 process_id
        process_id = file_name

    # 如果提供了預設日誌名稱，則使用預設格式
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
        "tag_filter_config": tag_filter_config,
    }
    
    # 合併自定義配置（如果有）
    if custom_config:
        logger_config.update(custom_config)
    
    # 初始化 Loguru 日誌系統
    log_file_path = init_logger(**logger_config)

    # 啟動日誌清理器，定期清理過期日誌
    logger_cleaner = LoggerClear()
    logger_cleaner.start()

    return process_id


class InterceptHandler(logging.Handler):
    """
    攔截標準日誌庫的日誌並轉發給 Loguru

    此處理器用於將 Python 標準日誌庫的日誌消息攔截並轉發到 Loguru，實現統一的日誌管理。
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        處理日誌記錄，將其轉發給 Loguru。

        Args:
            record (logging.LogRecord): 標準日誌庫的日誌記錄物件。
        """
        try:
            # 嘗試獲取對應的 Loguru 日誌等級
            level = _logger.level(record.levelname).name
        except ValueError:
            # 如果無法匹配，則使用數字等級
            level = str(record.levelno)

        # 獲取日誌消息的調用來源
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # 避免定位到標準日誌庫內部
            frame = cast(FrameType, frame.f_back)
            depth += 1

        # 使用 Loguru 記錄日誌，包含調用深度與異常資訊
        _logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )