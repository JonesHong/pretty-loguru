# Visual Features Examples

Showcasing Pretty-Loguru's visual features, including Rich blocks, ASCII art, and various visual components.

## Rich Blocks and Panels

### Using block() - Simple Blocks

```python
from pretty_loguru import create_logger

logger = create_logger("visual_demo")

# Basic block
logger.block(
    "System Info",
    [
        "Operating System: Ubuntu 22.04",
        "Python Version: 3.10.5",
        "Memory Usage: 4.2GB / 16GB",
        "CPU Usage: 35%"
    ]
)

# Custom style
logger.block(
    "✅ Deployment Successful",
    [
        "Version: v2.1.0",
        "Deploy Time: 2024-01-20 15:30:00",
        "Environment: Production",
        "Status: Healthy"
    ],
    border_style="green",
    log_level="SUCCESS"
)

# Error report block
logger.block(
    "❌ Error Details",
    [
        "Error Code: E001",
        "Error Message: Database connection timeout",
        "Occurred At: 2024-01-20 15:25:00",
        "Impact: User login functionality",
        "Suggested Action: Check database service status"
    ],
    border_style="red",
    log_level="ERROR"
)
```

### Using panel() - Advanced Panels

```python
from pretty_loguru import create_logger
from rich.table import Table
from rich.text import Text

logger = create_logger("panel_demo")

# Basic Panel
logger.panel("Important Announcement", title="Notice", border_style="yellow")

# Panel with subtitle
logger.panel(
    "System maintenance will begin at 10 PM tonight",
    title="Maintenance Notice",
    subtitle="Estimated 2 hours",
    border_style="orange1",
    box_style="double"
)

# Using Rich Text object
status = Text()
status.append("Server Status: ", style="bold")
status.append("Running\n", style="bold green")
status.append("Uptime: ", style="bold")
status.append("72 hours 15 minutes\n", style="cyan")
status.append("Connections: ", style="bold")
status.append("1,234", style="yellow")

logger.panel(
    status,
    title="Live Status",
    border_style="green",
    box_style="rounded",
    padding=(1, 2)
)

# Display table in Panel
error_table = Table(show_header=True, header_style="bold red")
error_table.add_column("Time", style="dim", width=20)
error_table.add_column("Error Code", style="red")
error_table.add_column("Description")

error_table.add_row("2025-01-13 19:45:00", "E001", "Connection timeout")
error_table.add_row("2025-01-13 19:46:15", "E002", "Authentication failed")
error_table.add_row("2025-01-13 19:47:30", "E001", "Connection timeout")

logger.panel(
    error_table,
    title="Recent Errors",
    subtitle="Last updated: 19:48",
    border_style="red",
    box_style="heavy",
    title_align="center",
    width=80
)

# Compact mode (no padding)
logger.panel(
    "URGENT: System will restart soon",
    title="⚠️ Warning",
    border_style="red",
    padding=0,
    expand=False
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/03_visual/blocks.py)

## ASCII Art

Create eye-catching ASCII art headers:

```python
from pretty_loguru import create_logger

logger = create_logger("ascii_demo")

# Basic ASCII headers
logger.ascii_header("WELCOME")
logger.ascii_header("SUCCESS", border_style="green")
logger.ascii_header("WARNING", border_style="yellow")

# Different font showcase
fonts = ["standard", "slant", "small", "doom", "block"]
for font in fonts:
    logger.ascii_header(f"FONT {font.upper()}", font=font)

# Use case: Startup header
logger.ascii_header("MyApp", font="slant", border_style="blue")
logger.info("Application starting...")
logger.success("✅ All services ready")

# Use case: Deployment flow
logger.ascii_header("DEPLOY", font="doom", border_style="cyan")
logger.block(
    "Deployment Info",
    [
        "Environment: Production",
        "Branch: main",
        "Commit: abc123def"
    ]
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/03_visual/ascii_art.py)

## ASCII Blocks

Combine ASCII art with Rich blocks:

