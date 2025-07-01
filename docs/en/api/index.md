# API Reference

Welcome to the complete API documentation for pretty-loguru. Here you'll find detailed descriptions and usage examples for all public APIs.

## 📚 API Overview

### Core Module - `pretty_loguru`

Main imports and functions:

```python
from pretty_loguru import (
    create_logger,    # Create custom logger (RECOMMENDED)
    logger,           # Main logger instance (legacy)
    logger_start,     # Quick initialization function (legacy)
    init_logger,      # Advanced initialization
    is_ascii_only     # Utility function
)
```

### Main Classes

| Class/Function | Purpose | Module |
|----------------|---------|--------|
| `logger` | Main logging instance | `pretty_loguru` |
| `create_logger()` | Create custom logger | `pretty_loguru.factory` |
| `create_logger()` | Create custom logger | `pretty_loguru.factory` |
| `init_logger()` | Advanced initialization | `pretty_loguru.core` |

## 🚀 Core API

### Recommended Usage Pattern

The modern and recommended way to use pretty-loguru:

```python
from pretty_loguru import create_logger

# Create your logger instance
logger = create_logger(
    name="my_app",
    log_path="logs",
    level="INFO"
)

# Use the logger
logger.info("Application started")
```

### `logger` - Main Logger Instance

This is the object you'll use most frequently, providing all logging functionality.

#### Basic Logging Methods

```python
# Standard log levels
logger.debug(message)    # Debug messages
logger.info(message)     # General messages
logger.success(message)  # Success messages (unique feature)
logger.warning(message)  # Warning messages
logger.error(message)    # Error messages
logger.critical(message) # Critical errors
```

#### Visualization Methods

```python
# Rich blocks
logger.block(title, content_list, border_style="solid", log_level="INFO")

# ASCII art headers
logger.ascii_header(text, font="standard", border_style="solid", log_level="INFO")

# ASCII art blocks
logger.ascii_block(title, content_list, ascii_header, ascii_font="standard", 
                  border_style="solid", log_level="INFO")
```

#### Target-specific Methods

```python
# Console-only output
logger.console_debug(message)
logger.console_info(message)
logger.console_success(message)
logger.console_warning(message)
logger.console_error(message)
logger.console_critical(message)

# File-only output
logger.file_debug(message)
logger.file_info(message)
logger.file_success(message)
logger.file_warning(message)
logger.file_error(message)
logger.file_critical(message)
```

### `create_logger()` - Create Custom Logger

Create a logger instance with specific name and configuration.

```python
def create_logger(
    name: str,
    log_path: Optional[str] = None,
    level: str = "DEBUG", 
    rotation: str = "10MB",
    retention: str = "7 days",
    compression: str = "zip"
) -> Logger
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `folder` | `str` | `"logs"` | Log folder name |
| `level` | `str` | `"DEBUG"` | Minimum log level |
| `rotation` | `str` | `"10MB"` | File rotation condition |
| `retention` | `str` | `"7 days"` | File retention time |
| `compression` | `str` | `"zip"` | Compression format |

**Returns:**
- `str`: Auto-generated component name

**Examples:**

```python
# Basic usage
logger = create_logger(
    name="demo",
    log_path="logs"
)

# Custom configuration
logger = create_logger(
    name="api_service",
    log_path="api_logs",
    level="INFO",
    rotation="50MB", 
    retention="30 days"
)
```

### `create_logger()` - Create Custom Logger

Create a logger instance with specific name and configuration.

```python
def create_logger(
    name: str,
    level: str = "DEBUG",
    log_path: Optional[str] = None,
    rotation: str = "10MB",
    retention: str = "7 days",
    compression: str = "zip"
) -> Logger
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Logger name |
| `level` | `str` | `"DEBUG"` | Minimum log level |
| `log_path` | `Optional[str]` | `None` | Log file path |
| `rotation` | `str` | `"10MB"` | File rotation condition |
| `retention` | `str` | `"7 days"` | File retention time |
| `compression` | `str` | `"zip"` | Compression format |

**Examples:**

```python
# Create dedicated API logger
api_logger = create_logger(
    name="api_service",
    level="INFO",
    log_path="logs/api"
)

api_logger.info("API service started")
```

## 🎨 Visualization API

### `logger.block()` - Rich Blocks

Create structured Rich panels.

