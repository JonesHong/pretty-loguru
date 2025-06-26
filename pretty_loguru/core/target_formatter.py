"""
目標導向格式化工具模組

此模組提供用於創建目標導向格式化方法的工具函數，
使得能夠輕鬆添加 file_xxx 和 console_xxx 方法。
"""

from typing import Any, Callable, Dict, List, Optional, Set, Union, TypeVar, cast

from rich.console import Console

F = TypeVar('F', bound=Callable)


import inspect

def create_target_method(
    original_method: Callable,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    name_prefix: str = "",
) -> Callable:
    if to_console_only and to_log_file_only:
        raise ValueError("to_console_only 和 to_log_file_only 不能同時為 True")

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 動態計算堆棧深度
        stack = inspect.stack()
        depth = 4  # 默認深度（適用於直接調用）
        for frame in stack:
            if frame.function == "<module>":
                depth -= 1  # 如果檢測到模組級調用，增加深度
                break
            if frame.function == "wrapper":
                depth += 1  # 如果檢測到模組級調用，增加深度
                break
        
        # 添加目標導向參數
        kwargs['to_console_only'] = to_console_only
        kwargs['to_log_file_only'] = to_log_file_only
        kwargs['_target_depth'] = depth  # 使用動態計算的深度
        
        return original_method(*args, **kwargs)

    method_type = "console" if to_console_only else "file" if to_log_file_only else "both"
    wrapper.__name__ = f"{name_prefix}_{method_type}" if name_prefix else f"{method_type}_method"
    
    if original_method.__doc__:
        target_info = "僅輸出到控制台" if to_console_only else "僅輸出到文件" if to_log_file_only else "輸出到控制台和文件"
        wrapper.__doc__ = f"{original_method.__doc__}\n\n此版本{target_info}。"
    
    return wrapper

def add_target_methods(
    logger_instance: Any,
    method_name: str,
    original_method: Callable,
) -> None:
    """
    為 logger 實例添加目標導向的格式化方法版本

    Args:
        logger_instance: 要添加方法的 logger 實例
        method_name: 方法的基本名稱 (如 'block', 'ascii_header')
        original_method: 原始的格式化方法

    Example:
        ::
            # 假設 logger_instance 已有 block 方法
            add_target_methods(logger_instance, 'block', logger_instance.block)
            
            # 現在 logger_instance 將有 console_block 和 file_block 方法
    """
    # 創建僅控制台版本
    console_method = create_target_method(
        original_method,
        to_console_only=True,
        to_log_file_only=False,
        name_prefix=method_name
    )
    
    # 創建僅文件版本
    file_method = create_target_method(
        original_method,
        to_console_only=False,
        to_log_file_only=True,
        name_prefix=method_name
    )
    
    # 添加到 logger 實例
    setattr(logger_instance, f"console_{method_name}", console_method)
    setattr(logger_instance, f"file_{method_name}", file_method)


def ensure_target_parameters(method: Callable) -> Callable:
    """
    確保方法接受目標導向參數

    這個裝飾器用於確保格式化方法接受 to_console_only 和 to_log_file_only 參數。
    這對於創建新的格式化方法很有用。

    Args:
        method: 要裝飾的方法

    Returns:
        Callable: 確保接受目標導向參數的方法
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 確保關鍵參數存在，即使調用時未提供
        if 'to_console_only' not in kwargs:
            kwargs['to_console_only'] = False
        if 'to_log_file_only' not in kwargs:
            kwargs['to_log_file_only'] = False
        if '_target_depth' not in kwargs:
            kwargs['_target_depth'] = 4  # 默認深度
        
        return method(*args, **kwargs)
    
    # 複製原始方法的元數據
    wrapper.__name__ = method.__name__
    wrapper.__doc__ = method.__doc__
    
    return wrapper