# Features

The core advantage of pretty-loguru lies in its rich visualization features. This section will detail each feature, allowing you to fully leverage the potential of this logging library.

## 🎨 Visualization Features Overview

### Rich Block Logs
Create structured, bordered log blocks using the powerful panel feature from the Rich library.

- ✨ Multiple border styles and colors
- 📋 Clear information hierarchy  
- 🎯 Ideal for status reports and summaries

[Learn about Rich Blocks →](./rich-blocks)

### ASCII Art Headers
Generate eye-catching text art titles using the art and pyfiglet libraries.

- 🎯 Multiple font choices
- 🌈 Support for colored borders
- 🚀 Highlight important events

[Learn about ASCII Headers →](./ascii-art)

### ASCII Art Blocks
Combine the power of ASCII art headers and Rich blocks.

- 🔥 Optimal visual effects
- 📊 Complete report formatting
- 🎨 Highly customizable

[Learn about ASCII Blocks →](./ascii-blocks)

### Code Highlighting
Display syntax-highlighted code snippets with Rich integration.

- 💻 Multi-language syntax highlighting
- 🎨 Multiple color themes
- 📁 Direct file content display
- 🔀 Side-by-side code comparison
- 📏 Line range selection

[Learn about Code Highlighting →](./code-highlighting)

## 🚀 Quick Preview

### Rich Block Example

```python
logger.block(
    "System Monitoring Report",
    [
        "🖥️  CPU Usage: 23%",
        "💾  Memory Usage: 1.2GB / 8GB",
        "💿  Disk Space: 156GB Available",
        "🌐  Network Status: Connected",
        "⚡  Service Status: All Running"
    ],
    border_style="green",
    level="INFO"
)
```

### ASCII Header Example

```python
logger.ascii_header(
    "SYSTEM READY",
    font="slant",
    border_style="blue"
)
```

### ASCII Block Example

```python
logger.ascii_block(
    "Deployment Complete Report",
    [
        "⏱️  Deployment Time: 2m 30s",
        "✅  Service Check: Passed",
        "🔄  Health Check: Normal", 
        "📡  Load Balancer: Enabled"
    ],
    header_text="DEPLOYED",
    font="block",
    border_style="green"
)
```

### Code Highlighting Example

```python
# Display Python code with syntax highlighting
code = '''
def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

logger.code(code, language="python", title="Fibonacci Function")

# Compare code versions
logger.diff(
    old_code="def old_func(): pass",
    new_code="def new_func(): return True",
    old_title="Before",
    new_title="After"
)
```

## 🎯 Use Cases

### 🖥️ System Monitoring
Use Rich blocks to display system status, performance metrics, and resource usage.

### 🚀 Application Startup
Use ASCII headers to mark important application lifecycle events.

### 📊 Report Generation
Use ASCII blocks to create complete status reports and summaries.

### ⚠️ Error Tracking
Use different border colors and styles to distinguish the severity of errors.

### 🔄 Workflows
Use visual logs to mark progress in long-running tasks.

### 💻 Code Documentation
Use code highlighting to display code snippets, file contents, and code comparisons in logs.

## 🎮 Interactive Learning

Want to try it out now?

1. **[Install pretty-loguru](../guide/installation)**
2. **[Follow the Quick Start](../guide/quick-start)** 
3. **[View Complete Examples](../examples/visual/)**

## 🔧 Advanced Features

### Target-Oriented Logging
pretty-loguru also provides target-oriented logging methods:

```python
from pretty_loguru.addons import log_to_targets

# Output only to the console
log_to_targets(logger, "This will only be displayed in the console", level="INFO", console_only=True)

# Write only to a file
log_to_targets(logger, "This will only be written to the log file", level="DEBUG", file_only=True)

# Simultaneous output (default behavior)
logger.info("This will be displayed in both the console and the file")
```

### Custom Styles
All visual features support customization:

- **Border Styles**: `"solid"`, `"double"`, `"rounded"`, `"thick"`, etc.
- **Color Themes**: `"red"`, `"green"`, `"blue"`, `"yellow"`, `"magenta"`, `"cyan"`, etc.
- **Font Choices**: Dozens of ASCII art fonts
- **Log Levels**: Freely control the importance of the output

Ready to dive deep into each feature? Choose one to start your journey! 🎯
