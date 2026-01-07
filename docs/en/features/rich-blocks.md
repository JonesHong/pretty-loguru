# Rich Block Logs

Rich blocks are one of the most practical features of pretty-loguru, allowing you to create structured, beautiful log outputs, especially suitable for displaying system status, configuration information, or error reports.

## 🎯 Basic Usage

### Simple Block

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_dir="logs",
    level="INFO"
)

logger.block(
    "Basic Information",
    [
        "Application Name: MyApp",
        "Version: 1.1.2",
        "Start Time: 2024-06-30 10:30:00"
    ]
)
```

### Styled Block

```python
logger.block(
    "System Status",
    [
        "CPU: 25%",
        "Memory: 2.1GB / 8GB", 
        "Disk: 150GB Available"
    ],
    border_style="green",    // Green border
    level="INFO"             // Log level
)
```

## 🎨 Border Styles

Rich supports multiple border styles, each with a different visual effect:

### Solid Border

```python
logger.block(
    "Solid Border",
    ["This is an example of a solid border"],
    border_style="solid"
)
```

### Double Border

```python
logger.block(
    "Double Border", 
    ["This is an example of a double border"],
    border_style="double"
)
```

### Rounded Border

```python
logger.block(
    "Rounded Border",
    ["This is an example of a rounded border"], 
    border_style="rounded"
)
```

### Thick Border

```python
logger.block(
    "Thick Border",
    ["This is an example of a thick border"],
    border_style="thick"
)
```

## 🌈 Color Themes

Use different colors to express different meanings:

### Success Status (Green)

```python
logger.block(
    "Deployment Successful",
    [
        "✅ Code deployment complete",
        "✅ Database migration complete", 
        "✅ Service health check passed",
        "✅ Load balancer updated"
    ],
    border_style="green",
    level="SUCCESS"
)
```

### Warning Status (Yellow)

```python
logger.block(
    "Performance Warning",
    [
        "⚠️  CPU Usage: 85%",
        "⚠️  Memory Usage: 90%",
        "⚠️  Response Time: 2.5s",
        "💡 Suggestion: Scale up service instances"
    ],
    border_style="yellow",
    level="WARNING"
)
```

### Error Status (Red)

```python
logger.block(
    "System Error",
    [
        "❌ Database connection failed",
        "❌ Redis service not responding",
        "❌ External API timeout",
        "🔧 Recommendation: Check network connection"
    ],
    border_style="red", 
    level="ERROR"
)
```

### Information Status (Blue)

```python
logger.block(
    "System Information",
    [
        "🖥️  Operating System: Ubuntu 20.04",
        "🐍 Python Version: 3.9.7",
        "📦 Package Version: pretty-loguru 1.1.2",
        "🌐 Network Interface: eth0"
    ],
    border_style="blue",
    level="INFO"
)
```

## 📊 Practical Application Scenarios

### Application Startup Report

```python
def log_startup_info():
    import os
    import psutil
    from datetime import datetime
    
    logger.block(
        "Application Startup Report",
        [
            f"🚀 Application Name: {os.environ.get('APP_NAME', 'MyApp')}",
            f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🆔 Process ID: {os.getpid()}", 
            f"💾 Available Memory: {psutil.virtual_memory().available // 1024 // 1024}MB",
            f"🖥️  CPU Cores: {psutil.cpu_count()}",
            f"🌐 Working Directory: {os.getcwd()}"
        ],
        border_style="cyan",
        level="INFO"
    )
```

### Database Connection Status

```python
def log_database_status(connections):
    status_items = []
    overall_status = "green"
    
    for db_name, is_connected in connections.items():
        if is_connected:
            status_items.append(f"✅ {db_name}: Connected")
        else:
            status_items.append(f"❌ {db_name}: Connection failed")
            overall_status = "red"
    
    logger.block(
        "Database Connection Status",
        status_items,
        border_style=overall_status,
        level="INFO" if overall_status == "green" else "ERROR"
    )
```

### Performance Monitoring Report

```python
def log_performance_metrics():
    import psutil
    import os
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Determine color based on usage
    if cpu_percent > 80 or memory.percent > 80:
        border_color = "red"
        level = "WARNING"
    elif cpu_percent > 60 or memory.percent > 60:
        border_color = "yellow" 
        level = "WARNING"
    else:
        border_color = "green"
        level = "INFO"
    
    logger.block(
        "System Performance Monitoring",
        [
            f"🖥️  CPU Usage: {cpu_percent:.1f}%",
            f"💾 Memory Usage: {memory.percent:.1f}% ({memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB)",
            f"💿 Disk Usage: {disk.percent:.1f}% ({disk.free // 1024 // 1024 // 1024}GB Available)",
            f"📊 Load Average: {', '.join(map(str, os.getloadavg()))}" if hasattr(os, 'getloadavg') else "📊 Load Average: N/A"
        ],
        border_style=border_color,
        level=level
    )
```

## 🔧 Advanced Techniques

### Dynamic Content

```python
def log_user_activity(users_online, recent_actions):
    content = [
        f"👥 Online Users: {users_online}",
        "📈 Recent Activities:"
    ]
    
    # Dynamically add recent actions
    for action in recent_actions[-5:]:  # Show only the last 5
        content.append(f"   • {action}")
    
    logger.block(
        "User Activity Summary",
        content,
        border_style="cyan"
    )
```

### Conditional Styling

```python
def log_service_health(services):
    all_healthy = all(status == "healthy" for status in services.values())
    
    content = []
    for service, status in services.items():
        icon = "✅" if status == "healthy" else "❌"
        content.append(f"{icon} {service}: {status}")
    
    logger.block(
        "Service Health Check",
        content,
        border_style="green" if all_healthy else "red",
        level="INFO" if all_healthy else "ERROR"
    )
```

## 📝 Best Practices

### 1. Keep Content Concise
Each line of content should be clear and to the point, avoiding overly long text.

### 2. Use Appropriate Colors
- 🟢 Green: Success, normal status
- 🟡 Yellow: Warning, needs attention
- 🔴 Red: Error, failure status  
- 🔵 Blue: General information
- 🟣 Purple: Special events
- 🟠 Orange: Ongoing operations

### 3. Use Emojis to Enhance Readability
Appropriate use of emojis can make logs more intuitive and easy to read.

### 4. Group Related Information
Place related information in the same block to improve organization.

## 🚀 Next Steps

- [Explore ASCII Art Headers](./ascii-art) - More eye-catching titles
- [Learn about ASCII Art Blocks](./ascii-blocks) - The powerful combination of both features
- [View Complete Examples](../examples/visual/blocks) - More practical application scenarios

Rich blocks make your logs no longer monotonous. Start creating professional-grade log outputs now! 🎨
