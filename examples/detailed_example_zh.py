"""
pretty_loguru 詳細使用範例

這個範例展示了各種使用方式和進階功能，包括:
1. 基本的 logger 實例創建與使用
2. 多個 logger 的管理與使用
3. 特殊格式輸出 (區塊、ASCII 藝術、FIGlet)
4. 不同輸出目標 (控制台、文件)
5. 與 FastAPI/Uvicorn 的整合
6. 進階配置與自定義
"""

import sys
from pathlib import Path

# 提前處理載入路徑選擇
使用本地函式庫 = input("是否要載入全域函式庫？ [Y/n]: ").strip().lower()
if 使用本地函式庫 in {"no", "n"}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    print("將使用本地函式庫。\n")
else:
    print("將使用全域函式庫。\n")

import time
time.sleep(0.8)
import random
import threading


# 導入 pretty_loguru 模塊
from pretty_loguru import (
    # 工廠函數和預配置 logger
    create_logger,
    default_logger,
    get_logger,
    list_loggers,
    configure_logger,
    # logger_start,
    # 特殊功能函數
    print_block,
    print_ascii_header,
    print_ascii_block,
    is_ascii_only,
    # 配置相關
    LOG_PATH,
    LoggerConfig,
    # 整合相關
    configure_uvicorn,
    LOGGER_FORMAT,
)

# 檢查是否有 FIGlet 支援
try:
    from pretty_loguru import print_figlet_header, print_figlet_block, get_figlet_fonts

    _has_figlet = True
except ImportError:
    _has_figlet = False

# 檢查是否有 FastAPI 支援
try:
    from pretty_loguru import setup_fastapi_logging

    _has_fastapi = True
except ImportError:
    _has_fastapi = False

logger = default_logger()  # 獲取默認 logger 實例


def example_1_basic_usage():
    """基本使用方式範例 (已修正 KeyError，綁定後才套用 custom_fmt，並在後續 restore)"""
    print("\n--- 範例 1: 基本使用方式 ---\n")

    # 1.0 載入或創建配置
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

    # 1.1 建立 logger（使用預設 format）
    app_logger = create_logger(
        name="app",
        # service_tag="example_app",
        subdirectory="example_1_basic",
        log_name_preset="daily",
        level=config.level,
        rotation=config.rotation,
        log_path=config.log_path,
    )

    # 1.2 無需 user_id 的日誌測試 (涵蓋各級別)
    app_logger.debug("這是一條調試訊息，用於開發時查看詳細資訊")
    app_logger.info("這是一條資訊訊息，記錄正常的程序運行情況")
    app_logger.success("這是一條成功訊息，表示操作已成功完成")
    app_logger.warning("這是一條警告訊息，提示可能的問題或異常情況")
    app_logger.error("這是一條錯誤訊息，表示程序遇到錯誤但可以繼續運行")
    app_logger.critical("這是一條嚴重錯誤訊息，通常表示程序無法繼續運行")

    # 1.3 綁定 user_id / session_id
    user_logger = app_logger.bind(user_id="12345", session_id="abc-xyz-123")

    # 1.4 僅對 user_logger 套用 custom_fmt
    custom_fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}{process}</level> | "
        "<cyan>{extra[folder]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
        " | <yellow>user={extra[user_id]}</yellow> "
        "<magenta>session={extra[session_id]}</magenta>"
    )

    configure_logger(
        level=config.level,
        log_path=config.log_path,
        rotation=config.rotation,
        subdirectory="example_1_basic",
        logger_instance=user_logger,
        service_tag="example_app",
        component_name="user_logger",
        isolate_handlers=True,
        logger_format=custom_fmt,
    )

    # 1.5 用 user_logger 輸出（這兩條都有 user_id/session_id，不會報 KeyError）
    user_logger.info("用戶已登入系統")
    user_logger.warning("用戶嘗試訪問受限資源")

    # 1.6 恢復原始 format，供後續 app_logger 或 global logger 使用
    configure_logger(
        level=config.level,
        log_path=config.log_path,
        rotation=config.rotation,
        subdirectory="example_1_basic",
        logger_instance=app_logger,
        service_tag="example_app",
        isolate_handlers=True,
        # logger_format=LOGGER_FORMAT,  # 恢復預設
    )

    # 1.7 測試全域 logger (原 default_logger)
    logger.info("這條訊息來自全域 default_logger")

    # 1.8 列出所有 logger，也不會報錯
    all_loggers = list_loggers()
    app_logger.info(f"已註冊的所有 logger: {all_loggers}")

    # 1.9 額外測試：ANSI 顏色支持
    app_logger.opt(colors=True).info("這是一條帶有<green>顏色</green>的<red>訊息</red>")

    # 1.10 重複使用已創建的 logger
    same_logger = get_logger("app")  # 返回相同的實例
    if same_logger:
        same_logger.info("這條訊息來自重複獲取的相同 logger 實例")
    else:
        app_logger.warning("無法重複獲取相同的 logger 實例")

    # 1.11 使用默認 logger
    default_logger().info("這條訊息來自默認的 logger 實例")

    # 1.12 向後兼容的全域 logger
    logger.info("這條訊息來自全域 logger (向後兼容)")

    # 1.13 使用 LoggerConfig 進行配置管理示例
    new_config = LoggerConfig(
        level="INFO", rotation="10 KB", log_path=Path.cwd() / "logs" 
    )
    app_logger.info(f"Logger 配置: {new_config.to_dict()}")
    # 將新配置保存到一個範例路徑
    example_path = Path.cwd() / "logs" / "logger_config_example.json"
    new_config.save_to_file(example_path)
    app_logger.info(f"Logger 配置已保存到: {example_path}")

    return app_logger


