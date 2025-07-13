# Pretty Loguru Event System Usage Guide

## Overview

Pretty Loguru provides a clean publish/subscribe event system that allows decoupled communication between different modules. This system is thread-safe and suitable for complex applications.

## Core Features

### Basic API

```python
from pretty_loguru.core.event_system import subscribe, post_event, unsubscribe

# Subscribe to events
subscribe("event_name", callback_function)

# Publish events
post_event("event_name", *args, **kwargs)

# Unsubscribe
unsubscribe("event_name", callback_function)
```

## Built-in Events

### 1. Logger Registration Event

Triggered when a new Logger is registered into the system.

```python
from pretty_loguru.core.event_system import subscribe
from pretty_loguru import create_logger

def on_logger_registered(name, logger):
    print(f"New Logger registered: {name}")
    print(f"Logger type: {type(logger)}")

# Subscribe to logger registration event
subscribe("logger_registered", on_logger_registered)

# Creating a logger will trigger the event
logger = create_logger("my_app")
# Output: New Logger registered: my_app
```

### 2. Logger Update Event

Triggered when an existing Logger is updated.

```python
def on_logger_updated(name, new_logger):
    print(f"Logger '{name}' has been updated")
    print(f"New Logger instance: {id(new_logger)}")

subscribe("logger_updated", on_logger_updated)

# Recreating a logger with the same name triggers update event
updated_logger = create_logger("my_app", force_new_instance=True)
```

## Usage Examples

### Example 1: Logger Monitoring System

Create a monitoring system to track all Logger creation and usage:

```python
from pretty_loguru.core.event_system import subscribe
from pretty_loguru import create_logger
from datetime import datetime
from typing import Dict, Any

class LoggerMonitor:
    def __init__(self):
        self.logger_registry: Dict[str, Dict[str, Any]] = {}
        
        # Subscribe to relevant events
        subscribe("logger_registered", self.on_logger_registered)
        subscribe("logger_updated", self.on_logger_updated)
    
    def on_logger_registered(self, name: str, logger):
        """Handle Logger registration event"""
        self.logger_registry[name] = {
            'logger': logger,
            'created_at': datetime.now(),
            'updated_at': None,
            'update_count': 0
        }
        print(f"📝 Logger '{name}' registered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def on_logger_updated(self, name: str, new_logger):
        """Handle Logger update event"""
        if name in self.logger_registry:
            self.logger_registry[name]['logger'] = new_logger
            self.logger_registry[name]['updated_at'] = datetime.now()
            self.logger_registry[name]['update_count'] += 1
            
            update_count = self.logger_registry[name]['update_count']
            print(f"🔄 Logger '{name}' updated (update #{update_count})")
    
    def get_stats(self):
        """Get monitoring statistics"""
        total_loggers = len(self.logger_registry)
        updated_loggers = sum(1 for info in self.logger_registry.values() if info['updated_at'])
        
        return {
            'total_loggers': total_loggers,
            'updated_loggers': updated_loggers,
            'logger_names': list(self.logger_registry.keys())
        }

# Using the monitoring system
monitor = LoggerMonitor()

# Create some loggers
app_logger = create_logger("app")
db_logger = create_logger("database") 
cache_logger = create_logger("cache")

# Update a logger
updated_app_logger = create_logger("app", force_new_instance=True)

# View statistics
stats = monitor.get_stats()
print(f"Statistics: {stats}")
```

### Example 2: Custom Event System

Create application-specific events:

```python
from pretty_loguru.core.event_system import subscribe, post_event
from pretty_loguru import create_logger

class DatabaseConnectionManager:
    def __init__(self):
        self.logger = create_logger("db_manager")
        
        # Subscribe to connection events
        subscribe("db_connected", self.on_db_connected)
        subscribe("db_disconnected", self.on_db_disconnected)
    
    def connect(self):
        """Simulate database connection"""
        # Execute connection logic...
        connection_info = {"host": "localhost", "port": 5432, "database": "myapp"}
        
        # Publish connection event
        post_event("db_connected", connection_info)
    
    def disconnect(self):
        """Simulate database disconnection"""
        # Execute disconnection logic...
        post_event("db_disconnected", reason="manual_disconnect")
    
    def on_db_connected(self, connection_info):
        """Handle database connection event"""
        self.logger.info(f"Database connected: {connection_info}")
    
    def on_db_disconnected(self, reason):
        """Handle database disconnection event"""
        self.logger.warning(f"Database disconnected, reason: {reason}")

# Create other listeners
def audit_db_events(event_type, **kwargs):
    audit_logger = create_logger("audit")
    audit_logger.info(f"Database audit: {event_type} - {kwargs}")

subscribe("db_connected", lambda info: audit_db_events("connected", info=info))
subscribe("db_disconnected", lambda reason: audit_db_events("disconnected", reason=reason))

# Usage
db_manager = DatabaseConnectionManager()
db_manager.connect()    # Triggers connection event
db_manager.disconnect() # Triggers disconnection event
```

