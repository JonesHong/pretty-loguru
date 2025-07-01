# Basic Usage

This page provides a detailed introduction to the basic concepts and core features of pretty-loguru.

## 🎯 Core Concepts

### Logger Initialization

pretty-loguru offers multiple initialization methods to meet the needs of different scenarios.

#### Quick Initialization (Recommended)

```python
from pretty_loguru import create_logger

# Complete all settings with one line of code
component_name = logger = create_logger(
    name="basic-usage_demo",
    log_path="my_logs",
    level="INFO"
)
print(f"Logger has been initialized, component name: {component_name}")
```

#### Custom Initialization

```python
from pretty_loguru import init_logger

init_logger(
    level="INFO",
    log_path="custom_logs",
    component_name="my_app",
    rotation="50MB",
    retention="30 days"
)
```

#### Creating a Dedicated Logger

```python
from pretty_loguru import create_logger

# Create a dedicated logger for the API
api_logger = create_logger(
    name="api_service",
    level="DEBUG",
    log_path="logs/api"
)

api_logger.info("API service has been started")
```

## 📊 Log Levels

pretty-loguru supports standard log levels and adds a `SUCCESS` level:

### Basic Log Levels

```python
# Debug message (lowest level)
logger.debug("Detailed debug information")

# General information
logger.info("Application is running normally")

# Success message (specific to pretty-loguru)
logger.success("Operation completed successfully")

# Warning message
logger.warning("Memory usage is high")

# Error message
logger.error("Failed to connect to the database")

# Critical error
logger.critical("System is about to crash")
```

### Level Description Table

| Level    | Value | Purpose                  | Color      |
|----------|-------|--------------------------|------------|
| DEBUG    | 10    | Detailed debug info      | Blue       |
| INFO     | 20    | General operational info | White      |
| SUCCESS  | 25    | Successful operations    | Green      |
| WARNING  | 30    | Warning messages         | Yellow     |
| ERROR    | 40    | Error messages           | Red        |
| CRITICAL | 50    | Critical errors          | Red (Bold) |

## 🎯 Output Control

### Simultaneous Output (Default Behavior)

```python
# By default, output is sent to both the console and the file
logger.info("This message will appear in two places")
```

### Console-Only Output

```python
# Display only in the console, not written to the file
logger.console_info("Display only in the console")
logger.console_warning("Console warning")
logger.console_error("Console error")
```

### File-Only Output

```python
# Write only to the file, not displayed in the console
logger.file_info("Write only to the log file")
logger.file_debug("File debug message")
logger.file_error("File error record")
```

## 📁 File Management

### Automatic File Naming

pretty-loguru automatically generates meaningful filenames:

```
Format: [component_name]_YYYYMMDD-HHMMSS.log
Example: [my_app_20240630_143022]_20240630-143022.log
```

### Log Rotation

```python
# Rotate by file size
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", rotation="10MB",
    level="INFO"
)

# Rotate by time
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", rotation="1 day",
    level="INFO"
)

# Rotate by count (at midnight)
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", rotation="midnight", retention=10,
    level="INFO"
)
```

### Log Cleanup

```python
# Automatically clean up old files
logger_start(
    folder="logs",
    retention="7 days"  # Keep for 7 days
)

logger_start(
    folder="logs", 
    retention=5  # Keep 5 files
)
```

## 🔧 Advanced Configuration

### Custom Formatting

```python
from pretty_loguru import create_logger

# Log extra information
logger.info("User login", extra={"user_id": 12345, "ip": "192.168.1.1"})
```

### Multi-Environment Configuration

```python
import os

def setup_logging():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return logger_start(
            folder="prod_logs",
            level="INFO",
            rotation="100MB",
            retention="30 days"
        )
    else:
        return logger_start(
            folder="dev_logs",
            level="DEBUG",
            rotation="10MB",
            retention="7 days"
        )
```

### Conditional Logging

```python
import logging

# Set log level
if logger.level("DEBUG").no >= logging.DEBUG:
    logger.debug("This is a debug message")
```

## 🎮 Practical Example

### Complete Application Example

```python
import time
from pretty_loguru import create_logger

def main():
    # Initialize the logging system
    component_name = logger_start(
        folder="app_logs",
        level="INFO",
        rotation="50MB",
        retention="14 days"
    )
    
    logger.info(f"Application started, component: {component_name}")
    
    try:
        # Simulate application logic
        logger.info("Loading configuration file...")
        time.sleep(0.5)
        logger.success("Configuration file loaded successfully")
        
        logger.info("Connecting to the database...")
        time.sleep(1)
        logger.success("Database connection successful")
        
        logger.info("Starting web service...")
        time.sleep(0.8)
        logger.success("Web service started, listening on port 8080")
        
        # Simulate a warning
        logger.warning("Memory usage reached 75%")
        
        logger.info("Application running normally")
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        logger.critical("System is about to exit")
        return 1
    
    logger.info("Application shut down normally")
    return 0

if __name__ == "__main__":
    exit(main())
```

### Error Handling Example

```python
def process_data(data):
    try:
        logger.info(f"Starting to process data, size: {len(data)}")
        
        # Processing logic
        result = some_complex_operation(data)
        
        logger.success(f"Data processing complete, result: {len(result)} records")
        return result
        
    except ValueError as e:
        logger.error(f"Data format error: {e}")
        raise
    except Exception as e:
        logger.critical(f"A critical error occurred during processing: {e}")
        raise
    finally:
        logger.debug("Data processing flow finished")
```

## ❓ Frequently Asked Questions

### Q: Why can't I see DEBUG level logs?
A: Check the log level setting:
```python
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", level="DEBUG",
    level="INFO"
)
```

### Q: How to log sensitive information only in the file?
A: Use the file-specific method:
```python
logger.file_info(f"User password reset: {user_id}")  # Writes only to file
logger.console_info("User password reset successful")      # Displays only in console
```

### Q: What to do if there are too many log files?
A: Set up automatic cleanup:
```python
logger = create_logger(
    name="basic-usage_demo",
    log_path="logs", retention="7 days",
    level="INFO"
)
```

### Q: How to use the same logger in different modules?
A: The logger is global, just import it directly:
```python
# module_a.py
from pretty_loguru import create_logger
logger.info("Message from Module A")

# module_b.py  
from pretty_loguru import create_logger
logger.info("Message from Module B")
```

## 🚀 Next Steps

Now that you have mastered the basic usage of pretty-loguru, you can:

- [Explore Visualization Features](../features/) - Rich blocks and ASCII art
- [View Practical Examples](../examples/) - Complete application scenarios
- [Learn about Framework Integration](../integrations/) - FastAPI and Uvicorn integration
- [Dive into the API Documentation](../api/) - Detailed technical reference

Start building beautiful and practical logging systems!
