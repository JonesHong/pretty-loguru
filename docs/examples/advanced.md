# 進階功能範例

展示 Pretty-Loguru 的進階功能，包括直接存取底層庫、自定義擴展和性能優化。

## 直接存取 Loguru

存取底層的 Loguru 功能：

```python
from pretty_loguru import create_logger
from loguru import logger as loguru_logger

# 創建 Pretty-Loguru logger
pretty_logger = create_logger("advanced")

# 存取底層 Loguru logger
# Pretty-Loguru 的 logger 是 Loguru 的增強版本
pretty_logger.info("這是 Pretty-Loguru 的日誌")

# 使用 Loguru 的進階功能
@pretty_logger.catch(message="處理函數發生錯誤")
def risky_function(x):
    return 1 / x

# 使用 Loguru 的 bind 功能
request_logger = pretty_logger.bind(request_id="12345")
request_logger.info("處理請求")

# 使用 Loguru 的 opt 功能
pretty_logger.opt(colors=True, capture=False).info("彩色日誌")
pretty_logger.opt(depth=1).info("調整調用深度")

# 使用 Loguru 的序列化功能
pretty_logger.add(
    "logs/json_logs.json",
    serialize=True,  # JSON 格式
    rotation="1 day"
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/07_advanced/direct_library_access.py)

## 自定義格式化器

創建自定義的日誌格式化器：

```python
from pretty_loguru import create_logger
import json
from typing import Dict, Any

def custom_formatter(record: Dict[str, Any]) -> str:
    """自定義格式化器 - 結構化日誌"""
    log_entry = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "logger": record["name"],
        "message": record["message"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
    }
    
    # 添加額外字段
    if record.get("extra"):
        log_entry["extra"] = record["extra"]
    
    # 添加異常資訊
    if record.get("exception"):
        log_entry["exception"] = {
            "type": record["exception"].type.__name__,
            "value": str(record["exception"].value),
            "traceback": record["exception"].traceback
        }
    
    return json.dumps(log_entry, ensure_ascii=False) + "\n"

# 使用自定義格式化器
logger = create_logger("custom_format")

# 添加自定義格式的處理器
logger.add(
    "logs/structured.log",
    format=custom_formatter,
    rotation="100 MB"
)

