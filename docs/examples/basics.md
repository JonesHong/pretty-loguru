# 基礎功能範例

本頁展示 Pretty-Loguru 的核心功能和使用方式。

## 簡單使用

展示最基本的 logger 創建和使用：

```python
from pretty_loguru import create_logger

# 最簡單的方式 - 只需要一個名稱
logger = create_logger("simple_demo")

# 開始記錄
logger.info("這是一個簡單的開始")
logger.success("看！使用 Pretty-Loguru 就是這麼簡單！")

# 帶檔案輸出
logger_with_file = create_logger(
    name="with_file",
    log_path="logs/demo"
)

# 自定義等級和格式
custom_logger = create_logger(
    name="custom",
    level="DEBUG",
    log_path="logs/custom",
    rotation="100 MB",
    retention="30 days"
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/simple_usage.py)

## 多個 Logger 管理

在大型應用中管理多個 logger：

```python
from pretty_loguru import create_logger, LoggerConfig, list_loggers

# 為不同模組創建 logger
app_logger = create_logger("app", log_path="logs/app")
db_logger = create_logger("database", log_path="logs/db", level="DEBUG")
api_logger = create_logger("api", log_path="logs/api", level="WARNING")

# 使用統一配置
config = LoggerConfig(
    level="INFO",
    log_path="logs/services",
    rotation="1 day",
    retention="7 days"
)

# 創建多個使用相同配置的 logger
auth_logger = create_logger("auth", config=config)
payment_logger = create_logger("payment", config=config)

# 列出所有 logger
print(f"已註冊的 logger: {list_loggers()}")

# 階層式命名
main_logger = create_logger("myapp")
user_logger = create_logger("myapp.user")
order_logger = create_logger("myapp.order")
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/multiple_loggers.py)

## 控制台 vs 檔案輸出

分別控制輸出目標：

```python
from pretty_loguru import create_logger

logger = create_logger("output_demo", log_path="logs")

# 同時輸出到控制台和檔案
logger.info("這條訊息會出現在控制台和檔案中")

# 只輸出到控制台
logger.console_info("這條訊息只在控制台顯示")
logger.console_success("✅ 控制台專屬成功訊息")

# 只輸出到檔案
logger.file_info("這條訊息只會記錄到檔案")
logger.file_error("檔案專屬錯誤記錄")

# 視覺化元素的目標控制
logger.console_block(
    "控制台專屬區塊",
    ["不會出現在日誌檔案中", "只在終端顯示"],
    border_style="cyan"
)

logger.file_block(
    "檔案專屬區塊",
    ["只記錄到檔案", "控制台看不到"],
    border_style="yellow"
)
```

使用場景：
- 敏感資訊只記錄到檔案
- 進度條只在控制台顯示
- 詳細除錯資訊只寫入檔案

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/console_vs_file.py)

## 錯誤處理範例

優雅地處理和記錄錯誤：

```python
from pretty_loguru import create_logger
import traceback

logger = create_logger("error_demo", log_path="logs/errors")

def risky_operation():
    """可能失敗的操作"""
    import random
    if random.random() > 0.5:
        raise ValueError("模擬的錯誤")
    return "操作成功"

# 基本錯誤處理
try:
    result = risky_operation()
    logger.success(f"操作完成: {result}")
except Exception as e:
    logger.error(f"操作失敗: {type(e).__name__}: {str(e)}")
    
    # 記錄完整的錯誤追蹤
    logger.error(f"錯誤詳情:\n{traceback.format_exc()}")
    
    # 使用區塊顯示錯誤詳情
    logger.block(
        "❌ 錯誤報告",
        [
            f"錯誤類型: {type(e).__name__}",
            f"錯誤訊息: {str(e)}",
            f"發生位置: risky_operation()",
            "建議動作: 檢查輸入參數或重試"
        ],
        border_style="red",
        log_level="ERROR"
    )

# 使用 logger 的異常捕獲
@logger.catch
def auto_logged_function():
    """自動記錄異常的函數"""
    raise RuntimeError("這個錯誤會自動被記錄")
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/error_handling.py)

## 格式化基礎

自定義日誌格式：

```python
from pretty_loguru import create_logger

# 使用原生 loguru 格式
native_logger = create_logger(
    "native_demo",
    use_native_format=True
)

# 自定義格式
custom_logger = create_logger(
    "custom_format",
    logger_format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>"
)

# 精簡格式（適合生產環境）
minimal_logger = create_logger(
    "minimal",
    logger_format="{time:HH:mm:ss} {level} {message}"
)

# 詳細格式（適合除錯）
verbose_logger = create_logger(
    "verbose",
    logger_format="{time} | {level} | {name}:{function}:{line} - {message}"
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/formatting_basics.py)

## 下一步

- [視覺化功能](./visual.md) - Rich 區塊和 ASCII 藝術
- [配置管理](./configuration.md) - 進階配置和輪替策略
- [框架整合](./integrations.md) - FastAPI 和其他框架