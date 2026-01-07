"""
Rich 組件集成模組

此模組提供 Rich 庫的常用組件與 pretty-loguru 的集成，包括：
- Progress: 進度條顯示
- Table: 表格顯示
- Tree: 樹狀結構顯示  
- Columns: 分欄顯示

設計原則：
- KISS: 保持簡潔易用
- 整合而非取代：充分利用 Rich 的強大功能
- 一致性：與現有 block、ascii 等方法保持一致的 API
"""

import time
from typing import List, Dict, Any, Optional, Union, Callable, Tuple, Literal
from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from ..core.base import get_console
from rich.tree import Tree
from rich.columns import Columns
from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeElapsedColumn
from rich.text import Text
from rich.syntax import Syntax
from rich.panel import Panel
from rich import box as rich_box
from rich.align import Align

from ..types import PrettyLogger
from ..core.target_formatter import ensure_target_parameters
from ..core.pretty_event import PRETTY_VERSION_V1, build_renderable, render_renderable_to_text


@ensure_target_parameters
def print_renderable(
    renderable: Any,
    title: Optional[str] = None,
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    顯示任意 Rich renderable，並以「單 event」方式記錄到 console/file。

    這個入口用於「原生物件優先」的進階使用情境：使用者自行建立 Rich 的 Table/Tree/Panel/...，
    pretty-loguru 只負責把同一份輸出在 console/file 呈現一致。
    """
    if console is None:
        console = get_console()

    if logger_instance is None:
        return

    text = render_renderable_to_text(renderable)
    payload = {
        "title": title,
        "text": text,
    }
    pretty_text = "\n" + text + "\n"

    display_title = title or "Renderable"
    bind_kwargs = {
        "pretty_kind": "renderable",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Renderable: {display_title}")


@ensure_target_parameters
def print_table(
    title: str,
    data: List[Dict[str, Any]],
    headers: Optional[List[str]] = None,
    show_header: bool = True,
    show_lines: bool = False,
    style: str = "none",
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    創建並顯示 Rich 表格，同時記錄到日誌
    
    Args:
        title: 表格標題
        data: 表格數據，列表中每個字典代表一行
        headers: 可選的列標題，如果不提供則使用數據的鍵
        show_header: 是否顯示表頭
        show_lines: 是否顯示行分隔線
        style: Rich Table 的 style（例如 "blue"）
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> data = [
        ...     {"name": "Alice", "age": 30, "city": "NYC"},
        ...     {"name": "Bob", "age": 25, "city": "LA"}
        ... ]
        >>> print_table("Users", data)
    """
    if console is None:
        console = get_console()
    
    if not data:
        if logger_instance:
            logger_instance.warning(f"Table '{title}' has no data to display")
        return
    
    column_names = [str(x) for x in (headers or list(data[0].keys()))]
    rows = [{str(col): str(row.get(col, "")) for col in column_names} for row in data]

    if logger_instance is None:
        return

    payload = {
        "title": title,
        "headers": column_names,
        "rows": rows,
        "show_header": show_header,
        "show_lines": show_lines,
        "style": style,
    }
    renderable = build_renderable("table", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "table",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Table: {title}")


@ensure_target_parameters  
def print_tree(
    title: str,
    tree_data: Dict[str, Any],
    style: str = "tree",
    guide_style: str = "tree.line",
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    創建並顯示 Rich 樹狀結構
    
    Args:
        title: 樹的根節點標題
        tree_data: 樹狀數據結構，字典的值可以是字符串或嵌套字典
        style: Rich Tree 的 style（例如 "green"）
        guide_style: Rich Tree 的 guide_style（例如 "tree.line"）
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> tree_data = {
        ...     "Services": {
        ...         "Web": "Running",
        ...         "Database": "Running", 
        ...         "Cache": "Warning"
        ...     }
        ... }
        >>> print_tree("System Status", tree_data)
    """
    if console is None:
        console = get_console()
    
    if logger_instance is None:
        return

    payload = {
        "title": title,
        "data": tree_data,
        "style": style,
        "guide_style": guide_style,
    }
    renderable = build_renderable("tree", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "tree",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Tree: {title}")


@ensure_target_parameters
def print_columns(
    title: str,
    items: List[str],
    padding: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int, int]] = (0, 1),
    width: Optional[int] = None,
    expand: bool = False,
    equal: bool = False,
    column_first: bool = False,
    right_to_left: bool = False,
    align: Optional[Literal["left", "center", "right"]] = None,
    level: str = "INFO", 
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    以分欄格式顯示項目列表
    
    Args:
        title: 分欄顯示的標題
        items: 要顯示的項目列表
        padding: Rich Columns 的 padding
        width: Rich Columns 的 width
        expand: Rich Columns 的 expand
        equal: Rich Columns 的 equal
        column_first: Rich Columns 的 column_first
        right_to_left: Rich Columns 的 right_to_left
        align: Rich Columns 的 align（"left"/"center"/"right"）
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        >>> print_columns("Available Options", items, padding=(0, 2))
    """
    if console is None:
        console = get_console()
    
    if not items:
        if logger_instance:
            logger_instance.warning(f"Column display '{title}' has no items")
        return
    
    if logger_instance is None:
        return

    payload = {
        "title": title,
        "items": [str(x) for x in items],
        "padding": padding,
        "width": width,
        "expand": expand,
        "equal": equal,
        "column_first": column_first,
        "right_to_left": right_to_left,
        "align": align,
    }
    renderable = build_renderable("columns", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "columns",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Columns: {title}")


class LoggerProgress:
    """
    與 logger 集成的進度條類
    
    這個類包裝了 Rich Progress，並與 pretty-loguru 的日誌系統集成
    """
    
    def __init__(
        self, 
        logger_instance: Any,
        console: Optional[Console] = None,
        log_start: bool = True,
        log_complete: bool = True
    ):
        """
        建立與 logger 綁定的 progress helper。

        Args:
            logger_instance: pretty-loguru logger（用於記錄 start/complete 訊息）。
            console: Rich Console（預設會建立新的 Console）。
            log_start: 是否在開始時記錄一筆 info。
            log_complete: 是否在結束時記錄一筆 success。
        """
        self.logger = logger_instance
        self.console = console or Console()
        self.log_start = log_start
        self.log_complete = log_complete
        self.progress = None
        self.tasks = {}
    
    @contextmanager
    def progress_context(self, description: str = "Processing", total: int = 100):
        """
        進度條上下文管理器
        
        Args:
            description: 進度條描述
            total: 總步數
            
        Yields:
            function: 更新進度的函數
            
        Example:
            >>> with logger.progress_context("Loading data", 100) as update:
            ...     for i in range(100):
            ...         # 做一些工作
            ...         time.sleep(0.01)
            ...         update(1)  # 增加 1 步
        """
        if self.log_start:
            self.logger.info(f"Starting progress: {description}")
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task_id = progress.add_task(description, total=total)
            
            def update_progress(advance: int = 1):
                progress.update(task_id, advance=advance)
            
            try:
                yield update_progress
            finally:
                if self.log_complete:
                    self.logger.success(f"Completed progress: {description}")
    
    def track_list(
        self, 
        items: List[Any], 
        description: str = "Processing items"
    ) -> List[Any]:
        """
        跟蹤列表處理進度
        
        Args:
            items: 要處理的項目列表
            description: 進度描述
            
        Returns:
            與輸入相同的列表，但會顯示進度
            
        Example:
            >>> items = [1, 2, 3, 4, 5]
            >>> for item in logger.track_list(items, "Processing numbers"):
            ...     # 處理每個項目
            ...     time.sleep(0.1)
        """
        if self.log_start:
            self.logger.info(f"Tracking progress: {description} ({len(items)} items)")
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task_id = progress.add_task(description, total=len(items))
            
            for item in items:
                yield item
                progress.update(task_id, advance=1)
        
        if self.log_complete:
            self.logger.success(f"Completed tracking: {description}")


@ensure_target_parameters
def print_code(
    code: str,
    language: str = "python",
    theme: str = "monokai",
    line_numbers: bool = True,
    word_wrap: bool = False,
    indent_guides: bool = True,
    title: Optional[str] = None,
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    顯示語法高亮的程式碼
    
    Args:
        code: 要顯示的程式碼字符串
        language: 程式語言 (python, javascript, html, css, json, sql, etc.)
        theme: 語法高亮主題 (monokai, github-dark, one-dark, etc.)
        line_numbers: 是否顯示行號
        word_wrap: 是否自動換行
        indent_guides: 是否顯示縮排引導線
        title: 可選的程式碼標題
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> code = '''
        ... def hello_world():
        ...     print("Hello, World!")
        ...     return True
        ... '''
        >>> print_code(code, language="python", title="Hello World Example")
    """
    if console is None:
        console = get_console()
    
    if not code.strip():
        if logger_instance:
            logger_instance.warning("Code block is empty")
        return
    
    if logger_instance is None:
        return

    payload = {
        "title": title,
        "code": code,
        "language": language,
        "theme": theme,
        "line_numbers": line_numbers,
        "word_wrap": word_wrap,
        "indent_guides": indent_guides,
    }
    renderable = build_renderable("code", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    display_title = title or f"({str(language).upper()})"
    bind_kwargs = {
        "pretty_kind": "code",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Code: {display_title}")


@ensure_target_parameters
def print_code_from_file(
    file_path: str,
    language: Optional[str] = None,
    theme: str = "monokai",
    line_numbers: bool = True,
    word_wrap: bool = False,
    indent_guides: bool = True,
    start_line: Optional[int] = None,
    end_line: Optional[int] = None,
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    從文件讀取並顯示語法高亮的程式碼
    
    Args:
        file_path: 文件路徑
        language: 程式語言，如果不提供則嘗試從文件擴展名推斷
        theme: 語法高亮主題
        line_numbers: 是否顯示行號
        word_wrap: 是否自動換行
        indent_guides: 是否顯示縮排引導線
        start_line: 開始行號 (1-based)
        end_line: 結束行號 (1-based)
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> print_code_from_file("example.py", start_line=10, end_line=20)
    """
    import os
    
    if console is None:
        console = get_console()
    
    if not os.path.exists(file_path):
        if logger_instance:
            logger_instance.error(f"File not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 處理行號範圍
        if start_line is not None:
            start_idx = max(0, start_line - 1)
        else:
            start_idx = 0
            
        if end_line is not None:
            end_idx = min(len(lines), end_line)
        else:
            end_idx = len(lines)
        
        code = ''.join(lines[start_idx:end_idx])
        
        # 自動推斷語言
        if language is None:
            ext = os.path.splitext(file_path)[1].lower()
            language_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.ts': 'typescript',
                '.html': 'html',
                '.css': 'css',
                '.json': 'json',
                '.sql': 'sql',
                '.md': 'markdown',
                '.yaml': 'yaml',
                '.yml': 'yaml',
                '.xml': 'xml',
                '.sh': 'bash',
                '.cpp': 'cpp',
                '.c': 'c',
                '.java': 'java',
                '.go': 'go',
                '.rs': 'rust',
                '.php': 'php',
                '.rb': 'ruby'
            }
            language = language_map.get(ext, 'text')
        
        # 構建標題
        range_info = ""
        if start_line is not None or end_line is not None:
            range_info = f" (lines {start_line or 1}-{end_line or len(lines)})"
        title = f"{os.path.basename(file_path)}{range_info}"
        
        print_code(
            code=code,
            language=language,
            theme=theme,
            line_numbers=line_numbers,
            word_wrap=word_wrap,
            indent_guides=indent_guides,
            title=title,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
        
    except Exception as e:
        if logger_instance:
            logger_instance.error(f"Error reading file {file_path}: {str(e)}")


@ensure_target_parameters
def print_diff(
    old_code: str,
    new_code: str,
    old_title: str = "Before",
    new_title: str = "After",
    language: str = "python",
    theme: str = "monokai",
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    並排顯示程式碼差異對比，使用紅色（舊版本）和綠色（新版本）視覺區分
    
    Args:
        old_code: 舊版本程式碼
        new_code: 新版本程式碼
        old_title: 舊版本標題
        new_title: 新版本標題
        language: 程式語言
        theme: 語法高亮主題
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> old = "def hello():\n    print('Hi')"
        >>> new = "def hello():\n    print('Hello, World!')"
        >>> print_diff(old, new)
    """
    if console is None:
        console = get_console()
    
    if logger_instance is None:
        return

    payload = {
        "old_title": old_title,
        "new_title": new_title,
        "old_code": old_code,
        "new_code": new_code,
        "language": language,
        "theme": theme,
    }
    renderable = build_renderable("diff", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    bind_kwargs = {
        "pretty_kind": "diff",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Code Diff: {old_title} → {new_title}")


@ensure_target_parameters
def print_panel(
    content: Union[str, Any],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    border_style: str = "cyan",
    box_style: Optional[str] = None,
    title_align: str = "left",
    subtitle_align: str = "right", 
    width: Optional[int] = None,
    height: Optional[int] = None,
    padding: Union[int, tuple] = 1,
    expand: bool = True,
    level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_file_only: bool = False,
    _target_depth: int = None,
) -> None:
    """
    顯示 Rich Panel（面板），這是 block 方法的原生 Rich 版本
    
    這個函數展示了如何直接使用 Rich Panel API，提供了更多的自定義選項。
    相比於 logger.block() 方法，這個函數支援更多 Rich Panel 的原生功能。
    
    Args:
        content: 面板內容，可以是字符串或任何 Rich 可渲染對象
        title: 面板標題
        subtitle: 面板副標題
        border_style: 邊框顏色樣式 (如 "cyan", "red", "green" 等)
        box_style: 邊框樣式名稱 (如 "rounded", "double", "heavy" 等)
        title_align: 標題對齊方式 ("left", "center", "right")
        subtitle_align: 副標題對齊方式 ("left", "center", "right")
        width: 面板寬度，None 表示自動
        height: 面板高度，None 表示自動
        padding: 內邊距，可以是整數或 (top, right, bottom, left) 元組
        expand: 是否擴展到可用寬度
        level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_file_only: 僅輸出到文件
        _target_depth: 調用深度
        
    Example:
        >>> # 基本使用
        >>> print_panel("Hello, World!", title="Welcome")
        
        >>> # 使用不同的邊框樣式
        >>> print_panel("Important Message", title="Notice", 
        ...            border_style="red", box_style="double")
        
        >>> # 使用副標題和對齊
        >>> print_panel("System Status: OK", 
        ...            title="Status", subtitle="Last updated: 12:00",
        ...            title_align="center", subtitle_align="center")
        
        >>> # 自定義尺寸和內邊距
        >>> print_panel("Compact info", width=40, height=5, padding=0)
        
        >>> # 使用 Rich 對象作為內容
        >>> from rich.table import Table
        >>> table = Table(title="Data")
        >>> table.add_column("Name")
        >>> table.add_column("Value")
        >>> table.add_row("CPU", "45%")
        >>> table.add_row("Memory", "2.3GB")
        >>> print_panel(table, title="System Resources")
    """
    if console is None:
        console = get_console()
    
    if logger_instance is None:
        return

    content_text: str
    if isinstance(content, str):
        content_text = content
    else:
        content_text = render_renderable_to_text(content)

    payload = {
        "content": content_text,
        "title": title,
        "subtitle": subtitle,
        "border_style": border_style,
        "box_style": box_style,
        "title_align": title_align,
        "subtitle_align": subtitle_align,
        "width": width,
        "height": height,
        "padding": padding,
        "expand": expand,
    }
    renderable = build_renderable("panel", payload)
    pretty_text = "\n" + render_renderable_to_text(renderable) + "\n"

    display_title = title or "Panel"
    bind_kwargs = {
        "pretty_kind": "panel",
        "pretty_version": PRETTY_VERSION_V1,
        "pretty_payload": payload,
        "pretty_text": pretty_text,
    }
    if to_console_only:
        bind_kwargs["to_console_only"] = True
    if to_file_only:
        bind_kwargs["to_file_only"] = True

    logger_instance.opt(colors=True, depth=_target_depth).bind(**bind_kwargs).log(level, f"Panel: {display_title}")


def create_rich_methods(logger_instance: Any, console: Optional[Console] = None) -> None:
    """
    為 logger 實例創建 Rich 組件方法
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        console: 要使用的 Rich console 實例
    """
    if console is None:
        console = get_console()
    
    # 1. 表格方法
    @ensure_target_parameters
    def table_method(
        title: str,
        data: List[Dict[str, Any]],
        headers: Optional[List[str]] = None,
        show_header: bool = True,
        show_lines: bool = False,
        style: str = "none",
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_table(
            title=title,
            data=data,
            headers=headers,
            show_header=show_header,
            show_lines=show_lines,
            style=style,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 2. 樹狀結構方法
    @ensure_target_parameters  
    def tree_method(
        title: str,
        tree_data: Dict[str, Any],
        style: str = "tree",
        guide_style: str = "tree.line",
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_tree(
            title=title,
            tree_data=tree_data,
            style=style,
            guide_style=guide_style,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 3. 分欄顯示方法
    @ensure_target_parameters
    def columns_method(
        title: str,
        items: List[str],
        padding: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int, int]] = (0, 1),
        width: Optional[int] = None,
        expand: bool = False,
        equal: bool = False,
        column_first: bool = False,
        right_to_left: bool = False,
        align: Optional[Literal["left", "center", "right"]] = None,
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_columns(
            title=title,
            items=items,
            padding=padding,
            width=width,
            expand=expand,
            equal=equal,
            column_first=column_first,
            right_to_left=right_to_left,
            align=align,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 4. 程式碼高亮方法
    @ensure_target_parameters
    def code_method(
        code: str,
        language: str = "python",
        theme: str = "monokai",
        line_numbers: bool = True,
        word_wrap: bool = False,
        indent_guides: bool = True,
        title: Optional[str] = None,
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_code(
            code=code,
            language=language,
            theme=theme,
            line_numbers=line_numbers,
            word_wrap=word_wrap,
            indent_guides=indent_guides,
            title=title,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 5. 從文件讀取程式碼方法
    @ensure_target_parameters
    def code_file_method(
        file_path: str,
        language: Optional[str] = None,
        theme: str = "monokai",
        line_numbers: bool = True,
        word_wrap: bool = False,
        indent_guides: bool = True,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_code_from_file(
            file_path=file_path,
            language=language,
            theme=theme,
            line_numbers=line_numbers,
            word_wrap=word_wrap,
            indent_guides=indent_guides,
            start_line=start_line,
            end_line=end_line,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 6. 程式碼差異對比方法
    @ensure_target_parameters
    def diff_method(
        old_code: str,
        new_code: str,
        old_title: str = "Before",
        new_title: str = "After",
        language: str = "python",
        theme: str = "monokai",
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_diff(
            old_code=old_code,
            new_code=new_code,
            old_title=old_title,
            new_title=new_title,
            language=language,
            theme=theme,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 7. Panel 方法（Rich 原生版本）
    @ensure_target_parameters
    def panel_method(
        content: Union[str, Any],
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        border_style: str = "cyan",
        box_style: Optional[str] = None,
        title_align: str = "left",
        subtitle_align: str = "right",
        width: Optional[int] = None,
        height: Optional[int] = None,
        padding: Union[int, tuple] = 1,
        expand: bool = True,
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_panel(
            content=content,
            title=title,
            subtitle=subtitle,
            border_style=border_style,
            box_style=box_style,
            title_align=title_align,
            subtitle_align=subtitle_align,
            width=width,
            height=height,
            padding=padding,
            expand=expand,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )

    # 8. 原生 renderable（Table/Tree/Panel/...）入口
    @ensure_target_parameters
    def render_method(
        renderable: Any,
        title: Optional[str] = None,
        level: str = "INFO",
        to_console_only: bool = False,
        to_file_only: bool = False,
        _target_depth: int = None,
    ) -> None:
        print_renderable(
            renderable=renderable,
            title=title,
            level=level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_file_only=to_file_only,
            _target_depth=_target_depth,
        )
    
    # 8. 進度條方法（作為屬性）
    def get_progress():
        return LoggerProgress(logger_instance, console)
    
    # 將方法添加到 logger 實例
    logger_instance.table = table_method
    logger_instance.tree = tree_method  
    logger_instance.columns = columns_method
    logger_instance.code = code_method
    logger_instance.code_file = code_file_method
    logger_instance.diff = diff_method
    logger_instance.panel = panel_method  # 新增 panel 方法
    logger_instance.progress = get_progress()
    logger_instance.render = render_method
    
    # 不再注入 console_*/file_* 目標方法：統一走單一路徑（loguru pipeline）


# 導出的函數和類
__all__ = [
    'print_table',
    'print_tree', 
    'print_columns',
    'print_code',
    'print_code_from_file',
    'print_diff',
    'print_panel',
    'print_renderable',
    'LoggerProgress',
    'create_rich_methods'
]
