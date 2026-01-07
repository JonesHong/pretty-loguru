# Pretty-Loguru 🎨

<p align="center">
  <img src="https://raw.githubusercontent.com/JonesHong/pretty-loguru/refs/heads/master/docs/public/logo.png" alt="pretty-loguru icon" width="200"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/pretty-loguru.svg">
  </a>
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pretty-loguru.svg">
  </a>
  <a href="https://joneshong.github.io/pretty-loguru/">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-ghpages-blue.svg">
  </a>
  <a href="https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/JonesHong/pretty-loguru.svg">
  </a>
  <a href="https://deepwiki.com/JonesHong/pretty-loguru">
    <img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki">
  </a>
</p>

A pretty Python logging library built on [Loguru](https://github.com/Delgan/loguru), integrating [Rich](https://github.com/Textualize/rich) and ASCII [art](https://github.com/sepandhaghighi/art) to make logging more elegant and intuitive.

---

## ✨ Features

- 🎨 **Rich Block Logging** - Display structured logs using Rich panels
- 🎯 **ASCII Art Headers** - Generate eye-catching ASCII art titles
- 🔥 **One-Click Setup** - Simple configuration for both file and console logging
- 🚀 **FastAPI Integration** - Perfect integration with FastAPI and Uvicorn
- 📊 **Preset Configurations** - Best practices for development, production, and testing
- 🛠️ **Highly Customizable** - Support for custom formats, colors, and rotation strategies

## 📦 Installation

```bash
# Recommended (uv)
uv add pretty-loguru

# Alternative (pip)
pip install pretty-loguru
```

Optional extras:

```bash
# FIGlet support (optional)
uv add "pretty-loguru[figlet]"

# Integrations alias (FastAPI/Uvicorn)
uv add "pretty-loguru[integrations]"
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
logger = create_logger("my_app", log_dir="logs", level="INFO")
```

## ✅ Semantic Consistency (console ↔ file)

pretty-loguru follows a simple contract:

- **One call → one Loguru event** (no `console.print(...)` side-channel inside a logging API).
- Console/file are just **different renderers** of the same event.
- Pretty methods (e.g. `block/table/tree/...`) attach `pretty_kind` + `pretty_payload` + `pretty_text` into `record["extra"]`.

Recommended for observability pipelines:

- Enable JSON file logs via `serialize=True`, then ship via Filebeat/Fluent Bit (ELK) or Promtail/Grafana Agent (Loki).
- Use `loki_enabled=True` direct push only for simple setups (best-effort: no retries / no offline buffer / no backpressure).

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
