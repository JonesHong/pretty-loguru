"""
這是一個類型存根文件 (.pyi)，用於提供精確的類型標註
IDE 會優先參考這個文件進行類型檢查和自動完成提示
"""
from typing import Any, Callable, Dict, List, Optional, Union, overload
import loguru

class EnhancedLogger(loguru._logger.Logger):
    """擴展 loguru 的內部 Logger 類，添加自定義方法的類型提示"""
    
    def block(
        self,
        title: str,
        message_list: List[str],
        border_style: str = ...,
        log_level: str = ...,
    ) -> None: ...
    
    def ascii_header(
        self,
        text: str,
        font: str = ...,
        log_level: str = ...,
        border_style: str = ...,
        to_console_only: bool = ...,
        to_log_file_only: bool = ...,
    ) -> None: ...
    
    def ascii_block(
        self,
        title: str,
        message_list: List[str],
        ascii_header: Optional[str] = ...,
        ascii_font: str = ...,
        border_style: str = ...,
        log_level: str = ...,
    ) -> None: ...
    
    def is_ascii_only(self, text: str) -> bool: ...

# 導出的主要 logger 對象
logger: EnhancedLogger

def print_block(
    title: str,
    message_list: List[str],
    border_style: str = ...,
    log_level: str = ...,
) -> None: ...

def print_ascii_header(
    text: str,
    font: str = ...,
    log_level: str = ...,
    border_style: str = ...,
    to_console_only: bool = ...,
    to_log_file_only: bool = ...,
) -> None: ...

def print_ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = ...,
    ascii_font: str = ...,
    border_style: str = ...,
    log_level: str = ...,
) -> None: ...

def is_ascii_only(text: str) -> bool: ...

def logger_start(file: Optional[str] = None, folder: Optional[str] = None) -> str: ...

def uvicorn_init_config() -> None: ...

log_path: str