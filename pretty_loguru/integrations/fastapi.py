"""
FastAPI 整合模組

此模組提供與 FastAPI 框架的整合功能，包括請求日誌中間件、
依賴注入和異常處理器，使 FastAPI 應用能夠充分利用 Pretty Loguru。
"""

import time
from typing import Callable, Optional, Dict, Any, Union, List, Set, Tuple
import typing
import warnings

try:
    from fastapi import FastAPI, Request, Response, Depends
    from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
    from fastapi.routing import APIRoute

    _has_fastapi = True
except ImportError:
    _has_fastapi = False

from ..types import PrettyLogger, LogLevelType, LogRotationType, LogDirType
from ..factory.creator import create_logger, default_logger
from ._errors import missing_dependency


if _has_fastapi:

    async def _peek_request_body(request: Request, max_bytes: int) -> Tuple[bytes, bool]:
        """
        讀取最多 max_bytes 的 request body 預覽，並保留原始資料供後續處理。
        """
        cached_body = getattr(request, "_body", None)
        if cached_body is not None:
            return cached_body[:max_bytes], len(cached_body) > max_bytes

        receive = request._receive
        buffered = []
        preview = b""
        collected = 0
        more_body = True
        truncated = False

        while more_body and collected < max_bytes:
            message = await receive()
            buffered.append(message)
            body = message.get("body", b"")
            if body:
                take = min(max_bytes - collected, len(body))
                preview += body[:take]
                if take < len(body):
                    truncated = True
                collected += take
            more_body = message.get("more_body", False)
            if not more_body:
                break

        if more_body:
            truncated = True

        async def new_receive():
            if buffered:
                return buffered.pop(0)
            return await receive()

        request._receive = new_receive
        return preview, truncated

    class LoggingMiddleware(BaseHTTPMiddleware):
        """
        FastAPI 日誌中間件，記錄請求和響應的詳細信息
        """

        def __init__(
            self,
            app: FastAPI,
            logger_instance: Optional[PrettyLogger] = None,
            exclude_paths: Optional[List[str]] = None,
            exclude_methods: Optional[List[str]] = None,
            log_request_body: bool = False,
            log_response_body: bool = False,
            log_headers: bool = True,
            sensitive_headers: Optional[Set[str]] = None,
            log_request_body_if_unknown_length: bool = False,
            max_body_bytes: int = 1000,
        ):
            """
            初始化日誌中間件

            Args:
                app: FastAPI 應用實例
                logger_instance: 要使用的 logger 實例，如果為 None 則使用默認 logger
                exclude_paths: 不記錄日誌的路徑列表，例如 ["/health", "/metrics"]
                exclude_methods: 不記錄日誌的 HTTP 方法列表，例如 ["OPTIONS"]
                log_request_body: 是否記錄請求體，預設為 False
                log_response_body: 是否記錄響應體，預設為 False
                log_headers: 是否記錄請求和響應頭，預設為 True
                sensitive_headers: 敏感頭部字段集合，這些字段的值將被遮蔽
                log_request_body_if_unknown_length: 若無 content-length 是否記錄請求體
                max_body_bytes: 記錄 body 的最大大小（bytes），預設為 1000
            """
            super().__init__(app)
            # 使用函數調用而不是直接引用，確保延遲初始化
            self.logger = logger_instance or default_logger()
            self.exclude_paths = exclude_paths or []
            self.exclude_methods = [m.upper() for m in (exclude_methods or [])]
            self.log_request_body = log_request_body
            self.log_response_body = log_response_body
            self.log_headers = log_headers
            self.log_request_body_if_unknown_length = log_request_body_if_unknown_length
            self.max_body_bytes = max_body_bytes
            self.sensitive_headers = {
                h.lower()
                for h in (
                    sensitive_headers or {"authorization", "cookie", "set-cookie"}
                )
            }

        async def dispatch(
            self,
            request: Request,
            call_next: typing.Callable[[Request], typing.Awaitable[Response]],
        ) -> Response:
            """
            處理請求和響應，記錄相關日誌

            Args:
                request: FastAPI 請求對象
                call_next: 處理請求的下一個函數

            Returns:
                Response: FastAPI 響應對象
            """
            # 檢查是否需要記錄此請求
            path = request.url.path
            method = request.method

            if path in self.exclude_paths or method in self.exclude_methods:
                return await call_next(request)

            # 記錄請求信息
            request_id = f"{time.time():.9f}"
            client_host = request.client.host if request.client else "unknown"
            client_port = request.client.port if request.client else 0

            self.logger.info(
                f"Request [{request_id}]: {method} {path} from {client_host}:{client_port}"
            )

            # 記錄請求頭
            if self.log_headers:
                headers = dict(request.headers.items())
                sanitized_headers = self._sanitize_headers(headers)
                self.logger.debug(
                    f"Request [{request_id}] headers: {sanitized_headers}"
                )

            # 記錄請求體
            if self.log_request_body:
                try:
                    content_length = request.headers.get("content-length")
                    if content_length and content_length.isdigit():
                        if int(content_length) > self.max_body_bytes:
                            self.logger.debug(
                                f"Request [{request_id}] body: <skipped, size {content_length} bytes exceeds limit>"
                            )
                        else:
                            body = await request.body()
                            try:
                                if len(body) > self.max_body_bytes:
                                    body = body[: self.max_body_bytes]
                                    suffix = "... (truncated)"
                                else:
                                    suffix = ""
                                body_text = body.decode("utf-8")
                                self.logger.debug(
                                    f"Request [{request_id}] body: {body_text}{suffix}"
                                )
                            except UnicodeDecodeError:
                                self.logger.debug(
                                    f"Request [{request_id}] body: <binary data, size: {len(body)} bytes>"
                                )
                    else:
                        if not self.log_request_body_if_unknown_length:
                            self.logger.debug(
                                f"Request [{request_id}] body: <skipped, content-length unknown>"
                            )
                        else:
                            preview, truncated = await _peek_request_body(
                                request, self.max_body_bytes
                            )
                            try:
                                body_text = preview.decode("utf-8")
                                suffix = "... (truncated)" if truncated else ""
                                self.logger.debug(
                                    f"Request [{request_id}] body: {body_text}{suffix}"
                                )
                            except UnicodeDecodeError:
                                self.logger.debug(
                                    f"Request [{request_id}] body: <binary data, size: {len(preview)} bytes>"
                                )
                except Exception as e:
                    self.logger.debug(
                        f"Request [{request_id}] body: <unable to read body: {type(e).__name__}>"
                    )

            # 記錄響應時間和狀態
            start_time = time.time()
            try:
                response = await call_next(request)
                process_time = time.time() - start_time

                self.logger.info(
                    f"Response [{request_id}]: {response.status_code} in {process_time:.3f}s"
                )

                # 記錄響應頭
                if self.log_headers:
                    sanitized_headers = self._sanitize_headers(
                        dict(response.headers.items())
                    )
                    self.logger.debug(
                        f"Response [{request_id}] headers: {sanitized_headers}"
                    )

                # 記錄響應體
                if self.log_response_body:
                    try:
                        body = getattr(response, "body", None)
                        if body is None:
                            self.logger.debug(
                                f"Response [{request_id}] body: <streaming or not buffered>"
                            )
                        else:
                            if isinstance(body, memoryview):
                                body = body.tobytes()
                            if isinstance(body, bytes):
                                try:
                                    if len(body) > self.max_body_bytes:
                                        preview = body[: self.max_body_bytes]
                                        suffix = "... (truncated)"
                                    else:
                                        preview = body
                                        suffix = ""
                                    body_text = preview.decode("utf-8")
                                    self.logger.debug(
                                        f"Response [{request_id}] body: {body_text}{suffix}"
                                    )
                                except UnicodeDecodeError:
                                    self.logger.debug(
                                        f"Response [{request_id}] body: <binary data, size: {len(body)} bytes>"
                                    )
                            else:
                                body_text = str(body)
                                if len(body_text.encode('utf-8')) > self.max_body_bytes:
                                    body_text = body_text.encode("utf-8")[: self.max_body_bytes].decode(
                                        "utf-8", errors="ignore"
                                    ) + "... (truncated)"
                                self.logger.debug(
                                    f"Response [{request_id}] body: {body_text}"
                                )
                    except Exception as e:
                        self.logger.debug(
                            f"Response [{request_id}] body: <unable to read body: {type(e).__name__}>"
                        )

                return response
            except Exception as exc:
                process_time = time.time() - start_time
                self.logger.error(
                    f"Response [{request_id}]: Exception after {process_time:.3f}s - {exc.__class__.__name__}: {str(exc)}"
                )
                raise

        def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
            """
            處理請求/響應頭，遮蔽敏感信息

            Args:
                headers: 原始頭部字典

            Returns:
                Dict[str, str]: 處理後的頭部字典
            """
            sanitized = {}
            for key, value in headers.items():
                if key.lower() in self.sensitive_headers:
                    sanitized[key] = "******"
                else:
                    sanitized[key] = value
            return sanitized

    class LoggingRoute(APIRoute):
        """
        帶有日誌功能的 FastAPI 路由

        此類擴展了標準的 FastAPI 路由，添加了請求和響應的日誌記錄功能。
        """

        def __init__(
            self,
            *args: Any,
            logger_instance: Optional[PrettyLogger] = None,
            log_request_body: bool = False,
            log_response_body: bool = False,
            log_request_body_if_unknown_length: bool = False,
            max_body_bytes: int = 1000,
            **kwargs: Any,
        ):
            """
            建立帶有日誌功能的 route。

            Args:
                logger_instance: 用於輸出路由日誌的 logger（預設 `default_logger()`）。
                log_request_body: 是否記錄 request body（注意隱私與大小）。
                log_response_body: 是否記錄 response body（注意隱私與大小）。
                log_request_body_if_unknown_length: 沒有 content-length 時是否仍嘗試記錄 request body。
                max_body_bytes: 最多記錄多少 bytes（超過會截斷或略過）。
            """
            # 使用函數調用而不是直接引用，確保延遲初始化
            self.logger = logger_instance or default_logger()
            self.log_request_body = log_request_body
            self.log_response_body = log_response_body
            self.log_request_body_if_unknown_length = log_request_body_if_unknown_length
            self.max_body_bytes = max_body_bytes
            super().__init__(*args, **kwargs)

        def get_route_handler(self) -> Callable:
            """
            回傳 FastAPI 用來處理 request 的 handler（帶有日誌紀錄）。

            實作策略：
            - 先取得 FastAPI 原始 handler
            - 用 wrapper 包一層，在呼叫前後記錄 request/response（可選 body）
            """
            original_route_handler = super().get_route_handler()

            async def custom_route_handler(request: Request) -> Response:
                # 記錄請求信息
                request_id = f"{time.time():.9f}"
                self.logger.info(
                    f"API Route [{request_id}]: {request.method} {request.url.path}"
                )

                # 記錄請求體
                if self.log_request_body:
                    try:
                        content_length = request.headers.get("content-length")
                        if content_length and content_length.isdigit():
                            if int(content_length) > self.max_body_bytes:
                                self.logger.debug(
                                    f"API Route [{request_id}] request body: <skipped, size {content_length} bytes exceeds limit>"
                                )
                            else:
                                try:
                                    body = await request.body()
                                    if len(body) > self.max_body_bytes:
                                        body = body[: self.max_body_bytes]
                                        suffix = "... (truncated)"
                                    else:
                                        suffix = ""
                                    body_text = body.decode("utf-8")
                                    self.logger.debug(
                                        f"API Route [{request_id}] request body: {body_text}{suffix}"
                                    )
                                except UnicodeDecodeError:
                                    self.logger.debug(
                                        f"API Route [{request_id}] request body: <binary data, size: {len(body)} bytes>"
                                    )
                        else:
                            if not self.log_request_body_if_unknown_length:
                                self.logger.debug(
                                    f"API Route [{request_id}] request body: <skipped, content-length unknown>"
                                )
                            else:
                                preview, truncated = await _peek_request_body(
                                    request, self.max_body_bytes
                                )
                                try:
                                    body_text = preview.decode("utf-8")
                                    suffix = "... (truncated)" if truncated else ""
                                    self.logger.debug(
                                        f"API Route [{request_id}] request body: {body_text}{suffix}"
                                    )
                                except UnicodeDecodeError:
                                    self.logger.debug(
                                        f"API Route [{request_id}] request body: <binary data, size: {len(preview)} bytes>"
                                    )
                    except Exception as e:
                        self.logger.debug(
                            f"API Route [{request_id}] request body: <unable to read body: {type(e).__name__}>"
                        )

                # 執行原始路由處理器
                start_time = time.time()
                try:
                    response = await original_route_handler(request)
                    process_time = time.time() - start_time

                    self.logger.info(
                        f"API Route [{request_id}]: completed in {process_time:.3f}s with status {getattr(response, 'status_code', 'unknown')}"
                    )

                    # 記錄響應體
                    if self.log_response_body:
                        try:
                            body = getattr(response, "body", None)
                            if body is None:
                                self.logger.debug(
                                    f"API Route [{request_id}] response body: <streaming or not buffered>"
                                )
                            else:
                                if isinstance(body, memoryview):
                                    body = body.tobytes()
                                if isinstance(body, bytes):
                                    try:
                                        if len(body) > self.max_body_bytes:
                                            preview = body[: self.max_body_bytes]
                                            suffix = "... (truncated)"
                                        else:
                                            preview = body
                                            suffix = ""
                                        body_text = preview.decode("utf-8")
                                        self.logger.debug(
                                            f"API Route [{request_id}] response body: {body_text}{suffix}"
                                        )
                                    except UnicodeDecodeError:
                                        self.logger.debug(
                                            f"API Route [{request_id}] response body: <binary data, size: {len(body)} bytes>"
                                        )
                                else:
                                    body_text = str(body)
                                    if len(body_text.encode('utf-8')) > self.max_body_bytes:
                                        body_text = body_text.encode("utf-8")[: self.max_body_bytes].decode(
                                            "utf-8", errors="ignore"
                                        ) + "... (truncated)"
                                    self.logger.debug(
                                        f"API Route [{request_id}] response body: {body_text}"
                                    )
                        except Exception as e:
                            self.logger.debug(
                                f"API Route [{request_id}] response body: <unable to read body: {type(e).__name__}>"
                            )

                    return response
                except Exception as exc:
                    process_time = time.time() - start_time
                    self.logger.error(
                        f"API Route [{request_id}]: failed after {process_time:.3f}s - {exc.__class__.__name__}: {str(exc)}"
                    )
                    raise

            return custom_route_handler

        @staticmethod
        def _receive_factory(body: bytes):
            """創建一個能夠重複讀取請求體的函數"""

            async def receive():
                return {"type": "http.request", "body": body}

            return receive

    def get_logger_dependency(logger_instance: PrettyLogger) -> Callable[[], PrettyLogger]:
        """
        創建一個返回 logger 實例的依賴函數。

        該函數只做一件事：回傳「既有的 logger」。

        這樣可以避免在 request scope 內隱式建立/更新 logger，讓 DI 行為更可預期。

        Args:
            logger_instance: 既有的 pretty-loguru logger 實例

        Returns:
            Callable[[], PrettyLogger]: 依賴函數，返回 logger 實例

        Example::

            from fastapi import FastAPI, Depends
            from pretty_loguru.integrations.fastapi import get_logger_dependency
            from pretty_loguru import create_logger

            app = FastAPI()
            logger = create_logger("my_api", log_dir="./logs", level="INFO")
            route_logger = get_logger_dependency(logger)

            @app.get("/items/")
            async def get_items(logger: PrettyLogger = Depends(route_logger)):
                logger.info("Getting items")
                return {"items": []}
        """
        def _get_logger() -> PrettyLogger:
            return logger_instance

        return _get_logger

    def install_fastapi_middleware(
        app: FastAPI,
        *,
        logger_instance: Optional[PrettyLogger] = None,
        exclude_paths: Optional[List[str]] = None,
        exclude_methods: Optional[List[str]] = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
        log_headers: bool = True,
        sensitive_headers: Optional[Set[str]] = None,
        log_request_body_if_unknown_length: bool = False,
        max_body_bytes: int = 1000,
    ) -> PrettyLogger:
        """
        安裝 FastAPI LoggingMiddleware（較低階 building block）。

        回傳實際使用的 logger_instance，方便呼叫端串接其他安裝步驟。
        """
        if logger_instance is None:
            logger_instance = create_logger(
                name="fastapi",
                component_name="fastapi_app",
        )

        app.add_middleware(
            LoggingMiddleware,
            logger_instance=logger_instance,
            exclude_paths=exclude_paths,
            exclude_methods=exclude_methods,
            log_request_body=log_request_body,
            log_response_body=log_response_body,
            log_headers=log_headers,
            sensitive_headers=sensitive_headers,
            log_request_body_if_unknown_length=log_request_body_if_unknown_length,
            max_body_bytes=max_body_bytes,
        )
        try:
            import types
            if not hasattr(app.state, "_pretty_loguru_original_middleware_len"):
                app.state._pretty_loguru_original_middleware_len = len(app.user_middleware) - 1
        except Exception:
            pass
        logger_instance.info("FastAPI logging middleware added")
        return logger_instance

    def install_fastapi_route_class(
        app: FastAPI,
        *,
        logger_instance: Optional[PrettyLogger] = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
        log_request_body_if_unknown_length: bool = False,
        max_body_bytes: int = 1000,
    ) -> PrettyLogger:
        """
        安裝 FastAPI LoggingRoute route_class（較低階 building block）。

        回傳實際使用的 logger_instance，方便呼叫端串接其他安裝步驟。
        """
        if logger_instance is None:
            logger_instance = create_logger(
                name="fastapi",
                component_name="fastapi_app",
            )

        if not hasattr(app.state, "_pretty_loguru_original_route_class"):
            try:
                app.state._pretty_loguru_original_route_class = app.router.route_class
            except Exception:
                pass

        app.router.route_class = lambda *args, **kwargs: LoggingRoute(
            *args,
            **kwargs,
            logger_instance=logger_instance,
            log_request_body=log_request_body,
            log_response_body=log_response_body,
            log_request_body_if_unknown_length=log_request_body_if_unknown_length,
            max_body_bytes=max_body_bytes,
        )
        logger_instance.info("FastAPI custom route class has been set")
        return logger_instance

    def setup_fastapi_logging(
        app: FastAPI,
        logger_instance: Optional[PrettyLogger] = None,
        middleware: bool = True,
        custom_routes: bool = False,
        exclude_paths: Optional[List[str]] = None,
        exclude_methods: Optional[List[str]] = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
        log_headers: bool = True,
        sensitive_headers: Optional[Set[str]] = None,
        log_request_body_if_unknown_length: bool = False,
        max_body_bytes: int = 1000,
    ) -> None:
        """
        為 FastAPI 應用設置日誌功能

        此函數提供了一種便捷的方式來配置 FastAPI 應用的日誌功能。

        Args:
            app: FastAPI 應用實例
            logger_instance: 要使用的 logger 實例，如果為 None 則使用默認 logger
            middleware: 是否添加日誌中間件，預設為 True
            custom_routes: 是否使用自定義 LoggingRoute，預設為 False
            exclude_paths: 不記錄日誌的路徑列表
            exclude_methods: 不記錄日誌的 HTTP 方法列表
            log_request_body: 是否記錄請求體，預設為 False
            log_response_body: 是否記錄響應體，預設為 False
            log_headers: 是否記錄請求和響應頭，預設為 True
            sensitive_headers: 敏感頭部字段集合，這些字段的值將被遮蔽
            log_request_body_if_unknown_length: 若無 content-length 是否記錄請求體
            max_body_bytes: 記錄 body 的最大大小（bytes），預設為 1000
        """
        # 使用默認 logger 或創建新的
        if logger_instance is None:
            logger_instance = create_logger(
                name="fastapi",
                component_name="fastapi_app",
            )

        # 添加中間件
        if middleware:
            install_fastapi_middleware(
                app,
                logger_instance=logger_instance,
                exclude_paths=exclude_paths,
                exclude_methods=exclude_methods,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
                log_headers=log_headers,
                sensitive_headers=sensitive_headers,
                log_request_body_if_unknown_length=log_request_body_if_unknown_length,
                max_body_bytes=max_body_bytes,
            )

        # 設置自定義路由類
        if custom_routes:
            install_fastapi_route_class(
                app,
                logger_instance=logger_instance,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
                log_request_body_if_unknown_length=log_request_body_if_unknown_length,
                max_body_bytes=max_body_bytes,
            )


    def integrate_fastapi(
        app: FastAPI,
        logger: PrettyLogger,
        enable_uvicorn: bool = True,
        exclude_health_checks: bool = True,
        exclude_paths: Optional[List[str]] = None,
        exclude_methods: Optional[List[str]] = None,
        # 中間件配置
        middleware: bool = True,
        custom_routes: bool = False,
        log_request_body: bool = False,
        log_response_body: bool = False,
        log_headers: bool = True,
        sensitive_headers: Optional[Set[str]] = None,
        log_request_body_if_unknown_length: bool = False,
        max_body_bytes: int = 1000,
    ) -> None:
        """
        將 FastAPI 應用與 Pretty Loguru logger 進行完整集成
        
        Args:
            app: FastAPI 應用實例
            logger: 已創建的 Pretty Loguru logger 實例
            enable_uvicorn: 是否同時配置 uvicorn 日誌，默認為 True
            exclude_health_checks: 是否排除健康檢查路徑，默認為 True
            exclude_paths: 額外排除的路徑列表
            exclude_methods: 排除的 HTTP 方法列表
            middleware: 是否添加日誌中間件，預設為 True
            custom_routes: 是否使用自定義 LoggingRoute，預設為 False
            log_request_body: 是否記錄請求體，預設為 False
            log_response_body: 是否記錄響應體，預設為 False
            log_headers: 是否記錄請求和響應頭，預設為 True
            sensitive_headers: 敏感頭部字段集合，這些字段的值將被遮蔽
            log_request_body_if_unknown_length: 若無 content-length 是否記錄請求體
            max_body_bytes: 記錄 body 的最大大小（bytes），預設為 1000
        
        Example:
            from fastapi import FastAPI
            from pretty_loguru import create_logger
            from pretty_loguru.integrations.fastapi import integrate_fastapi
            
            app = FastAPI()
            logger = create_logger("my_api", log_dir="./logs")
            integrate_fastapi(
                app,
                logger,
                log_request_body=True,  # 記錄請求體
                log_headers=True        # 記錄頭部資訊
            )
            
            @app.get("/")
            async def root():
                logger.info("處理首頁請求")
                return {"message": "Hello World"}
        """
        # 設置排除路徑
        final_exclude_paths = exclude_paths or []
        if exclude_health_checks:
            default_exclude = ["/health", "/metrics", "/docs", "/openapi.json", "/redoc"]
            final_exclude_paths.extend(default_exclude)
        
        # 設置排除方法
        final_exclude_methods = exclude_methods or ["OPTIONS"]
        
        # 設置 FastAPI 日誌（可組裝）
        if middleware:
            install_fastapi_middleware(
                app,
                logger_instance=logger,
                exclude_paths=final_exclude_paths,
                exclude_methods=final_exclude_methods,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
                log_headers=log_headers,
                sensitive_headers=sensitive_headers,
                log_request_body_if_unknown_length=log_request_body_if_unknown_length,
                max_body_bytes=max_body_bytes,
            )

        if custom_routes:
            install_fastapi_route_class(
                app,
                logger_instance=logger,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
                log_request_body_if_unknown_length=log_request_body_if_unknown_length,
                max_body_bytes=max_body_bytes,
            )
        
        # 配置 uvicorn 日誌（如果啟用）
        if enable_uvicorn:
            try:
                from .uvicorn import integrate_uvicorn
                integrate_uvicorn(logger, monkeypatch=True)
            except ImportError:
                logger.warning("Uvicorn not available, skipping uvicorn logging setup")


    def build_fastapi_logging_options(
        logger_instance: Optional[PrettyLogger] = None,
        *,
        exclude_paths: Optional[List[str]] = None,
        exclude_methods: Optional[List[str]] = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
        log_headers: bool = True,
        sensitive_headers: Optional[Set[str]] = None,
        log_request_body_if_unknown_length: bool = False,
        max_body_bytes: int = 1000,
    ) -> Dict[str, Any]:
        """
        提供 FastAPI 日誌中間件與 route_class 的「非直接安裝」選項。

        回傳的內容可以讓呼叫端自行決定是否套用，避免直接改寫 app。
        """
        if logger_instance is None:
            logger_instance = create_logger(
                name="fastapi",
                component_name="fastapi_app",
            )

        return {
            "middleware_class": LoggingMiddleware,
            "middleware_kwargs": {
                "logger_instance": logger_instance,
                "exclude_paths": exclude_paths or [],
                "exclude_methods": exclude_methods or ["OPTIONS"],
                "log_request_body": log_request_body,
                "log_response_body": log_response_body,
                "log_headers": log_headers,
                "sensitive_headers": sensitive_headers,
                "log_request_body_if_unknown_length": log_request_body_if_unknown_length,
                "max_body_bytes": max_body_bytes,
            },
            "route_class_factory": lambda *args, **kwargs: LoggingRoute(
                *args,
                **kwargs,
                logger_instance=logger_instance,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
                log_request_body_if_unknown_length=log_request_body_if_unknown_length,
                max_body_bytes=max_body_bytes,
            ),
        }

    def restore_fastapi_logging(app: FastAPI) -> None:
        """
        嘗試還原 integrate_fastapi/setup_fastapi_logging 對 app 的變更。

        備註：middleware 刪除 FastAPI 未提供原生 API，這裡僅還原 route_class，並記錄提示。
        """
        try:
            if hasattr(app.state, "_pretty_loguru_original_route_class"):
                app.router.route_class = app.state._pretty_loguru_original_route_class
            # middleware 無法安全移除，留訊息讓使用者知悉
            if hasattr(app.state, "_pretty_loguru_original_middleware_len"):
                expected = getattr(app.state, "_pretty_loguru_original_middleware_len")
                if len(app.user_middleware) > expected:
                    warnings.warn("FastAPI middleware added by pretty-loguru cannot be auto-removed; recreate app to fully restore.", UserWarning)
        except Exception:
            warnings.warn("Failed to restore FastAPI logging state.", UserWarning)


