#!/usr/bin/env python3
"""
Config from File - 檔案配置

學習如何從 JSON、YAML 等檔案載入配置，
掌握配置檔案的管理和更新。

運行方式：
    python config_from_file.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import json
import os

def create_sample_configs():
    """創建範例配置檔案"""
    print("📄 創建範例配置檔案")
    print("-" * 30)
    
    config_dir = Path("./configs")
    config_dir.mkdir(exist_ok=True)
    
    # 1. JSON 配置檔案
    json_config = {
        "development": {
            "log_dir": "./logs/configuration/dev",
            "preset": "detailed",
            "retention": "1 day"
        },
        "production": {
            "log_dir": "./logs/configuration/prod", 
            "preset": "daily",
            "retention": "30 days"
        },
        "testing": {
            "log_dir": "./logs/configuration/test",
            "preset": "simple",
            "retention": "3 days"
        }
    }
    
    with open(config_dir / "logging.json", "w", encoding="utf-8") as f:
        json.dump(json_config, f, indent=2, ensure_ascii=False)
    
    # 2. 應用特定配置
    app_config = {
        "app_name": "MyApplication",
        "version": "1.0.0",
        "logging": {
            "default": {
                "log_dir": "./logs/app",
                "preset": "daily"
            },
            "modules": {
                "auth": {
                    "log_dir": "./logs/app/auth",
                    "preset": "detailed",
                    "retention": "7 days"
                },
                "api": {
                    "log_dir": "./logs/app/api",
                    "preset": "hourly",
                    "retention": "3 days"
                },
                "database": {
                    "log_dir": "./logs/app/db",
                    "preset": "simple",
                    "retention": "14 days"
                }
            }
        }
    }
    
    with open(config_dir / "app.json", "w", encoding="utf-8") as f:
        json.dump(app_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 配置檔案已創建在 ./configs/ 目錄")

def load_json_config():
    """載入 JSON 配置"""
    print("\n📖 載入 JSON 配置")
    print("-" * 30)
    
    config_file = Path("./configs/logging.json")
    
    if not config_file.exists():
        print("❌ 配置檔案不存在，請先運行 create_sample_configs()")
        return
    
    # 載入配置檔案
    with open(config_file, "r", encoding="utf-8") as f:
        configs = json.load(f)
    
    # 獲取當前環境
    env = os.getenv("ENVIRONMENT", "development")
    
    if env not in configs:
        print(f"❌ 未找到環境 {env} 的配置，使用 development")
        env = "development"
    
    config = configs[env]
    
    # 創建 logger
    logger = create_logger(f"app_{env}", **config)
    logger.info(f"從 JSON 配置檔案載入 {env} 環境配置")
    logger.success(f"配置參數：{config}")

def load_app_config():
    """載入應用配置"""
    print("\n🏗️ 載入應用配置")
    print("-" * 30)
    
    config_file = Path("./configs/app.json")
    
    if not config_file.exists():
        print("❌ 應用配置檔案不存在")
        return
    
    with open(config_file, "r", encoding="utf-8") as f:
        app_config = json.load(f)
    
    # 載入默認日誌配置
    default_config = app_config["logging"]["default"]
    app_logger = create_logger("app_main", **default_config)
    app_logger.info(f"應用程序 {app_config['app_name']} v{app_config['version']} 啟動")
    
    # 載入模組特定配置
    modules_config = app_config["logging"]["modules"]
    
    for module_name, module_config in modules_config.items():
        module_logger = create_logger(f"app_{module_name}", **module_config)
        module_logger.info(f"{module_name} 模組初始化完成")

def config_file_watcher():
    """配置檔案監控（演示概念）"""
    print("\n👀 配置檔案監控")
    print("-" * 30)
    
    config_file = Path("./configs/logging.json")
    
    if not config_file.exists():
        print("❌ 配置檔案不存在")
        return
    
    # 獲取檔案修改時間
    initial_mtime = config_file.stat().st_mtime
    
    logger = create_logger("config_watcher", log_dir="./logs/configuration")
    logger.info(f"開始監控配置檔案：{config_file}")
    logger.info(f"初始修改時間：{initial_mtime}")
    
    # 在實際應用中，這裡會是一個持續運行的監控循環
    current_mtime = config_file.stat().st_mtime
    
    if current_mtime != initial_mtime:
        logger.warning("配置檔案已更新，需要重新載入")
        # 這裡可以實現配置重新載入邏輯
    else:
        logger.info("配置檔案未更改")

def config_validation_from_file():
    """從檔案載入並驗證配置"""
    print("\n✅ 從檔案載入並驗證配置")
    print("-" * 30)
    
    def validate_logging_config(config):
        """驗證日誌配置"""
        errors = []
        
        required_fields = ["log_dir"]
        for field in required_fields:
            if field not in config:
                errors.append(f"缺少必要欄位：{field}")
        
        if "preset" in config:
            valid_presets = ["simple", "detailed", "daily", "hourly", "minute", "weekly", "monthly"]
            if config["preset"] not in valid_presets:
                errors.append(f"無效的 preset：{config['preset']}")
        
        return errors
    
    config_file = Path("./configs/logging.json")
    
    if not config_file.exists():
        print("❌ 配置檔案不存在")
        return
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            configs = json.load(f)
        
        logger = create_logger("validator", log_dir="./logs/configuration")
        logger.success("配置檔案載入成功")
        
        # 驗證每個環境的配置
        for env_name, env_config in configs.items():
            errors = validate_logging_config(env_config)
            if errors:
                logger.error(f"環境 {env_name} 配置驗證失敗：{errors}")
            else:
                logger.success(f"環境 {env_name} 配置驗證通過")
                
    except json.JSONDecodeError as e:
        logger = create_logger("validator_error", log_dir="./logs/configuration")
        logger.error(f"JSON 解析錯誤：{e}")
    except Exception as e:
        logger = create_logger("validator_error", log_dir="./logs/configuration")
        logger.error(f"載入配置檔案時發生錯誤：{e}")

def environment_specific_loading():
    """環境特定載入"""
    print("\n🌍 環境特定載入")
    print("-" * 30)
    
    def load_config_for_environment(env):
        """為特定環境載入配置"""
        config_files = {
            "development": "./configs/logging.json",
            "staging": "./configs/staging.json",  # 可能不存在
            "production": "./configs/logging.json"
        }
        
        config_file = Path(config_files.get(env, "./configs/logging.json"))
        
        if not config_file.exists():
            print(f"⚠️ 環境 {env} 的配置檔案不存在，使用默認配置")
            return {
                "log_dir": f"./logs/{env}",
                "preset": "simple",
                "retention": "7 days"
            }
        
        with open(config_file, "r", encoding="utf-8") as f:
            configs = json.load(f)
        
        return configs.get(env, configs.get("development"))
    
    # 測試不同環境
    environments = ["development", "staging", "production"]
    
    for env in environments:
        try:
            config = load_config_for_environment(env)
            logger = create_logger(f"env_{env}", **config)
            logger.info(f"成功載入 {env} 環境配置")
        except Exception as e:
            print(f"❌ 載入 {env} 環境配置失敗：{e}")

def config_inheritance():
    """配置繼承"""
    print("\n🔗 配置繼承")
    print("-" * 30)
    
    # 創建具有繼承關係的配置檔案
    inheritance_config = {
        "base": {
            "log_dir": "./logs/base",
            "retention": "7 days"
        },
        "development": {
            "inherits": "base",
            "preset": "detailed",
            "log_dir": "./logs/dev"  # 覆蓋父配置
        },
        "production": {
            "inherits": "base",
            "preset": "daily",
            "retention": "30 days"  # 覆蓋父配置
        }
    }
    
    def resolve_inheritance(config_name, configs):
        """解析配置繼承"""
        if config_name not in configs:
            raise ValueError(f"配置 {config_name} 不存在")
        
        config = configs[config_name].copy()
        
        if "inherits" in config:
            parent_name = config.pop("inherits")
            parent_config = resolve_inheritance(parent_name, configs)
            
            # 父配置在前，子配置覆蓋父配置
            result = parent_config.copy()
            result.update(config)
            return result
        
        return config
    
    # 測試配置繼承
    for env in ["development", "production"]:
        try:
            resolved_config = resolve_inheritance(env, inheritance_config)
            logger = create_logger(f"inherited_{env}", **resolved_config)
            logger.info(f"{env} 環境使用繼承配置：{resolved_config}")
        except Exception as e:
            print(f"❌ 解析 {env} 配置繼承失敗：{e}")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 檔案配置範例")
    print("=" * 50)
    
    # 1. 創建範例配置檔案
    create_sample_configs()
    
    # 2. 載入 JSON 配置
    load_json_config()
    
    # 3. 載入應用配置
    load_app_config()
    
    # 4. 配置檔案監控
    config_file_watcher()
    
    # 5. 配置驗證
    config_validation_from_file()
    
    # 6. 環境特定載入
    environment_specific_loading()
    
    # 7. 配置繼承
    config_inheritance()
    
    print("\n" + "=" * 50)
    print("✅ 檔案配置範例完成！")
    print("💡 檔案配置最佳實踐：")
    print("   - 使用 JSON/YAML 格式的配置檔案")
    print("   - 為不同環境準備不同配置檔案")
    print("   - 實施配置檔案驗證")
    print("   - 支援配置繼承以減少重複")

if __name__ == "__main__":
    main()