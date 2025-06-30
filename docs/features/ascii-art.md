# ASCII 藝術標題

ASCII 藝術標題是 pretty-loguru 的特色功能之一，能夠建立引人注目的文字藝術標題，為你的日誌輸出增添專業感和視覺吸引力。

## 🎯 基本用法

### 簡單的 ASCII 標題

```python
from pretty_loguru import logger

# 最基本的 ASCII 標題
logger.ascii_header("HELLO WORLD")
```

### 帶參數的 ASCII 標題

```python
logger.ascii_header(
    "SYSTEM START",
    font="slant",           # 字體樣式
    border_style="blue",    # 邊框顏色
    log_level="INFO"        # 日誌級別
)
```

## 🎨 字體樣式

pretty-loguru 支援多種 ASCII 藝術字體，每種都有不同的視覺效果：

### 標準字體系列

#### standard - 標準字體
```python
logger.ascii_header("STANDARD", font="standard")
```
輸出效果：
```
 ____  _____  _     _   _  ____    _    ____  ____  
/ ___|_   _|/ \   | \ | |/ ___|  / \  |  _ \|  _ \ 
\___ \ | | / _ \  |  \| | |  _   / _ \ | |_) | | | |
 ___) || |/ ___ \ | |\  | |_| | / ___ \|  _ <| |_| |
|____/ |_/_/   \_\|_| \_|\____||_/   \_\_| \_\____/ 
```

#### slant - 斜體字
```python
logger.ascii_header("SLANT", font="slant")
```
輸出效果：
```
   _____ __    ___    _   ________
  / ___// /   /   |  / | / /_  __/
  \__ \/ /   / /| | /  |/ / / /   
 ___/ / /___/ ___ |/ /|  / / /    
/____/_____/_/  |_/_/ |_/ /_/     
```

#### doom - 粗體字
```python
logger.ascii_header("DOOM", font="doom")
```
輸出效果：
```
______   _____  _____ ___  ___ 
|  _  \ |  _  ||  _  ||  \/  |
| | | | | | | || | | || .  . |
| | | | | | | || | | || |\/| |
| |/ /  \ \_/ /\ \_/ /| |  | |
|___/    \___/  \___/ \_|  |_/
```

#### small - 小型字體
```python
logger.ascii_header("SMALL", font="small")
```
輸出效果：
```
 __  __  __   __    
(_  |\/| / /  |  |   
__) |  | \__  |__|__ 
```

#### block - 方塊字體
```python
logger.ascii_header("BLOCK", font="block")
```
輸出效果：
```
_|_|_|    _|        _|_|      _|_|_|  _|    _|
_|    _|  _|      _|    _|  _|        _|  _|  
_|_|_|    _|      _|    _|  _|        _|_|    
_|    _|  _|      _|    _|  _|        _|  _|  
_|_|_|    _|_|_|    _|_|      _|_|_|  _|    _|
```

### 特殊字體

#### digital - 數位字體
```python
logger.ascii_header("12345", font="digital")
```
輸出效果：
```
+-+-+ +-+-+ +-+-+ +-+-+ +-+-+
|1| | |2| | |3| | |4| | |5| |
+-+-+ +-+-+ +-+-+ +-+-+ +-+-+
```

#### banner - 橫幅字體
```python
logger.ascii_header("BANNER", font="banner")
```

## 🌈 邊框樣式和顏色

### 邊框顏色

```python
# 不同顏色的邊框
logger.ascii_header("SUCCESS", border_style="green")
logger.ascii_header("WARNING", border_style="yellow") 
logger.ascii_header("ERROR", border_style="red")
logger.ascii_header("INFO", border_style="blue")
logger.ascii_header("SPECIAL", border_style="magenta")
logger.ascii_header("NEUTRAL", border_style="cyan")
```

### 邊框樣式

```python
# 不同樣式的邊框
logger.ascii_header("SOLID", border_style="solid")
logger.ascii_header("DOUBLE", border_style="double")
logger.ascii_header("ROUNDED", border_style="rounded")
logger.ascii_header("THICK", border_style="thick")
```

## 📊 日誌級別控制

ASCII 標題可以與不同的日誌級別結合：

```python
# 不同級別的 ASCII 標題
logger.ascii_header("DEBUG MODE", log_level="DEBUG")
logger.ascii_header("APP START", log_level="INFO")
logger.ascii_header("SUCCESS", log_level="SUCCESS")
logger.ascii_header("WARNING", log_level="WARNING")
logger.ascii_header("ERROR", log_level="ERROR")
logger.ascii_header("CRITICAL", log_level="CRITICAL")
```

