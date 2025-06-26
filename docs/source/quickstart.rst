快速入門
============

本節將幫助你快速上手 Pretty Loguru。

安裝
------

使用 pip 安裝 Pretty Loguru：

.. code-block:: bash

   pip install pretty-loguru

可選依賴：

.. code-block:: bash

   # 安裝 ASCII 藝術支持
   pip install art
   
   # 安裝 FIGlet 藝術支持
   pip install pyfiglet
   
   # 安裝 YAML 配置支持
   pip install pyyaml

創建日誌實例
------------------


.. code-block:: python

   from pretty_loguru import create_logger
   
   # 創建一個基本日誌實例
   logger = create_logger("my_app")
   
   # 基本日誌記錄
   logger.info("這是一條資訊日誌")
   logger.warning("這是一條警告日誌")
   logger.error("這是一條錯誤日誌")

使用區塊日誌
------------------


.. code-block:: python

   # 使用區塊功能記錄結構化日誌
   logger.block(
       "系統啟動",
       [
           "開始初始化應用程序...",
           "已載入配置文件",
           "啟動完成"
       ]
   )

.. locale-image:: block_example.png
   :alt: 區塊日誌示例
   :width: 500px

目標導向日誌
------------------


.. code-block:: python

   # 僅輸出到控制台
   logger.console_info("這條日誌只會顯示在控制台")
   
   # 僅輸出到文件
   logger.file_info("這條日誌只會寫入文件")
   
   # 開發模式（控制台別名）
   logger.dev_info("開發調試信息")

ASCII 和 FIGlet 藝術
---------------------------------------------------


.. code-block:: python

   # ASCII 藝術標題 (需要安裝 art 庫)
   logger.ascii_header("System start")
   
   # FIGlet 藝術標題 (需要安裝 pyfiglet 庫)
   logger.figlet_header("Warning", font="slant")

.. locale-image:: figlet_example.png
   :alt: FIGlet 藝術示例
   :width: 500px


框架集成
------------

與 FastAPI 集成：

.. code-block:: python

   from fastapi import FastAPI
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.fastapi import setup_fastapi_logging
   
   
   app = FastAPI()
   logger = create_logger("fastapi_app")
   setup_fastapi_logging(app, logger_instance=logger)

   @app.get("/")
   def read_root():
      logger.info("處理首頁請求")
      return {"Hello": "World"}

   if __name__ == "__main__":
      import uvicorn
      uvicorn.run(
         app,
         host="localhost",
         port=8000,
      )


.. locale-image:: fastAPI_example.png
   :alt: FastAPI 集成示例
   :width: 500px


與 Uvicorn 集成：

.. code-block:: python

   from fastapi import FastAPI
   from pretty_loguru import create_logger
   from pretty_loguru.integrations.uvicorn import configure_uvicorn

   app = FastAPI()
   logger = create_logger("app")

   if __name__ == "__main__":
      import uvicorn
      # 先設定好 Loguru 攔截
      configure_uvicorn(logger_instance=logger)
      # 關閉 Uvicorn 內建的 log_config
      uvicorn.run(
         app,
         host="localhost",
         port=8000,
         log_config=None,     # ← 這行關鍵
      )

.. locale-image:: uvicorn_example.png
   :alt: FastAPI 集成示例
   :width: 500px

自定義配置
---------------

.. code-block:: python

   # 自定義配置
   logger = create_logger(
       name="custom_app",
       service_tag="payment_service",
       level="DEBUG",
       log_path="/var/log/myapp",
       rotation="20 MB",
       subdirectory="payments",
       log_name_preset="daily"
   )
   
   # 使用自定義格式
   custom_format = (
       "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
       "<level>{level: <8}</level> | "
       "<cyan>{name}</cyan> - <level>{message}</level>"
   )
   
   formatted_logger = create_logger(
       name="formatted_app",
       logger_format=custom_format
   )

日誌清理
------------

自動清理舊日誌文件：

.. code-block:: python

   from pretty_loguru.core.cleaner import LoggerCleaner
   
   # 創建清理器
   cleaner = LoggerCleaner(
       log_retention=30,      # 保留30天的日誌
       log_path="/var/log/myapp",
       check_interval=3600,   # 每小時檢查一次
       logger_instance=logger
   )
   
   # 啟動清理器
   cleaner.start()

更多功能
------------

Pretty Loguru 還提供了更多功能，請繼續閱讀以下章節了解更多詳情：

- :doc:`basic_usage` -` 基本用法和主要功能`
- :doc:`advanced_features` -` 進階功能和特性`
- :doc:`integrations` -` 框架集成功能`

更多示例
------------

查看 :doc:`advanced_features` 獲取更多使用示例。`