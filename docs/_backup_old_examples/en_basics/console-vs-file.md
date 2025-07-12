# Console vs File Logging

Learn the differences between console and file logging, and when to use each approach.

## 🖥️ Console Logging

Console logging outputs directly to the terminal, perfect for development and debugging.

### Basic Console Setup

```python
from pretty_loguru import create_logger

# Start with console logging only
logger = create_logger(
    name="demo",
    console_only=True
)

logger.info("This appears in the console")
logger.debug("Debug information for development")
logger.success("Operation completed successfully!")
logger.warning("This is a warning message")
logger.error("Something went wrong")
```

### Console Output Formatting

```python
from pretty_loguru import create_logger

# Configure console with custom format
logger = create_logger(
    name="console_demo",
    level="DEBUG",
    console_only=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
)

logger.info("Clean console output")
logger.debug("Debug with timestamp")
```

### Rich Console Features

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Use visual features in console
logger.block("Status Report", [
    "✅ Database: Connected",
    "✅ API: Running on port 8000",
    "⚠️  Cache: 85% full"
], border_style="green")

logger.ascii_header("SYSTEM STARTUP", font="slant")
```

## 📁 File Logging

File logging saves logs to disk for persistence, auditing, and analysis.

### Basic File Setup

```python
from pretty_loguru import create_logger

# Start with file logging only
logger = create_logger(
    name="demo",
    log_path=
    folder="logs",
    console_only=False  # Enable file logging
)

logger.info("This message is saved to file")
logger.error("Errors are persisted for investigation")
```

### Custom File Configuration

```python
from pretty_loguru import create_logger

# Configure file logging with rotation
create_logger(
    level="INFO",
    log_path="application_logs",
    component_name="my_app",
    rotation="10MB",  # Rotate when file reaches 10MB
    retention="7 days",  # Keep logs for 7 days
    compression="gz"  # Compress old files
)

logger.info("File logging with rotation enabled")
```

### Multiple Log Files

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
), create_logger

# Initialize base logger
create_logger(level="DEBUG", log_path="logs")

# Add specific error file
logger.add(
    "logs/errors.log",
    level="ERROR",
    rotation="5MB",
    retention="30 days",
    format="{time} | {level} | {name}:{function}:{line} - {message}"
)

# Add audit trail file
logger.add(
    "logs/audit.log",
    level="INFO",
    filter=lambda record: "audit" in record["extra"],
    rotation="daily"
)

# Usage
logger.info("Regular log message")
logger.error("This goes to both general and error logs")
logger.bind(audit=True).info("Audit trail entry")  # Only to audit.log
```

## 🔄 Combined Console + File Logging

The most common setup uses both console and file outputs.

### Hybrid Configuration

```python
from pretty_loguru import create_logger

# Initialize with both console and file
create_logger(
    level="DEBUG",
    log_path="logs",
    component_name="web_app"
    # console_only=False is default
)

# Console shows INFO and above, file captures everything
logger.debug("Debug info (file only)")
logger.info("Info message (console + file)")
logger.error("Error message (console + file)")
```

### Different Levels for Console vs File

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
), create_logger

# Base initialization
create_logger(level="DEBUG", log_path="logs")

# Remove default console handler and add custom ones
logger.remove()

# Console: INFO and above with colors
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

# File: Everything including debug
logger.add(
    "logs/app.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="20MB",
    retention="14 days"
)

# Test different levels
logger.debug("Debug: Only in file")
logger.info("Info: Console and file")
logger.warning("Warning: Console and file")
logger.error("Error: Console and file")
```

## 📊 Comparison Table

| Feature | Console Logging | File Logging | Combined |
|---------|----------------|--------------|----------|
| **Persistence** | ❌ Lost on restart | ✅ Permanent storage | ✅ Best of both |
| **Real-time Monitoring** | ✅ Immediate feedback | ❌ Manual file checking | ✅ Real-time + archive |
| **Performance** | ⚠️ Can slow down apps | ✅ Asynchronous writes | ⚠️ Moderate impact |
| **Storage** | ❌ No storage | ⚠️ Requires disk space | ⚠️ Requires disk space |
| **Analysis** | ❌ Hard to analyze | ✅ Log aggregation tools | ✅ Flexible analysis |
| **Development** | ✅ Perfect for dev | ❌ Less convenient | ✅ Ideal setup |
| **Production** | ❌ Not suitable | ✅ Required for audit | ✅ Recommended |

## 🎯 When to Use Each

### Console Only
- **Development environment**
- **Quick debugging sessions**
- **Interactive scripts**
- **One-time utilities**

```python
# Development setup
from pretty_loguru import create_logger

logger = create_logger(
    name="console_demo",
    log_path=None,  # Console only
    level="INFO"
)
logger.info("Perfect for development")
```

### File Only
- **Background services**
- **Batch processing**
- **Production systems without monitoring**
- **When console output is not accessible**

```python
# Background service
from pretty_loguru import create_logger
import sys

# Disable console output
create_logger(
    level="INFO",
    log_path="service_logs",
    component_name="background_service"
)

# Remove any console handlers
for handler_id in logger._core.handlers.copy():
    if logger._core.handlers[handler_id]._sink._stream in (sys.stdout, sys.stderr):
        logger.remove(handler_id)

logger.info("Service started - logged to file only")
```

### Combined (Recommended)
- **Web applications**
- **APIs and microservices**
- **Production systems with monitoring**
- **Any system requiring both real-time feedback and persistence**

```python
# Production-ready setup
from pretty_loguru import create_logger

create_logger(
    level="INFO",
    log_path="logs",
    component_name="api_server",
    rotation="50MB",
    retention="30 days"
)

logger.info("API server starting...")
logger.success("Server ready - logged to both console and file")
```

## 🔧 Advanced Scenarios

### Environment-based Configuration

```python
import os
from pretty_loguru import create_logger

env = os.getenv('ENVIRONMENT', 'development')

if env == 'development':
    # Development: Console only with debug level
    create_logger(level="DEBUG", console_only=True)
elif env == 'testing':
    # Testing: File only to avoid cluttering test output
    create_logger(level="INFO", log_path="test_logs", console_only=False)
    logger.remove()  # Remove console handler
    logger.add("test_logs/test.log", level="INFO")
else:
    # Production: Both console and file
    create_logger(
        level="INFO",
        log_path="logs",
        component_name="prod_app",
        rotation="100MB",
        retention="90 days"
    )

logger.info(f"Logger configured for {env} environment")
```

### Dynamic Switching

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
), create_logger

class LoggerManager:
    def __init__(self):
        self.file_handler_id = None
        self.console_handler_id = None
        
    def enable_console(self):
        if self.console_handler_id is None:
            self.console_handler_id = logger.add(
                sink=lambda msg: print(msg, end=""),
                format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
                level="INFO",
                colorize=True
            )
    
    def disable_console(self):
        if self.console_handler_id is not None:
            logger.remove(self.console_handler_id)
            self.console_handler_id = None
    
    def enable_file(self, path="logs/app.log"):
        if self.file_handler_id is None:
            self.file_handler_id = logger.add(
                path,
                level="DEBUG",
                rotation="10MB"
            )
    
    def disable_file(self):
        if self.file_handler_id is not None:
            logger.remove(self.file_handler_id)
            self.file_handler_id = None

# Usage
log_manager = LoggerManager()
log_manager.enable_console()
logger.info("Console enabled")

log_manager.enable_file()
logger.info("File logging enabled")

log_manager.disable_console()
logger.info("Console disabled - file only")
```

Choose the right logging strategy based on your application's needs and environment!