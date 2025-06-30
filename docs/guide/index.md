# 指南

歡迎來到 pretty-loguru 的完整指南！這裡將帶你從零開始，逐步掌握這個強大的日誌庫。

## 🎯 學習路徑

### 🚀 新手入門
如果你是第一次使用 pretty-loguru，建議按照以下順序學習：

1. **[安裝](./installation)** - 環境設置和安裝步驟
2. **[快速開始](./quick-start)** - 5分鐘上手
3. **[基本用法](./basic-usage)** - 核心功能和基礎概念

### 🎨 功能探索
掌握基礎後，探索 pretty-loguru 的獨特功能：

4. **[Rich 區塊日誌](../features/rich-blocks)** - 結構化的視覺日誌
5. **[ASCII 藝術標題](../features/ascii-art)** - 引人注目的標題
6. **[ASCII 藝術區塊](../features/ascii-blocks)** - 結合區塊和藝術

### 🔧 進階配置
深入了解高級功能和最佳實踐：

7. **[自定義配置](./custom-config)** - 客製化日誌行為
8. **[日誌輪換](./log-rotation)** - 檔案管理和清理
9. **[效能最佳化](./performance)** - 生產環境調優

### 🌐 整合應用
將 pretty-loguru 整合到你的專案中：

10. **[FastAPI 整合](../integrations/fastapi)** - Web API 日誌
11. **[Uvicorn 整合](../integrations/uvicorn)** - ASGI 伺服器日誌
12. **[生產環境部署](./production)** - 企業級部署指南

## 📚 核心概念

### Logger 初始化
pretty-loguru 提供多種初始化方式：

```python
from pretty_loguru import logger, logger_start, create_logger

# 方式一：快速開始（推薦）
component_name = logger_start(folder="logs")

# 方式二：自定義 logger
my_logger = create_logger(
    name="my_app",
    level="DEBUG",
    log_path="custom_logs"
)

# 方式三：進階配置
from pretty_loguru import init_logger
init_logger(
    level="INFO",
    log_path="logs",
    component_name="web_app",
    rotation="10MB",
    retention="7 days"
)
```

### 日誌級別
支援標準的日誌級別，並新增了 `success` 級別：

- `logger.debug()` - 除錯訊息
- `logger.info()` - 一般訊息  
- `logger.success()` - 成功訊息（綠色顯示）
- `logger.warning()` - 警告訊息
- `logger.error()` - 錯誤訊息
- `logger.critical()` - 嚴重錯誤

### 視覺化功能
pretty-loguru 的特色在於豐富的視覺化輸出：

```python
# Rich 區塊
logger.block("標題", ["內容1", "內容2"], border_style="green")

# ASCII 標題
logger.ascii_header("STARTUP", font="slant")

# ASCII 區塊（結合兩者）
logger.ascii_block(
    "報告",
    ["狀態: 正常", "時間: 10:30"],
    ascii_header="REPORT",
    ascii_font="small"
)
```

## 🎮 互動式範例

想要立即體驗？查看我們的 [範例集合](../examples/)，包含：

- [基礎用法範例](../examples/basics/) - 從簡單開始
- [視覺化範例](../examples/visual/) - 展示所有視覺功能
- [FastAPI 範例](../examples/fastapi/) - Web 應用整合
- [生產環境範例](../examples/production/) - 實際部署案例

## ❓ 遇到問題？

- 查看 [常見問題](../faq) 
- 參考 [API 文件](../api/)
- 在 [GitHub](https://github.com/JonesHong/pretty-loguru/issues) 提交問題

讓我們開始這個優雅的日誌之旅吧！ 🚀