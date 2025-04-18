# https://betterstack.com/community/guides/logging/loguru/#getting-started-with-loguru
# https://www.readfog.com/a/1640196300205035520
# https://stackoverflow.com/questions/70977165/how-to-use-loguru-defaults-and-extra-information
from enum import Enum
import logging
import os
from pathlib import Path
import sys
from typing import List
import time
from loguru import logger as _logger
from datetime import datetime, timedelta
from threading import Thread

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


# # 获取项目根目录
# THIS_DIR = os.path.dirname(__file__)
# UTILS_DIR = os.path.dirname(THIS_DIR)
# PYTHON_DIR = os.path.dirname(UTILS_DIR)
# ROOT_DIR = os.path.dirname(PYTHON_DIR)
# # 添加项目根目录到 sys.path
# sys.path.append(ROOT_DIR)


# config = ConfigManager()
# system_config = config.system
# log_config = config.log
log_level = "INFO"  # 日誌級別
log_rotation = 20  # 日誌輪換大小，單位MB
log_path = Path.cwd() / "logs"


class LogLevelEnum(Enum):
    """日誌級別枚舉

    Args:
        Enum: 繼承自Enum類
    """
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# "<level>{time:YYYY-MM-DD HH:mm:ss} | {level}\t{process} | {file}:{function}:{line} - {message} </level>"
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}{process}</level> | "
    "<cyan>{extra[folder]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

def init_logger(
    level: str = log_level,
    log_path: str | Path | None = None,
    process_id: str = "",
    rotation: str = f"{log_rotation}",
):
    """
    初始化日誌系統

    如果 log_path 為 None，就在當前工作目錄下建立 ./logs 資料夾。
    """
    # 1. 決定最終要用的資料夾
    if log_path is None:
        base = Path.cwd() / "logs"
    else:
        base = Path(log_path)
    base.mkdir(parents=True, exist_ok=True)

    # 2. 移除舊的 handler
    for handler_id in _logger._core.handlers:
        _logger.remove(handler_id)

    # 3. 設定附加資訊
    _logger.configure(
        extra={
            "folder": process_id,
            "to_console_only": False,
            "to_log_file_only": False,
        }
    )

    # 4. 新增檔案 handler
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    logfile = base / f"[{process_id}]{timestamp}.log"
    _logger.add(
        str(logfile),
        format=logger_format,
        rotation=f"{rotation}MB",
        encoding="utf-8",
        enqueue=True,
        level=level,
        filter=lambda record: not record["extra"].get("to_console_only", False),
    )

    # 5. 新增 console handler
    _logger.add(
        sys.stderr,
        format=logger_format,
        level=level,
        filter=lambda record: not record["extra"].get("to_log_file_only", False),
    )


class LoggerClear:
    """日誌清理器，用於清理過舊的日誌檔案"""
    
    def __init__(
        self, log_retention=f"{log_rotation}", log_path=log_path
    ) -> None:
        """初始化日誌清理器

        Args:
            log_retention: 日誌保留天數
            log_path: 日誌保存路徑
        """
        self.clear_thread = Thread(
            target=self.__clean_old_log_loop,
            args=(log_path, log_retention),
            daemon=True,
        )
        self.__is_running = False

    def start(self):
        """啟動日誌清理線程"""
        if self.__is_running:
            _logger.info(f"Logger: Already Running...!!!")
        else:
            self.clear_thread.start()
            _logger.info(f"Logger: Clear Log Thread Started...!!!")
            self.__is_running = True

    def __clean_old_log_loop(self, log_path, log_retention):
        """清理過舊日誌的內部方法

        Args:
            log_path: 日誌路徑
            log_retention: 日誌保留天數
        """
        check_path = log_path
        current_datetime = datetime.now()
        try:
            if not os.path.exists(check_path):
                os.makedirs(check_path, exist_ok=True)
                return
                
            existing_record_list = os.listdir(check_path)
            for file in existing_record_list:
                if file.startswith("."):
                    continue
                file_path = os.path.join(check_path, file)
                if not os.path.exists(file_path):
                    continue
                    
                is_file = os.path.isfile(file_path)
                try:
                    is_expired_days = (
                        os.path.getctime(file_path)
                        < (
                            current_datetime - timedelta(days=int(log_retention))
                        ).timestamp()
                    )
                except (ValueError, OSError):
                    is_expired_days = False
                    
                if is_file and is_expired_days:
                    try:
                        os.remove(file_path)
                        _logger.info(f"Logger: Clean Log: {file_path}")
                    except (PermissionError, OSError) as e:
                        _logger.warning(f"Logger: Cannot remove log file {file_path}: {str(e)}")
        except Exception as e:
            _logger.error(f"Logger: Failed to clean log files. Exception: {str(e)}")


# 配置 Rich Console
console = Console()