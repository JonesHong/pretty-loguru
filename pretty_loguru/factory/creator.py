"""
簡化的 Logger 創建模組

按照KISS原則重新設計，大幅減少參數數量和複雜性，保持核心功能。
專注於最常用的功能，去除過度設計的部分。
"""

import inspect
import os
import threading
import warnings
from pathlib import Path
from typing import Dict, Optional, Union, List, cast, Any, Callable

from loguru import logger as _base_logger

from ..types import PrettyLogger, LogLevelType, LogRotationType, LogDirType
from ..core.config import LoggerConfig
from ..core.base import configure_logger, get_console
from ..core.cleaner import LoggerCleaner
from ..core.presets import get_preset_config
from ..core import registry
from ..utils.warn_once import warn_once

_console = get_console()
# 將全域清理器標誌替換為路徑基礎的清理器實例管理
_active_cleaners: Dict[str, LoggerCleaner] = {}
_cleaner_lock = threading.RLock()
_default_logger_instance = None
_default_logger_lock = threading.RLock()
_base_logger_prepared = False


def _ensure_base_logger_prepared() -> None:
    """
    使用 loguru public API 時，所有 Pretty-Loguru logger 會共享同一個 core。

    為避免 loguru 的「預設 handler」造成重複輸出，這裡在第一次建立 Pretty-Loguru logger 時，
    只嘗試移除預設 handler（通常是 handler id=0），避免清掉使用者先前透過 loguru 設定的 sinks。

    注意：這是「最新版本」行為，不保證與過往隔離 core 的行為相容。
    """
    global _base_logger_prepared
    if _base_logger_prepared:
        return
    skip_env = os.getenv("PRETTY_LOGURU_SKIP_REMOVE_DEFAULT_HANDLER", "").lower() in ("1", "true", "yes")
    if not skip_env:
        try:
            _base_logger.remove(0)
        except Exception:
            pass
    _base_logger_prepared = True


def _install_user_handler_tracking(logger_instance: Any) -> None:
    """
    追蹤「使用者透過此 logger 實例 add()」建立的 handler ids。

    目的：支援 `reinit_logger(reset_handlers=True)` 時，能有機會做到「只重置此 logger 自己的 sinks」，
    而不是粗暴地清空整個 shared core。
    """
    if getattr(logger_instance, "_pretty_loguru_add_wrapped", False):
        return

    original_add = getattr(logger_instance, "add", None)
    if original_add is None:
        return

    setattr(logger_instance, "_pretty_loguru_original_add", original_add)
    setattr(logger_instance, "_pretty_loguru_user_handler_ids", [])

    def _add_wrapper(*args: Any, **kwargs: Any) -> Any:
        handler_id = original_add(*args, **kwargs)
        try:
            ids = getattr(logger_instance, "_pretty_loguru_user_handler_ids", None)
            if isinstance(ids, list) and handler_id is not None:
                ids.append(handler_id)
        except Exception:
            pass
        return handler_id

    setattr(logger_instance, "add", _add_wrapper)
    setattr(logger_instance, "_pretty_loguru_add_wrapped", True)


def _emit_cleaner_message(
    logger_instance: Optional[Any],
    message: str,
    level: str = "INFO",
    verbose: bool = False,
) -> None:
    """
    統一輸出 cleaner 的提示訊息。

    行為：
    - 若有 logger：verbose=True 或 WARNING/ERROR 才會輸出（避免噪音）
    - 若沒有 logger：僅 WARNING/ERROR 會以 warnings.warn 顯示
    """
    if logger_instance:
        if verbose or level in ("WARNING", "ERROR"):
            getattr(logger_instance, level.lower(), logger_instance.info)(message)
    elif level in ("WARNING", "ERROR"):
        warnings.warn(message)


