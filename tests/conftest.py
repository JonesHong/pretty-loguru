from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Iterator, List

import pytest
from loguru import logger as _base_logger

from pretty_loguru import cleanup_loggers


@pytest.fixture(autouse=True)
def _isolate_pretty_loguru_global_state() -> Iterator[None]:
    """
    pretty-loguru / loguru 共享全域 core（handlers/queue），測試必須隔離避免互相干擾。
    """
    try:
        from pretty_loguru.core.event_system import clear_events
        clear_events()
    except Exception:
        pass

    cleanup_loggers()
    try:
        _base_logger.remove()
    except Exception:
        pass

    yield

    cleanup_loggers()
    try:
        _base_logger.remove()
    except Exception:
        pass

    try:
        from pretty_loguru.core.event_system import clear_events
        clear_events()
    except Exception:
        pass


@contextmanager
def capture_loguru_messages(
    logger_instance: Any,
    *,
    level: str = "DEBUG",
    formatter: Callable[[Any], Any] | None = None,
) -> Iterator[List[Any]]:
    """
    以同步方式捕捉指定 logger 的 loguru messages（避免 enqueue 造成測試不穩）。

    `formatter` 可把 message 轉成你要的型別（例如 str 或 record dict）。
    """
    items: List[Any] = []

    def sink(message: Any) -> None:
        items.append(formatter(message) if formatter else message)

    handler_id = logger_instance.add(sink, level=level, enqueue=False)
    try:
        yield items
    finally:
        try:
            logger_instance.remove(handler_id)
        except Exception:
            pass
