# Preset Configuration Examples

pretty-loguru provides multiple preset configurations to help you quickly use the best logging setup for different scenarios. This page demonstrates how to use and customize various preset configurations.

## 🚀 Quick Start

### Basic Preset Configurations

```python
from pretty_loguru import create_logger

# Use the default configuration
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Use the development environment preset
logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)

# Use the production environment preset
logger = create_logger(
    name="production_demo",
    log_path="production_logs",
    level="INFO"
)

# Use the debug preset
logger = create_logger(
    name="debug_demo",
    log_path="debug_logs",
    level="INFO"
)
```

## 🎯 Preset Configuration Types

### 1. Development Environment Configuration (development)

Suitable for local development, with rich visual effects and detailed log information:

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Enable the development environment preset
logger = create_logger(
    name="development_demo",
    log_path="dev_logs",
    level="INFO"
)

def development_demo():
    """Showcase of the development environment configuration"""
    
    logger.ascii_header("DEV MODE", font="slant", border_style="cyan")
    
    logger.debug("Debug info: variable x = 42")
    logger.info("Starting development server...")
    logger.success("Server started successfully, listening on localhost:8000")
    
    logger.block(
        "Development Environment Status",
        [
            "🔧 Debug Mode: Enabled",
            "🌐 Environment: Development", 
            "📝 Log Level: DEBUG",
            "🎨 Visualization: Fully enabled"
        ],
        border_style="cyan"
    )

development_demo()
```

**Features of Development Configuration:**
- Full visualization effects (ASCII art, Rich blocks)
- Detailed debug information
- Colored output
- Dual output to file and console

### 2. Production Environment Configuration (production)

Suitable for production environments, emphasizing performance and conciseness:

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Enable the production environment preset
logger = create_logger(
    name="production_demo",
    log_path="prod_logs",
    level="INFO"
)

def production_demo():
    """Showcase of the production environment configuration"""
    
    logger.info("Application started")
    logger.success("Service started successfully")
    
    logger.block(
        "Service Status",
        [
            "Status: Running",
            "Version: v2.1.0",
            "Instance: prod-server-01"
        ],
        border_style="green"
    )
    
    logger.warning("Memory usage reached 75%")
    logger.error("Database connection timed out")

production_demo()
```

**Features of Production Configuration:**
- Simplified visual effects
- Structured output for important information
- Optimized performance
- Focus on errors and warnings
- Support for log rotation

### 3. Debug Configuration (debug)

Suitable for troubleshooting and in-depth debugging:

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Enable the debug preset
logger = create_logger(
    name="debug_demo",
    log_path="debug_logs",
    level="INFO"
)

def debug_demo():
    """Showcase of the debug configuration"""
    
    logger.ascii_header("DEBUG", font="doom", border_style="yellow")
    
    logger.debug("Entering function: debug_demo()")
    data = {"user_id": 123, "action": "login"}
    logger.debug(f"Processing data: {data}")
    
    logger.block(
        "Debug Information",
        [
            f"🔍 Function: {debug_demo.__name__}",
            f"💾 Memory Usage: 45MB",
            f"⏱️  Execution Time: 0.002s"
        ],
        border_style="yellow"
    )
    
    logger.debug("Function execution complete")

debug_demo()
```

**Features of Debug Configuration:**
- The most detailed log output
- Function tracing and performance monitoring
- Variable state logging

### 4. Testing Configuration (testing)

Suitable for unit and integration testing:

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Enable the testing preset
logger = create_logger(
    name="testing_demo",
    log_path="test_logs",
    level="INFO"
)

def testing_demo():
    """Showcase of the testing configuration"""
    
    logger.ascii_header("TESTING", font="standard", border_style="magenta")
    
    logger.info("Starting test suite execution...")
    
    test_results = {
        "test_login": "PASS",
        "test_logout": "PASS", 
        "test_register": "FAIL"
    }
    
    passed_tests = [f"✅ {name}" for name, res in test_results.items() if res == "PASS"]
    failed_tests = [f"❌ {name}" for name, res in test_results.items() if res == "FAIL"]
    
    if passed_tests:
        logger.block("Passed Tests", passed_tests, border_style="green")
    
    if failed_tests:
        logger.block("Failed Tests", failed_tests, border_style="red", log_level="ERROR")

testing_demo()
```

## 🔧 Custom Preset Configurations

### Creating Your Own Preset

```python
from pretty_loguru import create_logger

def create_custom_preset():
    """Create a custom preset configuration"""
    
    api_preset = {
        "folder": "api_logs",
        "level": "INFO",
        "rotation": "500 MB",
        "retention": "30 days",
        "compression": "zip"
    }
    
    create_logger(**api_preset)
    
    logger.ascii_header("API SERVICE", font="small", border_style="blue")
    logger.info("API service has started")

create_custom_preset()
```

## 💡 Best Practices

### 1. Choose Configuration Based on Environment

```python
import os

def smart_logger_init():
    if os.getenv("DEBUG"):
        logger = create_logger(
    name="debug_demo",
    log_path="debug_logs",
    level="INFO"
)
    elif os.getenv("TESTING"):
        logger = create_logger(
    name="testing_demo",
    log_path="testing_logs",
    level="INFO"
)
    elif os.getenv("PROD"):
        logger = create_logger(
    name="production_demo",
    log_path="production_logs",
    level="INFO"
)
    else:
        logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)

smart_logger_init()
```

### 2. Manage Configuration with Files

```python
import json

def load_config_from_file(config_path="logger_config.json"):
    """Load logging configuration from a file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        create_logger(**config)
        logger.success(f"Loaded configuration from: {config_path}")
    except FileNotFoundError:
        logger.warning(f"Config file {config_path} not found, using default.")
        logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)

load_config_from_file()
```
Preset configurations allow pretty-loguru to quickly adapt to different use cases. Choosing the right preset is key to successfully using the logging system!
