"""
Logger 創建模組 - 改進版

此模組提供創建和管理 Logger 實例的功能，
實現了單例模式、工廠模式和延遲初始化，確保 Logger 實例的有效隔離和管理。
"""

import inspect
import os
import warnings
import uuid
from pathlib import Path
from typing import Dict, Optional, Union, Literal, List, Any, cast

from loguru import logger as _base_logger
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from rich.console import Console

from pretty_loguru.core.presets import LogPreset, PresetFactory, PresetType

from ..types import (
    EnhancedLogger,
    LogLevelType,
    LogPathType,
    LogNameFormatType,
    LogRotationType,
    LogConfigType,
)
from ..core.config import LOG_NAME_FORMATS, LOGGER_FORMAT_NATIVE
from ..core.base import configure_logger, get_console
from ..core.cleaner import LoggerCleaner
from .methods import add_custom_methods

# 全局 logger 實例註冊表
# 用於保存、查找和管理已創建的 logger 實例
_logger_registry: Dict[str, EnhancedLogger] = {}

# 保存 logger 實例的文件路徑
_logger_file_paths: Dict[str, str] = {}

# 保存是否已啟動清理器的標誌
_cleaner_started = False

# 默認 console 實例，用於共享視覺輸出
_console = get_console()

# 保存延遲初始化的 default_logger
_default_logger_instance = None


