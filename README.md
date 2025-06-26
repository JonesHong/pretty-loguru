# pretty-loguru
<p align="center">
  <img src="https://raw.githubusercontent.com/JonesHong/pretty-loguru/refs/heads/master/assets/images/logo.png" alt="pretty-loguru icon" width="200"/>
</p>


<p align="center">
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/pretty-loguru.svg">
  </a>
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pretty-loguru.svg">
  </a>
  <a href="https://joneshong.github.io/pretty-loguru/en/index.html">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-ghpages-blue.svg">
  </a>
  <a href="https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/JonesHong/pretty-loguru.svg">
  </a>
</p>


## Description

**pretty-loguru** is a Python logging library that extends the power of [Loguru](https://github.com/Delgan/loguru) with elegant outputs using [Rich](https://github.com/Textualize/rich) panels, ASCII [art](https://github.com/sepandhaghighi/art) and [pyfiglet](https://github.com/pwaller/pyfiglet) headers, and customizable blocks. It provides:

- **Rich Panels**: Display structured log blocks with borders and styles.
- **ASCII Art Headers**: Generate eye-catching headers using the `art` library.
- **ASCII Blocks**: Combine ASCII art and block logs for comprehensive sections.
- **FIGlet Support**: Use FIGlet fonts for even more impressive text art (optional).
- **Multiple Logger Management**: Create, retrieve, and manage multiple logger instances.
- **Logger Synchronization**: Proxy pattern for seamless logger reinitialization across modules.
- **Flexible File Output**: Optional file logging - console-only by default, like native loguru.
- **Smart Format Detection**: Automatic format selection based on usage patterns.
- **Time-based Log Files**: Auto-organize logs by date, hour, or minute.
- **Subdirectory Support**: Organize logs in nested directories by component.
- **Output Targeting**: Separate console-only and file-only logging methods.
- **Framework Integrations**: Ready-to-use integrations with Uvicorn and FastAPI.
- **Configuration Management**: Load and save configurations from various sources.

### Showcase

Here are some examples of using **pretty-loguru**:

#### Basic Log Output
![Basic Example Terminal](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_1_en_terminal.png)
![Basic Example File 1](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_1_en_file_1.png)
![Basic Example File 2](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_1_en_file_2.png)

#### Multiple Logger Management
![Multiple Logger Example Terminal](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_2_en_terminal.png)
![Multiple Logger Example File 1](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_2_en_file_1.png)
![Multiple Logger Example File 2](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_2_en_file_2.png)
![Multiple Logger Example File 3](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_2_en_file_3.png)

#### Special Format Output
![Special Format Example Terminal](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_3_en_terminal.png)
![Special Format Example File](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_3_en_file_1.png)

#### Different Output Targets
![Different Output Example Terminal](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_4_en_terminal.png)
![Different Output Example File](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_4_en_file_1.png)

#### Integrated Features
![Integrated Example Terminal](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_5_en_terminal.png)
![Integrated Example File](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_5_en_file_1.png)

#### Advanced Features and Customization
![Advanced Features and Customization Example Terminal 1](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_6_en_terminal_1.png)
![Advanced Features and Customization Example Terminal 2](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_6_en_terminal_2.png)
![Advanced Features and Customization Example File 1](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_6_en_file_1.png)
![Advanced Features and Customization Example File 2](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/assets/images/example_6_en_file_2.png)

### Example Code

For complete example code, refer to [examples/detailed_example_en.py](https://raw.githubusercontent.com/JonesHong/pretty-loguru/master/examples/detailed_example_en.py).


## Installation

Install via pip:

```bash
pip install pretty-loguru
```


## Quick Start

```python
from pretty_loguru import create_logger, print_block

# Console-only logger (like native loguru)
dev_logger = create_logger("dev_app")
dev_logger.info("Development message - console only")

# Logger with file output
app_logger = create_logger(
    name="my_application",
    log_path="./logs",  # Enable file logging
    log_name_preset="daily",  # Use daily log files
    subdirectory="services/api"  # Save in logs/services/api/
)

# Basic logging
app_logger.info("Application started")
app_logger.success("Database connected")
app_logger.warning("Cache nearly full")
app_logger.error("API request failed")

# Output targeting
app_logger.console_info("Console-only debug info")
app_logger.file_error("Critical error - file only")

# Block logging with borders
app_logger.block(
    "System Status",
    [
        "CPU: 45%",
        "Memory: 2.3GB / 8GB",
        "Uptime: 3d 12h 5m",
        "Status: Operational"
    ],
    border_style="green"
)

# ASCII art header
app_logger.ascii_header(
    "STARTUP COMPLETE",
    font="slant",
    border_style="blue"
)
```

## Features

### Logger Factory

Create and manage multiple loggers with different configurations:

```python
from pretty_loguru import create_logger, get_logger, list_loggers, reinit_logger

# Console-only logger (no log_path specified)
dev_logger = create_logger("development")

# File-enabled loggers with different configurations
db_logger = create_logger(
    name="database",
    log_path="./logs",
    subdirectory="database",
    log_name_preset="hourly"
)

auth_logger = create_logger(
    name="auth",
    log_path="./logs",
    subdirectory="auth",
    level="DEBUG"
)

# Get an existing logger by name
auth_log = get_logger("auth")

# List all registered loggers
all_loggers = list_loggers()  # Returns ["development", "database", "auth"]

# Reinitialize logger with new configuration
reinit_logger("database", log_path="./production_logs", level="WARNING")
```

### Flexible File Output

Control whether logs are written to files:

```python
from pretty_loguru import create_logger

# Console-only (like native loguru) - no files created
console_logger = create_logger("console_app")
console_logger.info("This only appears in console")

# File + console output 
file_logger = create_logger(
    name="file_app", 
    log_path="./logs"  # Enables file logging
)
file_logger.info("This appears in both console and file")

# Different file organization
api_logger = create_logger(
    name="api_service",
    log_path="./logs",
    log_name_preset="daily",
    subdirectory="api"  # logs/api/[api_service]daily_latest.temp.log
)

worker_logger = create_logger(
    name="worker_service", 
    log_path="./logs",
    log_name_preset="hourly",
    subdirectory="workers"  # logs/workers/[worker_service]hourly_latest.temp.log
)

# Custom format
custom_logger = create_logger(
    name="custom_service",
    log_path="./logs",
    log_name_format="{year}-{month}-{day}_{name}.log"
)
```

Available presets:
- `"detailed"`: "[{component_name}]{timestamp}.log"
- `"simple"`: "{component_name}.log"
- `"minute"`: "[{component_name}]minute_latest.temp.log"
- `"hourly"`: "[{component_name}]hourly_latest.temp.log"
- `"daily"`: "[{component_name}]daily_latest.temp.log"
- `"weekly"`: "[{component_name}]weekly_latest.temp.log"
- `"monthly"`: "[{component_name}]monthly_latest.temp.log"

### Output Targeting

Control where logs appear:

```python
# Create logger with file output enabled
logger = create_logger("app", log_path="./logs")

# Regular log (both console and file)
logger.info("This appears everywhere")

# Console-only logs
logger.console_info("This only appears in the console")
logger.console_warning("Console-only warning")
logger.dev_info("Development info - console only")

# File-only logs  
logger.file_info("This only appears in the log file")
logger.file_error("File-only error message")
```

**Note**: If you use `file_*` methods on a console-only logger (no `log_path`), you'll get a warning and the message will be output to console instead.

### Rich Block Logging

Create structured log blocks with borders:

```python
logger.block(
    "System Summary",
    [
        "CPU Usage: 45%",
        "Memory Usage: 60%",
        "Disk Space: 120GB free"
    ],
    border_style="green",
    log_level="INFO"
)
```

### ASCII Art Headers

```python
logger.ascii_header(
    "APP START",
    font="slant",
    border_style="blue",
    log_level="INFO"
)
```

### ASCII Art Blocks

```python
logger.ascii_block(
    "Startup Report",
    ["Step 1: OK", "Step 2: OK", "Step 3: OK"],
    ascii_header="SYSTEM READY",
    ascii_font="small",
    border_style="cyan",
    log_level="SUCCESS"
)
```

### Logger Synchronization

Solve the cross-module logger synchronization problem using proxy pattern:

```python
# config/logger_config.py
from pretty_loguru import create_logger, reinit_logger

# Create logger with proxy enabled
app_logger = create_logger("app", use_proxy=True)

def init_logger(**kwargs):
    """Reinitialize logger - all imports will sync automatically"""
    return reinit_logger("app", **kwargs)

# modules/service.py  
from config.logger_config import app_logger

def do_work():
    app_logger.info("Working...")  # Always uses latest configuration

# main.py
from config.logger_config import init_logger

# Initialize with production settings
init_logger(log_path="./production_logs", level="WARNING")
# All modules automatically use new configuration!
```

### FIGlet Support (Optional)

If you install pyfiglet, you can use FIGlet fonts:

```python
logger.figlet_header(
    "WELCOME",
    font="big",
    border_style="magenta"
)

# List available fonts
fonts = logger.get_figlet_fonts()
logger.info(f"Available fonts: {list(fonts)[:5]}")
```

### Framework Integrations

#### Uvicorn Integration

```python
from pretty_loguru import configure_uvicorn

# Configure Uvicorn to use pretty-loguru
configure_uvicorn()
```

#### FastAPI Integration

```python
from fastapi import FastAPI
from pretty_loguru import setup_fastapi_logging, create_logger

# Create a logger for the API
api_logger = create_logger(
    name="api_service",
    log_path="./logs",
    subdirectory="api"
)

# Create FastAPI app
app = FastAPI()

# Configure FastAPI logging
setup_fastapi_logging(
    app,
    logger_instance=api_logger,
    log_request_body=True,
    log_response_body=True
)

@app.get("/")
def read_root():
    api_logger.info("Processing root request")
    return {"Hello": "World"}
```

### Configuration Management

Manage your logger configurations:

```python
from pretty_loguru import LoggerConfig
from pathlib import Path

# Create a configuration
config = LoggerConfig(
    level="DEBUG",
    rotation="10 MB",
    log_path=Path.cwd() / "logs" / "custom"
)

# Save to file
config.save_to_file("logger_config.json")

# Load from file
loaded_config = LoggerConfig.from_file("logger_config.json")

# Use in logger creation
from pretty_loguru import create_logger
logger = create_logger(
    name="config_service",
    level=config.level,
    rotation=config.rotation,
    log_path=config.log_path
)
```

## Advanced Configuration

### Smart Format Selection

pretty-loguru automatically selects the appropriate format based on usage:

```python
# No name provided -> uses native loguru format with {file}
logger1 = create_logger()
logger1.info("Message")  # Shows actual filename

# Name provided -> uses pretty-loguru format with enhanced info
logger2 = create_logger("my_service") 
logger2.info("Message")  # Shows service name, function, line number

# Custom format override
logger3 = create_logger(
    "custom_service",
    logger_format="{time} | {level} | {message}"
)
```

### Advanced Options

Customize logger with advanced options:

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="advanced_app",
    log_path="./logs",
    subdirectory="advanced",
    log_name_preset="daily",
    timestamp_format="%Y-%m-%d_%H-%M-%S",
    log_file_settings={
        "rotation": "500 KB",
        "retention": "1 week",
        "compression": "zip",
    },
    level="DEBUG",
    start_cleaner=True  # Auto-clean old logs
)
```

## Migration Guide

### Key Changes in Latest Version

1. **Console-only by default**: No files created unless `log_path` is specified
2. **Simplified parameters**: `service_tag` is deprecated, use `name` instead  
3. **Smart format selection**: Automatic format based on usage patterns
4. **Proxy support**: Solve cross-module synchronization with `use_proxy=True`

### Upgrading from Older Versions

```python
# OLD: Automatic file creation
logger = create_logger("app", service_tag="my_service")

# NEW: Explicit file control  
console_logger = create_logger("my_service")  # Console only
file_logger = create_logger("my_service", log_path="./logs")  # Files enabled

# OLD: Complex parameter combinations
logger = create_logger(name="app", service_tag="my_service")

# NEW: Simplified 
logger = create_logger("my_service")  # Single parameter

# NEW: Proxy for cross-module sync
logger = create_logger("my_service", use_proxy=True)
reinit_logger("my_service", log_path="./production")  # All modules sync
```

## API Reference

### Core Functions

- `create_logger(name, log_path=None, use_proxy=False, ...)` - Create logger instance
- `get_logger(name)` - Get existing logger by name
- `reinit_logger(name, **kwargs)` - Reinitialize logger with new config
- `list_loggers()` - List all registered logger names
- `default_logger()` - Get default logger instance

### Output Methods

- `logger.info/debug/warning/error/critical()` - Standard logging
- `logger.console_*()` - Console-only output
- `logger.file_*()` - File-only output (warns if no file configured)
- `logger.block()` - Rich bordered blocks
- `logger.ascii_header()` - ASCII art headers
- `logger.figlet_header()` - FIGlet headers (if pyfiglet installed)


## Contributing

Contributions welcome! Please open issues and pull requests on [GitHub](https://github.com/yourusername/pretty-loguru).

## License

This project is licensed under the [MIT License](LICENSE).