"""
pretty_loguru 詳細使用範例

這個範例展示了各種使用方式和進階功能，包括:
1. 基本的 logger 實例創建與使用
2. 多個 logger 的管理與使用
3. 特殊格式輸出 (區塊、ASCII 藝術)
4. 不同輸出目標 (控制台、文件)
5. 與 FastAPI/Uvicorn 的整合
6. 進階配置與自定義
"""
import os
import time
from pathlib import Path
import random
import threading

# 確保本地路徑優先
import sys
sys.path.insert(0, r'C:\work\pretty-loguru')
# 導入 pretty_loguru 模塊
from pretty_loguru import (
    # 工廠函數和預配置 logger
    create_logger, 
    default_logger,
    
    # 向後兼容的全局 logger
    logger, 
    logger_start,
    
    # 特殊功能函數
    print_block,
    print_ascii_header,
    print_ascii_block,
    
    # Uvicorn 整合
    uvicorn_init_config,
    
    # 其他
    log_path,
)


def example_1_basic_usage():
    """基本使用方式範例"""
    print("\n--- 範例 1: 基本使用方式 ---\n")
    
    # 1.1 使用工廠函數創建 logger
    app_logger = create_logger(
        name="app",                    # logger 名稱 (用於在字典中查找)
        service_name="example_app",    # 服務名稱 (用於日誌檔案名稱)
        subdirectory="examples",       # 子目錄 (logs/examples/)
        log_name_preset="daily",       # 使用每日一檔的命名格式
    )
    
    # 1.2 不同級別的日誌記錄
    app_logger.debug("這是一條調試訊息，用於開發時查看詳細資訊")
    app_logger.info("這是一條資訊訊息，記錄正常的程序運行情況")
    app_logger.success("這是一條成功訊息，表示操作已成功完成")
    app_logger.warning("這是一條警告訊息，提示可能的問題或異常情況")
    app_logger.error("這是一條錯誤訊息，表示程序遇到錯誤但可以繼續運行")
    app_logger.critical("這是一條嚴重錯誤訊息，通常表示程序無法繼續運行")
    
    # 1.3 使用上下文綁定添加額外資訊
    user_logger = app_logger.bind(user_id="12345", session_id="abc-xyz-123")
    user_logger.info("用戶已登入系統")
    user_logger.warning("用戶嘗試訪問受限資源")
    
    # 1.4 使用選項設置額外功能
    # colors=True 允許在訊息中使用 ANSI 顏色代碼
    app_logger.opt(colors=True).info(
        "這是一條帶有<green>顏色</green>的<red>訊息</red>"
    )
    
    # 1.5 重複使用已創建的 logger
    same_logger = create_logger(name="app")  # 返回相同的實例
    same_logger.info("這條訊息來自重複獲取的相同 logger 實例")
    
    # 1.6 使用默認 logger
    default_logger.info("這條訊息來自默認的 logger 實例")
    
    # 1.7 向後兼容的全局 logger
    logger.info("這條訊息來自全局 logger (向後兼容)")
    
    return app_logger


