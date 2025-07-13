# Performance Optimization

In production environments, the performance of the logging system directly impacts the overall application performance. This guide will help you optimize pretty-loguru's performance.

## ⚡ Performance Benchmarks

### Benchmarking

pretty-loguru's performance in different scenarios:

```python
import time
from pretty_loguru import create_logger

def benchmark_logging(logger, iterations=10000):
    """Logging performance benchmark"""
    start_time = time.time()
    
    for i in range(iterations):
        logger.info(f"Test message {i}", extra={"iteration": i})
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Executed {iterations} log operations")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Average per operation: {(duration/iterations)*1000:.3f} ms")
    print(f"Operations per second: {iterations/duration:.0f} ops/sec")

# Test different configurations
console_logger = create_logger("console_only", sink="stdout")
file_logger = create_logger("file_only", log_path="logs/perf.log")
async_logger = create_logger("async", log_path="logs/async.log", enqueue=True)

print("Console logging performance:")
benchmark_logging(console_logger)

print("\nFile logging performance:")
benchmark_logging(file_logger)

print("\nAsync logging performance:")
benchmark_logging(async_logger)
```

## 🚀 Optimization Strategies

### 1. Asynchronous Logging

```python
# Enable async processing for high-concurrency performance
async_logger = create_logger(
    name="async_app",
    log_path="logs/app.log",
    enqueue=True,        # Enable async queue
    rotation="100 MB",
    compression="gz"
)

# Batch logging
import asyncio

async def batch_logging():
    """Batch logging example"""
    tasks = []
    
    for i in range(1000):
        # Create logging tasks without immediate execution
        task = asyncio.create_task(
            async_log_message(f"Batch message {i}")
        )
        tasks.append(task)
    
    # Execute all logging tasks in batch
    await asyncio.gather(*tasks)

async def async_log_message(message):
    """Async logging"""
    async_logger.info(message)

# Execute batch logging
asyncio.run(batch_logging())
```

### 2. Conditional Logging

```python
# Avoid unnecessary string formatting
def optimized_logging():
    logger = create_logger("optimized", level="INFO")
    
    # ❌ Inefficient: Always performs string formatting
    expensive_data = get_expensive_data()
    logger.debug(f"Detailed data: {expensive_data}")
    
    # ✅ Efficient: Format only when needed
    if logger.level <= 10:  # DEBUG level
        expensive_data = get_expensive_data()
        logger.debug(f"Detailed data: {expensive_data}")
    
    # ✅ Better: Use lazy formatting
    logger.opt(lazy=True).debug(
        "Detailed data: {data}",
        data=lambda: get_expensive_data()
    )
```

### 3. Proxy Mode

For ultra-high performance scenarios:

```python
from pretty_loguru import create_logger

# Enable proxy mode - reduces overhead
proxy_logger = create_logger(
    name="proxy_app",
    log_path="logs/proxy.log",
    proxy_mode=True,     # Enable proxy mode
    level="WARNING"      # Higher level for less output
)

# Proxy mode characteristics:
# - Minimal overhead when log level not met
# - Reduced feature set for performance
# - Ideal for hot paths in code
```

### 4. Buffer Management

```python
# Custom buffer size for batch writes
import sys
from loguru import logger

class BufferedHandler:
    """Custom handler with buffer management"""
    
    def __init__(self, filepath, buffer_size=1000):
        self.filepath = filepath
        self.buffer = []
        self.buffer_size = buffer_size
        self.file = open(filepath, 'a')
    
    def write(self, message):
        self.buffer.append(message)
        
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def flush(self):
        if self.buffer:
            self.file.writelines(self.buffer)
            self.file.flush()
            self.buffer.clear()
    
    def close(self):
        self.flush()
        self.file.close()

# Use buffered handler
handler = BufferedHandler("logs/buffered.log")
logger.add(handler, format="{message}")
```

## 📊 Performance Tips

### 1. Log Level Optimization

```python
# Production configuration
prod_logger = create_logger(
    "production",
    level="INFO",        # Skip DEBUG messages
    log_path="logs/prod.log"
)

# Development configuration
dev_logger = create_logger(
    "development",
    level="DEBUG",       # All messages
    log_path="logs/dev.log"
)

# Dynamic level adjustment
import os
log_level = os.getenv("LOG_LEVEL", "INFO")
dynamic_logger = create_logger("app", level=log_level)
```

### 2. Minimize Serialization

```python
# Avoid complex objects in logs
import json

# ❌ Inefficient: Complex object serialization
class ComplexObject:
    def __str__(self):
        # Expensive operation
        return json.dumps(self.__dict__, indent=2)

logger.info(f"Object: {ComplexObject()}")

# ✅ Efficient: Simple representations
def log_object_summary(obj):
    logger.info(
        "Object summary",
        type=type(obj).__name__,
        id=id(obj),
        size=sys.getsizeof(obj)
    )
```