```python
from pretty_loguru import create_logger

logger = create_logger("combined_visual")

# ASCII header + content block
logger.ascii_block(
    "System Status Report",
    [
        "🟢 Web Service: Running",
        "🟢 Database: Connected",
        "🟡 Cache Service: Performance degraded",
        "🔴 Mail Service: Offline"
    ],
    ascii_header="STATUS",
    ascii_font="small",
    border_style="cyan"
)

# Deployment completion report
logger.ascii_block(
    "Deployment Result",
    [
        "✅ Code update completed",
        "✅ Database migration successful",
        "✅ Service restart completed",
        "✅ Health check passed",
        "",
        "Deploy Duration: 3m 15s",
        "Version: v2.1.0 → v2.2.0"
    ],
    ascii_header="DEPLOY",
    ascii_font="block",
    border_style="green",
    log_level="SUCCESS"
)
```

## Rich Components

Using Rich's advanced components:

```python
from pretty_loguru import create_logger

logger = create_logger("rich_components")

# Table
table_data = [
    ["Service Name", "Status", "Memory", "CPU"],
    ["Web Server", "🟢 Running", "125MB", "12%"],
    ["Database", "🟢 Running", "512MB", "25%"],
    ["Cache", "🟡 Warning", "256MB", "45%"],
    ["Queue", "🔴 Stopped", "0MB", "0%"]
]
logger.table("Service Monitor", table_data, style="blue")

# Tree structure
tree_data = {
    "Project Structure": {
        "src": {
            "models": ["user.py", "product.py"],
            "views": ["home.py", "api.py"],
            "utils": ["helpers.py", "validators.py"]
        },
        "tests": ["test_models.py", "test_views.py"],
        "docs": ["README.md", "API.md"]
    }
}
logger.tree("Directory Structure", tree_data, style="green")

# Progress bar
with logger.progress("Processing Files") as progress:
    task = progress.add_task("Download", total=100)
    for i in range(100):
        progress.update(task, advance=1)
        time.sleep(0.01)

# Multi-column display
columns_data = [
    ["Feature A", "✅ Complete\nTests passed"],
    ["Feature B", "🚧 In Progress\n70% done"],
    ["Feature C", "📅 Planned\nNext week"]
]
logger.columns("Development Progress", columns_data, style="cyan")
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/03_visual/rich_components.py)

## Code Highlighting

Display syntax-highlighted code:

```python
from pretty_loguru import create_logger

logger = create_logger("code_demo")

# Python code
python_code = '''
def fibonacci(n):
    """Calculate Fibonacci sequence"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
logger.code("Python Example", python_code, language="python")

# SQL query
sql_code = '''
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
HAVING order_count > 5
ORDER BY order_count DESC;
'''
logger.code("SQL Query", sql_code, language="sql")

# JSON configuration
json_code = '''{
    "name": "pretty-loguru",
    "version": "1.0.0",
    "features": {
        "visual": true,
        "colors": ["red", "green", "blue"]
    }
}'''
logger.code("Configuration File", json_code, language="json")
```

## Figlet Display (if pyfiglet is installed)

Use Figlet fonts to create large ASCII art:

```python
from pretty_loguru import create_logger, has_figlet

if has_figlet():
    from pretty_loguru import print_figlet_header, get_figlet_fonts
    
    logger = create_logger("figlet_demo")
    
    # Show available fonts
    fonts = get_figlet_fonts()
    logger.info(f"Available Figlet fonts: {len(fonts)}")
    
    # Use Figlet headers
    logger.figlet_header("BIG", font="3-d")
    logger.figlet_header("BANNER", font="banner3")
    
    # Figlet blocks
    logger.figlet_block(
        "Status Report",
        ["System running normally", "All tests passed"],
        figlet_text="OK",
        font="bubble"
    )
```

## Next Steps

- [Configuration Management](./configuration.md) - LoggerConfig and preset configurations
- [Framework Integration](./integrations.md) - FastAPI/Uvicorn integration
- [Production Environment](./production.md) - Deployment and monitoring