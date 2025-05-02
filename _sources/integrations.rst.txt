框架集成
============

Pretty Loguru 設計為能夠與流行的 Python 框架無縫集成。本節介紹如何將 Pretty Loguru 集成到不同的框架中。

FastAPI 集成
------------------------------

Pretty Loguru 提供了與 FastAPI 的完整集成，包括請求日誌、依賴注入和錯誤處理。

基本設置
^^^^^^^^^^^^

.. code-block:: python

   from fastapi import FastAPI, Depends
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.fastapi import setup_fastapi_logging, get_logger_dependency
   
   # 創建 FastAPI 應用
   app = FastAPI()
   
   # 創建日誌實例
   logger = create_logger("fastapi_app")
   
   # 設置 FastAPI 日誌
   setup_fastapi_logging(
       app,
       logger_instance=logger,
       middleware=True,
       custom_routes=True,
       log_request_body=True,
       log_response_body=False
   )
   
   # 基本路由
   @app.get("/")
   async def root():
       logger.info("處理首頁請求")
       return {"message": "Hello World"}

依賴注入
^^^^^^^^^^^^

使用 ``get_logger_dependency`` 函數可以為每個路由提供專用的日誌實例：`

.. code-block:: python

   # 創建路由特定的日誌依賴
   users_logger = get_logger_dependency(name="users_api")
   
   @app.get("/users/")
   async def get_users(logger=Depends(users_logger)):
       logger.info("獲取用戶列表")
       return {"users": ["user1", "user2"]}
   
   # 另一個範例
   items_logger = get_logger_dependency(name="items_api", service_tag="inventory")
   
   @app.get("/items/")
   async def get_items(logger=Depends(items_logger)):
       logger.info("獲取商品列表")
       return {"items": ["item1", "item2"]}

日誌中間件
^^^^^^^^^^^^^^^

當使用 ``setup_fastapi_logging`` 設置中間件時，它將自動記錄所有請求和響應的詳細信息：`

.. code-block:: python

   # 自定義中間件設置
   setup_fastapi_logging(
       app,
       logger_instance=logger,
       exclude_paths=["/health", "/metrics"],  # 排除某些路徑不記錄日誌
       exclude_methods=["OPTIONS"],            # 排除某些 HTTP 方法
       log_request_body=True,                  # 記錄請求體
       log_response_body=True,                 # 記錄響應體
   )

輸出範例：

.. code-block:: text

   2023-05-01 12:34:56 | INFO | Request [1682938496.123]: GET /users/ from 127.0.0.1:56789
   2023-05-01 12:34:56 | INFO | Response [1682938496.123]: 200 in 0.015s

自定義路由
^^^^^^^^^^^^^^^

使用 ``custom_routes=True`` 參數可啟用更詳細的路由級別日誌記錄：`

.. code-block:: python
   
   # 啟用自定義路由
   setup_fastapi_logging(
       app,
       logger_instance=logger,
       custom_routes=True,
       log_request_body=True,
   )

Uvicorn 集成
------------------------------

Pretty Loguru 可以接管 Uvicorn 的日誌系統，使所有日誌使用相同的格式和處理方式。

基本設置
^^^^^^^^^^^^

.. code-block:: python

   import uvicorn
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.uvicorn import configure_uvicorn
   
   # 創建日誌實例
   logger = create_logger("uvicorn_app")
   
   # 配置 Uvicorn 使用 Pretty Loguru
   configure_uvicorn(logger_instance=logger, level="INFO")
   
   # 啟動 Uvicorn
   if __name__ == "__main__":
       uvicorn.run("app:app", host="0.0.0.0", port=8000)

攔截處理器
^^^^^^^^^^^^^^^

``InterceptHandler`` 類用於攔截標準庫的日誌並轉發給` Loguru：`

.. code-block:: python

   import logging
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.uvicorn import InterceptHandler
   
   # 創建日誌實例
   logger = create_logger("my_app")
   
   # 設置攔截處理器
   logging.basicConfig(handlers=[InterceptHandler(logger_instance=logger)], level=0)
   
   # 從此以後，所有透過標準庫的日誌都會被轉發給 Loguru
   logging.info("這條日誌會被 Loguru 處理")

集成到其他 ASGI 服務器
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

與其他 ASGI 服務器的集成方法相似：

.. code-block:: python

   from pretty_loguru import create_logger
   from pretty_loguru.integrations.uvicorn import configure_uvicorn
   
   # 創建日誌實例
   logger = create_logger("asgi_app")
   
   # 配置日誌
   configure_uvicorn(
       logger_instance=logger,
       level="INFO",
       logger_names=["uvicorn.asgi", "uvicorn.access", "hypercorn", "daphne"]
   )

與其他庫集成
------------------

Pretty Loguru 可以與任何使用標準日誌庫的工具集成：

SQLAlchemy 範例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import logging
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.uvicorn import InterceptHandler
   
   # 創建日誌實例
   logger = create_logger("sqlalchemy_app")
   
   # 設置 SQLAlchemy 日誌
   sql_logger = logging.getLogger("sqlalchemy.engine")
   sql_logger.setLevel(logging.INFO)
   sql_logger.addHandler(InterceptHandler(logger_instance=logger))
   
   # 現在 SQLAlchemy 的日誌將使用 Pretty Loguru 格式

Django 範例
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # settings.py
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'loguru': {
               'class': 'pretty_loguru.integrations.uvicorn.InterceptHandler',
           },
       },
       'root': {
           'handlers': ['loguru'],
           'level': 'INFO',
       },
   }

Flask 範例
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from flask import Flask
   import logging
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.uvicorn import InterceptHandler
   
   app = Flask(__name__)
   
   # 創建日誌實例
   logger = create_logger("flask_app")
   
   # 配置 Flask 日誌
   app.logger.handlers = [InterceptHandler(logger_instance=logger)]
   app.logger.setLevel(logging.INFO)
   
   # 路由範例
   @app.route('/')
   def hello():
       app.logger.info("處理首頁請求")
       return "Hello World!"