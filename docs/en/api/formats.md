# Formatting & Visualization API

The `pretty-loguru` formatting module provides powerful visualization tools that can transform monotonous logs into well-structured, easily readable information. This includes structured blocks, ASCII art, and deep integration with Rich library's advanced components.

## `logger.block()` - Structured Blocks

Using `logger.block()` creates a panel with a title and border, perfect for displaying a group of related information.

```python
def block(
    title: str,
    message_list: List[str],
    border_style: str = "cyan",
    log_level: str = "INFO",
    to_console_only: bool = False,
    to_log_file_only: bool = False
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `title` | `str` | Title of the block. |
| `message_list` | `List[str]` | List of messages to display within the block. |
| `border_style` | `str` | Rich border style like `"solid"`, `"double"`, `"rounded"` or color name `"green"`. |
| `log_level` | `str` | Log level for this message, such as `"INFO"`, `"WARNING"`. |
| `to_console_only` | `bool` | If `True`, this message only appears in console, not written to file. |
| `to_log_file_only` | `bool` | If `True`, this message only written to file, not displayed in console. |

**Examples:**

```python
logger.block(
    "System Status",
    [
        "Service: API Server - OK",
        "Database Connection: Success",
        "CPU Usage: 35%",
    ],
    border_style="green",
    log_level="SUCCESS"
)
```

---

## ASCII Art Features

This feature requires additional installation of the `art` library (`pip install art`).

### `logger.ascii_header()` - ASCII Art Headers

Converts text into ASCII art form headers, commonly used to mark program startup, shutdown, or important phases.

```python
def ascii_header(
    text: str,
    font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO"
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `text` | `str` | Text to convert (ASCII characters only). |
| `font` | `str` | Font supported by `art` library, such as `"standard"`, `"slant"`, `"doom"`, `"block"`. |
| `border_style` | `str` | Border style or color. |
| `log_level` | `str` | Log level. |

**Examples:**

```python
logger.ascii_header("STARTUP", font="block", border_style="magenta")
```

### `logger.ascii_block()` - ASCII Art Blocks

Combines ASCII headers with structured blocks, displaying both artistic headers and detailed information within one panel.

```python
def ascii_block(
    title: str,
    message_list: List[str],
    ascii_header: Optional[str] = None,
    ascii_font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO"
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `title` | `str` | Title of the block. |
| `message_list` | `List[str]` | List of messages within the block. |
| `ascii_header` | `Optional[str]` | ASCII text to convert. If `None`, uses `title`. |
| `ascii_font` | `str` | Font for ASCII art. |
| `border_style` | `str` | Border style or color. |
| `log_level` | `str` | Log level. |

---

## Rich Advanced Components

`pretty-loguru` integrates various Rich advanced components to make log presentations more diverse.

### `logger.table()` - Table Display

Display structured data in formatted tables.

```python
def table(
    title: str,
    data: List[Dict[str, Any]],
    headers: Optional[List[str]] = None,
    log_level: str = "INFO",
    **table_kwargs
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `title` | `str` | Title of the table. |
| `data` | `List[Dict[str, Any]]` | Data source for the table, a list of dictionaries. |
| `headers` | `Optional[List[str]]` | Custom headers. If `None`, uses keys from the first dictionary in `data`. |
| `log_level` | `str` | Log level. |
| `**table_kwargs` | `Any` | Additional parameters passed to `rich.table.Table`, such as `show_lines=True`. |

**Examples:**

```python
user_data = [
    {"ID": "001", "Name": "Alice", "Status": "Online"},
    {"ID": "002", "Name": "Bob", "Status": "Offline"},
]
logger.table("User Status", user_data, show_lines=True)
```

### `logger.tree()` - Tree Structure

Display hierarchical data in tree structure format.

```python
def tree(
    title: str,
    tree_data: Dict[str, Any],
    log_level: str = "INFO",
    **tree_kwargs
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `title` | `str` | Title for the tree root node. |
| `tree_data` | `Dict[str, Any]` | Tree structure data, supports nested dictionaries. |
| `log_level` | `str` | Log level. |
| `**tree_kwargs` | `Any` | Additional parameters passed to `rich.tree.Tree`. |

**Examples:**

```python
file_system = {
    "C:": {
        "Program Files": {"..."},
        "Users": {"Alice": {"Desktop": "..."}},
    }
}
logger.tree("File System", file_system)
```

### `logger.columns()` - Column Display

Arrange a list of items neatly in multiple columns.

```python
def columns(
    title: str,
    items: List[str],
    columns: int = 3,
    log_level: str = "INFO",
    **columns_kwargs
) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `title` | `str` | Title for the column display. |
| `items` | `List[str]` | List of items to display. |
| `columns` | `int` | Number of columns to divide into. |
| `log_level` | `str` | Log level. |
| `**columns_kwargs` | `Any` | Additional parameters passed to `rich.columns.Columns`. |

### `logger.progress` - Progress Bars

Provides a progress bar tool integrated with the logging system, suitable for tracking long-running tasks.

#### `logger.progress.progress_context()`

A context manager for tracking tasks with a fixed total number of steps.

```python
@contextmanager
def progress_context(description: str = "Processing", total: int = 100):
    ...
```

**Examples:**

```python
with logger.progress.progress_context("Downloading files", total=1024) as update:
    for chunk in range(1024):
        # ... process data ...
        update(1)
```

#### `logger.progress.track_list()`

An iterator for tracking progress when processing lists or other iterable objects.

```python
def track_list(items: List[Any], description: str = "Processing items") -> List[Any]:
    ...
```

**Examples:**

```python
import time
tasks = range(5)
for task in logger.progress.track_list(tasks, "Executing tasks"):
    time.sleep(0.5)
```

---

[Back to API Overview](./index.md)