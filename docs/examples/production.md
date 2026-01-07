# 生產環境範例

展示在生產環境中部署 Pretty-Loguru 的最佳實踐，包括性能監控、錯誤追蹤和日誌管理。

## 環境配置管理

根據不同環境使用不同的日誌配置：

```python
import os
from pretty_loguru import LoggerConfig, create_logger
from pretty_loguru.addons import ConfigTemplates

def get_environment_config() -> LoggerConfig:
    """根據環境變數獲取配置"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    configs = {
        "development": ConfigTemplates.development(),
        "testing": ConfigTemplates.testing(),
        "staging": LoggerConfig(
            level="INFO",
            log_dir="logs/staging",
            rotation="100 MB",
            retention="14 days",
            compression="zip"
        ),
        "production": ConfigTemplates.production()
    }
    
    config = configs.get(env, ConfigTemplates.development())
    
    # 環境特定覆寫
    if env == "production":
        # 生產環境使用 JSON 格式便於日誌聚合
        config.format = '{"time":"{time}", "level":"{level}", "message":"{message}"}'
    
    return config

# 使用環境配置
config = get_environment_config()
logger = create_logger("app", config=config)

# 記錄環境資訊
logger.info(f"Application started in {os.getenv('ENVIRONMENT', 'development')} mode")
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/06_production/deployment_logging.py)

## 性能監控

監控應用程序性能並記錄指標：

```python
from pretty_loguru import create_logger
import time
import psutil
import asyncio
from functools import wraps

logger = create_logger("performance", log_dir="logs/metrics")

def monitor_performance(func):
    """性能監控裝飾器"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = await func(*args, **kwargs)
            status = "success"
        except Exception as e:
            result = None
            status = "error"
            raise
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            duration = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # 記錄性能指標
            logger.info(
                f"Performance metrics",
                function=func.__name__,
                duration=f"{duration:.3f}s",
                memory_start=f"{start_memory:.1f}MB",
                memory_end=f"{end_memory:.1f}MB",
                memory_delta=f"{memory_delta:+.1f}MB",
                status=status
            )
            
            # 警告：慢速操作
            if duration > 1.0:
                logger.warning(f"Slow operation detected: {func.__name__} took {duration:.3f}s")
            
            # 警告：高記憶體使用
            if memory_delta > 100:
                logger.warning(f"High memory usage: {func.__name__} used {memory_delta:.1f}MB")
        
        return result
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        # 同步版本的監控邏輯
        # ... (類似實現)
        pass
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

# 使用範例
@monitor_performance
async def process_large_dataset(size: int):
    """模擬大數據處理"""
    logger.info(f"Processing dataset of size {size}")
    
    # 模擬處理
    data = list(range(size))
    await asyncio.sleep(0.5)  # 模擬 I/O 操作
    
    result = sum(data)
    logger.success(f"Processing complete. Result: {result}")
    return result

# 系統監控
class SystemMonitor:
    def __init__(self, logger):
        self.logger = logger
        self.running = False
    
    async def start(self):
        """開始監控系統資源"""
        self.running = True
        while self.running:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # 定期記錄系統狀態
            self.logger.info(
                "System resources",
                cpu=f"{cpu_percent}%",
                memory_used=f"{memory.percent}%",
                memory_available=f"{memory.available / 1024**3:.1f}GB",
                disk_used=f"{disk.percent}%",
                disk_free=f"{disk.free / 1024**3:.1f}GB"
            )
            
            # 資源警告
            if cpu_percent > 80:
                self.logger.warning(f"High CPU usage: {cpu_percent}%")
            
            if memory.percent > 85:
                self.logger.warning(f"High memory usage: {memory.percent}%")
            
            if disk.percent > 90:
                self.logger.critical(f"Low disk space: {disk.free / 1024**3:.1f}GB free")
            
            await asyncio.sleep(60)  # 每分鐘檢查一次
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/06_production/performance_monitoring.py)

## 錯誤追蹤

完整的錯誤追蹤和報告系統：

```python
from pretty_loguru import create_logger
import traceback
import sys
from datetime import datetime
from typing import Dict, Any

logger = create_logger(
    "error_tracker",
    log_dir="logs/errors",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

class ErrorTracker:
    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        self.last_errors: Dict[str, datetime] = {}
    
    def track_error(self, error: Exception, context: Dict[str, Any] = None):
        """追蹤和記錄錯誤"""
        error_type = type(error).__name__
        error_key = f"{error_type}:{str(error)}"
        
        # 更新錯誤計數
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        self.last_errors[error_key] = datetime.now()
        
        # 記錄錯誤詳情
        logger.error(f"Error occurred: {error_type}")
        
        # 詳細錯誤報告
        error_details = [
            f"Type: {error_type}",
            f"Message: {str(error)}",
            f"Occurrences: {self.error_counts[error_key]}",
            f"First seen: {self.last_errors.get(error_key)}",
        ]
        
        if context:
            error_details.append(f"Context: {context}")
        
        # 添加堆疊追蹤
        tb = traceback.format_exc()
        error_details.extend([
            "Traceback:",
            *tb.split('\n')
        ])
        
        logger.block(
            f"❌ Error Report - {error_type}",
            error_details,
            border_style="red",
            level="ERROR"
        )
        
        # 頻繁錯誤警告
        if self.error_counts[error_key] > 10:
            logger.critical(
                f"Frequent error detected: {error_key} "
                f"occurred {self.error_counts[error_key]} times"
            )
    
    def get_error_summary(self):
        """獲取錯誤摘要"""
        summary = []
        for error_key, count in sorted(
            self.error_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            last_seen = self.last_errors.get(error_key)
            summary.append(
                f"{error_key}: {count} times, "
                f"last: {last_seen.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        
        logger.block(
            "📊 Error Summary",
            summary[:10],  # Top 10 errors
            border_style="yellow",
            level="INFO"
        )
        
        return summary

# 全局錯誤處理器
error_tracker = ErrorTracker()

def setup_global_error_handler():
    """設置全局錯誤處理"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_tracker.track_error(
            exc_value,
            context={"type": "uncaught_exception"}
        )
    
    sys.excepthook = handle_exception

