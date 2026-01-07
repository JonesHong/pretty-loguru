"""
整合模組入口

此模組提供與第三方庫和框架的整合功能，使 Pretty Loguru 能夠
與各種流行的 Python 工具和框架無縫協作。
"""

from . import uvicorn as _uvicorn
from . import fastapi as _fastapi

setup_uvicorn_logging = _uvicorn.setup_uvicorn_logging
integrate_uvicorn = _uvicorn.integrate_uvicorn
build_uvicorn_log_config = _uvicorn.build_uvicorn_log_config
InterceptHandler = _uvicorn.InterceptHandler
_has_uvicorn = bool(getattr(_uvicorn, "_has_uvicorn", False))

# 對 Sphinx 說明：這是轉出來的，不需要索引
InterceptHandler.__doc__ = """
:meta noindex:

參見 :class:`pretty_loguru.integrations.uvicorn.InterceptHandler`
"""

setup_fastapi_logging = _fastapi.setup_fastapi_logging
integrate_fastapi = _fastapi.integrate_fastapi
get_logger_dependency = _fastapi.get_logger_dependency
LoggingMiddleware = _fastapi.LoggingMiddleware
LoggingRoute = _fastapi.LoggingRoute
_has_fastapi = bool(getattr(_fastapi, "_has_fastapi", False))

# Loki（stdlib only, always available）
from .loki import (
    LokiSink,
    LokiSinkConfig,
    create_loki_sink,
)

# 定義對外可見的功能
__all__ = [
    "setup_uvicorn_logging",
    "integrate_uvicorn",
    "build_uvicorn_log_config",
    "InterceptHandler",
    "setup_fastapi_logging",
    "integrate_fastapi",
    "get_logger_dependency",
    "LoggingMiddleware",
    "LoggingRoute",
    "LokiSink",
    "LokiSinkConfig",
    "create_loki_sink",
]

# 提供檢查各種整合是否可用的函數
def has_uvicorn() -> bool:
    """
    檢查 Uvicorn 整合是否可用
    
    Returns:
        bool: 如果 Uvicorn 整合可用則返回 True，否則返回 False
    """
    return _has_uvicorn

def has_fastapi() -> bool:
    """
    檢查 FastAPI 整合是否可用
    
    Returns:
        bool: 如果 FastAPI 整合可用則返回 True，否則返回 False
    """
    return _has_fastapi
