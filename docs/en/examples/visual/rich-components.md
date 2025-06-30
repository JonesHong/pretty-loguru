# Rich Component Examples

pretty-loguru provides rich visualization components by integrating with the Rich library. This page demonstrates how to use various Rich components to enhance the visual effect of log output.

## 📊 Table Component

### Basic Table

```python
from pretty_loguru import logger, logger_start
from rich.table import Table
from rich.console import Console

# Initialize the logging system
logger_start(folder="rich_components_demo")

def system_status_table():
    """Display system status using a table"""
    
    # Create a table
    table = Table(title="System Service Status", show_header=True, header_style="bold magenta")
    table.add_column("Service Name", style="cyan", width=12)
    table.add_column("Status", style="green", width=8)
    table.add_column("Memory Usage", style="yellow", width=10)
    table.add_column("CPU Usage", style="red", width=8)
    table.add_column("Uptime", style="blue", width=12)
    
    # Add data
    table.add_row("Web Server", "✅ Running", "245MB", "12%", "2d 3h")
    table.add_row("Database", "✅ Running", "1.2GB", "8%", "5d 1h")
    table.add_row("Redis", "✅ Running", "128MB", "3%", "2d 3h")
    table.add_row("Queue Worker", "⚠️ Warning", "456MB", "25%", "1d 5h")
    table.add_row("Log Service", "❌ Stopped", "0MB", "0%", "Stopped")
    
    # Output using Rich console
    console = Console()
    console.print(table)
    
    logger.info("System status table has been displayed")

system_status_table()
```

## 🌳 Tree Structure

### File System Structure

```python
from rich.tree import Tree

def show_project_structure():
    """Display project directory structure"""
    
    tree = Tree("📁 my-project/", style="bold blue")
    
    # Source code directory
    src = tree.add("📁 src/", style="cyan")
    src.add("📄 __init__.py")
    src.add("📄 main.py")
    src.add("📄 config.py")
    
    # Modules directory
    modules = src.add("📁 modules/", style="cyan")
    modules.add("📄 auth.py")
    modules.add("📄 database.py")
    modules.add("��� api.py")
    
    # Tests directory
    tests = tree.add("📁 tests/", style="green")
    tests.add("📄 test_auth.py")
    
    console = Console()
    console.print(tree)
    
    logger.info("Project structure tree has been displayed")

show_project_structure()
```

## 📈 Progress Bar

### Task Progress Display

```python
from rich.progress import Progress
import time

def show_deployment_progress():
    """Display deployment progress"""
    
    with Progress() as progress:
        # Create multiple tasks
        build_task = progress.add_task("🔨 Building application...", total=100)
        test_task = progress.add_task("🧪 Running tests...", total=100)
        deploy_task = progress.add_task("🚀 Deploying to production...", total=100)
        
        # Simulate build process
        for i in range(100):
            time.sleep(0.02)
            progress.update(build_task, advance=1)
        
        logger.success("Application build complete")
        
        # Simulate test process
        for i in range(100):
            time.sleep(0.01)
            progress.update(test_task, advance=1)
        
        logger.success("Tests executed successfully")
        
        # Simulate deployment process
        for i in range(100):
            time.sleep(0.03)
            progress.update(deploy_task, advance=1)
        
        logger.success("Deployment complete")

show_deployment_progress()
```

## 📋 Panel

### Information Panel

```python
from rich.panel import Panel
from rich.align import Align

def show_system_info():
    """Display system information panel"""
    
    system_info = """
🖥️  OS: Linux Ubuntu 20.04
🐍 Python Version: 3.9.7
💾 Memory: 16GB DDR4
💿 Storage: 512GB SSD
🌐 Network: 1Gbps Ethernet
    """
    
    panel = Panel(
        Align.center(system_info),
        title="💻 System Information",
        title_align="center",
        border_style="blue",
        padding=(1, 2)
    )
    
    console = Console()
    console.print(panel)

show_system_info()
```

## 🎨 Styles and Themes

### Custom Styles

```python
from rich.style import Style
from rich.text import Text

def show_styled_output():
    """Showcase various style effects"""
    
    console = Console()
    
    # Text styles
    console.print("This is [bold]bold[/bold] text")
    console.print("This is [italic]italic[/italic] text")
    console.print("This is [underline]underline[/underline] text")
    console.print("This is [strike]strikethrough[/strike] text")
    
    # Color styles
    console.print("This is [red]red[/red] text")
    console.print("This is [green]green[/green] text")
    
    # Background colors
    console.print("This is [white on red]white on red[/white on red] text")
    
    # Combined styles
    console.print("This is [bold red on white]bold red on white[/bold red on white] text")

show_styled_output()
```

Rich components provide powerful visualization capabilities for pretty-loguru, making log output more professional and readable!
