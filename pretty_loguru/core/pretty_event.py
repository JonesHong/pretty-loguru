"""
Pretty Event（視覺化事件）工具

目的：
- 視覺化方法（block/panel/table/...）只能送出「一筆」loguru event
- console/file 端各自 renderer，但都來自同一份 payload（語意一致）

本模組提供：
- `build_renderable()`：由 payload 重建 Rich renderable
- `render_renderable_to_text()`：把 renderable 渲染成純文字（用於檔案）
"""

from __future__ import annotations

import io
from typing import Any, Dict, Iterable, Mapping, Optional, TypedDict, Literal

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich import box as rich_box


PRETTY_VERSION_V1 = 1


PrettyKind = Literal[
    "block",
    "panel",
    "table",
    "tree",
    "columns",
    "code",
    "diff",
    "renderable",
    "ascii_header",
    "ascii_block",
    "figlet_header",
    "figlet_block",
]


class PrettyBlockPayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"block\"`（v1）。"""
    title: str
    lines: list[str]
    border_style: str
    box: Optional[str]


class PrettyPanelPayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"panel\"`（v1）。"""
    content: str
    title: Optional[str]
    subtitle: Optional[str]
    border_style: str
    box_style: Optional[str]
    title_align: str
    subtitle_align: str
    width: Optional[int]
    height: Optional[int]
    padding: Any
    expand: bool


class PrettyTablePayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"table\"`（v1）。"""
    title: str
    headers: list[str]
    rows: list[Dict[str, str]]
    show_header: bool
    show_lines: bool
    style: str


class PrettyTreePayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"tree\"`（v1）。"""
    title: str
    data: Dict[str, Any]
    style: str
    guide_style: str
    expanded: bool
    highlight: bool
    hide_root: bool


class PrettyColumnsPayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"columns\"`（v1）。"""
    title: str
    items: list[str]
    padding: Any
    width: Optional[int]
    expand: bool
    equal: bool
    column_first: bool
    right_to_left: bool
    align: Optional[str]


class PrettyCodePayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"code\"`（v1）。"""
    title: Optional[str]
    code: str
    language: Optional[str]
    theme: str
    line_numbers: bool
    word_wrap: bool
    indent_guides: bool


class PrettyDiffPayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"diff\"`（v1）。"""
    old_title: str
    new_title: str
    old_code: str
    new_code: str
    language: Optional[str]
    theme: str


class PrettyAsciiHeaderPayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"ascii_header\"`（v1）。"""
    text: str
    font: str
    art: str
    border_style: str


class PrettyFigletHeaderPayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"figlet_header\"`（v1）。"""
    text: str
    font: str
    art: str
    border_style: str


class PrettyRenderablePayloadV1(TypedDict, total=False):
    """`pretty_payload` schema for `pretty_kind=\"renderable\"`（v1）。"""
    title: Optional[str]
    text: str


def validate_pretty_payload(kind: str, payload: Dict[str, Any]) -> None:
    """
    最小化 payload 檢核（避免 renderer/sink 因缺欄位炸掉）。

    注意：這是「合約底線」，不是完整 schema validation。
    """
    if not isinstance(kind, str) or not kind:
        raise ValueError("pretty_kind must be a non-empty string")
    if not isinstance(payload, dict):
        raise ValueError("pretty_payload must be a dict")

    if kind in ("block", "ascii_block", "figlet_block"):
        if "title" not in payload or "lines" not in payload:
            raise ValueError(f"pretty_payload for {kind} must include 'title' and 'lines'")
        if not isinstance(payload.get("lines"), list):
            raise ValueError(f"pretty_payload for {kind} must include 'lines' as a list")
        return

    if kind in ("ascii_header", "figlet_header"):
        if "art" not in payload:
            raise ValueError(f"pretty_payload for {kind} must include 'art'")
        return

    if kind == "table":
        if "title" not in payload or "rows" not in payload:
            raise ValueError("pretty_payload for table must include 'title' and 'rows'")
        return

    if kind == "tree":
        if "title" not in payload or "data" not in payload:
            raise ValueError("pretty_payload for tree must include 'title' and 'data'")
        return

    if kind == "columns":
        if "title" not in payload or "items" not in payload:
            raise ValueError("pretty_payload for columns must include 'title' and 'items'")
        return

    if kind == "code":
        if "code" not in payload:
            raise ValueError("pretty_payload for code must include 'code'")
        return

    if kind == "diff":
        if "old_code" not in payload or "new_code" not in payload:
            raise ValueError("pretty_payload for diff must include 'old_code' and 'new_code'")
        return

    if kind == "panel":
        if "content" not in payload:
            raise ValueError("pretty_payload for panel must include 'content'")
        return

    if kind == "renderable":
        if "text" not in payload:
            raise ValueError("pretty_payload for renderable must include 'text'")
        return

def _get_box(box_style: Optional[str]) -> "rich_box.Box":
    """將使用者輸入的 box style（字串/None）映射為 Rich box 物件。"""
    if not box_style:
        return rich_box.ROUNDED

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
        "thick": rich_box.HEAVY,
    }
    return box_styles.get(str(box_style).lower(), rich_box.ROUNDED)


def _tree_add(node: Tree, value: Any) -> None:
    """遞迴把任意結構（dict/list/primitive）加入 Rich Tree。"""
    if isinstance(value, Mapping):
        for k, v in value.items():
            child = node.add(str(k))
            _tree_add(child, v)
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            child = node.add("")
            _tree_add(child, item)
        return
    node.add(str(value))


