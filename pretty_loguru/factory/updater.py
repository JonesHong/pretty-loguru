"""
Logger 動態更新功能

提供真正的動態配置更新，而非創建新實例
"""

from typing import Optional
from ..types import PrettyLogger, LogLevelType
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

    # 最新版本：避免直接操作 logger._core.handlers（多 logger 共用 core 時會波及其他 logger）
    cfg = getattr(logger, "_pretty_loguru_config", None)
    if cfg is None:
        warnings.warn(
            f"Logger '{name}' has no stored config; cannot safely update level. "
            "Please reinit_logger() or update_logger_config() instead."
        )
        return False

    try:
        updated = cfg.clone(level=level)
    except Exception:
        # fallback：若 clone() 失敗，直接改值（仍交由 configure_logger 做驗證）
        updated = cfg
        setattr(updated, "level", level)

    updated.name = name
    configure_logger(logger, updated)
    return True


def update_logger_config(
    name: str,
    config: LoggerConfig,
    restart_cleaner: bool = False,
    reset_handlers: bool = False,
) -> bool:
    """
    使用 LoggerConfig 更新現有 logger
    
    Args:
        name: Logger 名稱
        config: 新的配置
        restart_cleaner: 是否重啟清理器以套用新的清理設定
        
    Returns:
        bool: 更新是否成功
    """
    logger = get_logger(name)
    if logger is None:
        warnings.warn(f"Logger '{name}' not found")
        return False
    
    # 確保配置有正確的名稱
    updated_config = config.clone()
    updated_config.name = name
    
    # 使用新配置重新配置 logger
    configure_logger(logger, updated_config, reset_handlers=reset_handlers)

    # 需要時重啟清理器以套用新設定
    if restart_cleaner and updated_config.start_cleaner and updated_config.log_dir:
        from .creator import _restart_cleaner_for_path
        _restart_cleaner_for_path(
            str(updated_config.log_dir),
            logger_instance=logger,
            verbose=updated_config.verbose,
            include_patterns=updated_config.cleaner_include_patterns,
            exclude_patterns=updated_config.cleaner_exclude_patterns,
        )
    
    return True
