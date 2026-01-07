#!/usr/bin/env python3
"""
LoggerConfig Usage Examples - 配置模板使用範例

這個範例展示了如何使用 pretty-loguru 的配置模板系統：

1. 創建可重用的 `LoggerConfig`
2. 以相同模板建立多個 logger
3. 透過 `apply_to()` 將 logger 附加到模板，讓 `update()` 能自動同步更新
4. 配置繼承與克隆
5. 配置持久化（save/load）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pretty_loguru import LoggerConfig, config_from_preset, create_config, create_logger
from pretty_loguru.addons import ConfigTemplates

def basic_usage():
    """基本使用範例"""
    print("🎯 基本使用範例")
    print("=" * 50)
    
    # 1. 創建一個配置模板
    web_config = LoggerConfig(
        level="INFO",
        log_dir="logs/web",
        rotation="daily",
        retention="30 days",
        compression="gz",
    )
    
    # 2. 先建立多個 logger（apply_to 只會套用到「已存在」的 logger）
    api_logger = create_logger("api", config=web_config)
    db_logger = create_logger("database", config=web_config)
    cache_logger = create_logger("cache", config=web_config)

    # 3. 將 logger 附加到模板，之後 update() 會自動同步更新
    web_config.apply_to("api", "database", "cache")
    
    # 4. 使用 logger
    api_logger.info("API 服務啟動")
    db_logger.info("資料庫連接建立")
    cache_logger.info("緩存服務準備就緒")
    
    print(f"已附加的 logger: {web_config.get_attached_loggers()}")
    
    # 5. 修改配置 - 所有附加的 logger 會自動更新！
    print("\n🔄 修改配置，自動更新所有 logger")
    web_config.update(level="DEBUG", rotation="100 MB")
    
    # 6. 測試更新後的設定
    api_logger.debug("這個 DEBUG 訊息現在會顯示了")
    db_logger.debug("資料庫查詢詳細資訊")
    
    print("✅ 基本使用完成")


def template_usage():
    """使用預設模板"""
    print("\n\n🏗️ 使用預設模板")
    print("=" * 50)
    
    # 1. 使用預設的開發環境配置
    dev_config = ConfigTemplates.development()
    dev_logger = create_logger("dev_app", config=dev_config)
    dev_config.apply_to("dev_app")
    
    # 2. 使用預設的生產環境配置
    prod_config = ConfigTemplates.production()
    prod_logger = create_logger("prod_app", config=prod_config)
    prod_config.apply_to("prod_app")
    
    # 3. 使用便利函數創建配置
    test_config = config_from_preset("testing")
    test_config.update(level="ERROR")
    test_logger = create_logger("test_app", config=test_config)
    test_config.apply_to("test_app")
    
    dev_logger.debug("開發環境日誌")
    prod_logger.info("生產環境日誌")
    test_logger.error("測試環境錯誤")
    
    print("✅ 模板使用完成")


def advanced_usage():
    """進階使用範例"""
    print("\n\n⚙️ 進階使用範例")
    print("=" * 50)
    
    # 1. 配置繼承
    base_config = LoggerConfig(
        level="INFO",
        rotation="daily",
        retention="30 days"
    )
    
    # API 服務繼承基礎配置並添加特定設定
    api_config = LoggerConfig().inherit_from(
        base_config,
        log_dir="logs/api",
        component_name="api_service"
    )
    
    # 資料庫服務也繼承基礎配置但有不同的路徑
    db_config = LoggerConfig().inherit_from(
        base_config,
        log_dir="logs/database",
        level="DEBUG",  # 資料庫需要更詳細的日誌
        component_name="db_service"
    )
    
    # 2. 套用配置
    api_logger = create_logger("api_service", config=api_config)
    db_logger = create_logger("db_service", config=db_config)
    api_config.apply_to("api_service")
    db_config.apply_to("db_service")
    
    api_logger.info("API 服務使用繼承的配置")
    db_logger.debug("資料庫服務使用繼承並自訂的配置")
    
    # 3. 克隆配置用於測試
    test_api_config = api_config.clone(log_dir="logs/test/api", level="DEBUG")
    test_api_logger = create_logger("test_api", config=test_api_config)
    test_api_config.apply_to("test_api")
    
    test_api_logger.debug("測試用的 API 服務")
    
    print("✅ 進階使用完成")


def dynamic_management():
    """動態配置管理"""
    print("\n\n🔄 動態配置管理")
    print("=" * 50)
    
    # 1. 創建一個配置並附加多個 logger
    app_config = create_config(
        level="INFO",
        log_dir="logs/app",
        rotation="50 MB"
    )
    
    # 2. 先建立多個 logger，再附加到模板
    create_logger("web", config=app_config)
    create_logger("worker", config=app_config)
    create_logger("scheduler", config=app_config)

    loggers = app_config.apply_to("web", "worker", "scheduler")
    print(f"已創建 {len(loggers)} 個 logger")
    
    # 3. 動態調整日誌級別（比如在運行時調試）
    print("\n調整到 DEBUG 級別進行故障排除...")
    app_config.update(level="DEBUG")
    
    # 所有 logger 現在都是 DEBUG 級別
    for logger in loggers:
        logger.debug("現在可以看到 DEBUG 訊息了")
    
    # 4. 調整輪替策略
    print("\n調整輪替策略...")
    app_config.update(rotation="00:00", compression="gz")
    
    # 5. 分離不需要的 logger
    print("\n分離 scheduler logger...")
    app_config.detach("scheduler")
    print(f"剩餘附加的 logger: {app_config.get_attached_loggers()}")
    
    # 6. 再次調整配置，只會影響剩餘的 logger
    app_config.update(level="WARNING")
    
    print("✅ 動態管理完成")


def chaining_example():
    """鏈式調用範例"""
    print("\n\n⛓️ 優雅的鏈式調用")
    print("=" * 50)
    
    # 這就是您想要的優雅 API！（注意：apply_to 需要 logger 已存在）
    elegant_config = ConfigTemplates.production().update(level="DEBUG", compression=None)
    logger = create_logger("elegant_app", config=elegant_config)
    elegant_config.apply_to("elegant_app")
    
    logger.debug("使用鏈式調用創建的 logger")
    
    # 更複雜的鏈式操作
    chain_config = create_config(level="INFO", log_dir="logs/chain")
    create_logger("service1", config=chain_config)
    create_logger("service2", config=chain_config)
    create_logger("service3", config=chain_config)

    (chain_config
     .apply_to("service1", "service2", "service3")
     .update(rotation="hourly")
     .detach("service3")
     .save("configs/chain_config.json"))
    
    print("✅ 鏈式調用完成")


def configuration_persistence():
    """配置持久化"""
    print("\n\n💾 配置持久化")
    print("=" * 50)
    
    # 1. 創建並保存配置
    Path("configs").mkdir(parents=True, exist_ok=True)
    config = ConfigTemplates.development()
    config.update(log_dir="logs/persistent", level="DEBUG")
    config.save("configs/my_app_config.json")
    
    # 2. 載入配置
    loaded_config = LoggerConfig.load("configs/my_app_config.json")
    logger = create_logger("persistent_app", config=loaded_config)
    loaded_config.apply_to("persistent_app")
    
    logger.debug("使用載入的配置")
    
    # 3. 修改並重新保存
    loaded_config.update(retention="14 days").save("configs/updated_config.json")
    
    print("✅ 配置持久化完成")


def microservices_example():
    """微服務配置範例"""
    print("\n\n🏗️ 微服務配置範例")
    print("=" * 50)
    
    # 1. 定義基礎配置
    base_config = LoggerConfig(
        level="INFO",
        rotation="00:00",
        retention="30 days",
        compression="gz",
    )
    
    # 2. 為不同服務創建專用配置
    services = {
        "user-service": base_config.clone(log_dir="logs/user-service"),
        "order-service": base_config.clone(log_dir="logs/order-service"),
        "payment-service": base_config.clone(log_dir="logs/payment-service", level="DEBUG"),
        "notification-service": base_config.clone(log_dir="logs/notification-service")
    }
    
    # 3. 為每個服務創建 logger
    service_loggers = {}
    for service_name, config in services.items():
        service_loggers[service_name] = create_logger(service_name, config=config)
        config.apply_to(service_name)
    
    # 4. 使用服務 logger
    service_loggers["user-service"].info("用戶服務啟動")
    service_loggers["order-service"].info("訂單服務啟動")
    service_loggers["payment-service"].debug("支付服務調試資訊")
    service_loggers["notification-service"].info("通知服務啟動")
    
    # 5. 全域調整（比如在高負載時降低日誌級別）
    print("\n高負載期間，調整所有服務為 WARNING 級別...")
    for config in services.values():
        config.update(level="WARNING")
    
    service_loggers["user-service"].info("這個 INFO 訊息不會顯示")
    service_loggers["payment-service"].warning("這個 WARNING 訊息會顯示")
    
    print("✅ 微服務配置完成")


def main():
    """主函數"""
    print("🎉 LoggerConfig 完整範例")
    print("🎯 展示可重用配置模板與同步更新能力")
    print("=" * 60)
    
    # 運行所有範例
    basic_usage()
    template_usage()
    advanced_usage()
    dynamic_management()
    chaining_example()
    configuration_persistence()
    microservices_example()
    
    print("\n\n🎊 所有範例完成！")
    print("現在您可以：")
    print("1. 創建可重用的配置模板")
    print("2. 套用配置到多個 logger")
    print("3. 動態修改配置並自動更新所有 logger")
    print("4. 使用優雅的鏈式調用")
    print("5. 配置繼承和克隆")
    print("6. 配置持久化")


if __name__ == "__main__":
    main()
