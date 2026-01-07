"""
日誌系統基礎模組

此模組提供 Pretty Loguru 的基本功能，包括核心初始化、
日誌實例的配置和管理等基礎功能。
"""

import sys
import warnings
from pathlib import Path
from typing import Dict, Any, Optional, Union, Callable, cast

from loguru import logger as _logger
from rich.console import Console

from ..types import PrettyLogger
from .config import LoggerConfig, NATIVE_LOGGER_FORMAT
from .handlers import create_destination_filters, format_filename
from ..utils.warn_once import warn_once

# Rich Console 實例，用於美化輸出（與 loguru console handler 對齊使用 stderr）
_console = Console(stderr=True)

def get_console() -> Console:
    """獲取 Rich Console 實例"""
    return _console

def _get_or_create_pretty_extra_defaults(logger_instance: PrettyLogger) -> Dict[str, Any]:
    """
    取得（或建立）pretty-loguru 需要的 `record['extra']` 預設欄位容器。

    這些欄位用於：
    - handler 隔離（`logger_id`）
    - 顯示名稱（`name`）
    - 目標導向（`to_console_only` / `to_file_only`）
    - 檔案端渲染（`pretty_text`）
    """
    defaults = getattr(logger_instance, "_pretty_loguru_extra_defaults", None)
    if isinstance(defaults, dict):
        return defaults
    defaults = {}
    setattr(logger_instance, "_pretty_loguru_extra_defaults", defaults)
    return defaults

