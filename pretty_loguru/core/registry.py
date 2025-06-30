"""
Logger Registry Module

This module provides a centralized registry for logger instances with
thread-safe operations.

Thread Safety: All registry operations are protected with RLock for concurrent access.
"""

import threading
from typing import Dict, List, Optional
from ..types import EnhancedLogger
from .event_system import post_event

# Thread-safe lock for protecting registry state
_registry_lock = threading.RLock()

# Global registry for logger instances
_logger_registry: Dict[str, EnhancedLogger] = {}

def register_logger(name: str, logger: EnhancedLogger) -> None:
    """Registers a logger instance by name. Thread-safe."""
    with _registry_lock:
        _logger_registry[name] = logger
        # Notify subscribers about logger registration
        post_event("logger_registered", name, logger)

def get_logger(name: str) -> Optional[EnhancedLogger]:
    """Retrieves a logger instance by name. Thread-safe."""
    with _registry_lock:
        return _logger_registry.get(name)

def unregister_logger(name: str) -> bool:
    """Unregisters a logger instance by name. Thread-safe."""
    with _registry_lock:
        if name in _logger_registry:
            del _logger_registry[name]
            return True
        return False

def list_loggers() -> List[str]:
    """Lists the names of all registered loggers. Thread-safe."""
    with _registry_lock:
        return list(_logger_registry.keys())

def update_logger(name: str, logger: EnhancedLogger) -> bool:
    """Updates an existing logger instance by name. Thread-safe."""
    with _registry_lock:
        if name in _logger_registry:
            _logger_registry[name] = logger
            # Notify subscribers about logger update
            post_event("logger_updated", name, logger)
            return True
        return False
