# Rich Panel - Advanced Panel Display

Pretty-Loguru provides two panel display methods: the simple `block()` method and the full-featured `panel()` method. This page details the advanced features of the `panel()` method.

## 🎯 Panel vs Block Comparison

| Feature | `logger.block()` | `logger.panel()` |
|---------|-----------------|------------------|
| **Content Format** | Only accepts string lists | Accepts any Rich renderable object |
| **Subtitle** | ❌ Not supported | ✅ Supported |
| **Title Alignment** | Fixed left alignment | ✅ Customizable (left/center/right) |
| **Size Control** | ❌ Not supported | ✅ Supports width/height |
| **Padding** | Fixed value | ✅ Customizable |
| **Rich Objects** | ❌ Not supported | ✅ Full support |
| **Use Case** | Simple text messages | Complex data display |

## 📦 Basic Usage

### Simple Panels

```python
from pretty_loguru import create_logger

logger = create_logger("demo")

# Basic panel
logger.panel("This is a basic Panel", title="Message")

# With subtitle
logger.panel(
    "System running normally",
    title="Status",
    subtitle="Last checked: 2025-01-13 20:00"
)
```

### Border Styles

```python
# Different border styles
logger.panel("Double line border", title="Double", box_style="double")
logger.panel("Heavy line border", title="Heavy", box_style="heavy")
logger.panel("ASCII border", title="ASCII", box_style="ascii")
logger.panel("Minimal border", title="Minimal", box_style="minimal")

# Border colors
logger.panel("Red border", title="Warning", border_style="red")
logger.panel("Green border", title="Success", border_style="green")
logger.panel("Blue border", title="Info", border_style="blue")
```

## 🎨 Advanced Features

### Title Alignment

```python
# Center title
logger.panel(
    "Center-aligned title",
    title="Title",
    title_align="center"
)

# Subtitles can also be aligned
logger.panel(
    "Content",
    title="Left-aligned title",
    subtitle="Right-aligned subtitle",
    title_align="left",
    subtitle_align="right"
)
```

### Size Control

```python
# Fixed width
logger.panel(
    "Fixed 60 characters wide",
    title="Width Control",
    width=60
)

# Fixed height (suitable for fixed format output)
logger.panel(
    "Fixed height panel",
    title="Height Control",
    height=10,
    width=40
)

# No expansion (use actual content width)
logger.panel(
    "Compact display",
    expand=False
)
```

### Padding Control

```python
# No padding (compact mode)
logger.panel("No padding", padding=0)

# Custom padding: (vertical, horizontal)
logger.panel(
    "More vertical spacing",
    padding=(3, 1)  # 3 vertical, 1 horizontal
)

# Full control: (top, right, bottom, left)
logger.panel(
    "Asymmetric padding",
    padding=(1, 2, 3, 4)
)
```

## 🚀 Rich Object Integration

### Using Table

```python
from rich.table import Table

# Create table
table = Table(title="Sales Statistics")
table.add_column("Month", style="cyan", no_wrap=True)
table.add_column("Revenue", style="magenta")
table.add_column("Growth", justify="right", style="green")

table.add_row("January", "$10,000", "+5%")
table.add_row("February", "$12,000", "+20%")
table.add_row("March", "$11,500", "-4%")

# Display table in panel
logger.panel(
    table,
    title="Quarterly Report",
    subtitle="Q1 2025",
    border_style="blue",
    box_style="double"
)
```

### Using Tree

```python
from rich.tree import Tree

# Create tree structure
tree = Tree("📁 Project Structure")
src = tree.add("📁 src")
src.add("📄 main.py")
src.add("📄 config.py")
models = src.add("📁 models")
models.add("📄 user.py")
models.add("📄 product.py")

# Display in panel
logger.panel(
    tree,
    title="Directory Structure",
    border_style="green"
)
```

### Using Syntax (Code Highlighting)

```python
from rich.syntax import Syntax

code = '''
def calculate_fibonacci(n):
    """Calculate Fibonacci sequence"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)

logger.panel(
    syntax,
    title="Example Code",
    subtitle="fibonacci.py",
    border_style="yellow"
)
```

### Using Rich Text

```python
from rich.text import Text

# Create formatted text
text = Text()
text.append("System Status: ", style="bold white")
text.append("Running\n", style="bold green")
text.append("CPU Usage: ", style="white")
text.append("45%\n", style="yellow")
text.append("Memory: ", style="white")
text.append("2.3GB / 8GB", style="cyan")

logger.panel(
    text,
    title="System Monitor",
    border_style="blue",
    box_style="rounded"
)
```

