# Native Format (原生格式)

`use_native_format` 是 pretty-loguru v2.1.0+ 新增的功能，讓你可以使用接近 loguru 原生的日誌格式。

## 🎯 設計目標

- **無縫遷移**：從 loguru 遷移到 pretty-loguru 時保持格式一致性
- **開發友好**：使用檔案名稱定位程式碼更直觀
- **保持簡潔**：遵循 KISS 原則，一個參數控制格式切換

## 🔄 格式對比

### Enhanced 格式 (預設)
```python
from pretty_loguru import create_logger

logger = create_logger("my_service")
logger.info("用戶登入成功")
```
**輸出：**
```
2025-06-30 20:15:30 | INFO    12345 | my_service:login:42 - 用戶登入成功
```

### Native 格式
```python
from pretty_loguru import create_logger

logger = create_logger("my_service", use_native_format=True)
logger.info("用戶登入成功")
```
**輸出：**
```
2025-06-30 20:15:30.123 | INFO     | main.py:login:42 - 用戶登入成功
```

## 📊 詳細差異

| 特性 | Enhanced 格式 | Native 格式 |
|------|---------------|-------------|
| **顯示名稱** | 自定義名稱 | 檔案名稱 |
| **時間格式** | `HH:mm:ss` | `HH:mm:ss.SSS` (含毫秒) |
| **Process ID** | ✅ 顯示 | ❌ 隱藏 |
| **檔案命名** | `[name]_timestamp.log` | `name.log` |
| **適用場景** | 生產環境、服務監控 | 開發調試、遷移 |

## 🚀 使用場景

### 1. 從 Loguru 遷移

如果你原本使用 loguru：

```python
# 原本的 loguru 代碼
from loguru import logger
logger.info("應用啟動")
```

遷移到 pretty-loguru 時保持格式：

```python
# 遷移後的代碼
from pretty_loguru import create_logger
logger = create_logger("app", use_native_format=True)
logger.info("應用啟動")
```

### 2. 開發環境設定

```python
import os

def create_app_logger():
    if os.getenv("ENV") == "development":
        return create_logger(
            "dev_app",
            use_native_format=True,  # 開發時使用原生格式
            level="DEBUG"
        )
    else:
        return create_logger(
            "prod_app", 
            use_native_format=False,  # 生產時使用增強格式
            level="INFO"
        )
```

### 3. 混合使用

```python
# 同時使用兩種格式
debug_logger = create_logger("debug", use_native_format=True)
service_logger = create_logger("service", use_native_format=False) 

debug_logger.debug("變數檢查", var="value")      # 原生格式
service_logger.info("API 請求處理完成")           # 增強格式
```

## 🔧 配置範例

### 基本配置

```python
from pretty_loguru import create_logger

# 最簡單的原生格式 logger
logger = create_logger(use_native_format=True)
```

### 完整配置

```python
logger = create_logger(
    name="my_app",
    use_native_format=True,
    log_path="./logs",
    level="DEBUG",
    rotation="10MB",
    retention="7 days"
)
```

### 與預設值結合

```python
logger = create_logger(
    name="api_service",
    use_native_format=True,
    preset="detailed"  # 可與預設值結合使用
)
```

## 📁 檔案命名差異

### Enhanced 格式檔案命名
```
logs/
├── [api_service]_20250630-201530.log
├── [user_service]_20250630-201535.log
└── [order_service]_20250630-201540.log
```

### Native 格式檔案命名
```
logs/
├── api_service.log
├── user_service.log
└── order_service.log
```

## 💡 最佳實踐

### 1. 環境區分
```python
def setup_logger(service_name: str, env: str):
    return create_logger(
        name=service_name,
        use_native_format=(env == "development"),
        log_path=f"logs/{env}",
        level="DEBUG" if env == "development" else "INFO"
    )
```

### 2. 團隊協作
```python
# 在團隊項目中提供統一的 logger 工廠
def create_team_logger(name: str, for_development: bool = False):
    return create_logger(
        name=name,
        use_native_format=for_development,
        log_path="logs",
        preset="detailed" if not for_development else None
    )

# 使用
prod_logger = create_team_logger("api")
dev_logger = create_team_logger("api", for_development=True)
```

### 3. 遷移策略
```python
# 階段性遷移：先保持原生格式，再逐步切換
class LoggerMigration:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.migration_complete = os.getenv("LOGGER_MIGRATION", "false") == "true"
    
    def get_logger(self):
        return create_logger(
            name=self.service_name,
            use_native_format=not self.migration_complete,
            log_path="logs"
        )
```

## ❓ 常見問題

### Q: 何時應該使用 Native 格式？
**A:** 
- 從 loguru 遷移時
- 開發和調試階段
- 需要快速定位程式碼檔案時
- 偏好簡潔檔案命名時

### Q: 能否動態切換格式？
**A:** 可以通過重新建立 logger 實現：
```python
# 重新建立不同格式的 logger
logger = create_logger("app", use_native_format=True, force_new_instance=True)
```

### Q: Native 格式是否支援所有功能？
**A:** 是的，只是輸出格式不同，所有 pretty-loguru 功能都完全支援。

### Q: 如何選擇格式？
**A:** 
- **開發階段**：使用 Native 格式便於調試
- **生產環境**：使用 Enhanced 格式便於監控
- **遷移場景**：使用 Native 格式保持一致性

## 🔗 相關文檔

- [基本用法](../guide/basic-usage.md) - 瞭解基礎概念
- [範例集合](../examples/) - 查看實際應用
- [API 文檔](../api/core.md) - 詳細參數說明