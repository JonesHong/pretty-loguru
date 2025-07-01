# 簡單用法

這是使用 pretty-loguru 的最基本範例，展示如何快速開始記錄日誌。

## 🎯 學習目標

- 了解 `logger_start()` 的用法
- 掌握基本的日誌級別
- 理解日誌檔案的自動管理

## 💻 基礎範例

### 最簡單的開始

```python
from pretty_loguru import create_logger

# 初始化日誌系統
component_name = logger = create_logger(
    name="simple-usage_demo",
    log_path="simple_logs",
    level="INFO"
)
print(f"日誌元件 ID: {component_name}")

# 基本日誌輸出
logger.debug("這是除錯訊息")
logger.info("這是一般訊息")
logger.success("這是成功訊息")  # pretty-loguru 特有的成功級別
logger.warning("這是警告訊息")
logger.error("這是錯誤訊息")
logger.critical("這是嚴重錯誤訊息")
```

### 運行結果

**控制台輸出：**
```
日誌元件 ID: simple_logs_20240630_143022
2024-06-30 14:30:22.123 | DEBUG    | __main__:<module>:8 - 這是除錯訊息
2024-06-30 14:30:22.124 | INFO     | __main__:<module>:9 - 這是一般訊息
2024-06-30 14:30:22.125 | SUCCESS  | __main__:<module>:10 - 這是成功訊息
2024-06-30 14:30:22.126 | WARNING  | __main__:<module>:11 - 這是警告訊息
2024-06-30 14:30:22.127 | ERROR    | __main__:<module>:12 - 這是錯誤訊息
2024-06-30 14:30:22.128 | CRITICAL | __main__:<module>:13 - 這是嚴重錯誤訊息
```

**檔案輸出：**
在 `simple_logs/` 目錄下會產生一個日誌檔案，例如：
`[simple_logs_20240630_143022]_20240630-143022.log`

## 🔧 參數說明

### `logger_start()` 參數

```python
component_name = logger_start(
    folder="logs",           # 日誌資料夾名稱
    level="DEBUG",           # 日誌級別（可選）
    rotation="10MB",         # 檔案輪換大小（可選）
    retention="7 days"       # 保留天數（可選）
)
```

### 日誌級別說明

| 級別 | 用途 | 顏色 |
|------|------|------|
| `DEBUG` | 除錯資訊 | 藍色 |
| `INFO` | 一般資訊 | 白色 |
| `SUCCESS` | 成功訊息 | 綠色 |
| `WARNING` | 警告訊息 | 黃色 |
| `ERROR` | 錯誤訊息 | 紅色 |
| `CRITICAL` | 嚴重錯誤 | 紅色（粗體） |

## 🎮 實際練習

### 練習 1：基本日誌

建立一個簡單的 Python 腳本：

```python
# practice_1.py
from pretty_loguru import create_logger

def main():
    # 初始化日誌
    component_name = logger = create_logger(
    name="simple-usage_demo",
    log_path="practice_logs",
    level="INFO"
)
    
    # 模擬應用程式啟動
    logger.info("應用程式開始啟動...")
    logger.debug("載入設定檔...")
    logger.success("設定檔載入成功")
    
    # 模擬一些操作
    logger.info("連接資料庫...")
    logger.success("資料庫連接成功")
    
    logger.info("啟動 Web 伺服器...")
    logger.success("伺服器啟動完成，監聽埠 8080")
    
    logger.warning("記憶體使用率較高：75%")
    
    # 模擬錯誤
    try:
        result = 1 / 0  # 這會產生錯誤
    except ZeroDivisionError:
        logger.error("發生除零錯誤")
    
    logger.critical("應用程式即將關閉")

if __name__ == "__main__":
    main()
```

### 練習 2：不同級別測試

```python
# practice_2.py
from pretty_loguru import create_logger
import time

def test_all_levels():
    logger = create_logger(
    name="simple-usage_demo",
    log_path="level_test",
    level="INFO"
)
    
    # 測試所有日誌級別
    levels = [
        ("debug", "除錯模式已啟用"),
        ("info", "系統運行正常"),
        ("success", "任務執行成功"),
        ("warning", "磁碟空間不足"),
        ("error", "網路連接失敗"),
        ("critical", "系統即將崩潰")
    ]
    
    for level, message in levels:
        getattr(logger, level)(f"{level.upper()}: {message}")
        time.sleep(0.5)  # 稍等一下以便觀察

if __name__ == "__main__":
    test_all_levels()
```

## 📁 檔案結構

執行範例後，你的目錄結構會是：

```
your_project/
├── practice_1.py
├── practice_2.py
├── practice_logs/
│   └── [practice_logs_20240630_143022]_20240630-143022.log
└── level_test/
    └── [level_test_20240630_143500]_20240630-143500.log
```

## 💡 重要概念

### 1. 自動元件命名
`logger_start()` 會自動產生一個唯一的元件名稱，格式為：
`{folder_name}_{timestamp}`

### 2. 同時輸出
預設情況下，日誌會同時：
- 在控制台顯示（帶顏色）
- 寫入檔案（純文字）

### 3. 自動檔案管理
pretty-loguru 會自動：
- 建立日誌資料夾
- 產生時間戳檔名
- 管理檔案輪換

## ❓ 常見問題

### Q: 為什麼我看不到 DEBUG 級別的日誌？
A: 預設情況下，DEBUG 級別在生產環境可能被過濾。可以明確設定：
```python
logger = create_logger(
    name="simple-usage_demo",
    log_path="logs", level="DEBUG",
    level="INFO"
)
```

### Q: 如何自定義日誌格式？
A: 這屬於進階功能，請參考 [自定義配置](../../guide/custom-config) 章節。

### Q: 日誌檔案太多怎麼辦？
A: 可以設定自動清理：
```python
logger = create_logger(
    name="simple-usage_demo",
    log_path="logs", retention="7 days",
    level="INFO"
)
```

## 🚀 下一步

恭喜！你已經掌握了 pretty-loguru 的基礎用法。接下來可以：

- [了解控制台 vs 檔案輸出](./console-vs-file) - 學習精確控制輸出
- [探索視覺化功能](../visual/) - 體驗 Rich 區塊和 ASCII 藝術
- [查看進階配置](../../guide/custom-config) - 深度自定義

你現在已經可以在任何 Python 專案中使用 pretty-loguru 了！ 🎉