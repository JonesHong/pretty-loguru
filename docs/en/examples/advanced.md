# Advanced Features Examples

Showcasing Pretty-Loguru's advanced features, including direct library access, custom extensions, and performance optimization.

## Direct Loguru Access

Access underlying Loguru functionality:

```python
from pretty_loguru import create_logger
from loguru import logger as loguru_logger

# Create Pretty-Loguru logger
pretty_logger = create_logger("advanced")

# Access underlying Loguru logger
# Pretty-Loguru's logger is an enhanced version of Loguru
pretty_logger.info("This is a Pretty-Loguru log")

# Use Loguru's advanced features
@pretty_logger.catch(message="Error occurred in function")
def risky_function(x):
    return 1 / x

# Use Loguru's bind feature
request_logger = pretty_logger.bind(request_id="12345")
request_logger.info("Processing request")

# Use Loguru's opt feature
pretty_logger.opt(colors=True, capture=False).info("Colored log")
pretty_logger.opt(depth=1).info("Adjust call depth")

# Use Loguru's serialization feature
pretty_logger.add(
    "logs/json_logs.json",
    serialize=True,  # JSON format
    rotation="1 day"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/07_advanced/direct_library_access.py)

## Custom Formatters

Create custom log formatters:

```python
from pretty_loguru import create_logger
import json
from typing import Dict, Any

def custom_formatter(record: Dict[str, Any]) -> str:
    """Custom formatter - structured logging"""
    log_entry = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "logger": record["name"],
        "message": record["message"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
    }
    
    # Add extra fields
    if record.get("extra"):
        log_entry["extra"] = record["extra"]
    
    # Add exception info
    if record.get("exception"):
        log_entry["exception"] = {
            "type": record["exception"].type.__name__,
            "value": str(record["exception"].value),
            "traceback": record["exception"].traceback
        }
    
    return json.dumps(log_entry, ensure_ascii=False) + "\n"

# Use custom formatter
logger = create_logger("custom_format")

# Add handler with custom format
logger.add(
    "logs/structured.log",
    format=custom_formatter,
    rotation="100 MB"
)

# Log structured data
logger.bind(
    user_id=123,
    action="login",
    ip="192.168.1.1"
).info("User logged in")
```

## Performance Optimization

Tips for optimizing log performance:

```python
from pretty_loguru import create_logger
import time

# 1. Use lazy evaluation
logger = create_logger("performance")

# Bad: String formatting happens regardless of log level
def bad_example(data):
    logger.debug(f"Processing data: {json.dumps(data, indent=2)}")

# Good: String formatting only happens if debug is enabled
def good_example(data):
    logger.opt(lazy=True).debug("Processing data: {data}", data=lambda: json.dumps(data, indent=2))

# 2. Use appropriate log levels
logger = create_logger(
    "production",
    level="INFO"  # Don't log DEBUG in production
)

# 3. Use asynchronous logging for high throughput
logger.add(
    "logs/async.log",
    enqueue=True,  # Asynchronous logging
    rotation="1 GB"
)

# 4. Batch operations
from contextvars import ContextVar

batch_logs = ContextVar("batch_logs", default=[])

def batch_log(message):
    logs = batch_logs.get()
    logs.append(message)
    
    if len(logs) >= 100:  # Flush every 100 messages
        for msg in logs:
            logger.info(msg)
        batch_logs.set([])

# 5. Use conditional logging
if logger.level("DEBUG").no:
    # Skip expensive debug operations
    pass
else:
    # Perform debug logging
    debug_info = expensive_debug_calculation()
    logger.debug(debug_info)
```

## Custom Handlers

Create custom log handlers:

```python
from pretty_loguru import create_logger
import requests
from typing import Dict, Any

