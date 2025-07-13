# Pretty-Loguru 🎨

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

增強版 Python 日誌庫，基於 [Loguru](https://github.com/Delgan/loguru)，整合 [Rich](https://github.com/Textualize/rich) 和 ASCII 藝術，讓日誌輸出更加優雅和直觀。

## ✨ 特色功能

- 🎨 **Rich 區塊日誌** - 使用 Rich 面板顯示結構化日誌
- 🎯 **ASCII 藝術標題** - 生成引人注目的 ASCII 藝術標題
- 🔥 **一鍵初始化** - 簡單配置即可同時設置文件和控制台日誌
- 🚀 **FastAPI 整合** - 完美整合 FastAPI 和 Uvicorn
- 📊 **預設配置** - 提供開發、生產、測試環境的最佳實踐
- 🛠️ **高度自定義** - 支援自定義格式、顏色、輪換策略

## 📦 安裝

```bash
pip install pretty-loguru
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

### 使用配置物件

```python
from pretty_loguru import create_logger, LoggerConfig, ConfigTemplates

# 使用預設模板
config = ConfigTemplates.production()
logger = create_logger("app", config=config)

# 自定義配置
custom_config = LoggerConfig(
    level="DEBUG",
    log_path="logs",
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
config = LoggerConfig(level="INFO", log_path="logs")
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