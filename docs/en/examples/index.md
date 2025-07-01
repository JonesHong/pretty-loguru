# Example Collection

Welcome to the pretty-loguru example collection! This provides a complete learning path from basic to advanced to help you quickly master all the features.

## 🎯 Learning Path

### 🚀 Must-See for Beginners (5-10 minutes)
Start here to understand the core concepts:

1. **[Basic Usage](./basics/)** - Log initialization, basic output, file management
2. **[Visualization Features](./visual/)** - Basic usage of Rich blocks and ASCII art

### 🎨 Exploring Features (15-20 minutes)
Dive deep into the detailed usage of each feature:

3. **[Preset Configurations](./presets/)** - Advanced features like log rotation, cleanup, and compression
4. **[Web Application Integration](./fastapi/)** - Complete integration with FastAPI and Uvicorn

### 🚀 Production Practices (20-30 minutes)
Learn the best practices in real projects:

5. **[Production Environment](./production/)** - Enterprise-level features like deployment, monitoring, and error tracking

## 📚 Example Categories

### 🔰 Basic Examples
<div class="vp-card-container">

**[Simple Usage](./basics/simple-usage)**  
The most basic logger initialization and usage methods

**[Console vs. File](./basics/console-vs-file)**  
Understand the differences between different output targets

**[Target-Oriented Logging](./basics/target-logging)**  
Use `console_*` and `file_*` methods to control output

</div>

### 🎨 Visualization Examples
<div class="vp-card-container">

**[Rich Blocks](./visual/blocks)**  
Structured and beautiful log blocks

**[ASCII Art](./visual/ascii-art)**  
Eye-catching text art titles

**[Rich Components](./visual/rich-components)**  
A complete showcase of Rich features

</div>

### ⚙️ Preset Configuration Examples
<div class="vp-card-container">

**[Log Rotation](./presets/rotation-examples)**  
Automatically rotate log files by time or size

**[Preset Comparison](./presets/preset-comparison)**  
Best practice configurations for different environments

**[Custom Presets](./presets/custom-presets)**  
Create your own preset configurations

</div>

### 🌐 Web Application Examples
<div class="vp-card-container">

**[Simple API](./fastapi/simple-api)**  
Basic FastAPI integration

**[Middleware](./fastapi/middleware-demo)**  
Using pretty-loguru in middleware

**[Dependency Injection](./fastapi/dependency-injection)**  
FastAPI dependency injection pattern

</div>

### 🏭 Production Environment Examples
<div class="vp-card-container">

**[Deployment Logging](./production/deployment-logging)**  
Complete logging for the deployment process

**[Performance Monitoring](./production/performance-monitoring)**  
Continuous monitoring of system performance

**[Error Tracking](./production/error-tracking)**  
Complete error handling and tracking

</div>

## 🎮 Interactive Experience

### Quick Experience
Want to see the effect immediately? Copy the following code into your Python environment:

```python
# Install: pip install pretty-loguru
from pretty_loguru import create_logger

# One-line initialization
component_name = logger = create_logger(
    name="examples_demo",
    log_path="demo",
    level="INFO"
)

# Basic logs
logger.info("Welcome to pretty-loguru!")
logger.success("Installation successful!")

# Rich block
logger.block(
    "Quick Experience",
    [
        "✅ Installation complete",
        "✅ Initialization successful", 
        "🎯 Ready to explore more features"
    ],
    border_style="green"
)

# ASCII header
logger.ascii_header("WELCOME", font="slant")
```

### Complete Demo Program
We have prepared a complete demo program to showcase all major features:

```python
# demo_complete.py
import time
import random
from pretty_loguru import create_logger

def complete_demo():
    """Complete feature demonstration"""
    # Initialization
    logger = create_logger(
    name="examples_demo",
    log_path="complete_demo",
    level="INFO"
)
    
    # Startup sequence
    logger.ascii_header("DEMO START", font="slant", border_style="blue")
    
    # System check
    logger.block(
        "System Check",
        [
            "🖥️  Operating System: Checking...",
            "🐍 Python Environment: Checking...",
            "📦 Dependencies: Checking..."
        ],
        border_style="yellow"
    )
    
    time.sleep(1)
    
    # Check results
    logger.block(
        "Check Results", 
        [
            "✅ Operating System: Linux/Windows/Mac",
            "✅ Python Environment: 3.8+",
            "✅ Dependencies: Installed"
        ],
        border_style="green"
    )
    
    # Feature showcase
    features = [
        ("Rich Blocks", "Structured logs"),
        ("ASCII Headers", "Artistic text titles"),
        ("File Rotation", "Automatic management"),
        ("Multiple Outputs", "Console + File")
    ]
    
    for i, (feature, desc) in enumerate(features):
        logger.info(f"Showcasing feature {i+1}: {feature}")
        logger.success(f"{desc} - Complete!")
        time.sleep(0.5)
    
    # Completion report
    logger.ascii_block(
        "Demo Summary",
        [
            f"📊 Features showcased: {len(features)}",
            "⏱️  Execution time: 3.2 seconds",
            "✨ Status: Running perfectly",
            "🎯 Next step: Check the full documentation"
        ],
        ascii_header="COMPLETE",
        ascii_font="block",
        border_style="green"
    )

if __name__ == "__main__":
    complete_demo()
```

## 📖 How to Use These Examples

### 1. Learn Sequentially
Follow the learning path in order. Each example builds on the previous one.

### 2. Practice Hands-On
Each example provides complete, executable code. It is recommended to run it and see the output.

### 3. Modify and Experiment
After understanding the basic usage, try modifying the example code to explore different parameters and effects.

### 4. Check the Output
Pay special attention to:
- **Console Output** - Colorful, formatted real-time display
- **File Output** - Complete log records, suitable for subsequent analysis

## 💡 Learning Suggestions

### For Beginners
- Start with [Basic Usage](./basics/)
- Focus on the usage of `logger_start()`
- Understand the difference between console and file output

### For Experienced Developers
- Jump directly to [Visualization Features](./visual/)
- Check out [Web Application Integration](./fastapi/)
- Study the best practices in the [Production Environment](./production/)

### For System Administrators
- Focus on [Preset Configurations](./presets/)
- Learn about [Log Rotation and Management](./presets/rotation-examples)
- Study [Deployment and Monitoring](./production/)

## 🚀 Start Exploring

Choose a starting point that suits your level and begin your pretty-loguru learning journey:

- 🔰 **Beginner**: [Basic Usage →](./basics/)
- 🎨 **Explorer**: [Visualization Features →](./visual/)  
- 🚀 **Practitioner**: [Production Environment →](./production/)

Each example includes detailed explanations, complete code, and expected output. Let's get started! 🎯
