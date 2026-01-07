#!/usr/bin/env python3
"""
Multiple Loggers - 多個 Logger 管理

學習如何管理多個 logger，了解 logger 註冊表和命名策略。
掌握不同模組間的日誌隔離和共享。

運行方式：
    python multiple_loggers.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger, get_logger, list_loggers, unregister_logger

def basic_multiple_loggers():
    """基本多 logger 使用"""
    print("👥 基本多 logger 使用")
    print("-" * 30)
    
    # 創建不同用途的 logger
    app_logger = create_logger("app", log_dir="./logs/basics")
    db_logger = create_logger("database", log_dir="./logs/basics")
    auth_logger = create_logger("auth", log_dir="./logs/basics")
    
    # 模擬應用程序運行
    app_logger.info("應用程序啟動")
    db_logger.info("連接到數據庫")
    auth_logger.info("認證系統初始化")
    
    # 模擬業務流程
    app_logger.info("處理用戶請求")
    auth_logger.success("用戶認證成功")
    db_logger.info("執行數據庫查詢")
    app_logger.success("請求處理完成")
    
    print("✅ 多個 logger 已創建並記錄日誌")

def logger_registry_management():
    """Logger 註冊表管理"""
    print("\n📋 Logger 註冊表管理")
    print("-" * 30)
    
    # 創建一些 logger
    create_logger("service1")
    create_logger("service2") 
    create_logger("service3")
    
    # 列出所有已註冊的 logger
    loggers = list_loggers()
    print(f"目前已註冊的 logger: {loggers}")
    
    # 獲取已存在的 logger
    service1_logger = get_logger("service1")
    if service1_logger:
        service1_logger.info("從註冊表獲取的 logger")
    
    # 嘗試獲取不存在的 logger
    non_exist_logger = get_logger("non_exist")
    print(f"獲取不存在的 logger: {non_exist_logger}")
    
    # 註銷 logger
    result = unregister_logger("service2")
    print(f"註銷 service2 結果: {result}")
    
    # 再次列出 logger
    loggers_after = list_loggers()
    print(f"註銷後的 logger: {loggers_after}")

def hierarchical_loggers():
    """階層式 logger 設計"""
    print("\n🌳 階層式 logger 設計")
    print("-" * 30)
    
    # 創建階層式 logger
    app_logger = create_logger("myapp", log_dir="./logs/basics")
    user_logger = create_logger("myapp.user", log_dir="./logs/basics")
    order_logger = create_logger("myapp.order", log_dir="./logs/basics")
    payment_logger = create_logger("myapp.payment", log_dir="./logs/basics")
    
    # 模擬階層式日誌記錄
    app_logger.info("=== 開始處理訂單 ===")
    
    user_logger.info("驗證用戶身份")
    user_logger.success("用戶驗證通過")
    
    order_logger.info("創建新訂單")
    order_logger.info("計算訂單金額")
    order_logger.success("訂單創建成功")
    
    payment_logger.info("處理付款")
    payment_logger.warning("付款處理中，請稍候")
    payment_logger.success("付款完成")
    
    app_logger.success("=== 訂單處理完成 ===")

def logger_configuration_sharing():
    """Logger 配置共享"""
    print("\n⚙️ Logger 配置共享")
    print("-" * 30)
    
    # 創建具有相同配置的 logger
    common_config = {
        "log_dir": "./logs/basics",
        "preset": "detailed",
        "retention": "1 day"
    }
    
    frontend_logger = create_logger("frontend", **common_config)
    backend_logger = create_logger("backend", **common_config)
    api_logger = create_logger("api", **common_config)
    
    # 記錄不同層次的日誌
    frontend_logger.info("前端頁面加載")
    api_logger.info("API 請求接收")
    backend_logger.info("後端業務處理")
    backend_logger.success("處理完成")
    api_logger.success("API 響應發送")
    frontend_logger.success("頁面渲染完成")

def logger_isolation_demo():
    """Logger 隔離演示"""
    print("\n🔒 Logger 隔離演示")
    print("-" * 30)
    
    # 創建完全隔離的 logger
    error_only_logger = create_logger(
        "errors_only",
        log_dir="./logs/basics",
        # 注意：在實際應用中，您可能想要配置不同的日誌等級
    )
    
    debug_logger = create_logger(
        "debug_info",
        log_dir="./logs/basics"
    )
    
    # 演示不同 logger 記錄不同類型的資訊
    debug_logger.debug("詳細的除錯資訊")
    debug_logger.info("一般資訊")
    
    # 只記錄錯誤
    error_only_logger.error("這是一個錯誤")
    error_only_logger.critical("這是一個嚴重錯誤")
    
    print("✅ 不同 logger 記錄了不同類型的日誌")

def logger_best_practices():
    """Logger 最佳實踐"""
    print("\n💡 Logger 最佳實踐")
    print("-" * 30)
    
    # 1. 使用有意義的名稱
    user_service_logger = create_logger("user_service", log_dir="./logs/basics")
    
    # 2. 為不同環境使用不同的 logger
    dev_logger = create_logger("app_dev", log_dir="./logs/basics")
    prod_logger = create_logger("app_prod", log_dir="./logs/basics")
    
    # 3. 記錄關鍵業務事件
    user_service_logger.info("用戶服務啟動")
    
    # 4. 使用適當的日誌等級
    dev_logger.debug("開發環境：詳細除錯資訊")
    prod_logger.info("生產環境：重要資訊")
    
    # 5. 記錄關鍵參數
    user_id = 12345
    action = "登入"
    user_service_logger.info(f"用戶操作：用戶 {user_id} 執行 {action}")
    
    print("✅ 演示了 logger 使用的最佳實踐")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 多個 Logger 管理範例")
    print("=" * 50)
    
    # 1. 基本多 logger 使用
    basic_multiple_loggers()
    
    # 2. Logger 註冊表管理
    logger_registry_management()
    
    # 3. 階層式 logger 設計
    hierarchical_loggers()
    
    # 4. Logger 配置共享
    logger_configuration_sharing()
    
    # 5. Logger 隔離演示
    logger_isolation_demo()
    
    # 6. Logger 最佳實踐
    logger_best_practices()
    
    print("\n" + "=" * 50)
    print("✅ 多個 Logger 管理範例完成！")
    print("💡 多 Logger 最佳實踐：")
    print("   - 使用有意義的命名")
    print("   - 合理設計 logger 階層")
    print("   - 適當隔離不同模組的日誌")
    print("   - 共享相同的配置以保持一致性")

if __name__ == "__main__":
    main()