# Uvicorn Integration

Complete guide for integrating pretty-loguru with Uvicorn ASGI server for enhanced web server logging.

## 🚀 Basic Uvicorn Integration

### Simple Setup

```python
# main.py
from fastapi import FastAPI
from pretty_loguru import create_logger
import uvicorn

# Initialize pretty-loguru
logger = create_logger(
    name="demo",
    log_path="logs/",
    level="INFO"
)

app = FastAPI()

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}

if __name__ == "__main__":
    logger.ascii_header("UVICORN SERVER", font="slant")
    logger.info("Starting Uvicorn server with pretty-loguru")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None  # Disable Uvicorn's default logging
    )
```

### Custom Uvicorn Configuration

```python
import uvicorn
from pretty_loguru import create_logger

# Configure pretty-loguru for server logging
create_logger(
    level="INFO",
    log_path="logs",
    component_name="uvicorn_server",
    rotation="50MB",
    retention="30 days"
)

# Custom Uvicorn configuration
config = uvicorn.Config(
    app="main:app",
    host="0.0.0.0",
    port=8000,
    log_config=None,  # Disable default logging
    access_log=False,  # We'll handle access logs ourselves
    use_colors=False,  # pretty-loguru handles colors
    reload=True  # Development mode
)

server = uvicorn.Server(config)

async def serve():
    logger.success("🚀 Starting Uvicorn server with pretty-loguru")
    await server.serve()

if __name__ == "__main__":
    import asyncio
    asyncio.run(serve())
```

## 🔧 Access Log Integration

### Custom Access Logger

```python
import logging
import time
from typing import Callable, Any
from uvicorn.protocols.http.h11_impl import H11Protocol
from pretty_loguru import create_logger

class PrettyLoguruAccessLogger:
    """Custom access logger using pretty-loguru"""
    
    def __init__(self):
        self.logger = logger
    
    def log_access(self, 
                   method: str, 
                   path: str, 
                   status_code: int, 
                   response_time: float,
                   client_ip: str = None,
                   user_agent: str = None,
                   content_length: int = None):
        """Log HTTP access with pretty formatting"""
        
        # Choose log level based on status code
        if 200 <= status_code < 300:
            log_func = self.logger.success
            status_emoji = "✅"
        elif 300 <= status_code < 400:
            log_func = self.logger.info
            status_emoji = "🔄"
        elif 400 <= status_code < 500:
            log_func = self.logger.warning
            status_emoji = "⚠️"
        else:
            log_func = self.logger.error
            status_emoji = "❌"
        
        # Format response time
        if response_time < 0.1:
            time_color = "green"
        elif response_time < 0.5:
            time_color = "yellow"
        else:
            time_color = "red"
        
        # Log the access
        log_func(
            f"{status_emoji} {method} {path} - {status_code} ({response_time:.3f}s)",
            method=method,
            path=path,
            status_code=status_code,
            response_time=response_time,
            client_ip=client_ip,
            user_agent=user_agent,
            content_length=content_length,
            access_log=True
        )

# Global access logger instance
access_logger = PrettyLoguruAccessLogger()
```

### Uvicorn Protocol Override

```python
from uvicorn.protocols.http.h11_impl import H11Protocol
import time

class LoggingH11Protocol(H11Protocol):
    """Custom H11Protocol with pretty-loguru access logging"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None
    
    async def handle_request(self, message):
        """Override to add request timing and logging"""
        self.start_time = time.time()
        
        try:
            await super().handle_request(message)
        finally:
            if self.start_time:
                response_time = time.time() - self.start_time
                
                # Extract request details
                method = self.scope.get('method', 'UNKNOWN')
                path = self.scope.get('path', '/')
                client = self.scope.get('client', ['unknown', 0])
                client_ip = client[0] if client else 'unknown'
                
                # Get response status
                status_code = getattr(self, 'status_code', 200)
                
                # Log the access
                access_logger.log_access(
                    method=method,
                    path=path,
                    status_code=status_code,
                    response_time=response_time,
                    client_ip=client_ip
                )

# Configure Uvicorn to use custom protocol
config = uvicorn.Config(
    app="main:app",
    host="0.0.0.0",
    port=8000,
    http="uvicorn.protocols.http.h11_impl:H11Protocol",  # Use custom protocol
    log_config=None
)
```

## 🎯 Server Event Logging

### Lifecycle Event Logging

