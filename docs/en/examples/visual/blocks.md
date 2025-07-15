# Rich Block Examples

Rich blocks are the most practical visualization feature of pretty-loguru. This page showcases various practical applications of Rich blocks.

## 🎯 Basic Usage

### Simple Block

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="blocks_demo",
    log_path="blocks_demo",
    level="INFO"
)

# The most basic block
logger.block(
    "Basic Information",
    [
        "Application Name: MyApp",
        "Version: 1.1.2",
        "Author: Development Team"
    ]
)
```

### Styled Block

```python
# Green block for success status
logger.block(
    "Startup Successful",
    [
        "✅ Configuration loaded successfully",
        "✅ Database connection successful",
        "✅ Service has started"
    ],
    border_style="green",
    log_level="SUCCESS"
)
```

## 🎨 Border Style Showcase

### Borders with Different Colors

```python
def demo_border_colors():
    """Showcase border effects with different colors"""
    
    # Green - Success status
    logger.block(
        "Success Status",
        [
            "✅ All checks passed",
            "✅ System is running normally",
            "✅ Ready"
        ],
        border_style="green"
    )
    
    # Yellow - Warning status  
    logger.block(
        "Warning Status",
        [
            "⚠️  Memory usage at 75%",
            "⚠️  Recommend monitoring load",
            "💡 Consider scaling resources"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    # Red - Error status
    logger.block(
        "Error Status", 
        [
            "❌ Service connection failed",
            "❌ Database not responding",
            "🔧 Immediate action required"
        ],
        border_style="red",
        log_level="ERROR"
    )
    
    # Blue - Info status
    logger.block(
        "System Information",
        [
            "🖥️  Operating System: Linux",
            "🐍 Python Version: 3.9",
            "📦 Package Version: 1.1.2"
        ],
        border_style="blue"
    )
```

### Different Border Styles

```python
def demo_border_styles():
    """Showcase different border styles"""
    
    # Solid border
    logger.block(
        "Solid Border",
        ["This is the effect of a solid border"],
        border_style="solid"
    )
    
    # Double border
    logger.block(
        "Double Border",
        ["This is the effect of a double border"],
        border_style="double"
    )
    
    # Rounded border
    logger.block(
        "Rounded Border",
        ["This is the effect of a rounded border"],
        border_style="rounded"
    )
    
    # Thick border
    logger.block(
        "Thick Border",
        ["This is the effect of a thick border"],
        border_style="thick"
    )
```

## 📊 Practical Application Scenarios

### System Monitoring Dashboard

```python
import psutil
import datetime

def system_monitoring_dashboard():
    """System monitoring dashboard"""
    
    # Get system information
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # CPU monitoring
    cpu_color = "red" if cpu_percent > 80 else "yellow" if cpu_percent > 60 else "green"
    logger.block(
        "CPU Monitoring",
        [
            f"🖥️  Usage: {cpu_percent:.1f}%",
            f"⚡ Cores: {psutil.cpu_count()}",
            f"🌡️  Status: {'Overloaded' if cpu_percent > 80 else 'Normal'}"
        ],
        border_style=cpu_color
    )
    
    # Memory monitoring
    memory_color = "red" if memory.percent > 80 else "yellow" if memory.percent > 60 else "green"
    logger.block(
        "Memory Monitoring",
        [
            f"💾 Usage: {memory.percent:.1f}%",
            f"📊 Used: {memory.used // 1024 // 1024 // 1024}GB",
            f"📈 Total: {memory.total // 1024 // 1024 // 1024}GB",
            f"🔄 Available: {memory.available // 1024 // 1024 // 1024}GB"
        ],
        border_style=memory_color
    )
```

### Application Configuration Report

```python
def application_config_report(config):
    """Application configuration report"""
    
    logger.block(
        "Application Configuration",
        [
            f"📱 Application Name: {config.get('app_name', 'Unknown')}",
            f"🏷️  Version: {config.get('version', '1.1.2')}",
            f"🌍 Environment: {config.get('environment', 'development')}",
            f"🔧 Debug Mode: {'On' if config.get('debug', False) else 'Off'}"
        ],
        border_style="blue"
    )
    
    logger.block(
        "Server Configuration",
        [
            f"🌐 Host: {config.get('host', 'localhost')}",
            f"🚪 Port: {config.get('port', 8000)}",
            f"👥 Workers: {config.get('workers', 1)}",
            f"⏱️  Timeout: {config.get('timeout', 30)}s"
        ],
        border_style="cyan"
    )
```

## 💡 Best Practices

### 1. Keep Content Concise

```python
# Recommended - Concise and clear
logger.block(
    "Status Check",
    [
        "API: OK",
        "DB: OK", 
        "Redis: OK"
    ],
    border_style="green"
)

# Avoid - Overly verbose content
logger.block(
    "Very detailed system status check report",
    [
        "The API service is running normally, and the response time is within an acceptable range...",
        "The database connection pool status is good, and all connections are available..."
    ]
)
```

### 2. Use Meaningful Colors

```python
# Create a color specification
STATUS_COLORS = {
    "success": "green",
    "warning": "yellow", 
    "error": "red",
    "info": "blue",
    "debug": "cyan"
}

def status_report(status, message_list):
    logger.block(
        f"{status.upper()} Report",
        message_list,
        border_style=STATUS_COLORS.get(status, "blue")
    )
```

### 3. Enhance Readability with Emojis

```python
logger.block(
    "System Health Check",
    [
        "🖥️  CPU: Normal",
        "💾 Memory: Normal",
        "💿 Disk: Warning",
        "🌐 Network: Normal"
    ],
    border_style="yellow"  # Because there is a warning item
)
```
This complete example showcases all the main features and best practices of Rich blocks. You can run this code directly to see the actual effects!