## 📊 Practical Application Examples

### Error Message Panel

```python
from rich.text import Text
from rich.table import Table

def display_error_details(error_type, message, traceback_info):
    # Create error content
    content = Text()
    content.append("Error Type: ", style="bold red")
    content.append(f"{error_type}\n\n", style="red")
    content.append("Error Message: ", style="bold")
    content.append(f"{message}\n\n", style="white")
    
    # Add traceback info table
    trace_table = Table(show_header=False, box=None)
    trace_table.add_column("File", style="cyan")
    trace_table.add_column("Line", style="yellow")
    trace_table.add_column("Function", style="green")
    
    for trace in traceback_info:
        trace_table.add_row(trace['file'], str(trace['line']), trace['function'])
    
    # Display error panel
    logger.panel(
        content,
        title="❌ Error Occurred",
        subtitle="Please check the following information",
        border_style="red",
        box_style="double",
        padding=(1, 2)
    )
    
    # Display traceback
    logger.panel(
        trace_table,
        title="Call Stack",
        border_style="yellow"
    )
```

### Configuration Summary Panel

```python
from rich.tree import Tree
from rich.text import Text

def display_config_summary(config):
    # Create configuration tree
    tree = Tree("⚙️ Application Configuration")
    
    # Basic settings
    basic = tree.add("📋 Basic Settings")
    basic.add(f"Environment: {config['env']}")
    basic.add(f"Debug Mode: {'✅' if config['debug'] else '❌'}")
    basic.add(f"Log Level: {config['log_level']}")
    
    # Database settings
    db = tree.add("🗄️ Database")
    db.add(f"Type: {config['db']['type']}")
    db.add(f"Host: {config['db']['host']}")
    db.add(f"Port: {config['db']['port']}")
    
    # API settings
    api = tree.add("🌐 API")
    api.add(f"Version: {config['api']['version']}")
    api.add(f"Rate Limit: {config['api']['rate_limit']}/minute")
    
    # Display configuration panel
    logger.panel(
        tree,
        title="Startup Configuration",
        subtitle=f"Loaded from: {config['config_file']}",
        border_style="cyan",
        box_style="rounded",
        title_align="center"
    )
```

### Progress Report Panel

```python
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table

def display_task_progress(tasks):
    # Create progress table
    table = Table(title="Task Progress")
    table.add_column("Task Name", style="cyan", width=20)
    table.add_column("Status", style="yellow")
    table.add_column("Progress", style="green")
    table.add_column("ETA", style="magenta")
    
    for task in tasks:
        status = "🟢 Running" if task['active'] else "⏸️ Paused"
        progress = f"{task['completed']}/{task['total']} ({task['percentage']}%)"
        eta = task.get('eta', 'N/A')
        
        table.add_row(task['name'], status, progress, eta)
    
    # Display progress panel
    logger.panel(
        table,
        title="Batch Processing Progress",
        subtitle="Auto-updating...",
        border_style="green",
        box_style="heavy",
        width=80
    )
```

## 🎯 Best Practices

### 1. Choose the Appropriate Method

```python
# Use block() for simple text messages
logger.block("Simple message", ["Line 1", "Line 2"])

# Use panel() for complex content
logger.panel(rich_table, title="Data Display")
```

### 2. Use Colors Effectively

```python
# Error - Red
logger.panel(error_msg, title="Error", border_style="red")

# Success - Green
logger.panel(success_msg, title="Success", border_style="green")

# Warning - Yellow
logger.panel(warning_msg, title="Warning", border_style="yellow")

# Info - Blue
logger.panel(info_msg, title="Info", border_style="blue")
```

### 3. Target-Oriented Output

```python
# Console only for progress
logger.console_panel(
    progress_table,
    title="Real-time Progress",
    border_style="cyan"
)

# File only for detailed information
logger.file_panel(
    detailed_report,
    title="Complete Report",
    subtitle=f"Generated: {datetime.now()}"
)
```

### 4. Combine Usage

```python
# First use panel to display summary
logger.panel(
    summary_text,
    title="Execution Summary",
    border_style="blue"
)

# Then use other Rich components for details
logger.table("Detailed Data", data_list)
logger.tree("Processing Flow", process_tree)
```

## 📚 Reference Resources

- [Rich Panel Documentation](https://rich.readthedocs.io/en/latest/panel.html)
- [Pretty-Loguru API Documentation](../api/#loggerpanel-rich-panel)
- [Visual Methods Comparison](../guide/visual-methods)