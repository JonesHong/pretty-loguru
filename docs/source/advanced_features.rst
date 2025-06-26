進階功能
============

本節介紹 Pretty Loguru 的進階功能和特性。

ASCII 藝術標題
------------------------------

使用 ASCII 藝術標題增強你的日誌視覺效果：

.. code-block:: python

   # 需要安裝 art 庫：pip install art
    logger.ascii_header("System Startup", font="standard")
   
   # 帶有 ASCII 標題的區塊
   logger.ascii_block(
    "Scheduled Task",
       [
           "開始執行每日計劃任務...",
           "數據備份完成",
           "用戶統計報告已生成"
       ],
       ascii_font="standard"
   )


FIGlet 藝術標題
---------------------------------

使用 FIGlet 藝術標題提供更多字體選擇：

.. code-block:: python

   # 需要安裝 pyfiglet 庫：pip install pyfiglet
    logger.figlet_header("Warning Message", font="slant")
   
   # 獲取所有可用的 FIGlet 字體
   available_fonts = logger.get_figlet_fonts()
   print(f"可用字體數量: {len(available_fonts)}")
   
   # 帶有 FIGlet 標題的區塊
   logger.figlet_block(
    "Exception Summary",
       [
           "檢測到系統異常",
           "服務中斷時間：14:30-15:45",
           "影響用戶數：1,234"
       ],
       figlet_font="banner"
   )

日誌清理
------------

自動清理過期的日誌文件，避免磁碟空間浪費：

.. code-block:: python

   from pretty_loguru import create_logger
   from pretty_loguru.core.cleaner import LoggerCleaner
   
   # 創建日誌實例
   logger = create_logger("my_app")
   
   # 創建並啟動日誌清理器（保留30天的日誌）
   cleaner = LoggerCleaner(
       log_retention=30,  # 保留30天
       log_path="/var/log/myapp",
       check_interval=3600,  # 每小時檢查一次
       logger_instance=logger
   )
   
   # 啟動清理器
   cleaner.start()

自定義格式化
------------------

完全自定義日誌格式和排版：

.. code-block:: python

   from pretty_loguru import create_logger
   
   # 自定義日誌格式
   custom_format = (
       "<blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</blue> | "
       "<level>{level: <8}</level> | "
       "<cyan>{name}</cyan>:<green>{function}</green>:<yellow>{line}</yellow> - "
       "<level>{message}</level>"
   )
   
   # 創建使用自定義格式的日誌實例
   logger = create_logger(
       name="custom_format_app",
       logger_format=custom_format
   )
   
   logger.info("使用自定義格式的日誌")

管理多個日誌實例
------------------------

Pretty Loguru 讓你可以輕鬆管理多個日誌實例：

.. code-block:: python

   from pretty_loguru import create_logger, get_logger, list_loggers, unregister_logger
   
   # 創建多個日誌實例
   api_logger = create_logger("api")
   db_logger = create_logger("db")
   worker_logger = create_logger("worker")
   
   # 獲取已註冊的日誌實例
   loggers = list_loggers()
   print(f"已註冊的日誌實例: {loggers}")  # ['api', 'db', 'worker']
   
   # 按名稱獲取日誌實例
   logger = get_logger("api")
   logger.info("從註冊表獲取的日誌實例")
   
   # 取消註冊日誌實例
   unregister_logger("worker")

配置從文件或環境變數載入
------------------------------------

從配置文件或環境變數載入設置：

.. code-block:: python

   from pretty_loguru import LoggerConfig, create_logger
   
   # 從 JSON 文件載入配置
   config = LoggerConfig.from_file("config.json", format="json")
   
   # 從 YAML 文件載入配置 (需要 PyYAML)
   config = LoggerConfig.from_file("config.yaml", format="yaml")
   
   # 使用配置創建日誌實例
   logger = create_logger(
       name="configured_app",
       level=config.level,
       rotation=config.rotation,
       log_path=config.log_path,
       logger_format=config.format
   )

使用環境變數：

.. code-block:: bash

   # 設置環境變數
   export PRETTY_LOGURU_LEVEL=DEBUG
   export PRETTY_LOGURU_PATH=/var/log/myapp
   export PRETTY_LOGURU_ROTATION=50MB

.. code-block:: python

   # 環境變數會自動生效
   from pretty_loguru import create_logger
   
   logger = create_logger("env_configured_app")
   # 會使用環境變數中的設置

自定義處理器
------------------

添加自定義輸出目標：

.. code-block:: python

   from pretty_loguru import create_logger
   import logging
   import sys
   
   # 創建日誌實例
   logger = create_logger("custom_handlers")
   
   # 添加標準輸出處理器
   stdout_handler_id = logger.add(
       sys.stdout,
       format="{time} | {level} | {message}",
       level="INFO",
       colorize=True
   )
   
   # 添加自定義檔案處理器
   file_handler_id = logger.add(
       "special.log",
       format="{time:YYYY-MM-DD} | {level} | {message}",
       level="WARNING",
       rotation="1 week"
   )
   
   # 添加自定義處理器函數
   def my_sink(message):
       # 自定義處理日誌消息
       print(f"自定義處理: {message}")
   
   custom_handler_id = logger.add(my_sink, level="ERROR")
   
   # 使用日誌
   logger.info("普通信息")  # 輸出到標準輸出
   logger.warning("警告信息")  # 輸出到標準輸出和文件
   logger.error("錯誤信息")  # 輸出到所有處理器
   
   # 移除處理器
   logger.remove(custom_handler_id)

性能優化
------------

對於高性能需求，可以使用以下技巧：

.. code-block:: python

   # 1. 使用懶惰格式化
   for i in range(1000000):
       # 不建議: 即使日誌級別不符合也會進行格式化
       logger.debug(f"循環迭代: {i}, 複雜計算: {expensive_function(i)}")
       
       # 建議: 使用 % 格式化或參數傳遞
       logger.debug("循環迭代: %d, 複雜計算: %s", i, expensive_function(i))
       
   # 2. 使用條件檢查 (極端情況下)
   for i in range(1000000):
       if logger.level("DEBUG").no <= logger.level(logger._core.min_level).no:
           logger.debug(f"循環迭代: {i}")
           
   # 3. 使用異步日誌
   async_logger = create_logger(
       name="async_logger",
       log_file_settings={"enqueue": True}  # 啟用異步日誌
   )