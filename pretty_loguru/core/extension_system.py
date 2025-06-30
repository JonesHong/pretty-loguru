"""
擴展系統模組

此模組提供動態擴展 Logger 功能的機制，
允許註冊自定義方法到 Logger 實例中。
"""

from typing import Any, Callable, Dict
from functools import wraps


# 全局註冊表，用於存儲擴展方法
_extension_methods: Dict[str, Callable] = {}


def register_extension_method(logger_instance: Any, name: str, method: Callable, overwrite: bool = False) -> None:
    """
    註冊擴展方法並直接綁定到 Logger 實例
    
    Args:
        logger_instance: Logger 實例
        name: 方法名稱
        method: 要註冊的方法
        overwrite: 是否覆蓋已存在的方法
    """
    # 檢查是否已存在該方法
    if hasattr(logger_instance, name) and not overwrite:
        raise ValueError(f"Method '{name}' already exists on logger instance. Use overwrite=True to replace it.")
    
    # 將方法綁定到 logger 實例
    if hasattr(method, '__get__'):
        # 如果是綁定方法，直接綁定
        bound_method = method.__get__(logger_instance, type(logger_instance))
    else:
        # 如果是普通函數，創建綁定方法
        bound_method = method
    
    setattr(logger_instance, name, bound_method)
    
    # 同時保存到全局註冊表以便查詢
    _extension_methods[name] = method


def get_extension_method(name: str) -> Callable:
    """
    獲取已註冊的擴展方法
    
    Args:
        name: 方法名稱
        
    Returns:
        註冊的方法，如果不存在則返回None
    """
    return _extension_methods.get(name)


def apply_extensions(logger_instance: Any) -> None:
    """
    將所有已註冊的擴展方法應用到 Logger 實例
    
    Args:
        logger_instance: Logger 實例
    """
    for name, method in _extension_methods.items():
        # 將方法綁定到 logger 實例
        bound_method = method.__get__(logger_instance, type(logger_instance))
        setattr(logger_instance, name, bound_method)


def list_extensions() -> Dict[str, Callable]:
    """
    列出所有已註冊的擴展方法
    
    Returns:
        擴展方法字典
    """
    return _extension_methods.copy()


def clear_extensions() -> None:
    """
    清除所有已註冊的擴展方法
    """
    _extension_methods.clear()