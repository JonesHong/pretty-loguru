"""
定義日誌系統的類型協議，用於提供 IDE 自動完成和類型檢查功能
"""
from typing import List, Optional, Protocol, Any, Union, Dict, TypeVar, Callable

# 定義一個協議來描述 logger 對象
class EnhancedLoggerProtocol(Protocol):
    """
    定義擴展的 logger 協議，提供多種日誌記錄方法與自定義格式化功能。
    """

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        記錄調試級別的日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        記錄資訊級別的日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...

    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        記錄成功級別的日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        記錄警告級別的日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        記錄錯誤級別的日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        記錄嚴重錯誤級別的日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...

    def block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None:
        """
        記錄一個帶有邊框的區塊日誌。
        :param title: 區塊標題
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
        記錄一個 ASCII 標題日誌。
        :param text: 標題文字
        :param font: 字體樣式，預設為 "standard"
        :param log_level: 日誌級別，預設為 "INFO"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param to_console_only: 是否僅輸出到控制台，預設為 False
        :param to_log_file_only: 是否僅輸出到日誌檔案，預設為 False
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
    ) -> None:
        """
        記錄一個帶有 ASCII 標題的區塊日誌。
        :param title: 區塊標題
        :param message_list: 區塊內的訊息列表
        :param ascii_header: 可選的 ASCII 標題
        :param ascii_font: ASCII 標題的字體樣式，預設為 "standard"
        :param border_style: 邊框樣式，預設為 "cyan"
        :param log_level: 日誌級別，預設為 "INFO"
        """
        ...

    def is_ascii_only(self, text: str) -> bool:
        """
        檢查文字是否僅包含 ASCII 字元。
        :param text: 要檢查的文字
        :return: 如果僅包含 ASCII 字元則返回 True，否則返回 False
        """
        ...
        
    # 控制台專用方法
    def console(self, level: str, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的日誌記錄方法。
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def console_debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的調試級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def console_info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的資訊級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def console_success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的成功級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def console_warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的警告級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def console_error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的錯誤級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def console_critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅在控制台顯示的嚴重錯誤級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    # 文件專用方法
    def file(self, level: str, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的日誌記錄方法。
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def file_debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的調試級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def file_info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的資訊級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def file_success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的成功級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def file_warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的警告級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def file_error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的錯誤級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def file_critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        僅寫入文件的嚴重錯誤級別日誌。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    # 開發模式方法 (僅控制台)
    def dev(self, level: str, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式日誌記錄方法，僅在控制台顯示。
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def dev_debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式調試級別日誌，僅在控制台顯示。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def dev_info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式資訊級別日誌，僅在控制台顯示。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def dev_success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式成功級別日誌，僅在控制台顯示。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def dev_warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式警告級別日誌，僅在控制台顯示。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def dev_error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式錯誤級別日誌，僅在控制台顯示。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
        
    def dev_critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        開發模式嚴重錯誤級別日誌，僅在控制台顯示。
        :param message: 日誌訊息
        :param args: 其他參數
        :param kwargs: 關鍵字參數
        """
        ...
    
    # 核心方法
    def bind(self, **kwargs) -> 'EnhancedLoggerProtocol':
        """
        創建一個綁定上下文的 logger 實例
        :param kwargs: 要綁定的上下文資訊
        :return: 綁定後的 logger 實例
        """
        ...
    
    def opt(self, **kwargs) -> 'EnhancedLoggerProtocol':
        """
        創建一個具有特定選項的 logger 實例
        :param kwargs: 要設置的選項
        :return: 選項設置後的 logger 實例
        """
        ...
    
    def log(self, level, message, *args, **kwargs) -> None:
        """
        記錄特定級別的日誌
        :param level: 日誌級別
        :param message: 日誌訊息
        :param args: 其他位置參數
        :param kwargs: 其他關鍵字參數
        """
        ...
    
    def patch(self, patcher) -> 'EnhancedLoggerProtocol':
        """
        創建一個使用指定修補器的 logger 實例
        :param patcher: 日誌修補器函數
        :return: 修補後的 logger 實例
        """
        ...
    
    def level(self, name) -> Any:
        """
        獲取指定名稱的日誌級別
        :param name: 日誌級別名稱
        :return: 日誌級別
        """
        ...
    
    def configure(self, **kwargs) -> None:
        """
        配置 logger 實例
        :param kwargs: 配置參數
        """
        ...
    
    def add(self, sink, **kwargs) -> int:
        """
        添加日誌處理器
        :param sink: 處理器對象
        :param kwargs: 其他設置
        :return: 處理器 ID
        """
        ...
    
    def remove(self, handler_id=None) -> None:
        """
        移除日誌處理器
        :param handler_id: 處理器 ID
        """
        ...


# 類型別名
EnhancedLogger = EnhancedLoggerProtocol