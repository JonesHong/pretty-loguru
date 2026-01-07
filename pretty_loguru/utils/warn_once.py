"""
單次警告輔助工具。

透過 key 去重，同一 key 只會警告一次；可用環境變數關閉或改為 debug。
"""

import os
import warnings
from typing import Any, Hashable, Optional, Type

_seen: set[Hashable] = set()


def warn_once(message: str, category: Type[Warning] = UserWarning, *, key: Optional[Hashable] = None) -> None:
    """
    發出一次性的警告，同一 key 僅警告一次。

    環境變數：
    - PRETTY_LOGURU_WARNINGS_SUPPRESS=1/true：完全不輸出。
    """
    suppress = os.getenv("PRETTY_LOGURU_WARNINGS_SUPPRESS", "").lower() in ("1", "true", "yes")
    if suppress:
        return
    k = key if key is not None else message
    if k in _seen:
        return
    _seen.add(k)
    warnings.warn(message, category)
