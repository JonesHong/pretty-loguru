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
from pretty_loguru import logger, logger_start

# Initialize the logging system with one line of code
component_name = logger_start(folder="my_logs")

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

## 🚀 Next Steps

<div class="vp-doc">

- [📖 Read the Full Guide](/en/guide/) - Learn about all features and configuration options.
- [🎮 View Examples](/en/examples/) - Complete examples from basic to advanced.
- [🔌 Integration Guide](/en/integrations/) - Integrate with frameworks like FastAPI and Uvicorn.
- [📚 API Documentation](/en/api/) - Detailed API reference documentation.

</div>

## 📄 License

This project is licensed under the [MIT License](https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE).
