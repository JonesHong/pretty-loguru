"""
Logger Proxy 模組

此模組提供 LoggerProxy 類，解決 logger 實例在重新初始化後
其他模組無法同步到新實例的問題。
"""

from typing import Any, Optional, Callable
import warnings
from ..types import EnhancedLogger


class LoggerProxy:
    """
    Logger 代理類
    
    這個類作為真實 logger 的代理，確保所有引用都能獲得最新的 logger 實例。
    當真實的 logger 被重新初始化時，所有通過 proxy 的調用都會自動使用新的實例。
    """
    
    def __init__(self, target_logger: EnhancedLogger, registry_name: Optional[str] = None):
        """
        初始化 Logger Proxy
        
        Args:
            target_logger: 目標 logger 實例
            registry_name: 在註冊表中的名稱，用於獲取最新實例
        """
        self._target_logger = target_logger
        self._registry_name = registry_name
        self._registry_getter: Optional[Callable[[str], Optional[EnhancedLogger]]] = None
    
    def set_registry_getter(self, getter_func: Callable[[str], Optional[EnhancedLogger]]):
        """
        設定註冊表 getter 函數
        
        Args:
            getter_func: 從註冊表獲取 logger 的函數
        """
        self._registry_getter = getter_func
    
    def _get_current_logger(self) -> EnhancedLogger:
        """獲取當前的真實 logger"""
        # 如果有註冊表且有名稱，嘗試從註冊表獲取最新實例
        if self._registry_getter and self._registry_name:
            registry_logger = self._registry_getter(self._registry_name)
            if registry_logger is not None:
                # 如果註冊表中的是另一個 proxy，取其真實 logger
                if isinstance(registry_logger, LoggerProxy):
                    return registry_logger._target_logger
                return registry_logger
        
        # 否則使用目標 logger
        return self._target_logger
    
    def update_target(self, new_logger: EnhancedLogger):
        """
        更新目標 logger
        
        Args:
            new_logger: 新的 logger 實例
        """
        self._target_logger = new_logger
    
    def get_real_logger(self) -> EnhancedLogger:
        """
        獲取真實的 logger 實例
        
        Returns:
            EnhancedLogger: 當前的真實 logger 實例
        """
        return self._get_current_logger()
    
    def console_debug(self, message: str, *args, **kwargs):
        """Logs a DEBUG message to the console only."""
        self._get_current_logger().bind(to_console_only=True).debug(message, *args, **kwargs)

    def console_info(self, message: str, *args, **kwargs):
        """Logs an INFO message to the console only."""
        self._get_current_logger().bind(to_console_only=True).info(message, *args, **kwargs)

    def console_warning(self, message: str, *args, **kwargs):
        """Logs a WARNING message to the console only."""
        self._get_current_logger().bind(to_console_only=True).warning(message, *args, **kwargs)

    def console_error(self, message: str, *args, **kwargs):
        """Logs an ERROR message to the console only."""
        self._get_current_logger().bind(to_console_only=True).error(message, *args, **kwargs)

    def console_success(self, message: str, *args, **kwargs):
        """Logs a SUCCESS message to the console only."""
        self._get_current_logger().bind(to_console_only=True).success(message, *args, **kwargs)

    def console_critical(self, message: str, *args, **kwargs):
        """Logs a CRITICAL message to the console only."""
        self._get_current_logger().bind(to_console_only=True).critical(message, *args, **kwargs)

    def file_debug(self, message: str, *args, **kwargs):
        """Logs a DEBUG message to the file only."""
        self._get_current_logger().bind(to_log_file_only=True).debug(message, *args, **kwargs)

    def file_info(self, message: str, *args, **kwargs):
        """Logs an INFO message to the file only."""
        self._get_current_logger().bind(to_log_file_only=True).info(message, *args, **kwargs)

    def file_warning(self, message: str, *args, **kwargs):
        """Logs a WARNING message to the file only."""
        self._get_current_logger().bind(to_log_file_only=True).warning(message, *args, **kwargs)

    def file_error(self, message: str, *args, **kwargs):
        """Logs an ERROR message to the file only."""
        self._get_current_logger().bind(to_log_file_only=True).error(message, *args, **kwargs)

    def file_success(self, message: str, *args, **kwargs):
        """Logs a SUCCESS message to the file only."""
        self._get_current_logger().bind(to_log_file_only=True).success(message, *args, **kwargs)

    def file_critical(self, message: str, *args, **kwargs):
        """Logs a CRITICAL message to the file only."""
        self._get_current_logger().bind(to_log_file_only=True).critical(message, *args, **kwargs)

    # 代理所有 logger 方法
    def __getattr__(self, name: str) -> Any:
        """代理屬性和方法調用到真實的 logger"""
        real_logger = self._get_current_logger()
        attr = getattr(real_logger, name)
        
        # 如果是方法，包裝一下以確保使用最新的 logger
        if callable(attr):
            def wrapper(*args, **kwargs):
                # By adding .opt(depth=1), we tell Loguru to look one level up in the call stack
                # to find the correct function name, line number, etc.
                current_logger = self._get_current_logger().opt(depth=1)
                return getattr(current_logger, name)(*args, **kwargs)
            return wrapper
        
        return attr
    
    def __repr__(self) -> str:
        real_logger = self._get_current_logger()
        return f"LoggerProxy(target={repr(real_logger)}, registry_name={self._registry_name})"


def create_logger_proxy(logger: EnhancedLogger, name: Optional[str] = None) -> LoggerProxy:
    """
    創建 Logger Proxy
    
    Args:
        logger: 要代理的 logger 實例
        name: logger 在註冊表中的名稱
        
    Returns:
        LoggerProxy: logger 代理實例
    """
    proxy = LoggerProxy(logger, name)
    
    # 嘗試設定註冊表 getter - 延遲導入避免循環導入
    def _delayed_get_logger(logger_name: str) -> Optional['EnhancedLogger']:
        try:
            from .creator import _logger_registry
            return _logger_registry.get(logger_name)
        except ImportError:
            return None
    
    proxy.set_registry_getter(_delayed_get_logger)
    
    return proxy