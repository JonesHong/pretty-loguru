"""
Event System Module

This module provides a publish/subscribe mechanism to allow different parts
of the library to communicate without direct dependencies.

Thread Safety: All event operations are protected with RLock for concurrent access.

Built-in Events:
- "logger_registered": Triggered when a new logger is registered
- "logger_updated": Triggered when an existing logger is updated

Usage Example:
    from pretty_loguru.core.event_system import subscribe, post_event
    
    def my_handler(name, logger):
        print(f"Logger {name} was registered")
    
    subscribe("logger_registered", my_handler)
    
    # Event will be triggered automatically when creating loggers
    from pretty_loguru import create_logger
    logger = create_logger("my_app")  # Triggers the event

For more examples, see: docs/event_system_examples.md
"""

import threading
from typing import Dict, Callable, List, Any

# Thread-safe lock for protecting event system state
_event_lock = threading.RLock()

# Global registry for event listeners
_listeners: Dict[str, List[Callable]] = {}

def subscribe(event_name: str, callback: Callable) -> None:
    """Subscribes a callback to a specific event. Thread-safe."""
    with _event_lock:
        if event_name not in _listeners:
            _listeners[event_name] = []
        _listeners[event_name].append(callback)

def unsubscribe(event_name: str, callback: Callable) -> bool:
    """Unsubscribes a callback from a specific event. Thread-safe."""
    with _event_lock:
        if event_name in _listeners and callback in _listeners[event_name]:
            _listeners[event_name].remove(callback)
            # Clean up empty event lists
            if not _listeners[event_name]:
                del _listeners[event_name]
            return True
        return False

def post_event(event_name: str, *args: Any, **kwargs: Any) -> None:
    """Posts an event, triggering all subscribed callbacks. Thread-safe."""
    # Get a copy of callbacks under lock to minimize lock time
    with _event_lock:
        callbacks = _listeners.get(event_name, []).copy()
    
    # Execute callbacks outside the lock to prevent deadlocks
    for callback in callbacks:
        try:
            callback(*args, **kwargs)
        except Exception as e:
            print(f"Error in event listener for '{event_name}': {e}")

def list_events() -> List[str]:
    """Lists all registered event names. Thread-safe."""
    with _event_lock:
        return list(_listeners.keys())

def clear_events() -> None:
    """Clears all event listeners. Thread-safe."""
    with _event_lock:
        _listeners.clear()

def list_listeners(event_name: str) -> List[Callable]:
    """Lists all listeners for a specific event. Thread-safe."""
    with _event_lock:
        return _listeners.get(event_name, []).copy()

def event_count() -> int:
    """Returns the total number of registered events. Thread-safe."""
    with _event_lock:
        return len(_listeners)

def listener_count(event_name: str) -> int:
    """Returns the number of listeners for a specific event. Thread-safe."""
    with _event_lock:
        return len(_listeners.get(event_name, []))