# 效能最佳化

在生產環境中，日誌系統的效能直接影響應用程式的整體表現。本指南將幫助您優化 pretty-loguru 的效能。

## ⚡ 效能基準

### 基準測試

pretty-loguru 在不同場景下的效能表現：

```python
import time
from pretty_loguru import create_logger

def benchmark_logging(logger, iterations=10000):
    """日誌效能基準測試"""
    start_time = time.time()
    
    for i in range(iterations):
        logger.info(f"測試訊息 {i}", extra={"iteration": i})
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"執行 {iterations} 次日誌操作")
    print(f"總時間: {duration:.2f} 秒")
    print(f"平均每次: {(duration/iterations)*1000:.3f} 毫秒")
    print(f"每秒操作數: {iterations/duration:.0f} ops/sec")

# 測試不同配置
console_logger = create_logger("console_only", sink="stdout")
file_logger = create_logger("file_only", log_path="logs/perf.log")
async_logger = create_logger("async", log_path="logs/async.log", enqueue=True)

print("控制台日誌效能:")
benchmark_logging(console_logger)

print("\n檔案日誌效能:")
benchmark_logging(file_logger)

print("\n非同步日誌效能:")
benchmark_logging(async_logger)
```

## 🚀 優化策略

### 1. 非同步日誌記錄

```python
# 啟用非同步處理，提升高併發效能
async_logger = create_logger(
    name="async_app",
    log_path="logs/app.log",
    enqueue=True,        # 啟用非同步佇列
    rotation="100 MB",
    compression="gz"
)

# 批次處理日誌
import asyncio

async def batch_logging():
    """批次日誌記錄範例"""
    tasks = []
    
    for i in range(1000):
        # 建立日誌任務但不立即執行
        task = asyncio.create_task(
            async_log_message(f"批次訊息 {i}")
        )
        tasks.append(task)
    
    # 批次執行所有日誌任務
    await asyncio.gather(*tasks)

async def async_log_message(message):
    """非同步日誌記錄"""
    async_logger.info(message)

# 執行批次日誌
asyncio.run(batch_logging())
```

### 2. 條件式日誌記錄

```python
# 避免不必要的字串格式化
def optimized_logging():
    logger = create_logger("optimized", level="INFO")
    
    # ❌ 低效：總是執行字串格式化
    expensive_data = get_expensive_data()
    logger.debug(f"詳細資料: {expensive_data}")
    
    # ✅ 高效：只在需要時格式化
    if logger.level <= 10:  # DEBUG 級別
        expensive_data = get_expensive_data()
        logger.debug(f"詳細資料: {expensive_data}")
    
    # ✅ 更好：使用延遲格式化
    logger.debug("詳細資料: {data}", data=lambda: get_expensive_data())

def get_expensive_data():
    """模擬耗時的資料處理"""
    time.sleep(0.1)
    return {"complex": "data structure"}
```

### 3. 過濾器優化

```python
# 高效的過濾器設計
def create_efficient_filter():
    """建立高效的日誌過濾器"""
    
    # 預編譯正則表達式
    import re
    sensitive_pattern = re.compile(r'password|token|secret', re.IGNORECASE)
    
    def efficient_filter(record):
        # 快速檢查：避免昂貴的操作
        if record["level"].no < 20:  # 低於 INFO 級別
            return False
        
        # 只在必要時進行模式匹配
        message = record.get("message", "")
        return not sensitive_pattern.search(message)
    
    return efficient_filter

# 使用高效過濾器
logger = create_logger(
    name="filtered",
    filter=create_efficient_filter()
)
```

### 4. 記憶體管理

```python
# 控制記憶體使用
memory_optimized_logger = create_logger(
    name="memory_optimized",
    log_path="logs/app.log",
    rotation="50 MB",        # 較小的檔案大小
    retention="7 days",      # 較短的保留期
    compression="gz",        # 啟用壓縮
    enqueue=True,           # 非同步處理
    # 控制佇列大小
    catch=True              # 捕獲例外，避免記憶體洩漏
)

# 定期清理資源
import gc

def periodic_cleanup():
    """定期清理記憶體"""
    gc.collect()  # 強制垃圾回收
    print(f"記憶體清理完成，當前物件數: {len(gc.get_objects())}")

# 每小時執行一次清理
import threading
timer = threading.Timer(3600, periodic_cleanup)
timer.daemon = True
timer.start()
```

