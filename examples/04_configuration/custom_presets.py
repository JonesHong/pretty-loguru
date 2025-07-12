#!/usr/bin/env python3
"""
Custom Presets - 自訂預設配置

展示如何創建符合特定需求的自訂配置。

運行方式：
    python custom_presets.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import os

def environment_configs():
    """環境配置範例"""
    print("🌍 環境配置範例")
    print("=" * 30)
    
    # 不同環境的配置需求
    configs = {
        "development": {
            "log_path": "./logs/environments/dev",
            "rotation": "5 MB",
            "retention": "3 days"
        },
        "testing": {
            "log_path": "./logs/environments/test",
            "rotation": "10 MB", 
            "retention": "7 days"
        },
        "production": {
            "log_path": "./logs/environments/prod",
            "preset": "daily",
            "retention": "90 days"
        }
    }
    
    for env_name, config in configs.items():
        print(f"\n📋 {env_name} 環境")
        
        # 顯示配置
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        # 創建 logger 並測試
        logger = create_logger(f"app_{env_name}", **config)
        logger.info(f"{env_name} 環境測試日誌")
        
        print(f"   ✅ {env_name} 配置完成")

def service_configs():
    """服務專用配置"""
    print("\n⚙️ 服務專用配置")
    print("=" * 30)
    
    services = {
        "api_gateway": {
            "log_path": "./logs/services/api_gateway",
            "preset": "hourly",
            "retention": "7 days",
            "description": "高頻請求，按小時歸檔"
        },
        "user_service": {
            "log_path": "./logs/services/user_service",
            "preset": "daily", 
            "retention": "30 days",
            "description": "用戶操作，每日歸檔"
        },
        "payment_service": {
            "log_path": "./logs/services/payment_service",
            "preset": "daily",
            "retention": "365 days",
            "description": "金融資料，長期保存"
        }
    }
    
    for service_name, config in services.items():
        description = config.pop('description')
        
        print(f"\n📦 {service_name}")
        print(f"   說明: {description}")
        
        # 顯示配置
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        # 創建服務 logger
        logger = create_logger(service_name, **config)
        logger.info(f"{service_name} 服務測試日誌")
        
        print(f"   ✅ {service_name} 配置完成")

def dynamic_configs():
    """動態配置範例"""
    print("\n📊 動態配置範例")
    print("=" * 30)
    
    # 根據環境變數選擇配置
    def get_config_by_env():
        env = os.getenv('APP_ENV', 'development')
        
        configs = {
            'development': {
                'log_path': './logs/dynamic/dev',
                'rotation': '5 MB',
                'retention': '3 days'
            },
            'production': {
                'log_path': './logs/dynamic/prod',
                'preset': 'daily', 
                'retention': '90 days'
            }
        }
        
        return configs.get(env, configs['development'])
    
    print(f"\n📋 當前環境: {os.getenv('APP_ENV', 'development')}")
    
    # 獲取動態配置
    config = get_config_by_env()
    
    print("   動態配置:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # 創建動態 logger
    logger = create_logger("dynamic_app", **config)
    logger.info("動態配置測試日誌")
    
    print("   ✅ 動態配置完成")

def best_practices():
    """配置最佳實踐"""
    print("\n💡 配置最佳實踐")
    print("=" * 30)
    
    practices = [
        "開發環境: 使用 simple 預設，短保留期間",
        "測試環境: 使用 detailed 預設，中等保留期間",
        "生產環境: 使用 daily 預設，長保留期間",
        "高頻應用: 考慮 hourly 預設，按需求調整",
        "合規需求: 設定適當的保留期間",
        "存儲考量: 平衡檔案大小和保留期間"
    ]
    
    for i, practice in enumerate(practices, 1):
        print(f"   {i}. {practice}")

def main():
    """主函數"""
    print("🎯 Pretty Loguru 自訂預設配置")
    print("=" * 50)
    
    # 1. 環境配置
    environment_configs()
    
    # 2. 服務配置  
    service_configs()
    
    # 3. 動態配置
    dynamic_configs()
    
    # 4. 最佳實踐
    best_practices()
    
    print("\n" + "=" * 50)
    print("📁 檢查以下目錄查看配置效果:")
    print("   - ./logs/environments/")
    print("   - ./logs/services/")
    print("   - ./logs/dynamic/")
    print("\n💡 根據您的需求選擇合適的配置策略")

if __name__ == "__main__":
    main()