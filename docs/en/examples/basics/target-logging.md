# Target-based Logging

Learn how to send logs to multiple targets simultaneously with different configurations for each destination.

## 🎯 Multi-Target Overview

Target-based logging allows you to send the same log messages to different destinations (console, files, remote services) with unique formatting and filtering for each target.

## 📤 Basic Multi-Target Setup

### Console + File Targets

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
), create_logger

# Initialize base logger
create_logger(level="DEBUG", log_path="logs")

# Target 1: Console (INFO and above, colored)
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Target 2: Debug file (everything)
logger.add(
    "logs/debug.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="20MB"
)

# Target 3: Error file (errors only)
logger.add(
    "logs/errors.log",
    format="{time} | {level} | {name}:{function}:{line} - {message} | {extra}",
    level="ERROR",
    rotation="10MB",
    retention="90 days"
)

# Test different levels
logger.debug("Debug message - only in debug.log")
logger.info("Info message - console + debug.log")
logger.error("Error message - all three targets")
```

### Level-based Target Separation

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Remove default handlers
logger.remove()

# Target 1: Debug console (development)
logger.add(
    sink=lambda msg: print(f"[DEBUG] {msg}", end=""),
    level="DEBUG",
    filter=lambda record: record["level"].name == "DEBUG"
)

# Target 2: Info console (general output)
logger.add(
    sink=lambda msg: print(f"[INFO] {msg}", end=""),
    level="INFO",
    filter=lambda record: record["level"].name in ["INFO", "SUCCESS"]
)

# Target 3: Warning console (attention needed)
logger.add(
    sink=lambda msg: print(f"[WARN] {msg}", end=""),
    level="WARNING",
    filter=lambda record: record["level"].name == "WARNING"
)

# Target 4: Error console (problems)
logger.add(
    sink=lambda msg: print(f"[ERROR] {msg}", end=""),
    level="ERROR",
    filter=lambda record: record["level"].name in ["ERROR", "CRITICAL"]
)

# Test level separation
logger.debug("Debug information")
logger.info("General information")
logger.success("Success message")
logger.warning("Warning message")
logger.error("Error message")
```

## 🏢 Enterprise Multi-Target Setup

### Production Logging Architecture

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
), create_logger
import json
import socket

# Initialize base logger
create_logger(level="INFO", log_path="logs", component_name="api_server")

# Target 1: Application logs (structured JSON)
logger.add(
    "logs/application.json",
    format=lambda record: json.dumps({
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "service": "api_server",
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
        "message": record["message"],
        "extra": record["extra"]
    }),
    level="INFO",
    rotation="50MB",
    retention="30 days"
)

# Target 2: Security audit log
logger.add(
    "logs/security.log",
    format="{time} | SECURITY | {message} | {extra}",
    filter=lambda record: "security" in record["extra"],
    level="INFO",
    rotation="daily",
    retention="365 days"  # Keep security logs longer
)

# Target 3: Performance monitoring
logger.add(
    "logs/performance.log",
    format="{time} | PERF | {message} | duration: {extra[duration]} | {extra}",
    filter=lambda record: "performance" in record["extra"],
    level="INFO",
    rotation="daily"
)