def _start_cleaner_for_path(
    log_dir: str,
    logger_instance: Optional[Any] = None,
    verbose: bool = False,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    log_retention: Optional[Union[int, str]] = None,
) -> None:
    """
    為指定路徑啟動清理器，如果該路徑已有清理器則重複使用
    
    Args:
        log_dir: 日誌目錄
    """
    global _active_cleaners
    
    if not log_dir:
        _emit_cleaner_message(
            logger_instance,
            "LoggerCleaner: log_dir 為空，跳過啟動清理器",
            level="WARNING",
            verbose=verbose,
        )
        return

    normalized_path = str(Path(log_dir).resolve())
    with _cleaner_lock:
        if normalized_path not in _active_cleaners:
            try:
                cleaner = LoggerCleaner(
                    log_retention=log_retention or "30 days",
                    log_dir=log_dir,
                    logger_instance=logger_instance,
                    verbose=verbose,
                    include_patterns=include_patterns,
                    exclude_patterns=exclude_patterns,
                )
                cleaner.start()
                _active_cleaners[normalized_path] = cleaner
                _emit_cleaner_message(
                    logger_instance,
                    f"LoggerCleaner: 為路徑 {normalized_path} 啟動清理器",
                    verbose=verbose,
                )
            except Exception as e:
                _emit_cleaner_message(
                    logger_instance,
                    f"LoggerCleaner: 無法為路徑 {normalized_path} 啟動清理器: {e}",
                    level="ERROR",
                    verbose=verbose,
                )
        else:
            _emit_cleaner_message(
                logger_instance,
                f"LoggerCleaner: 路徑 {normalized_path} 已有活躍的清理器",
                verbose=verbose,
            )


def _stop_all_cleaners() -> None:
    """停止所有活躍的清理器"""
    global _active_cleaners
    with _cleaner_lock:
        for path, cleaner in list(_active_cleaners.items()):
            try:
                cleaner.stop()
            except Exception as e:
                warnings.warn(f"LoggerCleaner: 停止路徑 {path} 的清理器時發生錯誤: {e}")
        _active_cleaners.clear()


def _stop_cleaner_for_path(
    log_dir: str,
    logger_instance: Optional[Any] = None,
    verbose: bool = False,
) -> None:
    """停止指定路徑的清理器（若存在）"""
    if not log_dir:
        return

    normalized_path = str(Path(log_dir).resolve())
    with _cleaner_lock:
        cleaner = _active_cleaners.pop(normalized_path, None)
    if cleaner:
        try:
            cleaner.stop()
            _emit_cleaner_message(
                logger_instance,
                f"LoggerCleaner: 已停止路徑 {normalized_path} 的清理器",
                verbose=verbose,
            )
        except Exception as e:
            _emit_cleaner_message(
                logger_instance,
                f"LoggerCleaner: 停止路徑 {normalized_path} 的清理器時發生錯誤: {e}",
                level="ERROR",
                verbose=verbose,
            )


def _restart_cleaner_for_path(
    log_dir: str,
    logger_instance: Optional[Any] = None,
    verbose: bool = False,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    log_retention: Optional[Union[int, str]] = None,
) -> None:
    """重啟指定路徑的清理器，確保設定生效"""
    _stop_cleaner_for_path(log_dir, logger_instance=logger_instance, verbose=verbose)
    _start_cleaner_for_path(
        log_dir,
        logger_instance=logger_instance,
        verbose=verbose,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        log_retention=log_retention,
    )


# 註冊程序退出時的清理函數
import atexit
atexit.register(_stop_all_cleaners)