```python
import signal
import uvicorn
from pretty_loguru import create_logger

class LoggingServer(uvicorn.Server):
    """Custom Uvicorn server with enhanced logging"""
    
    async def startup(self, sockets=None):
        """Server startup with logging"""
        logger.block("Server Startup", [
            f"Host: {self.config.host}",
            f"Port: {self.config.port}",
            f"Workers: {self.config.workers or 1}",
            f"Reload: {self.config.reload}",
            f"Environment: {self.config.env_file or 'default'}"
        ], border_style="green")
        
        await super().startup(sockets)
        
        logger.success("🚀 Uvicorn server started successfully")
        logger.info(f"Server accessible at http://{self.config.host}:{self.config.port}")
    
    async def shutdown(self, sockets=None):
        """Server shutdown with logging"""
        logger.warning("🔴 Initiating server shutdown...")
        
        await super().shutdown(sockets)
        
        logger.info("🔽 Server shutdown completed")
        logger.ascii_header("SHUTDOWN", font="small")

# Configure custom server
config = uvicorn.Config(
    app="main:app",
    host="0.0.0.0",
    port=8000,
    log_config=None
)

server = LoggingServer(config)

# Handle shutdown signals
async def signal_handler(signum, frame):
    logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
    server.should_exit = True

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.serve())
```

### Worker Process Logging

```python
import os
import multiprocessing
from pretty_loguru import create_logger, create_logger

def setup_worker_logging():
    """Setup logging for worker processes"""
    worker_id = os.getpid()
    
    create_logger(
        level="INFO",
        log_path=f"logs/worker_{worker_id}",
        component_name=f"uvicorn_worker_{worker_id}",
        rotation="20MB",
        retention="7 days"
    )
    
    logger.success(f"Worker {worker_id} logging initialized")

class WorkerLoggingApplication:
    """ASGI application wrapper with worker logging"""
    
    def __init__(self, app):
        self.app = app
        setup_worker_logging()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            worker_id = os.getpid()
            logger.debug(f"Worker {worker_id} handling request: {scope['method']} {scope['path']}")
        
        await self.app(scope, receive, send)

# Wrap your FastAPI app
from main import app
worker_app = WorkerLoggingApplication(app)

# Multi-worker configuration
if __name__ == "__main__":
    uvicorn.run(
        "uvicorn_integration:worker_app",
        host="0.0.0.0",
        port=8000,
        workers=multiprocessing.cpu_count(),
        log_config=None
    )
```

## 📊 Performance and Monitoring

### Request Performance Monitoring

```python
import time
import asyncio
from typing import Dict, List
from collections import defaultdict, deque
from pretty_loguru import create_logger

class PerformanceMonitor:
    """Monitor and log server performance metrics"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.request_times: deque = deque(maxlen=window_size)
        self.endpoint_stats: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.error_count = 0
        self.total_requests = 0
    
    def record_request(self, endpoint: str, duration: float, status_code: int):
        """Record request performance data"""
        self.total_requests += 1
        self.request_times.append(duration)
        self.endpoint_stats[endpoint].append(duration)
        
        if status_code >= 400:
            self.error_count += 1
        
        # Log slow requests
        if duration > 1.0:
            logger.warning(
                f"Slow request detected: {endpoint} took {duration:.3f}s",
                endpoint=endpoint,
                duration=duration,
                performance=True
            )
    
    def get_stats(self) -> dict:
        """Get current performance statistics"""
        if not self.request_times:
            return {}
        
        avg_response_time = sum(self.request_times) / len(self.request_times)
        error_rate = (self.error_count / self.total_requests) * 100 if self.total_requests > 0 else 0
        
        return {
            "total_requests": self.total_requests,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate,
            "current_window_size": len(self.request_times)
        }
    
    async def log_periodic_stats(self, interval: int = 60):
        """Periodically log performance statistics"""
        while True:
            await asyncio.sleep(interval)
            stats = self.get_stats()
            
            if stats:
                logger.block("Performance Statistics", [
                    f"Total Requests: {stats['total_requests']}",
                    f"Average Response Time: {stats['avg_response_time']:.3f}s",
                    f"Error Rate: {stats['error_rate']:.2f}%",
                    f"Window Size: {stats['current_window_size']}"
                ], border_style="blue")

# Global performance monitor
perf_monitor = PerformanceMonitor()

# Start periodic logging task
async def start_performance_monitoring():
    asyncio.create_task(perf_monitor.log_periodic_stats())

# Add to your FastAPI startup
@app.on_event("startup")
async def startup_event():
    await start_performance_monitoring()
    logger.info("Performance monitoring started")
```

### Memory and Resource Monitoring

