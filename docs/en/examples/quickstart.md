# Quick Start Examples

This page demonstrates Pretty-Loguru's quick start examples.

## Hello World

The simplest way to use:

```python
#!/usr/bin/env python3
"""
🎯 Pretty-Loguru Hello World
The simplest usage example - beautify logs with just 3 lines of code
"""

from pretty_loguru import create_logger

# Create logger
logger = create_logger("hello_world")

# Start logging
logger.info("Hello, Pretty-Loguru! 🌟")
logger.success("Congratulations! You've successfully used Pretty-Loguru")
logger.warning("This is a warning message")
logger.error("This is an error message")
```

Output:
```
2025-07-12 21:47:50 | INFO    | hello_world:main:27 - Hello, Pretty-Loguru! 🌟
2025-07-12 21:47:50 | SUCCESS | hello_world:main:28 - Congratulations! You've successfully used Pretty-Loguru
2025-07-12 21:47:50 | WARNING | hello_world:main:29 - This is a warning message
2025-07-12 21:47:50 | ERROR   | hello_world:main:30 - This is an error message
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/hello_world.py)

## Console Logging

Console-only output configuration:

```python
from pretty_loguru import create_logger

# Create console-only logger (no log_path specified)
logger = create_logger("console_app")

# Basic log levels
logger.debug("Debug message - detailed info for development")
logger.info("Info message - normal program operation info")
logger.success("Success message - operation completed successfully")
logger.warning("Warning message - needs attention but doesn't affect operation")
logger.error("Error message - error occurred but program can continue")
logger.critical("Critical error - program may not continue")

# Use visual features
logger.block(
    "System Status",
    [
        "🟢 Service Status: Running",
        "📊 CPU Usage: 45%",
        "💾 Memory Usage: 2.3GB / 8GB",
        "🌡️ System Temperature: Normal"
    ],
    border_style="green"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/console_logging.py)

## File Logging

Output to both console and file:

```python
from pretty_loguru import create_logger

# Create logger that outputs to both console and file
logger = create_logger(
    "file_app",
    log_path="logs",           # Log directory
    rotation="1 day",          # Daily rotation
    retention="7 days",        # Keep for 7 days
    compression="zip"          # Compress old files
)

# Log different types of messages
logger.info("Application started")
logger.debug("Loading config file: config.json")
logger.success("Database connection successful")
logger.warning("Cache about to expire")
logger.error("Unable to connect to external API")

# ASCII art header (appears in both console and file)
logger.ascii_header("APP START", font="small")

# Structured logging
logger.block(
    "Startup Info",
    [
        "Version: 1.0.0",
        "Environment: Production",
        "Config: Loaded",
        "Services: All running"
    ]
)

# Target-specific output
logger.console_info("This only shows in console")
logger.file_info("This only goes to the log file")
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/file_logging.py)

## Configuration Templates

Using predefined configuration templates:

```python
from pretty_loguru import ConfigTemplates

# Development configuration - detailed logs for debugging
dev_config = ConfigTemplates.development()
dev_logger = dev_config.apply_to("dev_app")

# Production configuration - optimized for performance
prod_config = ConfigTemplates.production()
prod_logger = prod_config.apply_to("prod_app")

# Daily rotation - perfect for regular applications
daily_config = ConfigTemplates.daily()
daily_logger = daily_config.apply_to("daily_app")

# Quick comparison
dev_logger.debug("This appears in development")  # ✅ Logged
prod_logger.debug("This won't appear in production")  # ❌ Not logged

# Visual demonstration
dev_logger.console_block(
    "Development Mode",
    [
        "Log Level: DEBUG",
        "Rotation: 10 MB",
        "Retention: 7 days",
        "Compression: None"
    ],
    border_style="yellow"
)

prod_logger.console_block(
    "Production Mode",
    [
        "Log Level: INFO",
        "Rotation: 50 MB",
        "Retention: 30 days",
        "Compression: ZIP"
    ],
    border_style="green"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/configuration_templates.py)

