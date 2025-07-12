# 基礎用法範例

這裡展示 pretty-loguru 的基本功能，適合初學者快速上手。

## 📖 本章內容

- **[簡單用法](./simple-usage)** - 最基本的初始化和日誌輸出
- **[控制台 vs 檔案](./console-vs-file)** - 了解不同輸出目標的差異
- **[目標導向日誌](./target-logging)** - 精確控制日誌輸出位置

## 🚀 快速預覽

### 簡單開始

```python
from pretty_loguru import create_logger

# 一行初始化
logger  = create_logger(
    name="basics_demo",
    log_path="my_logs",
    level="INFO"
)

# 開始記錄日誌
logger.info("應用程式已啟動")
logger.success("初始化完成")
logger.warning("這是一個警告")
logger.error("這是一個錯誤")
```

### 控制台 vs 檔案輸出

```python
# 同時輸出到控制台和檔案（預設）
logger.info("這會出現在兩個地方")

# 只輸出到控制台
logger.console_info("只在控制台顯示")

# 只寫入檔案
logger.file_info("只寫入日誌檔案")
```

### 目標導向日誌

```python
# 不同級別的目標導向日誌
logger.console_debug("控制台除錯訊息")
logger.file_debug("檔案除錯訊息")
logger.console_error("控制台錯誤訊息")
logger.file_error("檔案錯誤訊息")
```

## ⏱️ 學習時間

- **總計**: 約 10 分鐘
- **簡單用法**: 2 分鐘
- **控制台 vs 檔案**: 3 分鐘  
- **目標導向日誌**: 5 分鐘

## 🎯 學習目標

完成這個章節後，你將能夠：

✅ 正確初始化 pretty-loguru  
✅ 使用基本的日誌級別  
✅ 理解控制台和檔案輸出的區別  
✅ 精確控制日誌的輸出目標  

## 🚀 開始學習

選擇一個範例開始：

- 👶 **新手**: 從 [簡單用法](./simple-usage) 開始
- 🎯 **進階**: 直接查看 [目標導向日誌](./target-logging)

準備好了嗎？讓我們開始！ 🎮