# 自定義配置

pretty-loguru 提供靈活的配置選項，讓您能夠根據需求自訂日誌行為。

## 🎯 配置方式

### 使用 LoggerConfig 類（推薦）

```python
from pretty_loguru import LoggerConfig

# 創建配置物件
config = LoggerConfig(
    level="INFO",
    log_path="logs/app",
    rotation="100 MB",
    retention="30 days",
    compression=True
)

# 應用到單個 logger
logger = config.apply_to("my_app")

# 或應用到多個 logger
api_logger, db_logger = config.apply_to("api", "database")

# 動態更新配置（所有使用此配置的 logger 都會更新）
config.update(level="DEBUG")
```

### LoggerConfig 的優勢

1. **統一管理**：一個配置可以管理多個 logger
2. **動態更新**：修改配置會自動更新所有相關 logger
3. **配置複用**：可以克隆和繼承配置

```python
# 克隆配置
api_config = config.clone()
api_config.update(level="WARNING", retention="7 days")

# 從父配置繼承
test_config = LoggerConfig()
test_config.inherit_from(config, level="DEBUG")
```

### 基本配置

```python
from pretty_loguru import create_logger

# 基本自訂配置
logger = create_logger(
    name="my_app",
    level="INFO",
    log_path="logs/app",
    rotation="10 MB",
    retention="30 days",
    compression=True
)
```

### 進階配置

```python
from pretty_loguru import create_logger

# 進階自訂配置
logger = create_logger(
    name="advanced_app",
    level="DEBUG",
    log_path="logs/advanced",
    rotation="daily",
    retention="1 week",
    compression=True,
    # 自訂格式
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    # 過濾器
    filter=lambda record: "sensitive" not in record["message"].lower(),
    # 序列化
    serialize=True
)
```

## 📁 配置文件

### JSON 配置

建立 `config/logging.json`:

```json
{
    "version": 1,
    "formatters": {
        "detailed": {
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        }
    },
    "handlers": {
        "console": {
            "sink": "sys.stdout",
            "level": "INFO",
            "format": "detailed"
        },
        "file": {
            "sink": "logs/app.log",
            "level": "DEBUG",
            "rotation": "10 MB",
            "retention": "7 days"
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG"
        }
    }
}
```

### 使用配置文件

```python
from pretty_loguru import create_logger_from_config

# 從 JSON 配置創建
logger = create_logger_from_config("config/logging.json")
```

## 🎨 格式自訂

### 自訂格式字符串

```python
# 簡潔格式
simple_format = "{time:HH:mm:ss} | {level} | {message}"

# 詳細格式
detailed_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {process} | {thread} | {name}:{function}:{line} - {message}"

# 生產環境格式（JSON）
json_format = '{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", "level": "{level}", "logger": "{name}", "message": "{message}", "extra": {extra}}'
```

### 彩色輸出控制

```python
# 啟用/停用彩色輸出
logger = create_logger(
    name="colorful",
    colorize=True,  # 啟用彩色
    # 或
    colorize=False  # 停用彩色
)
```

## 🔄 輪替策略

### 大小輪替

```python
logger = create_logger(
    name="size_rotation",
    rotation="50 MB"  # 檔案達到 50MB 時輪替
)
```

### 時間輪替

```python
# 每日輪替
logger = create_logger(name="daily", rotation="daily")

# 每週輪替
logger = create_logger(name="weekly", rotation="weekly")

# 自訂時間輪替
logger = create_logger(name="hourly", rotation="1 hour")
```

### 複合輪替

```python
# 同時使用大小和時間條件
logger = create_logger(
    name="hybrid",
    rotation=["100 MB", "1 day"]  # 任一條件滿足即輪替
)
```

## 🗂️ 保留策略

```python
# 保留最近 10 個檔案
logger = create_logger(retention=10)

# 保留 30 天內的檔案
logger = create_logger(retention="30 days")

# 保留 1 週內的檔案
logger = create_logger(retention="1 week")

# 複合保留策略
logger = create_logger(retention=["7 days", 50])  # 7天內或最多50個檔案
```

## 🗜️ 壓縮選項

```python
# 啟用 gzip 壓縮
logger = create_logger(compression="gz")

# 啟用 zip 壓縮
logger = create_logger(compression="zip")

# 啟用 bz2 壓縮
logger = create_logger(compression="bz2")
```

## 🎯 過濾器

### 基本過濾

```python
# 過濾敏感訊息
def sensitive_filter(record):
    return "password" not in record["message"].lower()

logger = create_logger(
    name="filtered",
    filter=sensitive_filter
)
```

### 級別過濾

```python
# 只記錄錯誤以上級別
def error_only_filter(record):
    return record["level"].no >= 40  # ERROR 級別

logger = create_logger(
    name="errors_only",
    filter=error_only_filter
)
```

## 🏷️ 環境變數配置

```bash
# 設定環境變數
export PRETTY_LOGURU_LEVEL=DEBUG
export PRETTY_LOGURU_PATH=/var/log/myapp
export PRETTY_LOGURU_ROTATION=daily
```

```python
import os
from pretty_loguru import create_logger

# 使用環境變數
logger = create_logger(
    name="env_config",
    level=os.getenv("PRETTY_LOGURU_LEVEL", "INFO"),
    log_path=os.getenv("PRETTY_LOGURU_PATH", "logs"),
    rotation=os.getenv("PRETTY_LOGURU_ROTATION", "10 MB")
)
```

## 📚 完整範例

```python
from pretty_loguru import create_logger
import os

# 根據環境建立不同配置
env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    logger = create_logger(
        name="prod_app",
        level="INFO",
        log_path="/var/log/app",
        rotation="daily",
        retention="30 days",
        compression=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        serialize=True  # JSON 格式用於日誌聚合
    )
elif env == "development":
    logger = create_logger(
        name="dev_app",
        level="DEBUG",
        log_path="logs/dev",
        rotation="100 MB",
        retention="7 days",
        colorize=True  # 開發時使用彩色輸出
    )
else:  # testing
    logger = create_logger(
        name="test_app",
        level="WARNING",
        log_path="logs/test",
        rotation="10 MB",
        retention="1 day"
    )

# 使用配置好的 logger
logger.info("應用程式啟動", extra={"environment": env})
```

## 🔗 相關資源

- [基本用法](./basic-usage) - 基礎功能使用
- [日誌輪換](./log-rotation) - 詳細輪換設定
- [API 文檔](../api/) - 完整 API 參考