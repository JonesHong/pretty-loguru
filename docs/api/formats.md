# 格式化與視覺化 API

`pretty-loguru` 的格式化模組提供了強大的視覺化工具，可以將單調的日誌轉換為結構清晰、易於閱讀的資訊。這包括結構化區塊、ASCII 藝術以及與 Rich 庫進階元件的深度整合。

## `logger.block()` - 結構化區塊

使用 `logger.block()` 可以創建一個帶有標題和邊框的面板，非常適合用於顯示一組相關的資訊。

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

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `title` | `str` | 區塊的標題。 |
| `message_list` | `List[str]` | 要顯示在區塊內的訊息列表。 |
| `border_style` | `str` | Rich 邊框樣式，如 `"solid"`, `"double"`, `"rounded"` 或顏色名 `"green"`。 |
| `log_level` | `str` | 此日誌的級別，如 `"INFO"`, `"WARNING"`。 |
| `to_console_only` | `bool` | 若為 `True`，此訊息僅顯示在控制台，不寫入檔案。 |
| `to_log_file_only` | `bool` | ��為 `True`，此訊息僅寫入檔案，不顯示在控制台。 |

**範例：**

```python
logger.block(
    "系統狀態",
    [
        "服務: API Server - 正常",
        "資料庫連線: 成功",
        "CPU 使用率: 35%",
    ],
    border_style="green",
    log_level="SUCCESS"
)
```

---

## ASCII 藝術功能

此功能需要額外安裝 `art` 函式庫 (`pip install art`)。

### `logger.ascii_header()` - ASCII 藝術標題

將文字轉換為 ASCII 藝術形式的標題，常用於標記程式啟動、關閉或重要階段。

```python
def ascii_header(
    text: str,
    font: str = "standard",
    border_style: str = "cyan",
    log_level: str = "INFO"
) -> None:
    ...
```

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `text` | `str` | 要轉換的文字 (僅支援 ASCII 字元)。 |
| `font` | `str` | `art` 函式庫支援的字體，如 `"standard"`, `"slant"`, `"doom"`, `"block"`。 |
| `border_style` | `str` | 邊框樣式或顏色。 |
| `log_level` | `str` | 日誌級別。 |

**範例：**

```python
logger.ascii_header("STARTUP", font="block", border_style="magenta")
```

### `logger.ascii_block()` - ASCII 藝術區塊

結合了 ASCII 標題和結構化區塊，在一個面板內同時顯示藝術標題和��細資訊。

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

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `title` | `str` | 區塊的標題。 |
| `message_list` | `List[str]` | 區塊內的訊息列表。 |
| `ascii_header` | `Optional[str]` | 要轉換的 ASCII 文字。若為 `None`，則使用 `title`。 |
| `ascii_font` | `str` | ASCII 藝術的字體。 |
| `border_style` | `str` | 邊框樣式或顏色。 |
| `log_level` | `str` | 日誌級別。 |

---

## Rich 進階元件

`pretty-loguru` 整合了多種 Rich 的進階元件，讓日誌呈現更加多元。

### `logger.table()` - 表格顯示

以格式化的表格來顯示結構化資料。

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

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `title` | `str` | 表格的標題。 |
| `data` | `List[Dict[str, Any]]` | 表格的資料來源，一個字典列表。 |
| `headers` | `Optional[List[str]]` | 自訂表頭。若�� `None`，則使用 `data` 中第一個字典的鍵。 |
| `log_level` | `str` | 日誌級別。 |
| `**table_kwargs` | `Any` | 傳遞給 `rich.table.Table` 的額外參數，如 `show_lines=True`。 |

**範例：**

```python
user_data = [
    {"ID": "001", "名稱": "Alice", "狀態": "在線"},
    {"ID": "002", "名稱": "Bob", "狀態": "離線"},
]
logger.table("使用者狀態", user_data, show_lines=True)
```

### `logger.tree()` - 樹狀結構

以樹狀結構來呈現階層關係的資料。

```python
def tree(
    title: str,
    tree_data: Dict[str, Any],
    log_level: str = "INFO",
    **tree_kwargs
) -> None:
    ...
```

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `title` | `str` | 樹的根節點標題。 |
| `tree_data` | `Dict[str, Any]` | 樹狀結構的資料，支援巢狀字典。 |
| `log_level` | `str` | 日誌級別。 |
| `**tree_kwargs` | `Any` | 傳遞給 `rich.tree.Tree` 的額外參數。 |

**範例：**

```python
file_system = {
    "C:": {
        "Program Files": {"..."},
        "Users": {"Alice": {"Desktop": "..."}},
    }
}
logger.tree("檔案系統", file_system)
```

### `logger.columns()` - 分欄顯示

將一個項目列表以多欄的形式整齊排列。

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

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `title` | `str` | 分欄顯示的標題。 |
| `items` | `List[str]` | 要顯示的項目列表。 |
| `columns` | `int` | 要分的欄數。 |
| `log_level` | `str` | 日誌級別。 |
| `**columns_kwargs` | `Any` | 傳遞給 `rich.columns.Columns` 的額外參數。 |

### `logger.progress` - 進度條

提供一個與日誌系統整合的進度條工具，適合用於追蹤長時間執行的任務。

#### `logger.progress.progress_context()`

一個上下文管理器，用於追蹤具有固定總步數的任務。

```python
@contextmanager
def progress_context(description: str = "Processing", total: int = 100):
    ...
```

**範例：**

```python
with logger.progress.progress_context("下載檔案", total=1024) as update:
    for chunk in range(1024):
        # ... 處理數據 ...
        update(1)
```

#### `logger.progress.track_list()`

一個迭代器，用於追蹤處理列表或其他可迭代物件的進度。

```python
def track_list(items: List[Any], description: str = "Processing items") -> List[Any]:
    ...
```

**範例：**

```python
import time
tasks = range(5)
for task in logger.progress.track_list(tasks, "執行任務"):
    time.sleep(0.5)
```

---

[返回 API 總覽](./index.md)
