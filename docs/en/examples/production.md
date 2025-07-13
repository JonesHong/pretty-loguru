# Production Environment Examples

Demonstrating best practices for deploying Pretty-Loguru in production environments, including performance monitoring, error tracking, and log management.

## Environment Configuration Management

Using different log configurations for different environments:

```python
import os
from pretty_loguru import create_logger, ConfigTemplates, LoggerConfig

def get_environment_config() -> LoggerConfig:
    """Get configuration based on environment variables"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    configs = {
        "development": ConfigTemplates.development(),
        "testing": ConfigTemplates.testing(),
        "staging": LoggerConfig(
            level="INFO",
            log_path="logs/staging",
            rotation="100 MB",
            retention="14 days",
            compression="zip"
        ),
        "production": ConfigTemplates.production()
    }
    
    config = configs.get(env, ConfigTemplates.development())
    
    # Environment-specific overrides
    if env == "production":
        # Use JSON format in production for log aggregation
        config.logger_format = '{"time":"{time}", "level":"{level}", "message":"{message}"}'
    
    return config

# Use environment configuration
config = get_environment_config()
logger = create_logger("app", config=config)

# Log environment info
logger.info(f"Application started in {os.getenv('ENVIRONMENT', 'development')} mode")
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/06_production/deployment_logging.py)

## Performance Monitoring

Monitor application performance and log metrics:

```python
from pretty_loguru import create_logger
import time
import psutil
import asyncio
from functools import wraps

logger = create_logger("performance", log_path="logs/metrics")

def monitor_performance(func):
    """Performance monitoring decorator"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = await func(*args, **kwargs)
            status = "success"
        except Exception as e:
            result = None
            status = "error"
            raise
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            duration = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Log performance metrics
            logger.info(
                f"Performance metrics",
                function=func.__name__,
                duration=f"{duration:.3f}s",
                memory_start=f"{start_memory:.1f}MB",
                memory_end=f"{end_memory:.1f}MB",
                memory_delta=f"{memory_delta:+.1f}MB",
                status=status
            )
            
            # Warning: slow operation
            if duration > 1.0:
                logger.warning(f"Slow operation detected: {func.__name__} took {duration:.3f}s")
            
            # Warning: high memory usage
            if memory_delta > 100:
                logger.warning(f"High memory usage: {func.__name__} used {memory_delta:.1f}MB")
        
        return result
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        # Similar implementation for sync functions
        pass
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

# Usage example
@monitor_performance
async def process_large_dataset(data):
    """Process large dataset with monitoring"""
    logger.info(f"Processing {len(data)} records")
    # Simulate processing
    await asyncio.sleep(2)
    return {"processed": len(data)}
```

## Error Tracking

Comprehensive error tracking and reporting:

```python
from pretty_loguru import create_logger
import traceback
import sys
from typing import Optional, Dict, Any
import hashlib

class ErrorTracker:
    """Production error tracking system"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = create_logger(
            f"{service_name}_errors",
            log_path=f"logs/errors/{service_name}",
            level="WARNING"
        )
        
        # Error statistics
        self.error_counts = {}
        
        # Add error-specific handler
        self.logger.add(
            f"logs/errors/{service_name}_critical.log",
            level="ERROR",
            rotation="10 MB",
            retention="90 days",
            backtrace=True,
            diagnose=True
        )
    
    def track_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None
    ):
        """Track and log error with context"""
        error_type = type(error).__name__
        error_hash = self._generate_error_hash(error)
        
        # Update error statistics
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Create detailed error report
        error_report = {
            "error_type": error_type,
            "error_message": str(error),
            "error_hash": error_hash,
            "occurrence_count": self.error_counts[error_type],
            "user_id": user_id,
            "request_id": request_id,
            "context": context or {},
            "traceback": traceback.format_exc()
        }
        
        # Log based on severity
        if isinstance(error, (SystemExit, KeyboardInterrupt)):
            self.logger.critical(
                f"Critical error: {error_type}",
                **error_report
            )
        elif isinstance(error, (MemoryError, RecursionError)):
            self.logger.error(
                f"Resource error: {error_type}",
                **error_report
            )
            self._alert_operations_team(error_report)
        else:
            self.logger.error(
                f"Application error: {error_type}",
                **error_report
            )
        
        # Visual error report for console
        if self.error_counts[error_type] == 1:
            # First occurrence
            self.logger.console_block(
                f"🆕 New Error Type: {error_type}",
                [
                    f"Message: {str(error)}",
                    f"Hash: {error_hash[:8]}...",
                    f"User: {user_id or 'Unknown'}",
                    f"Request: {request_id or 'None'}"
                ],
                border_style="red"
            )
        elif self.error_counts[error_type] % 10 == 0:
            # Every 10th occurrence
            self.logger.console_panel(
                f"⚠️ Recurring Error: {error_type}\n"
                f"Occurrences: {self.error_counts[error_type]}",
                title="Error Pattern Detected",
                border_style="yellow"
            )
    
    def _generate_error_hash(self, error: Exception) -> str:
        """Generate unique hash for error type"""
        tb = traceback.extract_tb(error.__traceback__)
        if tb:
            # Hash based on error type and location
            key = f"{type(error).__name__}:{tb[-1].filename}:{tb[-1].lineno}"
        else:
            key = f"{type(error).__name__}:{str(error)}"
        
        return hashlib.md5(key.encode()).hexdigest()
    
    def _alert_operations_team(self, error_report: Dict[str, Any]):
        """Send alert to operations team"""
        # In production, this would send to PagerDuty, Slack, etc.
        self.logger.critical(
            "🚨 ALERTING OPERATIONS TEAM",
            alert_type="resource_error",
            **error_report
        )

