# 快速開始範例

本頁展示 Pretty-Loguru 的快速上手範例。

## Hello World

最簡單的使用方式：

```python
#!/usr/bin/env python3
"""
🎯 Pretty-Loguru Hello World
最簡單的使用範例 - 3行程式碼開始美化日誌
"""

from pretty_loguru import create_logger

# 創建 logger
logger = create_logger("hello_world")

# 開始記錄
logger.info("Hello, Pretty-Loguru! 🌟")
logger.success("恭喜！您已經成功使用 Pretty-Loguru")
logger.warning("這是一個警告訊息")
logger.error("這是一個錯誤訊息")
```

運行結果：
```
2025-07-12 21:47:50 | INFO    | hello_world:main:27 - Hello, Pretty-Loguru! 🌟
2025-07-12 21:47:50 | SUCCESS | hello_world:main:28 - 恭喜！您已經成功使用 Pretty-Loguru
2025-07-12 21:47:50 | WARNING | hello_world:main:29 - 這是一個警告訊息
2025-07-12 21:47:50 | ERROR   | hello_world:main:30 - 這是一個錯誤訊息
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/hello_world.py)

## 控制台日誌

只輸出到控制台的設定：

```python
from pretty_loguru import create_logger

# 創建只輸出到控制台的 logger（不指定 log_path）
logger = create_logger("console_app")

# 基本日誌級別
logger.debug("除錯訊息 - 用於開發時的詳細資訊")
logger.info("一般訊息 - 程式正常運行的資訊")
logger.success("成功訊息 - 操作成功完成")
logger.warning("警告訊息 - 需要注意但不影響運行")
logger.error("錯誤訊息 - 發生錯誤但程式可以繼續")
logger.critical("嚴重錯誤 - 程式可能無法繼續運行")

# 使用視覺化功能
logger.block(
    "系統狀態",
    [
        "🟢 服務狀態: 正常運行",
        "📊 CPU 使用率: 45%",
        "💾 記憶體使用: 2.3GB / 8GB",
        "🌡️ 系統溫度: 正常"
    ],
    border_style="green"
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/console_logging.py)

## 檔案日誌

同時輸出到控制台和檔案：

```python
from pretty_loguru import create_logger

# 創建同時輸出到控制台和檔案的 logger
logger = create_logger(
    "file_app",
    log_path="logs",           # 日誌目錄
    rotation="1 day",          # 每天輪替
    retention="7 days",        # 保留 7 天
    compression="zip"          # 壓縮舊檔案
)

# 記錄不同類型的日誌
logger.info("應用程序啟動")
logger.debug("載入配置檔案: config.json")
logger.success("資料庫連接成功")
logger.warning("快取即將過期")
logger.error("無法連接到外部 API")

# ASCII 藝術標題（同時出現在控制台和檔案）
logger.ascii_header("APP START", font="small")

# 結構化日誌
logger.block(
    "啟動資訊",
    [
        f"版本: v1.0.0",
        f"環境: production",
        f"配置: config.json",
        f"日誌路徑: logs/"
    ],
    border_style="blue"
)
```

檔案輸出位置：
- 控制台：彩色格式化輸出
- 檔案：`logs/[file_app]_YYYYMMDD.log`（純文字格式）

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/file_logging.py)

## 下一步

- [基礎功能](./basics.md) - 深入了解核心功能
- [視覺化功能](./visual.md) - Rich 區塊和 ASCII 藝術
- [配置管理](./configuration.md) - 進階配置選項