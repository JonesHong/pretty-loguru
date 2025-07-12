# 核心模組 API

`pretty_loguru` 的核心模組提供了日誌系統的基礎架構，包括配置管理、處理器設定、以及底層的初始化邏輯。這些元件共同確保了日誌系統的穩定性和可擴展性。

## 總覽

核心模組主要由以下幾個部分組成：

- **`config.py`**: 定義 `LoggerConfig` 資料類別，用於儲存所有日誌相關的配置。
- **`base.py`**: 包含 `configure_logger` 等核心函數，負責根據配置初始化 logger。
- **`handlers.py`**: 管理日誌的目標（console/file）過濾和檔名格式化。
- **`presets.py`**: 提供預設的配置模板，簡化常見場景的設定。

---

## `config.py` - 日誌配置

### `LoggerConfig`

這是一個 `dataclass`，集中管理單一 logger 實例的所有配置選項。

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable

@dataclass
class LoggerConfig:
    name: str
    level: str
    logger_format: str
    log_path: Optional[str] = None
    component_name: Optional[str] = None
    rotation: Optional[str] = None
    retention: Optional[str] = None
    compression: Optional[Union[str, Callable]] = None
    compression_format: Optional[str] = None
    subdirectory: Optional[str] = None
    preset: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
```

**屬性說明：**

| 屬性 | 類型 | 說明 |
| --- | --- | --- |
| `name` | `str` | Logger 的唯一識別名稱。 |
| `level` | `str` | 最低日誌級別，如 "DEBUG", "INFO"。 |
| `logger_format` | `str` | Loguru 的日誌格式化字串。 |
| `log_path` | `Optional[str]` | 日誌檔案的儲存目錄。若為 `None`，則僅輸出到控制台。 |
| `component_name` | `Optional[str]` | 元件名稱，通常用於日誌檔名。 |
| `rotation` | `Optional[str]` | 檔案輪換策略，如 "10 MB", "1 day"。 |
| `retention` | `Optional[str]` | 檔案保留策略，如 "7 days", 10 (個檔案)。 |
| `compression` | `Optional[Union[str, Callable]]` | 壓縮格式，如 "zip", "gz"，或自定義壓縮函數。 |
| `compression_format` | `Optional[str]` | 自定義壓縮檔的命名格式。 |
| `subdirectory` | `Optional[str]` | 在 `log_path` 下建立的子目錄。 |
| `preset` | `Optional[str]` | 使用的預設配置名稱。 |
| `extra` | `Dict[str, Any]` | 傳遞給 `logger.configure` 的額外參數。 |

**方法說明：**

### `apply_to(*names) -> Union[EnhancedLogger, Tuple[EnhancedLogger, ...]]`

將配置應用到一個或多個**現有的** logger。


```python
# 更新單個 logger
config = LoggerConfig(level="DEBUG")
updated_logger = config.apply_to("existing_logger")

# 更新多個 logger
loggers = config.apply_to("auth", "api", "database")
```

### `update(**kwargs) -> None`

動態更新配置並自動應用到所有相關的 logger。

```python
config = LoggerConfig(level="INFO")
config.apply_to("app1", "app2", "app3")

# 更新所有相關 logger 的日誌級別
config.update(level="DEBUG")
```

### `clone() -> LoggerConfig`

創建配置的深拷貝，避免相互影響。

```python
base_config = LoggerConfig(level="INFO", log_path="logs")
dev_config = base_config.clone()
dev_config.update(level="DEBUG")
```

### `logger_exists(name: str) -> bool` (靜態方法)

檢查指定名稱的 logger 是否已經存在。

```python
if LoggerConfig.logger_exists("my_logger"):
    config.apply_to("my_logger")
else:
    create_logger("my_logger", config=config)
```

---

## `base.py` - 基礎功能

此模組提供配置 logger 的核心邏輯。

### `configure_logger()`

根據 `LoggerConfig` 物件來配置指定的 logger 實例。此函數會移除舊的處理器、設定新的格式、級別，並新增控制台和檔案處理器。

```python
def configure_logger(logger_instance: EnhancedLogger, config: LoggerConfig) -> None:
    ...
```

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `logger_instance` | `EnhancedLogger` | 要進行配置的 `loguru` logger 實例。 |
| `config` | `LoggerConfig` | 包含所有配置資訊的物件。 |

### `get_console()`

獲取全域共享的 `rich.console.Console` 實例，用於所有 Rich 元件的渲染。

```python
def get_console() -> Console:
    ...
```

**回傳值：**
- `rich.console.Console`: 用於美化輸出的 Rich Console 實例。

---

## `handlers.py` - 處理器管理

此模組負責創建和管理日誌的輸出目標。

### `create_destination_filters()`

創建一組過濾器，用於將日誌記錄路由到正確的目標（僅控制台、僅檔案或兩者皆是）。

```python
def create_destination_filters() -> Dict[str, Callable]:
    ...
```

**回傳值：**
- `Dict[str, Callable]`: 一個字典，包含 `"console"` 和 `"file"` 兩個鍵，其值為對應的過濾函數。

### `format_filename()`

根據指定的格式模板生成日誌檔名。

```python
def format_filename(component_name: str, name_format: Optional[str] = None) -> str:
    ...
```

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `component_name` | `str` | 元件名稱，用於填充檔名模板。 |
| `name_format` | `Optional[str]` | 檔名格式模板。預設為 `"{name}_{time:YYYY-MM-DD}.log"`。 |

**範例：**

```python
# 預設格式
format_filename("my_app") 
# -> "my_app_2023-10-27.log"

# 自定義格式
format_filename("worker", name_format="{name}.log") 
# -> "worker.log"
```

---

## `presets.py` - 預設配置

此模組提供預先定義好的 logger 配置，方便快速設定。

### `get_preset_config()`

根據名稱獲取一個預設的配置字典。

```python
def get_preset_config(name: str) -> Dict[str, Any]:
    ...
```

**參數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `name` | `str` | 預設配置的名稱，如 `"default"`, `"production"`, `"development"`。 |

**回傳值：**
- `Dict[str, Any]`: 包含預設配置的字典。

### `create_custom_compression_function()`

當你需要自定義壓縮檔案的名稱格式時，使用此函數來創建一個傳遞給 `logger.add` 的 `compression` 參數。

```python
def create_custom_compression_function(format_str: str) -> Callable[[str], str]:
    ...
```

**��數說明：**

| 參數 | 類型 | 說明 |
| --- | --- | --- |
| `format_str` | `str` | 自定義的檔名格式，例如 `"{path}.{time:YYYY-MM}.zip"`。 |

**回傳值：**
- `Callable[[str], str]`: 一個函數，Loguru 會在壓縮時呼叫此函數以決定壓縮檔名。

---

[返回 API 總覽](./index.md)
