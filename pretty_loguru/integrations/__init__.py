"""
整合模組入口

此模組提供與第三方庫和框架的整合功能，使 Pretty Loguru 能夠
與各種流行的 Python 工具和框架無縫協作。
"""

try:
    from .uvicorn import (
        configure_uvicorn,
        InterceptHandler,
    )
    # 對 Sphinx 說明：這是轉出來的，不需要索引
    InterceptHandler.__doc__ = """
    :meta noindex:

    參見 :class:`pretty_loguru.integrations.uvicorn.InterceptHandler`
    """
    _has_uvicorn = True
except ImportError:
    _has_uvicorn = False

# 定義對外可見的功能
__all__ = []

# 如果 Uvicorn 可用，則添加相關功能
if _has_uvicorn:
    __all__.extend([
        "configure_uvicorn",
        "InterceptHandler",
    ])

# 提供檢查各種整合是否可用的函數
def has_uvicorn() -> bool:
    """
    檢查 Uvicorn 整合是否可用
    
    Returns:
        bool: 如果 Uvicorn 整合可用則返回 True，否則返回 False
    """
    return _has_uvicorn
