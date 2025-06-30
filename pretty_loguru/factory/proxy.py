"""
Logger Proxy 模組

此模組提供 LoggerProxy 類，解決 logger 實例在重新初始化後
其他模組無法同步到新實例的問題。

Performance: Uses method caching to minimize wrapper function creation overhead.
"""

from typing import Any, Dict, Callable
from functools import lru_cache
from ..types import EnhancedLogger
from ..core import registry
from ..core.event_system import subscribe

class LoggerProxy:
    """
    Logger 代理類，確保所有引用都能獲得最新的 logger 實例。
    通過訂閱 registry 中的更新事件來自動更新目標 logger。
    
    Performance optimizations:
    - Method caching to reduce wrapper function creation
    - Cached attribute lookup for frequently accessed methods
    """
    def __init__(self, target_logger: EnhancedLogger, registry_name: str):
        self._target_logger = target_logger
        self._registry_name = registry_name
        self._method_cache: Dict[str, Callable] = {}
        # 訂閱更新事件
        subscribe("logger_updated", self._handle_update)

    def _handle_update(self, name: str, new_logger: EnhancedLogger):
        """處理來自 registry 的 logger 更新事件。"""
        if name == self._registry_name:
            # 如果是另一個 proxy，取其真實 logger
            if isinstance(new_logger, LoggerProxy):
                self._target_logger = new_logger.get_real_logger()
            else:
                self._target_logger = new_logger
            # 清除方法緩存，因為 logger 實例已更新
            self._method_cache.clear()

    def get_real_logger(self) -> EnhancedLogger:
        """獲取當前的真實 logger 實例。"""
        return self._target_logger

    

    def bind(self, **kwargs) -> "LoggerProxy":
        """
        代理 loguru 的 bind 方法，確保返回的仍然是 LoggerProxy 實例。
        """
        new_bound_logger = self.get_real_logger().bind(**kwargs)
        # 返回一個新的 LoggerProxy 實例，包裝這個綁定後的 logger
        return LoggerProxy(new_bound_logger, self._registry_name)

    def __getattr__(self, name: str) -> Any:
        """代理所有其他屬性和方法到真實的 logger。使用緩存優化性能。"""
        # 檢查方法緩存
        if name in self._method_cache:
            return self._method_cache[name]
        
        real_logger = self.get_real_logger()
        attr = getattr(real_logger, name)

        if callable(attr):
            # 為常用日誌方法創建優化的wrapper
            if name in ('debug', 'info', 'warning', 'error', 'success', 'critical', 'trace'):
                # 使用閉包捕獲方法名，避免每次查找
                method_name = name  # 固定方法名避免閉包問題
                
                def optimized_wrapper(*args, **kwargs):
                    # 獲取logger並緩存opt調用
                    real_logger = self.get_real_logger()
                    opt_logger = real_logger.opt(depth=1)
                    # 直接調用方法避免重複查找
                    return getattr(opt_logger, method_name)(*args, **kwargs)
                
                # 緩存優化的wrapper
                self._method_cache[name] = optimized_wrapper
                return optimized_wrapper
            else:
                # 其他方法使用標準wrapper但不緩存（避免內存洩漏）
                def wrapper(*args, **kwargs):
                    current_logger = self.get_real_logger().opt(depth=1)
                    return getattr(current_logger, name)(*args, **kwargs)
                return wrapper
        return attr

    def __repr__(self) -> str:
        return f"LoggerProxy(target={repr(self.get_real_logger())}, name={self._registry_name})"

def create_logger_proxy(logger: EnhancedLogger, name: str) -> LoggerProxy:
    """創建一個 Logger Proxy 實例。"""
    if not name:
        raise ValueError("A name is required to create a logger proxy.")
    return LoggerProxy(logger, name)