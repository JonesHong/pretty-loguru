# Basic Features Examples

This page demonstrates Pretty-Loguru's core features and usage patterns.

## Simple Usage

Demonstrating the most basic logger creation and usage:

```python
from pretty_loguru import create_logger

# The simplest way - just need a name
logger = create_logger("simple_demo")

# Start logging
logger.info("This is a simple start")
logger.success("See! Using Pretty-Loguru is that easy!")

# With file output
logger_with_file = create_logger(
    name="with_file",
    log_path="logs/demo"
)

# Custom level and format
custom_logger = create_logger(
    name="custom",
    level="DEBUG",
    log_path="logs/custom",
    rotation="100 MB",
    retention="30 days"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/simple_usage.py)

## Multiple Logger Management

Managing multiple loggers in large applications:

```python
from pretty_loguru import create_logger, LoggerConfig, list_loggers

# Create loggers for different modules
app_logger = create_logger("app", log_path="logs/app")
db_logger = create_logger("database", log_path="logs/db", level="DEBUG")
api_logger = create_logger("api", log_path="logs/api", level="WARNING")

# Use unified configuration
config = LoggerConfig(
    level="INFO",
    log_path="logs/services",
    rotation="1 day",
    retention="7 days"
)

# Create multiple loggers with same config
auth_logger = create_logger("auth", config=config)
payment_logger = create_logger("payment", config=config)

# List all loggers
print(f"Registered loggers: {list_loggers()}")

# Hierarchical naming
main_logger = create_logger("myapp")
user_logger = create_logger("myapp.user")
order_logger = create_logger("myapp.order")
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/multiple_loggers.py)

## Console vs File Output

Controlling output targets separately:

```python
from pretty_loguru import create_logger

logger = create_logger("output_demo", log_path="logs")

# Output to both console and file
logger.info("This message appears in console and file")

# Console only
logger.console_info("This message only shows in console")
logger.console_success("✅ Console-exclusive success message")

# File only
logger.file_info("This message only logs to file")
logger.file_error("File-exclusive error log")

# Visual elements with target control
logger.console_block(
    "Console-exclusive block",
    ["Won't appear in log files", "Only shows in terminal"],
    border_style="cyan"
)

logger.file_block(
    "File-exclusive block",
    ["Won't appear in console", "Only in log files"],
    border_style="yellow"
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/02_basics/console_vs_file.py)

## Log Levels and Colors

Understanding log levels and their visual representation:

```python
from pretty_loguru import create_logger

logger = create_logger("levels_demo")

# Standard log levels
logger.debug("Debug information - for development")
logger.info("General information")
logger.success("Operation completed successfully ✅")
logger.warning("Warning: something needs attention")
logger.error("Error occurred but application continues")
logger.critical("Critical error - immediate action required!")

# Conditional logging based on level
debug_logger = create_logger("debug_app", level="DEBUG")
prod_logger = create_logger("prod_app", level="WARNING")

# This appears in debug_logger but not prod_logger
debug_logger.debug("Detailed debugging info")
prod_logger.debug("This won't be logged")

# Level filtering
@logger.catch(level="ERROR")
def risky_operation():
    # Only errors and above will be caught
    raise ValueError("Something went wrong")
```

## Error Handling

Proper error logging and exception handling:

```python
from pretty_loguru import create_logger

logger = create_logger("error_demo")

# Basic error handling
try:
    result = 10 / 0
except Exception as e:
    logger.error(f"Calculation failed: {e}")
    logger.exception("Detailed error with traceback:")

# Using decorator for automatic error catching
@logger.catch
def process_data(data):
    # Any exception will be automatically logged
    return data["key"]

# Custom error messages
@logger.catch(message="Failed to process user data")
def process_user(user_id):
    # Custom message on error
    user = get_user(user_id)  # May raise exception
    return user.process()

# Error context
with logger.contextualize(transaction_id="12345"):
    try:
        perform_transaction()
    except Exception:
        logger.exception("Transaction failed")
        # Log will include transaction_id in context
```

## Structured Logging

Adding context and structured data to logs:

```python
from pretty_loguru import create_logger

logger = create_logger("structured_demo")

# Bind contextual data
user_logger = logger.bind(user_id=123, session="abc-def")
user_logger.info("User action performed")
# Output includes user_id and session

# Temporary context
with logger.contextualize(request_id="req-789"):
    logger.info("Processing request")
    # All logs within this block include request_id
    
# Add structured data to specific log
logger.info(
    "Order processed",
    order_id=456,
    amount=99.99,
    items=3
)

# Performance timing
import time
start = time.time()
# ... some operation ...
logger.success(
    "Operation completed",
    duration=time.time() - start,
    records_processed=1000
)
```

## Lazy Evaluation

Optimizing performance with lazy evaluation:

```python
from pretty_loguru import create_logger
import json

logger = create_logger("lazy_demo", level="INFO")

# Bad: expensive operation always runs
def bad_example(data):
    # JSON serialization happens even if DEBUG is disabled
    logger.debug(f"Data: {json.dumps(data, indent=2)}")

# Good: expensive operation only runs if needed
def good_example(data):
    # JSON serialization only happens if DEBUG is enabled
    logger.opt(lazy=True).debug(
        "Data: {data}",
        data=lambda: json.dumps(data, indent=2)
    )

# Conditional expensive operations
if logger.level("DEBUG").no:
    # Skip expensive debug preparations
    pass
else:
    debug_stats = calculate_expensive_stats()
    logger.debug(f"Stats: {debug_stats}")
```

## Next Steps

- [Visual Features](./visual.md) - Rich blocks, ASCII art, and more
- [Configuration](./configuration.md) - Advanced configuration options
- [Integrations](./integrations.md) - Framework integrations