# pretty-loguru

[![PyPI version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![Python Version](https://img.shields.io/pypi/pyversions/pretty-loguru.svg)]

## Description

**pretty-loguru** is a Python logging library that extends the power of [Loguru](https://github.com/Delgan/loguru) with elegant outputs using [Rich](https://github.com/Textualize/rich) panels, ASCII art headers, and customizable blocks. It provides:

- **Rich Panels**: Display structured log blocks with borders and styles.
- **ASCII Art Headers**: Generate eye-catching headers using the `art` library.
- **ASCII Blocks**: Combine ASCII art and block logs for comprehensive sections.
- **Easy Initialization**: One-call setup for both file and console logging.
- **Uvicorn Integration**: Intercept and unify Uvicorn logs with Loguru formatting.

## Installation

Install via pip:

```bash
pip install pretty-loguru
```

## Quick Start

```python
from pretty_loguru import logger, logger_start

# Initialize the logger (creates file handler + console handler)
process_id = logger_start(folder="my_app")
logger.info("Logger initialized.")

# Basic logging
logger.debug("Debug message.")
logger.success("Operation was successful.")
logger.warning("This is a warning.")
logger.error("An error occurred.")
```

## Features

### Rich Block Logging

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

### Uvicorn Integration

```python
from pretty_loguru import uvicorn_init_config
uvicorn_init_config()
```

## Configuration

Customize file path, rotation, and level:

```python
from pretty_loguru import init_logger

init_logger(
    level="DEBUG",
    log_path="logs",
    process_id="my_app",
    rotation="10MB"
)
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

Contributions welcome! Please open issues and pull requests on [GitHub](https://github.com/yourusername/pretty-loguru).

## License

This project is licensed under the [MIT License](LICENSE).

