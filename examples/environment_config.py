"""
Pretty Loguru 環境配置管理範例

展示如何在不同環境（開發、測試、生產）中配置日誌系統
"""

import os
from enum import Enum
from pathlib import Path
from pretty_loguru import create_logger, LoggerConfig

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

def get_current_environment() -> Environment:
    """從環境變量獲取當前環境"""
    env = os.getenv("APP_ENV", "development").lower()
    try:
        return Environment(env)
    except ValueError:
        print(f"Unknown environment: {env}, defaulting to development")
        return Environment.DEVELOPMENT

def create_environment_logger(name: str, env: Environment = None):
    """根據環境創建適當的日誌配置"""
    if env is None:
        env = get_current_environment()
    
    if env == Environment.DEVELOPMENT:
        # 開發環境：詳細日誌，控制台輸出，快速迭代
        return create_logger(
            name=f"dev_{name}",
            log_path="./logs/dev",
            preset="detailed",
            level="DEBUG",
            subdirectory="development"
        )
    
    elif env == Environment.TESTING:
        # 測試環境：結構化日誌，每小時輪轉
        return create_logger(
            name=f"test_{name}",
            log_path="./logs/test", 
            preset="hourly",
            level="INFO",
            subdirectory="testing"
        )
    
    elif env == Environment.PRODUCTION:
        # 生產環境：性能優化，每日輪轉，錯誤重點關注
        return create_logger(
            name=f"prod_{name}",
            log_path="/var/log/myapp",  # 生產環境路徑
            preset="daily",
            level="WARNING",  # 只記錄警告和錯誤
            subdirectory="production",
            rotation="100 MB",  # 更大的輪轉大小
            retention="30 days",  # 保留30天
            start_cleaner=True  # 自動清理
        )

# === 示例1: 基本環境配置 ===
print("=== 環境配置管理示例 ===\n")

current_env = get_current_environment()
print(f"當前環境: {current_env.value}")

# 創建不同環境的日誌實例
app_logger = create_environment_logger("app", current_env)
api_logger = create_environment_logger("api", current_env)

app_logger.info(f"應用程序在 {current_env.value} 環境中啟動")

# === 示例2: 展示不同環境的日誌行為 ===
print("\n--- 不同環境的日誌行為對比 ---")

def test_logging_behavior(env: Environment):
    """測試不同環境下的日誌行為"""
    logger = create_environment_logger("test", env)
    
    print(f"\n{env.value.upper()} 環境:")
    logger.debug("這是調試信息")      # 只在開發環境顯示
    logger.info("這是一般信息")       # 開發和測試環境顯示  
    logger.warning("這是警告信息")    # 所有環境都顯示
    logger.error("這是錯誤信息")      # 所有環境都顯示

# 測試所有環境
for env in Environment:
    test_logging_behavior(env)

# === 示例3: 使用配置文件管理 ===
print("\n--- 使用配置文件管理 ---")

def create_config_for_environment(env: Environment) -> LoggerConfig:
    """為不同環境創建配置"""
    base_config = {
        "log_path": Path.cwd() / "logs" / env.value
    }
    
    if env == Environment.DEVELOPMENT:
        return LoggerConfig(
            level="DEBUG",
            rotation="10 MB",
            **base_config
        )
    elif env == Environment.TESTING:
        return LoggerConfig(
            level="INFO", 
            rotation="50 MB",
            **base_config
        )
    elif env == Environment.PRODUCTION:
        return LoggerConfig(
            level="WARNING",
            rotation="100 MB", 
            **base_config
        )

# 創建並保存環境配置
for env in Environment:
    config = create_config_for_environment(env)
    config_path = Path(f"config/logger_{env.value}.json")
    config_path.parent.mkdir(exist_ok=True)
    config.save_to_file(config_path)
    print(f"已保存 {env.value} 環境配置: {config_path}")

# === 示例4: 動態配置重載 ===
print("\n--- 動態配置重載 ---")

from pretty_loguru import reinit_logger

# 創建一個帶代理的日誌實例
proxy_logger = create_logger("dynamic_config", use_proxy=True, log_path="./logs")
proxy_logger.info("初始配置日誌")

# 模擬配置變更（比如從配置中心獲取新配置）
print("模擬配置變更...")
reinit_logger(
    "dynamic_config",
    log_path="./logs",
    preset="hourly",  # 變更為每小時輪轉
    level="DEBUG"     # 變更為更詳細的日誌級別
)

proxy_logger.info("重新配置後的日誌")
proxy_logger.debug("現在可以看到調試信息了")

# === 示例5: 條件式日誌記錄 ===
print("\n--- 條件式日誌記錄 ---")

class ConditionalLogger:
    """條件式日誌記錄器"""
    
    def __init__(self, name: str, env: Environment):
        self.logger = create_environment_logger(name, env)
        self.env = env
    
    def debug_if_dev(self, message: str):
        """只在開發環境記錄調試信息"""
        if self.env == Environment.DEVELOPMENT:
            self.logger.debug(message)
    
    def perf_log(self, message: str, execution_time: float):
        """性能日誌：只在執行時間超過閾值時記錄"""
        threshold = {
            Environment.DEVELOPMENT: 0.1,   # 開發環境更敏感
            Environment.TESTING: 0.5,
            Environment.PRODUCTION: 1.0     # 生產環境只關注真正慢的操作
        }
        
        if execution_time > threshold[self.env]:
            self.logger.warning(f"性能警告: {message}, 耗時: {execution_time:.3f}s")
    
    def business_metric(self, event: str, value: float):
        """業務指標日誌"""
        if self.env == Environment.PRODUCTION:
            # 生產環境記錄業務指標
            self.logger.bind(metric=event, value=value).info(f"業務指標: {event} = {value}")

# 使用條件式日誌記錄
conditional = ConditionalLogger("conditional", current_env)
conditional.debug_if_dev("這只會在開發環境顯示")
conditional.perf_log("數據庫查詢", 0.8)
conditional.business_metric("用戶註冊", 1)

# === 示例6: 最佳實踐總結 ===
print("\n--- 最佳實踐總結 ---")

def create_production_ready_logger(service_name: str):
    """創建生產就緒的日誌配置"""
    env = get_current_environment()
    
    logger = create_environment_logger(service_name, env)
    
    # 添加應用程序信息
    logger = logger.bind(
        service=service_name,
        environment=env.value,
        version=os.getenv("APP_VERSION", "unknown")
    )
    
    return logger

# 創建生產就緒的日誌實例
production_logger = create_production_ready_logger("user_service")
production_logger.info("生產就緒的日誌系統已啟動")

print(f"\n=== 環境配置管理示例完成 ===")
print(f"當前運行環境: {current_env.value}")
print("提示: 使用 APP_ENV=production python environment_config.py 來測試生產環境配置")