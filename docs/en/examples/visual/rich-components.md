# Rich Component Examples

pretty-loguru provides rich visualization components by integrating with the Rich library. This page demonstrates how to use various Rich components to enhance the visual effect of log output.

## 📊 Table Component

### Basic Table

```python
from pretty_loguru import create_logger
from rich.table import Table
from rich.console import Console

# Initialize the logging system
logger = create_logger(
    name="rich-components_demo",
    log_path="rich_components_demo",
    level="INFO"
)

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

## 💻 Code Highlighting

### Basic Code Display

```python
from pretty_loguru import create_logger

# Create logger with Rich components
logger = create_logger(name="code_demo", use_rich_components=True)

def show_python_code():
    """Display syntax-highlighted Python code"""
    
    code = '''
def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"fibonacci({i}) = {fibonacci(i)}")
'''
    
    logger.code(
        code=code,
        language="python",
        title="Fibonacci Function",
        theme="monokai"
    )

show_python_code()
```

### Multi-Language Support

```python
def show_different_languages():
    """Showcase syntax highlighting for different languages"""
    
    # JavaScript code
    js_code = '''
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        return { success: true, data: userData };
    } catch (error) {
        console.error('Failed to fetch user data:', error);
        return { success: false, error: error.message };
    }
}
'''
    
    logger.code(
        code=js_code,
        language="javascript",
        title="JavaScript Async Function",
        theme="github-dark"
    )
    
    # SQL query
    sql_code = '''
SELECT 
    u.user_id,
    u.username,
    u.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE u.created_at >= '2023-01-01'
    AND u.status = 'active'
GROUP BY u.user_id, u.username, u.email
ORDER BY total_spent DESC;
'''
    
    logger.code(
        code=sql_code,
        language="sql",
        title="User Order Statistics Query",
        theme="one-dark"
    )

show_different_languages()
```

### Code from Files

```python
def show_code_from_file():
    """Display code from a file with line range"""
    
    # Display specific lines from a file
    logger.code_file(
        file_path="my_script.py",
        start_line=10,
        end_line=25,
        theme="material"
    )
    
    # Display entire file (auto-detect language)
    logger.code_file(
        file_path="config.json",
        theme="monokai"
    )

show_code_from_file()
```

### Code Difference Comparison

```python
def show_code_diff():
    """Display side-by-side code comparison"""
    
    old_function = '''
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
'''
    
    new_function = '''
def process_data(data):
    """Process data by doubling positive numbers"""
    return [item * 2 for item in data if item > 0]
'''
    
    logger.diff(
        old_code=old_function,
        new_code=new_function,
        old_title="Before Refactoring",
        new_title="After Refactoring",
        language="python"
    )

show_code_diff()
```

### Available Themes

```python
def showcase_themes():
    """Show the same code in different themes"""
    
    sample_code = '''
class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.processed_count = 0
    
    def process(self, data):
        self.processed_count += 1
        return f"Processed: {data}"
'''
    
    themes = ["monokai", "github-dark", "one-dark", "material"]
    
    for theme in themes:
        logger.code(
            code=sample_code,
            language="python",
            title=f"DataProcessor Class ({theme} theme)",
            theme=theme,
            to_console_only=True  # Only display in console
        )

showcase_themes()
```

### Supported Languages

The code highlighting feature supports many programming languages including:

- **Python** (.py)
- **JavaScript** (.js)
- **TypeScript** (.ts)
- **HTML** (.html)
- **CSS** (.css)
- **JSON** (.json)
- **SQL** (.sql)
- **Markdown** (.md)
- **YAML** (.yaml, .yml)
- **XML** (.xml)
- **Bash** (.sh)
- **C/C++** (.c, .cpp)
- **Java** (.java)
- **Go** (.go)
- **Rust** (.rs)
- **PHP** (.php)
- **Ruby** (.rb)

### Available Themes

Choose from various syntax highlighting themes:

- `monokai` (default)
- `github-dark`
- `github-light`
- `one-dark`
- `material`
- `dracula`
- `nord`
- `solarized-dark`
- `solarized-light`

### Code Highlighting Features

✅ **Syntax Highlighting** - Full language syntax support  
✅ **Line Numbers** - Optional line number display  
✅ **Custom Themes** - Multiple color schemes  
✅ **File Reading** - Direct file content display  
✅ **Line Ranges** - Display specific line ranges  
✅ **Auto Detection** - Automatic language detection from file extensions  
✅ **Diff Comparison** - Side-by-side code comparison with Git-style colors  
✅ **Target Output** - Separate console/file output control  

Rich components provide powerful visualization capabilities for pretty-loguru, making log output more professional and readable!