## Visual Features

Quick examples of visual features:

```python
from pretty_loguru import create_logger

logger = create_logger("visual_demo")

# 1. Rich Blocks
logger.block(
    "📊 Server Statistics",
    [
        "Uptime: 15 days",
        "Requests: 1.2M",
        "Errors: 0.01%",
        "Avg Response: 45ms"
    ],
    border_style="blue"
)

# 2. Panel with Rich objects
from rich.table import Table

table = Table(title="Performance Metrics")
table.add_column("Metric", style="cyan")
table.add_column("Value", style="green")
table.add_row("QPS", "1,500")
table.add_row("Latency", "25ms")

logger.panel(
    table,
    title="Real-time Performance",
    border_style="green"
)

# 3. ASCII Art Headers
logger.ascii_header("WELCOME", font="slant", border_style="purple")

# 4. Combined visual elements
logger.ascii_block(
    "Deployment Status",
    [
        "✅ Code: Updated",
        "✅ Tests: Passed",
        "✅ Build: Successful",
        "✅ Deploy: Complete"
    ],
    ascii_header="DEPLOYED",
    ascii_font="small",
    border_style="green"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/visual_features.py)

## Error Handling

Basic error handling with Pretty-Loguru:

```python
from pretty_loguru import create_logger

logger = create_logger("error_demo", log_path="logs/errors")

# Automatic exception catching
@logger.catch
def risky_function(x):
    """This function will log exceptions automatically"""
    return 10 / x

# Test the function
try:
    result = risky_function(0)  # This will cause an error
except Exception:
    # The error is already logged by @logger.catch
    pass

# Manual error logging
try:
    # Some operation that might fail
    import requests
    response = requests.get("https://api.example.com", timeout=1)
except Exception as e:
    logger.error(f"API call failed: {e}")
    logger.exception("Detailed error information:")
    
    # Visual error report
    logger.block(
        "❌ Error Report",
        [
            f"Type: {type(e).__name__}",
            f"Message: {str(e)}",
            "Action: Check network connection",
            "Retry: In 5 minutes"
        ],
        border_style="red"
    )
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/error_handling.py)

## FastAPI Quick Start

Quick FastAPI integration:

```python
from fastapi import FastAPI
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

# Create FastAPI app
app = FastAPI()

# Setup Pretty-Loguru logging
logger = setup_fastapi_logging(app, log_path="logs/api")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}

@app.get("/status")
async def status():
    # Visual status display
    logger.console_block(
        "API Status",
        [
            "🟢 API: Online",
            "🟢 Database: Connected",
            "🟢 Cache: Active",
            "📊 Requests Today: 10,432"
        ],
        border_style="green"
    )
    return {"status": "healthy"}

# Run with: uvicorn quickstart_api:app --reload
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/quickstart_api.py)

## Multi-Logger Quick Start

Managing multiple loggers:

```python
from pretty_loguru import create_logger, LoggerConfig

# Create a shared configuration
config = LoggerConfig(
    level="INFO",
    log_path="logs",
    rotation="1 day",
    retention="7 days"
)

# Create multiple loggers with the same config
app_logger = create_logger("app", config=config)
db_logger = create_logger("database", config=config)
api_logger = create_logger("api", config=config)

# Use different loggers for different components
app_logger.info("Application started")
db_logger.success("Database connected")
api_logger.warning("API rate limit approaching")

# Update all loggers at once
config.update(level="DEBUG")  # All three loggers now log DEBUG messages

# Visual summary
from pretty_loguru import list_loggers

logger = create_logger("summary")
logger.console_block(
    "Active Loggers",
    list_loggers(),
    border_style="cyan"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/01_quickstart/multi_logger.py)

## Next Steps

Now that you've seen the basics, explore more:

- [Basic Features](./basics.md) - Core functionality in detail
- [Visual Features](./visual.md) - Rich blocks, ASCII art, and more
- [Configuration](./configuration.md) - Advanced configuration options
- [FastAPI Integration](./integrations.md) - Web framework integration