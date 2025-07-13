# Pretty-Loguru 🎨

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An enhanced Python logging library built on [Loguru](https://github.com/Delgan/loguru), integrating [Rich](https://github.com/Textualize/rich) and ASCII art to make logging more elegant and intuitive.

## ✨ Features

- 🎨 **Rich Block Logging** - Display structured logs using Rich panels
- 🎯 **ASCII Art Headers** - Generate eye-catching ASCII art titles
- 🔥 **One-Click Setup** - Simple configuration for both file and console logging
- 🚀 **FastAPI Integration** - Perfect integration with FastAPI and Uvicorn
- 📊 **Preset Configurations** - Best practices for development, production, and testing
- 🛠️ **Highly Customizable** - Support for custom formats, colors, and rotation strategies

## 📦 Installation

```bash
pip install pretty-loguru
```

## 🚀 Quick Start

### Basic Usage

```python
from pretty_loguru import create_logger

# Create logger
logger = create_logger("my_app")

# Basic logging
logger.info("Application started")
logger.success("Operation completed successfully")
logger.warning("This is a warning")
logger.error("An error occurred")

# Rich blocks
logger.block("System Status", "Everything is running smoothly", border_style="green")

# ASCII art
logger.ascii_header("WELCOME", font="slant")
```

### Using Configuration Objects

```python
from pretty_loguru import create_logger, LoggerConfig, ConfigTemplates

# Use preset templates
config = ConfigTemplates.production()
logger = create_logger("app", config=config)

# Custom configuration
custom_config = LoggerConfig(
    level="DEBUG",
    log_path="logs",
    rotation="1 day",
    retention="7 days"
)
logger = create_logger("debug_app", config=custom_config)

# Update existing logger
config.update(level="INFO")  # All loggers using this config will update
```

### Multi-Logger Management

```python
# Create multiple loggers
auth_logger = create_logger("auth", level="INFO")
db_logger = create_logger("database", level="DEBUG")
api_logger = create_logger("api", level="WARNING")

# Unified configuration management
config = LoggerConfig(level="INFO", log_path="logs")
loggers = config.apply_to("auth", "database", "api")

# Dynamic update for all loggers
config.update(level="DEBUG")  # All loggers update simultaneously
```

## 📖 Documentation

Full documentation available at: [https://joneshong.github.io/pretty-loguru/](https://joneshong.github.io/pretty-loguru/)

- [User Guide](docs/en/guide/index.md)
- [API Reference](docs/en/api/index.md)
- [Examples](examples/README.md)
- [Configuration Guide](docs/en/guide/custom-config.md)

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.