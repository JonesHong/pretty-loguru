# Integration Guide

pretty-loguru is designed to integrate seamlessly with modern Python frameworks. This section will show you how to integrate pretty-loguru into various web frameworks and applications.

## 🌐 Supported Frameworks

### Web Frameworks
- **[FastAPI](./fastapi)** - A modern, fast web framework
- **[Uvicorn](./uvicorn)** - A high-performance ASGI server

### Coming Soon
- **Flask** - A lightweight web framework
- **Django** - A full-featured web framework
- **Starlette** - A lightweight ASGI framework

## 🚀 Quick Start

### Basic FastAPI Integration

```python
from fastapi import FastAPI
from pretty_loguru import create_logger

# Initialize logging
logger = create_logger(
    name="integrations_demo",
    log_path="api_logs",
    level="INFO"
)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.ascii_header("API STARTUP", font="slant", border_style="blue")
    logger.success("FastAPI application started successfully")

@app.get("/")
async def root():
    logger.info("Received request to root path")
    return {"message": "Hello World"}
```

### Uvicorn Log Unification

```python
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

# Unify Uvicorn logs with pretty-loguru
integrate_uvicorn()

# Now all Uvicorn logs will use the pretty-loguru format upon startup
```

## 🎯 Integration Patterns

### 1. Basic Integration
The simplest way to integrate, replacing the default logging system.

### 2. Middleware Integration
Add logging in the request processing middleware.

### 3. Dependency Injection Integration
Manage the logger using the framework's dependency injection system.

### 4. Full Customization
Complete control over logging behavior and format.

## 📊 Integration Showcase

### Request Logging

```python
# Middleware to log each request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.time()
    
    logger.console_info(f"→ {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    status_color = "green" if response.status_code < 400 else "red"
    
    logger.block(
        "Request Complete",
        [
            f"Method: {request.method}",
            f"Path: {request.url.path}",
            f"Status: {response.status_code}",
            f"Processing Time: {process_time:.3f}s"
        ],
        border_style=status_color
    )
    
    return response
```

### Startup Logging

```python
@app.on_event("startup")
async def startup():
    logger.ascii_header("WEB API", font="block", border_style="cyan")
    
    logger.block(
        "Service Information",
        [
            f"Application Name: {settings.app_name}",
            f"Version: {settings.version}",
            f"Environment: {settings.environment}",
            f"Debug Mode: {'On' if settings.debug else 'Off'}"
        ],
        border_style="blue"
    )
    
    logger.success("🚀 Web API has started successfully")
```

## 🔧 Advanced Configuration

### Environment-Specific Configuration

```python
import os
from pretty_loguru import create_logger

def setup_logging():
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return logger = create_logger(
    name="demo",
    log_path="prod_logs",
    level="INFO"
)
    elif env == "staging":
        return logger = create_logger(
    name="demo",
    log_path="staging_logs",
    level="INFO"
)
    else:  # development
        return logger = create_logger(
    name="demo",
    log_path="dev_logs",
    level="INFO"
)
```

### Multiple Log Targets

```python
from pretty_loguru import create_logger

# Dedicated logger for API
api_logger = create_logger("api", log_path="logs/api")

# Dedicated logger for Database  
db_logger = create_logger("database", log_path="logs/db")

# Dedicated logger for background tasks
task_logger = create_logger("tasks", log_path="logs/tasks")

# Use in different modules
class APIService:
    def process_request(self):
        api_logger.info("Processing API request")
        
class DatabaseService:
    def connect(self):
        db_logger.success("Database connection successful")
```

## 🎮 Practical Example

### Complete FastAPI Application

```python
from fastapi import FastAPI, Request, HTTPException
from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn
import time
import uvicorn

# Initialize logging system
logger = create_logger(
    name="integrations_demo",
    log_path="webapp_logs",
    level="INFO"
)
integrate_uvicorn(logger)

app = FastAPI(title="Demo API", version="1.0.1")

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Request start
    logger.console_info(f"→ {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Successful response
        logger.block(
            "Request Successful",
            [
                f"📍 Path: {request.url.path}",
                f"⚡ Method: {request.method}",
                f"✅ Status: {response.status_code}",
                f"⏱️  Time: {process_time:.3f}s"
            ],
            border_style="green"
        )
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        
        # Error response
        logger.block(
            "Request Failed",
            [
                f"📍 Path: {request.url.path}",
                f"⚡ Method: {request.method}",
                f"❌ Error: {str(e)}",
                f"⏱️  Time: {process_time:.3f}s"
            ],
            border_style="red",
            log_level="ERROR"
        )
        raise

@app.on_event("startup")
async def startup_event():
    logger.ascii_header("WEBAPP START", font="slant", border_style="blue")
    
    logger.block(
        "Application Configuration",
        [
            "🌐 Name: Demo API",
            "📦 Version: 1.0.1",
            "🔧 Environment: Development",
            "🚀 Status: Starting"
        ],
        border_style="cyan"
    )
    
    logger.success("✨ Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.ascii_header("SHUTDOWN", font="standard", border_style="magenta")
    logger.info("Application is shutting down...")

@app.get("/")
async def root():
    logger.info("Handling root path request")
    return {"message": "Hello Pretty Loguru!"}

@app.get("/health")
async def health_check():
    logger.success("Health check passed")
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/error")
async def trigger_error():
    logger.error("Intentionally triggering an error for testing")
    raise HTTPException(status_code=500, detail="Test error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 💡 Best Practices

### 1. Log Layering
Use different loggers for different types of logs:

```python
# Layer by function
api_logger = create_logger("api")      # API related
auth_logger = create_logger("auth")    # Authentication related  
db_logger = create_logger("db")        # Database related
```

### 2. Structured Logging
Use Rich blocks to record structured information:

```python
logger.block(
    "User Action",
    [
        f"User ID: {user_id}",
        f"Action: {action}",
        f"IP Address: {ip_address}",
        f"Timestamp: {timestamp}"
    ]
)
```

### 3. Error Tracking
Record detailed error information:

```python
import inspect

try:
    # Business logic
    pass
except Exception as e:
    logger.ascii_block(
        "Error Report",
        [
            f"Error Type: {type(e).__name__}",
            f"Error Message: {str(e)}",
            f"Location: {__file__}:{inspect.currentframe().f_lineno}",
            f"User ID: {current_user.id}",
            f"Request ID: {request_id}"
        ],
        ascii_header="ERROR",
        border_style="red",
        log_level="ERROR"
    )
```

## 🚀 Next Steps

Choose the framework you use to start integrating:

- **[FastAPI Integration](./fastapi)** - Detailed FastAPI integration guide
- **[Uvicorn Integration](./uvicorn)** - Unify Uvicorn server logs
- **[View Examples](../examples/fastapi/)** - Complete practical application examples

Ready to integrate pretty-loguru into your project? 🎯
