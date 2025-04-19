"""
這是一個類型存根文件 (.pyi)，用於提供精確的類型標註
IDE 會優先參考這個文件進行類型檢查和自動完成提示
"""
from typing import Any, Callable, Dict, List, Optional, Union, overload
import loguru

class EnhancedLogger(loguru._logger.Logger):
    """
    擴展 loguru 的內部 Logger 類，添加自定義方法的類型提示。
    此類別提供額外的功能，例如區塊式日誌輸出和 ASCII 標題。
    """
    
    def block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = ...,
        log_level: str = ...,
    ) -> None:
        """
        輸出一個帶有邊框的日誌區塊。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param border_style: 邊框樣式，預設為系統樣式
        :param log_level: 日誌等級，預設為系統等級
        """
        ...
    
    def ascii_header(
        self,
        text: str,
        font: str = ...,
        log_level: str = ...,
        border_style: str = ...,
        to_console_only: bool = ...,
        to_log_file_only: bool = ...,
    ) -> None:
        """
        輸出一個 ASCII 標題。

        :param text: 標題文字
        :param font: 字體樣式，預設為系統字體
        :param log_level: 日誌等級，預設為系統等級
        :param border_style: 邊框樣式，預設為系統樣式
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        """
        ...
    
    def ascii_block(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = ...,
        ascii_font: str = ...,
        border_style: str = ...,
        log_level: str = ...,
    ) -> None:
        """
        輸出一個帶有 ASCII 標題的日誌區塊。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param ascii_header: ASCII 標題文字，預設為 None
        :param ascii_font: ASCII 字體樣式，預設為系統字體
        :param border_style: 邊框樣式，預設為系統樣式
        :param log_level: 日誌等級，預設為系統等級
        """
        ...
    
    def is_ascii_only(self, text: str) -> bool:
        """
        檢查文字是否僅包含 ASCII 字元。

        :param text: 要檢查的文字
        :return: 如果文字僅包含 ASCII 字元，返回 True，否則返回 False
        """
        ...

# 導出的主要 logger 對象
logger: EnhancedLogger

def print_block(
    title: str,
    message_list: List[str],
    border_style: str = ...,
    log_level: str = ...,
) -> None:
    """
    輸出一個帶有邊框的日誌區塊。

    :param title: 區塊的標題
    :param message_list: 區塊內的訊息列表
    :param border_style: 邊框樣式，預設為系統樣式
    :param log_level: 日誌等級，預設為系統等級
    """
    ...

def print_ascii_header(
    text: str,
    font: str = ...,
    log_level: str = ...,
    border_style: str = ...,
    to_console_only: bool = ...,
    to_log_file_only: bool = ...,
) -> None:
    """
    輸出一個 ASCII 標題。

    :param text: 標題文字
    :param font: 字體樣式，預設為系統字體
    :param log_level: 日誌等級，預設為系統等級
    :param border_style: 邊框樣式，預設為系統樣式
    :param to_console_only: 是否僅輸出到控制台，預設為 False
    :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
    """
    ...

def print_ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = ...,
    ascii_font: str = ...,
    border_style: str = ...,
    log_level: str = ...,
) -> None:
    """
    輸出一個帶有 ASCII 標題的日誌區塊。

    :param title: 區塊的標題
    :param message_list: 區塊內的訊息列表
    :param ascii_header: ASCII 標題文字，預設為 None
    :param ascii_font: ASCII 字體樣式，預設為系統字體
    :param border_style: 邊框樣式，預設為系統樣式
    :param log_level: 日誌等級，預設為系統等級
    """
    ...

def is_ascii_only(text: str) -> bool:
    """
    檢查文字是否僅包含 ASCII 字元。

    :param text: 要檢查的文字
    :return: 如果文字僅包含 ASCII 字元，返回 True，否則返回 False
    """
    ...

def logger_start(file: Optional[str] = None, folder: Optional[str] = None) -> str:
    """
    初始化 logger 並開始記錄日誌。

    :param file: 日誌文件的名稱，預設為 None
    :param folder: 日誌文件的資料夾，預設為 None
    :return: 日誌文件的完整路徑
    """
    ...

def uvicorn_init_config() -> None:
    """
    初始化 uvicorn 的配置。
    """
    ...

log_path: str
"""
日誌文件的路徑。
"""