def build_renderable(kind: str, payload: Dict[str, Any]) -> RenderableType:
    """
    由 `pretty_kind` + `pretty_payload` 重建 Rich renderable。

    這是 pretty-loguru 的核心合約之一：
    - console sink 以 renderable 顯示
    - file sink 也由同一份 payload 生成純文字（語意一致）

    Args:
        kind: `pretty_kind`（例如 `"block"`, `"table"`）。
        payload: `pretty_payload`（對應 kind 的 v1 schema）。

    Returns:
        Rich 的 `RenderableType` 物件。
    """
    kind = str(kind)

    if kind == "block":
        title = payload.get("title")
        message = "\n".join(payload.get("lines") or [])
        return Panel(
            message,
            title=title,
            title_align="left",
            border_style=payload.get("border_style", "cyan"),
            box=_get_box(payload.get("box")),
        )

    if kind == "panel":
        return Panel(
            payload.get("content", ""),
            title=payload.get("title"),
            subtitle=payload.get("subtitle"),
            border_style=payload.get("border_style", "cyan"),
            box=_get_box(payload.get("box_style") or payload.get("box")),
            title_align=payload.get("title_align", "left"),
            subtitle_align=payload.get("subtitle_align", "left"),
            width=payload.get("width"),
            height=payload.get("height"),
            padding=payload.get("padding", (1, 2)),
            expand=payload.get("expand", True),
        )

    if kind in ("ascii_header", "figlet_header"):
        return Panel(
            payload.get("art", ""),
            border_style=payload.get("border_style", "cyan"),
        )

    if kind in ("ascii_block", "figlet_block"):
        title = payload.get("title")
        message = "\n".join(payload.get("lines") or [])
        return Panel(
            message,
            title=title,
            title_align="left",
            border_style=payload.get("border_style", "cyan"),
            box=_get_box(payload.get("box")),
        )

    if kind == "table":
        title = payload.get("title")
        rows = payload.get("rows") or []
        headers = payload.get("headers")

        if headers is None and rows:
            headers = list(rows[0].keys())
        headers = headers or []

        table = Table(
            title=title,
            show_header=payload.get("show_header", True),
            show_lines=payload.get("show_lines", False),
            style=payload.get("style", "none"),
        )
        for col in headers:
            table.add_column(str(col), justify="left")
        for row in rows:
            table.add_row(*[str(row.get(col, "")) for col in headers])
        return table

    if kind == "tree":
        title = payload.get("title")
        data = payload.get("data") or {}
        tree = Tree(
            str(title),
            style=payload.get("style", "tree"),
            guide_style=payload.get("guide_style", "tree.line"),
            expanded=payload.get("expanded", True),
            highlight=payload.get("highlight", False),
            hide_root=payload.get("hide_root", False),
        )
        _tree_add(tree, data)
        return tree

    if kind == "columns":
        title = payload.get("title")
        items = payload.get("items") or []
        cols = Columns(
            [Text(str(x)) for x in items],
            padding=payload.get("padding", (0, 1)),
            width=payload.get("width"),
            expand=payload.get("expand", False),
            equal=payload.get("equal", False),
            column_first=payload.get("column_first", False),
            right_to_left=payload.get("right_to_left", False),
            align=payload.get("align"),
            title=title,
        )
        return cols

    if kind == "code":
        code = payload.get("code", "")
        language = payload.get("language")
        theme = payload.get("theme", "monokai")
        line_numbers = bool(payload.get("line_numbers", True))
        word_wrap = bool(payload.get("word_wrap", False))
        indent_guides = bool(payload.get("indent_guides", True))
        return Syntax(
            code,
            lexer=language,
            theme=theme,
            line_numbers=line_numbers,
            word_wrap=word_wrap,
            indent_guides=indent_guides,
        )

    if kind == "diff":
        old_code = payload.get("old_code", "")
        new_code = payload.get("new_code", "")
        language = payload.get("language")
        theme = payload.get("theme", "monokai")
        left = Syntax(old_code, lexer=language, theme=theme, line_numbers=True)
        right = Syntax(new_code, lexer=language, theme=theme, line_numbers=True)
        old_title = payload.get("old_title", "old")
        new_title = payload.get("new_title", "new")
        left_panel = Panel(left, title=f"- {old_title}", border_style="red", title_align="left")
        right_panel = Panel(right, title=f"+ {new_title}", border_style="green", title_align="left")
        return Columns([left_panel, right_panel], equal=True, expand=True)

    if kind == "renderable":
        return Text(str(payload.get("text", "")))

    # fallback：即使遇到未知 kind，也要能安全地顯示（避免 handler 因資料不完整而炸掉）。
    return Panel(str(payload), title=f"pretty:{kind}", border_style="yellow")


def render_renderable_to_text(renderable: RenderableType, *, width: int = 120) -> str:
    """
    將 Rich renderable 渲染為純文字（用於檔案輸出）。

    Args:
        renderable: Rich renderable 物件（Panel/Table/Tree/...）。
        width: 模擬終端寬度，用於控制換行效果。

    Returns:
        去除尾端換行的純文字結果。
    """
    buffer = io.StringIO()
    capture_console = Console(
        file=buffer,
        force_terminal=False,
        color_system=None,
        width=width,
    )
    capture_console.print(renderable)
    return buffer.getvalue().rstrip("\n")