# 記錄結構化日誌
logger.bind(
    user_id=123,
    action="login",
    ip="192.168.1.1"
).info("用戶登入")
```

## 性能優化

優化日誌性能的技巧：

```python
from pretty_loguru import create_logger
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# 1. 異步日誌
class AsyncLogger:
    def __init__(self, logger):
        self.logger = logger
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    async def log_async(self, level, message, **kwargs):
        """異步記錄日誌"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            lambda: getattr(self.logger, level)(message, **kwargs)
        )
    
    async def info(self, message, **kwargs):
        await self.log_async("info", message, **kwargs)
    
    async def error(self, message, **kwargs):
        await self.log_async("error", message, **kwargs)

# 2. 批量日誌
class BatchLogger:
    def __init__(self, logger, batch_size=100, flush_interval=1.0):
        self.logger = logger
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer = []
        self.last_flush = time.time()
    
    def log(self, level, message, **kwargs):
        """添加到緩衝區"""
        self.buffer.append({
            "level": level,
            "message": message,
            "kwargs": kwargs,
            "time": time.time()
        })
        
        # 檢查是否需要刷新
        if len(self.buffer) >= self.batch_size or \
           time.time() - self.last_flush > self.flush_interval:
            self.flush()
    
    def flush(self):
        """刷新緩衝區"""
        if not self.buffer:
            return
        
        # 批量記錄
        self.logger.info(f"批量日誌 ({len(self.buffer)} 條)")
        for entry in self.buffer:
            getattr(self.logger, entry["level"])(
                entry["message"], 
                **entry["kwargs"]
            )
        
        self.buffer.clear()
        self.last_flush = time.time()

# 3. 條件日誌
class ConditionalLogger:
    def __init__(self, logger):
        self.logger = logger
        self.enabled = True
        self.filters = []
    
    def add_filter(self, filter_func):
        """添加過濾器"""
        self.filters.append(filter_func)
    
    def should_log(self, level, message):
        """檢查是否應該記錄"""
        if not self.enabled:
            return False
        
        for filter_func in self.filters:
            if not filter_func(level, message):
                return False
        
        return True
    
    def log(self, level, message, **kwargs):
        """條件記錄"""
        if self.should_log(level, message):
            getattr(self.logger, level)(message, **kwargs)

# 使用範例
base_logger = create_logger("performance")

# 異步記錄
async_logger = AsyncLogger(base_logger)

async def async_task():
    await async_logger.info("異步日誌記錄")
    await async_logger.error("異步錯誤記錄")

# 批量記錄
batch_logger = BatchLogger(base_logger)
for i in range(150):
    batch_logger.log("info", f"批量消息 {i}")
batch_logger.flush()

# 條件記錄
cond_logger = ConditionalLogger(base_logger)
cond_logger.add_filter(lambda level, msg: level != "debug")
cond_logger.add_filter(lambda level, msg: "sensitive" not in msg)
```

## 自定義擴展

創建可重用的日誌擴展：

```python
from pretty_loguru import create_logger
from functools import wraps
import inspect

class LoggerExtension:
    """Logger 擴展基類"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def trace_calls(self, func):
        """函數調用追蹤裝飾器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            func_args = inspect.signature(func).bind(*args, **kwargs)
            func_args.apply_defaults()
            
            self.logger.debug(
                f"Calling {func_name}",
                arguments=dict(func_args.arguments)
            )
            
            try:
                result = func(*args, **kwargs)
                self.logger.debug(
                    f"Completed {func_name}",
                    result=result
                )
                return result
            except Exception as e:
                self.logger.error(
                    f"Failed {func_name}",
                    error=str(e),
                    error_type=type(e).__name__
                )
                raise
        
        return wrapper
    
    def log_context(self, **context):
        """上下文管理器"""
        class ContextLogger:
            def __init__(self, logger, context):
                self.logger = logger
                self.context = context
            
            def __enter__(self):
                self.logger.info(
                    "Entering context",
                    **self.context
                )
                return self.logger.bind(**self.context)
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type:
                    self.logger.error(
                        "Context failed",
                        error=str(exc_val),
                        **self.context
                    )
                else:
                    self.logger.info(
                        "Exiting context",
                        **self.context
                    )
        
        return ContextLogger(self.logger, context)

# 使用擴展
logger = create_logger("extended")
ext = LoggerExtension(logger)

# 函數追蹤
@ext.trace_calls
def calculate(x, y, operation="+"):
    operations = {
        "+": x + y,
        "-": x - y,
        "*": x * y,
        "/": x / y
    }
    return operations.get(operation, 0)

# 上下文日誌
with ext.log_context(user_id=123, action="purchase"):
    # 在上下文中的所有日誌都會包含 user_id 和 action
    logger.info("處理購買請求")
    logger.success("購買完成")
```

## 整合第三方庫

與其他日誌相關庫整合：

```python
# 整合 structlog
import structlog
from pretty_loguru import create_logger

# 創建 Pretty-Loguru logger
pretty_logger = create_logger("integrated")

# 配置 structlog 使用 Pretty-Loguru
structlog.configure(
    logger_factory=lambda: pretty_logger,
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# 使用 structlog API
log = structlog.get_logger()
log.info("使用 structlog API", user="alice", action="login")

# 整合 Python logging
import logging
from pretty_loguru import InterceptHandler

# 攔截標準 logging
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 現在 logging 模組的日誌會被 Pretty-Loguru 處理
logging.info("這是來自 logging 模組的訊息")
```

## 性能測試

測試和比較日誌性能：

```python
import time
import statistics
from pretty_loguru import create_logger

def benchmark_logger(logger, name, iterations=10000):
    """基準測試"""
    times = []
    
    for i in range(iterations):
        start = time.perf_counter()
        logger.info(f"Benchmark message {i}")
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = statistics.mean(times) * 1000  # 轉換為毫秒
    median_time = statistics.median(times) * 1000
    max_time = max(times) * 1000
    
    logger.block(
        f"📊 {name} 性能測試結果",
        [
            f"迭代次數: {iterations}",
            f"平均時間: {avg_time:.3f}ms",
            f"中位數: {median_time:.3f}ms",
            f"最大時間: {max_time:.3f}ms",
            f"每秒日誌數: {1000 / avg_time:.0f}"
        ],
        border_style="blue"
    )

# 測試不同配置
# 1. 基本配置
basic_logger = create_logger("perf_basic")
benchmark_logger(basic_logger, "基本配置")

# 2. 僅控制台
console_logger = create_logger("perf_console")
benchmark_logger(console_logger, "僅控制台")

# 3. 僅檔案
file_logger = create_logger("perf_file", log_path="logs/perf")
benchmark_logger(file_logger, "僅檔案")

# 4. 無格式化
import loguru
raw_logger = loguru.logger
raw_logger.remove()
raw_logger.add(lambda msg: None)  # 空處理器
benchmark_logger(raw_logger, "無格式化")
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/07_advanced/library_integration.py)

## 下一步

- [企業級應用](./enterprise.md) - 大規模部署方案
- [生產環境](./production.md) - 部署最佳實踐
- [配置管理](./configuration.md) - 深入配置選項