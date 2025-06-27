"""
Logger Proxy 模組

此模組提供 LoggerProxy 類，解決 logger 實例在重新初始化後
其他模組無法同步到新實例的問題。
"""

from typing import Any
from ..types import EnhancedLogger
from ..core import registry

class LoggerProxy:
    """
    Logger 代理類，確保所有引用都能獲得最新的 logger 實例。
    通過訂閱 registry 中的更新事件來自動更新目標 logger。
    """
    def __init__(self, target_logger: EnhancedLogger, registry_name: str):
        self._target_logger = target_logger
        self._registry_name = registry_name
        # 訂閱更新事件
        registry.subscribe("logger_updated", self._handle_update)

    def _handle_update(self, name: str, new_logger: EnhancedLogger):
        """處理來自 registry 的 logger 更新事件。"""
        if name == self._registry_name:
            # 如果是另一個 proxy，取其真實 logger
            if isinstance(new_logger, LoggerProxy):
                self._target_logger = new_logger.get_real_logger()
            else:
                self._target_logger = new_logger

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
        """代理所有其他屬性和方法到真實的 logger。"""
        real_logger = self.get_real_logger()
        attr = getattr(real_logger, name)

        if callable(attr):
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