# Global error tracker
error_tracker = ErrorTracker("api")

# Usage in exception handlers
try:
    # Some operation
    result = risky_operation()
except Exception as e:
    error_tracker.track_error(
        e,
        context={"operation": "risky_operation"},
        user_id=current_user_id,
        request_id=current_request_id
    )
    raise
```

## Log Rotation and Archival

Managing logs in production with proper rotation and archival:

```python
from pretty_loguru import create_logger, ConfigTemplates
import os
import shutil
from datetime import datetime, timedelta
import gzip

class ProductionLogManager:
    """Manage logs with rotation, compression, and archival"""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.log_base_path = f"/var/log/{app_name}"
        
        # Ensure log directories exist
        os.makedirs(f"{self.log_base_path}/current", exist_ok=True)
        os.makedirs(f"{self.log_base_path}/archive", exist_ok=True)
        
        # Create logger with production settings
        config = ConfigTemplates.production()
        config.update(
            log_path=f"{self.log_base_path}/current",
            rotation=self._rotation_function,
            retention=self._retention_function,
            compression="gz"
        )
        
        self.logger = create_logger(app_name, config=config)
    
    def _rotation_function(self, message, file):
        """Custom rotation logic"""
        # Rotate daily at 2 AM or when file exceeds 100MB
        current_time = message.record["time"]
        should_rotate_time = (
            current_time.hour == 2 and 
            current_time.minute == 0 and 
            current_time.second == 0
        )
        should_rotate_size = file.tell() > 100 * 1024 * 1024  # 100MB
        
        return should_rotate_time or should_rotate_size
    
    def _retention_function(self, path):
        """Custom retention logic"""
        # Keep logs for 30 days in current directory
        # Then move to archive for long-term storage
        
        file_age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
        
        if file_age > timedelta(days=30):
            # Move to archive instead of deleting
            archive_path = path.parent.parent / "archive" / path.name
            shutil.move(str(path), str(archive_path))
            
            # Compress archived logs older than 7 days
            if file_age > timedelta(days=37):
                self._compress_log(archive_path)
            
            return True  # Remove from current directory
        
        return False
    
    def _compress_log(self, log_path):
        """Compress log file with gzip"""
        compressed_path = f"{log_path}.gz"
        
        with open(log_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove original file
        os.unlink(log_path)
        
        self.logger.info(f"Compressed archived log: {log_path.name}")
    
    def get_logger(self):
        """Get the configured logger"""
        return self.logger
    
    def archive_old_logs(self):
        """Manually archive old logs"""
        current_dir = f"{self.log_base_path}/current"
        archive_dir = f"{self.log_base_path}/archive"
        
        archived_count = 0
        
        for filename in os.listdir(current_dir):
            file_path = os.path.join(current_dir, filename)
            
            # Check file age
            file_age = datetime.now() - datetime.fromtimestamp(
                os.path.getmtime(file_path)
            )
            
            if file_age > timedelta(days=30):
                # Archive the file
                archive_path = os.path.join(archive_dir, filename)
                shutil.move(file_path, archive_path)
                archived_count += 1
        
        self.logger.info(f"Archived {archived_count} log files")

# Usage
log_manager = ProductionLogManager("production_app")
logger = log_manager.get_logger()

# Schedule daily archival
import schedule

schedule.every().day.at("03:00").do(log_manager.archive_old_logs)
```

## Health Checks and Monitoring

Implementing health checks with logging:

```python
from pretty_loguru import create_logger
from typing import Dict, List, Tuple
import aiohttp
import asyncio
import psutil
import time

class HealthMonitor:
    """Monitor application and system health"""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.logger = create_logger(
            f"{app_name}_health",
            log_path="logs/health"
        )
        self.checks = {}
        self.last_results = {}
    
    def register_check(self, name: str, check_func):
        """Register a health check"""
        self.checks[name] = check_func
    
    async def run_health_checks(self) -> Tuple[bool, Dict[str, Dict]]:
        """Run all registered health checks"""
        results = {}
        all_healthy = True
        
        for name, check_func in self.checks.items():
            start_time = time.time()
            
            try:
                if asyncio.iscoroutinefunction(check_func):
                    result = await check_func()
                else:
                    result = check_func()
                
                duration = time.time() - start_time
                
                results[name] = {
                    "status": "healthy" if result else "unhealthy",
                    "duration": f"{duration:.3f}s",
                    "timestamp": time.time()
                }
                
                if not result:
                    all_healthy = False
                    
            except Exception as e:
                all_healthy = False
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                }
        
        # Log health status
        self._log_health_status(results)
        self.last_results = results
        
        return all_healthy, results
    
    def _log_health_status(self, results: Dict[str, Dict]):
        """Log health check results"""
        healthy_checks = [k for k, v in results.items() if v["status"] == "healthy"]
        unhealthy_checks = [k for k, v in results.items() if v["status"] != "healthy"]
        
        if not unhealthy_checks:
            self.logger.success(
                f"All health checks passed ({len(healthy_checks)} checks)"
            )
        else:
            self.logger.warning(
                f"Health check failures: {', '.join(unhealthy_checks)}"
            )
            
            # Log details of failures
            for check_name in unhealthy_checks:
                self.logger.error(
                    f"Health check failed: {check_name}",
                    **results[check_name]
                )
        
        # Visual health summary every 10 checks
        if hasattr(self, '_check_count'):
            self._check_count += 1
        else:
            self._check_count = 1
            
        if self._check_count % 10 == 0:
            self._display_health_summary(results)
    
    def _display_health_summary(self, results: Dict[str, Dict]):
        """Display visual health summary"""
        table_data = []
        
        for check_name, result in results.items():
            status = result["status"]
            if status == "healthy":
                status_icon = "🟢"
            elif status == "unhealthy":
                status_icon = "🟡"
            else:
                status_icon = "🔴"
            
            table_data.append({
                "Check": check_name,
                "Status": f"{status_icon} {status}",
                "Duration": result.get("duration", "N/A")
            })
        
        self.logger.console_table(
            "Health Check Summary",
            table_data
        )

