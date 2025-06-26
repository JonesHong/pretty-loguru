"""
Uvicorn 整合模組

此模組提供與 Uvicorn ASGI 伺服器的整合功能，
使 Uvicorn 的日誌能夠通過 Pretty Loguru 進行格式化和管理。
"""

import logging
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
        logger_names = ["uvicorn.asgi", "uvicorn.access", "uvicorn"]

    # 延遲獲取 default_logger
    if logger_instance is None:
        from ..factory.creator import default_logger
        logger_instance = default_logger()

    # 先移除所有現有的處理器，避免重複輸出
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    # 創建拦截处理器
    intercept_handler = InterceptHandler(logger_instance)
    
    # 添加到根 logger
    root_logger.addHandler(intercept_handler)
    root_logger.setLevel(level)

    # 設定 Uvicorn 特定日誌的處理器
    for logger_name in logger_names:
        logging_logger = logging.getLogger(logger_name)
        if logging_logger.handlers:
            for handler in logging_logger.handlers[:]:
                logging_logger.removeHandler(handler)
        logging_logger.addHandler(intercept_handler)
        logging_logger.propagate = False
        logging_logger.setLevel(level)

    # 記錄配置信息
    if logger_instance:
        logger_instance.debug(f"Uvicorn logging configured with level: {level}")