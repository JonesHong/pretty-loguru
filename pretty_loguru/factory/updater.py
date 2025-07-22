"""
Logger 動態更新功能

提供真正的動態配置更新，而非創建新實例
"""

from typing import Optional
from ..types import EnhancedLogger, LogLevelType
from ..core.registry import get_logger
from ..core.base import configure_logger
from ..core.config import LoggerConfig
import warnings


def update_logger_level(name: str, level: LogLevelType) -> bool:
    """
    動態更新 logger 的日誌級別
    
    通過移除並重新添加 handlers 來實現級別更新
    
    Args:
        name: Logger 名稱
        level: 新的日誌級別
        
    Returns:
        bool: 更新是否成功
    """
    logger = get_logger(name)
    if logger is None:
        warnings.warn(f"Logger '{name}' not found")
        return False
    
    # 保存當前的 handlers 配置
    handlers_config = []
    for handler_id, handler in logger._core.handlers.items():
        # 保存 handler 的配置
        config = {
            'sink': handler.sink,
            'level': level,  # 使用新的 level
            'format': handler.format,
            'filter': handler.filter,
            'colorize': handler.colorize,
            'serialize': handler.serialize,
            'backtrace': handler.backtrace,
            'diagnose': handler.diagnose,
            'enqueue': handler.enqueue,
            'catch': handler.catch
        }
        handlers_config.append((handler_id, config))
    
    # 移除所有現有 handlers
    for handler_id, _ in handlers_config:
        try:
            logger.remove(handler_id)
        except:
            pass
    
    # 重新添加 handlers，使用新的 level
    for _, config in handlers_config:
        logger.add(**config)
    
    return True


def update_logger_config(name: str, config: LoggerConfig) -> bool:
    """
    使用 LoggerConfig 更新現有 logger
    
    Args:
        name: Logger 名稱
        config: 新的配置
        
    Returns:
        bool: 更新是否成功
    """
    logger = get_logger(name)
    if logger is None:
        warnings.warn(f"Logger '{name}' not found")
        return False
    
    # 保存現有 handlers 的 IDs
    handler_ids = list(logger._core.handlers.keys())
    
    # 移除所有 handlers
    for handler_id in handler_ids:
        try:
            logger.remove(handler_id)
        except:
            pass
    
    # 確保配置有正確的名稱
    updated_config = config.clone()
    updated_config.name = name
    
    # 使用新配置重新配置 logger
    configure_logger(logger, updated_config)
    
    return True