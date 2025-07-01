# Guide

Welcome to the complete guide for pretty-loguru! This will take you from scratch to mastering this powerful logging library.

## 🎯 Learning Path

### 🚀 For Beginners
If you are using pretty-loguru for the first time, it is recommended to follow this order:

1. **[Installation](./installation)** - Environment setup and installation steps
2. **[Quick Start](./quick-start)** - Get started in 5 minutes
3. **[Basic Usage](./basic-usage)** - Core features and basic concepts

### 🎨 Exploring Features
After mastering the basics, explore the unique features of pretty-loguru:

4. **[Rich Block Logs](../features/rich-blocks)** - Structured visual logs
5. **[ASCII Art Headers](../features/ascii-art)** - Eye-catching titles
6. **[ASCII Art Blocks](../features/ascii-blocks)** - Combining blocks and art

### 🔧 Advanced Configuration
Dive deep into advanced features and best practices:

7. **[Custom Configuration](./custom-config)** - Customize logging behavior
8. **[Log Rotation](./log-rotation)** - File management and cleanup
9. **[Performance Optimization](./performance)** - Tuning for production environments

### 🌐 Application Integration
Integrate pretty-loguru into your projects:

10. **[FastAPI Integration](../integrations/fastapi)** - Web API logging
11. **[Uvicorn Integration](../integrations/uvicorn)** - ASGI server logging
12. **[Production Deployment](./production)** - Enterprise-level deployment guide

## 📚 Core Concepts

### Logger Initialization
pretty-loguru offers multiple initialization methods:

```python
from pretty_loguru import create_logger, create_logger

# Method 1: Quick Start (Recommended)
component_name = logger = create_logger(
    name="guide_demo",
    log_path="logs",
    level="INFO"
)

# Method 2: Custom Logger
my_logger = create_logger(
    name="my_app",
    level="DEBUG",
    log_path="custom_logs"
)

# Method 3: Advanced Configuration
from pretty_loguru import init_logger
init_logger(
    level="INFO",
    log_path="logs",
    component_name="web_app",
    rotation="10MB",
    retention="7 days"
)
```

### Log Levels
Supports standard log levels and adds a `success` level:

- `logger.debug()` - Debug messages
- `logger.info()` - General messages  
- `logger.success()` - Success messages (displayed in green)
- `logger.warning()` - Warning messages
- `logger.error()` - Error messages
- `logger.critical()` - Critical errors

### Visualization Features
The specialty of pretty-loguru lies in its rich visual output:

```python
# Rich Block
logger.block("Title", ["Content 1", "Content 2"], border_style="green")

# ASCII Header
logger.ascii_header("STARTUP", font="slant")

# ASCII Block (combining both)
logger.ascii_block(
    "Report",
    ["Status: Normal", "Time: 10:30"],
    ascii_header="REPORT",
    ascii_font="small"
)
```

## 🎮 Interactive Examples

Want to try it out now? Check out our [Example Collection](../examples/), which includes:

- [Basic Usage Examples](../examples/basics/) - Start simple
- [Visualization Examples](../examples/visual/) - Showcase all visual features
- [FastAPI Examples](../examples/fastapi/) - Web application integration
- [Production Environment Examples](../examples/production/) - Real-world deployment cases

## ❓ Having Problems?

- Check the [FAQ](../faq) 
- Refer to the [API Documentation](../api/)
- Submit an issue on [GitHub](https://github.com/JonesHong/pretty-loguru/issues)

Let's start this elegant logging journey! 🚀
