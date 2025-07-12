# 配置管理範例

展示如何使用 LoggerConfig、預設配置和各種輪替策略。

## 使用 LoggerConfig

使用配置物件管理 logger：

```python
from pretty_loguru import create_logger, LoggerConfig, ConfigTemplates

# 基本 LoggerConfig 使用
config = LoggerConfig(
    level="INFO",
    log_path="logs/app",
    rotation="1 day",
    retention="7 days"
)

# 使用配置創建 logger
logger = create_logger("app", config=config)

# 覆寫配置中的特定參數
debug_logger = create_logger("debug_app", config=config, level="DEBUG")

# 多 logger 管理
services = ["auth", "api", "database"]
service_loggers = {
    name: create_logger(name, config=config)
    for name in services
}

# 動態更新配置
config.update(level="DEBUG")  # 所有使用此配置的 logger 都會更新
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/04_configuration/using_logger_config.py)

## 配置模板

使用預定義的配置模板：

```python
from pretty_loguru import ConfigTemplates, create_logger

# 開發環境配置
dev_config = ConfigTemplates.development()
dev_logger = create_logger("dev_app", config=dev_config)
# - Level: DEBUG
# - Rotation: 10 MB
# - Retention: 7 days

# 生產環境配置
prod_config = ConfigTemplates.production()
prod_logger = create_logger("prod_app", config=prod_config)
# - Level: INFO
# - Rotation: 50 MB
# - Retention: 30 days
# - Compression: zip
# - Cleaner: 啟用

# 測試環境配置
test_config = ConfigTemplates.testing()
test_logger = create_logger("test_app", config=test_config)
# - Level: WARNING
# - Rotation: 5 MB
# - Retention: 3 days

# 輪替模板
daily_config = ConfigTemplates.daily()
hourly_config = ConfigTemplates.hourly()
weekly_config = ConfigTemplates.weekly()
monthly_config = ConfigTemplates.monthly()
```

## 檔案輪替策略

各種輪替策略的使用：

```python
from pretty_loguru import create_logger

# 按大小輪替
size_logger = create_logger(
    "size_rotation",
    log_path="logs/size",
    rotation="50 MB",  # 每 50MB 輪替
    retention=10       # 保留 10 個檔案
)

# 按時間輪替
time_logger = create_logger(
    "time_rotation",
    log_path="logs/time",
    rotation="1 day",   # 每天輪替
    retention="30 days" # 保留 30 天
)

# 自定義時間輪替
custom_time_logger = create_logger(
    "custom_time",
    log_path="logs/custom",
    rotation="00:00",   # 每天午夜輪替
    retention="1 week"  # 保留 1 週
)

# 混合策略
hybrid_logger = create_logger(
    "hybrid",
    log_path="logs/hybrid",
    rotation="100 MB",          # 100MB 或
    retention="7 days",         # 保留 7 天
    compression="zip"           # 壓縮舊檔案
)

# 極端情境（測試用）
test_logger = create_logger(
    "test_rotation",
    log_path="logs/test",
    rotation="1 KB",            # 1KB 立即輪替
    retention="10 seconds",     # 10 秒後刪除
    compression=lambda x: f"{x}.gz"  # 自定義壓縮
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/04_configuration/rotation_examples.py)

## 從檔案載入配置

從 JSON 檔案載入配置：

```python
from pretty_loguru import LoggerConfig, create_logger
import json

# config.json 內容
config_json = {
    "level": "INFO",
    "log_path": "logs/app",
    "rotation": "1 day",
    "retention": "30 days",
    "compression": "zip",
    "start_cleaner": true
}

# 載入配置
with open("config.json", "r") as f:
    config_data = json.load(f)

config = LoggerConfig.from_dict(config_data)
logger = create_logger("app", config=config)

# 環境特定配置
import os
env = os.getenv("ENV", "development")

with open(f"config/logger_{env}.json", "r") as f:
    env_config = json.load(f)

env_logger = create_logger("app", config=LoggerConfig.from_dict(env_config))
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/04_configuration/config_from_file.py)

## 自定義預設配置

創建自己的配置預設：

```python
from pretty_loguru import LoggerConfig, create_logger
from typing import Dict, Any

class MyConfigTemplates:
    """自定義配置模板"""
    
    @staticmethod
    def microservice() -> LoggerConfig:
        """微服務配置"""
        return LoggerConfig(
            level="INFO",
            log_path="logs/services",
            rotation="100 MB",
            retention="14 days",
            compression="zip",
            logger_format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[service]} | {message}"
        )
    
    @staticmethod
    def audit() -> LoggerConfig:
        """審計日誌配置"""
        return LoggerConfig(
            level="INFO",
            log_path="logs/audit",
            rotation="1 day",
            retention="365 days",  # 保留一年
            compression="gz",
            logger_format="{time} | {extra[user]} | {extra[action]} | {message}"
        )
    
    @staticmethod
    def performance() -> LoggerConfig:
        """性能監控配置"""
        return LoggerConfig(
            level="WARNING",
            log_path="logs/performance",
            rotation="1 hour",
            retention="7 days",
            logger_format="{time} | {level} | {extra[metric]} | {message}"
        )

# 使用自定義模板
service_config = MyConfigTemplates.microservice()
service_logger = create_logger("user_service", config=service_config)
service_logger.bind(service="user_service").info("服務啟動")

audit_config = MyConfigTemplates.audit()
audit_logger = create_logger("audit", config=audit_config)
audit_logger.bind(user="admin", action="login").info("用戶登入")
```

## 目標導向日誌

控制日誌輸出目標：

```python
from pretty_loguru import create_logger

logger = create_logger("target_demo", log_path="logs")

# 開發環境：所有訊息都顯示
logger.info("一般訊息")
logger.debug("除錯訊息")

# 生產環境：只記錄重要訊息到檔案
logger.file_info("記錄到檔案的重要事件")
logger.file_error("記錄錯誤詳情到檔案")

# 控制台顯示進度，但不記錄到檔案
logger.console_info("正在處理... 50%")
logger.console_success("✅ 處理完成")

# 敏感資訊只記錄到檔案
logger.file_info(f"用戶密碼重設: user_id=12345")

# 視覺元素分離
logger.console_block(
    "即時狀態",
    ["CPU: 45%", "記憶體: 2.3GB"],
    border_style="green"
)

logger.file_block(
    "系統快照",
    ["時間: 2024-01-20 15:30:00", "版本: v1.0.0"],
    border_style="blue"
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/04_configuration/target_logging.py)

## 下一步

- [框架整合](./integrations.md) - FastAPI 和 Uvicorn
- [生產環境](./production.md) - 部署最佳實踐
- [進階功能](./advanced.md) - 底層功能存取