### Example 3: Performance Monitoring Events

```python
from pretty_loguru.core.event_system import subscribe, post_event
import time
import functools

def performance_monitor(func):
    """Performance monitoring decorator"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            raise
        finally:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            # Publish performance event
            post_event("function_executed", {
                'function_name': func.__name__,
                'execution_time': execution_time,
                'success': success,
                'error': error,
                'args_count': len(args),
                'kwargs_count': len(kwargs)
            })
        
        return result
    return wrapper

# Performance event listener
def log_performance_event(event_data):
    perf_logger = create_logger("performance")
    
    func_name = event_data['function_name']
    exec_time = event_data['execution_time']
    success = event_data['success']
    
    if success:
        perf_logger.info(f"✅ {func_name} completed, took: {exec_time:.4f}s")
    else:
        perf_logger.error(f"❌ {func_name} failed, took: {exec_time:.4f}s, error: {event_data['error']}")

subscribe("function_executed", log_performance_event)

# Usage example
@performance_monitor
def slow_function():
    time.sleep(0.1)  # Simulate time-consuming operation
    return "Done"

@performance_monitor
def failing_function():
    raise ValueError("Simulated error")

# Test
slow_function()     # Triggers performance event
try:
    failing_function()  # Triggers error event
except ValueError:
    pass
```

## Best Practices

### 1. Event Naming Conventions

```python
# ✅ Good event names
"logger_registered"     # Clear action
"db_connection_lost"    # Specific state change
"user_login_success"    # Includes result

# ❌ Avoid these names
"event1"               # Not descriptive
"stuff_happened"       # Too vague
"update"              # Too generic
```

### 2. Error Handling

```python
def safe_event_handler(data):
    """Safe event handler with error handling"""
    try:
        # Event processing logic
        process_event_data(data)
    except Exception as e:
        # Log error but don't raise to avoid affecting other listeners
        error_logger = create_logger("event_errors")
        error_logger.error(f"Event processing failed: {e}")

subscribe("my_event", safe_event_handler)
```

### 3. Avoiding Memory Leaks

```python
class EventSubscriber:
    def __init__(self):
        self.callbacks = []
        
    def subscribe_to_events(self):
        """Subscribe to events and record callbacks"""
        callback = self.handle_event
        subscribe("my_event", callback)
        self.callbacks.append(("my_event", callback))
    
    def cleanup(self):
        """Clean up by unsubscribing all"""
        for event_name, callback in self.callbacks:
            unsubscribe(event_name, callback)
        self.callbacks.clear()
    
    def handle_event(self, data):
        # Handle event...
        pass
```

### 4. Thread Safety Considerations

The event system itself is thread-safe, but event handlers need to consider thread safety:

```python
import threading

class ThreadSafeEventHandler:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}
    
    def handle_event(self, event_data):
        """Thread-safe event handling"""
        with self.lock:
            # Safely modify shared data
            self.data.update(event_data)

subscribe("shared_data_update", ThreadSafeEventHandler().handle_event)
```

## Important Notes

1. **Avoid Circular Dependencies**: Ensure event handlers don't trigger events that lead to infinite loops
2. **Keep Handlers Lightweight**: Event handlers should execute quickly to avoid blocking the system
3. **Error Isolation**: An error in one handler shouldn't affect other handlers
4. **Resource Cleanup**: Long-running applications should properly clean up unused event subscriptions

## Debugging the Event System

```python
from pretty_loguru.core.event_system import list_events, list_listeners

# View all registered events
events = list_events()
print(f"Registered events: {events}")

# View number of listeners for a specific event
listeners = list_listeners("logger_registered")
print(f"logger_registered event has {len(listeners)} listeners")
```

The event system provides Pretty Loguru with powerful extensibility, allowing users to add custom functionality without modifying core code. Proper use of the event system can make your application more modular and maintainable.