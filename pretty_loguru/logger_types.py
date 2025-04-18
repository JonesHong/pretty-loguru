"""
定義日誌系統的類型協議，用於提供 IDE 自動完成和類型檢查功能
(簡化版本，不使用繼承)
"""
from typing import List, Optional, Protocol, Any, Union, Callable, Dict, TypeVar, overload

# 定義一個簡單的 Protocol 來描述 logger 對象
class EnhancedLoggerProtocol(Protocol):
    """定義擴展的 logger 協議"""
    
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def success(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    
    def block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None: ...
    
    def ascii_header(
        self,
        text: str,
        font: str = "standard",
        log_level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
    ) -> None: ...
    
    def ascii_block(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = None,
        ascii_font: str = "standard",
        border_style: str = "cyan",
        log_level: str = "INFO",
    ) -> None: ...
    
    def is_ascii_only(self, text: str) -> bool: ...

# 簡化的類型別名
EnhancedLogger = EnhancedLoggerProtocol