def configure_logger(
    logger_instance: PrettyLogger,
    config: LoggerConfig,
    *,
    reset_handlers: bool = False,
) -> None:
    """
    根據 LoggerConfig 配置日誌實例。
    """
    if config.strict_validation:
        config.validate_strict()
    else:
        config.validate()

    # 保存最近一次套用的配置（用於後續更新/除錯；最新版本不保證向後相容）
    try:
        setattr(logger_instance, "_pretty_loguru_config", config.clone())
    except Exception:
        # clone() 不應該失敗，但若使用者傳入奇怪型別也不應阻斷 logger 設定
        setattr(logger_instance, "_pretty_loguru_config", config)

    # 1. handler ownership
    #
    # - 預設：只移除 pretty-loguru 自己管理的 handlers（避免清掉使用者自行 logger.add() 的 sinks）
    # - reset_handlers=True：也會移除「使用者透過此 logger 實例 add()」建立的 handlers（顯式選擇）
    if hasattr(logger_instance, "_core"):
        managed_ids = getattr(logger_instance, "_pretty_loguru_managed_handler_ids", None)
        if managed_ids:
            for handler_id in list(managed_ids):
                try:
                    logger_instance.remove(handler_id)
                except Exception as e:
                    warnings.warn(f"Failed to remove managed handler {handler_id}: {e}")

        if reset_handlers:
            user_ids = getattr(logger_instance, "_pretty_loguru_user_handler_ids", None)
            if user_ids:
                for handler_id in list(user_ids):
                    try:
                        logger_instance.remove(handler_id)
                    except Exception as e:
                        warnings.warn(f"Failed to remove user handler {handler_id}: {e}")
                setattr(logger_instance, "_pretty_loguru_user_handler_ids", [])
        setattr(logger_instance, "_pretty_loguru_has_file_handler", False)
        setattr(logger_instance, "_pretty_loguru_managed_handler_ids", [])

    # 2. 根據 use_native_format 決定格式，並更新 Pretty-Loguru 的 per-logger extra defaults
    if config.use_native_format:
        actual_format = NATIVE_LOGGER_FORMAT
    else:
        actual_format = config.format

    extra_defaults = _get_or_create_pretty_extra_defaults(logger_instance)
    extra_defaults["logger_id"] = str(config.name)
    extra_defaults["name"] = str(config.component_name or config.name)

    # 3. 創建目標過濾器（加上 logger_id 隔離，避免多 logger 共用 core 時互相干擾）
    base_filters = create_destination_filters()

    def _scoped_filter(base_filter: Callable[[Dict[str, Any]], bool]) -> Callable[[Dict[str, Any]], bool]:
        def _filter(record: Dict[str, Any]) -> bool:
            record_logger_id = record.get("extra", {}).get("logger_id")
            if record_logger_id is None:
                warn_once(
                    "Record missing logger_id; configure_logger called without patch/bind. Allowing record through.",
                    UserWarning,
                    key="missing_logger_id",
                )
                return base_filter(record)
            if record_logger_id != str(config.name):
                return False
            return base_filter(record)

        return _filter

    filters = {
        "console": _scoped_filter(base_filters["console"]),
        "file": _scoped_filter(base_filters["file"]),
    }

    # 4. 新增 console handlers（plain + pretty）
    #
    # - plain：維持 loguru 原生字串輸出
    # - pretty：同一筆 event 依 payload 進行 Rich render（避免在 formats 內 console.print）
    def _is_pretty_record(record: Dict[str, Any]) -> bool:
        return bool(record.get("extra", {}).get("pretty_kind")) and bool(record.get("extra", {}).get("pretty_payload"))

    def _console_plain_filter(record: Dict[str, Any]) -> bool:
        return filters["console"](record) and not _is_pretty_record(record)

    def _console_pretty_filter(record: Dict[str, Any]) -> bool:
        return filters["console"](record) and _is_pretty_record(record)

    def _pretty_console_sink(message: Any) -> None:
        wrote_header = False
        try:
            record = getattr(message, "record", None) or {}
            extra = record.get("extra", {}) if isinstance(record, dict) else {}
            kind = extra.get("pretty_kind")
            payload = extra.get("pretty_payload")

            # 先輸出 header line（沿用 loguru format）
            sys.stderr.write(str(message))
            wrote_header = True

            if not kind or not isinstance(payload, dict):
                return

            from .pretty_event import build_renderable, validate_pretty_payload

            try:
                validate_pretty_payload(str(kind), payload)
                renderable = build_renderable(str(kind), payload)
                get_console().print(renderable)
            except Exception:
                fallback = extra.get("pretty_text")
                if isinstance(fallback, str) and fallback.strip():
                    get_console().print(fallback, markup=False)
        except Exception:
            # sink 不能炸掉：最差就只印出 loguru 的字串輸出
            if not wrote_header:
                try:
                    sys.stderr.write(str(message))
                except Exception:
                    pass

    console_plain_handler_id = logger_instance.add(
        sys.stderr,
        format=actual_format,
        level=config.level,
        filter=_console_plain_filter,
    )
    managed_ids = getattr(logger_instance, "_pretty_loguru_managed_handler_ids", [])
    managed_ids.append(console_plain_handler_id)
    setattr(logger_instance, "_pretty_loguru_managed_handler_ids", managed_ids)

    console_pretty_handler_id = logger_instance.add(
        _pretty_console_sink,
        format=actual_format,
        level=config.level,
        filter=_console_pretty_filter,
        # Console pretty render 必須盡量維持「呼叫順序」與避免 stdout/stderr 交錯造成黏行；
        # 因此預設不使用 enqueue（enqueue=True 會改為背景佇列輸出，容易與使用者的 print 混在一起）。
        enqueue=False,
    )
    managed_ids = getattr(logger_instance, "_pretty_loguru_managed_handler_ids", [])
    managed_ids.append(console_pretty_handler_id)
    setattr(logger_instance, "_pretty_loguru_managed_handler_ids", managed_ids)

    # 5. 如果需要，新增 file handler
    if config.log_dir:
        log_dir = Path(config.log_dir)
        if config.subdirectory:
            log_dir = log_dir / config.subdirectory

        if log_dir.exists() and not log_dir.is_dir():
            raise ValueError(f"log_dir '{log_dir}' is not a directory")

        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 決定檔案名稱
        if config.use_native_format:
            # 使用原生格式時，檔案名使用 logger 名稱，不使用自定義格式
            log_filename = f"{config.name}.log"
        else:
            # 使用自定義格式時，保持原有行為
            from ..core.presets import get_preset_config
            preset_conf = get_preset_config(config.preset) if config.preset else {}
            log_name_format = preset_conf.get('name_format')
            log_filename = format_filename(config.component_name or config.name, log_name_format)
        logfile = log_dir / log_filename

        # 處理壓縮設定
        compression_function = config.compression
        if compression_function is True:
            warnings.warn(
                "compression=True is deprecated; use compression='gz' (or another loguru-supported string) instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            compression_function = "gz"
        elif compression_function is False:
            warnings.warn(
                "compression=False is deprecated; use compression=None instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            compression_function = None

        # 自定義壓縮/重命名格式（會覆蓋 compression_function）
        if config.compression_format:
            from ..core.presets import create_custom_compression_function
            compression_function = create_custom_compression_function(config.compression_format)

        file_settings = {
            "rotation": config.rotation,
            "retention": config.retention,
            "compression": compression_function,
            "encoding": "utf-8",
            "enqueue": True,
            "serialize": bool(config.serialize),
            "filter": filters["file"],
        }
        # 過濾掉值為 None 的設置
        file_settings = {k: v for k, v in file_settings.items() if v is not None}

        file_format = f"{actual_format}{{extra[pretty_text]}}"
        file_handler_id = logger_instance.add(
            str(logfile),
            format=file_format,
            level=config.level,
            **file_settings
        )
        managed_ids = getattr(logger_instance, "_pretty_loguru_managed_handler_ids", [])
        managed_ids.append(file_handler_id)
        setattr(logger_instance, "_pretty_loguru_managed_handler_ids", managed_ids)
        setattr(logger_instance, "_pretty_loguru_has_file_handler", True)
        if config.verbose:
            logger_instance.info(f"Logger '{config.name}' (ID: {config.name}): Log file path set to {logfile}")
    else:
        if config.verbose:
            logger_instance.info(f"Logger '{config.name}' (ID: {config.name}): Console only mode")
        # console handler 已在前面加入 managed ids

    # 6. 如果需要，新增 Loki sink（遠端收集）
    if config.loki_enabled:
        try:
            from ..integrations.loki import create_loki_sink

            labels = {"logger": str(config.name)}
            if config.component_name:
                labels.setdefault("component", str(config.component_name))
            if config.loki_labels:
                labels.update(config.loki_labels)

            sink = create_loki_sink(
                url=config.loki_base_url or "",
                labels=labels,
                batch_size=config.loki_batch_size,
                flush_interval_seconds=config.loki_flush_interval_seconds,
                timeout_seconds=config.loki_timeout_seconds,
                tenant_id=config.loki_tenant_id,
                username=config.loki_username,
                password=config.loki_password,
            )

            loki_handler_id = logger_instance.add(
                sink,
                level=config.level,
                format="{message}",
                serialize=True,
                enqueue=True,
                filter=filters["file"],
            )
            managed_ids = getattr(logger_instance, "_pretty_loguru_managed_handler_ids", [])
            managed_ids.append(loki_handler_id)
            setattr(logger_instance, "_pretty_loguru_managed_handler_ids", managed_ids)
        except Exception as e:
            warnings.warn(f"Failed to initialize Loki sink: {e}", UserWarning)
