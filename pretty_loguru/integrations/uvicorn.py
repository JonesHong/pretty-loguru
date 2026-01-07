"""
Uvicorn 整合模組

此模組提供與 Uvicorn ASGI 伺服器的整合功能，
使 Uvicorn 的日誌能夠通過 Pretty Loguru 進行格式化和管理。
"""

import logging
import re
import sys
from typing import cast, Optional, Dict, Any, List

try:
    import uvicorn
    _has_uvicorn = True
except ImportError:
    _has_uvicorn = False

from ..types import PrettyLogger, LogLevelType
from ._errors import missing_dependency

_saved_logging_state: Dict[str, Any] | None = None

class InterceptHandler(logging.Handler):
    """
    攔截標準日誌庫的日誌並轉發給 Loguru

    此處理器用於將 Python 標準日誌庫的日誌消息攔截並轉發到 Loguru，
    實現統一的日誌管理，特別適用於 Uvicorn 等使用標準日誌庫的第三方庫。
    """

    def __init__(self, logger_instance: Optional[Any] = None):
        """
        初始化攔截處理器

        Args:
            logger_instance: 要使用的 logger 實例，如果為 None 則使用默認 logger
        """
        super().__init__()
        # 延遲導入，避免循環依賴
        if logger_instance is None:
            from ..factory.creator import default_logger
            self.logger = default_logger()
        else:
            self.logger = logger_instance

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        處理日誌記錄，將其轉發給 Loguru。

        Args:
            record: 標準日誌庫的日誌記錄物件。
        """
        # 避免遞歸處理
        # 跳過由 Loguru 產生的日誌記錄
        msg = record.getMessage()
        if record.name == "uvicorn.error" and msg.startswith("Traceback "):
            # 避免重複的異常追蹤
            return

        try:
            # 嘗試獲取對應的 Loguru 日誌等級
            level = self.logger.level(record.levelname).name
        except ValueError:
            # 如果無法匹配，則使用數字等級
            level = str(record.levelno)

        # 獲取日誌消息的調用來源
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # 避免定位到標準日誌庫內部
            frame = frame.f_back
            depth += 1

        # 使用 Loguru 記錄日誌，包含調用深度與異常資訊
        self.logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


def build_uvicorn_log_config(
    logger_instance: Optional[Any] = None,
    log_level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    建立可直接傳入 `uvicorn.run(..., log_config=...)` 的 logging config dict（non-monkeypatch）。

    這是推薦路徑：不修改 uvicorn 內部方法，只提供一份 log_config 讓 uvicorn 採用。
    """
    if not _has_uvicorn:
        raise missing_dependency("uvicorn", extra="integrations")

    if logger_names is None:
        logger_names = ["uvicorn.asgi", "uvicorn.access", "uvicorn", "uvicorn.error"]

    if logger_instance is None:
        from ..factory.creator import default_logger
        logger_instance = default_logger()

    loggers: Dict[str, Any] = {}
    for name in logger_names:
        loggers[name] = {
            "handlers": ["pretty_loguru_intercept"],
            "level": log_level,
            "propagate": False,
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "pretty_loguru_intercept": {
                "()": "pretty_loguru.integrations.uvicorn.InterceptHandler",
                "logger_instance": logger_instance,
            }
        },
        "root": {"handlers": ["pretty_loguru_intercept"], "level": log_level},
        "loggers": loggers,
    }


def _configure_uvicorn_logging(
    logger_instance: Optional[Any] = None,
    log_level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None
) -> None:
    """
    配置 Uvicorn 日誌以使用 Loguru 格式化輸出

    此函數用於將 Uvicorn 的日誌輸出格式改為 Loguru 的格式，
    適合需要統一日誌格式的應用場景。

    Args:
        logger_instance: 要使用的 logger 實例，如果為 None 則使用默認 logger
        log_level: 日誌級別，預設為 "INFO"（對齊 `uvicorn.run(..., log_level=...)`）
        logger_names: 要配置的 logger 名稱列表，默認為 Uvicorn 相關的 logger

    Raises:
        ImportError: 如果 uvicorn 未安裝
    """
    if not _has_uvicorn:
        raise missing_dependency("uvicorn", extra="integrations")

    # 默認的 Uvicorn logger 名稱
    if logger_names is None:
        logger_names = ["uvicorn.asgi", "uvicorn.access", "uvicorn", "uvicorn.error"]

    # 延遲獲取 default_logger
    if logger_instance is None:
        from ..factory.creator import default_logger
        logger_instance = default_logger()

    # 創建拦截处理器
    intercept_handler = InterceptHandler(logger_instance)
    
    # 先移除所有現有的處理器，避免重複輸出
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 添加到根 logger
    root_logger.addHandler(intercept_handler)
    root_logger.setLevel(log_level)

    # 設定 Uvicorn 特定日誌的處理器
    for logger_name in logger_names:
        logging_logger = logging.getLogger(logger_name)
        for handler in logging_logger.handlers[:]:
            logging_logger.removeHandler(handler)
        logging_logger.addHandler(intercept_handler)
        logging_logger.propagate = False
        logging_logger.setLevel(log_level)

    # 記錄配置信息
    if logger_instance:
        logger_instance.debug(f"Uvicorn logging configured with log_level: {log_level}")