def example_2_multiple_loggers():
    """多個 logger 實例的管理與使用範例"""
    print("\n--- 範例 2: 多個 logger 實例 ---\n")
    
    # 2.1 為不同組件創建不同的 logger
    auth_logger = create_logger(
        name="auth",
        service_name="auth_service", 
        subdirectory="services/auth",
        reuse_existing=False  # 確保不重用實例
    )
    
    db_logger = create_logger(
        name="database",
        service_name="database_service", 
        subdirectory="services/db",
        log_name_preset="hourly",  # 每小時一個日誌檔案
        reuse_existing=False  # 確保不重用實例
    )
    
    api_logger = create_logger(
        name="api",
        service_name="api_service", 
        subdirectory="services/api",
        reuse_existing=False  # 確保不重用實例
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
            user_id=user_id,
            endpoint=endpoint,
            request_id=f"req-{int(time.time())}"
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
    
    return auth_logger, db_logger, api_logger


def example_3_special_formats():
    """特殊格式輸出範例"""
    print("\n--- 範例 3: 特殊格式輸出 ---\n")
    
    # 創建用於特殊格式的 logger
    format_logger = create_logger(
        name="formats",
        service_name="format_demo",
        subdirectory="examples/formats"
    )
    
    # 3.1 使用區塊格式
    format_logger.block(
        title="系統狀態報告",
        message_list=[
            "CPU 使用率: 45%",
            "記憶體使用率: 60%",
            "磁碟空間: 120GB 可用",
            "網路: 正常",
            "服務狀態: 所有服務運行中"
        ],
        border_style="green",
        log_level="INFO"
    )
    
    # 3.2 使用 ASCII 藝術標題
    format_logger.ascii_header(
        text="WARNING",
        font="block",  # 使用 block 字體
        border_style="yellow",
        log_level="WARNING"
    )
    
    # 3.3 使用帶有 ASCII 藝術標題的區塊
    format_logger.ascii_block(
        title="系統警報",
        message_list=[
            "檢測到異常流量",
            "時間: 2025-04-28 15:30:45",
            "來源 IP: 192.168.1.100",
            "目標: 認證服務",
            "可能的攻擊類型: 暴力破解"
        ],
        ascii_header="ALERT",
        ascii_font="banner3",  # 使用 banner3 字體
        border_style="red",
        log_level="ERROR"
    )
    
    # 3.4 直接使用輔助函數 (不通過 logger 實例)
    print_block(
        title="直接使用區塊函數",
        message_list=[
            "這是使用直接函數而非通過 logger 實例",
            "適用於需要快速使用而不創建 logger 的場景"
        ],
        border_style="blue",
        log_level="INFO"
    )
    
    print_ascii_header(
        text="DIRECT",
        font="standard",
        border_style="magenta",
        log_level="INFO"
    )
    
    # 3.5 檢查文本是否只包含 ASCII 字符
    text1 = "Hello, World!"
    text2 = "你好，世界！"
    
    format_logger.info(f"'{text1}' 是否只包含 ASCII 字符: {format_logger.is_ascii_only(text1)}")
    format_logger.info(f"'{text2}' 是否只包含 ASCII 字符: {format_logger.is_ascii_only(text2)}")
    
    return format_logger


def example_4_output_targets():
    """不同輸出目標範例"""
    print("\n--- 範例 4: 不同輸出目標 ---\n")
    
    # 創建用於測試不同輸出目標的 logger
    target_logger = create_logger(
        name="targets",
        service_name="output_targets",
        subdirectory="examples/targets"
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
        to_console_only=True  # 僅輸出到控制台
    )
    
    target_logger.ascii_header(
        text="FILE",
        font="standard",
        border_style="cyan",
        to_log_file_only=True  # 僅輸出到日誌文件
    )
    
    return target_logger


def example_5_fastapi_integration():
    """FastAPI/Uvicorn 整合範例"""
    print("\n--- 範例 5: FastAPI/Uvicorn 整合 ---\n")
    
    # 5.1 創建 FastAPI 應用日誌記錄器
    fastapi_logger = create_logger(
        name="fastapi",
        service_name="fastapi_app",
        subdirectory="examples/fastapi"
    )
    
    # 5.2 配置 Uvicorn 使用 Loguru
    # 在真實的 FastAPI 應用中，這應該放在應用啟動前
    uvicorn_init_config()
    
    # 5.3 模擬 FastAPI 應用日誌
    fastapi_logger.info("FastAPI 應用已啟動")
    fastapi_logger.debug("Uvicorn 工作進程 1 已啟動")
    
    # 5.4 模擬請求處理
    def handle_fastapi_request(request_id, path, method):
        req_logger = fastapi_logger.bind(
            request_id=request_id,
            path=path,
            method=method
        )
        
        req_logger.info(f"收到 {method} 請求: {path}")
        req_logger.debug("處理請求中...")
        time.sleep(0.1)  # 模擬處理時間
        req_logger.info(f"請求 {request_id} 處理完成，狀態碼: 200")
    
    # 模擬處理多個請求
    handle_fastapi_request("req-001", "/api/users", "GET")
    handle_fastapi_request("req-002", "/api/auth/login", "POST")
    handle_fastapi_request("req-003", "/api/items/42", "GET")
    
    # 5.5 模擬優雅關閉
    fastapi_logger.info("收到關閉訊號")
    fastapi_logger.info("等待所有連接關閉...")
    fastapi_logger.info("FastAPI 應用已關閉")
    
    return fastapi_logger


def example_6_advanced_features():
    """進階功能與自定義範例"""
    print("\n--- 範例 6: 進階功能與自定義 ---\n")
    
    # 6.1 使用自定義配置創建 logger
    advanced_logger = create_logger(
        name="advanced",
        service_name="advanced_features",  # 這個將被傳遞到 format_log_filename
        subdirectory="examples/advanced",
        log_name_format="{date}_{hour}{minute}_{process_id}.log",  # 修改格式，移除 {service_name}
        timestamp_format="%Y-%m-%d_%H-%M-%S",  # 自定義時間戳格式
        log_file_settings={
            "rotation": "500 KB",     # 設定輪換大小
            "retention": "1 week",    # 保留時間
            "compression": "zip",     # 壓縮格式
        },
        custom_config={
            "level": "DEBUG",         # 自定義日誌級別
        }
    )
    
    # 6.2 創建強制新實例
    new_instance = create_logger(
        name="advanced",              # 相同名稱
        service_name="advanced_new",  # 不同服務名稱
        reuse_existing=False          # 強制創建新實例
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
            advanced_logger.opt(colors=True).info(
                f"<green>處理項目 {i}: 成功</green>"
            )
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
    
    # 6.6 ASCII 區塊與不同顏色組合
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
    for color in colors:
        advanced_logger.ascii_block(
            title=f"{color.upper()} 顏色示例",
            message_list=[
                f"這是一個使用 {color} 顏色的區塊示例",
                f"不同顏色可以用於區分不同類型的訊息",
                f"當前使用的顏色是: {color}"
            ],
            ascii_header=color.upper(),
            border_style=color
        )
    
    return advanced_logger
def main():
    """執行所有範例"""
    print("\n===== pretty_loguru 詳細使用範例 =====\n")
    print(f"日誌保存路徑: {log_path}\n")
    
    # 執行各個範例
    example_1_basic_usage()
    example_2_multiple_loggers()
    example_3_special_formats()
    example_4_output_targets()
    example_5_fastapi_integration()
    example_6_advanced_features()
    
    print("\n\n===== 所有範例已執行完畢 =====")
    print(f"請查看日誌檔案: {log_path}")


if __name__ == "__main__":
    main()
