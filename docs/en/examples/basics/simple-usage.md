# Simple Usage

This is the most basic example of using pretty-loguru, demonstrating how to quickly start logging.

## 🎯 Learning Objectives

- Understand the usage of `create_logger()`
- Master the basic log levels
- Understand automatic management of log files

## 💻 Basic Example

### The Simplest Start

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="simple_usage_demo",
    log_path="simple_logs",
    level="INFO"
)

# Basic log output
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.success("This is a success message")  # Success level specific to pretty-loguru
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

### Execution Results

**Console Output:**
```
Log component ID: simple_logs_20240630_143022
2024-06-30 14:30:22.123 | DEBUG    | __main__:<module>:8 - This is a debug message
2024-06-30 14:30:22.124 | INFO     | __main__:<module>:9 - This is an info message
2024-06-30 14:30:22.125 | SUCCESS  | __main__:<module>:10 - This is a success message
2024-06-30 14:30:22.126 | WARNING  | __main__:<module>:11 - This is a warning message
2024-06-30 14:30:22.127 | ERROR    | __main__:<module>:12 - This is an error message
2024-06-30 14:30:22.128 | CRITICAL | __main__:<module>:13 - This is a critical message
```

**File Output:**
A log file will be generated in the `simple_logs/` directory, for example:
`[simple_logs_20240630_143022]_20240630-143022.log`

## 🔧 Parameter Explanation

### `create_logger()` Parameters

```python
logger = create_logger(
    name="demo",               // Logger name (required)
    log_path="logs",           // Log folder path (required)
    level="DEBUG",             // Log level (optional)
    rotation="10MB",           // File rotation size (optional)
    retention="7 days"         // Retention period (optional)
)
```

### Log Level Descriptions

| Level    | Purpose                  | Color      |
|----------|--------------------------|------------|
| `DEBUG`  | Debug information        | Blue       |
| `INFO`   | General information      | White      |
| `SUCCESS`| Success messages         | Green      |
| `WARNING`| Warning messages         | Yellow     |
| `ERROR`  | Error messages           | Red        |
| `CRITICAL`| Critical errors          | Red (Bold) |

## 🎮 Practical Exercises

### Exercise 1: Basic Logging

Create a simple Python script:

```plogger  
# practice_1.py
from pretty_loguru import create_logger

def main():
    # Initialize logging
    logger = create_logger(
    name="simple-usage_demo",
    log_path="practice_logs",
    level="INFO"
)
    
    # Simulate application startup
    logger.info("Application is starting...")
    logger.debug("Loading configuration file...")
    logger.success("Configuration file loaded successfully")
    
    # Simulate some operations
    logger.info("Connecting to the database...")
    logger.success("Database connection successful")
    
    logger.info("Starting web server...")
    logger.success("Server started, listening on port 8080")
    
    logger.warning("Memory usage is high: 75%")
    
    # Simulate an error
    try:
        result = 1 / 0  # This will cause an error
    except ZeroDivisionError:
        logger.error("A division by zero error occurred")
    
    logger.critical("Application is about to shut down")

if __name__ == "__main__":
    main()
```

### Exercise 2: Testing Different Levels

```python
# practice_2.py
from pretty_loguru import create_logger
import time

def test_all_levels():
    logger = create_logger(
    name="simple-usage_demo",
    log_path="level_test",
    level="INFO"
)
    
    # Test all log levels
    levels = [
        ("debug", "Debug mode is enabled"),
        ("info", "System is running normally"),
        ("success", "Task executed successfully"),
        ("warning", "Disk space is low"),
        ("error", "Network connection failed"),
        ("critical", "System is about to crash")
    ]
    
    for level, message in levels:
        getattr(logger, level)(f"{level.upper()}: {message}")
        time.sleep(0.5)  # Pause to observe

if __name__ == "__main__":
    test_all_levels()
```

## 📁 File Structure

After running the examples, your directory structure will be:

```
your_project/
├── practice_1.py
├── practice_2.py
├── practice_logs/
│   └── [practice_logs_20240630_143022]_20240630-143022.log
└── level_test/
    └── [level_test_20240630_143500]_20240630-143500.log
```

## 💡 Important Concepts

### 1. Automatic Component Naming
`create_logger()` automatically generates a unique component name in the format:
`{folder_name}_{timestamp}`

### 2. Simultaneous Output
By default, logs are simultaneously:
- Displayed in the console (with color)
- Written to a file (plain text)

### 3. Automatic File Management
pretty-loguru automatically:
- Creates the log folder
- Generates a timestamped filename
- Manages file rotation

## ❓ Frequently Asked Questions

### Q: Why can't I see DEBUG level logs?
A: By default, the DEBUG level might be filtered in a production environment. You can set it explicitly:
```python
logger = create_logger(
    name="simple-usage_demo",
    log_path="logs", level="DEBUG",
    level="INFO"
)
```

### Q: How to customize the log format?
A: This is an advanced feature. Please refer to the [Custom Configuration](../../guide/custom-config) section.

### Q: What to do if there are too many log files?
A: You can set up automatic cleanup:
```python
logger = create_logger(
    name="simple-usage_demo",
    log_path="logs", retention="7 days",
    level="INFO"
)
```

## 🚀 Next Steps

Congratulations! You have mastered the basic usage of pretty-loguru. Next, you can:

- [Learn about Console vs. File Output](./console-vs-file) - Learn to control output precisely
- [Explore Visualization Features](../visual/) - Experience Rich blocks and ASCII art
- [Check out Advanced Configuration](../../guide/custom-config) - Deep customization

You can now use pretty-loguru in any of your Python projects! 🎉
