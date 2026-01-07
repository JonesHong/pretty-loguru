"""
ASCII 藝術模組

此模組提供用於生成 ASCII 藝術標題和區塊的功能，
增強日誌的視覺效果和結構化呈現。
"""

import warnings
from functools import lru_cache
from typing import List, Optional, Any, Union

from rich.panel import Panel
from rich.console import Console

from pretty_loguru.core.extension_system import register_extension_method
from pretty_loguru.core.base import get_console
from pretty_loguru.utils.dependencies import ensure_art_dependency
from pretty_loguru.utils.warn_once import warn_once
from pretty_loguru.utils.validators import validate_ascii_art_text, validate_ascii_header

try:
    from art import text2art
    _has_art = True
except ImportError:
    _has_art = False
    # 定義一個空的 text2art 函數，避免引用錯誤
    def text2art(text, **kwargs):
        """`art.text2art` 的 fallback：在未安裝 `art` 時回傳提示字串。"""
        warn_once("art library not installed; returning placeholder text.", ImportWarning, key="art_missing")
        return f"[Art library not installed: {text}]"


@lru_cache(maxsize=256)
def _cached_text2art(text: str, font: str) -> str:
    return text2art(text, font=font)

from ..types import PrettyLogger
from ..core.target_formatter import ensure_target_parameters
from ..core.pretty_event import PRETTY_VERSION_V1, build_renderable, render_renderable_to_text
from .block import print_block, format_block_message


# ASCII 字符檢查現在統一在 utils.validators 中處理





@ensure_target_parameters
def print_ascii_header(
    text: str,
    font: str = "standard",
    level: str = "INFO",
    border_style: str = "cyan",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
    strict: bool = False,
) -> None:
    """
    打印 ASCII 藝術標題
    
    Args:
        text: 要轉換為 ASCII 藝術的文本
        font: ASCII 藝術字體
        level: 日誌級別
        border_style: 邊框樣式
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
        ImportError: 如果未安裝 art 庫
    """
    # 檢查 art 庫是否已安裝
    try:
        ensure_art_dependency(logger_instance)
    except ImportError as e:
        warnings.warn(str(e), ImportWarning)
        return
    
    # 如果沒有提供 console，則使用統一的 console 實例
    if console is None:
        console = get_console()
    
    # 檢查並清理 ASCII 字符
    text = validate_ascii_art_text(text, logger_instance)
    
    # 使用 art 庫生成 ASCII 藝術
    try:
        ascii_art = _cached_text2art(text, font)
    except Exception as e:
        error_msg = f"Failed to generate ASCII art: {str(e)}"
        if strict:
            raise
        warn_once(error_msg, UserWarning, key=("ascii_header", font, text))
        if logger_instance:
            logger_instance.error(error_msg)
        return
    
    # 創建一個帶有邊框的 Panel
    panel = Panel(
        ascii_art,
        border_style=border_style,
    )
    
    # 若沒有 logger_instance，保留純輸出模式（不走 loguru pipeline）
    if logger_instance is None:
        if not to_file_only:
            console.print(panel)
        return

    payload = {
        "text": text,
        "font": font,
        "art": ascii_art,
        "border_style": border_style,
    }
    renderable = build_renderable("ascii_header", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "ascii_header",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"ASCIIHeader: {text}")


@ensure_target_parameters
def print_ascii_block(
    title: str,
    lines: Union[str, List[str]],
    header_text: Optional[str] = None,
    font: str = "standard",
    border_style: str = "cyan",
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
    strict: bool = False,
) -> None:
    """
    打印帶有 ASCII 藝術標題的區塊樣式日誌
    
    Args:
        title: 區塊的標題
        lines: 日誌的內容（可為單行字串或多行列表）
        header_text: ASCII 藝術標題文本 (如果不提供，則使用 title)
        font: ASCII 藝術字體
        border_style: 區塊邊框顏色
        level: 日誌級別
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果 ASCII 標題包含非 ASCII 字符
        ImportError: 如果未安裝 art 庫
    """
    # 檢查 art 庫是否已安裝
    try:
        ensure_art_dependency(logger_instance)
    except ImportError as e:
        warnings.warn(str(e), ImportWarning)
        return
    
    # 如果沒有提供 console，則使用統一的 console 實例
    if console is None:
        console = get_console()
    
    # 如果沒有提供 ASCII 標題，則使用普通標題
    final_header_text = header_text if header_text is not None else title
    
    # 檢查並清理 ASCII 字符
    final_header_text = validate_ascii_header(final_header_text, logger_instance)
    
    # 生成 ASCII 藝術
    try:
        ascii_art = _cached_text2art(final_header_text, font)
    except Exception as e:
        error_msg = f"Failed to generate ASCII art: {str(e)}"
        if strict:
            raise
        warn_once(error_msg, UserWarning, key=("ascii_block", font, final_header_text))
        if logger_instance:
            logger_instance.error(error_msg)
        return
    
    if isinstance(lines, str):
        normalized_lines = [lines]
    else:
        normalized_lines = [str(x) for x in lines]

    full_message_list = [ascii_art] + normalized_lines
    
    # 構造區塊內容，將多行訊息合併為單一字串
    message = "\n".join(full_message_list)
    panel = Panel(
        message,
        title=title,  # 設定區塊標題
        title_align="left",  # 標題靠左對齊
        border_style=border_style,  # 設定邊框樣式
    )

    if logger_instance is None:
        return

    payload = {
        "title": title,
        "lines": [str(x) for x in full_message_list],
        "border_style": border_style,
    }
    renderable = build_renderable("ascii_block", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "ascii_block",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"CustomBlock: {title}")



def create_ascii_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例創建 ASCII 藝術相關方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 rich console 實例，如果為 None 則使用新創建的
    """
    if console is None:
        console = get_console()
   
    # 定義 ascii_header 的實現
    @ensure_target_parameters
    def _ascii_header_impl(
        self,
        text: str,
        font: str = "standard",
        level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_ascii_header(text, font=font, level=level, border_style=border_style,
                           logger_instance=self, console=console,
                           to_console_only=to_console_only, to_file_only=to_file_only,
                           _target_depth=_target_depth)

    # 定義 ascii_block 的實現
    @ensure_target_parameters
    def _ascii_block_impl(
        self,
        title: str,
        lines: Union[str, List[str]],
        header_text: Optional[str] = None,
        font: str = "standard",
        border_style: str = "cyan",
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_ascii_block(title, lines, header_text=header_text, font=font,
                          border_style=border_style, level=level,
                          logger_instance=self, console=console,
                          to_console_only=to_console_only, to_file_only=to_file_only,
                          _target_depth=_target_depth)

    # 註冊方法
    register_extension_method(logger_instance, "ascii_header", _ascii_header_impl, overwrite=True)
    register_extension_method(logger_instance, "ascii_block", _ascii_block_impl, overwrite=True)
