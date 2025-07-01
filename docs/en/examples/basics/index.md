# Basic Usage Examples

This section demonstrates the basic features of pretty-loguru, suitable for beginners to get started quickly.

## 📖 Contents of this Chapter

- **[Simple Usage](./simple-usage)** - The most basic initialization and log output
- **[Console vs. File](./console-vs-file)** - Understand the differences between different output targets
- **[Target-Oriented Logging](./target-logging)** - Precisely control the log output location

## 🚀 Quick Preview

### Getting Started Simply

```python
from pretty_loguru import create_logger

# One-line initialization
component_name = logger = create_logger(
    name="basics_demo",
    log_path="my_logs",
    level="INFO"
)

# Start logging
logger.info("Application has started")
logger.success("Initialization complete")
logger.warning("This is a warning")
logger.error("This is an error")
```

### Console vs. File Output

```python
# Output to both console and file simultaneously (default)
logger.info("This will appear in two places")

# Output only to the console
logger.console_info("Display only in the console")

# Write only to the file
logger.file_info("Write only to the log file")
```

### Target-Oriented Logging

```python
# Target-oriented logging at different levels
logger.console_debug("Console debug message")
logger.file_debug("File debug message")
logger.console_error("Console error message")
logger.file_error("File error message")
```

## ⏱️ Learning Time

- **Total**: Approximately 10 minutes
- **Simple Usage**: 2 minutes
- **Console vs. File**: 3 minutes  
- **Target-Oriented Logging**: 5 minutes

## 🎯 Learning Objectives

After completing this chapter, you will be able to:

✅ Correctly initialize pretty-loguru  
✅ Use basic log levels  
✅ Understand the difference between console and file output  
✅ Precisely control the output target of your logs  

## 🚀 Start Learning

Choose an example to begin:

- 👶 **Beginner**: Start with [Simple Usage](./simple-usage)
- 🎯 **Advanced**: Go directly to [Target-Oriented Logging](./target-logging)

Ready? Let's get started! 🎮
