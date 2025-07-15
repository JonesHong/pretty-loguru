# 控制台與檔案日誌

學習控制台和檔案日誌之間的差異，以及何時使用每種方法。

## 🖥️ 控制台日誌

控制台日誌直接輸出到終端，非常適合開發和除錯。

### 基本控制台設定

```python
from pretty_loguru import create_logger

# 僅使用控制台日誌
logger = create_logger(
    name="demo",
    console_only=True
)

logger.info("這會出現在控制台")
logger.debug("開發用的除錯資訊")
logger.success("操作成功完成！")
logger.warning("這是一條警告訊息")
logger.error("發生了錯誤")
```

### 控制台輸出格式化

```python
from pretty_loguru import create_logger

# 配置控制台的自訂格式
logger = create_logger(
    name="console_demo",
    level="DEBUG",
    console_only=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
)

logger.info("乾淨的控制台輸出")
logger.debug("帶時間戳的除錯資訊")
```

### Rich 控制台功能

```python
from pretty_loguru import create_logger

# 建立日誌記錄器實例
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# 在控制台使用視覺化功能
logger.block("狀態報告", [
    "✅ 資料庫：已連接",
    "✅ API：執行於連接埠 8000",
    "⚠️  快取：已使用 85%"
], border_style="green")

logger.ascii_header("系統啟動", font="slant")
```

## 📁 檔案日誌

檔案日誌將日誌儲存到磁碟，用於持久化、稽核和分析。

### 基本檔案設定

```python
from pretty_loguru import create_logger

# 僅使用檔案日誌
logger = create_logger(
    name="demo",
    log_path="logs",
    console_only=False  # 啟用檔案日誌
)

logger.info("這條訊息會儲存到檔案")
logger.error("錯誤會被持久化以供調查")
```

### 自訂檔案配置

```python
from pretty_loguru import create_logger

# 配置帶輪換的檔案日誌
logger = create_logger(
    name="my_app",
    level="INFO",
    log_path="application_logs",
    rotation="10MB",  # 檔案達到 10MB 時輪換
    retention="7 days",  # 保留日誌 7 天
    compression="gz"  # 壓縮舊檔案
)

logger.info("已啟用輪換的檔案日誌")
```

### 多個日誌檔案

```python
from pretty_loguru import create_logger, get_logger

# 初始化基礎日誌記錄器
logger = create_logger(
    name="multi_file",
    level="DEBUG", 
    log_path="logs"
)

# 使用 loguru 的原生功能添加特定錯誤檔案
logger.add(
    "logs/errors.log",
    level="ERROR",
    rotation="5MB",
    retention="30 days",
    format="{time} | {level} | {name}:{function}:{line} - {message}"
)

# 添加稽核追蹤檔案
logger.add(
    "logs/audit.log",
    level="INFO",
    filter=lambda record: "audit" in record["extra"],
    rotation="daily"
)

# 使用方式
logger.info("一般日誌訊息")
logger.error("這會同時記錄到一般日誌和錯誤日誌")
logger.bind(audit=True).info("稽核追蹤條目")  # 僅記錄到 audit.log
```

## 🔄 控制台 + 檔案組合日誌

最常見的設定是同時使用控制台和檔案輸出。

### 混合配置

```python
from pretty_loguru import create_logger

# 同時初始化控制台和檔案
logger = create_logger(
    name="web_app",
    level="DEBUG",
    log_path="logs"
    # console_only=False 是預設值
)

# 控制台顯示 INFO 及以上，檔案捕獲所有內容
logger.debug("除錯資訊（僅檔案）")
logger.info("資訊訊息（控制台 + 檔案）")
logger.error("錯誤訊息（控制台 + 檔案）")
```

### 控制台與檔案的不同等級

```python
from pretty_loguru import create_logger

# 基礎初始化
logger = create_logger(
    name="level_demo",
    level="DEBUG", 
    log_path="logs"
)

# 移除預設控制台處理器並添加自訂處理器
logger.remove()

# 控制台：INFO 及以上，帶顏色
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

# 檔案：包括除錯的所有內容
logger.add(
    "logs/app.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="20MB",
    retention="14 days"
)

# 測試不同等級
logger.debug("除錯：僅在檔案中")
logger.info("資訊：控制台和檔案")
logger.warning("警告：控制台和檔案")
logger.error("錯誤：控制台和檔案")
```

## 📊 比較表

