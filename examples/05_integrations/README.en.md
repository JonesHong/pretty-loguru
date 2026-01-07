# 04_fastapi - Real Web Application Examples

This directory showcases deep integration of pretty-loguru with FastAPI, providing real runnable web application examples.

## 🎯 Learning Objectives

- Master integration of FastAPI with pretty-loguru
- Understand automatic logging features of middleware
- Learn to use logger dependency injection patterns
- Understand logging best practices for web applications

## 📋 Prerequisites

Install necessary dependencies:
```bash
pip install fastapi uvicorn
# or
pip install -r requirements.txt
```

## 📚 Example List

### 1. simple_api.py - Basic FastAPI Integration
**Learning Focus**: Basic combination of FastAPI and pretty-loguru

```bash
python simple_api.py
```

**Features Demonstrated**:
- Basic API route logging
- Startup/shutdown event logging
- Error handling and logging
- User-friendly console messages vs detailed file records

**Testing Methods**:
```bash
# After starting the service, test in a new terminal
curl http://localhost:8000/
curl http://localhost:8000/users/123
curl http://localhost:8000/users/999  # Test 404 error
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com"}'
```

### 2. middleware_demo.py - Complete Middleware Functionality
**Learning Focus**: LoggingMiddleware's automatic request/response logging

```bash
python middleware_demo.py
```

**Features Demonstrated**:
- Automatically log all API requests and responses
- Performance monitoring (response time)
- Request body and response body logging
- Error tracking and exception handling

**Testing Methods**:
```bash
# Service runs on http://localhost:8001
curl http://localhost:8001/
curl http://localhost:8001/slow        # Test slow requests
curl http://localhost:8001/error       # Test error handling
curl -X POST http://localhost:8001/data -H "Content-Type: application/json" -d '{"test":"data"}'
```

### 3. dependency_injection.py - Logger Dependency Injection
**Learning Focus**: Logger management in microservice architecture

```bash
python dependency_injection.py
```

**Features Demonstrated**:
- Different services use independent loggers
- Logger dependency injection pattern
- Log isolation between services
- Log management for multi-service architecture

**Testing Methods**:
```bash
# Service runs on http://localhost:8002
curl -X POST http://localhost:8002/auth/login
curl http://localhost:8002/users/profile
curl -X POST http://localhost:8002/orders/create
curl http://localhost:8002/logs/stats
```

## 🔧 Core Features

### Basic Integration
```python
from pretty_loguru import create_logger
from fastapi import FastAPI

logger = create_logger("my_api", log_dir="./logs")
app = FastAPI()

@app.get("/")
async def root():
    logger.info("Processing homepage request")
    return {"message": "Hello World"}
```

### Middleware Setup
```python
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

setup_fastapi_logging(
    app,
    logger_instance=logger,
    middleware=True,
    log_request_body=True,
    log_response_body=True,
    exclude_paths=["/health"]
)
```

### Dependency Injection
```python
from pretty_loguru.integrations.fastapi import get_logger_dependency
from pretty_loguru import create_logger

logger = create_logger("user_service")
user_logger_dep = get_logger_dependency(logger)

@app.get("/users")
async def get_users(logger: PrettyLogger = Depends(user_logger_dep)):
    logger.info("Querying user list")
    return {"users": []}
```

## 📁 Generated Log Files

After running examples, you will see:
```
logs/
├── simple_api_YYYYMMDD-HHMMSS.log          # Basic API logs
├── middleware_demo_YYYYMMDD-HHMMSS.log     # Middleware demo logs
├── dependency_app_YYYYMMDD-HHMMSS.log      # Main application logs
├── auth_service_YYYYMMDD-HHMMSS.log        # Authentication service logs
├── user_service_YYYYMMDD-HHMMSS.log        # User service logs
└── order_service_YYYYMMDD-HHMMSS.log       # Order service logs
```

## 🌟 Best Practices

### 1. Layered Logging
```python
# Concise messages for users
from pretty_loguru.addons import log_to_targets
log_to_targets(logger, "Processing your request...", level="INFO", console_only=True)

# Detailed information for system records
log_to_targets(logger, f"API request - Endpoint: {request.url}, User: {user_id}", level="INFO", file_only=True)
```

### 2. Error Handling
```python
try:
    result = process_data()
    logger.success("Data processing completed")
except Exception as e:
    logger.error(f"Processing failed: {str(e)}")
    logger.opt(exception=True).bind(to_file_only=True).error("Detailed error information")
    raise HTTPException(status_code=500, detail="Processing failed")
```

### 3. Performance Monitoring
```python
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"Request processing completed - Time: {process_time:.3f}s")
    return response
```

## 🚀 Quick Start Guide

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Run basic example**:
   ```bash
   python simple_api.py
   ```

3. **View Swagger documentation**:
   ```
   http://localhost:8000/docs
   ```

4. **Check log output**:
   ```bash
   ls ./logs/
   tail -f ./logs/*.log
   ```

## 🔗 Related Examples

- **01_basics/** - Learn basic concepts
- **03_presets/** - Log file management and rotation
- **05_production/** - Production environment configuration

## ❓ Frequently Asked Questions

**Q: How to customize middleware logging content?**
A: Use parameters of `setup_fastapi_logging` to control, such as `log_request_body`, `exclude_paths`, etc.

**Q: How to use different log configurations in different environments?**
A: Choose different presets or configuration parameters based on environment variables.

**Q: How to manage multiple loggers in microservice architecture?**
A: Use dependency injection pattern, each service uses independent logger instances for easy tracking and analysis.
