# ASCII Art Blocks

ASCII art blocks are the most powerful visualization feature of pretty-loguru, combining the advantages of ASCII art headers and Rich blocks to create a complete report format that is both eye-catching and informative.

## 🎯 Basic Concept

ASCII Art Block = ASCII Art Header + Rich Block Content

This combination provides:
- A striking ASCII art title
- Structured content display
- A unified visual style
- A complete report format

## 🚀 Basic Usage

### Simple ASCII Block

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_dir="logs",
    level="INFO"
)

logger.ascii_block(
    "System Status Report",   // Block title
    [                         // Content list
        "CPU Usage: 25%",
        "Memory Usage: 2.1GB", 
        "Disk Space: 120GB Available"
    ],
    header_text="STATUS",    // ASCII header text
    font="standard",    // ASCII font
    border_style="green",     // Border color
    level="INFO"          // Log level
)
```

### Full Parameter Example

```python
logger.ascii_block(
    title="Deployment Complete Report",
    content=[
        "Application Version: v2.1.0",
        "Deployment Time: 3m 45s",
        "Service Checks: All passed",
        "Load Balancer: Enabled"
    ],
    header_text="DEPLOYED",
    font="block",
    border_style="green",
    level="SUCCESS"
)
```

## 🎨 Visual Showcase

### Success Scenario

```python
logger.ascii_block(
    "Startup Complete Report",
    [
        "✅ Configuration file loaded successfully",
        "✅ Database connection normal",
        "✅ Redis cache ready",
        "✅ API service started",
        "✅ Health check passed"
    ],
    header_text="READY",
    font="slant",
    border_style="green",
    level="SUCCESS"
)
```

### Warning Scenario

```python
logger.ascii_block(
    "System Performance Warning",
    [
        "⚠️  CPU Usage: 87%",
        "⚠️  Memory Usage: 92%",
        "⚠️  Disk I/O: High load",
        "💡 Suggestion: Scale resources or optimize the application"
    ],
    header_text="WARNING",
    font="doom",
    border_style="yellow",
    level="WARNING"
)
```

### Error Scenario

```python
logger.ascii_block(
    "System Failure Report",
    [
        "❌ Database connection failed",
        "❌ Redis service not responding",
        "❌ API health check failed",
        "🔧 Corrective Action: Restart relevant services"
    ],
    header_text="ERROR",
    font="doom", 
    border_style="red",
    level="ERROR"
)
```

## 📊 Practical Application Scenarios

### Application Startup Sequence

```python
def application_startup(app_name, app_version, port, startup_time):
    logger.ascii_block(
        "Startup Checklist",
        [
            "🔧 Loading environment variables",
            "🔧 Parsing configuration file",
            "🔧 Initializing logging system", 
            "🔧 Creating database connection pool"
        ],
        header_text="STARTUP",
        font="slant",
        border_style="blue"
    )
    
    # Execute startup logic...
    
    logger.ascii_block(
        "Startup Complete Summary",
        [
            f"🚀 Application Name: {app_name}",
            f"📦 Version: {app_version}",
            f"🌐 Listening Port: {port}",
            f"⏱️  Startup Time: {startup_time}s"
        ],
        header_text="ONLINE",
        font="block",
        border_style="green",
        level="SUCCESS"
    )
```

### Deployment Process Report

```python
def deployment_report(deployment_info):
    logger.ascii_block(
        "Deployment Execution Report",
        [
            f"📦 Version: {deployment_info['version']}",
            f"🌍 Environment: {deployment_info['environment']}", 
            f"⏱️  Deployment Time: {deployment_info['duration']}",
            f"🔄 Rolling Update: {deployment_info['rolling_update']}",
            f"✅ Health Check: {deployment_info['health_check']}",
            f"📊 Success Rate: {deployment_info['success_rate']}%"
        ],
        header_text="DEPLOYED",
        font="standard",
        border_style="green" if deployment_info['success_rate'] == 100 else "yellow",
        level="SUCCESS" if deployment_info['success_rate'] == 100 else "WARNING"
    )
```

### Data Processing Pipeline

```python
def data_pipeline_summary(stats):
    logger.ascii_block(
        "Data Processing Complete Report",
        [
            f"📥 Input Records: {stats['input_records']:,}",
            f"✅ Processed Successfully: {stats['processed']:,}",
            f"❌ Processing Failed: {stats['failed']:,}",
            f"⏱️  Processing Time: {stats['duration']}",
            f"🚀 Processing Speed: {stats['records_per_second']:,} records/sec",
            f"💾 Output Size: {stats['output_size']}"
        ],
        header_text="COMPLETE",
        font="block",
        border_style="green",
        level="SUCCESS"
    )