| 功能 | 控制台日誌 | 檔案日誌 | 組合 |
|---------|----------------|--------------|----------|
| **持久性** | ❌ 重啟後遺失 | ✅ 永久儲存 | ✅ 兩全其美 |
| **即時監控** | ✅ 即時反饋 | ❌ 需手動檢查檔案 | ✅ 即時 + 歸檔 |
| **效能** | ⚠️ 可能拖慢應用 | ✅ 非同步寫入 | ⚠️ 中等影響 |
| **儲存** | ❌ 無儲存 | ⚠️ 需要磁碟空間 | ⚠️ 需要磁碟空間 |
| **分析** | ❌ 難以分析 | ✅ 日誌聚合工具 | ✅ 靈活分析 |
| **開發** | ✅ 非常適合開發 | ❌ 不太方便 | ✅ 理想設定 |
| **生產** | ❌ 不適合 | ✅ 稽核必需 | ✅ 推薦使用 |

## 🎯 何時使用

### 僅控制台
- **開發環境**
- **快速除錯會話**
- **互動式腳本**
- **一次性工具**

```python
# 開發設定
from pretty_loguru import create_logger

logger = create_logger(
    name="console_demo",
    log_path=None,  # 僅控制台
    level="INFO"
)
logger.info("非常適合開發")
```

### 僅檔案
- **背景服務**
- **批次處理**
- **無監控的生產系統**
- **無法存取控制台輸出時**

```python
# 背景服務
from pretty_loguru import create_logger
import sys

# 停用控制台輸出
logger = create_logger(
    name="background_service",
    level="INFO",
    log_path="service_logs"
)

# 移除所有控制台處理器
for handler_id in logger._core.handlers.copy():
    if logger._core.handlers[handler_id]._sink._stream in (sys.stdout, sys.stderr):
        logger.remove(handler_id)

logger.info("服務已啟動 - 僅記錄到檔案")
```

### 組合（推薦）
- **網路應用程式**
- **API 和微服務**
- **有監控的生產系統**
- **任何需要即時反饋和持久性的系統**

```python
# 生產就緒設定
from pretty_loguru import create_logger

logger = create_logger(
    name="api_server",
    level="INFO",
    log_path="logs",
    rotation="50MB",
    retention="30 days"
)

logger.info("API 伺服器啟動中...")
logger.success("伺服器準備就緒 - 同時記錄到控制台和檔案")
```

## 🔧 進階場景

### 基於環境的配置

```python
import os
from pretty_loguru import create_logger

env = os.getenv('ENVIRONMENT', 'development')

if env == 'development':
    # 開發：僅控制台，除錯等級
    logger = create_logger(name="dev", level="DEBUG", console_only=True)
elif env == 'testing':
    # 測試：僅檔案，避免混亂測試輸出
    logger = create_logger(name="test", level="INFO", log_path="test_logs", console_only=False)
    logger.remove()  # 移除控制台處理器
    logger.add("test_logs/test.log", level="INFO")
else:
    # 生產：控制台和檔案都使用
    logger = create_logger(
        name="prod_app",
        level="INFO",
        log_path="logs",
        rotation="100MB",
        retention="90 days"
    )

logger.info(f"日誌記錄器已配置為 {env} 環境")
```

### 動態切換

```python
from pretty_loguru import create_logger

class LoggerManager:
    def __init__(self):
        self.logger = create_logger(name="managed", level="INFO")
        self.file_handler_id = None
        self.console_handler_id = None
        
    def enable_console(self):
        if self.console_handler_id is None:
            self.console_handler_id = self.logger.add(
                sink=lambda msg: print(msg, end=""),
                format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
                level="INFO",
                colorize=True
            )
    
    def disable_console(self):
        if self.console_handler_id is not None:
            self.logger.remove(self.console_handler_id)
            self.console_handler_id = None
    
    def enable_file(self, path="logs/app.log"):
        if self.file_handler_id is None:
            self.file_handler_id = self.logger.add(
                path,
                level="DEBUG",
                rotation="10MB"
            )
    
    def disable_file(self):
        if self.file_handler_id is not None:
            self.logger.remove(self.file_handler_id)
            self.file_handler_id = None

# 使用方式
log_manager = LoggerManager()
log_manager.enable_console()
log_manager.logger.info("控制台已啟用")

log_manager.enable_file()
log_manager.logger.info("檔案日誌已啟用")

log_manager.disable_console()
log_manager.logger.info("控制台已停用 - 僅檔案")
```

根據您的應用程式需求和環境選擇正確的日誌策略！