def _create_logger_from_config(config: LoggerConfig, *, enable_addons: bool = True) -> PrettyLogger:
    """根據標準化的 LoggerConfig 物件創建 logger 實例。"""
    if not config.name:
        raise ValueError("Logger a name is required in LoggerConfig.")

    _ensure_base_logger_prepared()

    # 使用 loguru public API 建立 logger：共享 core + 透過 record extra 的 logger_id 進行 handler 隔離
    extra_defaults: Dict[str, Any] = {
        "logger_id": str(config.name),
        "name": str(config.component_name or config.name),
    }

    def _patch_record(record: Dict[str, Any]) -> Dict[str, Any]:
        extra = record.get("extra") or {}
        record["extra"] = extra

        # 為避免多 logger 共用 core 時彼此干擾，logger_id 必須穩定且不可被覆蓋
        if "logger_id" in extra and extra.get("logger_id") != extra_defaults["logger_id"]:
            if not extra_defaults.get("_reserved_warned"):
                warn_once("logger_id is reserved by pretty-loguru and will be overwritten.", UserWarning, key="logger_id_reserved")
                extra_defaults["_reserved_warned"] = True
        extra["logger_id"] = extra_defaults["logger_id"]
        extra["name"] = extra_defaults["name"]

        # 目標導向 flags：若呼叫端未指定，提供穩定的預設值
        extra.setdefault("to_console_only", False)
        extra.setdefault("to_file_only", False)

        # pretty event：避免 formatter 因缺少 extra key 而炸掉（用於檔案追加渲染文字）
        pretty_text = extra.get("pretty_text", "")
        if not isinstance(pretty_text, str):
            warnings.warn("pretty_text must be a string; resetting to empty string.", UserWarning)
            pretty_text = ""
        extra["pretty_text"] = pretty_text
        if "pretty_kind" in extra and not isinstance(extra.get("pretty_kind"), str):
            warn_once("pretty_kind must be a string; removing invalid value.", UserWarning, key="pretty_kind_type")
            extra.pop("pretty_kind", None)
        if "pretty_payload" in extra and not isinstance(extra.get("pretty_payload"), dict):
            warn_once("pretty_payload must be a dict; removing invalid value.", UserWarning, key="pretty_payload_type")
            extra.pop("pretty_payload", None)
        return record

    new_logger = _base_logger.patch(_patch_record)
    setattr(new_logger, "_pretty_loguru_extra_defaults", extra_defaults)

    # 配置 logger
    configure_logger(logger_instance=new_logger, config=config)

    pretty_logger = cast(PrettyLogger, new_logger)

    _install_user_handler_tracking(pretty_logger)

    # 啟動清理器 - 使用路徑基礎的實例管理
    if config.start_cleaner:
        if config.log_dir:
            _start_cleaner_for_path(
                str(config.log_dir),
                logger_instance=pretty_logger,
                verbose=config.verbose,
                include_patterns=config.cleaner_include_patterns,
                exclude_patterns=config.cleaner_exclude_patterns,
                log_retention=config.retention,
            )
        else:
            _emit_cleaner_message(
                pretty_logger,
                "LoggerCleaner: start_cleaner=True 但 log_dir 為 None，略過清理器啟動",
                level="WARNING",
                verbose=config.verbose,
            )

    # addons（格式化/targets 等）採 lazy import，避免 `import pretty_loguru` 時就拉入 heavy modules
    if enable_addons:
        from .methods import add_custom_methods

        add_custom_methods(pretty_logger, _console)

    registry.register_logger(config.name, pretty_logger)
    return pretty_logger

def _resolve_enable_addons(flag: Optional[bool]) -> bool:
    """
    根據傳入值或環境變數決定是否啟用 addons。
    環境變數：PRETTY_LOGURU_ENABLE_ADDONS_DEFAULT（1/true/yes 啟用，0/false/no 停用）
    """
    if flag is not None:
        return bool(flag)
    env = os.getenv("PRETTY_LOGURU_ENABLE_ADDONS_DEFAULT", "").lower()
    if env in ("0", "false", "no"):
        return False
    return True


