# pretty-loguru
![pretty-loguru.icon](https://raw.githubusercontent.com/JonesHong/pretty-loguru/refs/heads/master/docs/source/_static/logo.png)

[![PyPI version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![Python Version](https://img.shields.io/pypi/pyversions/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![License](https://img.shields.io/pypi/l/pretty-loguru.svg)](https://opensource.org/licenses/MIT)
## Description

**pretty-loguru** is a Python logging library that extends the power of [Loguru](https://github.com/Delgan/loguru) with elegant outputs using [Rich](https://github.com/Textualize/rich) panels, ASCII [art](https://github.com/sepandhaghighi/art) headers, and customizable blocks. It provides:

- **Rich Panels**: Display structured log blocks with borders and styles.
- **ASCII Art Headers**: Generate eye-catching headers using the `art` library.
- **ASCII Blocks**: Combine ASCII art and block logs for comprehensive sections.
- **FIGlet Support**: Use FIGlet fonts for even more impressive text art (optional).
- **Multiple Logger Management**: Create, retrieve, and manage multiple logger instances.
- **Time-based Log Files**: Auto-organize logs by date, hour, or minute.
- **Subdirectory Support**: Organize logs in nested directories by component.
- **Easy Initialization**: One-call setup for both file and console logging.
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
from pretty_loguru import create_logger, logger, print_block

# Create a logger with a specific name and configuration
app_logger = create_logger(
    name="app",
    service_tag="my_application",
    log_name_preset="daily",  # Use daily log files
    subdirectory="services/api"  # Save in logs/services/api/
)

# Basic logging
app_logger.info("Application started")
app_logger.success("Database connected")
app_logger.warning("Cache nearly full")
app_logger.error("API request failed")

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

Create multiple loggers with different configurations:

```python
from pretty_loguru import create_logger, get_logger, list_loggers

# Create loggers for different components
db_logger = create_logger(
    name="database",
    service_tag="db_service",
    subdirectory="database",
    log_name_preset="hourly"
)

auth_logger = create_logger(
    name="auth",
    service_tag="auth_service",
    subdirectory="auth",
    level="DEBUG"
)

# Get an existing logger by name
auth_log = get_logger("auth")

# List all registered loggers
all_loggers = list_loggers()  # Returns ["database", "auth"]
```

### Time-based Log Files

Choose from various log filename formats:

```python
from pretty_loguru import create_logger

# Daily logs: logs/api/20250429_api_service.log
api_logger = create_logger(
    name="api",
    service_tag="api_service",
    log_name_preset="daily"
)

# Hourly logs: logs/worker/20250429_14_worker_service.log
worker_logger = create_logger(
    name="worker",
    service_tag="worker_service",
    log_name_preset="hourly"
)

# Minute-level logs: logs/critical/20250429_1430_critical_service.log
critical_logger = create_logger(
    name="critical",
    service_tag="critical_service",
    log_name_preset="minute"
)

# Custom format
custom_logger = create_logger(
    name="custom",
    service_tag="custom_service",
    log_name_format="{year}-{month}-{day}_{service_tag}.log"
)
```

Available presets:
- `"default"`: "[{component_name}]{timestamp}.log"
- `"daily"`: "{date}_{component_name}.log"
- `"hourly"`: "{date}_{hour}_{component_name}.log"
- `"minute"`: "{date}_{hour}{minute}_{component_name}.log"
- `"simple"`: "{component_name}.log"
- `"detailed"`: "[{component_name}]_{date}_{time}.log"

### Output Targeting

Control where logs appear:

```python
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
    name="api",
    service_tag="api_service",
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
    name="configured",
    service_tag="config_service",
    level=config.level,
    rotation=config.rotation,
    log_path=config.log_path
)
```

## Advanced Configuration

Customize logger with advanced options:

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="advanced",
    service_tag="advanced_app",
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

## Backward Compatibility

For those upgrading from older versions:

```python
from pretty_loguru import logger, logger_start

# Old-style initialization (still supported)
component_name = logger_start(
    file=__file__,
    folder="my_app"
)

# Using the global logger
logger.info("Using global logger instance")
```


## Contributing

Contributions welcome! Please open issues and pull requests on [GitHub](https://github.com/yourusername/pretty-loguru).

## License

This project is licensed under the [MIT License](LICENSE).