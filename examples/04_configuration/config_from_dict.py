#!/usr/bin/env python3
"""
Config from Dictionary - 字典配置

學習如何使用字典來配置 Pretty-Loguru，
掌握不同配置選項的使用方法。

運行方式：
    python config_from_dict.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger

def basic_dict_config():
    """基本字典配置"""
    print("📚 基本字典配置")
    print("-" * 30)
    
    # 基本配置字典
    basic_config = {
        "log_path": "./logs/configuration",
        "preset": "simple",
        "retention": "7 days"
    }
    
    logger = create_logger("basic_dict", **basic_config)
    logger.info("使用基本字典配置創建的 logger")
    logger.success("配置參數已正確應用")

def advanced_dict_config():
    """進階字典配置"""
    print("\n⚙️ 進階字典配置")
    print("-" * 30)
    
    # 進階配置字典
    advanced_config = {
        "log_path": "./logs/configuration", 
        "preset": "detailed",
        "rotation": "10 MB",
        "retention": "30 days"
    }
    
    logger = create_logger("advanced_dict", **advanced_config)
    logger.info("使用進階字典配置創建的 logger")
    logger.info("配置包含輪替、保留和壓縮設定")

def environment_specific_configs():
    """環境特定配置"""
    print("\n🌍 環境特定配置")
    print("-" * 30)
    
    # 開發環境配置
    dev_config = {
        "log_path": "./logs/configuration/dev",
        "preset": "detailed",
        "retention": "1 day"
    }
    
    # 測試環境配置
    test_config = {
        "log_path": "./logs/configuration/test",
        "preset": "simple",
        "retention": "3 days"
    }
    
    # 生產環境配置
    prod_config = {
        "log_path": "./logs/configuration/prod",
        "preset": "daily",
        "retention": "30 days"
    }
    
    # 根據環境創建不同的 logger
    import os
    env = os.getenv("APP_ENV", "dev")  # 默認為開發環境
    
    configs = {
        "dev": dev_config,
        "test": test_config,
        "prod": prod_config
    }
    
    current_config = configs.get(env, dev_config)
    logger = create_logger(f"app_{env}", **current_config)
    
    logger.info(f"應用程序在 {env} 環境中啟動")
    logger.info(f"使用配置：{current_config}")

def modular_config_composition():
    """模組化配置組合"""
    print("\n🧩 模組化配置組合")
    print("-" * 30)
    
    # 基礎配置
    base_config = {
        "log_path": "./logs/configuration",
        "retention": "7 days"
    }
    
    # 開發特定配置
    dev_overrides = {
        "preset": "detailed"
    }
    
    # 生產特定配置
    prod_overrides = {
        "preset": "daily",
        "rotation": "1 day"
    }
    
    # 組合配置
    def merge_configs(*configs):
        """合併多個配置字典"""
        result = {}
        for config in configs:
            result.update(config)
        return result
    
    # 創建開發環境 logger
    dev_config = merge_configs(base_config, dev_overrides)
    dev_logger = create_logger("modular_dev", **dev_config)
    dev_logger.info("開發環境 logger，使用組合配置")
    
    # 創建生產環境 logger
    prod_config = merge_configs(base_config, prod_overrides)
    prod_logger = create_logger("modular_prod", **prod_config)
    prod_logger.info("生產環境 logger，使用組合配置")

def config_validation():
    """配置驗證"""
    print("\n✅ 配置驗證")
    print("-" * 30)
    
    def validate_config(config):
        """驗證配置字典"""
        errors = []
        
        # 檢查必要參數
        if "log_path" not in config:
            errors.append("缺少 log_path 參數")
        
        # 檢查預設類型
        valid_presets = ["simple", "detailed", "daily", "hourly", "minute", "weekly", "monthly"]
        if "preset" in config and config["preset"] not in valid_presets:
            errors.append(f"無效的 preset: {config['preset']}")
        
        # 檢查保留期格式
        if "retention" in config:
            retention = config["retention"]
            if not any(unit in retention for unit in ["day", "week", "month", "year", "hour", "minute"]):
                errors.append(f"無效的 retention 格式: {retention}")
        
        return errors
    
    # 測試有效配置
    valid_config = {
        "log_path": "./logs/configuration",
        "preset": "daily",
        "retention": "30 days"
    }
    
    errors = validate_config(valid_config)
    if not errors:
        logger = create_logger("validated", **valid_config)
        logger.success("配置驗證通過，logger 創建成功")
    else:
        print(f"配置錯誤：{errors}")
    
    # 測試無效配置
    invalid_config = {
        "preset": "invalid_preset",
        "retention": "invalid_retention"
    }
    
    errors = validate_config(invalid_config)
    if errors:
        print(f"發現配置錯誤：{errors}")

def dynamic_config_updates():
    """動態配置更新"""
    print("\n🔄 動態配置更新")
    print("-" * 30)
    
    # 初始配置
    initial_config = {
        "log_path": "./logs/configuration",
        "preset": "simple"
    }
    
    logger = create_logger("dynamic", **initial_config)
    logger.info("使用初始配置創建 logger")
    
    # 模擬配置更新（注意：實際中可能需要重新創建 logger）
    updated_config = {
        "log_path": "./logs/configuration/updated",
        "preset": "detailed",
        "retention": "14 days"
    }
    
    # 創建新的 logger 來演示配置更新
    from pretty_loguru import unregister_logger
    unregister_logger("dynamic")
    
    new_logger = create_logger("dynamic", **updated_config)
    new_logger.info("使用更新後的配置重新創建 logger")
    new_logger.success("配置更新完成")

def config_templates():
    """配置模板"""
    print("\n📋 配置模板")
    print("-" * 30)
    
    # 定義配置模板
    config_templates = {
        "web_app": {
            "log_path": "./logs/web",
            "preset": "daily",
            "retention": "30 days"
        },
        "microservice": {
            "log_path": "./logs/service",
            "preset": "hourly", 
            "retention": "7 days"
        },
        "batch_job": {
            "log_path": "./logs/batch",
            "preset": "simple",
            "retention": "14 days"
        },
        "debug": {
            "log_path": "./logs/debug",
            "preset": "detailed",
            "retention": "1 day"
        }
    }
    
    def create_logger_from_template(name, template_name, overrides=None):
        """從模板創建 logger"""
        if template_name not in config_templates:
            raise ValueError(f"未知的模板：{template_name}")
        
        config = config_templates[template_name].copy()
        if overrides:
            config.update(overrides)
        
        return create_logger(name, **config)
    
    # 使用模板創建不同類型的 logger
    web_logger = create_logger_from_template("web_app", "web_app")
    web_logger.info("Web 應用程序 logger")
    
    service_logger = create_logger_from_template("api_service", "microservice")
    service_logger.info("微服務 logger")
    
    # 使用模板並覆蓋部分配置
    debug_logger = create_logger_from_template(
        "special_debug", 
        "debug",
        {"retention": "2 hours"}  # 覆蓋保留期
    )
    debug_logger.info("特殊除錯 logger，使用自定義保留期")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 字典配置範例")
    print("=" * 50)
    
    # 1. 基本字典配置
    basic_dict_config()
    
    # 2. 進階字典配置
    advanced_dict_config()
    
    # 3. 環境特定配置
    environment_specific_configs()
    
    # 4. 模組化配置組合
    modular_config_composition()
    
    # 5. 配置驗證
    config_validation()
    
    # 6. 動態配置更新
    dynamic_config_updates()
    
    # 7. 配置模板
    config_templates()
    
    print("\n" + "=" * 50)
    print("✅ 字典配置範例完成！")
    print("💡 配置管理最佳實踐：")
    print("   - 使用字典進行結構化配置")
    print("   - 為不同環境準備不同配置")
    print("   - 實施配置驗證機制")
    print("   - 使用模板簡化配置管理")

if __name__ == "__main__":
    main()