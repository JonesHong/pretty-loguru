# Custom Configuration

Learn how to customize pretty-loguru to fit your specific logging needs with advanced configuration options.

## 🎯 Configuration Methods

### 1. Environment-Based Configuration

Configure pretty-loguru through environment variables for deployment flexibility:

```python
import os
from pretty_loguru import create_logger

# Set environment variables
os.environ['PRETTY_LOG_LEVEL'] = 'DEBUG'
os.environ['PRETTY_LOG_PATH'] = 'app_logs'
os.environ['PRETTY_LOG_ROTATION'] = '50MB'
os.environ['PRETTY_LOG_RETENTION'] = '30 days'

# Initialize with environment settings
logger = create_logger()
```

### 2. Configuration File

Create a JSON configuration file for complex setups:

```json
{
  "log_level": "INFO",
  "log_path": "logs",
  "component_name": "api_server",
  "rotation": "100MB",
  "retention": "14 days",
  "compression": "gz",
  "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
  "handlers": {
    "console": {
      "sink": "sys.stderr",
      "format": "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
      "level": "INFO"
    },
    "file": {
      "sink": "logs/app_{time:YYYY-MM-DD}.log",
      "rotation": "1 day",
      "retention": "7 days",
      "level": "DEBUG"
    }
  }
}
```

Load the configuration:

```python
import json
from pretty_loguru import create_logger

# Load configuration
with open('logger_config.json', 'r') as f:
    config = json.load(f)

# Apply configuration
create_logger(**config)

logger.info("Logger configured from file")
```

### 3. Programmatic Configuration

For dynamic configuration in your application:

```python
from pretty_loguru import create_logger, create_logger

# Custom configuration
config = {
    "level": "DEBUG",
    "log_path": "custom_logs",
    "component_name": "data_processor",
    "rotation": "20MB",
    "retention": "10 days",
    "format": "{time} | {level} | {name}:{function}:{line} - {message}"
}

# Initialize with custom config
create_logger(**config)

# Add custom handlers
logger.add(
    "logs/errors.log",
    filter=lambda record: record["level"].name == "ERROR",
    rotation="10MB",
    retention="30 days"
)

# Add structured logging handler
logger.add(
    "logs/structured.json",
    format="{time} {level} {message}",
    serialize=True,
    rotation="daily"
)
```

## 🎨 Custom Formatters

### Rich Format Customization

```python
from rich.console import Console
from pretty_loguru import create_logger, create_logger

# Custom rich format
custom_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

create_logger(
    level="DEBUG",
    format=custom_format,
    colorize=True
)

logger.info("Custom formatted message")
```

### JSON Structured Logging

```python
import json
from pretty_loguru import create_logger

def json_formatter(record):
    return json.dumps({
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
        "message": record["message"]
    })

# Add JSON handler
logger.add(
    "logs/structured.json",
    format=json_formatter,
    rotation="daily"
)
```

## 🔧 Advanced Handler Configuration

### Multiple Output Targets

```python
from pretty_loguru import create_logger, create_logger

# Initialize base logger
create_logger(level="DEBUG", log_path="logs")

# Console output for INFO and above
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

# File output for all levels
logger.add(
    "logs/debug.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="50MB",
    retention="7 days"
)

# Error-only file
logger.add(
    "logs/errors.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="10MB",
    retention="30 days"
)

# Network logging (example with socket)
import socket
logger.add(
    lambda msg: socket.socket().sendto(msg.encode(), ('localhost', 514)),
    format="{time} {level} {message}",
    level="WARNING"
)
```

### Conditional Logging

```python
from pretty_loguru import create_logger

def dev_filter(record):
    """Only log in development environment"""
    import os
    return os.getenv('ENV') == 'development'

def error_filter(record):
    """Only log errors and above"""
    return record["level"].no >= 40

# Apply filters
logger.add("logs/dev.log", filter=dev_filter)
logger.add("logs/errors.log", filter=error_filter)
```

## 🏭 Production Configuration Examples

### High-Performance Setup

```python
from pretty_loguru import create_logger

# Production configuration
create_logger(
    level="INFO",
    log_path="logs",
    component_name="production_app",
    rotation="100MB",
    retention="30 days",
    compression="gz",
    backtrace=False,  # Disable for performance
    diagnose=False,   # Disable in production
    enqueue=True,     # Asynchronous logging
    catch=True        # Catch exceptions
)

# Separate error tracking
logger.add(
    "logs/critical.log",
    level="CRITICAL",
    rotation="daily",
    retention="365 days",
    format="{time} | {level} | {name}:{function}:{line} - {message} | {extra}",
    backtrace=True,
    diagnose=True
)
```

### Microservices Configuration

```python
import os
from pretty_loguru import create_logger

service_name = os.getenv('SERVICE_NAME', 'unknown_service')
environment = os.getenv('ENVIRONMENT', 'development')

create_logger(
    level="INFO" if environment == "production" else "DEBUG",
    log_path=f"logs/{service_name}",
    component_name=service_name,
    rotation="50MB",
    retention="14 days"
)

# Add correlation ID to all logs
def add_correlation_id(record):
    import contextvars
    correlation_id = getattr(contextvars.copy_context().get('correlation_id', None), 'get', lambda: 'no-correlation')()
    record["extra"]["correlation_id"] = correlation_id

logger = logger.bind(correlation_id="request-123")
logger.info("Processing request")
```

## 🧪 Testing Configuration

```python
import pytest
from pretty_loguru import create_logger

@pytest.fixture
def test_logger():
    """Configure logger for testing"""
    logger.remove()  # Remove all existing handlers
    
    # Add test-specific handler
    logger.add(
        "tests/test.log",
        level="DEBUG",
        format="{time} | {level} | {message}",
        rotation="1MB",
        retention="1 day"
    )
    
    yield logger
    
    # Cleanup
    logger.remove()

def test_logging(test_logger):
    test_logger.info("Test message")
    # Assert log content...
```

## 🔒 Security Considerations

### Sensitive Data Filtering

```python
import re
from pretty_loguru import create_logger

def sanitize_record(record):
    """Remove sensitive data from logs"""
    sensitive_patterns = [
        r'password=\w+',
        r'token=[\w\-]+',
        r'key=[\w\-]+',
        r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b'  # Credit card numbers
    ]
    
    message = record["message"]
    for pattern in sensitive_patterns:
        message = re.sub(pattern, '[REDACTED]', message, flags=re.IGNORECASE)
    
    record["message"] = message
    return record

# Apply sanitization
logger.add(
    "logs/app.log",
    filter=sanitize_record,
    level="INFO"
)

# Test
logger.info("User login with password=secret123")  # Will log: "User login with [REDACTED]"
```

## 📊 Performance Monitoring

```python
import time
from contextlib import contextmanager
from pretty_loguru import create_logger

@contextmanager
def log_performance(operation_name):
    """Context manager to log operation performance"""
    start_time = time.time()
    logger.info(f"Starting {operation_name}")
    
    try:
        yield
    except Exception as e:
        logger.error(f"Failed {operation_name}: {e}")
        raise
    finally:
        duration = time.time() - start_time
        logger.success(f"Completed {operation_name} in {duration:.2f}s")

# Usage
with log_performance("data_processing"):
    # Your operation here
    time.sleep(1)
```

Ready to implement these configurations? Check out our [performance optimization guide](./performance) for production tuning tips!