### 3. File I/O Optimization

```python
# Optimize file operations
optimized_logger = create_logger(
    "optimized",
    log_path="logs/opt.log",
    rotation="500 MB",       # Larger files = fewer rotations
    compression="gz",        # Compress rotated files
    enqueue=True,           # Async writes
    encoding="utf-8",       # Explicit encoding
    buffering=8192          # Larger buffer
)
```

## 🔥 High-Performance Patterns

### 1. Sampling

Log only a sample of events in high-volume scenarios:

```python
import random

class SamplingLogger:
    """Logger that samples messages"""
    
    def __init__(self, logger, sample_rate=0.1):
        self.logger = logger
        self.sample_rate = sample_rate
    
    def log(self, level, message, **kwargs):
        if random.random() < self.sample_rate:
            getattr(self.logger, level)(
                f"[SAMPLED] {message}", 
                **kwargs
            )

# Sample 10% of debug messages
sampler = SamplingLogger(
    create_logger("sampled"),
    sample_rate=0.1
)

for i in range(10000):
    sampler.log("debug", f"High volume event {i}")
```

### 2. Aggregation

Aggregate similar messages:

```python
from collections import defaultdict
import threading
import time

class AggregatingLogger:
    """Logger that aggregates similar messages"""
    
    def __init__(self, logger, flush_interval=5.0):
        self.logger = logger
        self.flush_interval = flush_interval
        self.message_counts = defaultdict(int)
        self.lock = threading.Lock()
        self._start_flusher()
    
    def log(self, level, message):
        with self.lock:
            self.message_counts[(level, message)] += 1
    
    def _start_flusher(self):
        def flush():
            while True:
                time.sleep(self.flush_interval)
                self._flush()
        
        thread = threading.Thread(target=flush, daemon=True)
        thread.start()
    
    def _flush(self):
        with self.lock:
            for (level, message), count in self.message_counts.items():
                if count > 1:
                    getattr(self.logger, level)(
                        f"{message} (occurred {count} times)"
                    )
                else:
                    getattr(self.logger, level)(message)
            
            self.message_counts.clear()

# Use aggregating logger
agg_logger = AggregatingLogger(create_logger("aggregated"))

# Many similar messages
for i in range(1000):
    agg_logger.log("info", "Database query executed")
    agg_logger.log("warning", "Cache miss")
```

### 3. Zero-Copy Logging

Minimize memory allocations:

```python
# Pre-allocated message templates
MESSAGE_TEMPLATES = {
    "request": "Request: method={method} path={path} status={status}",
    "error": "Error: type={error_type} message={message}",
    "metric": "Metric: name={name} value={value} unit={unit}"
}

def log_request(logger, method, path, status):
    """Log with pre-allocated template"""
    logger.info(
        MESSAGE_TEMPLATES["request"],
        method=method,
        path=path,
        status=status
    )

# No string concatenation, minimal allocations
log_request(logger, "GET", "/api/users", 200)
```

## 📈 Monitoring Performance

### Performance Metrics

```python
import psutil
import os

class PerformanceMonitor:
    """Monitor logging performance impact"""
    
    def __init__(self, logger):
        self.logger = logger
        self.process = psutil.Process(os.getpid())
    
    def log_with_metrics(self, message):
        # Before logging
        cpu_before = self.process.cpu_percent()
        mem_before = self.process.memory_info().rss
        
        # Log message
        start_time = time.time()
        self.logger.info(message)
        duration = time.time() - start_time
        
        # After logging
        cpu_after = self.process.cpu_percent()
        mem_after = self.process.memory_info().rss
        
        # Log metrics (only in debug mode)
        self.logger.debug(
            "Logging metrics",
            duration_ms=duration * 1000,
            cpu_delta=cpu_after - cpu_before,
            memory_delta=mem_after - mem_before
        )

# Monitor performance impact
monitor = PerformanceMonitor(create_logger("monitored"))
monitor.log_with_metrics("Performance test message")
```

## 🎯 Best Practices

1. **Use Async Logging**: Enable `enqueue=True` for production
2. **Set Appropriate Levels**: Use INFO or higher in production
3. **Batch Operations**: Group related log operations
4. **Lazy Evaluation**: Use `opt(lazy=True)` for expensive operations
5. **Monitor Impact**: Regularly check logging performance impact
6. **Use Sampling**: Sample high-volume events
7. **Optimize Formats**: Use simple, efficient log formats

## 🔗 Related Resources

- [Production Guide](./production.md) - Production best practices
- [Configuration Guide](./enhanced-config.md) - Performance-related configs
- [API Reference](../api/) - Performance parameters