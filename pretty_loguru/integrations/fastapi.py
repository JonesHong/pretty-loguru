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

from ..types import EnhancedLogger, LogLevelType, LogRotationType, LogPathType
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
                    except UnicodeDecodeError:
                        # 如果無法解碼為文本，則記錄大小
                        self.logger.debug(
                            f"Request [{request_id}] body: <binary data, size: {len(body)} bytes>"
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
                        except UnicodeDecodeError:
                            self.logger.debug(
                                f"Response [{request_id}] body: <binary data, size: {len(body)} bytes>"
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
                        except UnicodeDecodeError:
                            self.logger.debug(
                                f"API Route [{request_id}] request body: <binary data, size: {len(body)} bytes>"
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
                            body = getattr(response, "body", b"")
                            try:
                                body_text = body.decode("utf-8")
                                if len(body_text) > 1000:
                                    body_text = body_text[:1000] + "... (truncated)"
                                self.logger.debug(
                                    f"API Route [{request_id}] response body: {body_text}"
                                )
                            except UnicodeDecodeError:
                                self.logger.debug(
                                    f"API Route [{request_id}] response body: <binary data, size: {len(body)} bytes>"
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

    def get_logger_dependency(
        name: Optional[str] = None,
        service_tag: Optional[str] = None,
        # 檔案輸出配置
        log_path: Optional[LogPathType] = None,
        rotation: Optional[LogRotationType] = None,
        retention: Optional[str] = None,
        compression: Optional[Union[str, Callable]] = None,
        compression_format: Optional[str] = None,
        # 格式化配置
        level: Optional[LogLevelType] = None,
        logger_format: Optional[str] = None,
        component_name: Optional[str] = None,
        subdirectory: Optional[str] = None,
        # 行為控制
        start_cleaner: Optional[bool] = None,
        use_native_format: bool = False,
        # 預設配置
        preset: Optional[str] = None
    ) -> Callable[[], EnhancedLogger]:
        """
        創建一個返回 logger 實例的依賴函數。

        該函數可用於在 FastAPI 路由中注入 logger 實例。

        Args:
            name: logger 實例的名稱，如果為 None 則使用路由路徑
            service_tag: 服務名稱 (已廢棄，使用 component_name 替代)
            log_path: 日誌檔案輸出路徑
            rotation: 日誌輪轉設定
            retention: 日誌保留設定
            compression: 壓縮設定
            compression_format: 壓縮格式
            level: 日誌等級
            logger_format: 自定義日誌格式字符串
            component_name: 組件名稱
            subdirectory: 子目錄
            start_cleaner: 是否啟動自動清理器
            use_native_format: 是否使用 loguru 原生格式
            preset: 預設配置名稱

        Returns:
            Callable[[], EnhancedLogger]: 依賴函數，返回 logger 實例

        Example::

            from fastapi import FastAPI, Depends
            from pretty_loguru.integrations.fastapi import get_logger_dependency

            app = FastAPI()
            route_logger = get_logger_dependency(
                name="my_api",
                log_path="./logs",
                level="INFO"
            )

            @app.get("/items/")
            async def get_items(logger: EnhancedLogger = Depends(route_logger)):
                logger.info("Getting items")
                return {"items": []}
        """
        def get_logger() -> EnhancedLogger:
            # 處理向後兼容的 service_tag 參數
            final_component_name = component_name or service_tag
            
            return create_logger(
                name=name,
                use_native_format=use_native_format,
                log_path=log_path,
                rotation=rotation,
                retention=retention,
                compression=compression,
                compression_format=compression_format,
                level=level,
                logger_format=logger_format,
                component_name=final_component_name,
                subdirectory=subdirectory,
                start_cleaner=start_cleaner,
                preset=preset
            )

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
        log_headers: bool = True,
        sensitive_headers: Optional[Set[str]] = None,
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
                log_headers=log_headers,
                sensitive_headers=sensitive_headers,
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


    def integrate_fastapi(
        app: FastAPI,
        logger: EnhancedLogger,
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
        sensitive_headers: Optional[Set[str]] = None
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
        
        Example:
            from fastapi import FastAPI
            from pretty_loguru import create_logger
            from pretty_loguru.integrations.fastapi import integrate_fastapi
            
            app = FastAPI()
            logger = create_logger("my_api", log_path="./logs")
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
        
        # 設置 FastAPI 日誌
        setup_fastapi_logging(
            app=app,
            logger_instance=logger,
            middleware=middleware,
            custom_routes=custom_routes,
            exclude_paths=final_exclude_paths,
            exclude_methods=final_exclude_methods,
            log_request_body=log_request_body,
            log_response_body=log_response_body,
            log_headers=log_headers,
            sensitive_headers=sensitive_headers
        )
        
        # 配置 uvicorn 日誌（如果啟用）
        if enable_uvicorn:
            try:
                from .uvicorn import integrate_uvicorn
                integrate_uvicorn(logger)
            except ImportError:
                logger.warning("Uvicorn not available, skipping uvicorn logging setup")
        
