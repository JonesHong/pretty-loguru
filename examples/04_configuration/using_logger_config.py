#!/usr/bin/env python3
"""
使用 LoggerConfig 物件的範例

展示如何使用 LoggerConfig 來管理和重用配置。
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pretty_loguru import create_logger, LoggerConfig, ConfigTemplates

def basic_config_usage():
    """基本的 LoggerConfig 使用方式"""
    print("🔧 基本 LoggerConfig 使用")
    print("=" * 60)
    
    # 創建配置物件
    config = LoggerConfig(
        level="INFO",
        log_path="logs/config_example",
        rotation="1 day",
        retention="7 days"
    )
    
    # 使用 config 創建 logger
    logger = create_logger("basic_app", config=config)
    logger.info("使用 LoggerConfig 物件創建的 logger")
    logger.debug("這個不會顯示，因為級別是 INFO")
    
    print(f"\n配置物件：{config}")
    print("✅ 基本使用完成\n")

def config_with_overrides():
    """使用配置物件並覆寫特定參數"""
    print("🔄 配置覆寫範例")
    print("=" * 60)
    
    # 基礎配置
    base_config = LoggerConfig(
        level="INFO",
        rotation="daily",
        retention="30 days"
    )
    
    # 創建多個 logger，每個都有不同的覆寫
    loggers = {
        "api": create_logger("api", config=base_config, log_path="logs/api"),
        "worker": create_logger("worker", config=base_config, log_path="logs/worker", level="DEBUG"),
        "scheduler": create_logger("scheduler", config=base_config, log_path="logs/scheduler", rotation="hourly")
    }
    
    # 測試不同的 logger
    loggers["api"].info("API logger - INFO 級別")
    loggers["worker"].debug("Worker logger - DEBUG 級別（覆寫）")
    loggers["scheduler"].info("Scheduler logger - 每小時輪轉（覆寫）")
    
    print("✅ 配置覆寫完成\n")

def template_usage():
    """使用配置模板"""
    print("📋 配置模板使用")
    print("=" * 60)
    
    # 使用不同的預設模板
    templates = {
        "development": ConfigTemplates.development(),
        "testing": ConfigTemplates.testing(),
        "daily": ConfigTemplates.daily(),
        "hourly": ConfigTemplates.hourly()
    }
    
    for name, config in templates.items():
        print(f"\n{name} 模板配置：")
        print(f"  - Level: {config.level}")
        print(f"  - Rotation: {config.rotation}")
        print(f"  - Retention: {config.retention}")
        
        # 創建 logger（覆寫路徑避免權限問題）
        logger = create_logger(
            f"{name}_logger",
            config=config,
            log_path=f"logs/templates/{name}"
        )
        logger.info(f"使用 {name} 模板的 logger")
    
    print("\n✅ 模板使用完成\n")

def config_management():
    """配置管理和更新"""
    print("⚙️ 配置管理範例")
    print("=" * 60)
    
    # 創建共享配置
    shared_config = LoggerConfig(
        level="INFO",
        log_path="logs/managed",
        rotation="daily"
    )
    
    # 創建多個 logger
    services = ["auth", "payment", "notification"]
    for service in services:
        logger = create_logger(f"{service}_service", config=shared_config)
        logger.info(f"{service} 服務初始化")
    
    print("\n動態更新配置級別到 DEBUG...")
    # 更新配置（會影響所有已附加的 logger）
    shared_config.update(level="DEBUG")
    
    # 應用更新到現有 logger
    for service in services:
        service_name = f"{service}_service"
        if LoggerConfig.logger_exists(service_name):
            shared_config.apply_to(service_name)
            print(f"✅ 已更新 {service_name} 的配置")
    
    print("\n✅ 配置管理完成\n")

def config_inheritance():
    """配置繼承和克隆"""
    print("🧬 配置繼承範例")
    print("=" * 60)
    
    # 基礎配置
    base = LoggerConfig(
        rotation="daily",
        retention="7 days",
        logger_format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    # 克隆並修改
    dev_config = base.clone()
    dev_config.update(level="DEBUG", log_path="logs/inheritance/dev")
    
    prod_config = base.clone()
    prod_config.update(level="INFO", log_path="logs/inheritance/prod", retention="30 days")
    
    # 創建 logger
    dev_logger = create_logger("dev_service", config=dev_config)
    prod_logger = create_logger("prod_service", config=prod_config)
    
    dev_logger.debug("開發環境：DEBUG 訊息")
    prod_logger.info("生產環境：INFO 訊息")
    
    print(f"\n基礎配置：{base}")
    print(f"開發配置：{dev_config}")
    print(f"生產配置：{prod_config}")
    
    print("\n✅ 配置繼承完成\n")

def error_handling():
    """錯誤處理範例"""
    print("❌ 錯誤處理範例")
    print("=" * 60)
    
    config = LoggerConfig(level="INFO")
    
    # 嘗試更新不存在的 logger
    try:
        config.apply_to("non_existent_logger")
    except ValueError as e:
        print(f"✅ 預期的錯誤：{e}")
    
    # 正確的做法：先創建再更新
    logger = create_logger("existing_logger", config=config)
    logger.info("Logger 已創建")
    
    # 現在可以更新了
    config.update(level="DEBUG")
    config.apply_to("existing_logger")
    print("✅ 成功更新現有 logger")
    
    print("\n✅ 錯誤處理完成\n")

def main():
    """執行所有範例"""
    print("🚀 Pretty Loguru - LoggerConfig 使用範例")
    print("=" * 80)
    print()
    
    # 執行各個範例
    basic_config_usage()
    config_with_overrides()
    template_usage()
    config_management()
    config_inheritance()
    error_handling()
    
    print("\n🎉 所有範例執行完成！")
    print("\n關鍵要點：")
    print("1. 使用 create_logger() 搭配 config 參數創建 logger")
    print("2. 可以覆寫 config 中的特定參數")
    print("3. LoggerConfig.apply_to() 只能更新現有 logger")
    print("4. 使用 LoggerConfig.logger_exists() 檢查 logger 是否存在")
    print("5. 使用 clone() 創建配置副本避免相互影響")

if __name__ == "__main__":
    main()