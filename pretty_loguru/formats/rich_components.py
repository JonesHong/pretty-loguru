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
from typing import List, Dict, Any, Optional, Union, Callable
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

from ..types import EnhancedLogger
from ..core.target_formatter import add_target_methods, ensure_target_parameters


@ensure_target_parameters
def print_table(
    title: str,
    data: List[Dict[str, Any]],
    headers: Optional[List[str]] = None,
    show_header: bool = True,
    show_lines: bool = False,
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **table_kwargs
) -> None:
    """
    創建並顯示 Rich 表格，同時記錄到日誌
    
    Args:
        title: 表格標題
        data: 表格數據，列表中每個字典代表一行
        headers: 可選的列標題，如果不提供則使用數據的鍵
        show_header: 是否顯示表頭
        show_lines: 是否顯示行分隔線
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **table_kwargs: 傳遞給 Rich Table 的額外參數
        
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
    
    # 創建 Rich 表格
    table = Table(title=title, show_header=show_header, show_lines=show_lines, **table_kwargs)
    
    # 添加列
    column_names = headers or list(data[0].keys())
    for col_name in column_names:
        table.add_column(str(col_name), justify="left")
    
    # 添加行
    for row in data:
        table.add_row(*[str(row.get(col, "")) for col in column_names])
    
    # 輸出到控制台
    if not to_log_file_only and logger_instance:
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, f"Displaying table: {title}"
        )
        console.print(table)
    
    # 輸出到文件
    if not to_console_only and logger_instance:
        # 創建文本版本的表格
        table_text = f"Table: {title}\n"
        table_text += " | ".join(column_names) + "\n"
        table_text += "-" * (len(" | ".join(column_names))) + "\n"
        for row in data:
            table_text += " | ".join(str(row.get(col, "")) for col in column_names) + "\n"
        
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{table_text}"
        )


@ensure_target_parameters  
def print_tree(
    title: str,
    tree_data: Dict[str, Any],
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **tree_kwargs
) -> None:
    """
    創建並顯示 Rich 樹狀結構
    
    Args:
        title: 樹的根節點標題
        tree_data: 樹狀數據結構，字典的值可以是字符串或嵌套字典
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **tree_kwargs: 傳遞給 Rich Tree 的額外參數
        
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
    
    # 創建 Rich 樹
    tree = Tree(title, **tree_kwargs)
    
    def add_tree_nodes(parent_node, data):
        """遞歸添加樹節點"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    branch = parent_node.add(str(key))
                    add_tree_nodes(branch, value)
                else:
                    parent_node.add(f"{key}: {value}")
        else:
            parent_node.add(str(data))
    
    add_tree_nodes(tree, tree_data)
    
    # 輸出到控制台
    if not to_log_file_only and logger_instance:
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, f"Displaying tree: {title}"
        )
        console.print(tree)
    
    # 輸出到文件 
    if not to_console_only and logger_instance:
        # 創建文本版本的樹
        def format_tree_text(data, indent=0):
            lines = []
            prefix = "  " * indent
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        lines.append(f"{prefix}{key}:")
                        lines.extend(format_tree_text(value, indent + 1))
                    else:
                        lines.append(f"{prefix}{key}: {value}")
            return lines
        
        tree_text = f"Tree: {title}\n"
        tree_text += "\n".join(format_tree_text(tree_data))
        
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{tree_text}"
        )


@ensure_target_parameters
def print_columns(
    title: str,
    items: List[str],
    columns: int = 3,
    log_level: str = "INFO", 
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **columns_kwargs
) -> None:
    """
    以分欄格式顯示項目列表
    
    Args:
        title: 分欄顯示的標題
        items: 要顯示的項目列表
        columns: 欄數，默認 3 欄
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **columns_kwargs: 傳遞給 Rich Columns 的額外參數
        
    Example:
        >>> items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        >>> print_columns("Available Options", items, columns=2)
    """
    if console is None:
        console = get_console()
    
    if not items:
        if logger_instance:
            logger_instance.warning(f"Column display '{title}' has no items")
        return
    
    # 創建 Rich 分欄顯示
    rich_columns = Columns(items, **columns_kwargs)
    
    # 輸出到控制台
    if not to_log_file_only and logger_instance:
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, f"Displaying columns: {title}"
        )
        console.print(f"[bold]{title}[/bold]")
        console.print(rich_columns)
    
    # 輸出到文件
    if not to_console_only and logger_instance:
        # 創建文本版本的分欄
        columns_text = f"Columns: {title}\n"
        
        # 按指定欄數分組
        for i in range(0, len(items), columns):
            row_items = items[i:i+columns]
            columns_text += " | ".join(f"{item:<20}" for item in row_items) + "\n"
        
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{columns_text}"
        )


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
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **syntax_kwargs
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
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **syntax_kwargs: 傳遞給 Rich Syntax 的額外參數
        
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
    
    # 創建 Rich Syntax 對象
    syntax = Syntax(
        code,
        language,
        theme=theme,
        line_numbers=line_numbers,
        word_wrap=word_wrap,
        indent_guides=indent_guides,
        **syntax_kwargs
    )
    
    # 輸出到控制台
    if not to_log_file_only and logger_instance:
        display_title = title or f"Code ({language.upper()})"
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, f"Displaying code: {display_title}"
        )
        
        if title:
            console.print(f"[bold cyan]{title}[/bold cyan]")
        console.print(syntax)
    
    # 輸出到文件
    if not to_console_only and logger_instance:
        # 創建純文本版本的程式碼
        code_text = f"Code: {title or f'({language.upper()})'}\n"
        code_text += "=" * 50 + "\n"
        
        if line_numbers:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                code_text += f"{i:4d} | {line}\n"
        else:
            code_text += code + "\n"
        
        code_text += "=" * 50
        
        logger_instance.opt(ansi=False, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{code_text}"
        )


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
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **syntax_kwargs
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
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **syntax_kwargs: 傳遞給 Rich Syntax 的額外參數
        
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
        
        # 確保不與 syntax_kwargs 衝突
        code_kwargs = {
            'code': code,
            'language': language,
            'theme': theme,
            'line_numbers': line_numbers,
            'word_wrap': word_wrap,
            'indent_guides': indent_guides,
            'title': title,
            'log_level': log_level,
            'logger_instance': logger_instance,
            'console': console,
            'to_console_only': to_console_only,
            'to_log_file_only': to_log_file_only,
            '_target_depth': _target_depth
        }
        
        # 合併額外參數，但不覆蓋已定義的參數
        for key, value in syntax_kwargs.items():
            if key not in code_kwargs:
                code_kwargs[key] = value
        
        # 調用 print_code
        print_code(**code_kwargs)
        
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
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **syntax_kwargs
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
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **syntax_kwargs: 傳遞給 Rich Syntax 的額外參數
        
    Example:
        >>> old = "def hello():\n    print('Hi')"
        >>> new = "def hello():\n    print('Hello, World!')"
        >>> print_diff(old, new)
    """
    if console is None:
        console = get_console()
    
    # 創建語法高亮的程式碼
    old_syntax = Syntax(
        old_code,
        language,
        theme=theme,
        line_numbers=True,
        **syntax_kwargs
    )
    
    new_syntax = Syntax(
        new_code,
        language,
        theme=theme,
        line_numbers=True,
        **syntax_kwargs
    )
    
    # 輸出到控制台
    if not to_log_file_only and logger_instance:
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, "Displaying code diff"
        )
        
        # 使用 Panel 包裝，加上紅色和綠色邊框
        old_panel = Panel(
            old_syntax,
            title=f"[bold red]- {old_title}[/bold red]",
            border_style="red",
            title_align="left"
        )
        
        new_panel = Panel(
            new_syntax,
            title=f"[bold green]+ {new_title}[/bold green]",
            border_style="green", 
            title_align="left"
        )
        
        # 顯示差異標題
        console.print(f"\n[bold cyan]Code Diff: {old_title} → {new_title}[/bold cyan]")
        
        # 並排顯示帶邊框的程式碼
        columns = Columns([old_panel, new_panel], equal=True, expand=True)
        console.print(columns)
        console.print()
    
    # 輸出到文件
    if not to_console_only and logger_instance:
        diff_text = f"Code Diff: {old_title} → {new_title}\n"
        diff_text += "=" * 60 + "\n"
        diff_text += f"\n[-] {old_title}:\n"
        diff_text += "-" * 30 + "\n"
        
        # 為舊程式碼每行添加 - 前綴
        old_lines = old_code.strip().split('\n')
        for i, line in enumerate(old_lines, 1):
            diff_text += f"- {i:3d} | {line}\n"
        
        diff_text += f"\n[+] {new_title}:\n"
        diff_text += "+" * 30 + "\n"
        
        # 為新程式碼每行添加 + 前綴
        new_lines = new_code.strip().split('\n')
        for i, line in enumerate(new_lines, 1):
            diff_text += f"+ {i:3d} | {line}\n"
            
        diff_text += "\n" + "=" * 60
        
        logger_instance.opt(ansi=False, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{diff_text}"
        )


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
    log_level: str = "INFO",
    logger_instance: Any = None,
    console: Optional[Console] = None,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    _target_depth: int = None,
    **panel_kwargs
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
        log_level: 日誌級別
        logger_instance: logger 實例
        console: Rich console 實例
        to_console_only: 僅輸出到控制台
        to_log_file_only: 僅輸出到文件
        _target_depth: 調用深度
        **panel_kwargs: 傳遞給 Rich Panel 的額外參數
        
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
    
    # 處理 box 樣式
    box = rich_box.ROUNDED  # 默認圓角邊框
    if box_style:
        box_styles = {
            "ascii": rich_box.ASCII,
            "ascii2": rich_box.ASCII2,
            "square": rich_box.SQUARE,
            "rounded": rich_box.ROUNDED,
            "double": rich_box.DOUBLE,
            "heavy": rich_box.HEAVY,
            "minimal": rich_box.MINIMAL,
            "simple": rich_box.SIMPLE,
            "heavy_head": rich_box.HEAVY_HEAD,
            "double_edge": rich_box.DOUBLE_EDGE,
            "thick": rich_box.HEAVY,  # 別名
        }
        box = box_styles.get(box_style.lower(), rich_box.ROUNDED)
    
    # 創建 Panel
    panel = Panel(
        content,
        title=title,
        subtitle=subtitle,
        border_style=border_style,
        box=box,
        title_align=title_align,
        subtitle_align=subtitle_align,
        width=width,
        height=height,
        padding=padding,
        expand=expand,
        **panel_kwargs
    )
    
    # 輸出到控制台
    if not to_log_file_only and logger_instance:
        display_title = title or "Panel"
        logger_instance.opt(ansi=True, depth=_target_depth).bind(to_console_only=True).log(
            log_level, f"Displaying panel: {display_title}"
        )
        console.print(panel)
    
    # 輸出到文件
    if not to_console_only and logger_instance:
        # 創建文本版本的面板
        panel_text = ""
        if title:
            panel_text += f"┌─ {title} " + "─" * (50 - len(title) - 3) + "┐\n"
        else:
            panel_text += "┌" + "─" * 50 + "┐\n"
        
        # 處理內容
        content_str = str(content)
        content_lines = content_str.split('\n')
        
        # 添加內邊距
        if isinstance(padding, int):
            pad_top = pad_bottom = pad_left = pad_right = padding
        elif len(padding) == 2:
            # (vertical, horizontal)
            pad_top = pad_bottom = padding[0]
            pad_left = pad_right = padding[1]
        elif len(padding) == 4:
            # (top, right, bottom, left)
            pad_top, pad_right, pad_bottom, pad_left = padding
        else:
            # 默認值
            pad_top = pad_bottom = pad_left = pad_right = 1
        
        # 頂部內邊距
        for _ in range(pad_top):
            panel_text += "│" + " " * 50 + "│\n"
        
        # 內容行
        for line in content_lines:
            padded_line = " " * pad_left + line + " " * pad_right
            panel_text += f"│{padded_line:<50}│\n"
        
        # 底部內邊距
        for _ in range(pad_bottom):
            panel_text += "│" + " " * 50 + "│\n"
        
        # 底部邊框
        if subtitle:
            panel_text += "└" + "─" * (47 - len(subtitle)) + f" {subtitle} ─┘"
        else:
            panel_text += "└" + "─" * 50 + "┘"
        
        logger_instance.opt(ansi=False, depth=_target_depth).bind(to_log_file_only=True).log(
            log_level, f"\n{panel_text}"
        )


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
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **table_kwargs
    ) -> None:
        print_table(
            title=title,
            data=data,
            headers=headers,
            show_header=show_header,
            show_lines=show_lines,
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **table_kwargs
        )
    
    # 2. 樹狀結構方法
    @ensure_target_parameters  
    def tree_method(
        title: str,
        tree_data: Dict[str, Any],
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **tree_kwargs
    ) -> None:
        print_tree(
            title=title,
            tree_data=tree_data,
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **tree_kwargs
        )
    
    # 3. 分欄顯示方法
    @ensure_target_parameters
    def columns_method(
        title: str,
        items: List[str],
        columns: int = 3,
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **columns_kwargs
    ) -> None:
        print_columns(
            title=title,
            items=items,
            columns=columns,
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **columns_kwargs
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
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **syntax_kwargs
    ) -> None:
        print_code(
            code=code,
            language=language,
            theme=theme,
            line_numbers=line_numbers,
            word_wrap=word_wrap,
            indent_guides=indent_guides,
            title=title,
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **syntax_kwargs
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
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **syntax_kwargs
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
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **syntax_kwargs
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
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **syntax_kwargs
    ) -> None:
        print_diff(
            old_code=old_code,
            new_code=new_code,
            old_title=old_title,
            new_title=new_title,
            language=language,
            theme=theme,
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **syntax_kwargs
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
        log_level: str = "INFO",
        to_console_only: bool = False,
        to_log_file_only: bool = False,
        _target_depth: int = None,
        **panel_kwargs
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
            log_level=log_level,
            logger_instance=logger_instance,
            console=console,
            to_console_only=to_console_only,
            to_log_file_only=to_log_file_only,
            _target_depth=_target_depth,
            **panel_kwargs
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
    
    # 添加目標特定方法
    add_target_methods(logger_instance, "table", table_method)
    add_target_methods(logger_instance, "tree", tree_method)
    add_target_methods(logger_instance, "columns", columns_method)
    add_target_methods(logger_instance, "code", code_method)
    add_target_methods(logger_instance, "code_file", code_file_method)
    add_target_methods(logger_instance, "diff", diff_method)
    add_target_methods(logger_instance, "panel", panel_method)  # 新增 panel 的目標方法


# 導出的函數和類
__all__ = [
    'print_table',
    'print_tree', 
    'print_columns',
    'print_code',
    'print_code_from_file',
    'print_diff',
    'print_panel',
    'LoggerProgress',
    'create_rich_methods'
]