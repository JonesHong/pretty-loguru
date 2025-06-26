"""
FastAPI 整合模組

此模組提供與 FastAPI 框架的整合功能，包括請求日誌中間件、
依賴注入和異常處理器，使 FastAPI 應用能夠充分利用 Pretty Loguru。
"""

import time
from typing import Callable, Optional, Dict, Any, Union, List, Set
import typing
import warnings

try:
    from fastapi import FastAPI, Request, Response, Depends
    from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
    from fastapi.routing import APIRoute

    _has_fastapi = True
except ImportError:
    _has_fastapi = False
    warnings.warn(
        "The 'fastapi' package is not installed. FastAPI integration will not be available. You can install it using 'pip install fastapi'.",
        ImportWarning,
        stacklevel=2,
    )

from ..types import EnhancedLogger
from ..factory.creator import create_logger, default_logger


if _has_fastapi:

    class LoggingMiddleware(BaseHTTPMiddleware):
        """
        FastAPI 日誌中間件，記錄請求和響應的詳細信息
        """

        def __init__(
            self,
            app: FastAPI,
            logger_instance: Optional[EnhancedLogger] = None,
            exclude_paths: Optional[List[str]] = None,
            exclude_methods: Optional[List[str]] = None,
            log_request_body: bool = False,
            log_response_body: bool = False,
            log_headers: bool = True,
            sensitive_headers: Optional[Set[str]] = None,
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
            """
            super().__init__(app)
            # 使用函數調用而不是直接引用，確保延遲初始化
            self.logger = logger_instance or default_logger()
            self.exclude_paths = exclude_paths or []
            self.exclude_methods = [m.upper() for m in (exclude_methods or [])]
            self.log_request_body = log_request_body
            self.log_response_body = log_response_body
            self.log_headers = log_headers
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
                    # 僅讀取內容而不消耗流
                    body = await request.body()
                    try:
                        # 嘗試解碼為文本
                        body_text = body.decode("utf-8")
                        # 如果內容太長，則截斷
                        if len(body_text) > 1000:
                            body_text = body_text[:1000] + "... (truncated)"
                        self.logger.debug(f"Request [{request_id}] body: {body_text}")
                    except:
                        # 如果無法解碼為文本，則記錄大小
                        self.logger.debug(
                            f"Request [{request_id}] body: <binary data, size: {len(body)} bytes>"
                        )
                except:
                    self.logger.debug(
                        f"Request [{request_id}] body: <unable to read body>"
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
                    # 需要使用特殊技術來讀取響應體而不影響發送給客戶端
                    # 在實際應用中可能需要更複雜的實現
                    # 這裡僅作為示例
                    try:
                        body = b""
                        for chunk in response.body_iterator:
                            body += chunk
                        response.body_iterator = [body]

                        try:
                            body_text = body.decode("utf-8")
                            if len(body_text) > 1000:
                                body_text = body_text[:1000] + "... (truncated)"
                            self.logger.debug(
                                f"Response [{request_id}] body: {body_text}"
                            )
                        except:
                            self.logger.debug(
                                f"Response [{request_id}] body: <binary data, size: {len(body)} bytes>"
                            )
                    except:
                        self.logger.debug(
                            f"Response [{request_id}] body: <unable to read body>"
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
            logger_instance: Optional[EnhancedLogger] = None,
            log_request_body: bool = False,
            log_response_body: bool = False,
            **kwargs: Any,
        ):
            # 使用函數調用而不是直接引用，確保延遲初始化
            self.logger = logger_instance or default_logger()
            self.log_request_body = log_request_body
            self.log_response_body = log_response_body
            super().__init__(*args, **kwargs)

        def get_route_handler(self) -> Callable:
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
                        body = await request.body()
                        request._receive = self._receive_factory(body)
                        try:
                            body_text = body.decode("utf-8")
                            if len(body_text) > 1000:
                                body_text = body_text[:1000] + "... (truncated)"
                            self.logger.debug(
                                f"API Route [{request_id}] request body: {body_text}"
                            )
                        except:
                            self.logger.debug(
                                f"API Route [{request_id}] request body: <binary data, size: {len(body)} bytes>"
                            )
                    except:
                        self.logger.debug(
                            f"API Route [{request_id}] request body: <unable to read body>"
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
                            body = getattr(response, "body", b"")
                            try:
                                body_text = body.decode("utf-8")
                                if len(body_text) > 1000:
                                    body_text = body_text[:1000] + "... (truncated)"
                                self.logger.debug(
                                    f"API Route [{request_id}] response body: {body_text}"
                                )
                            except:
                                self.logger.debug(
                                    f"API Route [{request_id}] response body: <binary data, size: {len(body)} bytes>"
                                )
                        except:
                            self.logger.debug(
                                f"API Route [{request_id}] response body: <unable to read body>"
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

    def get_logger_dependency(
        name: Optional[str] = None, service_tag: Optional[str] = None, **kwargs: Any
    ) -> Callable[[], EnhancedLogger]:
        """
        創建一個返回 logger 實例的依賴函數。

        該函數可用於在 FastAPI 路由中注入 logger 實例。

        :param name: logger 實例的名稱，如果為 None 則使用路由路徑
        :param service_tag: 服務名稱
        :param kwargs: 傳遞給 create_logger 的其他參數
        :return: Callable[[], EnhancedLogger] 依賴函數，返回 logger 實例

        Example::

            from fastapi import FastAPI, Depends
            from pretty_loguru.integrations.fastapi import get_logger_dependency

            app = FastAPI()
            route_logger = get_logger_dependency(name="my_api")

            @app.get("/items/")
            async def get_items(logger: EnhancedLogger = Depends(route_logger)):
                logger.info("Getting items")
                return {"items": []}
        """


        def get_logger() -> EnhancedLogger:
            return create_logger(name=name, service_tag=service_tag, **kwargs)

        return get_logger

    def setup_fastapi_logging(
        app: FastAPI,
        logger_instance: Optional[EnhancedLogger] = None,
        middleware: bool = True,
        custom_routes: bool = False,
        exclude_paths: Optional[List[str]] = None,
        exclude_methods: Optional[List[str]] = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
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
        """
        # 使用默認 logger 或創建新的
        if logger_instance is None:
            logger_instance = create_logger(
                name="fastapi", service_tag="fastapi_app", reuse_existing=True
            )

        # 添加中間件
        if middleware:
            app.add_middleware(
                LoggingMiddleware,
                logger_instance=logger_instance,
                exclude_paths=exclude_paths,
                exclude_methods=exclude_methods,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
            )
            logger_instance.info("FastAPI logging middleware added")

        # 設置自定義路由類
        if custom_routes:
            app.router.route_class = lambda *args, **kwargs: LoggingRoute(
                *args,
                **kwargs,
                logger_instance=logger_instance,
                log_request_body=log_request_body,
                log_response_body=log_response_body,
            )
            logger_instance.info("FastAPI custom route class has been set")