# Target 4: Critical alerts (immediate notification)
def send_alert(message):
    """Send critical alerts to monitoring system"""
    try:
        # Example: Send to monitoring service
        alert_data = {
            "service": "api_server",
            "severity": "critical",
            "message": message,
            "timestamp": "now"
        }
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.sendto(json.dumps(alert_data).encode(), ('monitoring-server', 514))
        print(f"ALERT SENT: {message}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

logger.add(
    send_alert,
    format="{message}",
    level="CRITICAL",
    filter=lambda record: record["level"].name == "CRITICAL"
)

# Usage examples
logger.info("Server started")

# Security logging
logger.bind(security=True, user_id="user123", action="login").info("User authentication successful")

# Performance logging
logger.bind(performance=True, duration=0.245, endpoint="/api/users").info("API request processed")

# Critical alert
logger.critical("Database connection lost - immediate attention required")
```

## 🌐 Remote Target Integration

### Syslog Integration

```python
import socket
import json
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

def syslog_handler(message):
    """Send logs to syslog server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # RFC3164 format: <priority>timestamp hostname tag: message
        syslog_msg = f"<134>{message}"  # 134 = facility 16 (local0) + severity 6 (info)
        sock.sendto(syslog_msg.encode(), ('syslog-server', 514))
        sock.close()
    except Exception as e:
        print(f"Syslog error: {e}")

# Add syslog target
logger.add(
    syslog_handler,
    format="{time:MMM DD HH:mm:ss} api-server pretty-loguru: {level} {message}",
    level="WARNING"  # Only warnings and above to syslog
)

logger.warning("This message goes to syslog")
```

### ELK Stack Integration

```python
import json
import requests
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

def elasticsearch_handler(record):
    """Send logs to Elasticsearch"""
    try:
        doc = {
            "@timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "service": "api_server",
            "module": record["name"],
            "function": record["function"],
            "line": record["line"],
            "message": record["message"],
            "extra": record["extra"]
        }
        
        # Send to Elasticsearch
        response = requests.post(
            'http://elasticsearch:9200/logs/_doc',
            json=doc,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Elasticsearch error: {e}")

# Add Elasticsearch target
logger.add(
    elasticsearch_handler,
    format="{message}",  # We handle formatting in the handler
    level="INFO"
)

logger.info("Log sent to Elasticsearch")
```

## 🔄 Dynamic Target Management

### Runtime Target Configuration

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)
import os
from typing import Dict, Any

class TargetManager:
    def __init__(self):
        self.targets: Dict[str, int] = {}
    
    def add_target(self, name: str, **config) -> bool:
        """Add a new logging target"""
        try:
            handler_id = logger.add(**config)
            self.targets[name] = handler_id
            logger.info(f"Added logging target: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add target {name}: {e}")
            return False
    
    def remove_target(self, name: str) -> bool:
        """Remove a logging target"""
        if name in self.targets:
            try:
                logger.remove(self.targets[name])
                del self.targets[name]
                logger.info(f"Removed logging target: {name}")
                return True
            except Exception as e:
                logger.error(f"Failed to remove target {name}: {e}")
                return False
        return False
    
    def list_targets(self) -> list:
        """List active targets"""
        return list(self.targets.keys())

# Usage
target_manager = TargetManager()

# Add targets based on environment
environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'development':
    target_manager.add_target(
        "dev_console",
        sink=lambda msg: print(f"[DEV] {msg}", end=""),
        level="DEBUG",
        colorize=True
    )

if environment in ['staging', 'production']:
    target_manager.add_target(
        "app_file",
        sink="logs/app.log",
        level="INFO",
        rotation="50MB",
        retention="30 days"
    )
    
    target_manager.add_target(
        "error_file",
        sink="logs/errors.log",
        level="ERROR",
        rotation="10MB"
    )

# Runtime target management
if os.getenv('ENABLE_DEBUG_LOG') == 'true':
    target_manager.add_target(
        "debug_file",
        sink="logs/debug.log",
        level="DEBUG",
        rotation="daily"
    )

logger.info(f"Active targets: {target_manager.list_targets()}")
```

### Configuration-driven Targets

```python
import json
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

def load_logging_config(config_file: str):
    """Load and apply logging configuration from JSON file"""
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Remove existing handlers
    logger.remove()
    
    # Add targets from configuration
    for target_name, target_config in config.get('targets', {}).items():
        try:
            logger.add(**target_config)
            logger.info(f"Configured target: {target_name}")
        except Exception as e:
            print(f"Failed to configure target {target_name}: {e}")

# Example config file (logging_config.json):
config_example = {
    "targets": {
        "console": {
            "sink": "sys.stderr",
            "format": "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
            "level": "INFO",
            "colorize": True
        },
        "application_log": {
            "sink": "logs/app.log",
            "format": "{time} | {level} | {name}:{function}:{line} - {message}",
            "level": "DEBUG",
            "rotation": "50MB",
            "retention": "14 days"
        },
        "error_log": {
            "sink": "logs/errors.log",
            "format": "{time} | {level} | {name}:{function}:{line} - {message} | {extra}",
            "level": "ERROR",
            "rotation": "daily",
            "retention": "90 days"
        }
    }
}

# Save example config
with open('logging_config.json', 'w') as f:
    json.dump(config_example, f, indent=2)

# Load configuration
load_logging_config('logging_config.json')

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## 📊 Target Performance Monitoring

### Measuring Target Performance

```python
import time
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)
from contextlib import contextmanager

class PerformanceTarget:
    def __init__(self, sink, **kwargs):
        self.sink = sink
        self.kwargs = kwargs
        self.message_count = 0
        self.total_time = 0
        
    def __call__(self, message):
        start_time = time.time()
        
        if callable(self.sink):
            result = self.sink(message)
        else:
            # Handle file sinks
            with open(self.sink, 'a') as f:
                f.write(str(message) + '\n')
            result = None
            
        self.total_time += time.time() - start_time
        self.message_count += 1
        
        return result
    
    @property
    def average_time(self):
        return self.total_time / self.message_count if self.message_count > 0 else 0

# Create performance-monitored targets
console_target = PerformanceTarget(lambda msg: print(msg, end=""))
file_target = PerformanceTarget("logs/perf_test.log")

# Add targets
logger.add(console_target, level="INFO")
logger.add(file_target, level="DEBUG")

# Generate test logs
for i in range(100):
    logger.info(f"Test message {i}")

print(f"Console average time: {console_target.average_time:.6f}s")
print(f"File average time: {file_target.average_time:.6f}s")
```

## 🎭 Conditional Target Routing

### Content-based Routing

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# Define routing functions
def route_database_logs(record):
    """Route database-related logs to specific file"""
    return "database" in record["message"].lower() or "db" in record.get("extra", {})

def route_api_logs(record):
    """Route API-related logs to specific file"""
    return "api" in record["message"].lower() or "endpoint" in record.get("extra", {})

def route_security_logs(record):
    """Route security-related logs to specific file"""
    return any(keyword in record["message"].lower() for keyword in ["auth", "login", "security", "unauthorized"])

# Add conditional targets
logger.add(
    "logs/database.log",
    filter=route_database_logs,
    level="DEBUG",
    rotation="daily"
)

logger.add(
    "logs/api.log",
    filter=route_api_logs,
    level="INFO",
    rotation="50MB"
)

logger.add(
    "logs/security.log",
    filter=route_security_logs,
    level="WARNING",
    rotation="daily",
    retention="365 days"
)

# Test routing
logger.info("Database connection established")  # → database.log
logger.info("API endpoint /users called")       # → api.log
logger.warning("Unauthorized access attempt")   # → security.log
logger.info("General application message")      # → general log (if configured)
```

Target-based logging provides maximum flexibility for complex applications requiring sophisticated log management strategies!