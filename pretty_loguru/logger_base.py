# https://betterstack.com/community/guides/logging/loguru/#getting-started-with-loguru
# https://www.readfog.com/a/1640196300205035520
# https://stackoverflow.com/questions/70977165/how-to-use-loguru-defaults-and-extra-information
from enum import Enum
import logging
import os
from pathlib import Path
import sys
from typing import List, Optional, Union, Dict, Any, Set, Callable
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

# 預定義的日誌檔案名格式
LOG_NAME_FORMATS = {
    "default": "[{process_id}]{timestamp}.log",  # 預設格式
    "daily": "{date}_{process_id}.log",  # 每日一檔
    "hourly": "{date}_{hour}_{process_id}.log",  # 每小時一檔
    "minute": "{date}_{hour}{minute}_{process_id}.log",  # 每分鐘一檔
    "simple": "{process_id}.log",  # 簡單格式，只包含進程 ID
    "detailed": "[{process_id}]_{date}_{time}.log",  # 詳細格式，包含日期和時間
}

# 輸出目標類型
OUTPUT_DESTINATIONS = {
    "console_only": "to_console_only",    # 僅顯示在控制台
    "file_only": "to_log_file_only",      # 僅寫入文件 
}


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


def create_destination_filters() -> Dict[str, Callable]:
    """
    創建基於目標的過濾器函數

    Returns:
        Dict[str, Callable]: 包含控制台和文件過濾器的字典
    """
    # 控制台過濾器
    def console_filter(record):
        # 如果記錄明確標記為只輸出到文件，則不在控制台顯示
        if record["extra"].get("to_log_file_only", False):
            return False
        return True

    # 文件過濾器
    def file_filter(record):
        # 如果記錄明確標記為只輸出到控制台，則不寫入文件
        if record["extra"].get("to_console_only", False):
            return False
        return True

    return {
        "console": console_filter,
        "file": file_filter
    }


def format_log_filename(
    process_id: str,
    log_name_format: Optional[str] = None,
    timestamp_format: Optional[str] = None
) -> str:
    """
    根據提供的格式生成日誌檔案名，並處理不合法的文件名字符
    
    Args:
        process_id (str): 進程 ID 或服務名稱
        log_name_format (Optional[str]): 日誌檔案名格式，可以是自定義的格式或 LOG_NAME_FORMATS 中的鍵
        timestamp_format (Optional[str]): 時間戳格式，預設為 "%Y%m%d-%H%M%S"
        
    Returns:
        str: 格式化後的日誌檔案名，已移除不合法字符
    """
    now = datetime.now()
    
    # 如果提供的是預定義格式的鍵，則獲取對應的格式
    if log_name_format in LOG_NAME_FORMATS:
        log_name_format = LOG_NAME_FORMATS[log_name_format]
    # 如果沒有提供格式，使用預設格式
    elif log_name_format is None:
        log_name_format = LOG_NAME_FORMATS["default"]
    
    # 使用提供的時間戳格式或預設格式
    ts_format = timestamp_format or "%Y%m%d-%H%M%S"
    timestamp = now.strftime(ts_format)
    
    # 準備替換變數
    format_vars = {
        "process_id": process_id,
        "timestamp": timestamp,
        "date": now.strftime("%Y%m%d"),
        "time": now.strftime("%H%M%S"),
        "year": now.strftime("%Y"),
        "month": now.strftime("%m"),
        "day": now.strftime("%d"),
        "hour": now.strftime("%H"),
        "minute": now.strftime("%M"),
        "second": now.strftime("%S"),
    }
    
    # 替換格式中的變數
    filename = log_name_format.format(**format_vars)
    
    # 替換文件名中的不合法字符
    # Windows 不允許的字符: \ / : * ? " < > |
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    
    return filename