## 🎮 實際應用場景

### 應用程式啟動

```python
def startup_sequence():
    logger.ascii_header("APP STARTUP", font="slant", border_style="blue")
    
    logger.info("正在載入配置...")
    logger.success("配置載入完成")
    
    logger.info("正在連接資料庫...")
    logger.success("資料庫連接成功")
    
    logger.ascii_header("READY", font="block", border_style="green")
```

### 錯誤處理

```python
def handle_critical_error(error):
    logger.ascii_header("ERROR", font="doom", border_style="red")
    logger.error(f"發生嚴重錯誤：{error}")
    logger.ascii_header("SHUTDOWN", font="standard", border_style="red")
```

### 階段標記

```python
def data_processing_pipeline():
    logger.ascii_header("PHASE 1", font="small", border_style="cyan")
    logger.info("開始數據提取...")
    
    logger.ascii_header("PHASE 2", font="small", border_style="cyan")
    logger.info("開始數據轉換...")
    
    logger.ascii_header("PHASE 3", font="small", border_style="cyan")  
    logger.info("開始數據載入...")
    
    logger.ascii_header("COMPLETE", font="slant", border_style="green")
```

### 系統監控

```python
def system_status_check():
    logger.ascii_header("HEALTH CHECK", font="standard", border_style="blue")
    
    # 檢查各個服務
    services = ["Database", "Redis", "API", "Queue"]
    
    for service in services:
        status = check_service(service)
        if status:
            logger.success(f"{service}: 運行正常")
        else:
            logger.error(f"{service}: 服務異常")
    
    logger.ascii_header("CHECK COMPLETE", font="small", border_style="green")
```

## ⚠️ 使用注意事項

### 文字限制

ASCII 藝術僅支援 ASCII 字符，使用非 ASCII 字符會產生錯誤：

```python
# 正確 - 僅 ASCII 字符
logger.ascii_header("HELLO WORLD")

# 錯誤 - 包含非 ASCII 字符
try:
    logger.ascii_header("你好世界")  # 這會拋出錯誤
except ValueError as e:
    logger.error(f"ASCII 錯誤：{e}")
```

### 檢查字串是否為 ASCII

```python
from pretty_loguru import is_ascii_only

text = "HELLO WORLD"
if is_ascii_only(text):
    logger.ascii_header(text)
else:
    logger.warning("文字包含非 ASCII 字符，使用普通標題")
    logger.info(f"=== {text} ===")
```

### 長度建議

為了最佳視覺效果，建議：
- 標題長度控制在 20 個字符以內
- 避免使用過長的文字
- 使用簡潔有力的詞語

```python
# 推薦 - 簡潔明瞭
logger.ascii_header("START")
logger.ascii_header("COMPLETE")
logger.ascii_header("ERROR")

# 不推薦 - 過長
logger.ascii_header("VERY LONG TITLE THAT MIGHT NOT LOOK GOOD")
```

## 🔧 進階技巧

### 動態字體選擇

```python
import random

def random_header(text):
    fonts = ["standard", "slant", "doom", "small", "block"]
    colors = ["blue", "green", "cyan", "magenta"]
    
    font = random.choice(fonts)
    color = random.choice(colors)
    
    logger.ascii_header(text, font=font, border_style=color)

# 每次執行都會有不同的效果
random_header("SURPRISE")
```

### 組合使用

```python
def deployment_complete():
    # 開始標題
    logger.ascii_header("DEPLOY", font="slant", border_style="blue")
    
    # 處理過程...
    logger.info("部署中...")
    
    # 成功標題
    logger.ascii_header("SUCCESS", font="block", border_style="green")
```

### 條件式標題

```python
def status_header(success: bool):
    if success:
        logger.ascii_header("SUCCESS", font="block", border_style="green")
    else:
        logger.ascii_header("FAILED", font="doom", border_style="red")

# 根據結果顯示不同標題
result = some_operation()
status_header(result.success)
```

## 🚀 下一步

現在你已經掌握了 ASCII 藝術標題的用法，可以：

- [探索 ASCII 藝術區塊](./ascii-blocks) - 結合標題和內容的強大功能
- [了解 Rich 區塊](./rich-blocks) - 結構化的視覺日誌
- [查看完整範例](../examples/visual/) - 視覺化功能的實際應用

讓你的日誌輸出更加引人注目！