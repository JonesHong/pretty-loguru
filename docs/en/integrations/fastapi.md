# FastAPI Integration

Complete guide for integrating pretty-loguru with FastAPI applications for enhanced API logging.

## 🚀 Quick Start

### Basic FastAPI Integration

```python
from fastapi import FastAPI
from pretty_loguru import create_logger, logger

# Initialize logger
logger = create_logger(
    name="demo",
    log_path=
    folder="logs",
    level="INFO"
)

# Create FastAPI app
app = FastAPI(title="My API with pretty-loguru")

@app.on_event("startup")
async def startup_event():
    logger.success("🚀 FastAPI application started successfully")
    logger.info(f"Logger component: {component_name}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("🔴 FastAPI application shutting down")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World", "logger": component_name}

@app.get("/health")
async def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
```

### Advanced FastAPI Setup

```python
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pretty_loguru import init_logger, logger
import time
import uuid
from contextlib import asynccontextmanager

# Configure logging for production
init_logger(
    level="INFO",
    log_path="logs",
    component_name="fastapi_app",
    rotation="50MB",
    retention="30 days"
)

# Add structured logging for APIs
logger.add(
    "logs/api_requests.json",
    format=lambda record: json.dumps({
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "request_id": record["extra"].get("request_id"),
        "endpoint": record["extra"].get("endpoint"),
        "method": record["extra"].get("method"),
        "status_code": record["extra"].get("status_code"),
        "duration": record["extra"].get("duration"),
        "ip": record["extra"].get("ip")
    }),
    level="INFO",
    rotation="daily"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.ascii_header("FASTAPI STARTUP", font="slant")
    logger.success("FastAPI application initialized")
    yield
    # Shutdown
    logger.warning("FastAPI application shutting down")

app = FastAPI(
    title="Enhanced API with pretty-loguru",
    description="API with comprehensive logging",
    version="1.0.1",
    lifespan=lifespan
)
```

## 🔧 Middleware Integration

### Request Logging Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())[:8]
        
        # Log request start
        start_time = time.time()
        logger.info(
            f"🔵 Request started: {request.method} {request.url.path}",
            request_id=request_id,
            method=request.method,
            endpoint=request.url.path,
            ip=request.client.host if request.client else "unknown"
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log successful response
            logger.success(
                f"✅ Request completed: {request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)",
                request_id=request_id,
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
                duration=duration,
                ip=request.client.host if request.client else "unknown"
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"❌ Request failed: {request.method} {request.url.path} - {str(e)} ({duration:.3f}s)",
                request_id=request_id,
                method=request.method,
                endpoint=request.url.path,
                error=str(e),
                duration=duration,
                ip=request.client.host if request.client else "unknown"
            )
            raise

# Add middleware to app
app.add_middleware(LoggingMiddleware)
```

### Correlation ID Middleware

```python
import contextvars
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable for request correlation
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar('correlation_id')

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get or generate correlation ID
        correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4())[:8])
        correlation_id_var.set(correlation_id)
        
        # Bind correlation ID to logger for this request
        bound_logger = logger.bind(correlation_id=correlation_id)
        
        bound_logger.info(f"Processing request with correlation ID: {correlation_id}")
        
        try:
            response = await call_next(request)
            response.headers['X-Correlation-ID'] = correlation_id
            return response
        except Exception as e:
            bound_logger.error(f"Request failed with correlation ID {correlation_id}: {e}")
            raise

app.add_middleware(CorrelationMiddleware)

# Usage in endpoints
@app.get("/correlated")
async def correlated_endpoint():
    correlation_id = correlation_id_var.get()
    logger.bind(correlation_id=correlation_id).info("Processing correlated request")
    return {"correlation_id": correlation_id}
```

## 🎯 Endpoint-Specific Logging

### Dependency Injection for Logging

```python
from fastapi import Depends
from typing import Dict, Any

