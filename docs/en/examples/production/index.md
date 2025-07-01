# Production Environment Examples

Using pretty-loguru in a production environment requires special consideration for performance, reliability, and maintainability. This page demonstrates how to optimize the configuration and use of pretty-loguru in a production environment.

## 🏭 Production Environment Configuration

### Basic Production Configuration

```python
from pretty_loguru import create_logger
import os
from pathlib import Path

def setup_production_logging():
    """Set up logging configuration for a production environment"""
    
    # Create log directory
    log_dir = Path("/var/log/myapp")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Production environment configuration
    logger_start(
        preset="production",
        folder=str(log_dir),
        file_name="app_{time:YYYY-MM-DD}.log",
        level="INFO",
        rotation="100 MB",      // Rotate automatically at 100MB
        retention="30 days",    // Keep for 30 days
        compression="gz",       // Compress old logs
        backtrace=False,        // Disable backtrace in production
        diagnose=False          // Disable diagnose mode
    )
    
    logger.ascii_header("PRODUCTION", font="standard", border_style="blue")
    
    logger.block(
        "Production Logging System Started",
        [
            f"📁 Log Directory: {log_dir}",
            f"📊 Log Level: INFO",
            f"🔄 Rotation Size: 100 MB",
            f"📅 Retention Period: 30 days",
            f"🗜️  Compression Format: gzip",
            f"🔒 Secure Mode: Enabled"
        ],
        border_style="green",
        log_level="SUCCESS"
    )

setup_production_logging()
```

### Environment-Aware Configuration

```python
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

def get_environment() -> Environment:
    """Get the current environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    try:
        return Environment(env)
    except ValueError:
        return Environment.DEVELOPMENT

def setup_environment_logging():
    """Set up logging based on the environment"""
    
    env = get_environment()
    
    configs = {
        Environment.DEVELOPMENT: {"preset": "development", "folder": "dev_logs", "level": "DEBUG"},
        Environment.STAGING: {"preset": "production", "folder": "/var/log/myapp/staging", "level": "INFO"},
        Environment.PRODUCTION: {"preset": "production", "folder": "/var/log/myapp/production", "level": "WARNING"}
    }
    
    config = configs[env]
    logger_start(**config)
    
    logger.ascii_block(
        f"Environment Configuration Loaded",
        [
            f"🌍 Environment: {env.value.upper()}",
            f"📁 Log Path: {config['folder']}",
            f"📊 Log Level: {config['level']}"
        ],
        ascii_header=env.value.upper(),
        border_style="cyan"
    )

setup_environment_logging()
```

## 🔐 Security Considerations

### Filtering Sensitive Information

```python
import re

class SecureLogger:
    """Secure Logger"""
    
    SENSITIVE_PATTERNS = {
        'password': re.compile(r'"password":\s*".*?"', re.IGNORECASE),
        'token': re.compile(r'"token":\s*".*?"', re.IGNORECASE),
    }
    
    def sanitize_string(self, text: str) -> str:
        """Sanitize sensitive information in a string"""
        for pattern_name, pattern in self.SENSITIVE_PATTERNS.items():
            text = pattern.sub(f'"{pattern_name}": "***"', text)
        return text
    
    def secure_log(self, level: str, message: str, data: dict = None):
        """Log securely"""
        clean_message = self.sanitize_string(message)
        
        clean_data_str = ""
        if data:
            import json
            clean_data_str = self.sanitize_string(json.dumps(data))
        
        getattr(logger, level)(f"{clean_message} | Data: {clean_data_str}")

secure_logger = SecureLogger()

def login_attempt(username: str, password: str):
    """Log a login attempt"""
    login_data = {"username": username, "password": password}
    secure_logger.secure_log("info", f"User login attempt: {username}", login_data)

login_attempt("john_doe", "secret123")
```

This complete production environment example demonstrates how to use pretty-loguru in a real product, including best practices for performance optimization, security, monitoring, and maintenance!
