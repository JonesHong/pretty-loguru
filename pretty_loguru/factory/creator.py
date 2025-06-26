"""
簡化的 Logger 創建模組

按照KISS原則重新設計，大幅減少參數數量和複雜性，保持核心功能。
專注於最常用的功能，去除過度設計的部分。
"""

import inspect
import warnings
from pathlib import Path
from typing import Dict, Optional, Union, List, cast

from loguru import logger as _base_logger
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from rich.console import Console

from ..types import EnhancedLogger, LogLevelType, LogPathType, LogConfigType
from ..core.config import LOGGER_FORMAT_NATIVE
from ..core.base import configure_logger, get_console
from ..core.cleaner import LoggerCleaner
from ..core.presets import get_preset_config, PresetType
from .methods import add_custom_methods

# 全局 logger 實例註冊表
_logger_registry: Dict[str, EnhancedLogger] = {}

# 默認 console 實例
_console = get_console()

# 默認 logger 實例
_default_logger_instance = None

# 是否已啟動清理器
_cleaner_started = False


def create_logger(
    name: Optional[str] = None,
    /,  # name 可以使用位置參數
    *,  # 其他參數必須使用關鍵字參數，防止誤用
    log_path: Optional[LogPathType] = None,
    preset: PresetType = "detailed",
    subdirectory: Optional[str] = None,
    level: LogLevelType = "INFO",
    use_proxy: bool = False,
    **kwargs  # 其他進階參數
) -> EnhancedLogger:
    """
    創建 logger 實例 - 簡化版本
    
    只保留最常用的參數，其他進階功能通過 kwargs 傳入。
    
    Args:
        name: logger 名稱，如果不提供則使用檔案名
        log_path: 日誌檔案路徑，None 表示只輸出到控制台
        preset: 預設配置類型 ("detailed", "simple", "daily", "hourly", "minute")
        subdirectory: 日誌子目錄
        level: 日誌級別
        use_proxy: 是否使用代理模式，解決跨模組同步問題
        **kwargs: 其他進階參數（rotation, retention, logger_format 等）
        
    Returns:
        EnhancedLogger: 配置好的 logger 實例
        
    Examples:
        >>> # 控制台專用 logger
        >>> logger = create_logger("my_app")
        
        >>> # 檔案 + 控制台 logger  
        >>> logger = create_logger("my_app", log_path="./logs")
        
        >>> # 使用預設配置
        >>> logger = create_logger("my_app", log_path="./logs", preset="daily")
    """
    
    # 1. 確定 logger 名稱
    if not name:
        frame = inspect.currentframe().f_back
        name = Path(frame.f_globals.get('__file__', 'unknown')).stem
    
    # 2. 檢查是否重用現有實例（簡化邏輯）
    force_new = kwargs.get('force_new_instance', True)
    if not force_new and name in _logger_registry:
        return _logger_registry[name]
    
    # 3. 獲取預設配置
    preset_config = get_preset_config(preset)
    
    # 4. 構建配置
    # 分離 configure_logger 參數和 log_file_settings 參數
    configure_params = {
        'level': level,
        'component_name': name,
        'log_path': log_path,
        'subdirectory': subdirectory,
        'isolate_handlers': True,
        'logger_format': kwargs.get('logger_format', 
                                   LOGGER_FORMAT_NATIVE if not name else None),
        'rotation': preset_config.get('rotation', '20 MB'),
        'log_name_format': preset_config.get('name_format'),
    }
    
    # 構建 log_file_settings
    log_file_settings = {}
    if 'retention' in preset_config:
        log_file_settings['retention'] = preset_config['retention']
    if 'compression' in preset_config and preset_config['compression']:
        log_file_settings['compression'] = preset_config['compression']
        
    # 從 kwargs 添加額外的設定
    for key in ['retention', 'compression']:
        if key in kwargs:
            log_file_settings[key] = kwargs[key]
    
    if log_file_settings:
        configure_params['log_file_settings'] = log_file_settings
        
    # 添加其他可能的 kwargs 參數
    allowed_params = {'rotation', 'timestamp_format', 'name'}
    for key, value in kwargs.items():
        if key in allowed_params:
            configure_params[key] = value
        elif key == 'name_format':
            # 將 name_format 映射到 log_name_format
            configure_params['log_name_format'] = value
    
    # 5. 創建新的 logger 核心
    new_core = _Core()
    new_logger = _Logger(
        core=new_core,
        exception=None,
        depth=0,
        record=False,
        lazy=False,
        colors=False,
        raw=False,
        capture=True,
        patchers=[],  # 這是關鍵：必須是空列表而不是 None
        extra={},
    )
    
    # 6. 配置 logger
    configure_logger(**configure_params, logger_instance=new_logger)
    
    # 7. 添加自定義方法
    add_custom_methods(new_logger, _console)
    enhanced_logger = cast(EnhancedLogger, new_logger)
    
    # 8. 啟動清理器（如果需要）
    global _cleaner_started
    if kwargs.get('start_cleaner', False) and not _cleaner_started:
        cleaner = LoggerCleaner()
        cleaner.start()
        _cleaner_started = True
    
    # 9. 處理代理模式
    if use_proxy:
        from .proxy import create_logger_proxy
        enhanced_logger = create_logger_proxy(enhanced_logger, name)
    
    # 10. 註冊 logger
    _logger_registry[name] = enhanced_logger
    
    return enhanced_logger


def get_logger(name: str) -> Optional[EnhancedLogger]:
    """根據名稱獲取已註冊的 logger 實例"""
    return _logger_registry.get(name)


def set_logger(name: str, logger_instance: EnhancedLogger) -> None:
    """手動註冊 logger 實例"""
    _logger_registry[name] = logger_instance


def list_loggers() -> List[str]:
    """列出所有已註冊的 logger 名稱"""
    return list(_logger_registry.keys())


def unregister_logger(name: str) -> bool:
    """取消註冊 logger 實例"""
    if name in _logger_registry:
        del _logger_registry[name]
        return True
    return False


def reinit_logger(name: str, **kwargs) -> Optional[EnhancedLogger]:
    """
    重新初始化已存在的 logger - 簡化版本
    
    Args:
        name: 要重新初始化的 logger 名稱
        **kwargs: 傳遞給 create_logger 的參數
        
    Returns:
        Optional[EnhancedLogger]: 重新初始化的 logger，如果原 logger 不存在則返回 None
    """
    existing_logger = get_logger(name)
    if existing_logger is None:
        warnings.warn(f"Logger '{name}' 不存在，無法重新初始化", UserWarning)
        return None
    
    # 檢查是否為代理
    from .proxy import LoggerProxy
    is_proxy = isinstance(existing_logger, LoggerProxy)
    
    if is_proxy:
        # 代理模式：更新目標 logger
        kwargs['force_new_instance'] = True
        kwargs['use_proxy'] = False  # 不再創建新代理
        
        # 臨時移除以避免衝突
        temp_logger = _logger_registry.pop(name, None)
        
        try:
            new_real_logger = create_logger(name, **kwargs)
            if hasattr(existing_logger, 'update_target'):
                existing_logger.update_target(new_real_logger)
            _logger_registry[name] = existing_logger
            return existing_logger
        except Exception:
            if temp_logger:
                _logger_registry[name] = temp_logger
            raise
    else:
        # 普通模式：直接重新創建
        kwargs['force_new_instance'] = True
        return create_logger(name, **kwargs)


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