def example_2_multiple_loggers():
    """多個 logger 實例的管理與使用範例"""
    print("\n--- 範例 2: 多個 logger 實例 ---\n")

    # 2.1 為不同組件創建不同的 logger
    auth_logger = create_logger(
        name="auth_logger",  # 使用更明確的名稱
        service_tag="auth_service",
        subdirectory="example_2_services/auth",  # 每個服務專用子目錄
    )

    db_logger = create_logger(
        name="db_logger",  # 使用更明確的名稱
        service_tag="database_service",
        subdirectory="example_2_services/db",  # 每個服務專用子目錄
        log_name_preset="hourly",
    )

    api_logger = create_logger(
        name="api_logger",  # 使用更明確的名稱
        service_tag="api_service",
        subdirectory="example_2_services/api",  # 每個服務專用子目錄
    )

    # 2.2 在不同組件中使用對應的 logger
    auth_logger.info("認證服務已啟動")
    db_logger.info("數據庫連接池已初始化，連接數: 10")
    api_logger.info("API 服務已啟動，監聽端口: 8000")

    # 2.3 在異常情況下記錄相關訊息
    try:
        # 模擬資料庫操作錯誤
        if random.random() > 0.5:
            raise Exception("數據庫連接失敗")
        db_logger.success("數據庫查詢成功")
    except Exception as e:
        db_logger.error(f"數據庫操作出錯: {str(e)}")
        api_logger.error("因數據庫錯誤，API 請求處理失敗")

    # 2.4 在處理用戶請求時記錄相關訊息
    def handle_request(user_id, endpoint):
        # 記錄請求開始
        request_logger = api_logger.bind(
            user_id=user_id, endpoint=endpoint, request_id=f"req-{int(time.time())}"
        )
        request_logger.info(f"收到來自用戶 {user_id} 的請求: {endpoint}")

        # 模擬認證過程
        auth_logger.debug(f"驗證用戶 {user_id} 的權限")

        # 模擬數據庫操作
        db_logger.debug(f"查詢用戶 {user_id} 的資料")

        # 記錄請求結束
        request_logger.info("請求處理完成")

    # 模擬處理幾個請求
    handle_request("user123", "/api/profile")
    handle_request("admin", "/api/users")

    # 2.5 查看所有已註冊的 logger
    all_loggers = list_loggers()
    auth_logger.info(f"已註冊的所有 logger: {all_loggers}")

    return auth_logger, db_logger, api_logger