```python
def block(
    title: str,
    content: List[str],
    border_style: str = "solid",
    log_level: str = "INFO"
) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | `str` | Block title |
| `content` | `List[str]` | Content list |
| `border_style` | `str` | Border style: `"solid"`, `"double"`, `"rounded"`, `"thick"`, etc. |
| `log_level` | `str` | Log level: `"DEBUG"`, `"INFO"`, `"SUCCESS"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"` |

**Examples:**

```python
logger.block(
    "System Status",
    [
        "CPU: 25%",
        "Memory: 60%",
        "Disk: 80%"
    ],
    border_style="green",
    log_level="INFO"
)
```

### `logger.ascii_header()` - ASCII Art Headers

Create ASCII art text headers.

```python
def ascii_header(
    text: str,
    font: str = "standard",
    border_style: str = "solid", 
    log_level: str = "INFO"
) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Text to convert (ASCII characters only) |
| `font` | `str` | Font name: `"standard"`, `"slant"`, `"doom"`, `"small"`, `"block"`, etc. |
| `border_style` | `str` | Border style and color |
| `log_level` | `str` | Log level |

**Available Fonts:**

- `"standard"` - Standard font
- `"slant"` - Italic font
- `"doom"` - Bold font
- `"small"` - Small font
- `"block"` - Block font
- `"digital"` - Digital font

**Examples:**

```python
logger.ascii_header("STARTUP", font="slant", border_style="blue")
```

### `logger.ascii_block()` - ASCII Art Blocks

Combine ASCII headers with Rich blocks.

```python
def ascii_block(
    title: str,
    content: List[str],
    ascii_header: str,
    ascii_font: str = "standard",
    border_style: str = "solid",
    log_level: str = "INFO"
) -> None
```

**Examples:**

```python
logger.ascii_block(
    "Deployment Report",
    [
        "Service: Web API",
        "Version: v1.2.0",
        "Status: Success"
    ],
    ascii_header="DEPLOYED",
    ascii_font="block",
    border_style="green"
)
```

## 🛠️ Utility Functions

### `is_ascii_only()` - ASCII Check

Check if a string contains only ASCII characters.

```python
def is_ascii_only(text: str) -> bool
```

**Examples:**

```python
from pretty_loguru import is_ascii_only

print(is_ascii_only("Hello World"))    # True
print(is_ascii_only("Hello 世界"))      # False
```

## 🔧 Configuration Options

### Log Levels

```python
LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "SUCCESS": 25,    # pretty-loguru specific
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}
```

### Rotation Options

```python
# Rotate by size
rotation="10MB"    # 10 MB
rotation="100KB"   # 100 KB
rotation="1GB"     # 1 GB

# Rotate by time
rotation="1 day"   # Daily
rotation="1 week"  # Weekly
rotation="1 hour"  # Hourly
```

### Retention Options

```python
retention="7 days"    # Keep for 7 days
retention="2 weeks"   # Keep for 2 weeks
retention="1 month"   # Keep for 1 month
retention=10          # Keep 10 files
```

### Compression Options

```python
compression="zip"    # ZIP compression
compression="gz"     # GZIP compression
compression="bz2"    # BZIP2 compression
compression=None     # No compression
```

## 🎯 Practical Applications

### Web Application Integration

```python
from pretty_loguru import create_logger

# FastAPI application
def setup_logging():
    return create_logger(
        name="api_service",
        log_path="api_logs",
        level="INFO"
    )

# Middleware usage
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"API request: {request.method} {request.url} - {response.status_code} ({process_time:.3f}s)")
    return response
```

### Error Handling

```python
try:
    # Some potentially failing operation
    result = risky_operation()
    logger.success("Operation completed successfully")
except Exception as e:
    logger.error(f"Operation failed: {e}")
    
    # Detailed error report
    logger.block(
        "Error Details",
        [
            f"Error type: {type(e).__name__}",
            f"Error message: {str(e)}",
            f"Timestamp: {datetime.now()}",
            "Suggested action: Check input parameters"
        ],
        border_style="red",
        log_level="ERROR"
    )
```

## 📖 More Resources

- [Features](../features/) - Detailed feature descriptions and examples
- [Integrations](../integrations/) - Integration with other frameworks
- [Examples](../examples/) - Real-world usage scenarios
- [GitHub](https://github.com/JonesHong/pretty-loguru) - Source code and issue reporting

This API reference covers all major features of pretty-loguru. For more detailed explanations or examples, please check the related sections.