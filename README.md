# Pretty-Loguru 🎨

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen)](https://joneshong.github.io/pretty-loguru/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://github.com/JonesHong/pretty-loguru)

An enhanced Python logging library built on [Loguru](https://github.com/Delgan/loguru), integrating [Rich](https://github.com/Textualize/rich) and ASCII [art](https://github.com/sepandhaghighi/art) to make logging more elegant and intuitive.

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

```python
from pretty_loguru import create_logger

# Create logger - it's this simple!
logger = create_logger("my_app")

# Basic logging
logger.info("Application started")
logger.success("Operation completed successfully")
logger.warning("This is a warning")
logger.error("An error occurred")

# Rich visual blocks
logger.block("System Status", "Everything is running smoothly", border_style="green")

# ASCII art headers
logger.ascii_header("WELCOME", font="slant")

# With file output
logger = create_logger("my_app", log_path="logs", level="INFO")
```

> 📚 **Want more?** Check out our [User Guide](https://joneshong.github.io/pretty-loguru/) for advanced features like configuration templates, multi-logger management, and framework integrations.

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