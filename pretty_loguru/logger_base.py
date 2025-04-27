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

# 預設的標籤過濾配置
DEFAULT_TAG_CONFIG = {
    "console_only": [],      # 僅顯示在控制台的標籤
    "file_only": [],         # 僅寫入文件的標籤
    "console_exclude": [],   # 不顯示在控制台的標籤
    "file_exclude": [],      # 不寫入文件的標籤
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


# 日誌輸出的格式設定 - 修正後版本
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}{process}</level> | "
    "<cyan>{extra[folder]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def create_tag_filter(filter_config: Dict[str, List[str]]) -> Dict[str, Callable]:
    """
    創建基於標籤的過濾器函數

    Args:
        filter_config: 過濾器配置，包含 console_only, file_only, console_exclude, file_exclude 鍵

    Returns:
        Dict[str, Callable]: 包含控制台和文件過濾器的字典
    """
    # 獲取過濾配置
    console_only = set(filter_config.get("console_only", []))
    file_only = set(filter_config.get("file_only", []))
    console_exclude = set(filter_config.get("console_exclude", []))
    file_exclude = set(filter_config.get("file_exclude", []))

    # 控制台過濾器
    def console_filter(record):
        # 檢查是否有舊的過濾設置（向後兼容）
        if record["extra"].get("to_log_file_only", False):
            return False
            
        # 獲取記錄中的標籤
        tags = set(_parse_tags(record["extra"].get("tags", "")))
        
        # 檢查標籤過濾規則
        # 1. 如果有 console_only 標籤且記錄沒有任何這些標籤，則過濾掉
        if console_only and not any(tag in console_only for tag in tags):
            return False
            
        # 2. 如果記錄有任何 console_exclude 標籤，則過濾掉
        if any(tag in console_exclude for tag in tags):
            return False
            
        # 3. 如果記錄有任何 file_only 標籤且沒有在 console_only 中，則過濾掉
        if any(tag in file_only for tag in tags) and not any(tag in console_only for tag in tags):
            return False
            
        return True

    # 文件過濾器
    def file_filter(record):
        # 檢查是否有舊的過濾設置（向後兼容）
        if record["extra"].get("to_console_only", False):
            return False
            
        # 獲取記錄中的標籤
        tags = set(_parse_tags(record["extra"].get("tags", "")))
        
        # 檢查標籤過濾規則
        # 1. 如果有 file_only 標籤且記錄沒有任何這些標籤，則過濾掉
        if file_only and not any(tag in file_only for tag in tags):
            return False
            
        # 2. 如果記錄有任何 file_exclude 標籤，則過濾掉
        if any(tag in file_exclude for tag in tags):
            return False
            
        # 3. 如果記錄有任何 console_only 標籤且沒有在 file_only 中，則過濾掉
        if any(tag in console_only for tag in tags) and not any(tag in file_only for tag in tags):
            return False
            
        return True

    return {
        "console": console_filter,
        "file": file_filter
    }


def _parse_tags(tags_str: str) -> List[str]:
    """
    解析標籤字符串為標籤列表，處理空字符串的情況

    Args:
        tags_str: 標籤字符串，以逗號分隔

    Returns:
        List[str]: 標籤列表
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(",") if tag.strip()]


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
    tag_filter_config: Optional[Dict[str, List[str]]] = None,
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
        tag_filter_config (Optional[Dict[str, List[str]]]): 標籤過濾器配置，可以包含以下鍵:
            - console_only: 僅顯示在控制台的標籤列表
            - file_only: 僅寫入文件的標籤列表
            - console_exclude: 不顯示在控制台的標籤列表
            - file_exclude: 不寫入文件的標籤列表

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
            "to_console_only": False,  # 是否僅輸出到控制台 (向後兼容)
            "to_log_file_only": False,  # 是否僅輸出到日誌檔案 (向後兼容)
            "tags": "",  # 標籤，用於過濾
        }
    )

    # 4. 生成日誌檔案名
    log_filename = format_log_filename(process_id, log_name_format, timestamp_format)
    logfile = base / log_filename
    
    # 5. 創建標籤過濾器
    filter_config = tag_filter_config or DEFAULT_TAG_CONFIG
    filters = create_tag_filter(filter_config)
    
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
        "filter": filters["file"],  # 基於標籤的文件過濾器
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
        filter=filters["console"],  # 基於標籤的控制台過濾器
    )
    
    # 返回完整的日誌文件路徑，方便外部使用
    return str(logfile)


# 添加標籤功能的擴展方法 - 修正後版本，直接修改消息
def _log_with_tags(level, message, *args, tags=None, **kwargs):
    """
    帶有標籤的日誌記錄方法，處理所有類型的空標籤情況
    
    Args:
        level: 日誌級別
        message: 日誌訊息
        *args: 其他位置參數
        tags: 標籤列表或逗號分隔的標籤字符串
        **kwargs: 其他關鍵字參數
    """
    # 處理標籤
    tags_str = ""
    
    # 更全面處理標籤
    if tags is not None:
        # 處理各種空標籤情況
        if isinstance(tags, list):
            if tags:  # 非空列表
                tags_str = ", ".join(str(tag) for tag in tags if str(tag).strip())
        elif isinstance(tags, str):
            tags_str = tags.strip()
        else:
            tags_str = str(tags).strip()
    
    # 如果經過處理後標籤非空，則在消息前添加標籤
    if tags_str:
        message = f"[{tags_str}] {message}"
    
    # 保存標籤用於過濾（即使不顯示在消息中）
    return _logger.bind(tags=tags_str).log(level, message, *args, **kwargs)


# 添加標籤版本的各級別日誌方法
def _debug_with_tags(message, *args, tags=None, **kwargs):
    return _log_with_tags("DEBUG", message, *args, tags=tags, **kwargs)

def _info_with_tags(message, *args, tags=None, **kwargs):
    return _log_with_tags("INFO", message, *args, tags=tags, **kwargs)

def _success_with_tags(message, *args, tags=None, **kwargs):
    return _log_with_tags("SUCCESS", message, *args, tags=tags, **kwargs)

def _warning_with_tags(message, *args, tags=None, **kwargs):
    return _log_with_tags("WARNING", message, *args, tags=tags, **kwargs)

def _error_with_tags(message, *args, tags=None, **kwargs):
    return _log_with_tags("ERROR", message, *args, tags=tags, **kwargs)

def _critical_with_tags(message, *args, tags=None, **kwargs):
    return _log_with_tags("CRITICAL", message, *args, tags=tags, **kwargs)


# 動態擴展 _logger
_logger.log_with_tags = _log_with_tags
_logger.debug_t = _debug_with_tags
_logger.info_t = _info_with_tags
_logger.success_t = _success_with_tags
_logger.warning_t = _warning_with_tags
_logger.error_t = _error_with_tags
_logger.critical_t = _critical_with_tags


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