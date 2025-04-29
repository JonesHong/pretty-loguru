# pretty-loguru
[![PyPI version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![Python Version](https://img.shields.io/pypi/pyversions/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![License](https://img.shields.io/pypi/l/pretty-loguru.svg)](https://opensource.org/licenses/MIT)

## 說明

**pretty-loguru** 是一個 Python 日誌庫，擴展了 [Loguru](https://github.com/Delgan/loguru) 的功能，並使用 [Rich](https://github.com/Textualize/rich) 面板、ASCII 藝術標題和可自定義區塊來呈現優雅的輸出。它提供：

- **Rich Panels**：顯示帶有邊框和樣式的結構化日誌區塊。
- **ASCII Art Headers**：使用 `art` 庫生成引人注目的標題。
- **ASCII Blocks**：結合 ASCII 藝術和區塊日誌，形成完整的區段。
- **輕鬆初始化**：一次呼叫即可同時設置文件和控制台日誌。
- **Uvicorn 整合**：攔截並統一 Uvicorn 日誌為 Loguru 格式。

## 安裝

通過 pip 安裝：

```bash
pip install pretty-loguru
```

## 快速開始

```python
# 定義主函式以執行所有測試\import random
import time


def main_example():
    try:
        # 首先，導入日誌模組
        from pretty_loguru import logger, logger_start, is_ascii_only
        # 初始化日誌系統
        component_name = logger_start(folder="logger_test")
        logger.info(f"Logger system initialized, process ID: {component_name}")
        logger.info("Logging system feature test example")
        
        # 執行每個測試套件
        test_basic_logging()
        time.sleep(1)
        
        test_block_logging()
        time.sleep(1)
        
        test_ascii_logging()
        time.sleep(1)
        
        test_mock_application()
        
        logger.success("All tests completed!")
    except Exception as e:
        # 初始化日誌系統時出錯
        print(f"Error initializing logger system: {e}")
        import traceback
        traceback.print_exc()


def test_basic_logging():
    """測試基本日誌功能"""
    from pretty_loguru import logger
    
    logger.info("=== Testing Basic Logging ===")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.success("This is a success message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    logger.info("Basic logging test completed")


def test_block_logging():
    """測試區塊日誌功能"""
    from pretty_loguru import logger
    
    logger.info("=== Testing Block Logging ===")
    
    logger.block(
        "System Status Summary",
        [
            "CPU Usage: 45%",
            "Memory Usage: 60%",
            "Disk Space: 120GB available",
            "Network Connection: OK",
            "Service Status: All running"
        ],
        border_style="green",
        log_level="INFO"
    )
    
    logger.block(
        "Warning Messages",
        [
            "High memory usage detected",
            "Current growth rate: 5% / min",
            "Estimated to reach threshold in 30 minutes",
            "Suggested action: check for memory leaks"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    logger.info("Block logging test completed")


def test_ascii_logging():
    """測試 ASCII 藝術日誌功能"""
    from pretty_loguru import logger, is_ascii_only
    
    logger.info("=== Testing ASCII Art Logging ===")
    
    # 測試僅 ASCII 檢查函數
    logger.info("Checking if text contains only ASCII characters:")
    test_strings = [
        "Hello World",
        "Hello 世界",
        "123-456-789",
        "Special chars: ©®™",
        "ASCII symbols: !@#$%^&*()"
    ]
    
    for s in test_strings:
        result = is_ascii_only(s)
        logger.info(f"'{s}' only ASCII: {result}")
    
    # 顯示簡單的 ASCII 藝術標題
    logger.ascii_header(
        "SYSTEM START",
        font="standard",
        border_style="blue",
        log_level="INFO"
    )
    
    # 顯示不同字體的標題
    fonts = ["standard", "slant", "doom", "small", "block"]
    for font in fonts:
        try:
            logger.ascii_header(
                f"Font: {font}",
                font=font,
                border_style="cyan",
                log_level="INFO"
            )
        except Exception as e:
            logger.error(f"Failed to generate ASCII art with font '{font}': {e}")
    
    # 測試包含非 ASCII 字符的標題
    try:
        logger.ascii_header(
            "ASCII and café mix",  # 包含非 ASCII 字符 é
            font="standard",
            border_style="magenta",
            log_level="WARNING"
        )
    except ValueError as e:
        logger.error(f"Expected error: {e}")
    
    # 測試 ASCII 藝術區塊
    logger.ascii_block(
        "System Diagnostics Report",
        [
            "Check Time: " + time.strftime("%Y-%m-%d %H:%M:%S"),
            "System Load: OK",
            "Security Status: Good",
            "Recent Error Count: 0",
            "Uptime: 24h 12m"
        ],
        ascii_header="SYSTEM OK",
        ascii_font="small",
        border_style="green",
        log_level="SUCCESS"
    )
    
    logger.info("ASCII art logging test completed")


def test_mock_application():
    """模擬真實應用場景"""
    from pretty_loguru import logger
    
    logger.info("=== Simulated Application Scenario ===")
    
    # 應用啟動
    logger.ascii_header(
        "APP STARTUP",
        font="slant",
        border_style="blue",
        log_level="INFO"
    )
    
    logger.info("Loading configuration...")
    time.sleep(0.5)
    logger.success("Configuration loaded successfully")
    
    logger.block(
        "Application Configuration Summary",
        [
            "Application Name: Logging System Test",
            "Version: 1.0.0",
            "Environment: Development",
            "Log Level: DEBUG",
            "Max Log File Size: 20MB"
        ],
        border_style="cyan",
        log_level="INFO"
    )
    
    logger.info("Connecting to the database...")
    time.sleep(1)
    
    # 隨機模擬錯誤情況
    if random.random() < 0.3:
        logger.error("Database connection failed")
        logger.ascii_block(
            "Error Report",
            [
                "Error Type: Database connection failed",
                "Error Code: DB-5001",
                "Reason: Unable to resolve hostname",
                "Attempt Count: 3",
                "Suggested Action: Check network connection and database service status"
            ],
            ascii_header="ERROR",
            ascii_font="doom",
            border_style="red",
            log_level="ERROR"
        )
    else:
        logger.success("Database connected successfully")
        
        logger.info("Initializing services...")
        time.sleep(1.5)
        logger.success("Services initialized successfully")
        
        logger.ascii_block(
            "System Ready",
            [
                "Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S"),
                "Registered Modules: User Management, Authorization Center, Data Processing, Report Generation",
                "System Status: Running",
                "Listening Port: 8080",
                "API Version: v2"
            ],
            ascii_header="READY",
            ascii_font="block",
            border_style="green",
            log_level="SUCCESS"
        )
        
        # 模擬處理請求
        for i in range(3):
            logger.info(f"Received request #{i+1}")
            time.sleep(0.8)
            logger.success(f"Request #{i+1} processed successfully")
    
    # 應用關閉
    logger.info("Shutting down services...")
    time.sleep(1)
    logger.success("Services shut down safely")
    
    logger.ascii_header(
        "SHUTDOWN",
        font="standard",
        border_style="magenta",
        log_level="INFO"
    )
    
    logger.info("Mock application scenario test completed")


if __name__ == "__main__":
    main_example()
```

## 功能

### Rich 區塊日誌

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

自定義文件路徑、輪換和級別：

```python
from pretty_loguru import init_logger

init_logger(
    level="DEBUG",
    log_path="logs",
    component_name="my_app",
    rotation="10MB"
)
```

## 測試

運行測試套件：

```bash
pytest tests/
```

## 貢獻

歡迎貢獻！請在 [GitHub](https://github.com/yourusername/pretty-loguru) 上提交 issue 和 pull request。

## 授權

本專案採用 [MIT License](LICENSE) 授權。