def example_3_special_formats():
    """特殊格式輸出範例"""
    print("\n--- 範例 3: 特殊格式輸出 ---\n")

    # 創建用於特殊格式的 logger
    format_logger = create_logger(
        name="formats", service_tag="format_demo", subdirectory="example_3_formats"
    )

    # 3.1 使用區塊格式
    format_logger.block(
        title="系統狀態報告",
        message_list=[
            "CPU 使用率: 45%",
            "記憶體使用率: 60%",
            "磁碟空間: 120GB 可用",
            "網路: 正常",
            "服務狀態: 所有服務運行中",
        ],
        border_style="green",
        log_level="INFO",
    )

    # 3.2 使用 ASCII 藝術標題
    format_logger.ascii_header(
        text="WARNING",
        font="block",  # 使用 block 字體
        border_style="yellow",
        log_level="WARNING",
    )

    # 3.3 使用帶有 ASCII 藝術標題的區塊
    format_logger.ascii_block(
        title="系統警報",
        message_list=[
            "檢測到異常流量",
            "時間: 2025-04-28 15:30:45",
            "來源 IP: 192.168.1.100",
            "目標: 認證服務",
            "可能的攻擊類型: 暴力破解",
        ],
        ascii_header="ALERT",
        ascii_font="banner3",  # 使用 banner3 字體
        border_style="red",
        log_level="ERROR",
    )

    # 3.4 直接使用輔助函數 (不通過 logger 實例)
    print_block(
        title="直接使用區塊函數",
        message_list=[
            "這是使用直接函數而非通過 logger 實例",
            "適用於需要快速使用而不創建 logger 的場景",
        ],
        border_style="blue",
        log_level="INFO",
    )

    print_ascii_header(
        text="DIRECT", font="standard", border_style="magenta", log_level="INFO"
    )

    # 3.5 檢查文本是否只包含 ASCII 字符
    text1 = "Hello, World!"
    text2 = "你好，世界！"

    format_logger.info(
        f"'{text1}' 是否只包含 ASCII 字符: {format_logger.is_ascii_only(text1)}"
    )
    format_logger.info(
        f"'{text2}' 是否只包含 ASCII 字符: {format_logger.is_ascii_only(text2)}"
    )
    format_logger.info(
        f"使用全局函數: '{text1}' 是否只包含 ASCII 字符: {is_ascii_only(text1)}"
    )

    # 3.6 使用 FIGlet 藝術 (若可用)
    try:
        if _has_figlet:
            format_logger.info("FIGlet 支援已啟用")

            # 通過 logger 實例使用 FIGlet
            if hasattr(format_logger, "figlet_header"):
                format_logger.figlet_header(
                    text="FIGLET", font="slant", border_style="cyan", log_level="INFO"
                )

                format_logger.figlet_block(
                    title="FIGlet 區塊示例",
                    message_list=[
                        "這是一個使用 FIGlet 藝術的區塊示例",
                        "FIGlet 提供比 ASCII 藝術更多的字體選項",
                    ],
                    figlet_header="DEMO",
                    figlet_font="big",
                    border_style="green",
                    log_level="INFO",
                )

                # 列出可用的 FIGlet 字體
                if hasattr(format_logger, "get_figlet_fonts"):
                    fonts = format_logger.get_figlet_fonts()
                    format_logger.info(f"可用的 FIGlet 字體數量: {len(fonts)}")
                    format_logger.info(f"部分 FIGlet 字體: {list(fonts)[:5]}")

            # 直接使用 FIGlet 輔助函數
            print_figlet_header(
                text="DIRECT", font="standard", border_style="blue", log_level="INFO"
            )
        else:
            format_logger.info("logger 實例不支援 figlet_header 方法")
    except Exception as e:
        format_logger.info(f"FIGlet 標題輸出跳過: {type(e).__name__}")

    return format_logger