def create_logger(
    name: Optional[str] = None,
    config: Optional[LoggerConfig] = None,
    use_native_format: bool = False,
    # 檔案輸出配置
    log_dir: Optional[LogDirType] = None,
    rotation: Optional[LogRotationType] = None,
    retention: Optional[str] = None,
    compression: Optional[Union[str, bool, Callable]] = None,
    compression_format: Optional[str] = None,
    # 格式化配置
    level: Optional[LogLevelType] = None,
    format: Optional[str] = None,
    component_name: Optional[str] = None,
    subdirectory: Optional[str] = None,
    # 行為控制
    start_cleaner: Optional[bool] = None,
    verbose: Optional[bool] = None,
    cleaner_include_patterns: Optional[List[str]] = None,
    cleaner_exclude_patterns: Optional[List[str]] = None,
    strict_validation: Optional[bool] = None,
    serialize: Optional[bool] = None,
    loki_enabled: Optional[bool] = None,
    loki_base_url: Optional[str] = None,
    loki_labels: Optional[Dict[str, str]] = None,
    loki_batch_size: Optional[int] = None,
    loki_flush_interval_seconds: Optional[float] = None,
    loki_timeout_seconds: Optional[float] = None,
    loki_tenant_id: Optional[str] = None,
    loki_username: Optional[str] = None,
    loki_password: Optional[str] = None,
    # 預設和實例控制
    preset: Optional[str] = None,
    force_new_instance: bool = False,
    enable_addons: Optional[bool] = None,
    clear_fields: Optional[List[str]] = None,
) -> PrettyLogger:
    """
    創建或獲取一個 logger 實例。

    這是一個高階介面，可以使用 LoggerConfig 物件或個別參數來創建 logger。
    如果提供了 config 參數，它將優先於其他參數。
    
    Args:
        name: Logger註冊名稱，若未提供則從調用文件名推斷
        config: LoggerConfig 物件，如果提供將優先使用
        use_native_format: 是否使用 loguru 原生格式 (file:function:line)
        log_dir: 日誌檔案輸出目錄
        rotation: 日誌輪轉設定 (例如: "1 day", "100 MB")
        retention: 日誌保留設定 (例如: "7 days")
        compression: 壓縮設定 (函數或字符串)
        compression_format: 壓縮格式
        level: 日誌等級 ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        format: 自定義日誌格式字符串（loguru 的 `format`）
        component_name: 組件名稱，用於日誌標識
        subdirectory: 子目錄，用於組織日誌檔案
        start_cleaner: 是否啟動自動清理器
        verbose: 是否輸出初始化與清理器訊息
        cleaner_include_patterns: 僅清理符合 pattern 的檔案
        cleaner_exclude_patterns: 排除符合 pattern 的檔案
        strict_validation: 是否啟用嚴格格式驗證（預設啟用）
        serialize: 是否將檔案輸出序列化為 JSON（便於 ELK/Filebeat/Promtail）
        loki_enabled: 是否啟用 Loki 直推
        loki_base_url: Loki base URL（會自動補上 /loki/api/v1/push）
        loki_labels: Loki stream labels（避免高基數）
        loki_batch_size: Loki 批次大小
        loki_flush_interval_seconds: Loki flush 間隔（秒）
        loki_timeout_seconds: Loki HTTP timeout（秒）
        loki_tenant_id: Loki multi-tenant org id（X-Scope-OrgID）
        loki_username: Loki Basic Auth 使用者
        loki_password: Loki Basic Auth 密碼
        preset: 預設配置名稱 ("minimal", "detailed", "production")
        force_new_instance: 是否強制創建新實例
        enable_addons: 是否啟用 addons（格式化/targets 等），若為 False 則不會載入 `pretty_loguru.formats/*`
        
    Examples:
        # 使用 config 物件
        config = LoggerConfig(level="INFO", log_dir="logs")
        logger = create_logger("app", config=config)
        
        # 使用個別參數
        logger = create_logger("app", level="INFO", log_dir="logs")
        
        # config + 覆寫參數
        logger = create_logger("debug_app", config=config, level="DEBUG")
    """
    resolved_addons = _resolve_enable_addons(enable_addons)

    # 1. 確定 logger 名稱
    if not name:
        frame = inspect.currentframe().f_back
        file_value = frame.f_globals.get('__file__')
        module_name = frame.f_globals.get('__name__')
        if file_value:
            name = Path(file_value).stem
        elif module_name and module_name != "__main__":
            name = module_name
        else:
            name = "interactive"
    
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
            'log_dir': log_dir,
            'rotation': rotation,
            'retention': retention,
            'compression': compression,
            'compression_format': compression_format,
            'level': level,
            'format': format,
            'component_name': component_name,
            'subdirectory': subdirectory,
            'start_cleaner': start_cleaner,
            'verbose': verbose,
            'cleaner_include_patterns': cleaner_include_patterns,
            'cleaner_exclude_patterns': cleaner_exclude_patterns,
            'strict_validation': strict_validation,
            'serialize': serialize,
            'loki_enabled': loki_enabled,
            'loki_base_url': loki_base_url,
            'loki_labels': loki_labels,
            'loki_batch_size': loki_batch_size,
            'loki_flush_interval_seconds': loki_flush_interval_seconds,
            'loki_timeout_seconds': loki_timeout_seconds,
            'loki_tenant_id': loki_tenant_id,
            'loki_username': loki_username,
            'loki_password': loki_password,
        }
        
        for key, value in explicit_params.items():
            if value is not None:  # 只覆寫明確提供的參數
                setattr(final_config, key, value)

        if clear_fields:
            for key in clear_fields:
                if hasattr(final_config, key):
                    setattr(final_config, key, None)
                else:
                    warn_once(f"Unknown clear field '{key}' ignored.", UserWarning, key=("clear_field", key))
        
        return _create_logger_from_config(final_config, enable_addons=resolved_addons)
    
    # 4. 使用個別參數建構配置
    config_args = {
        'name': name,
        'use_native_format': use_native_format,
    }
    
    # 只添加非 None 的參數
    explicit_params = {
        'log_dir': log_dir,
        'rotation': rotation,
        'retention': retention,
        'compression': compression,
        'compression_format': compression_format,
        'level': level,
        'format': format,
        'component_name': component_name,
        'subdirectory': subdirectory,
        'start_cleaner': start_cleaner,
        'verbose': verbose,
        'cleaner_include_patterns': cleaner_include_patterns,
        'cleaner_exclude_patterns': cleaner_exclude_patterns,
        'strict_validation': strict_validation,
        'serialize': serialize,
        'loki_enabled': loki_enabled,
        'loki_base_url': loki_base_url,
        'loki_labels': loki_labels,
        'loki_batch_size': loki_batch_size,
        'loki_flush_interval_seconds': loki_flush_interval_seconds,
        'loki_timeout_seconds': loki_timeout_seconds,
        'loki_tenant_id': loki_tenant_id,
        'loki_username': loki_username,
        'loki_password': loki_password,
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
            _warn_unknown_preset(preset)

    # 6. 創建 LoggerConfig 實例
    final_config = LoggerConfig.from_dict(config_args)

    # 7. 創建 logger
    return _create_logger_from_config(final_config, enable_addons=resolved_addons)



def get_logger(name: str) -> Optional[PrettyLogger]:
    """根據名稱獲取已註冊的 logger 實例"""
    return registry.get_logger(name)


def set_logger(name: str, logger_instance: PrettyLogger) -> None:
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
    use_native_format: Optional[bool] = None,
    # 檔案輸出配置
    log_dir: Optional[LogDirType] = None,
    rotation: Optional[LogRotationType] = None,
    retention: Optional[str] = None,
    compression: Optional[Union[str, bool, Callable]] = None,
    compression_format: Optional[str] = None,
    # 格式化配置
    level: Optional[LogLevelType] = None,
    format: Optional[str] = None,
    component_name: Optional[str] = None,
    subdirectory: Optional[str] = None,
    # 行為控制
    start_cleaner: Optional[bool] = None,
    verbose: Optional[bool] = None,
    cleaner_include_patterns: Optional[List[str]] = None,
    cleaner_exclude_patterns: Optional[List[str]] = None,
    strict_validation: Optional[bool] = None,
    serialize: Optional[bool] = None,
    loki_enabled: Optional[bool] = None,
    loki_base_url: Optional[str] = None,
    loki_labels: Optional[Dict[str, str]] = None,
    loki_batch_size: Optional[int] = None,
    loki_flush_interval_seconds: Optional[float] = None,
    loki_timeout_seconds: Optional[float] = None,
    loki_tenant_id: Optional[str] = None,
    loki_username: Optional[str] = None,
    loki_password: Optional[str] = None,
    # 預設配置
    preset: Optional[str] = None,
    reset_handlers: bool = False,
    clear_fields: Optional[List[str]] = None,
) -> Optional[PrettyLogger]:
    """
    重新初始化已存在的 logger。
    
    它會就地更新現有 logger 的 handlers 與設定。
    
    Args:
        name: Logger名稱
        use_native_format: 是否使用 loguru 原生格式（None 代表維持現有設定）
        log_dir: 日誌檔案輸出目錄
        rotation: 日誌輪轉設定
        retention: 日誌保留設定
        compression: 壓縮設定
        compression_format: 壓縮格式
        level: 日誌等級
        format: 自定義日誌格式字符串（loguru 的 `format`）
        component_name: 組件名稱
        subdirectory: 子目錄
        start_cleaner: 是否啟動自動清理器
        verbose: 是否輸出初始化與清理器訊息
        cleaner_include_patterns: 僅清理符合 pattern 的檔案
        cleaner_exclude_patterns: 排除符合 pattern 的檔案
        strict_validation: 是否啟用嚴格格式驗證（預設啟用）
        serialize: 是否將檔案輸出序列化為 JSON
        loki_enabled: 是否啟用 Loki 直推
        loki_base_url: Loki base URL（會自動補上 /loki/api/v1/push）
        loki_labels: Loki stream labels
        loki_batch_size: Loki 批次大小
        loki_flush_interval_seconds: Loki flush 間隔（秒）
        loki_timeout_seconds: Loki HTTP timeout（秒）
        loki_tenant_id: Loki multi-tenant org id（X-Scope-OrgID）
        loki_username: Loki Basic Auth 使用者
        loki_password: Loki Basic Auth 密碼
        preset: 預設配置名稱
        reset_handlers: 是否移除「使用者透過此 logger 實例 add()」建立的 sinks（顯式選擇）
        clear_fields: 顯式清空的欄位名稱清單（例如 ["log_dir"]）
    """
    if registry.get_logger(name) is None:
        warnings.warn(f"Logger '{name}' does not exist, cannot re-initialize.", UserWarning)
        return None

    existing_logger = registry.get_logger(name)
    existing_config = getattr(existing_logger, "_pretty_loguru_config", None)
    if existing_config and hasattr(existing_config, "to_dict"):
        config_args = existing_config.to_dict()
    else:
        config_args = {}
    config_args["name"] = name

    # 只添加非 None 的參數
    explicit_params = {
        'use_native_format': use_native_format,
        'log_dir': log_dir,
        'rotation': rotation,
        'retention': retention,
        'compression': compression,
        'compression_format': compression_format,
        'level': level,
        'format': format,
        'component_name': component_name,
        'subdirectory': subdirectory,
        'start_cleaner': start_cleaner,
        'verbose': verbose,
        'cleaner_include_patterns': cleaner_include_patterns,
        'cleaner_exclude_patterns': cleaner_exclude_patterns,
        'strict_validation': strict_validation,
        'serialize': serialize,
        'loki_enabled': loki_enabled,
        'loki_base_url': loki_base_url,
        'loki_labels': loki_labels,
        'loki_batch_size': loki_batch_size,
        'loki_flush_interval_seconds': loki_flush_interval_seconds,
        'loki_timeout_seconds': loki_timeout_seconds,
        'loki_tenant_id': loki_tenant_id,
        'loki_username': loki_username,
        'loki_password': loki_password,
        'preset': preset,
    }
    
    for key, value in explicit_params.items():
        if value is not None:
            config_args[key] = value

    if clear_fields:
        for key in clear_fields:
            if key in config_args:
                config_args[key] = None
            else:
                warn_once(f"Unknown clear field '{key}' ignored.", UserWarning, key=("clear_field", key))

    if clear_fields:
        for key in clear_fields:
            if key in config_args:
                config_args[key] = None
            else:
                warn_once(f"Unknown clear field '{key}' ignored.", UserWarning, key=("clear_field", key))

    # 載入 preset 配置（preset 作為底層，明確參數覆蓋它）
    if preset:
        try:
            preset_conf = get_preset_config(preset)
            config_args = {**config_args, **preset_conf}
        except ValueError:
            _warn_unknown_preset(preset)

    final_config = LoggerConfig.from_dict(config_args)

    from .updater import update_logger_config
    success = update_logger_config(name, final_config, reset_handlers=reset_handlers)
    if not success:
        warnings.warn(f"Logger '{name}' update failed.", UserWarning)
        return None

    if final_config.start_cleaner and final_config.log_dir:
        _restart_cleaner_for_path(
            str(final_config.log_dir),
            logger_instance=registry.get_logger(name),
            verbose=final_config.verbose,
            include_patterns=final_config.cleaner_include_patterns,
            exclude_patterns=final_config.cleaner_exclude_patterns,
            log_retention=final_config.retention,
        )

    updated_logger = registry.get_logger(name)
    registry.post_event("logger_updated", name=name, new_logger=updated_logger)
    return updated_logger


