# Enterprise Application Examples

Demonstrating best practices for deploying Pretty-Loguru in enterprise environments, including microservices architecture, security, compliance, and large-scale log management.

## Microservices Architecture

Unified log management in microservices environments:

```python
from pretty_loguru import create_logger, LoggerConfig
import os
import socket
from typing import Optional
import uuid

class MicroserviceLogger:
    """Logger for microservices"""
    
    def __init__(
        self,
        service_name: str,
        service_version: str,
        environment: str = "production"
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.instance_id = self._generate_instance_id()
        
        # Create configuration
        config = LoggerConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            log_path=f"logs/{service_name}",
            rotation="100 MB",
            retention="30 days",
            compression="zip"
        )
        
        # Create logger
        self.logger = create_logger(service_name, config=config)
        
        # Bind service information
        self.logger = self.logger.bind(
            service=service_name,
            version=service_version,
            environment=environment,
            instance_id=self.instance_id,
            hostname=socket.gethostname()
        )
    
    def _generate_instance_id(self) -> str:
        """Generate unique instance ID"""
        return f"{self.service_name}-{uuid.uuid4().hex[:8]}"
    
    def log_request(self, request_id: str, method: str, path: str):
        """Log request"""
        return self.logger.bind(
            request_id=request_id,
            method=method,
            path=path
        )
    
    def log_response(self, request_id: str, status_code: int, duration: float):
        """Log response"""
        self.logger.bind(request_id=request_id).info(
            f"Response: {status_code} ({duration:.3f}s)",
            status_code=status_code,
            duration=duration
        )
    
    def log_inter_service_call(
        self,
        target_service: str,
        operation: str,
        request_id: str
    ):
        """Log inter-service calls"""
        self.logger.bind(
            request_id=request_id,
            target_service=target_service,
            operation=operation
        ).info(f"Calling {target_service}.{operation}")

# Usage example
# User service
user_service = MicroserviceLogger(
    service_name="user-service",
    service_version="1.2.0",
    environment="production"
)

# Order service
order_service = MicroserviceLogger(
    service_name="order-service",
    service_version="2.1.0",
    environment="production"
)

# Log inter-service communication
request_id = str(uuid.uuid4())
user_service.log_inter_service_call(
    target_service="order-service",
    operation="create_order",
    request_id=request_id
)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/08_enterprise/microservices.py)

## Security and Compliance

Implementing security and compliance requirements:

```python
from pretty_loguru import create_logger, LoggerConfig
import hashlib
import re
from typing import Any, Dict
import json

class SecureLogger:
    """Logger with security and compliance features"""
    
    # Sensitive data patterns
    SENSITIVE_PATTERNS = {
        "credit_card": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "api_key": r"api[_\-]?key[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-]+)",
        "password": r"password[\"']?\s*[:=]\s*[\"']?([^\"'\s]+)"
    }
    
    def __init__(self, name: str, compliance_mode: str = "PCI"):
        config = LoggerConfig(
            level="INFO",
            log_path=f"logs/secure/{name}",
            rotation="50 MB",
            retention="90 days",  # Compliance requirement
            compression="zip"
        )
        
        self.logger = create_logger(name, config=config)
        self.compliance_mode = compliance_mode
        
        # Add secure file handler
        self.logger.add(
            f"logs/secure/{name}_audit.log",
            format=self._audit_formatter,
            filter=self._compliance_filter,
            rotation="1 day",
            retention="7 years",  # Long-term retention for audit
            compression="zip"
        )
    
    def _mask_sensitive_data(self, message: str) -> str:
        """Mask sensitive data in messages"""
        masked_message = message
        
        for data_type, pattern in self.SENSITIVE_PATTERNS.items():
            if data_type == "credit_card":
                # Keep first 4 and last 4 digits
                masked_message = re.sub(
                    pattern,
                    lambda m: m.group()[:4] + "*" * 8 + m.group()[-4:],
                    masked_message
                )
            else:
                # Completely mask other sensitive data
                masked_message = re.sub(
                    pattern,
                    f"[REDACTED-{data_type.upper()}]",
                    masked_message
                )
        
        return masked_message
    
    def _audit_formatter(self, record: Dict[str, Any]) -> str:
        """Format logs for audit trail"""
        audit_entry = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "user": record.get("extra", {}).get("user_id", "system"),
            "action": record.get("extra", {}).get("action", "unknown"),
            "resource": record.get("extra", {}).get("resource", ""),
            "result": record.get("extra", {}).get("result", ""),
            "ip_address": record.get("extra", {}).get("ip_address", ""),
            "message": self._mask_sensitive_data(record["message"]),
            "hash": ""  # Will be filled below
        }
        
        # Create tamper-proof hash
        content = json.dumps(audit_entry, sort_keys=True)
        audit_entry["hash"] = hashlib.sha256(content.encode()).hexdigest()
        
        return json.dumps(audit_entry) + "\n"
    
    def _compliance_filter(self, record: Dict[str, Any]) -> bool:
        """Filter logs based on compliance requirements"""
        # Always log security events
        if record.get("extra", {}).get("security_event", False):
            return True
        
        # Log based on compliance mode
        if self.compliance_mode == "PCI":
            # PCI DSS requires logging of access to cardholder data
            return record.get("extra", {}).get("cardholder_data_access", False)
        elif self.compliance_mode == "HIPAA":
            # HIPAA requires logging of PHI access
            return record.get("extra", {}).get("phi_access", False)
        
        return record["level"].no >= 20  # INFO and above

    def log_security_event(
        self,
        event_type: str,
        user_id: str,
        resource: str,
        action: str,
        result: str,
        ip_address: str,
        details: Optional[Dict] = None
    ):
        """Log security event with full context"""
        self.logger.bind(
            security_event=True,
            user_id=user_id,
            resource=resource,
            action=action,
            result=result,
            ip_address=ip_address,
            event_type=event_type,
            details=details or {}
        ).info(
            f"Security event: {event_type} - {action} on {resource} by {user_id}"
        )

