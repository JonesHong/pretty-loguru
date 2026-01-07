"""
目標導向格式化工具模組

此模組提供目標導向輸出（console / file）的輔助函式與共用工具。

本專案以「單一路徑」為原則：避免在 logger 上注入 `console_*` / `file_*` 類方法，
改以 loguru 原生 `bind()`（搭配 filters）或輔助函式 `log_to_targets()` 控制輸出去向。
"""

import sys
from typing import Any, Callable


def log_to_targets(
    logger_instance: Any,
    message: str,
    level: str = "INFO",
    console_only: bool = False,
    file_only: bool = False
) -> None:
    """
    目標日誌函數，支援分離的控制台和檔案輸出
    
    Args:
        logger_instance: Logger 實例
        message: 要記錄的消息
        level: 日誌級別
        console_only: 是否僅輸出到控制台
        file_only: 是否僅輸出到文件
    """
    if console_only and file_only:
        raise ValueError("console_only 和 file_only 不能同時為 True")
    
    if not logger_instance:
        return

    # 單一路徑：永遠只送出「一筆」loguru event，靠 filter 決定 console/file 去向
    if console_only:
        logger_instance.opt(depth=1).bind(to_console_only=True).log(level, message)
        return

    if file_only:
        logger_instance.opt(depth=1).bind(to_file_only=True).log(level, message)
        return

    # both
    logger_instance.opt(depth=1).log(level, message)


def mark_file_handler(logger_instance: Any, enabled: bool = True) -> None:
    """標記 logger 是否有檔案輸出 handler，供目標輸出判斷使用"""
    setattr(logger_instance, "_pretty_loguru_has_file_handler", enabled)

def ensure_target_parameters(method: Callable) -> Callable:
    """
    確保格式化方法接受目標導向參數（最新版本：不提供向後相容模式）

    目前 pretty-loguru 的 formats 會使用下列參數控制輸出目標與呼叫深度：
    - to_console_only / to_file_only：由 filters 決定輸出到 console/file
    - _target_depth：用於 logger.opt(depth=...) 正確定位呼叫來源
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("to_console_only", False)
        kwargs.setdefault("to_file_only", False)
        kwargs.setdefault("_target_depth", 2)
        return method(*args, **kwargs)

    wrapper.__name__ = method.__name__
    wrapper.__doc__ = method.__doc__
    return wrapper