# Define health checks
async def check_database():
    """Check database connectivity"""
    # Simulate database check
    await asyncio.sleep(0.1)
    return True

async def check_external_api():
    """Check external API availability"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                "https://api.example.com/health",
                timeout=5
            ) as response:
                return response.status == 200
        except:
            return False

def check_disk_space():
    """Check available disk space"""
    disk_usage = psutil.disk_usage('/')
    # Alert if less than 10% free
    return disk_usage.percent < 90

def check_memory():
    """Check memory usage"""
    memory = psutil.virtual_memory()
    # Alert if more than 90% used
    return memory.percent < 90

# Set up monitoring
monitor = HealthMonitor("api")
monitor.register_check("database", check_database)
monitor.register_check("external_api", check_external_api)
monitor.register_check("disk_space", check_disk_space)
monitor.register_check("memory", check_memory)

# Run health checks periodically
async def health_check_loop():
    while True:
        await monitor.run_health_checks()
        await asyncio.sleep(60)  # Check every minute

# Start monitoring
asyncio.create_task(health_check_loop())
```

## Production Deployment Script

Complete deployment script with logging:

```python
from pretty_loguru import create_logger
import subprocess
import sys
import os
from datetime import datetime

class DeploymentLogger:
    """Logger for deployment process"""
    
    def __init__(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = create_logger(
            "deployment",
            log_path=f"logs/deployments/{timestamp}"
        )
        
        # Also log to file for permanent record
        self.logger.add(
            f"logs/deployments/deployment_{timestamp}.log",
            level="DEBUG",
            format="{time} | {level} | {message}"
        )
    
    def run_command(self, command: str, description: str):
        """Run deployment command with logging"""
        self.logger.info(f"Running: {description}")
        self.logger.debug(f"Command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            
            self.logger.success(f"✓ {description}")
            if result.stdout:
                self.logger.debug(f"Output: {result.stdout}")
                
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"✗ {description} failed")
            self.logger.error(f"Error: {e.stderr}")
            return False
    
    def deploy(self):
        """Run full deployment process"""
        self.logger.ascii_header(
            "DEPLOYMENT",
            font="doom",
            border_style="blue"
        )
        
        steps = [
            ("git pull origin main", "Pull latest code"),
            ("pip install -r requirements.txt", "Install dependencies"),
            ("python -m pytest tests/", "Run tests"),
            ("python manage.py migrate", "Run database migrations"),
            ("python manage.py collectstatic --noinput", "Collect static files"),
            ("supervisorctl restart api", "Restart API service"),
            ("python scripts/health_check.py", "Verify deployment")
        ]
        
        # Display deployment plan
        self.logger.console_block(
            "Deployment Plan",
            [f"{i+1}. {desc}" for i, (_, desc) in enumerate(steps)],
            border_style="cyan"
        )
        
        # Execute steps
        for i, (command, description) in enumerate(steps):
            self.logger.console_panel(
                f"Step {i+1}/{len(steps)}: {description}",
                title="🚀 Deploying",
                border_style="yellow"
            )
            
            if not self.run_command(command, description):
                self.logger.error("Deployment failed!")
                self.logger.ascii_header(
                    "FAILED",
                    font="doom",
                    border_style="red"
                )
                sys.exit(1)
        
        # Success!
        self.logger.ascii_header(
            "SUCCESS",
            font="doom",
            border_style="green"
        )
        
        self.logger.success("Deployment completed successfully!")

# Run deployment
if __name__ == "__main__":
    deployer = DeploymentLogger()
    deployer.deploy()
```

## Next Steps

- [Enterprise Examples](./enterprise.md) - Enterprise-grade features
- [Performance Guide](../guide/performance.md) - Performance optimization
- [Production Guide](../guide/production.md) - Production best practices