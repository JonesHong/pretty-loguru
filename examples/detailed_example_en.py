"""
pretty_loguru Detailed Usage Examples

This example demonstrates various usage scenarios and advanced features, including:
1. Basic logger instance creation and usage
2. Managing and using multiple loggers
3. Special format outputs (blocks, ASCII art, FIGlet)
4. Different output targets (console, file)
5. Integration with FastAPI/Uvicorn
6. Advanced configuration and customization
"""
import sys
from pathlib import Path

# 提前處理載入路徑選擇
use_local_lib = input("Do you want to load global libraries? [Y/n]: ").strip().lower()
if use_local_lib in {"no", "n"}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    print("Local libraries will be used.\n")
else:
    print("Global libraries will be used.\n")

import time
time.sleep(0.8)
import random
import threading

# Import pretty_loguru module
from pretty_loguru import (
    # Factory functions and pre-configured loggers
    create_logger,
    default_logger,
    get_logger,
    list_loggers,
    reinit_logger,
    # Special utility functions
    print_block,
    print_ascii_header,
    print_ascii_block,
    is_ascii_only,
    # Configuration-related
    LoggerConfig,
    # Integration-related
    configure_uvicorn,
)

# Check for FIGlet support
try:
    from pretty_loguru import print_figlet_header, print_figlet_block, get_figlet_fonts

    _has_figlet = True
except ImportError:
    _has_figlet = False

# Check for FastAPI support
try:
    from pretty_loguru import setup_fastapi_logging

    _has_fastapi = True
except ImportError:
    _has_fastapi = False

logger = default_logger()  # Get the default logger instance


def example_1_basic_usage():
    """Basic usage example - console-only and file-enabled loggers"""
    print("\n--- Example 1: Basic Usage ---\n")

    # 1.0 Load or create configuration
    config_path = Path.cwd() / "logs" / "logger_config.json"
    if config_path.exists():
        try:
            config = LoggerConfig.from_file(config_path)
        except:
            config = LoggerConfig(
                level="DEBUG", rotation="10 MB", log_path=Path.cwd() / "logs"
            )
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config.save_to_file(config_path)
    else:
        config = LoggerConfig(
            level="DEBUG", rotation="10 MB", log_path=Path.cwd() / "logs"
        )
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config.save_to_file(config_path)

    # 1.1 Console-only logger (like native loguru)
    dev_logger = create_logger("dev_app")
    dev_logger.info("Development message - console only")

    # 1.2 Create a file-enabled logger
    app_logger = create_logger(
        name="example_app",
        log_path=config.log_path,
        preset="daily",
        subdirectory="example_1_basic",
        level=config.level,
        rotation=config.rotation,
    )

    # 1.3 Test basic logging (covering all levels)
    app_logger.debug("This is a debug message for detailed information during development")
    app_logger.info("This is an info message to record normal program operation")
    app_logger.success("This is a success message indicating successful operation")
    app_logger.warning("This is a warning message indicating potential issues or anomalies")
    app_logger.error("This is an error message indicating an error that can still continue")
    app_logger.critical("This is a critical error message indicating the program cannot continue")

    # 1.4 Output targeting - console vs file
    app_logger.console_info("Console-only debug info")
    app_logger.file_error("Critical error - file only")

    # 1.5 Bind user context
    user_logger = app_logger.bind(user_id="12345", session_id="abc-xyz-123")
    user_logger.info("User has logged into the system")
    user_logger.warning("User attempted to access restricted resources")

    # 1.6 Test global logger (original default_logger)
    logger.info("This message is from the global default_logger")

    # 1.7 List all loggers
    all_loggers = list_loggers()
    app_logger.info(f"All registered loggers: {all_loggers}")

    # 1.8 ANSI color support
    app_logger.opt(colors=True).info("This is a message with <green>colors</green> and <red>styles</red>")

    # 1.9 Reuse an already created logger
    same_logger = get_logger("example_app")  # Returns the same instance
    if same_logger:
        same_logger.info("This message is from the same logger instance retrieved again")
    else:
        app_logger.warning("Failed to retrieve the same logger instance")

    # 1.10 Use the default logger
    default_logger().info("This message is from the default logger instance")

    # 1.11 Backward-compatible global logger
    logger.info("This message is from the global logger (backward-compatible)")

    # 1.12 Example of configuration management using LoggerConfig
    new_config = LoggerConfig(
        level="INFO", rotation="5 KB", log_path=Path.cwd() / "logs" 
    )
    app_logger.info(f"Logger configuration: {new_config.to_dict()}")
    # Save the new configuration to an example path
    example_path = Path.cwd() / "logs" / "logger_config_example.json"
    new_config.save_to_file(example_path)
    app_logger.info(f"Logger configuration saved to: {example_path}")

    # 1.13 Logger proxy for cross-module synchronization
    proxy_logger = create_logger("proxy_test", log_path="./logs", use_proxy=True)
    proxy_logger.info("Logger with proxy support")
    
    # Reinitialize with new configuration
    reinit_logger("proxy_test", log_path="./logs", level="WARNING")
    proxy_logger.warning("Logger reconfigured - all imports will use new settings")

    return app_logger


