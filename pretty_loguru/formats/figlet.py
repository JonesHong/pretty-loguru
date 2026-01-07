"""
FIGlet 藝術模組

此模組提供用於生成 FIGlet 文本藝術的功能，
是 ASCII 藝術的替代選項，支援更多的字體和樣式。
需要安裝 pyfiglet 庫：pip install pyfiglet
"""

import re
from typing import List, Optional, Any, Set, Union

from rich.panel import Panel
from rich.console import Console
from pretty_loguru.core.base import get_console
from pretty_loguru.utils.dependencies import ensure_pyfiglet_dependency, warn_missing_dependency

import warnings
from functools import lru_cache

from pretty_loguru.utils.warn_once import warn_once
from ..types import PrettyLogger
from ..core.target_formatter import ensure_target_parameters
from ..core.pretty_event import PRETTY_VERSION_V1, build_renderable, render_renderable_to_text
from .block import print_block
from ..utils.validators import is_ascii_only


@ensure_target_parameters
def print_figlet_header(
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
    打印 FIGlet 藝術標題
    
    Args:
        text: 要轉換為 FIGlet 藝術的文本
        font: FIGlet 藝術字體
        level: 日誌級別
        border_style: 邊框樣式
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果文本包含非 ASCII 字符
        ImportError: 如果未安裝 pyfiglet 庫
    """
    if not _require_pyfiglet(logger_instance):
        return
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = get_console()
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(text):
        warning_msg = f"FIGlet only supports ASCII characters. The text '{text}' contains non-ASCII characters."
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        if logger_instance:
            logger_instance.warning(f"Non-ASCII characters have been removed. Using: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("The text contains only non-ASCII characters and cannot create FIGlet art.")
        
        text = cleaned_text
    
    # 使用 pyfiglet 生成 FIGlet 藝術
    try:
        figlet_art = _cached_figlet_format(text, font)
    except Exception as e:
        error_msg = f"Failed to generate FIGlet art: {str(e)}"
        if strict:
            raise
        warn_once(error_msg, UserWarning, key=("figlet_header", font, text))
        if logger_instance:
            logger_instance.error(error_msg)
        return
    
    # 創建一個帶有邊框的 Panel
    panel = Panel(
        figlet_art,
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
        "art": figlet_art,
        "border_style": border_style,
    }
    renderable = build_renderable("figlet_header", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "figlet_header",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"FIGletHeader: {text}")


@ensure_target_parameters
def print_figlet_block(
    title: str,
    lines: Union[str, List[str]],
    figlet_header: Optional[str] = None,
    figlet_font: str = "standard",
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
    打印帶有 FIGlet 藝術標題的區塊樣式日誌
    
    Args:
        title: 區塊的標題
        lines: 日誌的內容（可為單行字串或多行列表）
        figlet_header: FIGlet 藝術標題文本 (如果不提供，則使用 title)
        figlet_font: FIGlet 藝術字體
        border_style: 區塊邊框顏色
        level: 日誌級別
        logger_instance: 要使用的 logger 實例，如果為 None 則不記錄日誌
        console: 要使用的 rich console 實例，如果為 None 則創建新的
        to_console_only: 是否僅輸出到控制台，預設為 False
        to_file_only: 是否僅輸出到日誌文件，預設為 False
        _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        
    Raises:
        ValueError: 如果 FIGlet 標題包含非 ASCII 字符
        ImportError: 如果未安裝 pyfiglet 庫
    """
    if not _require_pyfiglet(logger_instance):
        return
    
    # 如果沒有提供 console，則創建一個新的
    if console is None:
        console = get_console()
    
    # 如果沒有提供 FIGlet 標題，則使用普通標題
    header_text = figlet_header if figlet_header is not None else title
    
    # 檢查是否包含非 ASCII 字符
    if not is_ascii_only(header_text):
        warning_msg = f"FIGlet only supports ASCII characters. The text '{header_text}' contains non-ASCII characters."
        if logger_instance:
            logger_instance.warning(warning_msg)
        
        # 移除非 ASCII 字符
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', header_text)
        
        if logger_instance:
            logger_instance.warning(f"Non-ASCII characters have been removed. Using: '{cleaned_text}'")
        
        if not cleaned_text:  # 如果移除後為空，則拋出異常
            raise ValueError("The FIGlet header contains only non-ASCII characters and cannot create FIGlet art.")
        
        header_text = cleaned_text
    
    # 生成 FIGlet 藝術
    try:
        figlet_art = _cached_figlet_format(header_text, figlet_font)
    except Exception as e:
        error_msg = f"Failed to generate FIGlet art: {str(e)}"
        if strict:
            raise
        warn_once(error_msg, UserWarning, key=("figlet_block", figlet_font, header_text))
        if logger_instance:
            logger_instance.error(error_msg)
        return
    
    if isinstance(lines, str):
        normalized_lines = [lines]
    else:
        normalized_lines = [str(x) for x in lines]

    full_message_list = [figlet_art] + normalized_lines
    
    # 構造區塊內容
    message = "\n".join(full_message_list)
    panel = Panel(
        message,
        title=title,
        title_align="left",
        border_style=border_style,
    )
    
    if logger_instance is None:
        return

    payload = {
        "title": title,
        "lines": [str(x) for x in full_message_list],
        "border_style": border_style,
    }
    renderable = build_renderable("figlet_block", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "figlet_block",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"CustomBlock: {title}")


def get_figlet_fonts() -> Set[str]:
    """
    獲取所有可用的 FIGlet 字體
    
    Returns:
        Set[str]: 可用字體名稱的集合
        
    Raises:
        ImportError: 如果未安裝 pyfiglet 庫
    """
    ensure_pyfiglet_dependency()
    
    return set(FigletFont.getFonts())


def create_figlet_methods(logger_instance: Any, console: Optional[Console] = None) -> bool:
    """
    為 logger 實例創建 FIGlet 藝術相關方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 rich console 實例，如果為 None 則使用新創建的
        
    Returns:
        bool: 如果成功添加方法則返回 True，否則返回 False
    """
    # 檢查 pyfiglet 庫是否已安裝
    global _has_pyfiglet
    if not _has_pyfiglet:
        return warn_missing_dependency("pyfiglet", logger_instance, False)
    
    if console is None:
        console = get_console()
    
    # 添加 figlet_header 方法
    @ensure_target_parameters
    def figlet_header_method(
        text: str,
        font: str = "standard",
        level: str = "INFO",
        border_style: str = "cyan",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        """
        logger 實例的 FIGlet 藝術標題方法
        
        Args:
            text: 要轉換為 FIGlet 藝術的文本
            font: FIGlet 藝術字體
            level: 日誌級別
            border_style: 邊框樣式
            to_console_only: 是否僅輸出到控制台，預設為 False
            to_file_only: 是否僅輸出到日誌文件，預設為 False
            _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        """
        # 直接傳遞明確參數
        print_figlet_header(
            text,
            font=font,
            level=level,
            border_style=border_style,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth
        )
    
    # 添加 figlet_block 方法
    @ensure_target_parameters
    def figlet_block_method(
        title: str,
        lines: Union[str, List[str]],
        figlet_header: Optional[str] = None,
        figlet_font: str = "standard",
        border_style: str = "cyan",
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        """
        logger 實例的 FIGlet 藝術區塊方法
        
        Args:
            title: 區塊的標題
            lines: 日誌的內容（可為單行字串或多行列表）
            figlet_header: FIGlet 藝術標題文本 (如果不提供，則使用 title)
            figlet_font: FIGlet 藝術字體
            border_style: 區塊邊框顏色
            level: 日誌級別
            to_console_only: 是否僅輸出到控制台，預設為 False
            to_file_only: 是否僅輸出到日誌文件，預設為 False
            _target_depth: 日誌堆棧深度，用於捕獲正確的調用位置
        """
        # 直接傳遞明確參數
        print_figlet_block(
            title,
            lines,
            figlet_header=figlet_header,
            figlet_font=figlet_font,
            border_style=border_style,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth
        )
    
    # 添加 get_figlet_fonts 方法
    def get_fonts_method() -> Set[str]:
        """
        獲取所有可用的 FIGlet 字體
        """
        return get_figlet_fonts()
    
    # 將方法添加到 logger 實例
    logger_instance.figlet_header = figlet_header_method
    logger_instance.figlet_block = figlet_block_method
    logger_instance.get_figlet_fonts = get_fonts_method
    
    # 不再注入 console_*/file_* 目標方法：統一走單一路徑（loguru pipeline）
    
    return True


# 狀態與 lazy 匯入
_has_pyfiglet: bool = False
pyfiglet = None  # type: ignore
FigletFont = None
_pyfiglet_module = None


def _lazy_pyfiglet():
    global _has_pyfiglet, _pyfiglet_module, pyfiglet, FigletFont
    if pyfiglet is not None:
        return pyfiglet
    if _pyfiglet_module is not None or _has_pyfiglet:
        return _pyfiglet_module
    try:
        import pyfiglet
        _pyfiglet_module = pyfiglet
        globals()["pyfiglet"] = pyfiglet
        globals()["FigletFont"] = getattr(pyfiglet, "FigletFont", None)
        _has_pyfiglet = True
    except ImportError:
        _pyfiglet_module = None
        _has_pyfiglet = False
    return _pyfiglet_module


_has_pyfiglet = _lazy_pyfiglet() is not None


@lru_cache(maxsize=256)
def _cached_figlet_format(text: str, font: str) -> str:
    mod = _lazy_pyfiglet()
    if mod is None:
        raise ImportError("pyfiglet not installed")
    return mod.figlet_format(text, font=font)


def _require_pyfiglet(logger_instance: Any = None) -> bool:
    mod = _lazy_pyfiglet()
    if mod is None:
        warn_once("pyfiglet not installed; figlet features disabled.", ImportWarning, key="pyfiglet_missing")
        return False
    try:
        ensure_pyfiglet_dependency(logger_instance)
        return True
    except ImportError as e:
        warn_once(str(e), ImportWarning, key="pyfiglet_missing")
        return False
