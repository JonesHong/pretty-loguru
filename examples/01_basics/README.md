# 01_basics - 核心功能 (3分鐘上手)

這個目錄包含 pretty-loguru 的核心功能範例，讓您在 3 分鐘內快速上手。

## 🎯 學習目標

- 掌握 `create_logger` 基本用法
- 理解控制台與檔案輸出的差異
- 學會使用目標導向的日誌方法

## 📚 範例列表

### 1. simple_usage.py - 最基本使用
**學習重點**: 創建 logger、基本日誌輸出、不同日誌級別

```bash
python simple_usage.py
```

**您會學到**:
- 如何創建最簡單的 logger
- 基本的日誌級別使用
- 如何添加檔案輸出

### 2. console_vs_file.py - 輸出目標對比  
**學習重點**: 控制台輸出 vs 檔案輸出的使用場景

```bash
python console_vs_file.py
```

**您會學到**:
- 什麼時候使用控制台輸出
- 什麼時候使用檔案輸出
- 實際應用場景示範

### 3. target_logging.py - 目標導向方法
**學習重點**: console_* 和 file_* 系列方法的使用

```bash
python target_logging.py
```

**您會學到**:
- `console_info()`, `console_error()` 等方法
- `file_debug()`, `file_warning()` 等方法
- 用戶註冊和錯誤處理的實際範例

## 🚀 快速開始

1. **運行第一個範例**:
   ```bash
   cd 01_basics
   python simple_usage.py
   ```

2. **檢查生成的日誌檔案**:
   ```bash
   ls ./logs/
   cat ./logs/*.log
   ```

3. **嘗試其他範例**:
   ```bash
   python console_vs_file.py
   python target_logging.py
   ```

## 💡 核心概念

### Logger 創建
```python
# 最簡單的方式 - 僅控制台
logger = create_logger("my_app")

# 添加檔案輸出
logger = create_logger("my_app", log_path="./logs")
```

### 基本日誌級別
```python
logger.debug("除錯資訊")
logger.info("一般資訊") 
logger.warning("警告訊息")
logger.error("錯誤訊息")
logger.success("成功訊息")
```

### 目標導向輸出
```python
# 僅控制台輸出
logger.console_info("用戶看到的訊息")

# 僅檔案輸出  
logger.file_debug("系統內部資訊")
```

## 📁 生成的檔案

運行範例後，您會看到：
```
logs/
├── my_app_YYYYMMDD-HHMMSS.log
├── demo_app_YYYYMMDD-HHMMSS.log
├── user_service_YYYYMMDD-HHMMSS.log
└── payment_service_YYYYMMDD-HHMMSS.log
```

## ➡️ 下一步

完成這些範例後，建議繼續學習：
- **02_visual/** - 視覺化功能和美化輸出
- **04_fastapi/** - Web 應用整合 (如果您開發 Web 應用)
- **03_presets/** - 檔案管理和輪替策略

## 🤔 常見問題

**Q: 為什麼要分控制台和檔案輸出？**
A: 控制台適合給用戶看的簡潔訊息，檔案適合系統記錄的詳細資訊。

**Q: 日誌檔案儲存在哪裡？**
A: 預設在 `./logs/` 目錄，可以透過 `log_path` 參數修改。

**Q: 如何選擇合適的日誌級別？**
A: `debug` 用於除錯、`info` 用於一般資訊、`warning` 用於警告、`error` 用於錯誤、`success` 用於成功操作。