def example_2_multiple_loggers():
    """Example of managing and using multiple logger instances"""
    print("\n--- Example 2: Multiple Logger Instances ---\n")

    # 2.1 Create different loggers for different components
    # Console-only logger for development
    dev_logger = create_logger("development")
    
    # File-enabled loggers with different configurations
    auth_logger = create_logger(
        name="auth_service",
        log_path="./logs",
        subdirectory="example_2_services/auth",
        level="DEBUG"
    )

    db_logger = create_logger(
        name="database_service",
        log_path="./logs",
        preset="hourly",
        subdirectory="example_2_services/db"
    )

    api_logger = create_logger(
        name="api_service",
        log_path="./logs",
        preset="daily",
        subdirectory="example_2_services/api"
    )

    # 2.2 Use corresponding loggers in different components
    dev_logger.info("Development mode - console only")
    auth_logger.info("Authentication service started")
    db_logger.info("Database connection pool initialized, connections: 10")
    api_logger.info("API service started, listening on port: 8000")

    # 2.3 Log relevant messages in exceptional situations
    try:
        # Simulate database operation error
        if random.random() > 0.5:
            raise Exception("Database connection failed")
        db_logger.success("Database query successful")
    except Exception as e:
        db_logger.error(f"Database operation error: {str(e)}")
        api_logger.error("API request processing failed due to database error")

    # 2.4 Log relevant messages during user request processing
    def handle_request(user_id, endpoint):
        # Log request start
        request_logger = api_logger.bind(
            user_id=user_id, endpoint=endpoint, request_id=f"req-{int(time.time())}"
        )
        request_logger.info(f"Received request from user {user_id}: {endpoint}")

        # Simulate authentication process
        auth_logger.debug(f"Authenticating user {user_id}")

        # Simulate database operation
        db_logger.debug(f"Querying data for user {user_id}")

        # Log request end
        request_logger.info("Request processing completed")

    # Simulate processing a few requests
    handle_request("user123", "/api/profile")
    handle_request("admin", "/api/users")

    # 2.5 View all registered loggers
    all_loggers = list_loggers()
    auth_logger.info(f"All registered loggers: {all_loggers}")
    
    # 2.6 Get existing logger by name
    auth_log = get_logger("auth_service")
    if auth_log:
        auth_log.info("Retrieved existing auth logger")

    return auth_logger, db_logger, api_logger


