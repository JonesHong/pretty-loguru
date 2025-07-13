# Configuration Management Examples

Demonstrating how to use LoggerConfig, preset configurations, and various rotation strategies.

## Using LoggerConfig

Managing loggers with configuration objects:

```python
from pretty_loguru import create_logger, LoggerConfig, ConfigTemplates

# Basic LoggerConfig usage
config = LoggerConfig(
    level="INFO",
    log_path="logs/app",
    rotation="1 day",
    retention="7 days"
)

# Create logger with config
logger = create_logger("app", config=config)

# Override specific parameters in config
debug_logger = create_logger("debug_app", config=config, level="DEBUG")

# Multi-logger management
services = ["auth", "api", "database"]
service_loggers = {
    name: create_logger(name, config=config)
    for name in services
}

# Dynamic config updates
config.update(level="DEBUG")  # All loggers using this config will update
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/04_configuration/using_logger_config.py)

## Configuration Templates

Using predefined configuration templates:

```python
from pretty_loguru import ConfigTemplates, create_logger

# Development environment
dev_config = ConfigTemplates.development()
dev_logger = create_logger("dev_app", config=dev_config)
# - Level: DEBUG
# - Rotation: 10 MB
# - Retention: 7 days

# Production environment
prod_config = ConfigTemplates.production()
prod_logger = create_logger("prod_app", config=prod_config)
# - Level: INFO
# - Rotation: 50 MB
# - Retention: 30 days
# - Compression: zip
# - Cleaner: Enabled

# Testing environment
test_config = ConfigTemplates.testing()
test_logger = create_logger("test_app", config=test_config)
# - Level: WARNING
# - Rotation: 5 MB
# - Retention: 3 days

# Rotation templates
daily_config = ConfigTemplates.daily()
# Rotates at midnight, keeps 30 days
# Current filename: [daily_app]daily_latest.temp.log
# After rotation: [daily_app]YYYYMMDD.log
daily_logger = create_logger("daily_app", config=daily_config)

hourly_config = ConfigTemplates.hourly()  
# Rotates every hour, keeps 7 days
# Current filename: [hourly_app]hourly_latest.temp.log
# After rotation: [hourly_app]YYYYMMDD_HH.log
hourly_logger = create_logger("hourly_app", config=hourly_config)

weekly_config = ConfigTemplates.weekly()
# Rotates every Monday, keeps 12 weeks
# Current filename: [weekly_app]weekly_latest.temp.log
# After rotation: [weekly_app]week_YYYYWNN.log  
weekly_logger = create_logger("weekly_app", config=weekly_config)

monthly_config = ConfigTemplates.monthly()
# Rotates monthly, keeps 12 months
# Current filename: [monthly_app]monthly_latest.temp.log
# After rotation: [monthly_app]YYYYMM.log
monthly_logger = create_logger("monthly_app", config=monthly_config)

# For testing: minute rotation
minute_config = ConfigTemplates.minute()
# Rotates every minute, keeps 24 hours
# Current filename: [test_app]minute_latest.temp.log
# After rotation: [test_app]YYYYMMDD_HHMM.log
test_logger = create_logger("test_app", config=minute_config)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/04_configuration/templates.py)

## Rotation Strategies

Different log rotation strategies:

```python
from pretty_loguru import create_logger
from datetime import time

# Size-based rotation
size_logger = create_logger(
    "size_based",
    log_path="logs/size",
    rotation="100 MB"  # Rotate when file reaches 100MB
)

# Time-based rotation
time_logger = create_logger(
    "time_based",
    log_path="logs/time",
    rotation="1 day"  # Daily rotation
)

# Specific time rotation
specific_time_logger = create_logger(
    "specific_time",
    log_path="logs/scheduled",
    rotation=time(2, 0)  # Rotate at 2:00 AM
)

# Complex rotation with function
def should_rotate(message, file):
    # Rotate if file is larger than 50MB or it's midnight
    return file.tell() > 50 * 1024 * 1024 or \
           message.record["time"].hour == 0

custom_rotation_logger = create_logger(
    "custom_rotation",
    log_path="logs/custom",
    rotation=should_rotate
)

# Multiple rotation conditions
weekend_logger = create_logger(
    "weekend_rotation",
    log_path="logs/weekend",
    rotation="1 week"  # Weekly rotation
)
```

