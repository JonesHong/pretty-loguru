# Pretty-Loguru 🎨

<p align="center">
  <img src="https://raw.githubusercontent.com/JonesHong/pretty-loguru/refs/heads/master/docs/public/logo.png" alt="pretty-loguru icon" width="200"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/pretty-loguru.svg">
  </a>
  <a href="https://pypi.org/project/pretty-loguru/">
    <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pretty-loguru.svg">
  </a>
  <a href="https://joneshong.github.io/pretty-loguru/">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-ghpages-blue.svg">
  </a>
  <a href="https://github.com/JonesHong/pretty-loguru/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/JonesHong/pretty-loguru.svg">
  </a>
  <a href="https://deepwiki.com/JonesHong/pretty-loguru">
    <img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki">
  </a>
</p>

增強版 Python 日誌庫，基於 [Loguru](https://github.com/Delgan/loguru)，整合 [Rich](https://github.com/Textualize/rich) 和 ASCII 藝術 [art](https://github.com/sepandhaghighi/art)，讓日誌輸出更加優雅和直觀。

---

## ✨ 特色功能

- 🎨 **Rich 區塊日誌** - 使用 Rich 面板顯示結構化日誌
- 🎯 **ASCII 藝術標題** - 生成引人注目的 ASCII 藝術標題
- 🔥 **一鍵初始化** - 簡單配置即可同時設置文件和控制台日誌
- 🚀 **FastAPI 整合** - 完美整合 FastAPI 和 Uvicorn
- 📊 **預設配置** - 提供開發、生產、測試環境的最佳實踐
- 🛠️ **高度自定義** - 支援自定義格式、顏色、輪換策略

## 📦 安裝

```bash
# 推薦（uv）
uv add pretty-loguru

# 備用（pip）
pip install pretty-loguru
```

可選 extras（加裝能力）：

```bash
# FIGlet 支援（可選）
uv add "pretty-loguru[figlet]"

# integrations 別名（FastAPI/Uvicorn）
uv add "pretty-loguru[integrations]"
```

## 🚀 快速開始

### 基本使用

```python
from pretty_loguru import create_logger

# 創建 logger
logger = create_logger("my_app")

# 基本日誌
logger.info("應用程序啟動")
logger.success("操作成功完成")
logger.warning("這是一個警告")
logger.error("發生錯誤")

# Rich 區塊
logger.block("系統狀態", "一切正常", border_style="green")

# ASCII 藝術
logger.ascii_header("WELCOME", font="slant")
```

## ✅ 語意一致（console ↔ file）

pretty-loguru 遵守一個簡單合約：

- **一次呼叫 → 一筆 Loguru event**（不在 logging API 內額外 `console.print(...)` 走旁路）
- console/file 只是同一筆 event 的**不同 renderer**
- 視覺化方法（例如 `block/table/tree/...`）會把 `pretty_kind`、`pretty_payload`、`pretty_text` 放進 `record["extra"]`

可觀測性建議路線：

- 先用 `serialize=True` 產生 JSON 檔案日誌，再用 Filebeat/Fluent Bit（ELK）或 Promtail/Grafana Agent（Loki）收集
- `loki_enabled=True` 直推僅建議用於簡單場景（best-effort：不重試 / 無離線緩衝 / 無 backpressure）

### 使用配置物件

```python
from pretty_loguru import LoggerConfig, create_logger
from pretty_loguru.addons import ConfigTemplates

# 使用預設模板
config = ConfigTemplates.production()
logger = create_logger("app", config=config)

# 自定義配置
custom_config = LoggerConfig(
    level="DEBUG",
    log_dir="logs",
    rotation="1 day",
    retention="7 days"
)
logger = create_logger("debug_app", config=custom_config)

# 更新現有 logger
config.update(level="INFO")  # 所有使用此配置的 logger 都會更新
```

### 多 Logger 管理

```python
# 創建多個 logger
auth_logger = create_logger("auth", level="INFO")
db_logger = create_logger("database", level="DEBUG")
api_logger = create_logger("api", level="WARNING")

# 統一配置管理
config = LoggerConfig(level="INFO", log_dir="logs")
loggers = config.apply_to("auth", "database", "api")

# 動態更新所有 logger
config.update(level="DEBUG")  # 所有 logger 同時更新
```

## 📖 文檔

完整文檔請訪問：[https://joneshong.github.io/pretty-loguru/](https://joneshong.github.io/pretty-loguru/)

- [使用指南](docs/guide/index.md)
- [API 參考](docs/api/index.md)
- [範例程式](examples/README.md)
- [配置說明](docs/guide/custom-config.md)


## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件。
