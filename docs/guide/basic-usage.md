# 基本用法

本頁面將詳細介紹 pretty-loguru 的基本概念和核心功能。

## 🎯 核心概念

### Logger 初始化

pretty-loguru 提供多種初始化方式，滿足不同場景的需求。

### ✅ 語意一致（核心合約）

- 一次 API 呼叫只會送出**一筆 Loguru event**（不在 logging 方法內額外 `console.print(...)` 走旁路）
- console/file 只是同一筆 event 的**不同 renderer**
- 視覺化方法（例如 `block/table/tree/...`）會把 `pretty_kind`、`pretty_payload`、`pretty_text` 放進 `record["extra"]`

#### 快速初始化 (推薦)

```python
from pretty_loguru import create_logger

# 一行代碼完成所有設定
logger = create_logger(
    name="basic-usage_demo",
    log_dir="my_logs",
    level="INFO"
)
```

#### 自定義初始化

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="my_app",
    level="INFO",
    log_dir="custom_logs",
    rotation="50MB",
    retention="30 days"
)
```

#### 建立專用 Logger

```python
from pretty_loguru import create_logger

# 建立 API 專用的 logger
api_logger = create_logger(
    name="api_service",
    level="DEBUG",
    log_dir="logs/api"
)

api_logger.info("API 服務已啟動")
```

#### 原生格式 Logger (v2.1.0+)

```python
# 使用接近 loguru 原生的格式，適合從 loguru 遷移
native_logger = create_logger(
    name="migration_app",
    use_native_format=True,  # 使用原生格式
    log_dir="logs"
)

# 輸出格式：file.name:function:line - message
native_logger.info("這是原生格式的訊息")
```

## 🎨 使用配置模板

pretty-loguru 提供了預設的配置模板，適合不同的使用場景：

### 內建配置模板

```python
from pretty_loguru.addons import ConfigTemplates

# 開發環境配置
dev_config = ConfigTemplates.development()
dev_logger = dev_config.apply_to("dev_app")
# - DEBUG 級別
# - 原生格式
# - 7 天保留

# 生產環境配置
prod_config = ConfigTemplates.production()
prod_logger = prod_config.apply_to("prod_app")
# - INFO 級別
# - 壓縮儲存
# - 30 天保留
# - 自動清理

# 測試環境配置
test_config = ConfigTemplates.testing()
test_logger = test_config.apply_to("test_app")
# - WARNING 級別
# - 3 天保留
```

### 模板的優勢

1. **一致性**：確保相同環境的應用使用相同配置
2. **最佳實踐**：內建經過優化的配置參數
3. **快速切換**：輕鬆在不同環境間切換

```python
import os
from pretty_loguru.addons import ConfigTemplates

# 根據環境變數自動選擇配置
env = os.getenv('APP_ENV', 'development')

if env == 'production':
    config = ConfigTemplates.production()
elif env == 'testing':
    config = ConfigTemplates.testing()
else:
    config = ConfigTemplates.development()

logger = config.apply_to("my_app")
```

## 📊 日誌級別

pretty-loguru 支援標準的日誌級別，並新增了 `SUCCESS` 級別：

### 基本日誌級別

```python
# 除錯訊息 (最低級別)
logger.debug("詳細的除錯資訊")

# 一般資訊
logger.info("應用程式正常運行")

# 成功訊息 (pretty-loguru 特有)
logger.success("操作成功完成")

# 警告訊息
logger.warning("記憶體使用率過高")

# 錯誤訊息
logger.error("連接資料庫失敗")

# 嚴重錯誤
logger.critical("系統即將崩潰")
```

### 級別說明表

| 級別 | 數值 | 用途 | 顏色 |
|------|------|------|------|
| DEBUG | 10 | 詳細的除錯資訊 | 藍色 |
| INFO | 20 | 一般運行資訊 | 白色 |
| SUCCESS | 25 | 成功操作 (特有) | 綠色 |
| WARNING | 30 | 警告訊息 | 黃色 |
| ERROR | 40 | 錯誤訊息 | 紅色 |
| CRITICAL | 50 | 嚴重錯誤 | 紅色粗體 |

## 🎯 輸出控制

### 同時輸出 (預設行為)

```python
# 預設會同時輸出到控制台和檔案
logger.info("這條訊息會出現在兩個地方")
```

### ✅ 最小範例（建議照這個心智模型）

#### 1) 語意一致（視覺化方法）

```python
from pretty_loguru import create_logger

logger = create_logger("demo", log_dir="logs/demo", level="INFO")

# 一次呼叫 -> 一筆 Loguru event
logger.block("BOOT", ["step=1", "step=2"])
logger.table("Users", [{"name": "Alice", "age": 30}])
```

#### 2) JSON 檔案日誌（ELK/Filebeat）

```python
from pretty_loguru import create_logger

logger = create_logger("json_demo", log_dir="logs/json_demo", level="INFO", serialize=True)
logger.block("STRUCTURED", ["檔案輸出會是 JSON line，extra 內含 pretty payload"])
```

#### 3) Loki 直推（可選）

```python
from pretty_loguru import create_logger

logger = create_logger(
    "loki_demo",
    log_dir="logs/loki_demo",
    level="INFO",
    serialize=True,
    loki_enabled=True,
    loki_base_url="http://localhost:3100",
    loki_labels={"app": "loki_demo"},
)
logger.info("hello loki")
```

### 僅控制台輸出

```python
# 只在控制台顯示，不寫入檔案
from pretty_loguru.addons import log_to_targets

log_to_targets(logger, "只在控制台顯示", console_only=True)
log_to_targets(logger, "控制台警告", level="WARNING", console_only=True)
log_to_targets(logger, "控制台錯誤", level="ERROR", console_only=True)
```

### 僅檔案輸出

```python
# 只寫入檔案，不在控制台顯示
from pretty_loguru.addons import log_to_targets

