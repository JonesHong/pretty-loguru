"""
簡化的 Logger 創建模組

按照KISS原則重新設計，大幅減少參數數量和複雜性，保持核心功能。
專注於最常用的功能，去除過度設計的部分。
"""

import inspect
import warnings
from pathlib import Path
from typing import Dict, Optional, Union, List, cast, Any, Callable
from datetime import datetime # Added for unique name generation

from loguru import logger as _base_logger
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from rich.console import Console

from ..types import EnhancedLogger, LogLevelType, LogRotationType, LogPathType
from ..core.config import LoggerConfig
from ..core.base import configure_logger, get_console
from ..core.cleaner import LoggerCleaner
from ..core.presets import get_preset_config
from ..core import registry
from .methods import add_custom_methods

_console = get_console()
# 將全域清理器標誌替換為路徑基礎的清理器實例管理
_active_cleaners: Dict[str, LoggerCleaner] = {}
_default_logger_instance = None


def _start_cleaner_for_path(log_path: str) -> None:
    """
    為指定路徑啟動清理器，如果該路徑已有清理器則重複使用
    
    Args:
        log_path: 日誌文件路徑
    """
    global _active_cleaners
    
    # 標準化路徑作為字典鍵
    normalized_path = str(Path(log_path).resolve().parent)
    
    # 如果該路徑已有清理器，則不重複創建
    if normalized_path not in _active_cleaners:
        try:
            cleaner = LoggerCleaner(log_path=log_path)
            cleaner.start()
            _active_cleaners[normalized_path] = cleaner
            print(f"LoggerCleaner: 為路徑 {normalized_path} 啟動清理器")
        except Exception as e:
            print(f"LoggerCleaner: 無法為路徑 {normalized_path} 啟動清理器: {e}")
    else:
        print(f"LoggerCleaner: 路徑 {normalized_path} 已有活躍的清理器")


def _stop_all_cleaners() -> None:
    """停止所有活躍的清理器"""
    global _active_cleaners
    
    for path, cleaner in _active_cleaners.items():
        try:
            cleaner.stop()
            print(f"LoggerCleaner: 已停止路徑 {path} 的清理器")
        except Exception as e:
            print(f"LoggerCleaner: 停止路徑 {path} 的清理器時發生錯誤: {e}")
    
    _active_cleaners.clear()


# 註冊程序退出時的清理函數
import atexit
atexit.register(_stop_all_cleaners)

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

    # 啟動清理器 - 使用路徑基礎的實例管理
    if config.start_cleaner:
        _start_cleaner_for_path(config.log_path)

    # 添加自定義方法
    add_custom_methods(enhanced_logger, _console)

    registry.register_logger(config.name, enhanced_logger)
    return enhanced_logger

