"""
目標導向格式化工具模組

此模組提供用於創建目標導向格式化方法的工具函數，
使得能夠輕鬆添加 file_xxx 和 console_xxx 方法。

注意：此模組已簡化以遵循 KISS 原則，移除了過度複雜的深度計算邏輯。
"""

from typing import Any, Callable, Dict, List, Optional, Set, Union, TypeVar, cast

from rich.console import Console

F = TypeVar('F', bound=Callable)


def log_to_targets(
    logger_instance: Any,
    message: str,
    level: str = "INFO",
    console_only: bool = False,
    file_only: bool = False
) -> None:
    """
    目標日誌函數，支援分離的控制台和檔案輸出
    
    Args:
        logger_instance: Logger 實例
        message: 要記錄的消息
        level: 日誌級別
        console_only: 是否僅輸出到控制台
        file_only: 是否僅輸出到文件
    """
    if console_only and file_only:
        raise ValueError("console_only 和 file_only 不能同時為 True")
    
    if not file_only and logger_instance:
        # 輸出到控制台
        logger_instance.opt(depth=1).log(level, message)
    
    if not console_only and logger_instance and hasattr(logger_instance, '_core'):
        # 檢查是否有文件處理器
        has_file_handler = any(
            hasattr(handler, 'sink') and hasattr(handler.sink, 'write')
            for handler in logger_instance._core.handlers.values()
        )
        
        if has_file_handler:
            # 輸出到文件
            logger_instance.opt(depth=1).bind(to_log_file_only=True).log(level, message)


def format_decorator_basic(func):
    """
    簡化的格式化裝飾器，替代複雜的 ensure_target_parameters
    
    這個裝飾器添加基本的目標導向功能，不進行複雜的深度計算
    """
    def wrapper(*args, **kwargs):
        # 設置默認值，但不強制複雜的參數
        console_only = kwargs.pop('console_only', False)
        file_only = kwargs.pop('file_only', False)
        
        # 移除舊的複雜參數（如果存在）
        kwargs.pop('to_console_only', None)
        kwargs.pop('to_log_file_only', None)
        kwargs.pop('_target_depth', None)
        
        # 調用原始函數
        result = func(*args, **kwargs)
        
        # 如果函數返回消息且有 logger_instance，使用目標輸出
        if 'logger_instance' in kwargs and kwargs['logger_instance']:
            logger = kwargs['logger_instance']
            if hasattr(logger, 'info') and isinstance(result, str):
                log_to_targets(logger, result, "INFO", console_only, file_only)
        
        return result
    
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

def create_target_method(
    original_method: Callable,
    to_console_only: bool = False,
    to_log_file_only: bool = False,
    name_prefix: str = "",
) -> Callable:
    """簡化版的目標方法創建器，移除複雜的深度計算"""
    if to_console_only and to_log_file_only:
        raise ValueError("to_console_only 和 to_log_file_only 不能同時為 True")

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 簡化：使用固定深度，移除動態計算
        kwargs['to_console_only'] = to_console_only
        kwargs['to_log_file_only'] = to_log_file_only
        kwargs['_target_depth'] = 2  # 使用固定深度，簡化邏輯
        
        return original_method(*args, **kwargs)

    method_type = "console" if to_console_only else "file" if to_log_file_only else "both"
    wrapper.__name__ = f"{name_prefix}_{method_type}" if name_prefix else f"{method_type}_method"
    
    if original_method.__doc__:
        target_info = "僅輸出到控制台" if to_console_only else "僅輸出到文件" if to_log_file_only else "輸出到控制台和文件"
        wrapper.__doc__ = f"{original_method.__doc__}\n\n此版本{target_info}。"
    
    return wrapper

def create_target_methods_simple(logger_instance: Any, method_name: str, original_method) -> None:
    """
    為 logger 創建簡化的目標方法（從 simple_formatter 合併）
    
    Args:
        logger_instance: Logger 實例
        method_name: 方法名稱
        original_method: 原始方法
    """
    # 創建控制台專用方法
    def console_method(*args, **kwargs):
        kwargs['console_only'] = True
        return original_method(*args, **kwargs)
    
    # 創建文件專用方法
    def file_method(*args, **kwargs):
        kwargs['file_only'] = True
        return original_method(*args, **kwargs)
    
    # 設置方法名稱和文檔
    console_method.__name__ = f"console_{method_name}"
    file_method.__name__ = f"file_{method_name}"
    
    if original_method.__doc__:
        console_method.__doc__ = f"{original_method.__doc__}\n\n此版本僅輸出到控制台。"
        file_method.__doc__ = f"{original_method.__doc__}\n\n此版本僅輸出到文件。"
    
    # 添加到 logger 實例
    setattr(logger_instance, f"console_{method_name}", console_method)
    setattr(logger_instance, f"file_{method_name}", file_method)


def add_target_methods(
    logger_instance: Any,
    method_name: str,
    original_method: Callable,
    use_simple_mode: bool = False
) -> None:
    """
    為 logger 實例添加目標導向的格式化方法版本

    Args:
        logger_instance: 要添加方法的 logger 實例
        method_name: 方法的基本名稱 (如 'block', 'ascii_header')
        original_method: 原始的格式化方法
        use_simple_mode: 是否使用簡化模式 (向後兼容)

    Example:
        ::
            # 假設 logger_instance 已有 block 方法
            add_target_methods(logger_instance, 'block', logger_instance.block)
            
            # 現在 logger_instance 將有 console_block 和 file_block 方法
    """
    if use_simple_mode:
        # 使用簡化模式（向後兼容）
        create_target_methods_simple(logger_instance, method_name, original_method)
    else:
        # 使用完整模式
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


def ensure_target_parameters(method: Callable, use_simple_mode: bool = False) -> Callable:
    """
    統一的參數確保裝飾器，支援簡化模式和完整模式
    
    Args:
        method: 要裝飾的方法
        use_simple_mode: 是否使用簡化模式 (向後兼容)

    Returns:
        Callable: 確保接受目標導向參數的方法
    """
    if use_simple_mode:
        # 使用簡化模式（向後兼容）
        return format_decorator_basic(method)
    else:
        # 使用完整模式
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 簡化：只設置基本參數，使用固定深度
            kwargs.setdefault('to_console_only', False)
            kwargs.setdefault('to_log_file_only', False)
            kwargs.setdefault('_target_depth', 2)  # 使用固定深度，簡化邏輯
            
            return method(*args, **kwargs)
        
        # 複製原始方法的元數據
        wrapper.__name__ = method.__name__
        wrapper.__doc__ = method.__doc__
        
        return wrapper


# 向後兼容的別名和包裝函數
def create_target_methods_compat(logger_instance: Any, method_name: str, original_method) -> None:
    """向後兼容的目標方法創建函數"""
    return create_target_methods_simple(logger_instance, method_name, original_method)


def add_target_methods_compat(logger_instance: Any, method_name: str, original_method):
    """向後兼容的方法添加函數，使用基本模式"""
    return add_target_methods(logger_instance, method_name, original_method, use_simple_mode=True)


def ensure_target_parameters_compat(method):
    """向後兼容的裝飾器，使用基本模式"""
    return ensure_target_parameters(method, use_simple_mode=True)


# 向後兼容的舊名稱別名
simple_format_decorator = format_decorator_basic
create_simple_target_methods = create_target_methods_simple
create_simple_target_methods_compat = create_target_methods_compat