log_to_targets(logger, "只寫入日誌檔案", file_only=True)
log_to_targets(logger, "檔案除錯訊息", level="DEBUG", file_only=True)
log_to_targets(logger, "檔案錯誤記錄", level="ERROR", file_only=True)
```

## 📁 檔案管理

### 自動檔案命名

pretty-loguru 會自動生成有意義的檔名：

```
格式：[component_name]_YYYYMMDD-HHMMSS.log
範例：[my_app_20240630_143022]_20240630-143022.log
```

### 日誌輪換

```python
# 按檔案大小輪換
logger = create_logger(
    name="basic-usage_demo",
    log_dir="logs",
    rotation="10MB",
    level="INFO"
)

# 按時間輪換
logger = create_logger(
    name="basic-usage_demo",
    log_dir="logs",
    rotation="1 day",
    level="INFO"
)

# 按數量輪換
logger = create_logger(
    name="basic-usage_demo",
    log_dir="logs",
    rotation="midnight",
    retention=10,
    level="INFO"
)
```

### 日誌清理

```python
# 自動清理舊檔案
logger = create_logger(
    name="demo",
    log_dir="logs",
    level="INFO"
)
```

### 多環境配置

```python
import os

def setup_logging():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return create_logger(
            name="demo",
            log_dir="prod_logs",
            level="INFO"
        )
    else:
        return create_logger(
            name="demo",
            log_dir="dev_logs",
            level="DEBUG"
        )
```

### 條件式日誌

```python
import logging

# 設定日誌級別
if logger.level("DEBUG").no >= logging.DEBUG:
    logger.debug("這是除錯訊息")
```

## 🎮 實際範例

### 完整的應用程式範例

```python
import time
from pretty_loguru import create_logger

def main():
    # 初始化日誌系統
    logger = create_logger(
        name="demo",
        log_dir="app_logs",
        level="INFO",
        rotation="50MB",
        retention="14 days"
    )
    
    logger.info("應用程式啟動")
    
    try:
        # 模擬應用程式邏輯
        logger.info("載入配置檔案...")
        time.sleep(0.5)
        logger.success("配置檔案載入成功")
        
        logger.info("連接資料庫...")
        time.sleep(1)
        logger.success("資料庫連接成功")
        
        logger.info("啟動 Web 服務...")
        time.sleep(0.8)
        logger.success("Web 服務已啟動，監聽埠 8080")
        
        # 模擬警告
        logger.warning("記憶體使用率達到 75%")
        
        logger.info("應用程式運行正常")
        
    except Exception as e:
        logger.error(f"應用程式啟動失敗：{e}")
        logger.critical("系統即將退出")
        return 1
    
    logger.info("應用程式正常關閉")
    return 0

if __name__ == "__main__":
    exit(main())
```

### 錯誤處理範例

```python
def process_data(data):
    try:
        logger.info(f"開始處理數據，大小：{len(data)}")
        
        # 處理邏輯
        result = some_complex_operation(data)
        
        logger.success(f"數據處理完成，結果：{len(result)} 筆記錄")
        return result
        
    except ValueError as e:
        logger.error(f"數據格式錯誤：{e}")
        raise
    except Exception as e:
        logger.critical(f"處理過程發生嚴重錯誤：{e}")
        raise
    finally:
        logger.debug("數據處理流程結束")
```

## ❓ 常見問題

### Q: 為什麼看不到 DEBUG 級別的日誌？
A: 檢查日誌級別設定：
```python
logger = create_logger(
    name="basic-usage_demo",
    log_dir="logs",
    level="DEBUG"
)
```

### Q: 如何只在檔案中記錄敏感資訊？
A: 使用檔案專用方法：
```python
from pretty_loguru.addons import log_to_targets

log_to_targets(logger, f"用戶密碼重設：{user_id}", file_only=True)  # 只寫入檔案
log_to_targets(logger, "用戶密碼重設成功", console_only=True)        # 只顯示在控制台
```

### Q: 日誌檔案太多怎麼辦？
A: 設定自動清理：
```python
logger = create_logger(
    name="basic-usage_demo",
    log_dir="logs",
    retention="7 days",
    level="INFO"
)
```

### Q: 如何在不同模組中使用同一個 logger？
A: 使用 `get_logger` 函數來獲取已創建的 logger：
```python
# main.py - 主程式，創建 logger
from pretty_loguru import create_logger

logger = create_logger(
    name="my_app",
    level="INFO",
    log_dir="logs"
)
logger.info("主程式啟動")

# module_a.py - 模組 A
from pretty_loguru import get_logger

logger = get_logger("my_app")
logger.info("模組 A 的訊息")

# module_b.py - 模組 B
from pretty_loguru import get_logger

logger = get_logger("my_app")
logger.info("模組 B 的訊息")
```

或者使用更簡單的方法，在共用的 logger 模組中初始化：
```python
# logger.py - 共用的 logger 配置
from pretty_loguru import create_logger

logger = create_logger(
    name="shared_app",
    level="INFO",
    log_dir="logs"
)

# module_a.py
from logger import logger
logger.info("模組 A 的訊息")

# module_b.py
from logger import logger  
logger.info("模組 B 的訊息")
```

## 🚀 下一步

現在你已經掌握了 pretty-loguru 的基本用法，可以：

- [探索視覺化功能](../features/) - Rich 區塊和 ASCII 藝術
- [查看實際範例](../examples/) - 完整的應用場景
- [了解框架整合](../integrations/) - FastAPI 和 Uvicorn 整合
- [深入 API 文件](../api/) - 詳細的技術參考

開始建立美觀且實用的日誌系統吧！
