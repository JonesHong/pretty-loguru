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

def clear_registry() -> int:
    """Clears all registered loggers. Returns the number of loggers cleared. Thread-safe."""
    with _registry_lock:
        count = len(_logger_registry)
        _logger_registry.clear()
        # Notify subscribers about registry clear
        post_event("registry_cleared", count=count)
        return count

def get_registry_size() -> int:
    """Returns the number of registered loggers. Thread-safe."""
    with _registry_lock:
        return len(_logger_registry)

def cleanup_unused_loggers() -> int:
    """
    Cleans up loggers that appear to be unused.
    This is a basic implementation that could be extended with more sophisticated checks.
    Returns the number of loggers removed.
    Thread-safe.
    """
    with _registry_lock:
        # 在實際應用中，您可能會檢查 logger 是否正在使用
        # 這裡我們只提供基本的框架
        removed_count = 0
        
        # 目前只是一個空的實現，可以在未來擴展
        # 例如：檢查 logger 的最後使用時間、引用計數等
        
        return removed_count
