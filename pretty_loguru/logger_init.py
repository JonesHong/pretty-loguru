"""
日誌系統初始化相關函數

此模組提供與日誌系統相關的初始化功能，包括與 Uvicorn 的整合以及自定義日誌處理器的設置。
"""

import inspect
import logging
import os
from types import FrameType
from typing import cast

from .logger_base import _logger, LoggerClear, init_logger


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


def logger_start(file=None, folder=None):
    """
    初始化 Loguru 日誌系統並啟動日誌清理器

    Args:
        file (str, optional): 指定的文件路徑，若提供則使用該文件名作為 process_id。
        folder (str, optional): 指定的文件夾名稱，若未提供 file 則使用該參數作為 process_id。

    Returns:
        str: 初始化的 process_id，用於標識當前日誌的來源。

    用法:
        1. logger_start() - 自動獲取調用文件和文件夾作為 process_id。
        2. logger_start(file=__file__) - 指定文件作為 process_id。
        3. logger_start(folder="custom_folder") - 指定文件夾作為 process_id。
    """
    # 獲取調用該函數的文件資訊
    caller_frame = inspect.currentframe().f_back  # 獲取上一層調用的堆疊幀
    caller_file = caller_frame.f_code.co_filename  # 獲取調用文件的完整路徑

    # 確定 process_id 的值
    process_id = None

    # 如果提供了 file 參數，使用該文件名作為 process_id
    if file is not None:
        process_id = os.path.splitext(os.path.basename(file))[0]
    # 如果提供了 folder 參數，使用該文件夾名稱作為 process_id
    elif folder is not None:
        process_id = folder
    # 如果都未提供，則嘗試從調用文件中推斷
    else:
        file_name = os.path.splitext(os.path.basename(caller_file))[0]  # 獲取文件名（無副檔名）
        folder_name = os.path.basename(os.path.dirname(caller_file))  # 獲取文件所在的文件夾名稱

        # 優先使用文件名作為 process_id
        process_id = file_name

    # 初始化 Loguru 日誌系統
    init_logger(process_id=process_id)

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