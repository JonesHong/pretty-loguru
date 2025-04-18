"""
日誌系統初始化相關函數
"""
import inspect
import logging
import os
from types import FrameType
from typing import cast

from .logger_base import _logger, LoggerClear, init_logger


# https://blog.csdn.net/qq_51967017/article/details/134045236
def uvicorn_init_config():
    """配置 uvicorn 日誌以使用 loguru
    
    用於與 Uvicorn 服務器集成，讓 Uvicorn 的日誌也使用 loguru 格式
    """
    LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

    # 先移除所有現有的處理器
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    root_logger.addHandler(InterceptHandler())
    
    # 設定 uvicorn 特定日誌
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        if logging_logger.handlers:
            for handler in logging_logger.handlers[:]:
                logging_logger.removeHandler(handler)
        logging_logger.addHandler(InterceptHandler())


def logger_start(file=None, folder=None):
    """
    初始化 logger 並啟動日誌清理器
    
    Args:
        file: 文件路徑，如果提供則使用文件名作為 process_id
        folder: 文件夾名稱，如果 file 未提供則使用 folder 作為 process_id
    
    Returns:
        str: 使用的 process_id
    
    用法:
        1. 簡單使用: logger_start() - 自動獲取調用文件和文件夾
        2. 指定文件: logger_start(file=__file__)
        3. 指定文件夾: logger_start(folder="custom_folder")
    """
    # 获取调用该函数的文件信息
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename
    
    # 确定process_id
    process_id = None
    
    # 如果提供了file参数，使用它
    if file is not None:
        process_id = os.path.splitext(os.path.basename(file))[0]
    # 如果提供了folder参数，使用它
    elif folder is not None:
        process_id = folder
    # 否则，尝试从调用文件中获取
    else:
        # 获取调用文件的文件名(不含扩展名)
        file_name = os.path.splitext(os.path.basename(caller_file))[0]
        # 获取调用文件所在的文件夹名称
        folder_name = os.path.basename(os.path.dirname(caller_file))
        
        # 优先使用文件名
        process_id = file_name
    
    # 初始化logger
    init_logger(process_id=process_id)
    
    # 启动日志清理器
    logger_cleaner = LoggerClear()
    logger_cleaner.start()
    
    return process_id


class InterceptHandler(logging.Handler):
    """用於捕獲標準日誌庫的日誌並轉發給 loguru
    
    這個處理器可以攔截 Python 標準庫的日誌消息，並將它們重定向到 loguru
    """
    
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)
 
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1
 
        _logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )