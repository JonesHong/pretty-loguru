"""
定義 Pretty Loguru 的類型協議

此模組提供所有與 Pretty Loguru 相關的類型定義和協議，
用於提供 IDE 自動完成和類型檢查功能，同時也作為開發人員
了解系統結構的參考。
"""
from typing import (
    Any, Callable, Dict, List, Literal, Optional, Protocol, Set, 
    TypeVar, Union, runtime_checkable, overload
)
from pathlib import Path
import sys

# 定義類型別名，使類型標註更簡潔
LogLevelType = Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
LogHandlerIdType = int
LogFilterType = Callable[[Dict[str, Any]], bool]
LogConfigType = Dict[str, Any]
LogPathType = Union[str, Path]
LogNameFormatType = Optional[str]
LogRotationType = Union[str, int]

# 預設日誌格式名稱
LogNamePresetType = Literal["default", "daily", "hourly", "minute", "simple", "detailed"]

# 輸出目標類型
OutputDestinationType = Literal["to_console_only", "to_log_file_only"]

# Logger 泛型型變量，用於方法鏈式調用
T = TypeVar('T', bound='EnhancedLoggerProtocol')


@runtime_checkable
class EnhancedLoggerProtocol(Protocol):
    """
    增強型 Logger 協議，定義 Pretty Loguru 擴展的 Logger 接口。
    
    這個協議包含 Loguru 原有的接口以及 Pretty Loguru 額外添加的方法。
    實現此協議的類可以被靜態類型檢查器識別為兼容的 Logger 類型。
    """
    
    #
    # 基本日誌記錄方法
    #
    
    @overload
    def debug(self, __message: str, *args: Any, **kwargs: Any) -> None: ...
    
    @overload
    def debug(self, __message: Any) -> None: ...
    
    @overload
    def info(self, __message: str, *args: Any, **kwargs: Any) -> None: ...
    
    @overload
    def info(self, __message: Any) -> None: ...
    
    @overload
    def success(self, __message: str, *args: Any, **kwargs: Any) -> None: ...
    
    @overload
    def success(self, __message: Any) -> None: ...
    
    @overload
    def warning(self, __message: str, *args: Any, **kwargs: Any) -> None: ...
    
    @overload
    def warning(self, __message: Any) -> None: ...
    
    @overload
    def error(self, __message: str, *args: Any, **kwargs: Any) -> None: ...
    
    @overload
    def error(self, __message: Any) -> None: ...
    
    @overload
    def critical(self, __message: str, *args: Any, **kwargs: Any) -> None: ...
    
    @overload
    def critical(self, __message: Any) -> None: ...
    
    #
    # Pretty Loguru 自定義格式化方法
    #
    
    def block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None:
        """
        輸出一個帶有邊框的日誌區塊。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        """
        ...
    
    def console_block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        輸出一個帶有邊框的日誌區塊，僅輸出到控制台。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...
    
    def file_block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        輸出一個帶有邊框的日誌區塊，僅輸出到日誌文件。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...

    def ascii_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None:
        """
        輸出一個 ASCII 標題。

        :param text: 標題文字
        :param font: 字體樣式，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        """
        ...
    
    def console_ascii_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
    ) -> None:
        """
        輸出一個 ASCII 標題，僅輸出到控制台。

        :param text: 標題文字
        :param font: 字體樣式，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        """
        ...
    
    def file_ascii_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
    ) -> None:
        """
        輸出一個 ASCII 標題，僅輸出到日誌文件。

        :param text: 標題文字
        :param font: 字體樣式，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        """
        ...

    def ascii_block(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = None,
        ascii_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None:
        """
        輸出一個帶有 ASCII 標題的日誌區塊。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param ascii_header: ASCII 標題文字，預設為 None
        :param ascii_font: ASCII 字體樣式，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        """
        ...
    
    def console_ascii_block(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = None,
        ascii_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        輸出一個帶有 ASCII 標題的日誌區塊，僅輸出到控制台。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param ascii_header: ASCII 標題文字，預設為 None
        :param ascii_font: ASCII 字體樣式，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...
    
    def file_ascii_block(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = None,
        ascii_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        輸出一個帶有 ASCII 標題的日誌區塊，僅輸出到日誌文件。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param ascii_header: ASCII 標題文字，預設為 None
        :param ascii_font: ASCII 字體樣式，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...

    def is_ascii_only(self, text: str) -> bool:
        """
        檢查文字是否僅包含 ASCII 字元。

        :param text: 要檢查的文字
        :return: 如果文字僅包含 ASCII 字元，返回 True，否則返回 False
        """
        ...
    
    # FIGlet 藝術方法 (若 pyfiglet 可用)
    def figlet_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None:
        """
        輸出一個 FIGlet 藝術標題。

        :param text: 標題文字
        :param font: FIGlet 字體，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        """
        ...
    
    def console_figlet_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
    ) -> None:
        """
        輸出一個 FIGlet 藝術標題，僅輸出到控制台。

        :param text: 標題文字
        :param font: FIGlet 字體，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        """
        ...
    
    def file_figlet_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
    ) -> None:
        """
        輸出一個 FIGlet 藝術標題，僅輸出到日誌文件。

        :param text: 標題文字
        :param font: FIGlet 字體，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        """
        ...
    
    def figlet_block(
        self,
        title: str,
        message_list: List[str],
        figlet_header: Optional[str] = None,
        figlet_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None:
        """
        輸出一個帶有 FIGlet 藝術標題的日誌區塊。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param figlet_header: FIGlet 標題文字，預設為 None
        :param figlet_font: FIGlet 字體，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌文件，預設為 False
        """
        ...
    
    def console_figlet_block(
        self,
        title: str,
        message_list: List[str],
        figlet_header: Optional[str] = None,
        figlet_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        輸出一個帶有 FIGlet 藝術標題的日誌區塊，僅輸出到控制台。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param figlet_header: FIGlet 標題文字，預設為 None
        :param figlet_font: FIGlet 字體，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...
    
    def file_figlet_block(
        self,
        title: str,
        message_list: List[str],
        figlet_header: Optional[str] = None,
        figlet_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        輸出一個帶有 FIGlet 藝術標題的日誌區塊，僅輸出到日誌文件。

        :param title: 區塊的標題
        :param message_list: 區塊內的訊息列表
        :param figlet_header: FIGlet 標題文字，預設為 None
        :param figlet_font: FIGlet 字體，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...
    
    def get_figlet_fonts(self) -> Set[str]:
        """
        獲取所有可用的 FIGlet 字體

        :return: 可用字體名稱的集合
        """
        ...
    
    #
    # 目標導向日誌方法 (控制台專用)
    #
    
    def console(self, level: str, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的日誌記錄方法。
        
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def console_debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的調試級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def console_info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的資訊級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def console_success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的成功級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def console_warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的警告級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def console_error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的錯誤級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def console_critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的嚴重錯誤級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    #
    # 目標導向日誌方法 (文件專用)
    #
    
    def file(self, level: str, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的日誌記錄方法。
        
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def file_debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的調試級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def file_info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的資訊級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def file_success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的成功級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def file_warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的警告級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def file_error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的錯誤級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def file_critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的嚴重錯誤級別日誌。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    #
    # 開發模式方法 (僅控制台別名)
    #
    
    def dev(self, level: str, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式日誌記錄方法，僅在控制台顯示 (console 的別名)。
        
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def dev_debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式調試級別日誌，僅在控制台顯示 (console_debug 的別名)。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def dev_info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式資訊級別日誌，僅在控制台顯示 (console_info 的別名)。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def dev_success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式成功級別日誌，僅在控制台顯示 (console_success 的別名)。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def dev_warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式警告級別日誌，僅在控制台顯示 (console_warning 的別名)。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def dev_error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式錯誤級別日誌，僅在控制台顯示 (console_error 的別名)。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def dev_critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式嚴重錯誤級別日誌，僅在控制台顯示 (console_critical 的別名)。
        
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    #
    # Loguru 原生核心方法 (支持方法鏈)
    #
    
    def bind(self, **kwargs: Any) -> T:
        """
        創建一個帶有綁定上下文變數的 logger 副本。
        
        :param kwargs: 要綁定的上下文變數
        :return: 綁定了上下文變數的 logger 實例
        """
        ...
    
    def opt(self, *, depth: int = 0, exception: Optional[BaseException] = None, 
            lazy: bool = False, colors: bool = False, raw: bool = False, 
            capture: bool = True, record: bool = False, ansi: bool = False) -> T:
        """
        創建一個帶有特定配置選項的 logger 副本。
        
        :param depth: 調用棧的深度偏移，影響日誌中顯示的文件/行號
        :param exception: 要記錄的異常對象
        :param lazy: 是否延遲格式化日誌消息，直到需要時才執行
        :param colors: 是否啟用 ANSI 顏色
        :param raw: 是否原樣輸出消息，不進行格式化
        :param capture: 是否捕獲調用者信息 (文件名、行號等)
        :param record: 是否創建記錄對象並返回，而不是輸出日誌
        :param ansi: 是否解釋日誌字符串中的 ANSI 轉義序列
        :return: 帶有特定配置選項的 logger 實例
        """
        ...
    
    def patch(self, patcher: Callable[[Dict[str, Any]], Dict[str, Any]]) -> T:
        """
        創建一個使用自定義函數修改記錄屬性的 logger 副本。
        
        :param patcher: 一個接收和返回記錄字典的函數
        :return: 使用修補器的 logger 實例
        """
        ...
    
    def level(self, name: str) -> Any:
        """
        獲取指定名稱的日誌級別。
        
        :param name: 日誌級別名稱
        :return: 日誌級別對象
        """
        ...
    
    def configure(self, **kwargs: Any) -> None:
        """
        配置 logger 設定，如處理程序和日誌級別。
        
        :param kwargs: 配置參數
        """
        ...
    
    def add(self, sink: Any, **kwargs: Any) -> int:
        """
        添加一個日誌處理程序。
        
        :param sink: 處理程序對象，可以是文件路徑、文件對象或回調函數
        :param kwargs: 處理程序選項
        :return: 處理程序 ID
        """
        ...
    
    def remove(self, handler_id: Optional[int] = None) -> None:
        """
        移除日誌處理程序。
        
        :param handler_id: 要移除的處理程序 ID，如果為 None 則移除所有處理程序
        """
        ...
    
    def complete(self) -> None:
        """
        等待所有添加的非同步處理程序完成。
        """
        ...
    
    def catch(self, exception: Union[type, tuple, None] = None, *,
              level: str = "ERROR", reraise: bool = False,
              message: str = "An error has been caught in function '{record[function]}', "
                             "process '{record[process].name}' ({record[process].id}), "
                             "thread '{record[thread].name}' ({record[thread].id}):"
             ) -> Callable:
        """
        創建一個 catch 裝飾器，用於捕獲函數中的異常並記錄。
        
        :param exception: 要捕獲的異常類型
        :param level: 捕獲異常時使用的日誌級別
        :param reraise: 是否在捕獲後重新拋出異常
        :param message: 捕獲異常時記錄的消息
        :return: 異常捕獲裝飾器
        """
        ...
    
    def log(self, level: Union[str, int], message: str, *args: Any, **kwargs: Any) -> None:
        """
        使用指定級別記錄日誌消息。
        
        :param level: 日誌級別
        :param message: 日誌消息
        :param args: 格式化參數
        :param kwargs: 關鍵字參數
        """
        ...


# 用於靜態類型檢查的類型別名
EnhancedLogger = EnhancedLoggerProtocol