def default_logger() -> PrettyLogger:
    """獲取默認 logger 實例 - 延遲初始化"""
    global _default_logger_instance
    with _default_logger_lock:
        if _default_logger_instance is None:
            _default_logger_instance = create_logger("default_service")
        return _default_logger_instance


# 簡化的預設獲取函數  
def _warn_unknown_preset(preset_name: str) -> None:
    warnings.warn(f"Unknown preset '{preset_name}', using 'detailed'", UserWarning)


def _get_preset(preset_name: str):
    """簡化的預設獲取函數"""
    try:
        return get_preset_config(preset_name)
    except ValueError:
        _warn_unknown_preset(preset_name)
        return get_preset_config("detailed")

def cleanup_loggers(names: Optional[List[str]] = None) -> int:
    """
    清理所有註冊的 logger 和清理器。
    
    Returns:
        int: 清理的 logger 數量
    """
    # 停止所有清理器
    _stop_all_cleaners()

    # 關閉所有 logger handlers（Windows 上可避免檔案鎖）
    try:
        target_names = registry.list_loggers() if names is None else [n for n in names if registry.get_logger(n)]
        for logger_name in target_names:
            lg = registry.get_logger(logger_name)
            if lg is None:
                continue
            try:
                lg.remove()
            except Exception:
                pass
    except Exception:
        pass
    
    # 清理 registry
    if names is None:
        count = registry.clear_registry()
    else:
        count = 0
        for name in names:
            if registry.unregister_logger(name):
                count += 1
    
    # 重置預設 logger
    global _default_logger_instance
    _default_logger_instance = None
    
    return count
