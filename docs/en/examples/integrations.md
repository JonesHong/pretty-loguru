# Framework Integration Examples

Demonstrating how to integrate Pretty-Loguru with various Python frameworks, especially FastAPI and Uvicorn.

## FastAPI Basic Integration

The simplest way to integrate with FastAPI:

```python
from fastapi import FastAPI
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

# Create FastAPI app
app = FastAPI(title="My API")

# Setup logging
setup_fastapi_logging(
    app,
    log_path="logs/api",
    level="INFO"
)

@app.get("/")
async def root():
    # Requests and responses are automatically logged
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Errors are automatically caught and logged
    if item_id == 0:
        raise ValueError("Invalid item ID")
    return {"item_id": item_id}

# Run: uvicorn main:app --reload
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/simple_api.py)

## Middleware Logging

Using middleware to log all requests:

```python
from fastapi import FastAPI, Request
from pretty_loguru import create_logger
import time

app = FastAPI()
logger = create_logger("api", log_path="logs/api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    start_time = time.time()
    
    # Log request info
    logger.info(f"📥 {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response info
    logger.info(
        f"📤 {request.method} {request.url.path} "
        f"- {response.status_code} ({process_time:.3f}s)"
    )
    
    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/slow")
async def slow_endpoint():
    """Simulate slow endpoint"""
    import asyncio
    await asyncio.sleep(2)
    return {"message": "Finally done!"}
```

Output example:
```
2024-01-20 15:30:00 | INFO | 📥 GET /slow
2024-01-20 15:30:02 | INFO | 📤 GET /slow - 200 (2.003s)
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/middleware_demo.py)

## Dependency Injection

Using FastAPI's dependency injection system to manage loggers:

```python
from fastapi import FastAPI, Depends
from typing import Annotated
from pretty_loguru import create_logger, EnhancedLogger
import uuid

app = FastAPI()

# Create base logger
base_logger = create_logger("api", log_path="logs/api")

async def get_logger() -> EnhancedLogger:
    """Provide logger as dependency"""
    return base_logger

async def get_request_logger(
    logger: Annotated[EnhancedLogger, Depends(get_logger)]
) -> EnhancedLogger:
    """Create request-specific logger"""
    request_id = str(uuid.uuid4())
    return logger.bind(request_id=request_id)

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    logger: Annotated[EnhancedLogger, Depends(get_request_logger)]
):
    """Endpoint with injected logger"""
    logger.info(f"Fetching user {user_id}")
    
    # Simulate database query
    user = {"id": user_id, "name": f"User {user_id}"}
    
    logger.success(f"Found user: {user['name']}")
    return user

@app.post("/users")
async def create_user(
    user_data: dict,
    logger: Annotated[EnhancedLogger, Depends(get_request_logger)]
):
    """Create new user with logging"""
    logger.info("Creating new user", user_data=user_data)
    
    # Simulate user creation
    new_user = {"id": 123, **user_data}
    
    logger.success(f"User created with ID: {new_user['id']}")
    return new_user
```

[View complete code](https://github.com/JonesHong/pretty-loguru/blob/master/examples/05_integrations/dependency_injection.py)

## Advanced FastAPI Integration

Comprehensive integration with structured logging:

```python
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from pretty_loguru import create_logger
import time
import json
from contextlib import asynccontextmanager

# Create logger
logger = create_logger("api", log_path="logs/api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.ascii_header("API STARTING", font="slant", border_style="green")
    logger.info("Initializing services...")
    
    # Initialize resources
    app.state.db = "Connected"  # Simulate DB connection
    
    logger.success("All services initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down services...")
    logger.ascii_header("API STOPPED", font="slant", border_style="yellow")

# Create app with lifespan
app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log validation errors"""
    logger.error(
        f"Validation error on {request.url.path}",
        errors=exc.errors(),
        body=exc.body
    )
    return Response(
        content=json.dumps({"detail": exc.errors()}),
        status_code=422,
        media_type="application/json"
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Log HTTP exceptions"""
    logger.warning(
        f"HTTP exception on {request.url.path}",
        status_code=exc.status_code,
        detail=exc.detail
    )
    return Response(
        content=json.dumps({"detail": exc.detail}),
        status_code=exc.status_code,
        media_type="application/json"
    )

class LoggingMiddleware:
    """Advanced logging middleware"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        
        # Extract request info
        request_info = {
            "method": scope["method"],
            "path": scope["path"],
            "query": scope.get("query_string", b"").decode(),
            "client": f"{scope['client'][0]}:{scope['client'][1]}"
                      if scope.get("client") else "unknown"
        }
        
        # Log request with visual block
        logger.console_block(
            "📥 Incoming Request",
            [
                f"Method: {request_info['method']}",
                f"Path: {request_info['path']}",
                f"Client: {request_info['client']}",
                f"Query: {request_info['query'] or 'None'}"
            ],
            border_style="blue"
        )
        
        # Process request
        status_code = 500
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response with color based on status
        if status_code < 400:
            border_color = "green"
            level = "success"
        elif status_code < 500:
            border_color = "yellow"
            level = "warning"
        else:
            border_color = "red"
            level = "error"
        
        logger.console_block(
            "📤 Response Sent",
            [
                f"Status: {status_code}",
                f"Duration: {duration:.3f}s",
                f"Path: {request_info['path']}"
            ],
            border_style=border_color,
            log_level=level.upper()
        )

# Add middleware
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def root():
    """Root endpoint with logging"""
    logger.info("Serving root endpoint")
    return {"message": "Advanced API with Pretty-Loguru"}

@app.get("/health")
async def health_check():
    """Health check with detailed logging"""
    logger.console_table(
        "System Health",
        [
            {"Component": "API", "Status": "🟢 Healthy", "Details": "Running"},
            {"Component": "Database", "Status": "🟢 Connected", "Details": "5ms ping"},
            {"Component": "Cache", "Status": "🟡 Warning", "Details": "High memory"}
        ]
    )
    return {"status": "healthy"}
```

## Uvicorn Integration

Integrating with Uvicorn server:

```python
from pretty_loguru.integrations.uvicorn import setup_uvicorn_logging
from pretty_loguru import create_logger
import uvicorn
from fastapi import FastAPI

# Create FastAPI app
app = FastAPI()

# Setup Uvicorn logging
logger = setup_uvicorn_logging(
    log_path="logs/server",
    level="INFO",
    access_log=True
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # Configure Uvicorn with Pretty-Loguru
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,  # Disable default logging
        access_log=False  # We handle this in Pretty-Loguru
    )
    
    # Custom server class with logging
    class LoggingServer(uvicorn.Server):
        def __init__(self, config):
            super().__init__(config)
            
        async def startup(self, sockets=None):
            logger.ascii_header("SERVER", font="block", border_style="green")
            logger.info(f"Starting server on {config.host}:{config.port}")
            await super().startup(sockets)
            logger.success("Server started successfully")
        
        async def shutdown(self, sockets=None):
            logger.info("Shutting down server...")
            await super().shutdown(sockets)
            logger.ascii_header("STOPPED", font="block", border_style="yellow")
    
    # Run server
    server = LoggingServer(config)
    server.run()
```

## Background Tasks with Logging

Logging in background tasks:

```python
from fastapi import FastAPI, BackgroundTasks
from pretty_loguru import create_logger
import asyncio

app = FastAPI()
logger = create_logger("tasks", log_path="logs/tasks")

async def process_data(item_id: int, logger: EnhancedLogger):
    """Background task with logging"""
    task_logger = logger.bind(
        task="process_data",
        item_id=item_id
    )
    
    task_logger.info("Starting background processing")
    
    try:
        # Simulate processing steps
        for step in range(1, 6):
            await asyncio.sleep(1)
            task_logger.info(f"Processing step {step}/5")
        
        task_logger.success("Processing completed")
        
    except Exception as e:
        task_logger.error(f"Processing failed: {e}")
        task_logger.exception("Full error details:")

@app.post("/process/{item_id}")
async def trigger_processing(
    item_id: int,
    background_tasks: BackgroundTasks
):
    """Trigger background processing"""
    logger.info(f"Received processing request for item {item_id}")
    
    # Add background task
    background_tasks.add_task(
        process_data,
        item_id,
        logger
    )
    
    return {
        "message": "Processing started",
        "item_id": item_id
    }

@app.get("/tasks/status")
async def task_status():
    """Show task processing status"""
    # In real app, query task status from database
    logger.console_tree(
        "Task Status",
        {
            "Running": {
                "process_data": ["item_123", "item_456"],
                "generate_report": ["report_789"]
            },
            "Completed": {
                "Today": "42 tasks",
                "This Week": "315 tasks"
            },
            "Failed": {
                "Recent": ["item_999 - Timeout", "item_888 - Invalid data"]
            }
        }
    )
    
    return {"status": "displayed in console"}
```

## WebSocket Logging

Logging WebSocket connections:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pretty_loguru import create_logger
import json

app = FastAPI()
logger = create_logger("websocket", log_path="logs/websocket")

class ConnectionManager:
    """Manage WebSocket connections with logging"""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.logger = logger.bind(component="ConnectionManager")
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"Client {client_id} connected")
        self.logger.console_panel(
            f"New WebSocket connection from {client_id}",
            title="🔌 Connected",
            border_style="green"
        )
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        self.logger.info(f"Client {client_id} disconnected")
        self.logger.console_panel(
            f"Client {client_id} disconnected",
            title="🔌 Disconnected",
            border_style="yellow"
        )
    
    async def broadcast(self, message: str, sender_id: str):
        self.logger.debug(f"Broadcasting from {sender_id}: {message}")
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Log received message
            logger.info(
                f"Message from {client_id}",
                content=data,
                connections=len(manager.active_connections)
            )
            
            # Broadcast to all
            await manager.broadcast(
                json.dumps({
                    "client_id": client_id,
                    "message": data
                }),
                client_id
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
```

## Next Steps

- [Production Examples](./production.md) - Production deployment
- [Enterprise Examples](./enterprise.md) - Enterprise features
- [API Reference](../api/) - Complete API documentation