## 📊 監控與分析

### 效能監控

```python
import psutil
import time
from collections import deque

class PerformanceMonitor:
    """日誌效能監控器"""
    
    def __init__(self, window_size=100):
        self.response_times = deque(maxlen=window_size)
        self.error_count = 0
        self.total_logs = 0
        self.start_time = time.time()
    
    def record_log_operation(self, duration, success=True):
        """記錄日誌操作"""
        self.response_times.append(duration)
        self.total_logs += 1
        
        if not success:
            self.error_count += 1
    
    def get_metrics(self):
        """獲取效能指標"""
        if not self.response_times:
            return {}
        
        current_time = time.time()
        uptime = current_time - self.start_time
        
        return {
            "avg_response_time": sum(self.response_times) / len(self.response_times),
            "max_response_time": max(self.response_times),
            "min_response_time": min(self.response_times),
            "total_logs": self.total_logs,
            "error_rate": self.error_count / self.total_logs if self.total_logs > 0 else 0,
            "logs_per_second": self.total_logs / uptime if uptime > 0 else 0,
            "memory_usage_mb": psutil.Process().memory_info().rss / 1024 / 1024,
            "cpu_percent": psutil.Process().cpu_percent()
        }

# 使用監控器
monitor = PerformanceMonitor()

def monitored_log_operation(logger, message):
    """監控的日誌操作"""
    start_time = time.time()
    
    try:
        logger.info(message)
        success = True
    except Exception as e:
        success = False
        print(f"日誌錯誤: {e}")
    
    duration = time.time() - start_time
    monitor.record_log_operation(duration, success)

# 定期輸出效能報告
def print_performance_report():
    metrics = monitor.get_metrics()
    print("\n📊 日誌效能報告:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

# 每分鐘輸出報告
import threading
def scheduled_report():
    print_performance_report()
    threading.Timer(60, scheduled_report).start()

scheduled_report()
```

### 瓶頸分析

```python
import cProfile
import pstats
from io import StringIO

def profile_logging_performance():
    """分析日誌效能瓶頸"""
    
    pr = cProfile.Profile()
    pr.enable()
    
    # 執行日誌操作
    logger = create_logger("profiling", log_path="logs/profile.log")
    
    for i in range(1000):
        logger.info(f"效能分析訊息 {i}", extra={"data": {"key": f"value_{i}"}})
    
    pr.disable()
    
    # 分析結果
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)  # 顯示前 20 個最慢的函數
    
    print("🔍 效能分析結果:")
    print(s.getvalue())

# 執行效能分析
profile_logging_performance()
```

## 🎯 特定場景優化

### 高併發 Web 應用

```python
# Web 應用優化配置
web_logger = create_logger(
    name="web_app",
    log_path="logs/web.log",
    level="INFO",           # 避免過多 DEBUG 訊息
    rotation="1 hour",      # 頻繁輪換避免單檔案過大
    retention="24 hours",   # 短期保留減少磁碟 I/O
    compression="gz",       # 壓縮節省空間
    enqueue=True,          # 非同步處理
    format="{time:HH:mm:ss} | {level} | {message}"  # 簡化格式
)

# 請求日誌優化
def log_request(request_id, method, path, response_time):
    """優化的請求日誌"""
    if response_time > 1.0:  # 只記錄慢請求的詳細資訊
        web_logger.warning(
            f"慢請求: {method} {path}",
            extra={
                "request_id": request_id,
                "response_time": response_time,
                "type": "slow_request"
            }
        )
    else:
        web_logger.info(f"{method} {path}")
```

### 微服務架構

```python
# 微服務日誌優化
microservice_logger = create_logger(
    name="microservice",
    log_path="logs/service.log",
    level="INFO",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
    enqueue=True,
    # 結構化格式便於日誌聚合
    serialize=True
)

def optimized_service_log(operation, service, duration, **kwargs):
    """優化的微服務日誌"""
    log_data = {
        "operation": operation,
        "service": service,
        "duration_ms": round(duration * 1000, 2),
        **kwargs
    }
    
    # 根據耗時決定日誌級別
    if duration > 5.0:
        microservice_logger.error("操作超時", extra=log_data)
    elif duration > 1.0:
        microservice_logger.warning("操作較慢", extra=log_data)
    else:
        microservice_logger.info("操作完成", extra=log_data)
```

