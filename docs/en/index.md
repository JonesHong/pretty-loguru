---
layout: home

hero:
  name: "pretty-loguru"
  text: "Enhanced Python Logging Library"
  tagline: "Based on Loguru, integrated with Rich and ASCII Art for more elegant log outputs."
  image:
    src: /logo.png
    alt: pretty-loguru
  actions:
    - theme: brand
      text: Get Started
      link: /en/guide/quick-start
    - theme: alt
      text: View Examples
      link: /en/examples/
    - theme: alt
      text: GitHub
      link: https://github.com/JonesHong/pretty-loguru

features:
  - icon: 🎨
    title: Rich Block Logging
    details: Display structured log blocks with borders and styles using Rich panels, making system status clear at a glance.
  - icon: 🎯
    title: ASCII Art Headers
    details: Generate eye-catching ASCII art titles using the art library and pyfiglet to enhance the visual appeal of your logs.
  - icon: 🔥
    title: One-Click Initialization
    details: Set up both file and console logging with a single call, including support for automatic rotation and compression.
  - icon: 🚀
    title: FastAPI Integration
    details: Seamlessly integrate with FastAPI and Uvicorn to unify logging formats and outputs for your web applications.
  - icon: 📊
    title: Default Configurations
    details: Provides multiple preset configurations, including best practice settings for development, production, and testing environments.
  - icon: 🛠️
    title: Highly Customizable
    details: Supports custom formats, colors, and rotation strategies to meet the logging needs of different scenarios.

---

## 🚀 Quick Installation

```bash
pip install pretty-loguru
```

## ⚡ Quick Start

```python
from pretty_loguru import create_logger

# Initialize the logging system with one line of code
logger  = create_logger(
    name="en_demo",
    log_path="my_logs",
    level="INFO"
)

# Start using various logging features
logger.info("Application started successfully")
logger.success("Database connection is normal")
logger.warning("Memory usage is high")

# Rich Block Log
logger.block(
    "System Status Summary",
    [
        "CPU Usage: 45%",
        "Memory Usage: 60%", 
        "Disk Space: 120GB available",
        "Network Connection: Normal"
    ],
    border_style="green",
    log_level="INFO"
)

# ASCII Art Header
logger.ascii_header(
    "SYSTEM READY",
    font="slant",
    border_style="blue"
)
```

## 📸 Showcase

### Basic Log Output
![Basic Example Terminal](/example_1_en_terminal.png)

### Rich Block Log
![Rich Block Example](/example_2_en_terminal.png)

### ASCII Art Header
![ASCII Art Example](/example_3_en_terminal.png)

## 🎯 Why choose pretty-loguru?

- **🎨 Visualization-First**: Rich visual elements make logs no longer monotonous.
- **⚡ Out-of-the-Box**: Minimalist API design, get started with just a few lines of code.
- **🔧 Highly Flexible**: Supports multiple output formats and custom configurations.
- **🌐 Framework Integration**: Perfect support for mainstream frameworks like FastAPI and Uvicorn.
- **📦 Production-Ready**: Built-in enterprise-level features like log rotation, compression, and cleanup.

## 🧭 **Where Should I Start?**

### 📊 Choose Based on Your Role

| I am... | Recommended Path | Estimated Time |
|---------|----------|----------|
| 🆕 **Python Logging Beginner** | [5-min Experience](/en/examples/) → [Core Features](/en/examples/) → [Visualization](/en/examples/) | 30 minutes |
| 🌐 **Web Developer** | [Quick Start](/en/guide/quick-start) → [Core Features](/en/examples/) → [Framework Integration](/en/integrations/) | 45 minutes |
| 🏭 **DevOps/Operations** | [Installation](/en/guide/installation) → [Production Guide](/en/examples/) → [Advanced Config](/en/examples/) | 1 hour |
| 🔬 **Advanced Developer** | [API Docs](/en/api/) → [Complete Examples](/en/examples/) → [Custom Development](/en/examples/) | 2-3 hours |

### 🎯 Choose Based on Your Needs

<div class="vp-doc">

| I want to... | Jump directly to |
|-----------|----------|
| ⚡ **5-minute Quick Experience** | [Quick Experience](/en/examples/) |
| 🎨 **Beautiful Log Output** | [Visualization Features](/en/examples/) |
| 🚀 **FastAPI Integration** | [Framework Integration](/en/integrations/) |
| 🏭 **Production Deployment** | [Production Guide](/en/examples/) |
| 📚 **Complete Learning** | [Learning Center](/en/examples/) |

</div>

## 🚀 Learning Paths

<div class="vp-doc">

- [🚀 5-minute Quick Experience](/en/examples/) - Immediately feel the charm of pretty-loguru
- [📚 Master Core Features](/en/examples/) - Master all basic functionality  
- [🎨 Visualization Features](/en/examples/) - Rich blocks and ASCII art
- [⚙️ Configuration & Management](/en/examples/) - File rotation and advanced configuration
- [🌐 Framework Integration](/en/integrations/) - FastAPI, Uvicorn integration
- [🏭 Production Environment](/en/examples/) - Enterprise deployment and operations
- [📚 API Reference](/en/api/) - Complete function documentation

</div>

## 📄 License

This project is licensed under the [MIT License](https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE).
