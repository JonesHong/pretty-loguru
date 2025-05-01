貢獻指南
============

感謝你考慮為 Pretty Loguru 專案做出貢獻！這個頁面介紹了如何參與專案開發。

開發環境設置
------------------

.. code-block:: bash

   # 克隆儲存庫
   git clone https://github.com/yourusername/pretty-loguru.git
   cd pretty-loguru
   
   # 創建虛擬環境（推薦）
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate  # Windows
   
   # 安裝開發依賴
   pip install -e ".[dev]"

代碼風格
------------

本專案遵循 PEP 8 代碼風格指南，並使用 Black 進行代碼格式化：

.. code-block:: bash

   # 在提交前格式化代碼
   black pretty_loguru

測試
------

在提交更改前，請確保所有測試都能通過：

.. code-block:: bash

   # 運行所有測試
   pytest
   
   # 運行特定測試模組
   pytest tests/test_core.py

   # 檢查代碼覆蓋率
   pytest --cov=pretty_loguru

文檔貢獻
------------

文檔是用 Sphinx 生成的:

.. code-block:: bash

   # 安裝文檔依賴
   pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser

   # 構建文檔
   cd docs
   make html
   
   # 在瀏覽器中查看文檔
   # Linux/macOS
   open build/html/index.html
   # Windows
   start build\\html\\index.html

貢獻流程
------------

1. Fork 儲存庫
2. 創建你的功能分支: `git` checkout` -b` feature/amazing-feature`
3. 提交你的更改: `git` commit` -m` '添加了一個很棒的功能'`
4. 推送到分支: `git` push` origin` feature/amazing-feature`
5. 開啟一個 Pull Request

Bug 報告
------------------

如果你發現了 bug，請在 GitHub Issues 中報告，並包含以下信息:

- 問題的簡短描述
- 重現步驟
- 預期行為與實際行為
- 環境信息 (操作系統, Python 版本等)
- 如果可能，提供一個最小的代碼示例來重現問題

功能請求
------------

如果你有新功能的想法，請在 GitHub Issues 中提出，並盡可能提供以下信息:

- 功能描述
- 為什麼這個功能對專案有價值
- 如何實現的建議 (如果有)
- 可能的使用示例

變更日誌
------------

當添加新特性或修復 bug 時，請在 `CHANGELOG`.md` 中添加相應的條目。`

許可證
---------

通過提交代碼，你同意將你的代碼貢獻授權給專案的許可證。