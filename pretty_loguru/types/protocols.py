"""
簡化的類型定義模塊

按照KISS原則重新設計，保留核心功能但大幅簡化類型定義。
去除過度複雜的overload和重複的方法定義。
"""
from typing import Any, Callable, Dict, List, Literal, Optional, Protocol, Union
from pathlib import Path
import typing

if typing.TYPE_CHECKING:
    from ..formats.rich_components import LoggerProgress

# 簡化的類型別名
LogLevelType = Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
LogHandlerIdType = int
LogFilterType = Callable[[Dict[str, Any]], bool]
LogConfigType = Dict[str, Any]
LogDirType = Union[str, Path]
LogNameFormatType = Optional[str]
LogRotationType = Union[str, int]

# 預設日誌格式名稱
LogNamePresetType = Literal["detailed", "simple", "daily", "hourly", "minute"]

# 輸出目標類型
OutputDestinationType = Literal["to_console_only", "to_file_only"]


class PrettyLoggerProtocol(Protocol):
    """
    簡化的 Pretty Logger 協議
    
    只定義必要的方法簽名，不再使用大量overload
    """
    
    # 基本日誌方法（對齊 loguru）
    def debug(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """記錄 `DEBUG` 級別訊息（對齊 `loguru.logger.debug`）。"""
        ...

    def info(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """記錄 `INFO` 級別訊息（對齊 `loguru.logger.info`）。"""
        ...

    def success(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """記錄 `SUCCESS` 級別訊息（對齊 `loguru.logger.success`）。"""
        ...

    def warning(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """記錄 `WARNING` 級別訊息（對齊 `loguru.logger.warning`）。"""
        ...

    def error(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """記錄 `ERROR` 級別訊息（對齊 `loguru.logger.error`）。"""
        ...

    def critical(self, message: Any, *args: Any, **kwargs: Any) -> None:
        """記錄 `CRITICAL` 級別訊息（對齊 `loguru.logger.critical`）。"""
        ...
    
    # Pretty 方法（enable_addons=True 時注入）
    def block(self, title: str, lines: Union[str, List[str]], **kwargs: Any) -> None:
        """以 Rich Panel 印出區塊（console/file 語意一致）。"""
        ...

    def ascii_header(self, text: str, **kwargs: Any) -> None:
        """印出 ASCII Art 標題（需要 `art`）。"""
        ...

    def ascii_block(self, title: str, lines: Union[str, List[str]], **kwargs: Any) -> None:
        """印出 ASCII Art 區塊（需要 `art`）。"""
        ...
    
    # FIGlet 方法（可選，需要 `pyfiglet`）
    def figlet_header(self, text: str, **kwargs: Any) -> None:
        """印出 FIGlet 標題（需要 `pyfiglet`）。"""
        ...

    def figlet_block(self, title: str, lines: Union[str, List[str]], **kwargs: Any) -> None:
        """印出 FIGlet 區塊（需要 `pyfiglet`）。"""
        ...

    # Rich 主要功能（enable_addons=True 時注入）
    def table(
        self,
        title: str,
        data: List[Dict[str, Any]],
        headers: Optional[List[str]] = ...,
        show_header: bool = ...,
        show_lines: bool = ...,
        style: str = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """以 Rich Table 顯示結構化資料。"""
        ...

    def tree(
        self,
        title: str,
        tree_data: Dict[str, Any],
        style: str = ...,
        guide_style: str = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """以 Rich Tree 顯示樹狀結構資料。"""
        ...

    def columns(
        self,
        title: str,
        items: List[str],
        padding: Union[int, tuple] = ...,
        width: Optional[int] = ...,
        expand: bool = ...,
        equal: bool = ...,
        column_first: bool = ...,
        right_to_left: bool = ...,
        align: Optional[Literal["left", "center", "right"]] = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """以 Rich Columns 以多欄方式排列字串項目。"""
        ...

    def code(
        self,
        code: str,
        language: str = ...,
        theme: str = ...,
        line_numbers: bool = ...,
        word_wrap: bool = ...,
        indent_guides: bool = ...,
        title: Optional[str] = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """以 Rich Syntax 顯示程式碼區塊（語法高亮）。"""
        ...

    def code_file(
        self,
        file_path: str,
        language: Optional[str] = ...,
        theme: str = ...,
        line_numbers: bool = ...,
        word_wrap: bool = ...,
        indent_guides: bool = ...,
        start_line: Optional[int] = ...,
        end_line: Optional[int] = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """讀取檔案並以 Rich Syntax 顯示（支援行號/範圍）。"""
        ...

    def diff(
        self,
        old_code: str,
        new_code: str,
        old_title: str = ...,
        new_title: str = ...,
        language: str = ...,
        theme: str = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """以 side-by-side 的方式顯示程式碼差異（舊/新）。"""
        ...

    def panel(
        self,
        content: Union[str, Any],
        title: Optional[str] = ...,
        subtitle: Optional[str] = ...,
        border_style: str = ...,
        box_style: Optional[str] = ...,
        title_align: str = ...,
        subtitle_align: str = ...,
        width: Optional[int] = ...,
        height: Optional[int] = ...,
        padding: Union[int, tuple] = ...,
        expand: bool = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """以 Rich Panel 顯示文字或任意可渲染物件。"""
        ...

    progress: "LoggerProgress"

    def render(
        self,
        renderable: Any,
        title: Optional[str] = ...,
        level: str = ...,
        to_console_only: bool = ...,
        to_file_only: bool = ...,
    ) -> None:
        """直接渲染任意 Rich renderable（並保證 file/console 語意一致）。"""
        ...
    
    # Loguru 核心方法（薄封裝/直接代理）
    def bind(self, **kwargs: Any) -> "PrettyLoggerProtocol":
        """回傳帶有額外 `record['extra']` 的 logger（對齊 `loguru.logger.bind`）。"""
        ...

    def opt(self, **kwargs: Any) -> "PrettyLoggerProtocol":
        """調整 event 參數（depth/colors/capture...；對齊 `loguru.logger.opt`）。"""
        ...

    def add(self, sink: Any, **kwargs: Any) -> LogHandlerIdType:
        """新增 sink（file/stdout/自定義 callable；對齊 `loguru.logger.add`）。"""
        ...

    def remove(self, handler_id: Optional[LogHandlerIdType] = None) -> None:
        """移除 sink（對齊 `loguru.logger.remove`）。"""
        ...


# 簡化的類型別名
PrettyLogger = PrettyLoggerProtocol
