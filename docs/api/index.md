# API 參考

歡迎查看 pretty-loguru 的完整 API 文件。這裡提供了所有公共 API 的詳細說明和使用範例。

## 📚 API 概覽

### 核心模組 - `pretty_loguru`

主要導入的模組和函數：

```python
from pretty_loguru import (
    create_logger,    # 建立自定義 logger (推薦)
    default_logger,   # 獲取預設 logger 實例
    get_logger,       # 根據名稱獲取 logger
    is_ascii_only     # 工具函數
)
```

### 主要類別

| 類別/函數 | 用途 | 模組 |
|-----------|------|------|
| `create_logger()` | 建立自定義 logger | `pretty_loguru.factory` |
| `default_logger()` | 獲取預設 logger 實例 | `pretty_loguru.factory` |
| `get_logger()` | 根據名稱獲取已存在的 logger | `pretty_loguru.factory` |

## 🚀 核心 API

### 推薦使用模式

建議使用以下方式獲取 logger 實例：

```python
# 方式一：創建自定義 logger (推薦)
logger = create_logger(name="my_app", log_path="logs/app.log")

# 方式二：使用預設 logger
logger = default_logger()

# 方式三：獲取已存在的 logger
logger = get_logger("my_app")
```

#### 基本日誌方法

```python
# 標準日誌級別
logger.debug(message)    # 除錯訊息
logger.info(message)     # 一般訊息
logger.success(message)  # 成功訊息（特有）
logger.warning(message)  # 警告訊息
logger.error(message)    # 錯誤訊息
logger.critical(message) # 嚴重錯誤
```

#### 視覺化方法

```python
# Rich 區塊
logger.block(title, content_list, border_style="solid", log_level="INFO")

# ASCII 藝術標題
logger.ascii_header(text, font="standard", border_style="solid", log_level="INFO")

# ASCII 藝術區塊
logger.ascii_block(title, content_list, ascii_header, ascii_font="standard", 
                  border_style="solid", log_level="INFO")
```

#### 目標導向方法

```python
# 僅控制台輸出
logger.console_debug(message)
logger.console_info(message)
logger.console_success(message)
logger.console_warning(message)
logger.console_error(message)
logger.console_critical(message)

# 僅檔案輸出
logger.file_debug(message)
logger.file_info(message)
logger.file_success(message)
logger.file_warning(message)
logger.file_error(message)
logger.file_critical(message)
```

### `create_logger()` - Logger 創建函數

主要的 logger 創建函數，用於建立具有特定配置的 logger 實例。

```python
def create_logger(
    name: Optional[str] = None,
    config: Optional[LoggerConfig] = None,
    use_native_format: bool = False,
    # 檔案輸出配置
    log_path: Optional[LogPathType] = None,
    rotation: Optional[LogRotationType] = None,
    retention: Optional[str] = None,
    compression: Optional[Union[str, Callable]] = None,
    compression_format: Optional[str] = None,
    # 格式化配置
    level: Optional[LogLevelType] = None,
    logger_format: Optional[str] = None,
    component_name: Optional[str] = None,
    subdirectory: Optional[str] = None,
    # 行為控制
    start_cleaner: Optional[bool] = None,
    # 預設和實例控制
    preset: Optional[str] = None,
    force_new_instance: bool = False
) -> EnhancedLogger
```

**參數說明：**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `name` | `Optional[str]` | `None` | Logger 名稱，若未提供則從調用文件名推斷 |
| `config` | `Optional[LoggerConfig]` | `None` | LoggerConfig 物件，如果提供將優先使用其配置 |
| `use_native_format` | `bool` | `False` | 是否使用 loguru 原生格式 (file:function:line) |

**檔案輸出配置：**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `log_path` | `Optional[LogPathType]` | `None` | 日誌檔案輸出路徑 |
| `rotation` | `Optional[LogRotationType]` | `None` | 日誌輪轉設定 (例如: "1 day", "100 MB") |
| `retention` | `Optional[str]` | `None` | 日誌保留設定 (例如: "7 days") |
| `compression` | `Optional[Union[str, Callable]]` | `None` | 壓縮設定 (函數或字符串) |
| `compression_format` | `Optional[str]` | `None` | 壓縮格式 |

