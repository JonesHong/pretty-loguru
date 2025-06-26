# Logger 同步問題解決方案

## 問題描述

當您在獨立的 `.py` 檔案中創建 logger，然後其他檔案 import 來使用時，如果在 `init_logger` 時重新創建新的 logger 實例，已經 import 的地方不會同步到新的實例。

## 問題範例

```python
# logger_config.py
from pretty_loguru import create_logger

logger = create_logger("app_logger")  # 物件 A

def init_logger():
    global logger
    logger = create_logger("app_logger", log_path="./logs")  # 物件 B
    # logger_config.py 中的 logger 現在指向物件 B

# main.py
from logger_config import logger  # 取得物件 A 的引用

# 即使調用 init_logger()，main.py 中的 logger 仍然是物件 A！
```

## 解決方案

### 方案 1: 使用 Logger Proxy（推薦）

```python
# logger_config.py
from pretty_loguru import create_logger, reinit_logger

# 使用 proxy 模式創建 logger
logger = create_logger("app_logger", use_proxy=True)

def init_logger(**kwargs):
    """重新初始化 logger，所有引用會自動同步"""
    return reinit_logger("app_logger", **kwargs)

# main.py
from logger_config import logger, init_logger

# 使用 logger
logger.info("初始訊息")

# 重新初始化
init_logger(log_path="./logs", level="DEBUG")

# logger 自動同步到新配置！
logger.info("重新初始化後的訊息")  # 會使用新配置
```

### 方案 2: 使用註冊表 + Getter 函數

```python
# logger_config.py
from pretty_loguru import create_logger, get_logger

# 創建並註冊 logger
create_logger("app_logger")

def get_app_logger():
    """總是返回最新的 logger 實例"""
    return get_logger("app_logger")

def init_logger(**kwargs):
    """重新初始化 logger"""
    return create_logger("app_logger", force_new_instance=True, **kwargs)

# main.py
from logger_config import get_app_logger, init_logger

# 使用 getter 函數
logger = get_app_logger()
logger.info("初始訊息")

# 重新初始化
init_logger(log_path="./logs", level="DEBUG")

# 重新取得 logger
logger = get_app_logger()  # 獲得新實例
logger.info("重新初始化後的訊息")
```

### 方案 3: 重新配置現有實例（限制較多）

```python
# logger_config.py
from pretty_loguru import create_logger, configure_logger

logger = create_logger("app_logger")

def init_logger(**kwargs):
    """重新配置現有 logger"""
    # 獲取真實的 logger 實例
    real_logger = logger.get_real_logger() if hasattr(logger, 'get_real_logger') else logger
    
    # 重新配置
    configure_logger(logger_instance=real_logger, **kwargs)
    
    return logger

# main.py 
from logger_config import logger, init_logger

# 使用相同的實例，但重新配置
logger.info("初始訊息")
init_logger(log_path="./logs", level="DEBUG")
logger.info("重新配置後的訊息")  # 使用新配置
```

## API 參考

### create_logger 新參數

```python
def create_logger(
    name: Optional[str] = None,
    use_proxy: bool = False,  # 新增：是否使用 proxy 模式
    # ... 其他參數
) -> EnhancedLogger:
```

### reinit_logger 函數

```python
def reinit_logger(name: str, **kwargs) -> Optional[EnhancedLogger]:
    """
    重新初始化已存在的 logger
    
    Args:
        name: 要重新初始化的 logger 名稱
        **kwargs: 傳遞給 create_logger 的參數
        
    Returns:
        重新初始化的 logger，如果原 logger 不存在則返回 None
    """
```

## 最佳實踐

### 1. 對於需要重新初始化的 Logger

```python
# 推薦：使用 proxy 模式
logger = create_logger("my_app", use_proxy=True)

# 重新初始化時
reinit_logger("my_app", log_path="./logs", level="DEBUG")
```

### 2. 對於簡單的使用場景

```python
# 使用 getter 函數模式
def get_logger():
    return get_logger("my_app") or create_logger("my_app")
```

### 3. 模組結構建議

```python
# config/logger_config.py
from pretty_loguru import create_logger, reinit_logger

# 創建全局 logger（使用 proxy）
app_logger = create_logger("app", use_proxy=True)
api_logger = create_logger("api", use_proxy=True)

def init_loggers(log_path: str = "./logs", level: str = "INFO"):
    """初始化所有 loggers"""
    reinit_logger("app", log_path=log_path, level=level)
    reinit_logger("api", log_path=f"{log_path}/api", level=level)

# modules/api.py
from config.logger_config import api_logger

def handle_request():
    api_logger.info("處理請求")  # 總是使用最新配置

# main.py
from config.logger_config import init_loggers

if __name__ == "__main__":
    # 初始化 loggers
    init_loggers(log_path="./production_logs", level="WARNING")
    
    # 其他模組會自動使用新配置
```

## 注意事項

1. **效能考量**：Proxy 模式會有輕微的效能開銷
2. **型別提示**：Proxy 物件可能會影響 IDE 的型別提示
3. **除錯**：如果需要除錯，可以使用 `logger.get_real_logger()` 獲取真實實例
4. **向後兼容**：現有程式碼無需修改，只需在需要時添加 `use_proxy=True`