"""
Uvicorn 整合模組

此模組提供與 Uvicorn ASGI 伺服器的整合功能，
使 Uvicorn 的日誌能夠通過 Pretty Loguru 進行格式化和管理。
"""

import logging
import re
import sys
from typing import cast, Optional, Dict, Any, List
import warnings

try:
    import uvicorn
    _has_uvicorn = True
except ImportError:
    _has_uvicorn = False
    warnings.warn(
        "Uvicorn package is not installed. Uvicorn integration will not be available. You can install it using 'pip install uvicorn'.",
        ImportWarning,
        stacklevel=2
    )

from ..types import EnhancedLogger, LogLevelType


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


def configure_uvicorn(
    logger_instance: Optional[Any] = None,
    level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None
) -> None:
    """
    配置 Uvicorn 日誌以使用 Loguru 格式化輸出

    此函數用於將 Uvicorn 的日誌輸出格式改為 Loguru 的格式，
    適合需要統一日誌格式的應用場景。

    Args:
        logger_instance: 要使用的 logger 實例，如果為 None 則使用默認 logger
        level: 日誌級別，預設為 "INFO"
        logger_names: 要配置的 logger 名稱列表，默認為 Uvicorn 相關的 logger

    Raises:
        ImportError: 如果 uvicorn 未安裝
    """
    if not _has_uvicorn:
        raise ImportError("未安裝 uvicorn 套件，無法配置 Uvicorn 日誌。可使用 'pip install uvicorn' 安裝。")

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
    root_logger.setLevel(level)

    # 設定 Uvicorn 特定日誌的處理器
    for logger_name in logger_names:
        logging_logger = logging.getLogger(logger_name)
        for handler in logging_logger.handlers[:]:
            logging_logger.removeHandler(handler)
        logging_logger.addHandler(intercept_handler)
        logging_logger.propagate = False
        logging_logger.setLevel(level)

    # 記錄配置信息
    if logger_instance:
        logger_instance.debug(f"Uvicorn logging configured with level: {level}")


def setup_uvicorn_logging(logger_instance: Optional[Any] = None, level: LogLevelType = "INFO"):
    """在 uvicorn.run 之前調用此函數來設置日誌攔截"""
    configure_uvicorn(logger_instance, level)
    
    # 確保 uvicorn 使用我們的配置
    import uvicorn.config
    import uvicorn.server
    
    # 保存原始的 configure_logging 方法
    _original_configure_logging = uvicorn.config.Config.configure_logging
    
    def patched_configure_logging(self):
        # 先調用原始方法
        _original_configure_logging(self)
        # 然後重新配置為我們的攔截器
        configure_uvicorn(logger_instance, level)
    
    # 替換方法
    uvicorn.config.Config.configure_logging = patched_configure_logging


def integrate_uvicorn(
    logger: Any,
    level: LogLevelType = "INFO",
    logger_names: Optional[List[str]] = None
) -> None:
    """
    將 Uvicorn 與 Pretty Loguru logger 進行集成
    
    Args:
        logger: Pretty Loguru logger 實例 (必需)
        level: 日誌級別，預設為 "INFO"
        logger_names: 要配置的 logger 名稱列表，默認為 Uvicorn 相關的 logger
    
    Example:
        from pretty_loguru import create_logger
        from pretty_loguru.integrations.uvicorn import integrate_uvicorn
        
        logger = create_logger("my_app", log_path="./logs")
        integrate_uvicorn(logger)
        
        # 然後正常使用 uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    """
    if not _has_uvicorn:
        raise ImportError("未安裝 uvicorn 套件，無法配置 Uvicorn 日誌。可使用 'pip install uvicorn' 安裝。")
    
    # 調用原有的配置函數
    configure_uvicorn(logger, level, logger_names)
    
    # 確保 uvicorn 使用我們的配置
    import uvicorn.config
    import uvicorn.server
    
    # 保存原始的 configure_logging 方法
    _original_configure_logging = uvicorn.config.Config.configure_logging
    
    def patched_configure_logging(self):
        # 先調用原始方法
        _original_configure_logging(self)
        # 然後重新配置為我們的攔截器
        configure_uvicorn(logger, level, logger_names)
    
    # 替換方法
    uvicorn.config.Config.configure_logging = patched_configure_logging
    