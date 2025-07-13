# Native Format

`use_native_format` is a new feature added in pretty-loguru v2.1.0+ that allows you to use a format closer to native loguru logging.

## 🎯 Design Goals

- **Seamless Migration**: Maintain format consistency when migrating from loguru to pretty-loguru
- **Developer Friendly**: More intuitive code location using filenames
- **Keep It Simple**: Follow the KISS principle with single parameter format switching

## 🔄 Format Comparison

### Enhanced Format (Default)
```python
from pretty_loguru import create_logger

logger = create_logger("my_service")
logger.info("User login successful")
```
**Output:**
```
2025-06-30 20:15:30 | INFO    12345 | my_service:login:42 - User login successful
```

### Native Format
```python
from pretty_loguru import create_logger

logger = create_logger("my_service", use_native_format=True)
logger.info("User login successful")
```
**Output:**
```
2025-06-30 20:15:30.123 | INFO     | main.py:login:42 - User login successful
```

## 📊 Detailed Differences

| Feature | Enhanced Format | Native Format |
|---------|-----------------|---------------|
| **Display Name** | Custom name | Filename |
| **Time Format** | `HH:mm:ss` | `HH:mm:ss.SSS` (with milliseconds) |
| **Process ID** | ✅ Shown | ❌ Hidden |
| **File Naming** | `[name]_timestamp.log` | `name.log` |
| **Use Cases** | Production, service monitoring | Development debugging, migration |

## 🚀 Use Cases

### 1. Migration from Loguru

If you're originally using loguru:

```python
# Original loguru code
from loguru import logger
logger.info("Application started")
```

Maintain format when migrating to pretty-loguru:

```python
# After migration
from pretty_loguru import create_logger
logger = create_logger("app", use_native_format=True)
logger.info("Application started")
```

### 2. Development Environment Setup

```python
import os

def create_app_logger():
    if os.getenv("ENV") == "development":
        return create_logger(
            "dev_app",
            use_native_format=True,  # Use native format in development
            level="DEBUG"
        )
    else:
        return create_logger(
            "prod_app", 
            use_native_format=False,  # Use enhanced format in production
            level="INFO"
        )
```

### 3. Mixed Usage

```python
# Use both formats simultaneously
debug_logger = create_logger("debug", use_native_format=True)
service_logger = create_logger("service", use_native_format=False) 

debug_logger.debug("Variable check", var="value")      # Native format
service_logger.info("API request processed")           # Enhanced format
```

## 🔧 Configuration Examples

### Basic Configuration

```python
from pretty_loguru import create_logger

# Simplest native format logger
logger = create_logger(use_native_format=True)
```

### Complete Configuration

```python
logger = create_logger(
    name="my_app",
    use_native_format=True,
    log_path="./logs",
    level="DEBUG",
    rotation="10MB",
    retention="7 days"
)
```

### Combining with Presets

```python
logger = create_logger(
    name="api_service",
    use_native_format=True,
    preset="detailed"  # Can be combined with presets
)
```

## 📁 File Naming Differences

### Enhanced Format File Naming
```
logs/
├── [api_service]_20250630-201530.log
├── [user_service]_20250630-201535.log
└── [order_service]_20250630-201540.log
```

### Native Format File Naming
```
logs/
├── api_service.log
├── user_service.log
└── order_service.log
```

## 💡 Best Practices

### 1. Environment Differentiation
```python
def setup_logger(service_name: str, env: str):
    return create_logger(
        name=service_name,
        use_native_format=(env == "development"),
        log_path=f"logs/{env}",
        level="DEBUG" if env == "development" else "INFO"
    )
```

### 2. Team Collaboration
```python
# Provide unified logger factory for team projects
def create_team_logger(name: str, for_development: bool = False):
    return create_logger(
        name=name,
        use_native_format=for_development,
        log_path="logs",
        preset="detailed" if not for_development else None
    )

# Usage
prod_logger = create_team_logger("api")
dev_logger = create_team_logger("api", for_development=True)
```

### 3. Migration Strategy
```python
# Phased migration: maintain native format first, then gradually switch
class LoggerMigration:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.migration_complete = os.getenv("LOGGER_MIGRATION", "false") == "true"
    
    def get_logger(self):
        return create_logger(
            name=self.service_name,
            use_native_format=not self.migration_complete,
            log_path="logs"
        )
```

## ❓ Frequently Asked Questions

### Q: When should I use Native format?
**A:** 
- When migrating from loguru
- During development and debugging phases
- When you need to quickly locate code files
- When you prefer concise file naming

### Q: Can I switch formats dynamically?
**A:** Yes, by recreating the logger:
```python
# Recreate logger with different format
logger = create_logger("app", use_native_format=True, force_new_instance=True)
```

### Q: Does Native format support all features?
**A:** Yes, only the output format differs. All pretty-loguru features are fully supported.

### Q: How to choose the format?
**A:** 
- **Development**: Use Native format for easier debugging
- **Production**: Use Enhanced format for better monitoring
- **Migration**: Use Native format for consistency

## 🔗 Related Documentation

- [Basic Usage](../guide/basic-usage.md) - Understand basic concepts
- [Examples](../examples/) - See practical applications
- [API Documentation](../api/core.md) - Detailed parameter descriptions