def init_logger(
    level: str = log_level,
    log_path: Union[str, Path, None] = None,
    process_id: str = "",
    rotation: str = f"{log_rotation}",
    subdirectory: Optional[str] = None,
    log_name_format: Optional[str] = None,
    timestamp_format: Optional[str] = None,
    log_file_settings: Optional[Dict[str, Any]] = None,
):
    """
    初始化日誌系統

    Args:
        level (str): 日誌級別，預設為全域變數 log_level。
        log_path (Union[str, Path, None]): 日誌儲存路徑，若為 None 則使用預設路徑。
        process_id (str): 處理程序 ID，用於標記日誌檔案。
        rotation (str): 日誌輪換大小，單位為 MB。
        subdirectory (Optional[str]): 子目錄名稱，用於分類不同類型的日誌。
        log_name_format (Optional[str]): 日誌檔案名稱格式，可以是自定義格式或 LOG_NAME_FORMATS 中的預定義格式。
        timestamp_format (Optional[str]): 時間戳格式，用於自定義時間顯示方式。
        log_file_settings (Optional[Dict[str, Any]]): 日誌檔案的其他設定，如壓縮、保留時間等。

    如果 log_path 為 None，就在當前工作目錄下建立 ./logs 資料夾。
    如果提供了 subdirectory，則會在 log_path 下建立相應的子目錄。

    Returns:
        str: 日誌檔案的完整路徑
    """
    # 1. 決定最終要用的資料夾
    if log_path is None:
        base = Path.cwd() / "logs"  # 預設日誌資料夾
    else:
        base = Path(log_path)
    
    # 如果指定了子目錄，將其添加到基礎路徑中
    if subdirectory:
        base = base / subdirectory
        
    # 確保資料夾存在
    base.mkdir(parents=True, exist_ok=True)

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

    # 4. 生成日誌檔案名
    log_filename = format_log_filename(process_id, log_name_format, timestamp_format)
    logfile = base / log_filename
    
    # 5. 創建目標過濾器
    filters = create_destination_filters()
    
    # 處理輪換大小格式
    rotation_value = rotation
    if isinstance(rotation, str):
        # 檢查是否已經包含單位 (如 "10 MB", "1 day" 等)
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
        "encoding": "utf-8",  # 檔案編碼
        "enqueue": True,  # 使用多線程安全的方式寫入
        "filter": filters["file"],  # 文件過濾器
    }
    
    # 合併自定義設置
    if log_file_settings:
        file_settings.update(log_file_settings)
    
    # 7. 新增檔案 handler
    _logger.add(
        str(logfile),
        format=logger_format,  # 使用定義的日誌格式
        level=level,  # 設定日誌級別
        **file_settings
    )

    # 8. 新增 console handler
    _logger.add(
        sys.stderr,
        format=logger_format,  # 使用相同的日誌格式
        level=level,  # 設定日誌級別
        filter=filters["console"],  # 控制台過濾器
    )
    
    # 返回完整的日誌文件路徑，方便外部使用
    return str(logfile)


# 新增目標導向日誌方法 - 只輸出到控制台
def _console_only(level, message, *args, **kwargs):
    """
    僅在控制台顯示的日誌記錄方法
    
    Args:
        level: 日誌級別
        message: 日誌訊息
        *args: 其他位置參數
        **kwargs: 其他關鍵字參數
    """
    return _logger.bind(to_console_only=True).log(level, message, *args, **kwargs)


# 新增目標導向日誌方法 - 只輸出到文件
def _file_only(level, message, *args, **kwargs):
    """
    僅寫入文件的日誌記錄方法
    
    Args:
        level: 日誌級別
        message: 日誌訊息
        *args: 其他位置參數
        **kwargs: 其他關鍵字參數
    """
    return _logger.bind(to_log_file_only=True).log(level, message, *args, **kwargs)


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


# 開發模式日誌方法 (別名為控制台方法)
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


# 動態擴展 _logger 的輸出目標方法
# 控制台專用方法
_logger.console = _console_only
_logger.console_debug = _console_debug
_logger.console_info = _console_info
_logger.console_success = _console_success
_logger.console_warning = _console_warning
_logger.console_error = _console_error
_logger.console_critical = _console_critical

# 文件專用方法
_logger.file = _file_only
_logger.file_debug = _file_debug
_logger.file_info = _file_info
_logger.file_success = _file_success
_logger.file_warning = _file_warning
_logger.file_error = _file_error
_logger.file_critical = _file_critical

# 開發模式方法 (別名)
_logger.dev = _console_only
_logger.dev_debug = _dev_debug
_logger.dev_info = _dev_info
_logger.dev_success = _dev_success
_logger.dev_warning = _dev_warning
_logger.dev_error = _dev_error
_logger.dev_critical = _dev_critical


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
                
            # 遞歸清理所有子目錄
            for root, dirs, files in os.walk(check_path):
                for file in files:
                    if file.startswith("."):  # 忽略隱藏檔案
                        continue
                    file_path = os.path.join(root, file)
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