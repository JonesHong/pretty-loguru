"""
診斷與觀測性工具。
"""

from typing import Any, Dict, List

from . import registry
from ..factory import creator


def get_cleaner_status() -> List[str]:
    """列出目前活躍的 cleaner 路徑。"""
    with creator._cleaner_lock:  # type: ignore[attr-defined]
        return list(getattr(creator, "_active_cleaners", {}).keys())


def get_handler_status() -> Dict[str, Dict[str, Any]]:
    """
    回傳各 logger 的 managed/user handler ids 以便排障。
    """
    status: Dict[str, Dict[str, Any]] = {}
    for name in registry.list_loggers():
        lg = registry.get_logger(name)
        if lg is None:
            continue
        status[name] = {
            "managed_handler_ids": list(getattr(lg, "_pretty_loguru_managed_handler_ids", []) or []),
            "user_handler_ids": list(getattr(lg, "_pretty_loguru_user_handler_ids", []) or []),
            "has_file_handler": bool(getattr(lg, "_pretty_loguru_has_file_handler", False)),
        }
    return status


def get_default_logger_state() -> Dict[str, Any]:
    """回報 default_logger 是否已建立。"""
    return {
        "default_logger_initialized": getattr(creator, "_default_logger_instance", None) is not None
    }