def setup_uvicorn_logging(logger_instance: Optional[Any] = None, log_level: LogLevelType = "INFO"):
    """
    在 uvicorn.run 之前調用此函數來設置日誌攔截（monkeypatch）。

    注意：此方法會 monkeypatch `uvicorn.config.Config.configure_logging`，請謹慎使用。
    建議優先改用 `build_uvicorn_log_config()` 並傳入 uvicorn.run 的 `log_config=`。
    """
    if logger_instance is None:
        from ..factory.creator import default_logger
        logger_instance = default_logger()

    integrate_uvicorn(logger_instance, log_level=log_level, monkeypatch=True)


def integrate_uvicorn(
    logger: Optional[Any] = None,
    log_level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None,
    *,
    monkeypatch: bool = False,
    snapshot_all_loggers: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    將 Uvicorn 與 Pretty Loguru logger 進行集成
    
    Args:
        logger: Pretty Loguru logger 實例 (必需)
        log_level: 日誌級別，預設為 "INFO"
        logger_names: 要配置的 logger 名稱列表，默認為 Uvicorn 相關的 logger
        monkeypatch: 是否 monkeypatch `uvicorn.config.Config.configure_logging`（預設 False）
    
    Example:
        from pretty_loguru import create_logger
        from pretty_loguru.integrations.uvicorn import integrate_uvicorn
        
        logger = create_logger("my_app", log_dir="./logs")
        log_config = integrate_uvicorn(logger)
        
        # 然後正常使用 uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
    """
    if not _has_uvicorn:
        raise missing_dependency("uvicorn", extra="integrations")

    if not monkeypatch:
        return build_uvicorn_log_config(
            logger_instance=logger,
            log_level=log_level,
            logger_names=logger_names,
        )

    # monkeypatch 路徑（顯式啟用）
    import uvicorn.config

    global _saved_logging_state
    if _saved_logging_state is None:
        root_logger = logging.getLogger()
        saved_loggers = {}
        target_names = (
            list(logging.root.manager.loggerDict.keys())
            if snapshot_all_loggers
            else (logger_names or ["uvicorn.asgi", "uvicorn.access", "uvicorn", "uvicorn.error"])
        )
        for name in target_names:
            lg = logging.getLogger(name)
            saved_loggers[name] = {
                "handlers": list(lg.handlers),
                "propagate": lg.propagate,
                "level": lg.level,
            }
        _saved_logging_state = {
            "root_handlers": list(root_logger.handlers),
            "root_level": root_logger.level,
            "loggers": saved_loggers,
        }

    _configure_uvicorn_logging(logger, log_level=log_level, logger_names=logger_names)

    original = getattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging", None)
    if original is None:
        setattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging", uvicorn.config.Config.configure_logging)
        original = uvicorn.config.Config.configure_logging

    def patched_configure_logging(self):
        original(self)
        _configure_uvicorn_logging(logger, log_level=log_level, logger_names=logger_names)

    uvicorn.config.Config.configure_logging = patched_configure_logging
    return None


def restore_uvicorn_logging() -> None:
    """
    還原被 monkeypatch 的 uvicorn logging 行為（若曾呼叫 integrate_uvicorn(monkeypatch=True)）。
    """
    if not _has_uvicorn:
        return
    import uvicorn.config

    original = getattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging", None)
    if original is not None:
        uvicorn.config.Config.configure_logging = original
        delattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging")

    global _saved_logging_state
    if _saved_logging_state:
        root_logger = logging.getLogger()
        root_logger.handlers[:] = _saved_logging_state.get("root_handlers", [])
        root_logger.setLevel(_saved_logging_state.get("root_level", root_logger.level))

        for name, state in _saved_logging_state.get("loggers", {}).items():
            lg = logging.getLogger(name)
            lg.handlers[:] = state.get("handlers", [])
            lg.propagate = state.get("propagate", lg.propagate)
            lg.setLevel(state.get("level", lg.level))

        _saved_logging_state = None