if not _has_fastapi:

    def _require_fastapi() -> None:
        """當 `fastapi` 未安裝時，統一拋出缺少依賴的錯誤。"""
        warnings.warn("fastapi not installed; FastAPI integration stubs will raise missing_dependency.", ImportWarning)
        raise missing_dependency("fastapi", extra="integrations")

    def setup_fastapi_logging(*args: Any, **kwargs: Any) -> None:  # type: ignore[name-defined]
        """`setup_fastapi_logging` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        _require_fastapi()

    def integrate_fastapi(*args: Any, **kwargs: Any) -> None:  # type: ignore[name-defined]
        """`integrate_fastapi` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        _require_fastapi()

    def get_logger_dependency(*args: Any, **kwargs: Any) -> Any:  # type: ignore[name-defined]
        """`get_logger_dependency` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        _require_fastapi()

    def install_fastapi_middleware(*args: Any, **kwargs: Any) -> Any:  # type: ignore[name-defined]
        """`install_fastapi_middleware` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        _require_fastapi()

    def install_fastapi_route_class(*args: Any, **kwargs: Any) -> Any:  # type: ignore[name-defined]
        """`install_fastapi_route_class` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        _require_fastapi()

    def build_fastapi_logging_options(*args: Any, **kwargs: Any) -> Any:  # type: ignore[name-defined]
        """`build_fastapi_logging_options` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        _require_fastapi()

    class LoggingMiddleware:  # type: ignore[name-defined]
        """`LoggingMiddleware` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """建立 stub；任何呼叫都會拋出缺少依賴錯誤。"""
            _require_fastapi()

    class LoggingRoute:  # type: ignore[name-defined]
        """`LoggingRoute` 的 stub（缺少 `fastapi` 時會拋錯）。"""
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """建立 stub；任何呼叫都會拋出缺少依賴錯誤。"""
            _require_fastapi()
        