def create_logger(
    name: Optional[str] = None,
    config: Optional[LoggerConfig] = None,
    use_native_format: bool = False,
    # 檔案輸出配置
    log_path: Optional[LogPathType] = None,
    rotation: Optional[LogRotationType] = None,
    retention: Optional[str] = None,
    compression: Optional[Union[str, Callable]] = None,
    compression_format: Optional[str] = None,
    # 格式化配置
    level: Optional[LogLevelType] = None,
    logger_format: Optional[str] = None,
    component_name: Optional[str] = None,
    subdirectory: Optional[str] = None,
    # 行為控制
    start_cleaner: Optional[bool] = None,
    # 預設和實例控制
    preset: Optional[str] = None,
    force_new_instance: bool = False
) -> EnhancedLogger:
    """
    創建或獲取一個 logger 實例。

    這是一個高階介面，可以使用 LoggerConfig 物件或個別參數來創建 logger。
    如果提供了 config 參數，它將優先於其他參數。
    
    Args:
        name: Logger註冊名稱，若未提供則從調用文件名推斷
        config: LoggerConfig 物件，如果提供將優先使用
        use_native_format: 是否使用 loguru 原生格式 (file:function:line)
        log_path: 日誌檔案輸出路徑
        rotation: 日誌輪轉設定 (例如: "1 day", "100 MB")
        retention: 日誌保留設定 (例如: "7 days")
        compression: 壓縮設定 (函數或字符串)
        compression_format: 壓縮格式
        level: 日誌等級 ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        logger_format: 自定義日誌格式字符串
        component_name: 組件名稱，用於日誌標識
        subdirectory: 子目錄，用於組織日誌檔案
        start_cleaner: 是否啟動自動清理器
        preset: 預設配置名稱 ("minimal", "detailed", "production")
        force_new_instance: 是否強制創建新實例
        
    Examples:
        # 使用 config 物件
        config = LoggerConfig(level="INFO", log_path="logs")
        logger = create_logger("app", config=config)
        
        # 使用個別參數
        logger = create_logger("app", level="INFO", log_path="logs")
        
        # config + 覆寫參數
        logger = create_logger("debug_app", config=config, level="DEBUG")
    """
    # 1. 確定 logger 名稱
    if not name:
        frame = inspect.currentframe().f_back
        name = Path(frame.f_globals.get('__file__', 'unknown')).name
    
    # 2. 如果 logger 已存在且非強制新建，直接返回
    if force_new_instance and registry.get_logger(name):
        from datetime import datetime # Import datetime here to avoid circular dependency if moved to top
        timestamp = datetime.now().strftime("-%Y%m%d%H%M%S-%f")
        name = f"{name}{timestamp}"
        warnings.warn(f"Logger with name '{name}' already exists. Creating a new instance with unique name: '{name}'.", UserWarning)

    if registry.get_logger(name) and not force_new_instance:
        return registry.get_logger(name)

    # 3. 如果提供了 config 參數，優先使用它
    if config is not None:
        # 複製 config 以避免修改原始物件
        final_config = config.clone()
        final_config.name = name
        
        # 覆寫明確提供的參數
        explicit_params = {
            'use_native_format': use_native_format,
            'log_path': log_path,
            'rotation': rotation,
            'retention': retention,
            'compression': compression,
            'compression_format': compression_format,
            'level': level,
            'logger_format': logger_format,
            'component_name': component_name,
            'subdirectory': subdirectory,
            'start_cleaner': start_cleaner,
        }
        
        for key, value in explicit_params.items():
            if value is not None:  # 只覆寫明確提供的參數
                setattr(final_config, key, value)
        
        return _create_logger_from_config(final_config)
    
    # 4. 使用個別參數建構配置
    config_args = {
        'name': name,
        'use_native_format': use_native_format,
    }
    
    # 只添加非 None 的參數
    explicit_params = {
        'log_path': log_path,
        'rotation': rotation,
        'retention': retention,
        'compression': compression,
        'compression_format': compression_format,
        'level': level,
        'logger_format': logger_format,
        'component_name': component_name,
        'subdirectory': subdirectory,
        'start_cleaner': start_cleaner,
        'preset': preset,
    }
    
    for key, value in explicit_params.items():
        if value is not None:
            config_args[key] = value

    # 5. 載入 preset 配置（preset 作為底層，明確參數覆蓋它）
    if preset:
        try:
            preset_conf = get_preset_config(preset)
            # 明確參數覆蓋 preset 配置
            config_args = {**preset_conf, **config_args}
        except ValueError:
            warnings.warn(f"Unknown preset '{preset}', ignoring.", UserWarning)

    # 6. 創建 LoggerConfig 實例
    final_config = LoggerConfig.from_dict(config_args)

    # 7. 創建 logger
    return _create_logger_from_config(final_config)



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


def reinit_logger(
    name: str,
    use_native_format: bool = False,
    # 檔案輸出配置
    log_path: Optional[LogPathType] = None,
    rotation: Optional[LogRotationType] = None,
    retention: Optional[str] = None,
    compression: Optional[Union[str, Callable]] = None,
    compression_format: Optional[str] = None,
    # 格式化配置
    level: Optional[LogLevelType] = None,
    logger_format: Optional[str] = None,
    component_name: Optional[str] = None,
    subdirectory: Optional[str] = None,
    # 行為控制
    start_cleaner: Optional[bool] = None,
    # 預設配置
    preset: Optional[str] = None
) -> Optional[EnhancedLogger]:
    """
    重新初始化已存在的 logger。
    
    它會創建一個新的 logger 實例。
    
    Args:
        name: Logger名稱
        use_native_format: 是否使用 loguru 原生格式
        log_path: 日誌檔案輸出路徑
        rotation: 日誌輪轉設定
        retention: 日誌保留設定
        compression: 壓縮設定
        compression_format: 壓縮格式
        level: 日誌等級
        logger_format: 自定義日誌格式字符串
        component_name: 組件名稱
        subdirectory: 子目錄
        start_cleaner: 是否啟動自動清理器
        preset: 預設配置名稱
    """
    if registry.get_logger(name) is None:
        warnings.warn(f"Logger '{name}' does not exist, cannot re-initialize.", UserWarning)
        return None

    # 強制創建一個新的實例
    new_logger = create_logger(
        name=name,
        use_native_format=use_native_format,
        log_path=log_path,
        rotation=rotation,
        retention=retention,
        compression=compression,
        compression_format=compression_format,
        level=level,
        logger_format=logger_format,
        component_name=component_name,
        subdirectory=subdirectory,
        start_cleaner=start_cleaner,
        preset=preset,
        force_new_instance=True
    )

    # 發布更新事件
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

def cleanup_loggers() -> int:
    """
    清理所有註冊的 logger 和清理器。
    
    Returns:
        int: 清理的 logger 數量
    """
    # 停止所有清理器
    _stop_all_cleaners()
    
    # 清理 registry
    count = registry.clear_registry()
    
    # 重置預設 logger
    global _default_logger_instance
    _default_logger_instance = None
    
    return count