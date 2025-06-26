# Console Only Behavior - 控制台專用行為

## 概述

從這個版本開始，`pretty-loguru` 的行為更接近原生 `loguru`：

**當沒有明確指定 `log_path` 時，將只輸出到控制台，不會自動創建日誌檔案。**

## 行為對比

### 舊行為（之前的版本）
```python
from pretty_loguru import create_logger

# 這會自動創建 logs/ 目錄和日誌檔案
logger = create_logger()  
logger.info("訊息")  # 同時輸出到控制台和檔案
```

### 新行為（當前版本）
```python
from pretty_loguru import create_logger

# 僅輸出到控制台，不創建任何檔案
logger = create_logger()  
logger.info("訊息")  # 只輸出到控制台

# 明確指定 log_path 才會創建檔案
logger_with_file = create_logger("my_service", log_path="./logs")
logger_with_file.info("訊息")  # 同時輸出到控制台和檔案
```

## 觸發條件

以下情況會**只輸出到控制台**（不創建檔案）：
- `log_path=None`（預設值）
- `log_path=""`（空字符串）

以下情況會**創建日誌檔案**：
- `log_path="./logs"`（任何有效路徑）
- `log_path=Path("./logs")`（Path 物件）

## 使用範例

### 1. 開發模式（僅控制台）
```python
from pretty_loguru import create_logger

# 開發時，只需要看控制台輸出
dev_logger = create_logger("dev_app")
dev_logger.info("開發中的訊息")  # 只在控制台顯示
```

### 2. 生產模式（控制台 + 檔案）
```python
from pretty_loguru import create_logger

# 生產環境需要持久化日誌
prod_logger = create_logger("prod_app", log_path="./logs")
prod_logger.info("生產環境訊息")  # 控制台 + 檔案
```

### 3. 混合使用
```python
from pretty_loguru import create_logger

# 不同的 logger 有不同的行為
console_logger = create_logger("console_app")  # 僅控制台
file_logger = create_logger("file_app", log_path="./logs")  # 控制台 + 檔案

console_logger.info("這只在控制台顯示")
file_logger.info("這會同時輸出到控制台和檔案")
```

## 格式行為

與格式相關的行為保持不變：

```python
# 沒有提供 name：使用原生 loguru 格式（{file}）
logger1 = create_logger()

# 提供了 name：使用 pretty-loguru 格式（{extra[folder]}）
logger2 = create_logger("my_service")

# 都只輸出到控制台（因為沒有指定 log_path）
```

## 向後兼容

此變更可能會影響現有程式碼，如果您的程式依賴自動檔案創建，請：

1. **明確指定 `log_path`**：
   ```python
   # 舊代碼
   logger = create_logger("my_app")
   
   # 新代碼（保持檔案輸出）
   logger = create_logger("my_app", log_path="./logs")
   ```

2. **使用環境變數或配置**：
   ```python
   import os
   
   log_path = os.getenv("LOG_PATH", "./logs") if os.getenv("ENABLE_FILE_LOGGING") else None
   logger = create_logger("my_app", log_path=log_path)
   ```

## file_xxx 方法的行為

當沒有指定 `log_path` 時，調用 `file_xxx` 方法會：

1. **發出 UserWarning 警告**
2. **自動降級到控制台輸出**
3. **確保訊息不會丟失**

```python
from pretty_loguru import create_logger
import warnings

# 沒有指定 log_path
logger = create_logger("test")

# 這會發出警告並輸出到控制台
logger.file_info("這條訊息會有警告")
# UserWarning: 調用了 file_info 方法，但此 logger 沒有配置檔案輸出（未指定 log_path）。
# 訊息將輸出到控制台。若要啟用檔案輸出，請在創建 logger 時指定 log_path 參數。

# 正確的做法
logger_with_file = create_logger("test", log_path="./logs")
logger_with_file.file_info("這條訊息會正常寫入檔案")  # 無警告
```

### 隱藏警告

如果您確定要在沒有檔案輸出的情況下使用 `file_xxx` 方法，可以隱藏警告：

```python
import warnings
from pretty_loguru import create_logger

with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    logger = create_logger("test")
    logger.file_info("不會顯示警告")
```

## 優點

1. **更接近 loguru 原生行為**
2. **避免意外的檔案創建**
3. **更適合開發環境**
4. **減少不必要的磁碟 I/O**
5. **給予用戶更多控制權**
6. **智能降級處理，確保訊息不丟失**
7. **清楚的警告訊息指導用戶正確使用**