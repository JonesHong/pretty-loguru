# 增強配置管理

pretty-loguru 提供了強大的增強配置系統，讓您能夠創建可重用的配置模板，並優雅地管理多個 logger。

## 🎯 核心特性

### 可重用配置模板
- 一個配置可以套用到多個 logger
- 修改配置自動更新所有附加的 logger
- 支援配置繼承和克隆

### 優雅的 API 設計
- 鏈式調用支援
- 直觀的方法命名
- 避免冗長的管理器模式

## 🚀 快速開始

### 基本使用

```python
from pretty_loguru import EnhancedLoggerConfig

# 1. 創建配置模板
config = EnhancedLoggerConfig(
    level="INFO",
    log_path="logs/app",
    rotation="daily",
    retention="30 days"
)

# 2. 套用到多個 logger
api_logger = config.apply_to("api")
db_logger, cache_logger = config.apply_to("database", "cache")

# 3. 修改配置 - 所有 logger 自動更新
config.update(level="DEBUG", rotation="100 MB")

# 現在所有 logger 都使用新的配置
api_logger.debug("現在可以看到 DEBUG 訊息")
```

### 使用預設模板

```python
from pretty_loguru import ConfigTemplates

# 開發環境
dev_logger = ConfigTemplates.development().apply_to("dev_app")

# 生產環境
prod_logger = ConfigTemplates.production().apply_to("prod_app")

# 自訂模板
test_logger = ConfigTemplates.testing().update(level="ERROR").apply_to("test_app")
```

## 🔧 進階功能

### 配置繼承

```python
# 基礎配置
base_config = EnhancedLoggerConfig(
    level="INFO",
    rotation="daily",
    retention="30 days"
)

# API 服務繼承基礎配置
api_config = EnhancedLoggerConfig().inherit_from(
    base_config,
    log_path="logs/api",
    component_name="api_service"
)

# 資料庫服務有特殊需求
db_config = EnhancedLoggerConfig().inherit_from(
    base_config,
    log_path="logs/database",
    level="DEBUG"  # 需要更詳細的日誌
)
```

### 配置克隆

```python
# 克隆生產配置用於測試
prod_config = ConfigTemplates.production()
test_config = prod_config.clone(
    log_path="logs/test",
    level="DEBUG",
    compression=None
)
```

### 鏈式調用

```python
# 優雅的鏈式操作
logger = (ConfigTemplates.production()
          .update(level="DEBUG", compression=None)
          .apply_to("elegant_app"))

# 複雜的鏈式配置
(EnhancedLoggerConfig(level="INFO", log_path="logs/chain")
 .apply_to("service1", "service2", "service3")
 .update(rotation="hourly")
 .detach("service3")
 .save("configs/chain_config.json"))
```

## 📊 動態管理

### 運行時配置調整

```python
# 創建配置並附加 logger
app_config = EnhancedLoggerConfig(level="INFO", log_path="logs/app")
loggers = app_config.apply_to("web", "worker", "scheduler")

# 動態調整日誌級別（故障排除）
app_config.update(level="DEBUG")  # 所有 logger 立即更新

# 分離不需要的 logger
app_config.detach("scheduler")

# 再次調整只會影響剩餘的 logger
app_config.update(level="WARNING")
```

### 附加關係管理

```python
# 查看附加的 logger
attached_loggers = config.get_attached_loggers()
print(f"附加的 logger: {attached_loggers}")

# 分離特定 logger
config.detach("old_logger")

# 分離所有 logger
config.detach_all()
```

## 💾 配置持久化

### 保存和載入配置

```python
# 保存配置
config = ConfigTemplates.development()
config.update(log_path="logs/my_app")
config.save("configs/my_app_config.json")

# 載入配置
loaded_config = EnhancedLoggerConfig.load("configs/my_app_config.json")
logger = loaded_config.apply_to("restored_app")

# 鏈式保存
config.update(retention="14 days").save("configs/updated_config.json")
```

### 配置轉換

```python
# 轉換為標準 LoggerConfig
standard_config = enhanced_config.to_logger_config("my_logger")

# 從標準 LoggerConfig 創建增強配置
enhanced_config = EnhancedLoggerConfig.from_logger_config(standard_config)
```

## 🏗️ 實際應用場景

### 微服務架構

```python
# 基礎配置
base_config = EnhancedLoggerConfig(
    level="INFO",
    rotation="daily",
    retention="30 days",
    compression="gzip"
)

# 為不同服務創建專用配置
services = {
    "user-service": base_config.clone(log_path="logs/user-service"),
    "order-service": base_config.clone(log_path="logs/order-service"),
    "payment-service": base_config.clone(
        log_path="logs/payment-service", 
        level="DEBUG"  # 支付服務需要詳細日誌
    )
}

# 為每個服務創建 logger
service_loggers = {
    name: config.apply_to(name)
    for name, config in services.items()
}

# 高負載時全域調整
for config in services.values():
    config.update(level="WARNING")
```

### 多環境部署

```python
import os

# 根據環境選擇配置
env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    config = ConfigTemplates.production()
elif env == "staging":
    config = ConfigTemplates.production().update(
        log_path="logs/staging",
        level="DEBUG"
    )
else:
    config = ConfigTemplates.development()

# 套用到應用 logger
app_logger = config.apply_to("myapp")
```

### 動態調試

```python
# 正常運行時使用 INFO 級別
config = EnhancedLoggerConfig(level="INFO", log_path="logs/app")
loggers = config.apply_to("web", "api", "database")

# 發現問題時，動態切換到 DEBUG
def enable_debug_mode():
    config.update(level="DEBUG")
    print("所有 logger 已切換到 DEBUG 模式")

def disable_debug_mode():
    config.update(level="INFO")
    print("所有 logger 已恢復到 INFO 模式")

# 可以通過 API 或信號觸發
enable_debug_mode()   # 開啟調試
# ... 故障排除 ...
disable_debug_mode()  # 關閉調試
```

## 📚 API 參考

### EnhancedLoggerConfig 類

#### 主要方法

- `apply_to(*logger_names)` - 套用配置到 logger(s)
- `update(**kwargs)` - 更新配置並自動同步到附加的 logger
- `clone(**overrides)` - 克隆配置
- `inherit_from(parent_config, **overrides)` - 繼承配置
- `detach(*logger_names)` - 分離 logger
- `detach_all()` - 分離所有 logger
- `get_attached_loggers()` - 獲取附加的 logger 列表
- `save(file_path)` - 保存配置到文件
- `load(file_path)` - 從文件載入配置

#### 預設模板

- `ConfigTemplates.development()` - 開發環境配置
- `ConfigTemplates.production()` - 生產環境配置
- `ConfigTemplates.testing()` - 測試環境配置
- `ConfigTemplates.debug()` - 調試配置
- `ConfigTemplates.high_performance()` - 高效能配置
- `ConfigTemplates.minimal()` - 最小配置

#### 便利函數

- `create_config(**kwargs)` - 創建配置
- `config_from_preset(preset_name, **overrides)` - 從預設創建配置

## 🎯 最佳實踐

1. **使用預設模板**：從預設模板開始，然後根據需要自訂
2. **配置分離**：為不同的服務或模組使用獨立的配置
3. **動態調整**：利用配置的動態更新功能進行故障排除
4. **配置持久化**：將重要的配置保存到文件中
5. **繼承優於重複**：使用配置繼承避免重複定義

這個增強配置系統讓您能夠以更優雅和高效的方式管理複雜的日誌配置需求！