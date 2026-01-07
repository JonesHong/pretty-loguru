from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient
from starlette.requests import Request
from starlette.responses import PlainTextResponse, StreamingResponse

from pretty_loguru import create_logger
from pretty_loguru.integrations import (
    has_fastapi,
    has_uvicorn,
    integrate_fastapi,
    integrate_uvicorn,
    build_uvicorn_log_config,
    get_logger_dependency,
)
from pretty_loguru.integrations._errors import missing_dependency
from pretty_loguru.integrations.fastapi import _peek_request_body
from tests.conftest import capture_loguru_messages


def test_missing_dependency_message():
    e1 = missing_dependency("fastapi")
    assert isinstance(e1, ImportError)
    assert "pip install fastapi" in str(e1)

    e2 = missing_dependency("uvicorn", extra="integrations")
    assert 'pretty-loguru[integrations]' in str(e2)


def test_integrations_availability_flags():
    assert isinstance(has_uvicorn(), bool)
    assert isinstance(has_fastapi(), bool)


def test_uvicorn_build_log_config_and_integrate(tmp_path: Path):
    logger = create_logger("uv", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    cfg = build_uvicorn_log_config(logger_instance=logger, log_level="DEBUG", logger_names=["uvicorn.error"])
    assert cfg["version"] == 1
    assert "pretty_loguru_intercept" in cfg["handlers"]
    assert "uvicorn.error" in cfg["loggers"]

    cfg2 = integrate_uvicorn(logger, log_level="INFO", monkeypatch=False)
    assert isinstance(cfg2, dict)
    assert "loggers" in cfg2


def test_uvicorn_integrate_monkeypatch_path_restores(logging_cleanup: Any, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    monkeypatch=True 會修改 root logger handlers 與 uvicorn Config.configure_logging；
    測試內做快照並復原，避免影響其他測試。
    """
    logger = create_logger("uv_mp", log_dir=str(tmp_path / "logs"), enable_addons=False)
    logger.remove()

    import uvicorn.config

    original_configure = uvicorn.config.Config.configure_logging
    root = logging.getLogger()
    original_handlers = list(root.handlers)
    original_level = root.level

    try:
        result = integrate_uvicorn(logger, monkeypatch=True)
        assert result is None
        assert uvicorn.config.Config.configure_logging is not original_configure
        assert hasattr(uvicorn.config.Config, "_pretty_loguru_original_configure_logging")
        assert any(isinstance(h, logging.Handler) for h in logging.getLogger().handlers)
    finally:
        uvicorn.config.Config.configure_logging = original_configure
        root.handlers = original_handlers
        root.setLevel(original_level)


@pytest.mark.asyncio
async def test_peek_request_body_buffers_and_restores_receive():
    scope: Dict[str, Any] = {
        "type": "http",
        "asgi": {"spec_version": "2.3", "version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "headers": [],
        "client": ("test", 123),
        "server": ("testserver", 80),
    }

    messages: List[Dict[str, Any]] = [
        {"type": "http.request", "body": b"hello", "more_body": True},
        {"type": "http.request", "body": b"world", "more_body": False},
    ]

    async def receive():
        return messages.pop(0)

    req = Request(scope, receive)
    preview, truncated = await _peek_request_body(req, max_bytes=7)
    assert preview == b"hellowo"
    assert truncated is True

    # 後續讀取 body 應該仍拿得到完整資料（因為 _receive 被包裝回放）
    body = await req.body()
    assert body == b"helloworld"


@pytest.mark.asyncio
async def test_peek_request_body_cached_and_fallback_to_original_receive():
    scope: Dict[str, Any] = {
        "type": "http",
        "asgi": {"spec_version": "2.3", "version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "headers": [],
        "client": ("test", 123),
        "server": ("testserver", 80),
    }

    messages: List[Dict[str, Any]] = [{"type": "http.request", "body": b"TAIL", "more_body": False}]

    async def receive():
        return messages.pop(0)

    # cached_body 分支（_peek_request_body 會直接回傳 slice）
    req = Request(scope, receive)
    req._body = b"0123456789"  # type: ignore[attr-defined]
    preview, truncated = await _peek_request_body(req, max_bytes=5)
    assert preview == b"01234"
    assert truncated is True

    # buffer 用盡後會回到 original receive（new_receive 的 else 分支）
    messages2: List[Dict[str, Any]] = [{"type": "http.request", "body": b"TAIL", "more_body": False}]

    async def receive2():
        return messages2.pop(0)

    req2 = Request(scope, receive2)
    _preview2, _truncated2 = await _peek_request_body(req2, max_bytes=2)
    # buffered pop 完後再呼叫一次 _receive，會走到 `return await receive()`
    _ = await req2._receive()


def test_fastapi_middleware_and_route_logging(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    logger = create_logger("api", log_dir=str(tmp_path / "logs"), level="DEBUG", enable_addons=False)
    logger.remove()

    app = FastAPI()

    # 覆蓋 enable_uvicorn 分支（不真的改 uvicorn logging）
    monkeypatch.setattr("pretty_loguru.integrations.uvicorn.integrate_uvicorn", lambda *a, **k: None)

    integrate_fastapi(
        app,
        logger,
        middleware=True,
        custom_routes=False,
        enable_uvicorn=True,
        log_request_body=True,
        log_response_body=True,
        log_headers=True,
        sensitive_headers={"authorization"},
        max_body_bytes=8,
    )

    @app.post("/echo")
    async def echo(data: bytes = b""):
        return Response(content=data, media_type="application/octet-stream")

    @app.get("/stream")
    async def stream():
        return StreamingResponse(iter([b"a", b"b"]), media_type="text/plain")

    @app.get("/health")
    async def health():
        return {"ok": True}

    client = TestClient(app, raise_server_exceptions=False)

    with capture_loguru_messages(logger, formatter=lambda m: m.record) as records:
        r1 = client.post("/echo", content=b"hello", headers={"Authorization": "secret"})
        assert r1.status_code == 200

        r2 = client.post("/echo", content=b"\xff\xfe\xfd")  # binary request/response
        assert r2.status_code == 200

        r3 = client.post("/echo", content=b"0123456789")  # request too large -> skipped
        assert r3.status_code == 200

        r4 = client.get("/stream")
        assert r4.status_code == 200

    msgs = [r["message"] for r in records]
    assert any("Request [" in m and "POST /echo" in m for m in msgs)
    assert any("Response [" in m and "200" in m for m in msgs)
    assert any("headers" in m and "******" in m for m in msgs)
    assert any("binary data" in m for m in msgs)
    assert any("skipped, size" in m for m in msgs)
    assert any("streaming or not buffered" in m for m in msgs)


def test_fastapi_exclude_paths_and_custom_routes(tmp_path: Path):
    logger = create_logger("api2", log_dir=str(tmp_path / "logs"), level="DEBUG", enable_addons=False)
    logger.remove()

    app = FastAPI()

    integrate_fastapi(
        app,
        logger,
        middleware=True,
        custom_routes=True,
        enable_uvicorn=False,
        exclude_paths=["/health"],
        exclude_methods=["OPTIONS"],
        log_request_body=True,
        log_response_body=True,
        log_headers=True,
        log_request_body_if_unknown_length=True,
        max_body_bytes=8,
    )

    dep = get_logger_dependency(logger)

    @app.get("/health")
    async def health():
        return {"ok": True}

    @app.post("/route")
    async def route(lg=Depends(dep)):
        lg.info("inside")
        return PlainTextResponse("ok")

    @app.get("/boom")
    async def boom():
        raise RuntimeError("boom")

    client = TestClient(app, raise_server_exceptions=False)

    with capture_loguru_messages(logger, formatter=str) as msgs:
        # exclude_paths：/health 不應留下 request log（但仍會回應）
        assert client.get("/health").status_code == 200
        assert client.options("/route").status_code in (200, 405)

        assert client.post("/route").status_code == 200
        assert client.get("/boom").status_code == 500

    # custom route logging
    assert any("API Route" in m for m in msgs)
    assert any("inside" in m for m in msgs)

    # middleware exclude_paths / exclude_methods 不應產生 request log
    assert not any("Request [" in m and "/health" in m for m in msgs)


def test_import_time_stubs_when_dependencies_missing():
    """
    覆蓋 integrations 的 ImportError 分支（在本機環境通常不會發生）。
    這能避免 coverage 永遠被「缺依賴 stub」拖累。
    """
    import importlib
    from contextlib import contextmanager
    from importlib.abc import MetaPathFinder
    from importlib.machinery import ModuleSpec

    @contextmanager
    def block_import(prefix: str):
        class Blocker(MetaPathFinder):
            def find_spec(self, fullname: str, path, target=None) -> ModuleSpec | None:  # type: ignore[override]
                if fullname == prefix or fullname.startswith(prefix + "."):
                    raise ImportError(f"blocked: {fullname}")
                return None

        blocker = Blocker()
        sys.meta_path.insert(0, blocker)
        try:
            yield
        finally:
            sys.meta_path = [x for x in sys.meta_path if x is not blocker]

    import pretty_loguru.integrations.fastapi as fastapi_mod
    import pretty_loguru.integrations.uvicorn as uvicorn_mod

    # fastapi missing -> 走 stub functions/classes（用 reload 讓相對匯入仍可用）
    with block_import("fastapi"):
        saved_fastapi = {k: v for k, v in list(sys.modules.items()) if k == "fastapi" or k.startswith("fastapi.")}
        for k in saved_fastapi:
            sys.modules.pop(k, None)
        importlib.reload(fastapi_mod)
        with pytest.raises(ImportError):
            fastapi_mod.integrate_fastapi()  # type: ignore[misc]
        with pytest.raises(ImportError):
            fastapi_mod.setup_fastapi_logging()  # type: ignore[misc]
        with pytest.raises(ImportError):
            fastapi_mod.get_logger_dependency()  # type: ignore[misc]
        with pytest.raises(ImportError):
            fastapi_mod.install_fastapi_middleware()  # type: ignore[misc]
        with pytest.raises(ImportError):
            fastapi_mod.install_fastapi_route_class()  # type: ignore[misc]
        with pytest.raises(ImportError):
            fastapi_mod.LoggingMiddleware(None)  # type: ignore[call-arg]
        with pytest.raises(ImportError):
            fastapi_mod.LoggingRoute()  # type: ignore[call-arg]
        sys.modules.update(saved_fastapi)

    # restore
    importlib.reload(fastapi_mod)

    # uvicorn missing -> build/integrate 會 raise missing_dependency()
    with block_import("uvicorn"):
        saved_uvicorn = {k: v for k, v in list(sys.modules.items()) if k == "uvicorn" or k.startswith("uvicorn.")}
        for k in saved_uvicorn:
            sys.modules.pop(k, None)
        importlib.reload(uvicorn_mod)
        with pytest.raises(ImportError):
            uvicorn_mod.build_uvicorn_log_config()
        with pytest.raises(ImportError):
            uvicorn_mod.integrate_uvicorn()
        sys.modules.update(saved_uvicorn)

    # restore
    importlib.reload(uvicorn_mod)


@pytest.fixture
def logging_cleanup():
    # placeholder fixture，方便將來擴充（例如 snapshot logging state）
    yield