**格式化配置：**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `level` | `Optional[LogLevelType]` | `None` | 日誌等級 ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL") |
| `logger_format` | `Optional[str]` | `None` | 自定義日誌格式字符串 |
| `component_name` | `Optional[str]` | `None` | 組件名稱，用於日誌標識 |
| `subdirectory` | `Optional[str]` | `None` | 子目錄，用於組織日誌檔案 |

**行為控制：**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `start_cleaner` | `Optional[bool]` | `None` | 是否啟動自動清理器 |

**預設和實例控制：**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `preset` | `Optional[str]` | `None` | 預設配置名稱 ("minimal", "detailed", "production") |
| `force_new_instance` | `bool` | `False` | 是否強制創建新實例 |

**回傳值：**
- `EnhancedLogger`: 配置好的 logger 實例

**範例：**

```python
# 基本用法
logger = create_logger(
    name="demo",
    log_path="logs/demo.log"
)

# 使用 LoggerConfig 物件
from pretty_loguru import LoggerConfig, ConfigTemplates

config = ConfigTemplates.production()
logger = create_logger("app", config=config)

# 自定義配置物件
custom_config = LoggerConfig(
    level="DEBUG",
    log_path="logs",
    rotation="1 day",
    retention="7 days"
)
logger = create_logger("debug_app", config=custom_config)

# 使用 config + 覆寫參數
logger = create_logger(
    "special_app", 
    config=config,
    level="DEBUG"  # 覆寫 config 中的 level
)

# 自定義設定
logger = create_logger(
    name="api_service",
    log_path="api_logs/api.log",
    level="INFO",
    rotation="50MB", 
    retention="30 days"
)

# 使用預設配置
logger = create_logger(preset="development")

# 使用原生格式
native_logger = create_logger(
    name="native_demo", 
    use_native_format=True
)
```

## 🎨 視覺化 API

### `logger.block()` - Rich 區塊

建立結構化的 Rich 面板。

```python
def block(
    title: str,
    content: List[str],
    border_style: str = "solid",
    log_level: str = "INFO"
) -> None
```

**參數說明：**

| 參數 | 類型 | 說明 |
|------|------|------|
| `title` | `str` | 區塊標題 |
| `content` | `List[str]` | 內容列表 |
| `border_style` | `str` | 邊框樣式：`"solid"`, `"double"`, `"rounded"`, `"thick"` 等 |
| `log_level` | `str` | 日誌級別：`"DEBUG"`, `"INFO"`, `"SUCCESS"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"` |

**範例：**

```python
logger.block(
    "系統狀態",
    [
        "CPU: 25%",
        "記憶體: 60%",
        "磁碟: 80%"
    ],
    border_style="green",
    log_level="INFO"
)
```

### `logger.ascii_header()` - ASCII 藝術標題

建立 ASCII 藝術文字標題。

```python
def ascii_header(
    text: str,
    font: str = "standard",
    border_style: str = "solid", 
    log_level: str = "INFO"
) -> None
```

**參數說明：**

| 參數 | 類型 | 說明 |
|------|------|------|
| `text` | `str` | 要轉換的文字（僅支援 ASCII 字符） |
| `font` | `str` | 字體名稱：`"standard"`, `"slant"`, `"doom"`, `"small"`, `"block"` 等 |
| `border_style` | `str` | 邊框樣式和顏色 |
| `log_level` | `str` | 日誌級別 |

**可用字體：**

- `"standard"` - 標準字體
- `"slant"` - 斜體字
- `"doom"` - 粗體字
- `"small"` - 小型字體
- `"block"` - 方塊字體
- `"digital"` - 數位字體

**範例：**

```python
logger.ascii_header("STARTUP", font="slant", border_style="blue")
```

### `logger.ascii_block()` - ASCII 藝術區塊

結合 ASCII 標題和 Rich 區塊。

```python
def ascii_block(
    title: str,
    content: List[str],
    ascii_header: str,
    ascii_font: str = "standard",
    border_style: str = "solid",
    log_level: str = "INFO"
) -> None
```