## Retention Policies

Managing old log files:

```python
from pretty_loguru import create_logger
import datetime

# Keep by time
time_retention_logger = create_logger(
    "time_retention",
    log_path="logs/timed",
    rotation="1 day",
    retention="30 days"  # Keep logs for 30 days
)

# Keep by count
count_retention_logger = create_logger(
    "count_retention",
    log_path="logs/counted",
    rotation="100 MB",
    retention=10  # Keep only 10 log files
)

# Custom retention function
def cleanup_old_logs(path):
    # Keep only logs from current month
    current_month = datetime.datetime.now().month
    file_month = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).month
    return current_month != file_month

custom_retention_logger = create_logger(
    "custom_retention",
    log_path="logs/custom_clean",
    rotation="1 day",
    retention=cleanup_old_logs
)

# No retention (keep all files)
no_retention_logger = create_logger(
    "no_retention",
    log_path="logs/archive",
    rotation="1 week",
    retention=None  # Keep all files
)
```

## Compression

Compressing rotated log files:

```python
from pretty_loguru import create_logger

# ZIP compression
zip_logger = create_logger(
    "zip_logs",
    log_path="logs/compressed",
    rotation="50 MB",
    compression="zip"
)

# GZIP compression
gzip_logger = create_logger(
    "gzip_logs",
    log_path="logs/gzipped",
    rotation="1 day",
    compression="gz"
)

# BZ2 compression
bz2_logger = create_logger(
    "bz2_logs",
    log_path="logs/bzipped",
    rotation="100 MB",
    compression="bz2"
)

# Custom compression function
import tarfile

def custom_compress(file_path):
    """Create tar.gz archive"""
    tar_path = f"{file_path}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(file_path, arcname=file_path.name)
    file_path.unlink()  # Remove original

custom_compress_logger = create_logger(
    "custom_compress",
    log_path="logs/custom_compressed",
    rotation="1 week",
    compression=custom_compress
)
```

## Environment-based Configuration

Configuring based on environment:

```python
from pretty_loguru import create_logger, LoggerConfig, ConfigTemplates
import os

# Get environment
ENV = os.getenv("APP_ENV", "development")

# Environment-specific configurations
ENV_CONFIGS = {
    "development": {
        "template": ConfigTemplates.development,
        "extra": {
            "diagnose": True,
            "backtrace": True
        }
    },
    "staging": {
        "template": ConfigTemplates.production,
        "extra": {
            "level": "DEBUG",
            "retention": "7 days"
        }
    },
    "production": {
        "template": ConfigTemplates.production,
        "extra": {
            "enqueue": True,  # Async logging
            "catch": True,    # Catch errors
            "compression": "gz"
        }
    }
}

# Create environment-specific logger
env_config = ENV_CONFIGS[ENV]
config = env_config["template"]()
config.update(**env_config["extra"])

logger = create_logger("app", config=config)
logger.info(f"Logger configured for {ENV} environment")

# Feature flags
FEATURES = {
    "detailed_errors": ENV != "production",
    "performance_tracking": ENV == "production",
    "debug_mode": ENV == "development"
}

if FEATURES["detailed_errors"]:
    logger.add(
        "logs/errors_detailed.log",
        level="ERROR",
        backtrace=True,
        diagnose=True
    )

if FEATURES["performance_tracking"]:
    logger.add(
        "logs/performance.log",
        filter=lambda record: "performance" in record["extra"]
    )
```

## Next Steps

- [FastAPI Integration](./integrations.md) - Web framework integration
- [Production Setup](./production.md) - Production best practices
- [Advanced Features](./advanced.md) - Advanced configuration options