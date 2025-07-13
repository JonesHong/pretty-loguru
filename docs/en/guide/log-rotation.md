# Log Rotation

Log rotation is an important mechanism for managing log file size and quantity. pretty-loguru provides flexible and powerful rotation strategies.

## 🎯 Configuration Template Rotation Presets

Pretty-Loguru provides predefined rotation configuration templates through `ConfigTemplates` to quickly set up common time-based rotation strategies:

### Daily Rotation

```python
from pretty_loguru import ConfigTemplates

# Daily rotation configuration
config = ConfigTemplates.daily()
logger = config.apply_to("daily_app")

# Configuration includes:
# - rotation: "00:00" (rotates at midnight daily)
# - retention: "30 days" (keeps logs for 30 days)
# - Current filename: [component]daily_latest.temp.log
# - Rotated compressed filename: [component]YYYYMMDD.log
```

### Hourly Rotation

```python
# Hourly rotation configuration
config = ConfigTemplates.hourly()
logger = config.apply_to("hourly_app")

# Configuration includes:
# - rotation: "1 hour" (rotates every hour)
# - retention: "7 days" (keeps logs for 7 days)
# - Current filename: [component]hourly_latest.temp.log
# - Rotated compressed filename: [component]YYYYMMDD_HH.log
```

### Weekly Rotation

```python
# Weekly rotation configuration
config = ConfigTemplates.weekly()
logger = config.apply_to("weekly_app")

# Configuration includes:
# - rotation: "monday" (rotates every Monday)
# - retention: "12 weeks" (keeps logs for 12 weeks)
# - Current filename: [component]weekly_latest.temp.log
# - Rotated compressed filename: [component]week_YYYYWNN.log
```

### Monthly Rotation

```python
# Monthly rotation configuration
config = ConfigTemplates.monthly()
logger = config.apply_to("monthly_app")

# Configuration includes:
# - rotation: "1 month" (rotates monthly)
# - retention: "12 months" (keeps logs for 12 months)
# - Current filename: [component]monthly_latest.temp.log
# - Rotated compressed filename: [component]YYYYMM.log
```

### Minute Rotation

```python
# Minute rotation configuration (suitable for high-frequency testing)
config = ConfigTemplates.minute()
logger = config.apply_to("minute_app")

# Configuration includes:
# - rotation: "1 minute" (rotates every minute)
# - retention: "24 hours" (keeps logs for 24 hours)
# - Current filename: [component]minute_latest.temp.log
# - Rotated compressed filename: [component]YYYYMMDD_HHMM.log
```

### File Naming Rules

Time-based rotation presets use fixed filenames, renaming based on time range only during rotation:

| Preset Type | Current Filename | Rotated Filename Format | Rotated Example |
|-------------|------------------|-------------------------|-----------------|
| daily | `[{name}]daily_latest.temp.log` | `[{name}]{date}.log` | `[myapp]20250113.log` |
| hourly | `[{name}]hourly_latest.temp.log` | `[{name}]{date}_{hour}.log` | `[myapp]20250113_14.log` |
| weekly | `[{name}]weekly_latest.temp.log` | `[{name}]week_{year}W{week_num}.log` | `[myapp]week_2025W03.log` |
| monthly | `[{name}]monthly_latest.temp.log` | `[{name}]{year}{month}.log` | `[myapp]202501.log` |
| minute | `[{name}]minute_latest.temp.log` | `[{name}]{date}_{hour}{minute}.log` | `[myapp]20250113_1430.log` |

**Note**:
- The currently active log file uses the `xxx_latest.temp.log` format
- When rotation is triggered, the file is renamed based on the time range it covers
- Example: `[myapp]daily_latest.temp.log` becomes `[myapp]20250113.log` when rotated at midnight

### Custom Rotation Configuration

You can customize based on preset configurations:

```python
# Customize daily rotation
custom_daily = ConfigTemplates.daily()
custom_daily.update(
    retention="60 days",     # Keep for 60 days instead of 30
    compression="gz"         # Use gzip compression
)
logger = custom_daily.apply_to("custom_app")
```

## 🔄 Rotation Strategies

### Size-Based Rotation

Rotate when file reaches a certain size:

```python
from pretty_loguru import create_logger

# Rotate when file reaches 10MB
logger = create_logger(
    "app",
    log_path="logs",
    rotation="10 MB"
)

# Other size units
logger = create_logger("app", rotation="100 KB")  # 100 kilobytes
logger = create_logger("app", rotation="1 GB")   # 1 gigabyte
```

### Time-Based Rotation

Rotate at specific time intervals:

```python
# Daily rotation at midnight
logger = create_logger("app", rotation="00:00")

# Rotate every 6 hours
logger = create_logger("app", rotation="6 hours")

# Rotate at specific time
from datetime import time
logger = create_logger("app", rotation=time(2, 0))  # 2:00 AM

# Rotate on specific weekday
logger = create_logger("app", rotation="monday")  # Every Monday
logger = create_logger("app", rotation="friday at 18:00")  # Friday 6 PM
```

### Custom Rotation Function

Create custom rotation logic:

```python
def should_rotate(message, file):
    """Custom rotation logic"""
    # Rotate if file is larger than 50MB or it's midnight
    file_size = file.tell()
    current_hour = message.record["time"].hour
    
    return file_size > 50 * 1024 * 1024 or current_hour == 0

logger = create_logger(
    "app",
    rotation=should_rotate
)
```

## 📦 Retention Policies

### Time-Based Retention

Keep logs for a specific duration:

```python
# Keep logs for 30 days
logger = create_logger("app", retention="30 days")

# Other time units
logger = create_logger("app", retention="1 week")
logger = create_logger("app", retention="3 months")
logger = create_logger("app", retention="1 year")
```

### Count-Based Retention

Keep a specific number of log files:

```python
# Keep only the 10 most recent log files
logger = create_logger("app", retention=10)
```

### Custom Retention Function

Create custom retention logic:

```python
from datetime import datetime, timedelta

def cleanup_old_logs(path):
    """Keep logs from current month only"""
    file_date = datetime.fromtimestamp(path.stat().st_mtime)
    current_month = datetime.now().month
    
    return file_date.month != current_month

logger = create_logger("app", retention=cleanup_old_logs)
```

## 🗜️ Compression

### Built-in Compression Formats

```python
# ZIP compression
logger = create_logger("app", compression="zip")

# GZIP compression
logger = create_logger("app", compression="gz")

# BZ2 compression
logger = create_logger("app", compression="bz2")

# TAR compression
logger = create_logger("app", compression="tar")

# TAR.GZ compression
logger = create_logger("app", compression="tar.gz")
```

### Custom Compression Function

```python
import gzip
import shutil

def custom_compress(path):
    """Custom compression with high compression level"""
    gz_path = f"{path}.gz"
    
    with open(path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Remove original file
    path.unlink()

logger = create_logger("app", compression=custom_compress)
```

## 🎯 Common Patterns

### Production Setup

```python
# Production configuration with daily rotation
prod_logger = create_logger(
    "production_app",
    log_path="/var/log/myapp",
    rotation="00:00",         # Rotate at midnight
    retention="90 days",      # Keep 3 months
    compression="gz"          # Compress old logs
)
```

### High-Volume Logging

```python
# For applications with high log volume
high_volume_logger = create_logger(
    "high_volume_app",
    log_path="logs",
    rotation="100 MB",        # Size-based rotation
    retention=20,             # Keep 20 files
    compression="gz",         # Compress immediately
    enqueue=True             # Async logging
)
```

### Development Setup

```python
# Development with frequent rotation for testing
dev_logger = create_logger(
    "dev_app",
    log_path="logs/dev",
    rotation="10 MB",         # Small files
    retention="3 days",       # Short retention
    compression=None          # No compression
)
```

## 📊 Rotation Examples

### Combined Strategies

```python
from datetime import time

# Rotate daily at 2 AM or when file reaches 100MB
def combined_rotation(message, file):
    # Check time
    current_time = message.record["time"]
    is_2am = current_time.hour == 2 and current_time.minute == 0
    
    # Check size
    is_large = file.tell() > 100 * 1024 * 1024
    
    return is_2am or is_large

logger = create_logger(
    "app",
    rotation=combined_rotation,
    retention="30 days"
)
```

### Environment-Based Rotation

```python
import os

def get_rotation_config():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return {
            "rotation": "00:00",      # Daily
            "retention": "90 days",   # 3 months
            "compression": "gz"
        }
    elif env == "staging":
        return {
            "rotation": "100 MB",     # Size-based
            "retention": "30 days",   # 1 month
            "compression": "zip"
        }
    else:  # development
        return {
            "rotation": "10 MB",      # Small files
            "retention": "7 days",    # 1 week
            "compression": None
        }

config = get_rotation_config()
logger = create_logger("app", **config)
```

## 🔍 Best Practices

1. **Choose Appropriate Strategy**: Use time-based for predictable patterns, size-based for variable log volume
2. **Consider Disk Space**: Set retention policies based on available storage
3. **Use Compression**: Enable compression for long-term storage
4. **Monitor Performance**: Large uncompressed logs can impact performance
5. **Test Rotation**: Verify rotation works as expected in development

## 🔗 Related Resources

- [Configuration Guide](./enhanced-config.md) - Advanced configuration options
- [Production Guide](./production.md) - Production best practices
- [API Reference](../api/#rotation-options) - Complete rotation API