```python
import psutil
import asyncio
from pretty_loguru import create_logger

class ResourceMonitor:
    """Monitor system resources used by Uvicorn"""
    
    def __init__(self, process_id: int = None):
        self.process = psutil.Process(process_id or os.getpid())
        self.initial_memory = self.process.memory_info().rss
    
    def get_resource_usage(self) -> dict:
        """Get current resource usage"""
        memory_info = self.process.memory_info()
        cpu_percent = self.process.cpu_percent()
        
        return {
            "memory_rss": memory_info.rss,
            "memory_vms": memory_info.vms,
            "memory_percent": self.process.memory_percent(),
            "cpu_percent": cpu_percent,
            "num_threads": self.process.num_threads(),
            "num_fds": self.process.num_fds() if hasattr(self.process, 'num_fds') else 0
        }
    
    async def log_resource_usage(self, interval: int = 300):
        """Periodically log resource usage"""
        while True:
            try:
                usage = self.get_resource_usage()
                
                # Convert bytes to MB
                memory_mb = usage["memory_rss"] / (1024 * 1024)
                initial_memory_mb = self.initial_memory / (1024 * 1024)
                memory_growth = memory_mb - initial_memory_mb
                
                # Log resource usage
                logger.info(
                    f"Resource usage - Memory: {memory_mb:.1f}MB (+{memory_growth:.1f}MB), "
                    f"CPU: {usage['cpu_percent']:.1f}%, Threads: {usage['num_threads']}",
                    memory_mb=memory_mb,
                    memory_growth=memory_growth,
                    cpu_percent=usage['cpu_percent'],
                    num_threads=usage['num_threads'],
                    resource_monitoring=True
                )
                
                # Warning for high resource usage
                if usage["memory_percent"] > 80:
                    logger.warning(
                        f"High memory usage: {usage['memory_percent']:.1f}%",
                        memory_percent=usage['memory_percent']
                    )
                
                if usage["cpu_percent"] > 80:
                    logger.warning(
                        f"High CPU usage: {usage['cpu_percent']:.1f}%",
                        cpu_percent=usage['cpu_percent']
                    )
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
                await asyncio.sleep(interval)

# Initialize and start resource monitoring
resource_monitor = ResourceMonitor()

@app.on_event("startup")
async def startup_monitoring():
    asyncio.create_task(resource_monitor.log_resource_usage())
    logger.info("Resource monitoring started")
```

## 🔧 Configuration Management

### Environment-Based Configuration

```python
import os
from typing import Optional
from pydantic import BaseSettings
from pretty_loguru import create_logger

class UvicornLoggingConfig(BaseSettings):
    """Configuration for Uvicorn with pretty-loguru"""
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: Optional[int] = None
    reload: bool = False
    
    # Logging settings
    log_level: str = "INFO"
    log_path: str = "logs"
    log_rotation: str = "50MB"
    log_retention: str = "30 days"
    enable_access_logs: bool = True
    enable_performance_monitoring: bool = True
    performance_log_interval: int = 60
    resource_log_interval: int = 300
    
    class Config:
        env_prefix = "UVICORN_"
        env_file = ".env"

def setup_logging_from_config(config: UvicornLoggingConfig):
    """Setup pretty-loguru based on configuration"""
    
    create_logger(
        level=config.log_level,
        log_path=config.log_path,
        component_name="uvicorn_server",
        rotation=config.log_rotation,
        retention=config.log_retention
    )
    
    # Add access log file if enabled
    if config.enable_access_logs:
        logger.add(
            f"{config.log_path}/access.log",
            filter=lambda record: record["extra"].get("access_log", False),
            format="{time} | {level} | {message}",
            rotation="daily",
            retention="90 days"
        )
    
    logger.success("Logging configuration applied successfully")
    logger.info(f"Log level: {config.log_level}")
    logger.info(f"Log path: {config.log_path}")
    logger.info(f"Access logs: {'enabled' if config.enable_access_logs else 'disabled'}")

# Usage
config = UvicornLoggingConfig()
setup_logging_from_config(config)

if __name__ == "__main__":
    logger.ascii_header("UVICORN STARTUP", font="slant")
    
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        workers=config.workers,
        reload=config.reload,
        log_config=None
    )
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create logs directory
RUN mkdir -p logs

# Environment variables for logging
ENV UVICORN_LOG_LEVEL=INFO
ENV UVICORN_LOG_PATH=logs
ENV UVICORN_ENABLE_ACCESS_LOGS=true

EXPOSE 8000

CMD ["python", "uvicorn_server.py"]
```

```python
# uvicorn_server.py for Docker
import os
import signal
import asyncio
from pretty_loguru import create_logger, create_logger
import uvicorn

# Docker-specific logging setup
def setup_docker_logging():
    """Configure logging for Docker environment"""
    
    # Use environment variables or defaults
    log_level = os.getenv("UVICORN_LOG_LEVEL", "INFO")
    log_path = os.getenv("UVICORN_LOG_PATH", "logs")
    
    create_logger(
        level=log_level,
        log_path=log_path,
        component_name="uvicorn_docker",
        rotation="100MB",
        retention="7 days"  # Shorter retention in containers
    )
    
    # Also log to stdout for Docker logs
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    logger.success("Docker logging configuration applied")

def main():
    """Main entry point for Docker container"""
    
    setup_docker_logging()
    
    logger.ascii_header("DOCKER UVICORN", font="small")
    logger.info("Starting Uvicorn server in Docker container")
    
    # Handle shutdown signals gracefully
    def signal_handler(signum, frame):
        logger.warning(f"Received signal {signum}, shutting down...")
        os._exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=int(os.getenv("WORKERS", 1)),
        log_config=None,
        access_log=False  # We handle this ourselves
    )

if __name__ == "__main__":
    main()
```

This comprehensive Uvicorn integration provides production-ready logging capabilities for ASGI applications!