# Visualization Feature Examples

The visualization features of pretty-loguru are its main characteristic. This chapter will demonstrate the practical application and effects of all visualization features.

## 📖 Contents of this Chapter

- **[Rich Block Examples](./blocks)** - Structured and beautiful log blocks  
- **[ASCII Art Examples](./ascii-art)** - Eye-catching text art titles
- **[Rich Component Examples](./rich-components)** - A complete showcase of Rich features
- **[Combined Effects Examples](./combined-effects)** - Using multiple features in combination

## 🎨 Visualization Features Overview

### Rich Blocks - Structured Logging

Rich blocks provide a structured content display with borders:

```python
from pretty_loguru import create_logger

logger.block(
    "System Status Check",
    [
        "CPU Usage: 25%",
        "Memory Usage: 60%",
        "Disk Space: 120GB Available",
        "Network Connection: Normal"
    ],
    border_style="green",
    log_level="INFO"
)
```

### ASCII Art - Eye-Catching Titles

Create visually stunning titles with various fonts:

```python
logger.ascii_header("SYSTEM READY", font="slant", border_style="blue")
logger.ascii_header("WARNING", font="doom", border_style="yellow")
logger.ascii_header("ERROR", font="block", border_style="red")
```

### ASCII Blocks - Complete Report Format

Combine the power of ASCII headers and Rich blocks:

```python
logger.ascii_block(
    "Deployment Complete Report",
    [
        "Version: v2.1.0",
        "Deployment Time: 3m 45s", 
        "Service Checks: All passed",
        "Load Balancer: Enabled"
    ],
    ascii_header="DEPLOYED",
    ascii_font="block",
    border_style="green"
)
```

## 🎯 Learning Path

### 🚀 Quick Experience (5 minutes)
For developers who want to quickly understand the visual effects:

1. **[Rich Block Basics](./blocks#basic-usage)** - Understand the basic block format
2. **[ASCII Header Experience](./ascii-art#basic-usage)** - Create your first ASCII header

### 🎨 In-Depth Exploration (15 minutes)  
For developers who want to master all visual features:

3. **[Border Styles and Colors](./blocks#border-styles)** - Master various visual effects
4. **[Complete ASCII Font List](./ascii-art#font-styles)** - Learn about all available fonts
5. **[Rich Component Integration](./rich-components)** - Advanced features like tables and trees

### 🚀 Practical Application (20 minutes)
For developers who want to apply these in real projects:

6. **[ASCII Block Applications](./ascii-blocks)** - Complete report formatting
7. **[Combined Effects Design](./combined-effects)** - Create professional-grade visual outputs
8. **[Real-World Scenarios](./real-world-scenarios)** - Use cases in real projects

## 🎮 Interactive Example

### Complete Visualization Showcase

Here is a comprehensive example showcasing all visual features:

```python
import time
from pretty_loguru import create_logger

def visual_showcase():
    """Complete showcase of visualization features"""
    
    # Initialize the logging system
    logger = create_logger(
    name="visual_demo",
    log_path="visual_demo",
    level="INFO"
)
    
    # 1. Startup title
    logger.ascii_header("VISUAL DEMO", font="slant", border_style="blue")
    
    # 2. Basic log level display
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.success("This is a success message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    time.sleep(1)
    
    # 3. Rich block display
    logger.block(
        "System Resource Monitoring",
        [
            "🖥️  CPU Usage: 23%",
            "💾 Memory Usage: 1.2GB / 8GB",
            "💿 Disk Space: 156GB Available",
            "🌐 Network Status: Connected",
            "⚡ Service Status: All Running"
        ],
        border_style="green"
    )
    
    time.sleep(1)
    
    # 4. Blocks with different colors
    logger.block(
        "Important Notes",
        [
            "⚠️  Memory usage is high",
            "⚠️  Recommend monitoring system load",
            "💡 Consider scaling hardware resources"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    time.sleep(1)
    
    # 5. ASCII art block
    logger.ascii_block(
        "Demo Completion Summary",
        [
            "✅ Basic logs: Displayed",
            "✅ Rich blocks: Displayed", 
            "✅ ASCII headers: Displayed",
            "✅ ASCII blocks: Displayed",
            "🎉 Status: Demo complete"
        ],
        ascii_header="COMPLETE",
        ascii_font="block",
        border_style="green",
        log_level="SUCCESS"
    )
    
    # 6. End title
    logger.ascii_header("DEMO END", font="standard", border_style="magenta")

if __name__ == "__main__":
    visual_showcase()
```

## 💡 Best Practice Suggestions

### 1. Use Visual Effects Moderately
```python
# Recommended - Use visualization for important events
logger.ascii_header("APP START", font="slant")  # Application startup
logger.block("Configuration Info", config_items) # Important information

# Not recommended - Overuse of visual effects
logger.ascii_header("DEBUG", font="doom")       # General debug message
```

### 2. Maintain a Consistent Style
```python
# Create a style guide
SUCCESS_STYLE = {"border_style": "green", "ascii_font": "slant"}
WARNING_STYLE = {"border_style": "yellow", "ascii_font": "standard"}
ERROR_STYLE = {"border_style": "red", "ascii_font": "doom"}
```

### 3. Consider the Output Environment
```python
import os

def adaptive_logging(message):
    """Adjust log style based on the environment"""
    if os.getenv("ENVIRONMENT") == "production":
        # Use a concise style in production
        logger.info(message)
    else:
        # Use a rich style in development
        logger.block("Development Message", [message], border_style="blue")
```

## 🚀 Next Steps

Choose an interesting example to start learning more:

- **Beginner**: Start with [Rich Block Examples](./blocks)
- **Advanced**: Go directly to [ASCII Block Examples](./ascii-blocks)
- **Expert**: Explore [Combined Effects Examples](./combined-effects)

Make your log output more professional and attractive!