def example_3_special_formats():
    """Example of special format outputs"""
    print("\n--- Example 3: Special Format Outputs ---\n")

    # Create a logger for special formats
    format_logger = create_logger(
        name="format_demo", 
        log_path="./logs",
        subdirectory="example_3_formats"
    )

    # 3.1 Use block format
    format_logger.block(
        title="System Status Report",
        message_list=[
            "CPU Usage: 45%",
            "Memory Usage: 60%",
            "Disk Space: 120GB Available",
            "Network: Normal",
            "Service Status: All services running",
        ],
        border_style="green",
        log_level="INFO",
    )

    # 3.2 Use ASCII art header
    format_logger.ascii_header(
        text="WARNING",
        font="block",  # Use block font
        border_style="yellow",
        log_level="WARNING",
    )

    # 3.3 Use block with ASCII art header
    format_logger.ascii_block(
        title="System Alert",
        message_list=[
            "Detected abnormal traffic",
            "Time: 2025-04-28 15:30:45",
            "Source IP: 192.168.1.100",
            "Target: Authentication Service",
            "Possible attack type: Brute Force",
        ],
        ascii_header="ALERT",
        ascii_font="banner3",  # Use banner3 font
        border_style="red",
        log_level="ERROR",
    )

    # 3.4 Directly use helper functions (not through logger instance)
    print_block(
        title="Directly Using Block Function",
        message_list=[
            "This is using direct functions instead of logger instance",
            "Suitable for quick usage without creating a logger",
        ],
        border_style="blue",
        log_level="INFO",
    )

    print_ascii_header(
        text="DIRECT", font="standard", border_style="magenta", log_level="INFO"
    )

    # 3.5 Check if text contains only ASCII characters
    text1 = "Hello, World!"
    text2 = "你好，世界！"

    format_logger.info(
        f"'{text1}' contains only ASCII characters: {format_logger.is_ascii_only(text1)}"
    )
    format_logger.info(
        f"'{text2}' contains only ASCII characters: {format_logger.is_ascii_only(text2)}"
    )
    format_logger.info(
        f"Using global function: '{text1}' contains only ASCII characters: {is_ascii_only(text1)}"
    )

    # 3.6 Use FIGlet art (if available)
    try:
        if _has_figlet:
            format_logger.info("FIGlet support enabled")

            # Use FIGlet through logger instance
            if hasattr(format_logger, "figlet_header"):
                format_logger.figlet_header(
                    text="FIGLET", font="slant", border_style="cyan", log_level="INFO"
                )

                format_logger.figlet_block(
                    title="FIGlet Block Example",
                    message_list=[
                        "This is a block example using FIGlet art",
                        "FIGlet offers more font options than ASCII art",
                    ],
                    figlet_header="DEMO",
                    figlet_font="big",
                    border_style="green",
                    log_level="INFO",
                )

                # List available FIGlet fonts
                if hasattr(format_logger, "get_figlet_fonts"):
                    fonts = format_logger.get_figlet_fonts()
                    format_logger.info(f"Number of available FIGlet fonts: {len(fonts)}")
                    format_logger.info(f"Some FIGlet fonts: {list(fonts)[:5]}")

            # Directly use FIGlet helper functions
            print_figlet_header(
                text="DIRECT", font="standard", border_style="blue", log_level="INFO"
            )
        else:
            format_logger.info("Logger instance does not support figlet_header method")
    except Exception as e:
        format_logger.info(f"FIGlet header output skipped: {type(e).__name__}")

    return format_logger


def example_4_output_targets():
    """Example of different output targets"""
    print("\n--- Example 4: Different Output Targets ---\n")

    # Create a logger for testing different output targets
    target_logger = create_logger(
        name="output_targets", 
        log_path="./logs",
        subdirectory="example_4_targets"
    )

    # 4.1 Standard logging (output to both console and file)
    target_logger.info("This message will appear in both console and log file")

    # 4.2 Console-only output
    target_logger.console_info("This message will only appear in the console, not in the log file")
    target_logger.console_warning("Console-only warning message")
    target_logger.console_error("Console-only error message")

    # 4.3 File-only output
    target_logger.file_info("This message will only be written to the log file, not shown in the console")
    target_logger.file_warning("File-only warning message")
    target_logger.file_error("File-only error message")

    # 4.4 Use general target methods
    target_logger.console("INFO", "General method: console-only output")
    target_logger.file("WARNING", "General method: file-only output")

    # 4.5 Development mode logging (same as console logging but more semantic)
    target_logger.dev_info("Development mode info - for debugging")
    target_logger.dev_debug("More detailed development mode debug message")

    # 4.6 Use ASCII art header specifying output target
    target_logger.ascii_header(
        text="CONSOLE",
        font="standard",
        border_style="cyan",
        to_console_only=True,  # Console-only output
    )

    target_logger.ascii_header(
        text="FILE",
        font="standard",
        border_style="cyan",
        to_log_file_only=True,  # File-only output
    )

    return target_logger


