"""
日誌系統功能測試示例
"""
import time
import sys
import os
import random
# 確保本地路徑優先
sys.path.insert(0, r'C:\work\pretty-loguru')

# 驗證一下導入的是哪個模組
import pretty_loguru
print(pretty_loguru.__file__)



# 加入模塊搜索路徑（根據實際路徑調整）
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

# 定義主函數，用於運行所有測試
def main_example():
    try:
        # 先導入日誌模塊
        from pretty_loguru import logger,logger_start, is_ascii_only
        # 初始化日志系统
        process_id = logger_start(folder="logger_test")
        logger.info(f"日誌系統初始化完成，進程ID: {process_id}")
        logger.info("日誌系統功能測試示例")
        
        # 執行各項測試
        test_basic_logging()
        time.sleep(1)
        
        test_block_logging()
        time.sleep(1)
        
        test_ascii_logging()
        time.sleep(1)
        
        test_mock_application()
        
        logger.success("所有測試完成!")
    except Exception as e:
        print(f"初始化日誌系統時發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()


def test_basic_logging():
    """測試基本日誌功能"""
    from pretty_loguru import logger
    
    logger.info("=== 測試基本日誌功能 ===")
    logger.debug("這是一條調試日誌")
    logger.info("這是一條信息日誌")
    logger.success("這是一條成功日誌")
    logger.warning("這是一條警告日誌")
    logger.error("這是一條錯誤日誌")
    logger.critical("這是一條嚴重錯誤日誌")
    logger.info("基本日誌測試完成")


def test_block_logging():
    """測試區塊日誌功能"""
    from pretty_loguru import logger
    
    logger.info("=== 測試區塊日誌功能 ===")
    
    logger.block(
        "系統狀態摘要", 
        [
            "CPU 使用率: 45%",
            "內存使用率: 60%",
            "磁盤空間: 120GB 可用",
            "網絡連接: 正常",
            "服務狀態: 全部運行中"
        ],
        border_style="green",
        log_level="INFO"
    )
    
    logger.block(
        "警告訊息", 
        [
            "檢測到內存使用率增長過快",
            "當前增長率: 5% / 分鐘",
            "預計 30 分鐘後達到警戒線",
            "建議檢查內存洩漏"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    logger.info("區塊日誌測試完成")


def test_ascii_logging():
    """測試 ASCII 藝術日誌功能"""
    from pretty_loguru import logger, is_ascii_only
    
    logger.info("=== 測試 ASCII 藝術日誌功能 ===")
    
    # 測試 ASCII 字符檢查函數
    logger.info("檢查文本是否只包含 ASCII 字符:")
    test_strings = [
        "Hello World",
        "Hello 世界",
        "123-456-789",
        "特殊字符: ©®™",
        "ASCII symbols: !@#$%^&*()"
    ]
    
    for s in test_strings:
        result = is_ascii_only(s)
        logger.info(f"'{s}' 是否只包含 ASCII 字符: {result}")
    
    # 顯示基本 ASCII 藝術標題
    logger.ascii_header(
        "SYSTEM START",
        font="standard",
        border_style="blue",
        log_level="INFO"
    )
    
    # 顯示不同字體的 ASCII 藝術標題
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
            logger.error(f"使用字體 '{font}' 生成 ASCII 藝術失敗: {str(e)}")
    
    # 測試包含非 ASCII 字符的文本
    try:
        logger.ascii_header(
            "ASCII與中文混合",  # 包含非 ASCII 字符
            font="standard",
            border_style="magenta",
            log_level="WARNING"
        )
    except ValueError as e:
        logger.error(f"預期的錯誤: {str(e)}")
    
    # 測試 ASCII 區塊
    logger.ascii_block(
        "系統診斷報告", 
        [
            "檢查時間: " + time.strftime("%Y-%m-%d %H:%M:%S"),
            "系統負載: 正常",
            "安全狀態: 良好",
            "最近錯誤數量: 0",
            "運行時間: 24小時12分鐘"
        ],
        ascii_header="SYSTEM OK",
        ascii_font="small",
        border_style="green",
        log_level="SUCCESS"
    )
    
    logger.info("ASCII 藝術日誌測試完成")


def test_mock_application():
    """模擬實際應用場景"""
    from pretty_loguru import logger
    
    logger.info("=== 模擬實際應用場景 ===")
    
    # 應用啟動
    logger.ascii_header(
        "APP STARTUP",
        font="slant",
        border_style="blue",
        log_level="INFO"
    )
    
    logger.info("正在加載配置...")
    time.sleep(0.5)
    logger.success("配置加載完成")
    
    logger.block(
        "應用配置摘要", 
        [
            "應用名稱: 日誌系統測試",
            "版本: 1.0.0",
            "環境: 開發環境",
            "日誌級別: DEBUG",
            "最大日誌文件大小: 20MB"
        ],
        border_style="cyan",
        log_level="INFO"
    )
    
    logger.info("正在連接資料庫...")
    time.sleep(1)
    
    # 隨機模擬錯誤情況
    if random.random() < 0.3:
        logger.error("資料庫連接失敗")
        logger.ascii_block(
            "錯誤報告", 
            [
                "錯誤類型: 資料庫連接失敗",
                "錯誤碼: DB-5001",
                "失敗原因: 無法解析主機名",
                "嘗試次數: 3",
                "建議措施: 檢查網絡連接和資料庫服務狀態"
            ],
            ascii_header="ERROR",
            ascii_font="doom",
            border_style="red",
            log_level="ERROR"
        )
    else:
        logger.success("資料庫連接成功")
        
        logger.info("正在初始化服務...")
        time.sleep(1.5)
        logger.success("服務初始化完成")
        
        logger.ascii_block(
            "系統就緒", 
            [
                "啟動時間: " + time.strftime("%Y-%m-%d %H:%M:%S"),
                "已註冊模塊: 用戶管理, 授權中心, 資料處理, 報表生成",
                "系統狀態: 運行中",
                "監聽端口: 8080",
                "API 版本: v2"
            ],
            ascii_header="READY",
            ascii_font="block",
            border_style="green",
            log_level="SUCCESS"
        )
        
        # 模擬處理請求
        for i in range(3):
            logger.info(f"接收到請求 #{i+1}")
            time.sleep(0.8)
            logger.success(f"請求 #{i+1} 處理完成")
    
    # 應用關閉
    logger.info("正在關閉服務...")
    time.sleep(1)
    logger.success("服務已安全關閉")
    
    logger.ascii_header(
        "SHUTDOWN",
        font="standard",
        border_style="magenta",
        log_level="INFO"
    )
    
    logger.info("模擬應用場景測試完成")


if __name__ == "__main__":
    main_example()