# Configuration Templates

pretty-loguru provides reusable `LoggerConfig` templates that help you create consistent loggers and (optionally) keep a group of loggers synchronized when you update the config.

## 🎯 Core Features

### Reusable Configuration Templates
- One configuration can be applied to multiple loggers
- Configuration changes automatically update all attached loggers
- Support for configuration inheritance and cloning

### Elegant API Design
- Chain method calls support
- Intuitive method naming
- Avoids verbose manager patterns

## 🚀 Quick Start

### Basic Usage

```python
from pretty_loguru import LoggerConfig, create_logger

# 1. Create a configuration template
config = LoggerConfig(
    level="INFO",
    log_dir="logs/app",
    rotation="daily",
    retention="30 days"
)

# 2. Create loggers using the same template
api_logger = create_logger("api", config=config)
db_logger = create_logger("database", config=config)
cache_logger = create_logger("cache", config=config)

# 3. Attach loggers to the config (so future updates are synchronized)
config.apply_to("api", "database", "cache")

# 4. Update configuration - all attached loggers are updated automatically
config.update(level="DEBUG", rotation="100 MB")

# Now all loggers use the new configuration
api_logger.debug("Now you can see DEBUG messages")
```

### Using Preset Templates

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

# Development environment
dev_config = ConfigTemplates.development()
dev_logger = create_logger("dev_app", config=dev_config)
dev_config.apply_to("dev_app")

# Production environment
prod_config = ConfigTemplates.production()
prod_logger = create_logger("prod_app", config=prod_config)
prod_config.apply_to("prod_app")

# Custom template
test_config = ConfigTemplates.testing().update(level="ERROR")
test_logger = create_logger("test_app", config=test_config)
test_config.apply_to("test_app")
```

## 🔧 Advanced Features

### Configuration Inheritance

```python
# Base configuration
base_config = LoggerConfig(
    level="INFO",
    rotation="daily",
    retention="30 days"
)

# API service inherits base configuration
api_config = LoggerConfig().inherit_from(
    base_config,
    log_dir="logs/api",
    component_name="api_service"
)

# Database service has special requirements
db_config = LoggerConfig().inherit_from(
    base_config,
    log_dir="logs/database",
    level="DEBUG"  # Needs more detailed logs
)
```

### Configuration Cloning

```python
# Clone production config for testing
prod_config = ConfigTemplates.production()
test_config = prod_config.clone(
    log_dir="logs/test",
    level="DEBUG",
    compression=None
)
```

### Method Chaining

```python
# Note: apply_to() creates missing loggers by default. Use create_if_missing=False to require existing.
from pretty_loguru import create_logger

chained_config = ConfigTemplates.production().update(level="DEBUG", retention="7 days")
create_logger("chained_app", config=chained_config)
logger = chained_config.apply_to("chained_app")
```

### Dynamic Configuration Updates

```python
from pretty_loguru import create_logger

config = LoggerConfig(level="INFO", log_dir="logs/services")
create_logger("service1", config=config)
create_logger("service2", config=config)
create_logger("service3", config=config)
loggers = config.apply_to("service1", "service2", "service3")

# Later in the application...
if debug_mode:
    config.update(level="DEBUG")  # All 3 loggers now log DEBUG
```

## 📋 Configuration Options

### Common Parameters

```python
config = LoggerConfig(
    # Basics
    level="INFO",
    use_native_format=False,

    # File output (log_dir is a directory)
    log_dir="logs",
    subdirectory="my_service",   # optional: put files under logs/my_service/
    rotation="daily",
    retention="30 days",
    compression="gz",
    compression_format=None,     # optional: custom compression naming/format

    # Formatting / identification
    format=None,
    component_name="my_service",
    preset=None,                # e.g. "minimal", "simple", "detailed"

    # Cleaner
    start_cleaner=True,
    cleaner_include_patterns=["*.log", "*.log.*"],
    cleaner_exclude_patterns=["*.lock"],
    verbose=False,

    # Validation & structured logs
    strict_validation=True,
    serialize=False,            # JSON file logs for ELK/Filebeat/Promtail

    # Optional Loki direct push
    loki_enabled=False,
    loki_base_url="http://localhost:3100",
    loki_labels={"app": "my_service"},
)
```

## 🎨 Configuration Templates

### Built-in Templates

```python
# Development - Detailed logs, no compression
dev_config = ConfigTemplates.development()
# level="DEBUG", rotation="10 MB", retention="7 days"

# Production - Optimized for performance
prod_config = ConfigTemplates.production()
# level="INFO", rotation="50 MB", retention="30 days", compression="zip"

# Testing - Minimal output
test_config = ConfigTemplates.testing()
# level="WARNING", rotation="5 MB", retention="3 days"

# Performance - higher thresholds / larger rotation
perf_config = ConfigTemplates.performance()
# level="ERROR", rotation="500 MB"
```

### Rotation Templates

```python
# Daily rotation at midnight
daily = ConfigTemplates.daily()

# Hourly rotation
hourly = ConfigTemplates.hourly()

# Weekly rotation on Monday
weekly = ConfigTemplates.weekly()

# Monthly rotation
monthly = ConfigTemplates.monthly()
```

## 🚀 Real-World Examples

### Microservices Configuration

```python
from pretty_loguru import LoggerConfig, create_logger

# Shared configuration for all microservices
base_config = LoggerConfig(
    level="INFO",
    rotation="100 MB",
    retention="30 days",
    compression="gz"
)

# Service-specific configurations
services = {
    "auth": base_config.clone(log_dir="logs/auth", component_name="auth-service"),
    "api": base_config.clone(log_dir="logs/api", component_name="api-gateway"),
    "worker": base_config.clone(log_dir="logs/worker", level="DEBUG")
}

# Create + attach all service loggers
loggers = {}
for name, service_config in services.items():
    create_logger(name, config=service_config)
    loggers[name] = service_config.apply_to(name)
```

### Environment-Based Configuration

```python
import os

def get_logger_config():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ConfigTemplates.production()
    elif env == "staging":
        return ConfigTemplates.production().update(level="DEBUG")
    else:
        return ConfigTemplates.development()

# Use environment-based config
config = get_logger_config()
from pretty_loguru import create_logger

create_logger("app", config=config)
logger = config.apply_to("app")
```

### Dynamic Reconfiguration

```python
class LoggerManager:
    def __init__(self):
        self.config = LoggerConfig(level="INFO", log_dir="logs/app")
        self.loggers = {}
    
    def get_logger(self, name: str):
        if name not in self.loggers:
            create_logger(name, config=self.config)
            self.loggers[name] = self.config.apply_to(name)
        return self.loggers[name]
    
    def set_debug_mode(self, enabled: bool):
        level = "DEBUG" if enabled else "INFO"
        self.config.update(level=level)

# Usage
manager = LoggerManager()
api_logger = manager.get_logger("api")
db_logger = manager.get_logger("database")

# Enable debug for all loggers
manager.set_debug_mode(True)
```

## 🔍 Best Practices

1. **Use Templates**: Start with built-in templates rather than manual configuration
2. **Share Configurations**: Create one config for multiple related loggers
3. **Clone for Variations**: Use `clone()` when you need slight variations
4. **Update Dynamically**: Leverage `update()` for runtime configuration changes
5. **Use Inheritance**: Build complex configs from simple base configurations

## 🔗 Related Resources

- [Basic Configuration](./custom-config.md) - Traditional configuration methods
- [API Reference](../api/#configuration-templates) - Complete API documentation
- [Examples](../examples/configuration.md) - More configuration examples
