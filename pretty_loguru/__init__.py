"""
pretty-loguru（core 預設匯出）

核心原則：
- `pretty_loguru` 頂層只匯出穩定 core API（Core Contract）
- addons / integrations 請改用顯式 import：`pretty_loguru.addons` / `pretty_loguru.integrations`

本專案已決定只保留最新版，不提供向後相容。
"""

from __future__ import annotations

import importlib
from typing import Any

from .types import PrettyLogger
from .core.base import configure_logger, get_console
from .core.config import LoggerConfig
from .factory.creator import (
    create_logger,
    default_logger,
    get_logger,
    set_logger,
    unregister_logger,
    list_loggers,
    reinit_logger,
    cleanup_loggers,
)

__all__ = [
    "PrettyLogger",
    "LoggerConfig",
    "configure_logger",
    "get_console",
    "create_logger",
    "default_logger",
    "get_logger",
    "set_logger",
    "unregister_logger",
    "list_loggers",
    "reinit_logger",
    "cleanup_loggers",
    "addons",
    "integrations",
]


def __getattr__(name: str) -> Any:
    """
    延遲載入 `pretty_loguru.addons` / `pretty_loguru.integrations`。

    目的：
    - 避免 `import pretty_loguru` 時就載入 heavy/optional 依賴（rich/fastapi/uvicorn...）
    - 讓 core contract 更穩定，並減少 import side-effects
    """
    if name == "addons":
        return importlib.import_module(".addons", __name__)
    if name == "integrations":
        return importlib.import_module(".integrations", __name__)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__version__ = "2.0.0b1"
