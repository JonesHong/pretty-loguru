"""
簡化的 Logger 創建模組

按照KISS原則重新設計，大幅減少參數數量和複雜性，保持核心功能。
專注於最常用的功能，去除過度設計的部分。
"""

import inspect
import warnings
from pathlib import Path
from typing import Dict, Optional, Union, List, cast, Any

from loguru import logger as _base_logger
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from rich.console import Console

from ..types import EnhancedLogger
from ..core.config import LoggerConfig
from ..core.base import configure_logger, get_console
from ..core.cleaner import LoggerCleaner
from ..core.presets import get_preset_config
from ..core import registry
from .methods import add_custom_methods

_console = get_console()
_cleaner_started = False
_default_logger_instance = None

def _create_logger_from_config(config: LoggerConfig) -> EnhancedLogger:
    """根據標準化的 LoggerConfig 物件創建 logger 實例。"""
    if not config.name:
        raise ValueError("Logger a name is required in LoggerConfig.")

    # 創建新的 logger 核心
    new_core = _Core()
    new_logger = _Logger(
        core=new_core, exception=None, depth=0, record=False, lazy=False,
        colors=False, raw=False, capture=True, patchers=[], extra={},
    )

    # 配置 logger
    configure_logger(logger_instance=new_logger, config=config)

    enhanced_logger = cast(EnhancedLogger, new_logger)

    # 啟動清理器
    global _cleaner_started
    if config.start_cleaner and not _cleaner_started:
        LoggerCleaner(log_path=config.log_path).start()
        _cleaner_started = True

    # 處理代理模式
    if config.use_proxy:
        from .proxy import create_logger_proxy
        enhanced_logger = create_logger_proxy(enhanced_logger, config.name)

    # 添加自定義方法 - 現在在代理創建之後調用
    add_custom_methods(enhanced_logger, _console)

    registry.register_logger(config.name, enhanced_logger)
    return enhanced_logger

def create_logger(
    name: Optional[str] = None,
    **kwargs: Any
) -> EnhancedLogger:
    """
    創建或獲取一個 logger 實例。

    這是一個高階介面，它將參數轉換為一個標準的 LoggerConfig 物件，
    然後調用核心工廠函數來創建 logger。
    """
    # 1. 確定 logger 名稱
    if not name:
        frame = inspect.currentframe().f_back
        name = Path(frame.f_globals.get('__file__', 'unknown')).stem
    
    # 2. 如果 logger 已存在且非強制新建，直接返回
    if registry.get_logger(name) and not kwargs.get('force_new_instance'):
        return registry.get_logger(name)

    # 3. 整合配置
    # 優先級: kwargs > preset > 默認值
    config_args = kwargs.copy()
    config_args['name'] = name

    # 載入 preset 配置
    preset_name = config_args.pop('preset', None)
    if preset_name:
        try:
            preset_conf = get_preset_config(preset_name)
            # 將 preset 配置作為底層，kwargs 可覆蓋它
            config_args = {**preset_conf, **config_args}
        except ValueError:
            warnings.warn(f"Unknown preset '{preset_name}', ignoring.", UserWarning)

    # 4. 創建 LoggerConfig 實例
    config = LoggerConfig.from_dict(config_args)

    # 5. 創建 logger
    return _create_logger_from_config(config)


def get_logger(name: str) -> Optional[EnhancedLogger]:
    """根據名稱獲取已註冊的 logger 實例"""
    return registry.get_logger(name)


def set_logger(name: str, logger_instance: EnhancedLogger) -> None:
    """手動註冊 logger 實例"""
    registry.register_logger(name, logger_instance)


def list_loggers() -> List[str]:
    """列出所有已註冊的 logger 名稱"""
    return registry.list_loggers()


def unregister_logger(name: str) -> bool:
    """取消註冊 logger 實例"""
    return registry.unregister_logger(name)


def reinit_logger(name: str, **kwargs) -> Optional[EnhancedLogger]:
    """
    重新初始化已存在的 logger。
    
    它會創建一個新的 logger 實例，然後發布一個事件，
    以便代理 logger 可以更新其目標。
    """
    if registry.get_logger(name) is None:
        warnings.warn(f"Logger '{name}' does not exist, cannot re-initialize.", UserWarning)
        return None

    # 強制創建一個新的實例
    kwargs['force_new_instance'] = True
    new_logger = create_logger(name, **kwargs)

    # 發布更新事件，以便代理可以捕獲
    registry.post_event("logger_updated", name=name, new_logger=new_logger)

    return new_logger


def default_logger() -> EnhancedLogger:
    """獲取默認 logger 實例 - 延遲初始化"""
    global _default_logger_instance
    if _default_logger_instance is None:
        _default_logger_instance = create_logger("default_service")
    return _default_logger_instance


# 簡化的預設獲取函數  
def _get_preset(preset_name: str):
    """簡化的預設獲取函數"""
    try:
        return get_preset_config(preset_name)
    except ValueError:
        warnings.warn(f"Unknown preset '{preset_name}', using 'detailed'", UserWarning)
        return get_preset_config("detailed")