def example_4_output_targets():
    """不同輸出目標範例"""
    print("\n--- 範例 4: 不同輸出目標 ---\n")

    # 創建用於測試不同輸出目標的 logger
    target_logger = create_logger(
        name="targets", service_tag="output_targets", subdirectory="example_4_targets"
    )

    # 4.1 標準日誌 (同時輸出到控制台和文件)
    target_logger.info("這條訊息會同時顯示在控制台和寫入到日誌文件")

    # 4.2 僅輸出到控制台
    target_logger.console_info("這條訊息只會顯示在控制台，不會寫入日誌文件")
    target_logger.console_warning("控制台專用警告訊息")
    target_logger.console_error("控制台專用錯誤訊息")

    # 4.3 僅寫入到日誌文件
    target_logger.file_info("這條訊息只會寫入到日誌文件，不會顯示在控制台")
    target_logger.file_warning("文件專用警告訊息")
    target_logger.file_error("文件專用錯誤訊息")

    # 4.4 使用通用目標方法
    target_logger.console("INFO", "通用方法：僅控制台輸出")
    target_logger.file("WARNING", "通用方法：僅文件輸出")

    # 4.5 開發模式日誌 (與控制台日誌功能相同，但更具語義)
    target_logger.dev_info("開發模式資訊 - 用於調試")
    target_logger.dev_debug("更詳細的開發模式調試訊息")

    # 4.6 使用 ASCII 藝術標題指定輸出目標
    target_logger.ascii_header(
        text="CONSOLE",
        font="standard",
        border_style="cyan",
        to_console_only=True,  # 僅輸出到控制台
    )

    target_logger.ascii_header(
        text="FILE",
        font="standard",
        border_style="cyan",
        to_log_file_only=True,  # 僅輸出到日誌文件
    )

    return target_logger


def example_5_integrations():
    """整合功能範例"""
    print("\n--- 範例 5: 整合功能 ---\n")

    # 5.1 創建用於整合示例的 logger
    integration_logger = create_logger(
        name="integrations",
        service_tag="integration_demo",
        subdirectory="example_5_integrations",
    )
    # 5.2 Uvicorn 整合
    integration_logger.info("配置 Uvicorn 使用 Loguru")
    try:
        configure_uvicorn(logger_instance=integration_logger)
        integration_logger.success("Uvicorn 已配置使用 Loguru")
    except ImportError as e:
        integration_logger.warning(f"Uvicorn 整合失敗: {str(e)}")

    # 5.3 FastAPI 整合 (如果可用)
    try:
        if _has_fastapi:
            integration_logger.info("FastAPI 支援已啟用")
            integration_logger.info(
                "在真實的 FastAPI 應用中，可以使用 setup_fastapi_logging 函數"
            )

            # 示例代碼片段
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

            integration_logger.info("FastAPI 整合示例代碼:")
            for line in fastapi_example.strip().split("\n"):
                integration_logger.console_info(f"    {line}")
        else:
            integration_logger.warning(
                "FastAPI 支援未啟用，請安裝 fastapi 套件以啟用此功能"
            )
    except ImportError:
        integration_logger.info("FastAPI 支援未啟用，但不影響其他功能")
    except Exception as e:
        integration_logger.info(f"FastAPI 整合示例跳過: {type(e).__name__}")

    # 5.4 模擬請求處理日誌
    integration_logger.info("模擬 Web 應用請求處理")

    for i in range(3):
        req_id = f"req-{i+1:03d}"
        path = f"/api/items/{random.randint(1, 100)}"
        method = random.choice(["GET", "POST", "PUT", "DELETE"])

        req_logger = integration_logger.bind(
            request_id=req_id, path=path, method=method, client_ip="192.168.1.100"
        )

        start_time = time.time()
        req_logger.info(f"收到 {method} 請求: {path}")

        # 模擬處理時間
        time.sleep(random.random() * 0.2)

        # 模擬不同的響應狀態
        status_code = random.choice([200, 200, 200, 201, 400, 404, 500])
        process_time = time.time() - start_time

        if status_code >= 500:
            req_logger.error(
                f"請求 {req_id} 處理出錯，狀態碼: {status_code}，耗時: {process_time:.3f}s"
            )
        elif status_code >= 400:
            req_logger.warning(
                f"請求 {req_id} 處理完成，客戶端錯誤，狀態碼: {status_code}，耗時: {process_time:.3f}s"
            )
        else:
            req_logger.success(
                f"請求 {req_id} 處理成功，狀態碼: {status_code}，耗時: {process_time:.3f}s"
            )

    return integration_logger


