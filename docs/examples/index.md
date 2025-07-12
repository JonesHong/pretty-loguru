# 範例總覽

Pretty Loguru 提供豐富的範例，幫助您快速上手和掌握各種功能。

## 🎯 學習路徑

### 1. 新手入門 (5分鐘)
**推薦順序**: 快速開始 → 基礎功能 → 視覺化功能

- **[快速開始](./quickstart.md)** - 3分鐘上手 Pretty-Loguru
  - Hello World 範例
  - 控制台輸出
  - 檔案日誌記錄

- **[基礎功能](./basics.md)** - 核心功能詳解
  - Logger 創建和使用
  - 多 Logger 管理
  - 錯誤處理
  - 輸出控制

- **[視覺化功能](./visual.md)** - Rich 區塊和 ASCII 藝術
  - Rich 面板和區塊
  - ASCII 藝術標題
  - 表格、樹狀、進度條
  - 程式碼高亮

### 2. 配置管理 (10分鐘)
**推薦順序**: 配置管理

- **[配置管理](./configuration.md)** - LoggerConfig 和輪替策略
  - LoggerConfig 使用
  - 配置模板 (ConfigTemplates)
  - 檔案輪替策略
  - 從檔案載入配置
  - 自定義預設配置

### 3. 實戰應用 (15分鐘)
**推薦順序**: 框架整合 → 生產環境

- **[框架整合](./integrations.md)** - FastAPI/Uvicorn 整合
  - FastAPI 基本整合
  - 中間件日誌
  - 依賴注入
  - Uvicorn 配置

- **[生產環境](./production.md)** - 部署最佳實踐
  - 環境配置管理
  - 性能監控
  - 錯誤追蹤
  - 日誌壓縮和清理

### 4. 進階探索 (30分鐘)
**適合**: 需要深度自訂功能的開發者

- **[進階功能](./advanced.md)** - 底層功能存取
  - 直接存取 Loguru
  - 自定義擴展
  - 性能優化

### 5. 企業級應用 (45分鐘)
**適合**: 大規模生產環境

- **[企業級應用](./enterprise.md)** - 大規模部署方案
  - 微服務架構
  - 安全性和合規
  - 監控系統整合
  - 集中式日誌管理

## 🚀 快速開始

### 安裝 Pretty-Loguru

```bash
pip install pretty-loguru
```

### 第一個範例

```python
from pretty_loguru import create_logger

# 創建 logger
logger = create_logger("my_app")

# 開始記錄
logger.info("Hello, Pretty-Loguru!")
logger.success("安裝成功！")
```

### 視覺化功能預覽

```python
# Rich 區塊
logger.block(
    "系統狀態",
    ["CPU: 45%", "記憶體: 2.3GB", "狀態: 正常"],
    border_style="green"
)

# ASCII 藝術
logger.ascii_header("WELCOME", font="slant")
```

## 📚 範例特色

### 完整可運行
- 每個範例都包含完整的程式碼
- 可直接複製使用
- 提供預期輸出說明

### 漸進式學習
- 從簡單到複雜的學習路徑
- 每個主題都有清晰的目標
- 實際應用場景導向

### 最佳實踐
- 遵循 Python 編碼規範
- 包含錯誤處理
- 性能和安全考量

## 🔥 熱門範例

### 快速開始
- **Hello World** - 最簡單的使用方式 ([查看範例](./quickstart.md#hello-world))
- **控制台日誌** - 只輸出到控制台 ([查看範例](./quickstart.md#控制台日誌))
- **檔案日誌** - 同時輸出到檔案 ([查看範例](./quickstart.md#檔案日誌))

### 基礎功能
- **簡單用法** - Logger 創建和基本使用 ([查看範例](./basics.md#簡單使用))
- **輸出控制** - 分離控制台和檔案輸出 ([查看範例](./basics.md#控制台-vs-檔案輸出))
- **錯誤處理** - 優雅的錯誤記錄 ([查看範例](./basics.md#錯誤處理範例))

### 視覺化功能
- **Rich 區塊** - 結構化的面板顯示 ([查看範例](./visual.md#rich-區塊))
- **ASCII 藝術** - 引人注目的標題 ([查看範例](./visual.md#ascii-藝術))
- **Rich 組件** - 表格、樹狀、進度條 ([查看範例](./visual.md#rich-組件))
- **程式碼高亮** - 語法高亮顯示 ([查看範例](./visual.md#程式碼高亮))

### 配置管理
- **LoggerConfig** - 配置物件使用 ([查看範例](./configuration.md#使用-loggerconfig))
- **配置模板** - 預定義配置 ([查看範例](./configuration.md#配置模板))
- **輪替策略** - 各種輪替方式 ([查看範例](./configuration.md#檔案輪替策略))
- **檔案配置** - 從 JSON 載入 ([查看範例](./configuration.md#從檔案載入配置))

## 💻 查看原始碼

所有範例的完整原始碼都可以在 GitHub 上查看：

📂 [GitHub - examples 目錄](https://github.com/JonesHong/pretty-loguru/tree/master/examples)

每個範例都包含：
- 📄 完整的 Python 程式碼
- 📖 詳細的說明文檔
- 🎯 實際運行效果

## 💡 使用技巧

### 開發階段
- 使用 `development` 配置模板
- 啟用 DEBUG 級別日誌
- 使用視覺化功能輔助除錯

### 測試階段
- 使用 `testing` 配置模板
- 分離測試日誌
- 使用目標導向輸出

### 生產階段
- 使用 `production` 配置模板
- 啟用日誌壓縮和清理
- 實施錯誤追蹤

## 🔗 相關資源

- **[安裝指南](../guide/installation.md)** - 安裝和環境設定
- **[API 文檔](../api/)** - 完整的 API 參考
- **[配置說明](../guide/custom-config.md)** - 深入配置選項
- **[最佳實踐](../guide/production.md)** - 生產環境建議

## ❓ 需要幫助？

- 📚 查看各範例頁面的詳細說明
- 💬 在 [GitHub Issues](https://github.com/JonesHong/pretty-loguru/issues) 提問
- 🔍 搜尋 [GitHub Discussions](https://github.com/JonesHong/pretty-loguru/discussions)

開始您的 Pretty Loguru 學習之旅吧！ 🎉