"""
Logger Registry and Event System

This module provides a centralized registry for logger instances and a simple
publish/subscribe mechanism to allow different parts of the library to
communicate without direct dependencies.
"""

from typing import Dict, Callable, List, Optional, Any
from ..types import EnhancedLogger

# Global registry for logger instances
_logger_registry: Dict[str, EnhancedLogger] = {}

# Global registry for event listeners
_listeners: Dict[str, List[Callable]] = {}

def register_logger(name: str, logger: EnhancedLogger) -> None:
    """Registers a logger instance by name."""
    _logger_registry[name] = logger

def get_logger(name: str) -> Optional[EnhancedLogger]:
    """Retrieves a logger instance by name."""
    return _logger_registry.get(name)

def unregister_logger(name: str) -> bool:
    """Unregisters a logger instance by name."""
    if name in _logger_registry:
        del _logger_registry[name]
        return True
    return False

def list_loggers() -> List[str]:
    """Lists the names of all registered loggers."""
    return list(_logger_registry.keys())

def subscribe(event_name: str, callback: Callable) -> None:
    """Subscribes a callback to a specific event."""
    if event_name not in _listeners:
        _listeners[event_name] = []
    _listeners[event_name].append(callback)

def post_event(event_name: str, *args: Any, **kwargs: Any) -> None:
    """Posts an event, triggering all subscribed callbacks."""
    if event_name in _listeners:
        for callback in _listeners[event_name]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Error in event listener for '{event_name}': {e}")

def register_extension_method(
    logger_instance: Any,
    method_name: str,
    method_function: Any,
    overwrite: bool = False
) -> bool:
    """
    註冊自定義擴展方法到 logger 實例
    
    此函數允許用戶動態地擴展 logger 的功能。
    
    Args:
        logger_instance: 要添加方法的 logger 實例
        method_name: 方法名稱
        method_function: 方法函數
        overwrite: 如果方法已存在，是否覆蓋，預設為 False
        
    Returns:
        bool: 如果成功註冊則返回 True，否則返回 False
        
    Examples:
        >>> def my_custom_log(self, message, *args, **kwargs):
        ...     self.info(f"CUSTOM: {message}", *args, **kwargs)
        >>> 
        >>> register_extension_method(logger, "custom", my_custom_log)
        >>> logger.custom("Hello, world!")  # 輸出: "CUSTOM: Hello, world!"
    """
    # 檢查方法是否已存在
    if hasattr(logger_instance, method_name) and not overwrite:
        if hasattr(logger_instance, "warning"):
            logger_instance.warning(f"方法 '{method_name}' 已存在，未註冊。若要覆蓋，請使用 overwrite=True。")
        return False
    
    # 設置方法到 logger 實例
    setattr(logger_instance, method_name, method_function.__get__(logger_instance, type(logger_instance)))
    
    # 記錄註冊信息
    if hasattr(logger_instance, "debug"):
        logger_instance.debug(f"Registered custom method: {method_name}")
    
    return True
