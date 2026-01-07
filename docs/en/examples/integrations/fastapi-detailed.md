# FastAPI Application Examples

pretty-loguru integrates perfectly with FastAPI, providing beautiful and practical API logging features. This page demonstrates how to fully leverage the visualization features of pretty-loguru in a FastAPI application.

## 🚀 Basic Integration

### Simple FastAPI Application

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pretty_loguru import create_logger
import time
import uvicorn

# Initialize the logging system
logger = create_logger(
    name="fastapi_demo",
    log_dir="fastapi_logs", preset="development",
    level="INFO"
)

app = FastAPI(title="Pretty Loguru API Demo", version="1.1.2")

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.ascii_header("API START", font="slant", border_style="blue")
    
    logger.block(
        "FastAPI Application Startup",
        [
            "🚀 Application Name: Pretty Loguru API Demo",
            "📦 Version: 1.1.2",
            "🌐 Environment: Development",
            "📝 Logging System: pretty-loguru",
            "⚡ Status: Ready"
        ],
        border_style="green",
        level="SUCCESS"
    )

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.ascii_header("SHUTDOWN", font="standard", border_style="yellow")
    logger.warning("FastAPI application is shutting down...")

@app.get("/")
async def root():
    logger.info("Received request to root path")
    return {"message": "Hello World", "status": "success"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Performing health check")
    
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.1.2"
    }
    
    logger.block(
        "Health Check Result",
        [
            "✅ Application Status: Normal",
            "✅ Database: Connected",
            "✅ Cache: Running",
            f"⏰ Check Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        ],
        border_style="green"
    )
    
    return health_status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔧 Middleware Integration

### Request Logging Middleware

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

class PrettyLoguruMiddleware(BaseHTTPMiddleware):
    """Pretty Loguru Logging Middleware"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        method = request.method
        url = str(request.url)
        
        logger.block(
            "New API Request",
            [
                f"🌐 Method: {method}",
                f"📍 URL: {url}",
                f"⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            ],
            border_style="blue"
        )
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            color = "green" if response.status_code < 400 else "red"
            level = "SUCCESS" if response.status_code < 400 else "ERROR"
            
            logger.block(
                "Request Processing Complete",
                [
                    f"📊 Status Code: {response.status_code}",
                    f"⏱️  Processing Time: {process_time:.3f}s"
                ],
                border_style=color,
                level=level
            )
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            
            logger.ascii_block(
                "Request Processing Failed",
                [
                    f"❌ Error: {str(e)}",
                    f"⏱️  Processing Time: {process_time:.3f}s"
                ],
                header_text="ERROR",
                border_style="red",
                level="ERROR"
            )
            
            raise

# Apply middleware
app = FastAPI()
app.add_middleware(PrettyLoguruMiddleware)
```

## 📊 Business Logic Logging

### User Authentication System

```python
class AuthService:
    """Authentication Service"""
    
    async def login(self, username: str, password: str):
        """User login"""
        logger.block(
            "User Login Attempt",
            [
                f"👤 Username: {username}",
                f"🕐 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            ],
            border_style="cyan"
        )
        
        if username == "admin" and password == "password":
            logger.ascii_block(
                "Login Successful",
                [
                    f"✅ User: {username}",
                    f"🎯 Status: Authenticated"
                ],
                header_text="SUCCESS",
                border_style="green",
                level="SUCCESS"
            )
            return {"access_token": "fake-token", "token_type": "bearer"}
        else:
            logger.ascii_block(
                "Login Failed",
                [
                    f"❌ User: {username}",
                    f"🚫 Reason: Invalid credentials"
                ],
                header_text="FAILED",
                border_style="red",
                level="WARNING"
            )
            raise HTTPException(
                status_code=401,
                detail="Authentication failed"
            )

auth_service = AuthService()

@app.post("/login")
async def login_endpoint(username: str, password: str):
    return await auth_service.login(username, password)
```
This complete FastAPI example demonstrates the powerful features of pretty-loguru in a real web application, providing professional-grade logging and monitoring capabilities!