# Usage
secure_logger = SecureLogger("payment-service", compliance_mode="PCI")

# Log security events
secure_logger.log_security_event(
    event_type="authentication",
    user_id="user123",
    resource="/api/login",
    action="login_attempt",
    result="success",
    ip_address="192.168.1.100"
)

# Sensitive data is automatically masked
secure_logger.logger.info(
    "Processing payment with card 4111-1111-1111-1234"
)  # Logs as: "Processing payment with card 4111********1234"
```

## Centralized Log Management

Integration with centralized logging systems:

```python
from pretty_loguru import create_logger
import json
from typing import Dict, Any
from dataclasses import dataclass
import requests

@dataclass
class LogShipper:
    """Ship logs to centralized system (ELK, Splunk, etc.)"""
    
    def __init__(
        self,
        service_name: str,
        log_endpoint: str,
        api_key: str,
        batch_size: int = 100
    ):
        self.service_name = service_name
        self.log_endpoint = log_endpoint
        self.api_key = api_key
        self.batch_size = batch_size
        self.buffer = []
        
        # Create logger with custom sink
        self.logger = create_logger(service_name)
        self.logger.add(
            self._ship_logs,
            format=self._format_for_shipping,
            level="INFO"
        )
    
    def _format_for_shipping(self, record: Dict[str, Any]) -> str:
        """Format logs for centralized system"""
        log_entry = {
            "@timestamp": record["time"].isoformat(),
            "service": self.service_name,
            "level": record["level"].name,
            "message": record["message"],
            "logger": record["name"],
            "thread": record["thread"].name,
            "process": record["process"].name,
            
            # Add trace context
            "trace": {
                "file": record["file"].path,
                "function": record["function"],
                "line": record["line"]
            },
            
            # Add custom fields
            **record.get("extra", {})
        }
        
        # Add exception if present
        if record["exception"]:
            log_entry["exception"] = {
                "type": record["exception"].type.__name__,
                "message": str(record["exception"].value),
                "stacktrace": record["exception"].traceback
            }
        
        return json.dumps(log_entry)
    
    def _ship_logs(self, message: str):
        """Ship logs to centralized system"""
        self.buffer.append(message.strip())
        
        # Ship when buffer is full
        if len(self.buffer) >= self.batch_size:
            self._flush_buffer()
    
    def _flush_buffer(self):
        """Send buffered logs to centralized system"""
        if not self.buffer:
            return
        
        try:
            response = requests.post(
                self.log_endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"logs": self.buffer},
                timeout=30
            )
            response.raise_for_status()
            self.buffer.clear()
        except Exception as e:
            # Fallback to local file if shipping fails
            with open(f"logs/failed_shipments/{self.service_name}.log", "a") as f:
                for log in self.buffer:
                    f.write(log + "\n")
            self.buffer.clear()

# Usage
log_shipper = LogShipper(
    service_name="api-gateway",
    log_endpoint="https://logs.company.com/ingest",
    api_key="your-api-key"
)

# Logs are automatically shipped
log_shipper.logger.info(
    "Request processed",
    request_id="req-123",
    duration=0.125,
    status_code=200
)
```

## Performance Monitoring

Enterprise-grade performance monitoring:

```python
from pretty_loguru import create_logger
import time
import psutil
import threading
from contextlib import contextmanager
from typing import Optional, Dict, Any
import statistics

