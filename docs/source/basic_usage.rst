基本用法
============

本節介紹 Pretty Loguru 的基本用法和主要功能。

創建和配置日誌實例
---------------------------

使用 ``create_logger`` 函數可以快速創建一個日誌實例：`

.. code-block:: python

   from pretty_loguru import create_logger
   
   # 基本創建
   logger = create_logger("app_name")
   
   # 使用自定義配置
   custom_logger = create_logger(
       name="custom_app",
       service_tag="payment_service",
       level="DEBUG",
       log_path="/var/log/myapp",
       rotation="20 MB",
       subdirectory="payments"
   )

日誌級別
------------

Pretty Loguru 支持以下日誌級別：

- ``TRACE`` -` 最詳細的輸出，用於追蹤程序執行過程`
- ``DEBUG`` -` 調試信息，幫助開發者進行問題診斷`
- ``INFO`` -` 一般信息，記錄應用程序的正常操作`
- ``SUCCESS`` -` 成功完成的操作`
- ``WARNING`` -` 警告信息，可能的問題或異常情況`
- ``ERROR`` -` 錯誤信息，應用程序運行中的失敗`
- ``CRITICAL`` -` 嚴重錯誤，可能導致應用程序無法繼續運行`

.. code-block:: python

   logger.trace("這是追蹤信息")
   logger.debug("這是調試信息")
   logger.info("這是一般信息")
   logger.success("操作成功！")
   logger.warning("這是警告信息")
   logger.error("這是錯誤信息")
   logger.critical("這是嚴重錯誤")

目標導向日誌
------------------

Pretty Loguru 允許指定日誌的輸出目標：

.. code-block:: python

   # 僅輸出到控制台
   logger.console_info("這條信息只會顯示在控制台")
   
   # 僅寫入日誌文件
   logger.file_info("這條信息只會寫入日誌文件")
   
   # 開發模式日誌（控制台別名）
   logger.dev_info("開發模式日誌，僅控制台顯示")

區塊日誌
------------

區塊日誌功能可以以結構化方式呈現相關信息：

.. code-block:: python

   logger.block(
       "資料庫操作摘要",
       [
           "連接成功：PostgreSQL 13.4",
           "執行查詢：SELECT * FROM users",
           "返回記錄數：42",
           "關閉連接"
       ],
       border_style="green",
       log_level="INFO"
   )
   
   # 僅輸出到控制台的區塊
   logger.console_block(
       "控制台區塊示例",
       ["這個區塊只會顯示在控制台"]
   )

捕獲異常
------------

使用 ``try-except`` 記錄異常：`

.. code-block:: python

   try:
       # 可能會拋出異常的代碼
       result = 1 / 0
   except Exception as e:
       logger.exception(f"操作失敗：{str(e)}")
       
   # 或使用 logger.catch 裝飾器
   @logger.catch
   def risky_function():
       return 1 / 0
       
   risky_function()  # 異常會被自動捕獲並記錄

日誌文件管理
------------------

Pretty Loguru 會自動處理日誌文件的創建和輪換：

.. code-block:: python

   # 設置20MB的輪換大小
   logger = create_logger(
       name="rotating_logs",
       rotation="20 MB"
   )
   
   # 使用預定義的日誌檔案名格式
   logger = create_logger(
       name="daily_logs",
       log_name_preset="daily"  # 使用每日輪換格式
   )

日誌內容格式化
---------------------

格式化日誌消息：

.. code-block:: python

   # 使用字符串格式化
   username = "admin"
   logger.info(f"用戶 {username} 登入系統")
   
   # 使用參數（性能更好）
   logger.info("用戶 {} 登入系統", username)
   
   # 使用關鍵字參數
   logger.info("用戶 {name} 執行了 {action}", name="admin", action="數據備份")

結構化日誌
---------------

綁定上下文變量：

.. code-block:: python

   # 創建帶有上下文的 logger
   request_logger = logger.bind(request_id="abc123")
   request_logger.info("處理請求")  # 會包含 request_id
   
   # 臨時上下文
   with logger.contextualize(user_id="user456"):
       logger.info("用戶操作")  # 會包含 user_id