class WebhookHandler:
    """Send logs to a webhook"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session = requests.Session()
    
    def write(self, message: str):
        """Send log message to webhook"""
        try:
            self.session.post(
                self.webhook_url,
                json={"message": message.strip()},
                timeout=5
            )
        except Exception as e:
            # Fallback to stderr
            print(f"Webhook failed: {e}", file=sys.stderr)

# Use custom handler
logger = create_logger("webhook_logger")

webhook_handler = WebhookHandler("https://example.com/logs")
logger.add(
    webhook_handler,
    format="{time} | {level} | {message}",
    level="ERROR"  # Only send errors to webhook
)
```

## Advanced Configuration

Using environment-specific configurations:

```python
from pretty_loguru import LoggerConfig, ConfigTemplates
import os
from typing import Optional

class AdvancedConfig:
    """Advanced configuration management"""
    
    @staticmethod
    def from_environment() -> LoggerConfig:
        """Create config based on environment"""
        env = os.getenv("APP_ENV", "development")
        
        if env == "production":
            config = ConfigTemplates.production()
            # Add custom production settings
            config.update(
                retention="90 days",
                compression="gz",
                enqueue=True  # Async in production
            )
        elif env == "staging":
            config = ConfigTemplates.production()
            config.update(
                level="DEBUG",
                retention="7 days"
            )
        else:  # development
            config = ConfigTemplates.development()
        
        # Add environment-specific handlers
        if env == "production":
            # Add error monitoring
            config.handlers.append({
                "sink": "logs/errors.log",
                "level": "ERROR",
                "rotation": "1 day",
                "retention": "30 days",
                "compression": "gz"
            })
        
        return config

# Use advanced config
config = AdvancedConfig.from_environment()
logger = config.apply_to("app")
```

## Event System Integration

Using the event system for advanced logging:

```python
from pretty_loguru import create_logger
from typing import Dict, Any
import asyncio

class LogEventProcessor:
    """Process log events asynchronously"""
    
    def __init__(self):
        self.queue = asyncio.Queue()
        self.metrics = {
            "total": 0,
            "by_level": {},
            "by_module": {}
        }
    
    async def process_events(self):
        """Process log events from queue"""
        while True:
            event = await self.queue.get()
            
            # Update metrics
            self.metrics["total"] += 1
            level = event["record"]["level"].name
            module = event["record"]["module"]
            
            self.metrics["by_level"][level] = self.metrics["by_level"].get(level, 0) + 1
            self.metrics["by_module"][module] = self.metrics["by_module"].get(module, 0) + 1
            
            # Process special events
            if level == "ERROR":
                await self.handle_error(event)
            elif level == "CRITICAL":
                await self.alert_admin(event)
    
    async def handle_error(self, event: Dict[str, Any]):
        """Handle error events"""
        # Send to error tracking service
        pass
    
    async def alert_admin(self, event: Dict[str, Any]):
        """Alert admin for critical events"""
        # Send notification
        pass

# Set up event processing
processor = LogEventProcessor()

def log_sink(message):
    """Custom sink that sends events to processor"""
    record = message.record
    asyncio.create_task(
        processor.queue.put({
            "record": record,
            "formatted": str(message)
        })
    )

logger = create_logger("event_logger")
logger.add(log_sink, format="{message}")

# Start event processor
asyncio.create_task(processor.process_events())
```

## Integration with Monitoring

Integrate with monitoring systems:

```python
from pretty_loguru import create_logger
from prometheus_client import Counter, Histogram
import time

# Prometheus metrics
log_counter = Counter(
    'app_logs_total',
    'Total number of log messages',
    ['level', 'module']
)

log_duration = Histogram(
    'app_log_duration_seconds',
    'Time spent logging'
)

class MetricsHandler:
    """Log handler that updates Prometheus metrics"""
    
    def write(self, message: str):
        # Update counters
        record = self.current_record
        log_counter.labels(
            level=record["level"].name,
            module=record["module"]
        ).inc()
    
    def set_record(self, record):
        self.current_record = record

# Create logger with metrics
logger = create_logger("metrics_logger")

# Add metrics handler
metrics_handler = MetricsHandler()
logger.add(
    metrics_handler.write,
    format=lambda record: metrics_handler.set_record(record) or "{message}"
)

# Log with timing
@log_duration.time()
def timed_operation():
    logger.info("Performing timed operation")
    time.sleep(0.1)
    logger.success("Operation completed")
```

## Next Steps

- [Production Deployment](./production.md) - Best practices for production
- [Enterprise Features](./enterprise.md) - Enterprise-grade logging
- [API Reference](../api/) - Complete API documentation