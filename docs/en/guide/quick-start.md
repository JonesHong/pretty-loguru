# Quick Start

Welcome to pretty-loguru! This page will guide you through experiencing all core features in 5 minutes.

## 🚀 Installation

```bash
pip install pretty-loguru
```

## ⚡ Your First Program

Create a new Python file and copy the following code:

```python
from pretty_loguru import logger, logger_start

# Initialize the logging system
component_name = logger_start(folder="quick_start_logs")
print(f"Logging system initialized, component ID: {component_name}")

# Basic log output
logger.debug("This is a debug message")
logger.info("This is an info message") 
logger.success("This is a success message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

Run the program, and you will see:
- Colorful log output in the console
- A log file generated in the `quick_start_logs/` directory

## 🎨 Experience Rich Blocks

```python
# Rich block log - to display system status
logger.block(
    "System Status Check",
    [
        "CPU Usage: 25%",
        "Memory Usage: 45%", 
        "Disk Space: 89GB available",
        "Network Connection: Normal",
        "Service Status: Running"
    ],
    border_style="green",
    log_level="INFO"
)

# Warning block
logger.block(
    "Important Notes",
    [
        "Memory usage is high",
        "Current growth rate: 3%/minute",
        "Threshold will be reached in 20 minutes",
        "Recommended action: Check for memory leaks"
    ],
    border_style="yellow", 
    log_level="WARNING"
)
```

## 🎯 Experience ASCII Art

```python
# ASCII art header
logger.ascii_header(
    "SYSTEM STARTUP",
    font="slant",
    border_style="blue",
    log_level="INFO"
)

# Try different fonts
fonts = ["standard", "slant", "small", "block"]
for font in fonts:
    logger.ascii_header(
        f"Font: {font.upper()}",
        font=font,
        border_style="cyan"
    )
```

## 🔥 Experience ASCII Blocks

```python
# ASCII block - combining header and content
logger.ascii_block(
    "Startup Report", 
    [
        "Initialization time: 2.3 seconds",
        "Modules loaded: 12",
        "Memory usage: 45MB",
        "Ready: ✓"
    ],
    ascii_header="READY",
    ascii_font="small",
    border_style="green",
    log_level="SUCCESS"
)
```

## 🎮 Complete Example

Save the following code as `quick_demo.py`:

```python
import time
import random
from pretty_loguru import logger, logger_start

def main():
    # Initialization
    component_name = logger_start(folder="demo_logs")
    
    # Application startup
    logger.ascii_header("APP STARTUP", font="slant", border_style="blue")
    
    logger.info("Loading configuration...")
    time.sleep(0.5)
    logger.success("Configuration loaded successfully")
    
    # System status
    logger.block(
        "System Initialization Status",
        [
            "Application Name: Quick Demo App",
            "Version: 1.0.0", 
            "Environment: Development",
            "Log Level: DEBUG"
        ],
        border_style="cyan"
    )
    
    # Simulate workflow
    logger.info("Starting to process tasks...")
    for i in range(3):
        logger.info(f"Processing task #{i+1}")
        time.sleep(0.8)
        
        if random.random() > 0.7:  # 30% chance of warning
            logger.warning(f"Task #{i+1} is processing slowly")
        else:
            logger.success(f"Task #{i+1} completed")
    
    # Completion report
    logger.ascii_block(
        "Execution Summary",
        [
            "Total tasks: 3",
            "Successfully completed: 3", 
            "Execution time: 3.2 seconds",
            "Status: Normal"
        ],
        ascii_header="COMPLETE",
        ascii_font="block", 
        border_style="green"
    )

if __name__ == "__main__":
    main()
```

## 📁 Check the Output

After running the program, check the generated files:

```bash
# View the generated log directory
ls -la demo_logs/

# View the log content
cat demo_logs/[your_component_name]_*.log
```

You will find:
- Rich, colorful output in the console
- Complete log records saved in the file
- ASCII art saved as plain text in the file

## 🎯 Key Takeaways

Through this quick start, you have experienced:

✅ **Basic Logging Functions** - 6 log levels  
✅ **Rich Blocks** - Structured visual logs  
✅ **ASCII Headers** - Eye-catching titles  
✅ **ASCII Blocks** - Combined functionality  
✅ **Automatic File Management** - Log rotation and saving  

## 🚀 Next Steps

Now that you have experienced the core features, you can:

- [Dive into Basic Usage](./basic-usage) - Detailed configuration options
- [Explore All Features](../features/) - Full functionality of Rich and ASCII
- [View More Examples](../examples/) - From basic to advanced
- [Integrate into Web Applications](../integrations/) - FastAPI and Uvicorn

Ready to dive deeper? 🎮
