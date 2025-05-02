Pretty Loguru 文檔
================================================


.. meta::
   :template: template.html

.. |lang_switcher| raw:: html

   <div class="language-switcher">
    <a href="../zh_TW/index.html">繁體中文</a> | <a href="../en/index.html">English</a>
   </div>

|lang_switcher|

.. image:: _static/logo.png
   :width: 200px
   :align: center
   :alt: Pretty Loguru 標誌

**Pretty Loguru** 是一個增強型的 Loguru 日誌系統，提供區塊式日誌、
ASCII 藝術標題以及與各種框架的集成功能，使日誌記錄變得更加直觀和美觀。

特點
------

- 區塊式日誌格式，提高可讀性
- ASCII 藝術標題，增強視覺效果
- 目標導向日誌方法，明確輸出目標 (控制台、文件)
- 與 FastAPI、Uvicorn 的無縫集成
- 優雅的日誌輪換和清理機制
- 高度可定制的格式和配置

安裝
------

.. code-block:: bash

   pip install pretty-loguru

快速使用示例
------------------

.. code-block:: python

   from pretty_loguru import create_logger
   
   # 創建日誌實例
   logger = create_logger("my_app")
   
   # 輸出不同級別的日誌
   logger.info("這是一條資訊日誌")
   logger.warning("這是一條警告日誌")
   
   # 使用區塊功能
   logger.block(
       "系統狀態", 
       [
           "數據庫連接: 正常",
           "緩存服務: 正常",
           "存儲空間: 76% 可用"
       ]
   )

.. toctree::
   :maxdepth: 1
   :caption: 入門指南
   
   quickstart
   basic_usage
   advanced_features
   integrations
   contributing
   api/modules