def create_logger(
    name: Optional[str] = None,
    service_tag: Optional[str] = None,  # DEPRECATED: 將在未來版本移除，請使用 name 參數
    subdirectory: Optional[str] = None,
    log_name_format: LogNameFormatType = None,
    log_name_preset: Optional[
        Literal["detailed", "simple", "monthly", "weekly", "daily", "hourly", "minute"]
        | PresetType
    ] = None,
    timestamp_format: Optional[str] = None,
    log_path: Optional[LogPathType] = None,
    log_file_settings: Optional[LogConfigType] = None,
    custom_config: Optional[LogConfigType] = None,
    reuse_existing: bool = False,
    start_cleaner: bool = False,
    force_new_instance: bool = True,
    use_proxy: bool = False,
    console: Optional[Console] = None,
    level: LogLevelType = "INFO",
    rotation: LogRotationType = "20 MB",
    logger_format: Optional[str] = None,
) -> EnhancedLogger:
    """
    創建有效隔離的 logger 實例

    Args:
        name: logger 實例的名稱和標識，如果不提供則使用檔案名
        service_tag: (已棄用) 請使用 name 參數替代
        subdirectory: 日誌子目錄，用於分類不同模組或功能的日誌
        log_name_format: 日誌檔案名稱格式，可包含變數如 {component_name}, {timestamp}, {date}, {time} 等
        log_name_preset: 預設的日誌檔案名格式，可選值為 "detailed", "daily", "hourly" 等
        timestamp_format: 時間戳格式，用於自定義時間顯示方式
        log_path: 日誌基礎路徑，覆蓋預設的 log_path
        log_file_settings: 日誌檔案的其他設定，如壓縮、保留時間等
        custom_config: 自定義日誌配置，可包含任意 configure_logger 支援的參數
        reuse_existing: 是否重用同名的既有實例，預設為 False
        start_cleaner: 是否啟動日誌清理器，預設為 False
        force_new_instance: 是否強制創建新實例，預設為 True
        use_proxy: 是否使用 Logger Proxy，解決重新初始化同步問題，預設為 False
        console: 要使用的 Rich Console 實例，預設為全局共享的實例
        level: 日誌級別，預設為 INFO
        rotation: 日誌輪換設置，預設為 20 MB
        logger_format: 日誌格式字符串，可使用 loguru 原生格式如 '{file}:{line} | {message}'，預設使用 pretty-loguru 格式

    Returns:
        EnhancedLogger: 已配置的日誌實例

    Examples:
        >>> # 創建基本 logger
        >>> logger = create_logger("my_app")
        >>>
        >>> # 創建帶有子目錄的 logger
        >>> logger = create_logger("api", subdirectory="api_logs")
        >>>
        >>> # 使用預設文件名格式
        >>> logger = create_logger("db", log_name_preset="daily")
        >>>
        >>> # 自定義日誌文件配置
        >>> logger = create_logger(
        ...     "background_tasks",
        ...     log_file_settings={"compression": "zip", "retention": "1 week"}
        ... )
    """
    global _cleaner_started

    # 取得調用者資訊，用於自動生成名稱
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename if caller_frame else "unknown"

    # 向後兼容：如果提供了 service_tag 但沒有 name，將 service_tag 作為 name
    if name is None and service_tag is not None:
        name = service_tag
        warnings.warn(
            "service_tag 參數已棄用，請使用 name 參數替代",
            DeprecationWarning,
            stacklevel=2
        )
    
    # 記錄是否原本沒有提供 name 參數 (用於決定是否使用原生 loguru 格式)
    name_was_none = name is None
    
    # 確定最終的標識名稱
    if name is None:
        file_name = os.path.splitext(os.path.basename(caller_file))[0]
        name = file_name
    
    # 統一使用 name 作為 component_name
    component_name = name

    # 創建唯一的 logger 標識
    logger_id = f"{name}_{component_name}"

    # 如果想重用實例且不是強制創建新的
    if reuse_existing and not force_new_instance:
        if name in _logger_registry:
            return _logger_registry[name]

        # 查找已存在的實例 (基於名稱但不包括唯一ID部分)
        base_id = f"{name}_"
        for existing_id, logger_instance in _logger_registry.items():
            if existing_id.startswith(base_id):
                return logger_instance

    # 處理預設配置 - 簡化邏輯，始終使用預設系統
    preset = _get_preset(log_name_preset)
    preset_settings = preset.get_settings()

    # 合併預設設定 - 僅在未明確指定時使用預設值
    log_name_format = log_name_format or preset_settings["name_format"]

    # 處理 log_file_settings 的合併邏輯
    log_file_settings = log_file_settings or {}

    # 1. rotation 的處理：
    #    - 如果 log_file_settings 中有 rotation，使用它
    #    - 否則，如果參數 rotation 不是預設值，使用參數 rotation
    #    - 否則，使用 preset 中的 rotation
    if "rotation" not in log_file_settings:
        if rotation != "20 MB":  # 使用者有提供 rotation 參數
            log_file_settings["rotation"] = rotation
        else:  # 使用 preset 中的 rotation
            log_file_settings["rotation"] = preset_settings["rotation"]

    # 2. retention 的處理：只在未指定時使用 preset 值
    log_file_settings.setdefault("retention", preset_settings["retention"])

    # 3. compression 的處理：只在未指定且 preset 有值時使用 preset 值
    if "compression" not in log_file_settings and preset_settings["compression"]:
        log_file_settings["compression"] = preset_settings["compression"]

    # 創建新的 logger 實例
    new_logger = _Logger(
        core=_Core(),
        exception=None,
        depth=0,
        record=False,
        lazy=False,
        colors=False,
        raw=False,
        capture=True,
        patchers=[],
        extra={},
    ).patch(
        lambda record: record.update(
            logger_name=name,
            logger_id=logger_id,
            folder=component_name,
        )
    )

    # 使用相同的 console 實例
    if console is None:
        console = _console

    # 準備日誌初始化參數
    logger_config = {
        "level": level,
        "component_name": component_name,
        "rotation": rotation,
        "log_path": log_path,
        "subdirectory": subdirectory,
        "log_name_format": log_name_format,
        "timestamp_format": timestamp_format,
        "log_file_settings": log_file_settings,
        "name": name,
        "isolate_handlers": True,
    }
    
    # 決定要使用的格式
    if logger_format is not None:
        # 明確指定了格式
        logger_config["logger_format"] = logger_format
    elif name_was_none:
        # 沒有指定 name，使用原生 loguru 格式
        logger_config["logger_format"] = LOGGER_FORMAT_NATIVE
    else:
        # 有指定 name 但沒有指定格式，使用預設 pretty-loguru 格式
        # 不設定 logger_config["logger_format"]，讓 configure_logger 使用預設值
        logger_config["logger_format"] = LOGGER_FORMAT_NATIVE

    print(f"Creating logger with config: {logger_config}")
    # 合併自定義配置
    if custom_config:
        logger_config.update(custom_config)

    # 配置 logger 實例
    log_file_path = configure_logger(logger_instance=new_logger, **logger_config)

    # 保存文件路徑（如果有的話）
    if log_file_path:
        _logger_file_paths[logger_id] = log_file_path

    # 加入自定義方法到新的 logger 實例
    add_custom_methods(new_logger, console)

    # 只有在被明確要求時才啟動日誌清理器，而且只啟動一次
    if start_cleaner and not _cleaner_started:
        logger_cleaner = LoggerCleaner(logger_instance=new_logger, log_path=log_path)
        logger_cleaner.start()
        _cleaner_started = True

    # 準備最終的 logger 實例
    final_logger = cast(EnhancedLogger, new_logger)
    
    # 如果使用 proxy，創建 proxy 實例
    if use_proxy:
        from .proxy import create_logger_proxy
        final_logger = create_logger_proxy(final_logger, name)
    
    # 將實例註冊到全局註冊表
    _logger_registry[name] = final_logger

    # 記錄創建信息
    new_logger.debug(
        f"Logger instance '{name}' (ID: {logger_id}) has been created, log file: {log_file_path}"
    )

    return final_logger