# 使用範例
def risky_operation(data):
    """可能出錯的操作"""
    try:
        # 某些操作
        result = process_data(data)
        logger.success("Operation completed successfully")
        return result
    except ValueError as e:
        error_tracker.track_error(e, context={"data": data})
        raise
    except Exception as e:
        error_tracker.track_error(e, context={"data": data, "unexpected": True})
        raise
```

## 日誌壓縮和清理

自動管理日誌檔案大小：

```python
from pretty_loguru import create_logger
import os
import gzip
import shutil
from pathlib import Path

def custom_compression(file_path: str) -> str:
    """自定義壓縮函數"""
    gz_path = f"{file_path}.gz"
    
    # 使用 gzip 壓縮
    with open(file_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # 刪除原始檔案
    os.remove(file_path)
    
    # 記錄壓縮資訊
    original_size = Path(file_path).stat().st_size
    compressed_size = Path(gz_path).stat().st_size
    ratio = (1 - compressed_size / original_size) * 100
    
    logger.info(
        f"Log compressed: {Path(file_path).name} "
        f"({original_size / 1024:.1f}KB → {compressed_size / 1024:.1f}KB, "
        f"saved {ratio:.1f}%)"
    )
    
    return gz_path

# 使用自定義壓縮
logger = create_logger(
    "production",
    log_dir="logs/prod",
    rotation="50 MB",
    retention="30 days",
    compression=custom_compression,
    start_cleaner=True  # 啟用自動清理
)

# 手動清理舊日誌
def cleanup_old_logs(log_dir: str, days: int = 30):
    """清理超過指定天數的日誌"""
    import time
    
    log_dir = Path(log_dir)
    if not log_dir.exists():
        return
    
    current_time = time.time()
    cutoff_time = current_time - (days * 24 * 60 * 60)
    
    cleaned_count = 0
    cleaned_size = 0
    
    for file_path in log_dir.glob("*.log*"):
        if file_path.stat().st_mtime < cutoff_time:
            file_size = file_path.stat().st_size
            file_path.unlink()
            cleaned_count += 1
            cleaned_size += file_size
    
    if cleaned_count > 0:
        logger.info(
            f"Cleaned {cleaned_count} old log files, "
            f"freed {cleaned_size / 1024**2:.1f}MB"
        )
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/06_production/test_compression.py)

## 部署檢查清單

生產環境部署前的檢查：

```python
def production_checklist():
    """生產環境部署檢查"""
    checks = []
    
    # 檢查日誌目錄權限
    log_dir = Path("logs")
    if log_dir.exists() and os.access(log_dir, os.W_OK):
        checks.append("✅ 日誌目錄可寫入")
    else:
        checks.append("❌ 日誌目錄無法寫入")
    
    # 檢查磁碟空間
    disk_usage = psutil.disk_usage('/')
    if disk_usage.free > 1024**3:  # 1GB
        checks.append(f"✅ 磁碟空間充足 ({disk_usage.free / 1024**3:.1f}GB)")
    else:
        checks.append(f"❌ 磁碟空間不足 ({disk_usage.free / 1024**3:.1f}GB)")
    
    # 檢查環境變數
    required_env = ["ENVIRONMENT", "LOG_LEVEL", "APP_VERSION"]
    for env_var in required_env:
        if os.getenv(env_var):
            checks.append(f"✅ 環境變數 {env_var} 已設置")
        else:
            checks.append(f"❌ 環境變數 {env_var} 未設置")
    
    # 顯示檢查結果
    logger.block(
        "🚀 生產環境部署檢查",
        checks,
        border_style="blue",
        level="INFO"
    )
    
    return all("✅" in check for check in checks)
```

## 監控整合

與監控系統整合（如 Prometheus）：

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Prometheus 指標
log_counter = Counter('app_logs_total', 'Total log entries', ['level'])
error_counter = Counter('app_errors_total', 'Total errors', ['type'])
response_time = Histogram('app_response_time_seconds', 'Response time')

# 包裝 logger 以收集指標
class MonitoredLogger:
    def __init__(self, logger):
        self.logger = logger
    
    def info(self, message, **kwargs):
        log_counter.labels(level='info').inc()
        self.logger.info(message, **kwargs)
    
    def error(self, message, error_type=None, **kwargs):
        log_counter.labels(level='error').inc()
        if error_type:
            error_counter.labels(type=error_type).inc()
        self.logger.error(message, **kwargs)
    
    @response_time.time()
    def log_with_timing(self, message, **kwargs):
        self.logger.info(message, **kwargs)

# 使用監控包裝的 logger
base_logger = create_logger("monitored_app")
logger = MonitoredLogger(base_logger)
```

## 下一步

- [進階功能](./advanced.md) - 自定義和擴展功能
- [企業級應用](./enterprise.md) - 大規模部署
- [配置管理](./configuration.md) - 深入配置選項