def get_logger_context(request: Request) -> Dict[str, Any]:
    """Dependency to provide logging context"""
    return {
        "endpoint": request.url.path,
        "method": request.method,
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown")
    }

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    context: Dict[str, Any] = Depends(get_logger_context)
):
    bound_logger = logger.bind(**context)
    
    bound_logger.info(f"Fetching user {user_id}")
    
    try:
        # Simulate user lookup
        if user_id == 0:
            bound_logger.warning(f"Invalid user ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = {"id": user_id, "name": f"User {user_id}"}
        bound_logger.success(f"User {user_id} fetched successfully")
        
        return user_data
    
    except HTTPException:
        raise
    except Exception as e:
        bound_logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Business Logic Logging

```python
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: str

class CreateUserRequest(BaseModel):
    name: str
    email: str

@app.post("/users", response_model=User)
async def create_user(user_data: CreateUserRequest):
    logger.info(f"Creating new user: {user_data.name}")
    
    try:
        # Validation logging
        if "@" not in user_data.email:
            logger.warning(f"Invalid email format: {user_data.email}")
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Business logic logging
        logger.debug(f"Validating user data: {user_data.dict()}")
        
        # Simulate user creation
        new_user = User(
            id=123,
            name=user_data.name,
            email=user_data.email
        )
        
        logger.success(f"User created successfully: {new_user.id}")
        logger.block("User Creation Summary", [
            f"ID: {new_user.id}",
            f"Name: {new_user.name}",
            f"Email: {new_user.email}"
        ], border_style="green")
        
        return new_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise HTTPException(status_code=500, detail="User creation failed")

@app.get("/users", response_model=List[User])
async def list_users(skip: int = 0, limit: int = 100):
    logger.info(f"Listing users with skip={skip}, limit={limit}")
    
    # Simulate user listing
    users = [
        User(id=i, name=f"User {i}", email=f"user{i}@example.com")
        for i in range(skip + 1, skip + limit + 1)
    ]
    
    logger.success(f"Retrieved {len(users)} users")
    return users
```

## 🔒 Security & Authentication Logging

### Authentication Logging

```python
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token with logging"""
    logger.info("Attempting token verification", token_prefix=credentials.credentials[:10])
    
    try:
        # Simulate token verification
        if credentials.credentials == "invalid":
            logger.warning("Invalid token provided", token_prefix=credentials.credentials[:10])
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        logger.success("Token verified successfully")
        return {"user_id": 123, "username": "john_doe"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

@app.get("/protected")
async def protected_endpoint(current_user = Depends(verify_token)):
    logger.info(f"Protected endpoint accessed by user {current_user['username']}")
    return {"message": "Access granted", "user": current_user}
```

### Security Event Logging

```python
from fastapi import Request
import json

def log_security_event(event_type: str, request: Request, details: dict = None):
    """Log security-related events"""
    security_data = {
        "event_type": event_type,
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "endpoint": request.url.path,
        "method": request.method,
        "timestamp": time.time(),
        "details": details or {}
    }
    
    logger.bind(security=True, **security_data).warning(
        f"Security event: {event_type}"
    )

@app.post("/login")
async def login(request: Request, credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    
    logger.info(f"Login attempt for user: {username}")
    
    # Simulate authentication
    if username == "admin" and password == "secret":
        log_security_event("login_success", request, {"username": username})
        logger.success(f"Successful login for user: {username}")
        return {"token": "fake-jwt-token"}
    else:
        log_security_event("login_failure", request, {
            "username": username,
            "reason": "invalid_credentials"
        })
        logger.warning(f"Failed login attempt for user: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
```

## 📊 Performance Monitoring

### Response Time Logging

```python
import asyncio
from functools import wraps

def log_performance(operation_name: str):
    """Decorator to log operation performance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.debug(f"Starting {operation_name}")
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                if duration > 1.0:  # Log slow operations
                    logger.warning(
                        f"Slow operation: {operation_name} took {duration:.3f}s",
                        operation=operation_name,
                        duration=duration,
                        performance=True
                    )
                else:
                    logger.debug(
                        f"Operation completed: {operation_name} ({duration:.3f}s)",
                        operation=operation_name,
                        duration=duration,
                        performance=True
                    )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Operation failed: {operation_name} after {duration:.3f}s - {e}",
                    operation=operation_name,
                    duration=duration,
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator

@app.get("/slow-operation")
@log_performance("slow_database_query")
async def slow_operation():
    # Simulate slow operation
    await asyncio.sleep(2)
    return {"result": "Operation completed"}
```

### Database Query Logging

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def log_database_operation(operation: str, **context):
    """Context manager for database operation logging"""
    start_time = time.time()
    logger.debug(f"Database operation started: {operation}", **context)
    
    try:
        yield
        duration = time.time() - start_time
        logger.info(
            f"Database operation completed: {operation} ({duration:.3f}s)",
            operation=operation,
            duration=duration,
            database=True,
            **context
        )
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"Database operation failed: {operation} after {duration:.3f}s - {e}",
            operation=operation,
            duration=duration,
            error=str(e),
            database=True,
            **context
        )
        raise

@app.get("/users/{user_id}/orders")
async def get_user_orders(user_id: int):
    async with log_database_operation("fetch_user_orders", user_id=user_id):
        # Simulate database query
        await asyncio.sleep(0.1)
        
        orders = [
            {"id": 1, "product": "Widget A", "price": 19.99},
            {"id": 2, "product": "Widget B", "price": 29.99}
        ]
        
        logger.success(f"Retrieved {len(orders)} orders for user {user_id}")
        return orders
```

## 🔥 Error Handling & Exception Logging

### Global Exception Handler

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with comprehensive logging"""
    
    # Generate error ID for tracking
    error_id = str(uuid.uuid4())[:8]
    
    # Log detailed error information
    logger.error(
        f"Unhandled exception [{error_id}]: {type(exc).__name__}: {str(exc)}",
        error_id=error_id,
        exception_type=type(exc).__name__,
        exception_message=str(exc),
        endpoint=request.url.path,
        method=request.method,
        traceback=traceback.format_exc()
    )
    
    # Return user-friendly error response
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_id": error_id,
            "message": "An unexpected error occurred. Please contact support with this error ID."
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler with logging"""
    
    logger.warning(
        f"HTTP exception: {exc.status_code} - {exc.detail}",
        status_code=exc.status_code,
        detail=exc.detail,
        endpoint=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

### Custom Exception Classes

```python
class BusinessLogicError(Exception):
    """Custom exception for business logic errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

@app.exception_handler(BusinessLogicError)
async def business_logic_exception_handler(request: Request, exc: BusinessLogicError):
    """Handle business logic exceptions"""
    
    logger.warning(
        f"Business logic error: {exc.message}",
        error_code=exc.error_code,
        endpoint=request.url.path,
        method=request.method,
        business_logic=True
    )
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Business logic error",
            "message": exc.message,
            "error_code": exc.error_code
        }
    )

# Usage in endpoints
@app.post("/process-order")
async def process_order(order_data: dict):
    try:
        if order_data.get("amount", 0) <= 0:
            raise BusinessLogicError("Order amount must be positive", "INVALID_AMOUNT")
        
        logger.info(f"Processing order: {order_data}")
        # Process order logic here
        
        return {"status": "success", "order_id": 12345}
        
    except BusinessLogicError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing order: {e}")
        raise HTTPException(status_code=500, detail="Order processing failed")
```

This comprehensive FastAPI integration provides enterprise-grade logging capabilities for modern web applications!