```

### System Monitoring Dashboard

```python
def system_health_dashboard():
    import psutil
    import datetime
    
    # Get system information
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Determine status color
    if cpu_percent > 80 or memory.percent > 80:
        color = "red"
        level = "WARNING"
        header = "ALERT"
    elif cpu_percent > 60 or memory.percent > 60:
        color = "yellow" 
        level = "WARNING"
        header = "CAUTION"
    else:
        color = "green"
        level = "INFO"
        header = "HEALTHY"
    
    logger.ascii_block(
        "System Health Monitoring",
        [
            f"🖥️  CPU Usage: {cpu_percent:.1f}%",
            f"💾 Memory Usage: {memory.percent:.1f}% ({memory.used//1024//1024//1024}GB/{memory.total//1024//1024//1024}GB)",
            f"💿 Disk Usage: {disk.percent:.1f}% ({disk.free//1024//1024//1024}GB Available)",
            f"⏰ Check Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ],
        header_text=header,
        font="standard",
        border_style=color,
        level=level
    )
```

### API Request Summary

```python
def api_request_summary(request_stats):
    logger.ascii_block(
        "API Request Statistics Report",
        [
            f"📊 Total Requests: {request_stats['total']:,}",
            f"✅ Successful Requests: {request_stats['success']:,} ({request_stats['success_rate']:.1f}%)",
            f"❌ Failed Requests: {request_stats['failed']:,} ({request_stats['error_rate']:.1f}%)",
            f"⚡ Average Response Time: {request_stats['avg_response_time']:.2f}ms",
            f"🚀 Fastest Response: {request_stats['min_response_time']:.2f}ms",
            f"🐌 Slowest Response: {request_stats['max_response_time']:.2f}ms"
        ],
        header_text="API STATS",
        font="small",
        border_style="blue",
        level="INFO"
    )
```

## 🔧 Advanced Techniques

### Dynamic Content Generation

```python
def dynamic_status_report(services):
    content = []
    all_healthy = True
    
    for service, status in services.items():
        if status['healthy']:
            content.append(f"✅ {service}: Running normally")
        else:
            content.append(f"❌ {service}: {status['error']}")
            all_healthy = False
    
    # Add statistics
    healthy_count = sum(1 for s in services.values() if s['healthy'])
    total_count = len(services)
    content.append(f"📊 Healthy Services: {healthy_count}/{total_count}")
    
    logger.ascii_block(
        "Service Health Check",
        content,
        header_text="HEALTHY" if all_healthy else "ISSUES",
        font="slant",
        border_style="green" if all_healthy else "red",
        level="SUCCESS" if all_healthy else "ERROR"
    )
```

### Conditional Formatting

```python
def build_result_report(build_success, test_results, deployment_ready):
    # Determine overall status based on results
    if build_success and all(test_results.values()) and deployment_ready:
        header = "SUCCESS"
        color = "green"
        level = "SUCCESS"
    elif build_success:
        header = "PARTIAL"
        color = "yellow"
        level = "WARNING"  
    else:
        header = "FAILED"
        color = "red"
        level = "ERROR"
    
    content = [
        f"🔨 Build Status: {'Success' if build_success else 'Failed'}",
        f"🧪 Unit Tests: {'Passed' if test_results.get('unit', False) else 'Failed'}",
        f"🔗 Integration Tests: {'Passed' if test_results.get('integration', False) else 'Failed'}",
        f"🚀 Ready for Deployment: {'Yes' if deployment_ready else 'No'}"
    ]
    
    logger.ascii_block(
        "Build and Test Report",
        content,
        header_text=header,
        font="doom",
        border_style=color,
        level=level
    )
```

## ⚠️ Usage Recommendations

### Content Organization

```python
# Recommended - Concise and organized content
logger.ascii_block(
    "Deployment Status",
    [
        "Version: v1.2.0",
        "Environment: Production", 
        "Status: Success"
    ],
    header_text="DEPLOY",
    font="slant"
)

# Not recommended - Overly verbose content
logger.ascii_block(
    "Very detailed deployment status report containing all possible information",
    [
        "This is a very long content line that contains too much information and may affect the visual effect...",
        "Another very long line of content..."
    ],
    header_text="VERY LONG HEADER",
    font="standard"
)
```

### Color Usage Principles

```python
# Success - Green
logger.ascii_block(..., border_style="green", level="SUCCESS")

# Warning - Yellow
logger.ascii_block(..., border_style="yellow", level="WARNING")

# Error - Red  
logger.ascii_block(..., border_style="red", level="ERROR")

# Info - Blue
logger.ascii_block(..., border_style="blue", level="INFO")

# Special - Purple/Cyan
logger.ascii_block(..., border_style="magenta", level="INFO")
```

## 🚀 Next Steps

ASCII art blocks are the most powerful feature of pretty-loguru. Now you can:

- [View complete visualization examples](../examples/visual/) - Practical applications of all visual features
- [Learn about Rich Blocks](./rich-blocks) - Detailed usage of pure Rich blocks  
- [Explore integration applications](../integrations/) - Use these features in web applications
- [Dive into the API documentation](../api/) - Complete parameter and option descriptions

Start building professional-grade logging report systems!
