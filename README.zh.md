# pretty-loguru

[![PyPI 版本](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![支援 Python 版本](https://img.shields.io/pypi/pyversions/pretty-loguru.svg)]

## 說明

**pretty-loguru** 是一個擴充 [Loguru](https://github.com/Delgan/loguru) 功能的 Python 日誌函式庫，結合 [Rich](https://github.com/Textualize/rich) 面板、ASCII 藝術標題與可客製化區塊，提供：

- **Rich 段落日誌**：使用邊框與樣式顯示結構化區塊日誌。
- **ASCII 藝術標題**：透過 `art` 函式庫產生吸睛的藝術標題。
- **ASCII 藝術區塊**：結合 ASCII 藝術與區塊日誌，打造完整區段。
- **簡易初始化**：一鍵同時設定檔案與終端輸出日誌。
- **Uvicorn 整合**：攔截並統一 Uvicorn 日誌格式。

## 安裝

使用 pip 安裝：

```bash
pip install pretty-loguru
```

## 快速開始

```python
from pretty_loguru import logger, logger_start

# Initialize the logger (creates file handler + console handler)
process_id = logger_start(folder="my_app")
logger.info("Logger initialized.")

# Basic logging
logger.debug("Debug message.")
logger.success("Operation was successful.")
logger.warning("This is a warning.")
logger.error("An error occurred.")
```

## 功能

### Rich 段落日誌

```python
logger.block(
    "System Summary",
    [
        "CPU Usage: 45%",
        "Memory Usage: 60%",
        "Disk Space: 120GB free"
    ],
    border_style="green",
    log_level="INFO"
)
```

### ASCII 藝術標題

```python
logger.ascii_header(
    "APP START",
    font="slant",
    border_style="blue",
    log_level="INFO"
)
```

### ASCII 藝術區塊

```python
logger.ascii_block(
    "Startup Report",
    ["Step 1: OK", "Step 2: OK", "Step 3: OK"],
    ascii_header="SYSTEM READY",
    ascii_font="small",
    border_style="cyan",
    log_level="SUCCESS"
)
```

### Uvicorn 整合

```python
from pretty_loguru import uvicorn_init_config
uvicorn_init_config()
```

## 設定

客製化檔案路徑、輪替與等級：

```python
from pretty_loguru import init_logger

init_logger(
    level="DEBUG",
    log_path="logs",
    process_id="my_app",
    rotation="10MB"
)
```

## 測試

執行測試套件：

```bash
pytest tests/
```

## 貢獻

歡迎貢獻！請在 [GitHub](https://github.com/yourusername/pretty-loguru) 開啟 issues 或 pull requests。

## 授權

本專案遵循 [MIT 授權條款](LICENSE)。

