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

# 日誌相關的全域變數
log_level = "INFO"  # 預設日誌級別
log_rotation = 20  # 日誌輪換大小，單位為 MB
log_path = Path.cwd() / "logs"  # 預設日誌儲存路徑


class LogLevelEnum(Enum):
    """日誌級別枚舉類別

    定義了不同的日誌級別，用於設定和過濾日誌輸出。
    """
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# 日誌輸出的格式設定
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

    Args:
        level (str): 日誌級別，預設為全域變數 log_level。
        log_path (str | Path | None): 日誌儲存路徑，若為 None 則使用預設路徑。
        process_id (str): 處理程序 ID，用於標記日誌檔案。
        rotation (str): 日誌輪換大小，單位為 MB。

    如果 log_path 為 None，就在當前工作目錄下建立 ./logs 資料夾。
    """
    # 1. 決定最終要用的資料夾
    if log_path is None:
        base = Path.cwd() / "logs"  # 預設日誌資料夾
    else:
        base = Path(log_path)
    base.mkdir(parents=True, exist_ok=True)  # 確保資料夾存在

    # 2. 移除舊的 handler
    for handler_id in _logger._core.handlers:
        _logger.remove(handler_id)  # 清除所有舊的日誌處理器

    # 3. 設定附加資訊
    _logger.configure(
        extra={
            "folder": process_id,  # 額外資訊：處理程序 ID
            "to_console_only": False,  # 是否僅輸出到控制台
            "to_log_file_only": False,  # 是否僅輸出到日誌檔案
        }
    )

    # 4. 新增檔案 handler
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # 生成時間戳
    logfile = base / f"[{process_id}]{timestamp}.log"  # 日誌檔案名稱
    _logger.add(
        str(logfile),
        format=logger_format,  # 使用定義的日誌格式
        rotation=f"{rotation}MB",  # 設定日誌輪換大小
        encoding="utf-8",  # 檔案編碼
        enqueue=True,  # 使用多線程安全的方式寫入
        level=level,  # 設定日誌級別
        filter=lambda record: not record["extra"].get("to_console_only", False),  # 過濾條件
    )

    # 5. 新增 console handler
    _logger.add(
        sys.stderr,
        format=logger_format,  # 使用相同的日誌格式
        level=level,  # 設定日誌級別
        filter=lambda record: not record["extra"].get("to_log_file_only", False),  # 過濾條件
    )


class LoggerClear:
    """日誌清理器類別

    用於定期清理過舊的日誌檔案，避免磁碟空間被佔滿。
    """
    
    def __init__(
        self, log_retention=f"{log_rotation}", log_path=log_path
    ) -> None:
        """
        初始化日誌清理器

        Args:
            log_retention (str): 日誌保留天數，預設為 log_rotation。
            log_path (Path): 日誌儲存路徑，預設為全域變數 log_path。
        """
        self.clear_thread = Thread(
            target=self.__clean_old_log_loop,  # 清理日誌的內部方法
            args=(log_path, log_retention),
            daemon=True,  # 設定為守護線程
        )
        self.__is_running = False  # 標記清理器是否正在運行

    def start(self):
        """啟動日誌清理線程"""
        if self.__is_running:
            _logger.info(f"Logger: Already Running...!!!")  # 如果已經在運行，記錄提示
        else:
            self.clear_thread.start()  # 啟動清理線程
            _logger.info(f"Logger: Clear Log Thread Started...!!!")  # 記錄啟動訊息
            self.__is_running = True  # 更新運行狀態

    def __clean_old_log_loop(self, log_path, log_retention):
        """
        清理過舊日誌的內部方法

        Args:
            log_path (Path): 日誌儲存路徑。
            log_retention (str): 日誌保留天數。
        """
        check_path = log_path  # 要檢查的日誌路徑
        current_datetime = datetime.now()  # 當前時間
        try:
            if not os.path.exists(check_path):  # 如果路徑不存在，則建立
                os.makedirs(check_path, exist_ok=True)
                return
                
            existing_record_list = os.listdir(check_path)  # 獲取日誌檔案列表
            for file in existing_record_list:
                if file.startswith("."):  # 忽略隱藏檔案
                    continue
                file_path = os.path.join(check_path, file)
                if not os.path.exists(file_path):  # 如果檔案不存在，跳過
                    continue
                    
                is_file = os.path.isfile(file_path)  # 檢查是否為檔案
                try:
                    is_expired_days = (
                        os.path.getctime(file_path)
                        < (
                            current_datetime - timedelta(days=int(log_retention))
                        ).timestamp()  # 檢查是否超過保留天數
                    )
                except (ValueError, OSError):
                    is_expired_days = False
                    
                if is_file and is_expired_days:  # 如果是檔案且過期
                    try:
                        os.remove(file_path)  # 刪除檔案
                        _logger.info(f"Logger: Clean Log: {file_path}")  # 記錄刪除訊息
                    except (PermissionError, OSError) as e:
                        _logger.warning(f"Logger: Cannot remove log file {file_path}: {str(e)}")  # 記錄錯誤訊息
        except Exception as e:
            _logger.error(f"Logger: Failed to clean log files. Exception: {str(e)}")  # 記錄異常訊息


# 配置 Rich Console，用於美化輸出
console = Console()