class PerformanceLogger:
    """Logger with built-in performance monitoring"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = create_logger(service_name)
        self.metrics = {
            "response_times": [],
            "memory_usage": [],
            "cpu_usage": []
        }
        
        # Start background monitoring
        self._start_monitoring()
    
    def _start_monitoring(self):
        """Start background system monitoring"""
        def monitor():
            while True:
                # Monitor system resources
                self.metrics["memory_usage"].append(psutil.virtual_memory().percent)
                self.metrics["cpu_usage"].append(psutil.cpu_percent(interval=1))
                
                # Keep only last 1000 measurements
                for key in self.metrics:
                    if len(self.metrics[key]) > 1000:
                        self.metrics[key] = self.metrics[key][-1000:]
                
                time.sleep(10)  # Monitor every 10 seconds
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    @contextmanager
    def measure_performance(
        self,
        operation: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Context manager to measure operation performance"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            yield
        finally:
            duration = time.time() - start_time
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_delta = end_memory - start_memory
            
            # Record metrics
            self.metrics["response_times"].append(duration)
            
            # Log performance data
            self.logger.bind(
                operation=operation,
                duration=duration,
                memory_delta=memory_delta,
                **(metadata or {})
            ).info(
                f"Operation '{operation}' completed in {duration:.3f}s "
                f"(Memory Δ: {memory_delta:+.2f}MB)"
            )
            
            # Alert on slow operations
            if duration > 1.0:  # Threshold: 1 second
                self.logger.warning(
                    f"Slow operation detected: {operation} took {duration:.3f}s"
                )
    
    def log_performance_summary(self):
        """Log performance summary statistics"""
        if self.metrics["response_times"]:
            response_stats = {
                "count": len(self.metrics["response_times"]),
                "mean": statistics.mean(self.metrics["response_times"]),
                "median": statistics.median(self.metrics["response_times"]),
                "p95": statistics.quantiles(
                    self.metrics["response_times"], n=20
                )[18],  # 95th percentile
                "max": max(self.metrics["response_times"])
            }
        else:
            response_stats = {"message": "No response time data"}
        
        self.logger.info(
            "Performance Summary",
            response_times=response_stats,
            avg_memory_usage=statistics.mean(self.metrics["memory_usage"])
                            if self.metrics["memory_usage"] else 0,
            avg_cpu_usage=statistics.mean(self.metrics["cpu_usage"])
                         if self.metrics["cpu_usage"] else 0
        )

# Usage
perf_logger = PerformanceLogger("data-processor")

# Measure operation performance
with perf_logger.measure_performance("process_batch", {"batch_size": 1000}):
    # Simulate processing
    time.sleep(0.5)
    # Process data...

# Log performance summary
perf_logger.log_performance_summary()
```

## High Availability Setup

Configuration for high availability:

```python
from pretty_loguru import create_logger, LoggerConfig
import os
from typing import List, Optional
import socket

class HALogger:
    """High Availability Logger with failover support"""
    
    def __init__(
        self,
        service_name: str,
        primary_path: str,
        backup_paths: List[str],
        sync_to_standby: bool = True
    ):
        self.service_name = service_name
        self.primary_path = primary_path
        self.backup_paths = backup_paths
        self.sync_to_standby = sync_to_standby
        
        # Primary logger configuration
        config = LoggerConfig(
            level="INFO",
            log_path=primary_path,
            rotation="100 MB",
            retention="30 days",
            compression="zip"
        )
        
        self.logger = create_logger(service_name, config=config)
        
        # Add backup handlers
        for backup_path in backup_paths:
            self._add_backup_handler(backup_path)
        
        # Add network replication if enabled
        if sync_to_standby:
            self._setup_replication()
    
    def _add_backup_handler(self, backup_path: str):
        """Add backup log handler"""
        try:
            # Test if path is accessible
            os.makedirs(backup_path, exist_ok=True)
            
            self.logger.add(
                f"{backup_path}/{self.service_name}.log",
                rotation="100 MB",
                retention="7 days",
                enqueue=True,  # Async to prevent blocking
                catch=True     # Don't fail if backup fails
            )
        except Exception as e:
            self.logger.warning(f"Failed to add backup handler: {backup_path}")
    
    def _setup_replication(self):
        """Setup log replication to standby servers"""
        standby_servers = os.getenv("STANDBY_SERVERS", "").split(",")
        
        for server in standby_servers:
            if server:
                self.logger.add(
                    lambda msg: self._replicate_to_standby(msg, server),
                    enqueue=True,
                    catch=True
                )
    
    def _replicate_to_standby(self, message: str, server: str):
        """Replicate log message to standby server"""
        try:
            # Simple TCP replication (in production, use proper protocol)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                host, port = server.split(":")
                s.connect((host, int(port)))
                s.sendall(message.encode())
        except Exception:
            # Silently fail - don't block on replication
            pass

# Usage
ha_logger = HALogger(
    service_name="critical-service",
    primary_path="/var/log/primary",
    backup_paths=[
        "/mnt/backup1/logs",
        "/mnt/backup2/logs",
        "/nfs/shared/logs"
    ],
    sync_to_standby=True
)

ha_logger.logger.info("Critical operation completed")
```

## Next Steps

- [Production Deployment](./production.md) - Production deployment guide
- [API Reference](../api/) - Complete API documentation
- [Performance Guide](../guide/performance.md) - Performance optimization