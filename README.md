# Pretty Loguru

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
  <a href="https://deepwiki.com/JonesHong/pretty-loguru"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

## 🎯 Why Choose Pretty Loguru?

**Pretty Loguru** is a beautiful and easy-to-use Python logging library that adds visual enhancements and production-ready features on top of [Loguru](https://github.com/Delgan/loguru):

### 🆚 Core Differences from Original Loguru

| Feature | Loguru | Pretty Loguru |
|---|---|---|
| **Visual Effects** | Plain text output | ✨ ASCII Art, Color Blocks, Rich Components |
| **Framework Integration** | Manual configuration | 🚀 One-line integration for FastAPI + Uvicorn |
| **Production Readiness** | Basic features | 📊 Monitoring, Compression, Error Tracking |
| **Configuration Management** | Code-based configuration | ⚙️ Factory Pattern, Preset System |
| **Learning Curve** | Requires learning | 📚 5-minute quick start, complete examples |

---

## ⚡ 5-Minute Quick Start

### Installation

```bash
pip install pretty-loguru
```

### Simplest Usage

```python
from pretty_loguru import create_logger

# Create logger and start using
logger = create_logger("my_app", log_path="./logs")

logger.info("This is an info message")
logger.success("This is a success message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```

### Native Format Support (v2.1.0+)

```python
# Suitable for migrating from loguru or for development debugging
logger = create_logger("my_app", use_native_format=True)
logger.info("Close to loguru native format")
# Output: main.py:function:42 - Close to loguru native format
```

### One-Line FastAPI Integration

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

app = FastAPI()
logger = create_logger("api", log_path="./logs")

# One-line integration of all logging features (including uvicorn)
integrate_fastapi(app, logger)

@app.get("/")
async def root():
    logger.info("API request processed")
    return {"message": "Hello World"}
```

---

## 🎨 Visual Features Showcase

### ASCII Art Header

```python
logger.ascii_header("WELCOME", style="block")
```

Output effect:
```
╭──────────────────────────────────────────────╮
│  _       __    ______    __    ______   ___  │
│ | |     / /   / ____/   / /   / ____/  / _ \ │
│ | | /| / /   / __/     / /   / /      / / / │
│ | |/ |/ /   / /___    / /___/ /___   / /_/ / │
│ |__/|__/   /_____/   /_____/\\____/   \\____/  │
╰──────────────────────────────────────────────╯
```

### Colored Information Block

```python
logger.block(
    "System Status Check",
    "✅ Database connection normal\n✅ API service running\n⚠️  Memory usage 85%",
    border_style="green"
)
```

### Rich Component Integration

```python
# Table display
logger.table(
    ["User", "Status", "Login Time"],
    [
        ["Alice", "Online", "10:30"],
        ["Bob", "Offline", "09:15"]
    ]
)

# Progress tracking
for item in logger.progress.track_list(items, description="Processing..."):
    process(item)
```

---

## 🏭 Production Environment Ready

### Automatic Rotation and Compression

```python
# Rotate by size (10MB) + ZIP compression
logger = create_logger(
    "production_app",
    log_path="./logs",
    rotation="10 MB",
    retention="30 days",
    compression="zip"
)
```

### Environment Adaptive Configuration

```python
import os

# Automatically adjust based on environment
env = os.getenv("APP_ENV", "development")
if env == "production":
    logger = create_logger("app", level="WARNING", rotation="daily")
else:
    logger = create_logger("app", level="DEBUG")
```

### Error Tracking and Retry Mechanism

```python
@retry_with_logging(max_attempts=3, logger=logger)
def database_operation():
    # Automatically log retry process
    return db.query("SELECT * FROM users")

# Structured error logging
logger.error("Database connection failed", extra={
    "error_type": "ConnectionError",
    "host": "db.example.com",
    "retry_count": 2
})
```

---

## 📚 Complete Learning Path

### 🟢 Beginner Level (5 minutes)
- [Basic Usage](examples_new/01_basics/simple_usage.py) - Create logger and basic output
- [Console vs File](examples_new/01_basics/console_vs_file.py) - Separate output targets
- [Targeted Logging](examples_new/01_basics/target_logging.py) - console_info, file_error, etc.

### 🟡 Intermediate Level (15 minutes)
- [ASCII Art](examples_new/02_visual/ascii_art.py) - Beautify titles and status
- [Color Blocks](examples_new/02_visual/blocks.py) - Structured information display
- [Rich Components](examples_new/02_visual/rich_components.py) - Tables, trees, progress bars

### 🟠 Professional Level (30 minutes)
- [Preset Configuration](examples_new/03_presets/preset_comparison.py) - Quickly configure for different scenarios
- [Rotation Strategy](examples_new/03_presets/rotation_examples.py) - File management best practices
- [Custom Presets](examples_new/03_presets/custom_presets.py) - Customized configuration

### 🔴 Expert Level (60 minutes)
- [FastAPI Integration](examples_new/04_fastapi/simple_api.py) - Web application logging
- [Middleware Application](examples_new/04_fastapi/middleware_demo.py) - Request tracking
- [Production Deployment](examples_new/05_production/deployment_logging.py) - Enterprise-grade configuration
- [Error Monitoring](examples_new/05_production/error_tracking.py) - Exception handling and analysis
- [Performance Monitoring](examples_new/05_production/performance_monitoring.py) - System health check

---

## 🔧 Core API Reference

### Basic Usage

```python
from pretty_loguru import create_logger

# Basic creation
logger = create_logger("app_name")

# Full configuration
logger = create_logger(
    name="my_service",
    log_path="./logs",
    level="INFO",
    rotation="1 day",
    retention="1 month",
    compression="zip"
)

# Native format (v2.1.0+)
logger = create_logger(
    name="my_app",
    use_native_format=True,  # Use format close to loguru native
    log_path="./logs"
)
```

### Framework Integration

```python
# FastAPI Integration
from pretty_loguru.integrations.fastapi import integrate_fastapi
integrate_fastapi(app, logger)

# Uvicorn Integration
from pretty_loguru.integrations.uvicorn import integrate_uvicorn
integrate_uvicorn(logger)
```

### Visual Components

```python
# ASCII Header
logger.ascii_header("TITLE", style="block")

# Custom Block
logger.block("Title", "Content", border_style="blue")

# Rich Components
logger.table(headers, rows)
logger.tree("Root", {"child1": "value1"})
```

---

## 🎯 Core Advantages Summary

1. **🎨 Visual First**: More beautiful output than Loguru, ASCII art gives logs visual impact
2. **🚀 Plug and Play**: FastAPI one-line integration, saves 80% time compared to manual configuration
3. **🏭 Production Ready**: Enterprise-grade features (rotation, compression, monitoring) out-of-the-box
4. **⚙️ Simplified Configuration**: Factory pattern and preset system, say goodbye to complex manual configuration
5. **📚 Learning Friendly**: 5-minute quick start, complete examples cover all usage scenarios

---

## 📖 Advanced Resources

- [📘 Full Documentation](https://joneshong.github.io/pretty-loguru/en/index.html)
- [🎯 Example Collection](examples_new/) - Complete learning path from beginner to expert
- [⚙️ API Reference](https://joneshong.github.io/pretty-loguru/en/api/index.html)
- [🐛 Report Issues](https://github.com/JonesHong/pretty-loguru/issues)
- [💡 Feature Suggestions](https://github.com/JonesHong/pretty-loguru/discussions)

---

## 🤝 Contribution

Contributions are welcome! Please see the [Contribution Guide](CONTRIBUTING.md) for how to participate in project development.

## 📜 License

This project is licensed under the [MIT License](LICENSE).