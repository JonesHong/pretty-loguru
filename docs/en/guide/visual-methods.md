# Visual Methods Guide

Pretty-Loguru provides various visual methods to beautify your log output. This guide will help you choose the most suitable method.

## 📊 Method Overview

| Method | Purpose | Complexity | Use Case |
|--------|---------|------------|----------|
| `logger.block()` | Simple text blocks | ⭐ | Basic messages, lists |
| `logger.panel()` | Advanced panel display | ⭐⭐⭐ | Complex content, Rich objects |
| `logger.ascii_header()` | ASCII art titles | ⭐ | Startup screens, section dividers |
| `logger.table()` | Table data | ⭐⭐ | Structured data |
| `logger.tree()` | Tree structure | ⭐⭐ | Hierarchical relationships |
| `logger.code()` | Code highlighting | ⭐ | Display code |

## 🎯 Block vs Panel Detailed Comparison

### When to Use `block()`

`block()` is the simplest block display method, perfect for quickly showing text lists.

**Advantages:**
- ✅ Simple and easy to use
- ✅ Few parameters, low learning curve
- ✅ Suitable for plain text content
- ✅ Better performance

**Limitations:**
- ❌ Can only display string lists
- ❌ No subtitle support
- ❌ Title can only be left-aligned
- ❌ Cannot control size and padding

**Usage Examples:**
```python
# Suitable scenarios
logger.block("System Info", [
    "CPU: Intel i7",
    "RAM: 16GB",
    "Disk: 512GB SSD"
])

# Status report
logger.block("Deployment Check", [
    "✓ Code updated",
    "✓ Database migrated",
    "✓ Service restarted",
    "✓ Health check passed"
], border_style="green")
```

### When to Use `panel()`

`panel()` is a full-featured panel display method that supports all Rich Panel features.

**Advantages:**
- ✅ Supports any Rich renderable object
- ✅ Customizable title and subtitle
- ✅ Flexible alignment options
- ✅ Precise size and padding control
- ✅ Supports complex visual effects

**Use Cases:**
- ❌ Requires learning more parameters
- ❌ Overkill for simple text

**Usage Examples:**
```python
# Display Rich objects
from rich.table import Table

table = Table(title="Performance Metrics")
table.add_column("Metric")
table.add_column("Value")
table.add_row("QPS", "10,000")
table.add_row("Latency", "15ms")

logger.panel(
    table,
    title="System Performance",
    subtitle="5-minute average",
    border_style="cyan",
    box_style="double"
)

# Complex layout
from rich.text import Text

content = Text()
content.append("Status: ", style="bold")
content.append("Running\n", style="green")
content.append("Version: ", style="bold")
content.append("v2.0.0", style="blue")

logger.panel(
    content,
    title="Application",
    padding=(2, 4),
    width=60
)
```

## 🔄 Selection Guide

### 1. Simple Text Messages
```python
# ✅ Use block
logger.block("Error Summary", [
    "File not found",
    "Permission denied",
    "Network timeout"
])

# ❌ Don't need panel
logger.panel("\n".join([...]))  # Over-engineered
```

### 2. Need Subtitle
```python
# ❌ block doesn't support subtitle
# logger.block("Title", [...], subtitle="Subtitle")  # Doesn't exist

# ✅ Use panel
logger.panel(
    "Content",
    title="Main Title",
    subtitle="Last updated: 15:30"
)
```

### 3. Display Rich Objects
```python
# ❌ block cannot display Rich objects
# logger.block("Table", table)  # Error

# ✅ Use panel
logger.panel(table, title="Data Table")
```

### 4. Need Precise Control
```python
# ✅ panel provides complete control
logger.panel(
    content,
    title="Report",
    title_align="center",
    width=80,
    padding=(1, 3),
    box_style="heavy"
)
```

## 🎨 Border Style Guide

### Color Semantics
Use consistent colors to convey message types:

```python
# Success - Green
logger.block("✅ Operation Successful", [...], border_style="green")
logger.panel(success_msg, border_style="green")

# Error - Red
logger.block("❌ Error", [...], border_style="red")
logger.panel(error_msg, border_style="red")

# Warning - Yellow
logger.block("⚠️ Warning", [...], border_style="yellow")
logger.panel(warning_msg, border_style="yellow")

# Info - Blue
logger.block("ℹ️ Info", [...], border_style="blue")
logger.panel(info_msg, border_style="blue")
```

### Box Style Selection
Different box styles convey different importance levels:

```python
# General messages - Rounded (default)
logger.panel(msg, box_style="rounded")

# Important messages - Double lines
logger.panel(important_msg, box_style="double")

# Critical messages - Heavy lines
logger.panel(critical_msg, box_style="heavy")

# Technical content - ASCII
logger.panel(technical_msg, box_style="ascii")
```

## 📋 Other Visual Methods

### Table - `logger.table()`
Suitable for displaying structured data:
```python
data = [
    {"Name": "Service A", "Status": "Running", "CPU": "25%"},
    {"Name": "Service B", "Status": "Stopped", "CPU": "0%"}
]
logger.table("Service Status", data)
```

### Tree Structure - `logger.tree()`
Suitable for displaying hierarchical relationships:
```python
structure = {
    "Application": {
        "Frontend": ["React", "Redux"],
        "Backend": ["FastAPI", "PostgreSQL"],
        "Deployment": ["Docker", "Kubernetes"]
    }
}
logger.tree("Tech Stack", structure)
```

### ASCII Art - `logger.ascii_header()`
Suitable for creating visual separators:
```python
# Application startup
logger.ascii_header("STARTUP", font="slant", border_style="green")

# Section separator
logger.ascii_header("PHASE 1", font="small")
```

## 🔧 Performance Considerations

1. **Simple First**: If `block()` meets your needs, don't use `panel()`
2. **Batch Display**: Avoid frequent visual method calls in loops
3. **Target-Oriented**: Use `console_*` and `file_*` prefixes to control output targets

```python
# Console shows progress, file logs results
logger.console_panel(progress_table, title="Progress")
logger.file_panel(final_results, title="Final Results")
```

## 📚 Best Practices

1. **Consistency**: Maintain consistent use of colors and styles throughout your application
2. **Moderation**: Visual elements should enhance, not distract from information delivery
3. **Consider Environment**: Some terminals may not support all visual effects
4. **Documentation**: Document your color and style conventions

## 🔗 Related Resources

- [API Documentation - Visual Methods](../api/#_2)
- [Rich Panel Feature Details](../features/rich-panel)
- [Example Collection](../examples/visual)