def _get_preset(
    log_name_preset: Optional[
        Literal["detailed", "simple", "monthly", "weekly", "daily", "hourly", "minute"]
        | PresetType
    ],
) -> LogPreset:
    """取得預設配置，優化版本"""
    if log_name_preset is None:
        return PresetFactory.get_preset(PresetType.DETAILED)

    if isinstance(log_name_preset, PresetType):
        return PresetFactory.get_preset(log_name_preset)

    try:
        preset_type = PresetType[log_name_preset.upper()]
        return PresetFactory.get_preset(preset_type)
    except KeyError:
        warnings.warn(
            f"Unknown log_name_preset '{log_name_preset}'. Using 'detailed' instead.",
            UserWarning,
            stacklevel=3,
        )
        return PresetFactory.get_preset(PresetType.DETAILED)


def get_logger(name: str) -> Optional[EnhancedLogger]:
    """
    根據名稱獲取已註冊的 logger 實例

    Args:
        name: logger 實例的名稱

    Returns:
        Optional[EnhancedLogger]: 如果找到則返回 logger 實例，否則返回 None
    """
    return _logger_registry.get(name)


def set_logger(name: str, logger_instance: EnhancedLogger) -> None:
    """
    手動註冊 logger 實例

    Args:
        name: logger 實例的名稱
        logger_instance: 要註冊的 logger 實例
    """
    _logger_registry[name] = logger_instance


def reinit_logger(name: str, **kwargs) -> Optional[EnhancedLogger]:
    """
    重新初始化已存在的 logger
    
    這個函數會重新創建指定名稱的 logger，並更新所有使用該 logger 的 proxy。
    對於解決模組間 logger 同步問題特別有用。
    
    Args:
        name: 要重新初始化的 logger 名稱
        **kwargs: 傳遞給 create_logger 的參數
        
    Returns:
        Optional[EnhancedLogger]: 重新初始化的 logger，如果原 logger 不存在則返回 None
        
    Examples:
        >>> # 原本的 logger
        >>> logger = create_logger("my_app", use_proxy=True)
        >>> 
        >>> # 在其他地方重新初始化
        >>> reinit_logger("my_app", log_path="./new_logs", level="DEBUG")
        >>> 
        >>> # 所有使用 proxy 的地方都會自動使用新配置
    """
    # 檢查 logger 是否存在
    existing_logger = get_logger(name)
    if existing_logger is None:
        warnings.warn(f"Logger '{name}' 不存在，無法重新初始化", UserWarning)
        return None
    
    # 檢查是否為 proxy
    from .proxy import LoggerProxy
    is_proxy = isinstance(existing_logger, LoggerProxy)
    
    if not is_proxy:
        warnings.warn(
            f"Logger '{name}' 不是 proxy 實例，重新初始化可能無法同步到其他模組。"
            f"建議在創建時使用 use_proxy=True",
            UserWarning
        )
    
    # 強制重新創建
    kwargs.setdefault('force_new_instance', True)
    
    if is_proxy:
        # 如果原來是 proxy，我們創建新的真實 logger 但不使用 proxy
        kwargs['use_proxy'] = False
        
        # 臨時從註冊表移除，避免名稱衝突
        temp_logger = _logger_registry.pop(name, None)
        
        try:
            # 創建新的真實 logger
            new_real_logger = create_logger(name, **kwargs)
            
            # 更新原有 proxy 的目標
            if hasattr(existing_logger, 'update_target'):
                existing_logger.update_target(new_real_logger)
            
            # 將 proxy 重新放回註冊表
            _logger_registry[name] = existing_logger
            
            return existing_logger
            
        except Exception:
            # 如果出錯，恢復原狀
            if temp_logger:
                _logger_registry[name] = temp_logger
            raise
    else:
        # 如果不是 proxy，正常重新創建
        kwargs['use_proxy'] = False
        new_logger = create_logger(name, **kwargs)
        return new_logger


def unregister_logger(name: str) -> bool:
    """
    取消註冊 logger 實例

    Args:
        name: 要取消註冊的 logger 實例名稱

    Returns:
        bool: 如果成功取消註冊則返回 True，否則返回 False
    """
    if name in _logger_registry:
        del _logger_registry[name]
        return True
    return False


def list_loggers() -> List[str]:
    """
    列出所有已註冊的 logger 名稱

    Returns:
        List[str]: 註冊的 logger 名稱列表
    """
    return list(_logger_registry.keys())


def default_logger() -> EnhancedLogger:
    """
    獲取默認的 logger 實例（延遲初始化）

    只有在首次呼叫這個函數時，才會創建默認的 logger 實例，
    避免在導入模組時就立即創建日誌文件。

    Returns:
        EnhancedLogger: 默認的 logger 實例
    """
    global _default_logger_instance
    if _default_logger_instance is None:
        _default_logger_instance = create_logger(
            name="default_service",
            start_cleaner=False,
            force_new_instance=False,
        )
    return _default_logger_instance