def example_5_integrations():
    """Example of integration features"""
    print("\n--- Example 5: Integration Features ---\n")

    # 5.1 Create a logger for integration examples
    integration_logger = create_logger(
        name="integration_demo",
        log_path="./logs",
        subdirectory="example_5_integrations",
    )
    # 5.2 Uvicorn integration
    integration_logger.info("Configuring Uvicorn to use Loguru")
    try:
        configure_uvicorn(logger_instance=integration_logger)
        integration_logger.success("Uvicorn configured to use Loguru")
    except ImportError as e:
        integration_logger.warning(f"Uvicorn integration failed: {str(e)}")

    # 5.3 FastAPI integration (if available)
    try:
        if _has_fastapi:
            integration_logger.info("FastAPI support enabled")
            integration_logger.info(
                "In a real FastAPI application, you can use the setup_fastapi_logging function"
            )

            # Example code snippet
            fastapi_example = """
            from fastapi import FastAPI
            from pretty_loguru import setup_fastapi_logging
            
            app = FastAPI()
            setup_fastapi_logging(
                app,
                log_request_body=True,
                log_response_body=True
            )
            
            @app.get("/")
            def read_root():
                return {"message": "Hello World"}
            """

            integration_logger.info("FastAPI integration example code:")
            for line in fastapi_example.strip().split("\n"):
                integration_logger.console_info(f"    {line}")
        else:
            integration_logger.warning(
                "FastAPI support not enabled, install the fastapi package to enable this feature"
            )
    except ImportError:
        integration_logger.info("FastAPI support not enabled, but other features are unaffected")
    except Exception as e:
        integration_logger.info(f"FastAPI integration example skipped: {type(e).__name__}")

    # 5.4 Simulate request processing logs
    integration_logger.info("Simulating web application request processing")

    for i in range(3):
        req_id = f"req-{i+1:03d}"
        path = f"/api/items/{random.randint(1, 100)}"
        method = random.choice(["GET", "POST", "PUT", "DELETE"])

        req_logger = integration_logger.bind(
            request_id=req_id, path=path, method=method, client_ip="192.168.1.100"
        )

        start_time = time.time()
        req_logger.info(f"Received {method} request: {path}")

        # Simulate processing time
        time.sleep(random.random() * 0.2)

        # Simulate different response statuses
        status_code = random.choice([200, 200, 200, 201, 400, 404, 500])
        process_time = time.time() - start_time

        if status_code >= 500:
            req_logger.error(
                f"Request {req_id} processing error, status code: {status_code}, time taken: {process_time:.3f}s"
            )
        elif status_code >= 400:
            req_logger.warning(
                f"Request {req_id} completed with client error, status code: {status_code}, time taken: {process_time:.3f}s"
            )
        else:
            req_logger.success(
                f"Request {req_id} processed successfully, status code: {status_code}, time taken: {process_time:.3f}s"
            )

    return integration_logger


def example_6_advanced_features():
    """Example of advanced features and customization"""
    print("\n--- Example 6: Advanced Features and Customization ---\n")

    # 6.1 Create a logger with custom configuration
    advanced_logger = create_logger(
        name="advanced_features",
        log_path="./logs",
        preset="daily",
        subdirectory="example_6_advanced",
        level="DEBUG",
        rotation="500 KB",
        retention="1 week",
        start_cleaner=True  # Auto-clean old logs
    )

    # Ensure some content is written immediately
    advanced_logger.info("Advanced features test started")

    # 6.2 Create another logger with different settings
    new_instance = create_logger(
        name="advanced_new",
        log_path="./logs",
        subdirectory="example_6_advanced_new",
        name_format="{year}-{month}-{day}_{name}.log"  # Custom format
    )

    advanced_logger.info("Message from original advanced logger")
    new_instance.info("Message from new advanced logger instance")

    # 6.3 Usage in multi-threaded environment
    def thread_function(thread_id):
        # Create a logger bound with thread ID for each thread
        thread_logger = advanced_logger.bind(thread_id=thread_id)
        thread_logger.info(f"Thread {thread_id} started")
        time.sleep(random.random())
        thread_logger.info(f"Thread {thread_id} processing data")
        time.sleep(random.random())
        thread_logger.info(f"Thread {thread_id} completed")

    # Create and start multiple threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=thread_function, args=(f"T{i}",))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # 6.4 Conditional logging with different formats
    for i in range(5):
        if i % 2 == 0:
            advanced_logger.opt(colors=True).info(f"<green>Processing item {i}: Success</green>")
        else:
            advanced_logger.opt(colors=True).warning(
                f"<yellow>Processing item {i}: Skipped</yellow>"
            )

    # 6.5 Simulate errors and exception capture
    try:
        advanced_logger.info("Attempting an operation that may fail")
        # Intentionally cause an error
        result = 100 / 0
    except Exception as e:
        # Capture and log exception with stack trace
        advanced_logger.opt(exception=True).error(f"Operation failed: {str(e)}")

    # 6.6 ASCII block with different color combinations - Use new_instance to avoid log mixing
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
    for color in colors:
        new_instance.ascii_block(
            title=f"{color.upper()} Color Example",
            message_list=[
                f"This is a block example using {color} color",
                f"Different colors can be used to distinguish different types of messages",
                f"The current color used is: {color}",
            ],
            ascii_header=color.upper(),
            border_style=color,
        )

    return advanced_logger, new_instance


def main():
    """Run all examples"""
    print("\n===== pretty_loguru Detailed Usage Examples =====\n")
    print("Logs will be saved to ./logs directory (for file-enabled loggers)\n")

    # Run each example
    example_1_basic_usage()
    example_2_multiple_loggers()
    example_3_special_formats()
    example_4_output_targets()
    example_5_integrations()
    example_6_advanced_features()

    print("\n\n===== All examples executed =====")
    print("Please check the log files in the ./logs directory")


if __name__ == "__main__":
    main()
