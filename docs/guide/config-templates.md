# 配置模板管理

pretty-loguru 提供可重用的 `LoggerConfig` 配置模板，讓您能夠用一致的方式建立多個 logger，並在需要時對一組 logger 做「同步更新」。

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
from pretty_loguru import LoggerConfig, create_logger

# 1. 創建配置模板
config = LoggerConfig(
    level="INFO",
    log_dir="logs/app",
    rotation="daily",
    retention="30 days"
)

# 2. 先用相同模板建立 logger（也可直接用 apply_to() 自動建立）
api_logger = create_logger("api", config=config)
db_logger = create_logger("database", config=config)
cache_logger = create_logger("cache", config=config)

# 3. 把這些 logger「加入追蹤」，之後 config.update() 會自動同步更新
config.apply_to("api", "database", "cache")

# 4. 修改配置 - 所有「已附加」的 logger 會自動更新
config.update(level="DEBUG", rotation="100 MB")

# 現在所有 logger 都使用新的配置
api_logger.debug("現在可以看到 DEBUG 訊息")
```

### 使用預設模板

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

# 開發環境
dev_config = ConfigTemplates.development()
dev_logger = create_logger("dev_app", config=dev_config)
dev_config.apply_to("dev_app")

# 生產環境
prod_config = ConfigTemplates.production()
prod_logger = create_logger("prod_app", config=prod_config)
prod_config.apply_to("prod_app")

# 自訂模板
test_config = ConfigTemplates.testing().update(level="ERROR")
test_logger = create_logger("test_app", config=test_config)
test_config.apply_to("test_app")
```

## 🔧 進階功能

### 配置繼承

```python
# 基礎配置
base_config = LoggerConfig(
    level="INFO",
    rotation="daily",
    retention="30 days"
)

# API 服務繼承基礎配置
api_config = LoggerConfig().inherit_from(
    base_config,
    log_dir="logs/api",
    component_name="api_service"
)

# 資料庫服務有特殊需求
db_config = LoggerConfig().inherit_from(
    base_config,
    log_dir="logs/database",
    level="DEBUG"  # 需要更詳細的日誌
)
```

### 配置克隆

```python
# 克隆生產配置用於測試
prod_config = ConfigTemplates.production()
test_config = prod_config.clone(
    log_dir="logs/test",
    level="DEBUG",
    compression=None
)
```

### 鏈式調用

```python
# 優雅的鏈式操作
from pretty_loguru import create_logger

elegant_config = ConfigTemplates.production().update(level="DEBUG", compression=None)
create_logger("elegant_app", config=elegant_config)
logger = elegant_config.apply_to("elegant_app")

# 複雜的鏈式配置
chain_config = LoggerConfig(level="INFO", log_dir="logs/chain")
create_logger("service1", config=chain_config)
create_logger("service2", config=chain_config)
create_logger("service3", config=chain_config)

(chain_config
 .apply_to("service1", "service2", "service3")
 .update(rotation="hourly")
 .detach("service3")
 .save("configs/chain_config.json"))
```

## 📊 動態管理

### 運行時配置調整

```python
# 創建配置並附加 logger
from pretty_loguru import create_logger

app_config = LoggerConfig(level="INFO", log_dir="logs/app")
create_logger("web", config=app_config)
create_logger("worker", config=app_config)
create_logger("scheduler", config=app_config)
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
config.update(log_dir="logs/my_app")
config.save("configs/my_app_config.json")

# 載入配置
loaded_config = LoggerConfig.load("configs/my_app_config.json")
create_logger("restored_app", config=loaded_config)
logger = loaded_config.apply_to("restored_app")

# 鏈式保存
config.update(retention="14 days").save("configs/updated_config.json")
```

### 配置轉換

```python
# LoggerConfig 本身就是標準化配置物件
config_dict = config.to_dict()
restored = LoggerConfig.from_dict(config_dict)
```

## 🏗️ 實際應用場景

### 微服務架構

```python
# 基礎配置
base_config = LoggerConfig(
    level="INFO",
    rotation="daily",
    retention="30 days",
    compression="gz"
)

# 為不同服務創建專用配置
services = {
    "user-service": base_config.clone(log_dir="logs/user-service"),
    "order-service": base_config.clone(log_dir="logs/order-service"),
    "payment-service": base_config.clone(
        log_dir="logs/payment-service", 
        level="DEBUG"  # 支付服務需要詳細日誌
    )
}

# 為每個服務創建 logger
from pretty_loguru import create_logger

service_loggers = {}
for name, service_config in services.items():
    create_logger(name, config=service_config)
    service_loggers[name] = service_config.apply_to(name)

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
        log_dir="logs/staging",
        level="DEBUG"
    )
else:
    config = ConfigTemplates.development()

# 套用到應用 logger
from pretty_loguru import create_logger

create_logger("myapp", config=config)
app_logger = config.apply_to("myapp")
```

### 動態調試

```python
# 正常運行時使用 INFO 級別
config = LoggerConfig(level="INFO", log_dir="logs/app")
from pretty_loguru import create_logger

create_logger("web", config=config)
create_logger("api", config=config)
create_logger("database", config=config)
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

### LoggerConfig 類

#### 主要方法

- `apply_to(*logger_names)` - 套用配置到 logger(s)
- `update(...)` - 更新配置並自動同步到附加的 logger（顯式欄位）
- `update_from_dict(overrides)` - 從 dict 更新配置並同步到附加的 logger
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

- `create_config(...)` - 創建配置（顯式欄位）
- `config_from_preset(preset_name, overrides=None)` - 從預設創建配置（可用 overrides dict 覆蓋）

## 📦 ELK / Loki（可觀測性建議）

- ELK：建議 `serialize=True`（JSON 檔案）+ Filebeat/Fluent Bit
- Loki：建議 `serialize=True` + Promtail/Grafana Agent；或 `loki_enabled=True` 直推（best-effort：不重試、無離線緩衝、無 backpressure；失敗即丟棄）

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(
    level="INFO",
    log_dir="logs/app",
    serialize=True,
    loki_enabled=False,
)
create_logger("my_app", config=config)
config.apply_to("my_app")
```

## 🎯 最佳實踐

1. **使用預設模板**：從預設模板開始，然後根據需要自訂
2. **配置分離**：為不同的服務或模組使用獨立的配置
3. **動態調整**：利用配置的動態更新功能進行故障排除
4. **配置持久化**：將重要的配置保存到文件中
5. **繼承優於重複**：使用配置繼承避免重複定義

這個增強配置系統讓您能夠以更優雅和高效的方式管理複雜的日誌配置需求！
