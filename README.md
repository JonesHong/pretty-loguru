# pretty-loguru

[![PyPI version](https://img.shields.io/pypi/v/pretty-loguru.svg)](https://pypi.org/project/pretty-loguru)
[![Python Version](https://img.shields.io/pypi/pyversions/pretty-loguru.svg)]

## Description

**pretty-loguru** is a Python logging library that extends the power of [Loguru](https://github.com/Delgan/loguru) with elegant outputs using [Rich](https://github.com/Textualize/rich) panels, ASCII art headers, and customizable blocks. It provides:

- **Rich Panels**: Display structured log blocks with borders and styles.
- **ASCII Art Headers**: Generate eye-catching headers using the `art` library.
- **ASCII Blocks**: Combine ASCII art and block logs for comprehensive sections.
- **Easy Initialization**: One-call setup for both file and console logging.
- **Uvicorn Integration**: Intercept and unify Uvicorn logs with Loguru formatting.

## Installation

Install via pip:

```bash
pip install pretty-loguru
```

## Quick Start

```python
# Define the main function to run all tests
import random
import time


def main_example():
    try:
        # First, import the logging module
        from pretty_loguru import logger, logger_start, is_ascii_only
        # Initialize the logging system
        process_id = logger_start(folder="logger_test")
        logger.info(f"Logger system initialized, process ID: {process_id}")
        logger.info("Logging system feature test example")
        
        # Run each test suite
        test_basic_logging()
        time.sleep(1)
        
        test_block_logging()
        time.sleep(1)
        
        test_ascii_logging()
        time.sleep(1)
        
        test_mock_application()
        
        logger.success("All tests completed!")
    except Exception as e:
        print(f"Error initializing logger system: {e}")
        import traceback
        traceback.print_exc()


def test_basic_logging():
    """Test basic logging functionality"""
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
    """Test block logging functionality"""
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
    """Test ASCII art logging functionality"""
    from pretty_loguru import logger, is_ascii_only
    
    logger.info("=== Testing ASCII Art Logging ===")
    
    # Test ASCII-only check function
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
    
    # Display a simple ASCII art header
    logger.ascii_header(
        "SYSTEM START",
        font="standard",
        border_style="blue",
        log_level="INFO"
    )
    
    # Display headers in different fonts
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
    
    # Test header containing a non-ASCII character
    try:
        logger.ascii_header(
            "ASCII and café mix",  # contains non-ASCII é
            font="standard",
            border_style="magenta",
            log_level="WARNING"
        )
    except ValueError as e:
        logger.error(f"Expected error: {e}")
    
    # Test ASCII art block
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
    """Simulate a real-world application scenario"""
    from pretty_loguru import logger
    
    logger.info("=== Simulated Application Scenario ===")
    
    # Application startup
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
    
    # Randomly simulate an error condition
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
        
        # Simulate handling requests
        for i in range(3):
            logger.info(f"Received request #{i+1}")
            time.sleep(0.8)
            logger.success(f"Request #{i+1} processed successfully")
    
    # Application shutdown
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

## Features

### Rich Block Logging

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

### ASCII Art Headers

```python
logger.ascii_header(
    "APP START",
    font="slant",
    border_style="blue",
    log_level="INFO"
)
```

### ASCII Art Blocks

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

### Uvicorn Integration

```python
from pretty_loguru import uvicorn_init_config
uvicorn_init_config()
```

## Configuration

Customize file path, rotation, and level:

```python
from pretty_loguru import init_logger

init_logger(
    level="DEBUG",
    log_path="logs",
    process_id="my_app",
    rotation="10MB"
)
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

Contributions welcome! Please open issues and pull requests on [GitHub](https://github.com/yourusername/pretty-loguru).

## License

This project is licensed under the [MIT License](LICENSE).

