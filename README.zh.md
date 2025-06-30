# Pretty Loguru

<p align="center">
  <img src="https://raw.githubusercontent.com/JonesHong/pretty-loguru/refs/heads/master/assets/images/logo.png" alt="pretty-loguru icon" width="200"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/pretty-loguru.svg">
  </a>
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pretty-loguru.svg">
  </a>
  <a href="https://joneshong.github.io/pretty-loguru/en/index.html">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-ghpages-blue.svg">
  </a>
  <a href="https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/JonesHong/pretty-loguru.svg">
  </a>
  <a href="https://deepwiki.com/JonesHong/pretty-loguru"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

## 🎯 為什麼選擇 Pretty Loguru？

**Pretty Loguru** 是一個美觀且易用的 Python 日誌庫，在 [Loguru](https://github.com/Delgan/loguru) 的基礎上增加了視覺增強和生產就緒功能：

### 🆚 與原始 Loguru 的核心差異

| 特色 | Loguru | Pretty Loguru |
|------|--------|---------------|
| **視覺效果** | 純文字輸出 | ✨ ASCII 藝術、色彩區塊、Rich 元件 |
| **框架整合** | 手動配置 | 🚀 一行整合 FastAPI + Uvicorn |
| **生產就緒** | 基礎功能 | 📊 監控、壓縮、錯誤追蹤 |
| **配置管理** | 程式碼配置 | ⚙️ 工廠模式、預設系統 |
| **學習曲線** | 需要學習 | 📚 5分鐘上手，範例完整 |

---

## ⚡ 5分鐘快速上手

### 安裝

```bash
pip install pretty-loguru
```

### 最簡單的使用方式

```python
from pretty_loguru import create_logger

# 創建 logger 並開始使用
logger = create_logger("my_app", log_path="./logs")

logger.info("這是普通訊息")
logger.success("這是成功訊息") 
logger.warning("這是警告訊息")
logger.error("這是錯誤訊息")
```

### 原生格式支援 (v2.1.0+)

```python
# 適合從 loguru 遷移或開發調試
logger = create_logger("my_app", use_native_format=True)
logger.info("接近 loguru 原生格式")
# 輸出：main.py:function:42 - 接近 loguru 原生格式
```

### 一行整合 FastAPI

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

app = FastAPI()
logger = create_logger("api", log_path="./logs")

# 一行整合所有日誌功能（包含 uvicorn）
integrate_fastapi(app, logger)

@app.get("/")
async def root():
    logger.info("API 請求處理")
    return {"message": "Hello World"}
```

---

## 🎨 視覺特色展示

### ASCII 藝術標題

```python
logger.ascii_header("WELCOME", style="block")
```

輸出效果：
```
╭───────────────────────────────────────────────────────────────────────────────╮
│  _       __    ______    __    ______   ____     __  ___    ______            │
│ | |     / /   / ____/   / /   / ____/  / __ \   /  |/  /   / ____/            │
│ | | /| / /   / __/     / /   / /      / / / /  / /|_/ /   / __/               │
│ | |/ |/ /   / /___    / /___/ /___   / /_/ /  / /  / /   / /___               │
│ |__/|__/   /_____/   /_____/\____/   \____/  /_/  /_/   /_____/               │
│                                                                               │
│                                                                               │
╰───────────────────────────────────────────────────────────────────────────────╯
```

### 彩色資訊區塊

```python
logger.block(
    "系統狀態檢查",
    "✅ 資料庫連線正常\n✅ API 服務運行中\n⚠️  記憶體使用率 85%",
    border_style="green"
)
```

### Rich 元件整合

```python
# 表格顯示
logger.table(
    ["用戶", "狀態", "登入時間"],
    [
        ["Alice", "在線", "10:30"],
        ["Bob", "離線", "09:15"]
    ]
)

# 進度追蹤
for item in logger.progress.track_list(items, description="處理中..."):
    process(item)
```

---

## 🏭 生產環境就緒

### 自動輪替與壓縮

```python
# 按大小輪替（10MB）+ ZIP 壓縮
logger = create_logger(
    "production_app",
    log_path="./logs",
    rotation="10 MB",
    retention="30 days",
    compression="zip"
)
```

### 環境自適應配置

```python
import os

# 根據環境自動調整
env = os.getenv("APP_ENV", "development")
if env == "production":
    logger = create_logger("app", level="WARNING", rotation="daily")
else:
    logger = create_logger("app", level="DEBUG")
```

### 錯誤追蹤與重試機制

```python
@retry_with_logging(max_attempts=3, logger=logger)
def database_operation():
    # 自動記錄重試過程
    return db.query("SELECT * FROM users")

# 結構化錯誤記錄
logger.error("資料庫連線失敗", extra={
    "error_type": "ConnectionError",
    "host": "db.example.com",
    "retry_count": 2
})
```

---

## 📚 完整學習路徑

### 🟢 新手級別 (5分鐘)
- [基礎使用](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/01_basics/simple_usage.py) - 創建 logger 和基本輸出
- [控制台vs檔案](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/01_basics/console_vs_file.py) - 分離輸出目標
- [目標導向日誌](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/01_basics/target_logging.py) - console_info, file_error 等

### 🟡 進階級別 (15分鐘)  
- [ASCII 藝術](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/02_visual/ascii_art.py) - 美化標題和狀態
- [色彩區塊](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/02_visual/blocks.py) - 結構化資訊展示
- [Rich 元件](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/02_visual/rich_components.py) - 表格、樹狀圖、進度條

### 🟠 專業級別 (30分鐘)
- [預設配置](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/03_presets/preset_comparison.py) - 快速配置不同場景
- [輪替策略](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/03_presets/rotation_examples.py) - 檔案管理最佳實踐
- [自訂預設](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/03_presets/custom_presets.py) - 客製化配置

### 🔴 專家級別 (60分鐘)
- [FastAPI 整合](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/04_fastapi/simple_api.py) - Web 應用日誌
- [中間件應用](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/04_fastapi/middleware_demo.py) - 請求追蹤
- [生產部署](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/05_production/deployment_logging.py) - 企業級配置
- [錯誤監控](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/05_production/error_tracking.py) - 異常處理與分析
- [性能監控](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/05_production/performance_monitoring.py) - 系統健康檢查

---

## 🔧 核心 API 參考

### 基本使用

```python
from pretty_loguru import create_logger

# 基本創建
logger = create_logger("app_name")

# 完整配置
logger = create_logger(
    name="my_service",
    log_path="./logs",
    level="INFO",
    rotation="1 day",
    retention="1 month",
    compression="zip"
)

# 原生格式 (v2.1.0+)
logger = create_logger(
    name="my_app",
    use_native_format=True,  # 使用接近 loguru 原生格式
    log_path="./logs"
)
```

### 框架整合

```python
# FastAPI 整合
from pretty_loguru.integrations.fastapi import integrate_fastapi
integrate_fastapi(app, logger)

# Uvicorn 整合
from pretty_loguru.integrations.uvicorn import integrate_uvicorn  
integrate_uvicorn(logger)
```

### 視覺元件

```python
# ASCII 標題
logger.ascii_header("TITLE", style="block")

# 自訂區塊
logger.block("標題", "內容", border_style="blue")

# Rich 元件
logger.table(headers, rows)
logger.tree("Root", {"child1": "value1"})
```

---

## 🎯 核心優勢總結

1. **🎨 視覺優先**: 比 Loguru 更美觀的輸出，ASCII 藝術讓日誌有視覺衝擊力
2. **🚀 即插即用**: FastAPI 一行整合，比手動配置節省 80% 時間  
3. **🏭 生產就緒**: 企業級功能（輪替、壓縮、監控）開箱即用
4. **⚙️ 配置簡化**: 工廠模式和預設系統，告別複雜的手動配置
5. **📚 學習友善**: 5分鐘上手，完整範例覆蓋所有使用場景

---

## 📖 進階資源

- [📘 完整文檔](https://joneshong.github.io/pretty-loguru/en/index.html)
- [🎯 範例集合](https://github.com/JonesHong/pretty-loguru/tree/master/examples_new/) - 從新手到專家的完整學習路徑
- [⚙️ API 參考](https://joneshong.github.io/pretty-loguru/en/api/index.html)
- [🐛 問題回報](https://github.com/JonesHong/pretty-loguru/issues)
- [💡 功能建議](https://github.com/JonesHong/pretty-loguru/discussions)

---

## 🤝 貢獻

歡迎貢獻！請查看 [貢獻指南](CONTRIBUTING.md) 了解如何參與專案開發。

## 📜 授權

本專案採用 [MIT 授權](LICENSE)。