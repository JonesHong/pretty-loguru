# Enhanced Configuration Management

pretty-loguru provides a powerful enhanced configuration system that allows you to create reusable configuration templates and elegantly manage multiple loggers.

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
from pretty_loguru import EnhancedLoggerConfig

# 1. Create configuration template
config = EnhancedLoggerConfig(
    level="INFO",
    log_path="logs/app",
    rotation="daily",
    retention="30 days"
)

# 2. Apply to multiple loggers
api_logger = config.apply_to("api")
db_logger, cache_logger = config.apply_to("database", "cache")

# 3. Update configuration - all loggers automatically updated
config.update(level="DEBUG", rotation="100 MB")

# Now all loggers use the new configuration
api_logger.debug("Now you can see DEBUG messages")
```

### Using Preset Templates

```python
from pretty_loguru import ConfigTemplates

# Development environment
dev_logger = ConfigTemplates.development().apply_to("dev_app")

# Production environment
prod_logger = ConfigTemplates.production().apply_to("prod_app")

# Custom template
test_logger = ConfigTemplates.testing().update(level="ERROR").apply_to("test_app")
```

## 🔧 Advanced Features

### Configuration Inheritance

```python
# Base configuration
base_config = EnhancedLoggerConfig(
    level="INFO",
    rotation="daily",
    retention="30 days"
)

# API service inherits base configuration
api_config = EnhancedLoggerConfig().inherit_from(
    base_config,
    log_path="logs/api",
    component_name="api_service"
)

# Database service has special requirements
db_config = EnhancedLoggerConfig().inherit_from(
    base_config,
    log_path="logs/database",
    level="DEBUG"  # Needs more detailed logs
)
```

### Configuration Cloning

```python
# Clone production config for testing
prod_config = ConfigTemplates.production()
test_config = prod_config.clone(
    log_path="logs/test",
    level="DEBUG",
    compression=None
)
```

### Method Chaining

```python
# Elegant chain operations
logger = (
    EnhancedLoggerConfig()
    .inherit_from(ConfigTemplates.production())
    .update(level="DEBUG", retention="7 days")
    .enable_proxy()
    .apply_to("chained_app")
)
```

### Dynamic Configuration Updates

```python
config = EnhancedLoggerConfig(level="INFO")
loggers = config.apply_to("service1", "service2", "service3")

# Later in the application...
if debug_mode:
    config.update(level="DEBUG")  # All 3 loggers now log DEBUG

if performance_issues:
    config.enable_proxy()  # All loggers switch to proxy mode
```

## 📋 Configuration Options

### Complete Parameter List

```python
config = EnhancedLoggerConfig(
    # Basic configuration
    level="INFO",                    # Log level
    use_native_format=False,         # Use loguru native format
    
    # File output configuration
    log_path="logs",                 # Log directory
    rotation="daily",                # Rotation strategy
    retention="30 days",             # Retention policy
    compression="zip",               # Compression format
    
    # Format configuration
    logger_format=None,              # Custom format string
    component_name=None,             # Component identifier
    subdirectory=None,               # Subdirectory organization
    
    # Behavior control
    start_cleaner=True,              # Auto-cleanup old logs
    proxy_mode=False,                # Proxy mode for performance
    
    # Advanced options
    enqueue=False,                   # Async logging
    serialize=False,                 # JSON serialization
    backtrace=True,                  # Error backtrace
    diagnose=True,                   # Diagnostic info
    catch=True                       # Auto catch exceptions
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

# Performance - Proxy mode enabled
perf_config = ConfigTemplates.performance()
# level="ERROR", proxy_mode=True, rotation="100 MB"
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
# Shared configuration for all microservices
base_config = EnhancedLoggerConfig(
    level="INFO",
    rotation="100 MB",
    retention="30 days",
    compression="gz"
)

# Service-specific configurations
services = {
    "auth": base_config.clone(log_path="logs/auth", component_name="auth-service"),
    "api": base_config.clone(log_path="logs/api", component_name="api-gateway"),
    "worker": base_config.clone(log_path="logs/worker", level="DEBUG")
}

# Create all service loggers
loggers = {
    name: config.apply_to(name)
    for name, config in services.items()
}
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
logger = config.apply_to("app")
```

### Dynamic Reconfiguration

```python
class LoggerManager:
    def __init__(self):
        self.config = EnhancedLoggerConfig(level="INFO")
        self.loggers = {}
    
    def get_logger(self, name: str):
        if name not in self.loggers:
            self.loggers[name] = self.config.apply_to(name)
        return self.loggers[name]
    
    def set_debug_mode(self, enabled: bool):
        level = "DEBUG" if enabled else "INFO"
        self.config.update(level=level)
    
    def enable_performance_mode(self):
        self.config.enable_proxy()
        self.config.update(level="WARNING")

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