**範例：**

```python
logger.ascii_block(
    "部署報告",
    [
        "服務: Web API",
        "版本: v1.2.0",
        "狀態: 成功"
    ],
    ascii_header="DEPLOYED",
    ascii_font="block",
    border_style="green"
)
```

## 🛠️ 工具函數

### `is_ascii_only()` - ASCII 檢查

檢查字串是否僅包含 ASCII 字符。

```python
def is_ascii_only(text: str) -> bool
```

**範例：**

```python
from pretty_loguru import is_ascii_only

print(is_ascii_only("Hello World"))    # True
print(is_ascii_only("Hello 世界"))      # False
```

## 🔧 配置選項

### 日誌級別

```python
LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "SUCCESS": 25,    # pretty-loguru 特有
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}
```

### 輪換選項

```python
# 按大小輪換
rotation="10MB"    # 10 MB
rotation="100KB"   # 100 KB
rotation="1GB"     # 1 GB

# 按時間輪換
rotation="1 day"   # 每日
rotation="1 week"  # 每週
rotation="1 hour"  # 每小時
```

### 保留選項

```python
retention="7 days"    # 保留 7 天
retention="2 weeks"   # 保留 2 週
retention="1 month"   # 保留 1 個月
retention=10          # 保留 10 個檔案
```

### 壓縮選項

```python
compression="zip"    # ZIP 壓縮
compression="gz"     # GZIP 壓縮
compression="bz2"    # BZIP2 壓縮
compression=None     # 不壓縮
```

## 🎯 實際應用

### Web 應用整合

```python
from pretty_loguru import create_logger

# FastAPI 應用
def setup_logging():
    return create_logger(
        name="fastapi_app",
        log_path="api_logs/app.log",
        level="INFO"
    )

# 中介軟體中使用
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"API 請求: {request.method} {request.url} - {response.status_code} ({process_time:.3f}s)")
    return response
```

### 錯誤處理

```python
try:
    # 一些可能失敗的操作
    result = risky_operation()
    logger.success("操作成功完成")
except Exception as e:
    logger.error(f"操作失敗: {e}")
    
    # 詳細錯誤報告
    logger.block(
        "錯誤詳情",
        [
            f"錯誤類型: {type(e).__name__}",
            f"錯誤訊息: {str(e)}",
            f"發生時間: {datetime.now()}",
            "建議動作: 檢查輸入參數"
        ],
        border_style="red",
        log_level="ERROR"
    )
```

## 🛠️ 工具函數

### `get_logger(name: str) -> Optional[EnhancedLogger]`

根據名稱獲取已註冊的 logger 實例。

```python
logger = get_logger("my_app")
if logger:
    logger.info("找到 logger")
else:
    logger = create_logger("my_app")
```

### `cleanup_loggers() -> int`

清理所有註冊的 logger 和相關資源。

```python
# 清理所有 logger
count = cleanup_loggers()
print(f"清理了 {count} 個 logger")
```

### `list_loggers() -> List[str]`

列出所有已註冊的 logger 名稱。

```python
loggers = list_loggers()
print(f"當前註冊的 logger: {loggers}")
```

### `ConfigTemplates` - 配置模板

提供預定義的配置模板。

```python
from pretty_loguru import ConfigTemplates

# 可用模板
config = ConfigTemplates.development()  # 開發環境
config = ConfigTemplates.production()   # 生產環境
config = ConfigTemplates.testing()      # 測試環境

# 輪替模板
config = ConfigTemplates.daily()        # 每日輪替
config = ConfigTemplates.hourly()       # 每小時輪替
config = ConfigTemplates.weekly()       # 每週輪替
config = ConfigTemplates.monthly()      # 每月輪替
```

## 📖 更多資源

- [功能展示](../features/) - 詳細的功能說明和範例
- [整合指南](../integrations/) - 與其他框架的整合
- [範例集合](../examples/) - 實際應用場景
- [GitHub](https://github.com/JonesHong/pretty-loguru) - 原始碼和問題回報

這個 API 參考涵蓋了 pretty-loguru 的所有主要功能。如需更詳細的說明或範例，請查看相關章節。