### 批次處理系統

```python
# 批次處理優化
batch_logger = create_logger(
    name="batch_processing",
    log_path="logs/batch.log",
    level="INFO",
    rotation="daily",
    retention="90 days",
    compression="gz",
    # 批次系統可以使用同步模式
    enqueue=False
)

class BatchProgressLogger:
    """批次進度日誌器"""
    
    def __init__(self, total_items, log_interval=1000):
        self.total_items = total_items
        self.log_interval = log_interval
        self.processed = 0
        self.start_time = time.time()
    
    def log_progress(self, items_processed=1):
        """記錄處理進度"""
        self.processed += items_processed
        
        if self.processed % self.log_interval == 0:
            elapsed = time.time() - self.start_time
            rate = self.processed / elapsed if elapsed > 0 else 0
            remaining = (self.total_items - self.processed) / rate if rate > 0 else 0
            
            batch_logger.info(
                f"批次進度: {self.processed}/{self.total_items}",
                extra={
                    "progress_percent": (self.processed / self.total_items) * 100,
                    "processing_rate": rate,
                    "estimated_remaining_seconds": remaining
                }
            )

# 使用批次進度記錄器
progress = BatchProgressLogger(total_items=10000)
for i in range(10000):
    # 處理資料
    time.sleep(0.001)  # 模擬處理時間
    progress.log_progress()
```

## ⚙️ 系統級優化

### 作業系統設定

```bash
# Linux 系統優化設定

# 增加檔案描述符限制
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# 優化磁碟 I/O
echo "deadline" > /sys/block/sda/queue/scheduler

# 調整 vm.dirty_ratio 以優化寫入效能
echo "vm.dirty_ratio = 15" >> /etc/sysctl.conf
echo "vm.dirty_background_ratio = 5" >> /etc/sysctl.conf
```

### Docker 環境優化

```dockerfile
# Dockerfile 優化
FROM python:3.11-slim

# 安裝 pretty-loguru
RUN pip install pretty-loguru

# 建立日誌目錄並設定權限
RUN mkdir -p /var/log/app && \
    chmod 755 /var/log/app

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV LOG_PATH=/var/log/app

# 使用非 root 用戶
RUN useradd -m appuser
USER appuser

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml 優化
version: '3.8'
services:
  app:
    build: .
    volumes:
      # 使用 tmpfs 提升日誌寫入效能
      - type: tmpfs
        target: /var/log/app
        tmpfs:
          size: 1G
    environment:
      - LOG_LEVEL=INFO
      - PYTHONUNBUFFERED=1
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

## 📈 效能基準與目標

### 效能目標

| 場景 | 目標效能 | 記憶體使用 |
|------|----------|------------|
| 低流量應用 | >1,000 logs/sec | <50MB |
| 中流量應用 | >5,000 logs/sec | <100MB |
| 高流量應用 | >20,000 logs/sec | <200MB |

### 監控指標

```python
# 關鍵效能指標 (KPI)
performance_kpis = {
    "avg_log_latency_ms": 1.0,      # 平均日誌延遲 < 1ms
    "p95_log_latency_ms": 5.0,      # 95% 日誌延遲 < 5ms
    "memory_usage_mb": 100,         # 記憶體使用 < 100MB
    "cpu_usage_percent": 5,         # CPU 使用率 < 5%
    "disk_io_wait_percent": 10,     # 磁碟 I/O 等待 < 10%
    "error_rate_percent": 0.1       # 錯誤率 < 0.1%
}

def validate_performance(current_metrics):
    """驗證效能是否符合目標"""
    for metric, target in performance_kpis.items():
        current = current_metrics.get(metric, 0)
        if current > target:
            print(f"⚠️ 效能警告: {metric} = {current}, 目標 < {target}")
        else:
            print(f"✅ 效能正常: {metric} = {current}")
```

## 🔗 相關資源

- [自定義配置](./custom-config) - 完整配置選項
- [日誌輪換](./log-rotation) - 檔案管理策略
- [生產環境部署](./production) - 生產環境最佳實踐
- [範例集合](../examples/production/) - 效能優化範例