def example_6_advanced_features():
    """進階功能與自定義範例"""
    print("\n--- 範例 6: 進階功能與自定義 ---\n")

    # 6.1 使用自定義配置創建 logger
    advanced_logger = create_logger(
        name="advanced_logger",
        service_tag="advanced_features",
        subdirectory="example_6_advanced",
        log_name_preset="daily",  # 使用預設格式而非自定義格式
        timestamp_format="%Y-%m-%d_%H-%M-%S",
        log_file_settings={
            "rotation": "500 KB",  # 設定輪換大小
            "retention": "1 week",  # 保留時間
            "compression": "zip",  # 壓縮格式
        },
        level="DEBUG",  # 直接設置日誌級別
    )

    # 確保立即寫入一些內容
    advanced_logger.info("進階功能測試開始")

    # 6.2 創建強制新實例
    new_instance = create_logger(
        name="advanced_logger",  # 相同名稱
        service_tag="advanced_new",  # 不同服務名稱
        subdirectory="example_6_advanced_new",  # 使用不同子目錄
        force_new_instance=True,  # 強制創建新實例
    )

    advanced_logger.info("來自原始 advanced logger 的訊息")
    new_instance.info("來自新 advanced logger 實例的訊息")

    # 6.3 多線程環境中的使用
    def thread_function(thread_id):
        # 為每個線程創建綁定了線程 ID 的 logger
        thread_logger = advanced_logger.bind(thread_id=thread_id)
        thread_logger.info(f"線程 {thread_id} 已啟動")
        time.sleep(random.random())
        thread_logger.info(f"線程 {thread_id} 正在處理數據")
        time.sleep(random.random())
        thread_logger.info(f"線程 {thread_id} 已完成")

    # 創建並啟動多個線程
    threads = []
    for i in range(5):
        thread = threading.Thread(target=thread_function, args=(f"T{i}",))
        threads.append(thread)
        thread.start()

    # 等待所有線程完成
    for thread in threads:
        thread.join()

    # 6.4 不同格式的條件日誌
    for i in range(5):
        if i % 2 == 0:
            advanced_logger.opt(colors=True).info(f"<green>處理項目 {i}: 成功</green>")
        else:
            advanced_logger.opt(colors=True).warning(
                f"<yellow>處理項目 {i}: 跳過</yellow>"
            )

    # 6.5 模擬錯誤及異常捕獲
    try:
        advanced_logger.info("嘗試執行可能失敗的操作")
        # 故意製造錯誤
        result = 100 / 0
    except Exception as e:
        # 捕獲並記錄異常和堆疊跟踪
        advanced_logger.opt(exception=True).error(f"操作失敗: {str(e)}")

    # 6.6 ASCII 區塊與不同顏色組合 - 使用 new_instance 避免日誌混合
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
    for color in colors:
        new_instance.ascii_block(
            title=f"{color.upper()} 顏色示例",
            message_list=[
                f"這是一個使用 {color} 顏色的區塊示例",
                f"不同顏色可以用於區分不同類型的訊息",
                f"當前使用的顏色是: {color}",
            ],
            ascii_header=color.upper(),
            border_style=color,
        )

    return advanced_logger, new_instance


def main():
    """執行所有範例"""
    print("\n===== pretty_loguru 詳細使用範例 =====\n")
    print(f"日誌保存路徑: {LOG_PATH}\n")

    # 執行各個範例
    example_1_basic_usage()
    example_2_multiple_loggers()
    example_3_special_formats()
    example_4_output_targets()
    example_5_integrations()
    example_6_advanced_features()

    print("\n\n===== 所有範例已執行完畢 =====")
    print(f"請查看日誌檔案: {LOG_PATH}")


if __name__ == "__main__":
    main()
