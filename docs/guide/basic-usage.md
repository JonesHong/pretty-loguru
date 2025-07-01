# 基本用法

本頁面將詳細介紹 pretty-loguru 的基本概念和核心功能。

## 🎯 核心概念

### Logger 初始化

pretty-loguru 提供多種初始化方式，滿足不同場景的需求。

#### 快速初始化 (推薦)

```python
from pretty_loguru import create_logger

# 一行代碼完成所有設定
logger  
    name="basic-usage_demo",
    log_path="my_logs",
    level="INFO"
)
print(f"Logger 已初始化，元件名稱：{component_name}")
```

#### 自定義初始化

```python
from pretty_loguru import init_logger

init_logger(
    level="INFO",
    log_path="custom_logs",
    component_name="my_app",
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
    log_path="logs/api"
)

api_logger.info("API 服務已啟動")
```

#### 原生格式 Logger (v2.1.0+)

```python
# 使用接近 loguru 原生的格式，適合從 loguru 遷移
native_logger = create_logger(
    name="migration_app",
    use_native_format=True,  # 使用原生格式
    log_path="logs"
)

# 輸出格式：file.name:function:line - message
native_logger.info("這是原生格式的訊息")
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

### 僅控制台輸出

```python
# 只在控制台顯示，不寫入檔案
logger.console_info("只在控制台顯示")
logger.console_warning("控制台警告")
logger.console_error("控制台錯誤")
```

### 僅檔案輸出

```python
# 只寫入檔案，不在控制台顯示
logger.file_info("只寫入日誌檔案")
logger.file_debug("檔案除錯訊息")
logger.file_error("檔案錯誤記錄")
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
    log_path="logs", rotation="10MB",
    level="INFO"
)

# 按時間輪換
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", rotation="1 day",
    level="INFO"
)

# 按數量輪換
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", rotation="midnight", retention=10,
    level="INFO"
)
```

### 日誌清理

```python
# 自動清理舊檔案
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)
```

### 多環境配置

```python
import os

def setup_logging():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return logger = create_logger(
    name="demo",
    log_path="prod_logs",
    level="INFO"
)
    else:
        return logger = create_logger(
    name="demo",
    log_path="dev_logs",
    level="INFO"
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
    log_path=
        folder="app_logs",
        level="INFO",
        rotation="50MB",
        retention="14 days"
    )
    
    logger.info(f"應用程式啟動，元件：{component_name}")
    
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
    log_path="logs", level="DEBUG",
    level="INFO"
)
```

### Q: 如何只在檔案中記錄敏感資訊？
A: 使用檔案專用方法：
```python
logger.file_info(f"用戶密碼重設：{user_id}")  # 只寫入檔案
logger.console_info("用戶密碼重設成功")        # 只顯示在控制台
```

### Q: 日誌檔案太多怎麼辦？
A: 設定自動清理：
```python
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", retention="7 days",
    level="INFO"
)
```

### Q: 如何在不同模組中使用同一個 logger？
A: logger 是全域的，直接匯入即可：
```python
# module_a.py
from pretty_loguru import create_logger
logger.info("模組 A 的訊息")

# module_b.py  
from pretty_loguru import create_logger
logger.info("模組 B 的訊息")
```

## 🚀 下一步

現在你已經掌握了 pretty-loguru 的基本用法，可以：

- [探索視覺化功能](../features/) - Rich 區塊和 ASCII 藝術
- [查看實際範例](../examples/) - 完整的應用場景
- [了解框架整合](../integrations/) - FastAPI 和 Uvicorn 整合
- [深入 API 文件](../api/) - 詳細的技術參考

開始建立美觀且實用的日誌系統吧！