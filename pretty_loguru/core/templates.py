"""
配置模板系統

提供預設的配置模板，包含環境配置和輪換配置等。
統一管理所有配置模板，移除"Enhanced"等修飾詞。
"""

from typing import Dict, List, Optional, Any
from .config import LoggerConfig


class ConfigTemplates:
    """配置模板管理系統"""
    
    # 註冊的自定義模板
    _custom_templates: Dict[str, LoggerConfig] = {}
    
    # === 環境配置模板 ===
    @staticmethod
    def development() -> LoggerConfig:
        """開發環境配置"""
        return LoggerConfig(
            level="DEBUG",
            log_path="logs/dev",
            rotation="10 MB",
            retention="7 days",
            use_native_format=True
        )
    
    @staticmethod
    def production() -> LoggerConfig:
        """生產環境配置"""
        import os
        import platform
        
        # 根據系統選擇適當的日誌路徑
        if platform.system() == "Windows":
            log_path = os.path.expanduser("~/AppData/Local/AppLogs")
        else:
            # 在 Unix 系統上，優先使用用戶目錄以避免權限問題
            log_path = os.path.expanduser("~/.local/share/app/logs")
        
        return LoggerConfig(
            level="INFO",
            log_path=log_path,
            rotation="100 MB",
            retention="30 days",
            compression="gzip",
            start_cleaner=True
        )
    
    @staticmethod
    def testing() -> LoggerConfig:
        """測試環境配置"""
        return LoggerConfig(
            level="WARNING",
            log_path="logs/test",
            rotation="5 MB",
            retention="3 days"
        )
    
    @staticmethod
    def debug() -> LoggerConfig:
        """調試配置"""
        return LoggerConfig(
            level="DEBUG",
            log_path="logs/debug",
            rotation="50 MB",
            retention="1 day",
            use_native_format=True
        )
    
    @staticmethod
    def performance() -> LoggerConfig:
        """高效能配置"""
        return LoggerConfig(
            level="ERROR",
            log_path="logs/perf",
            rotation="500 MB",
            retention="7 days",
            compression="gzip"
        )
    
    @staticmethod
    def minimal() -> LoggerConfig:
        """最小配置"""
        return LoggerConfig(
            level="INFO",
            log_path=None,  # 只輸出到控制台
            rotation=None,
            retention=None
        )
    
    # === 轮换配置模板 ===
    @staticmethod
    def detailed() -> LoggerConfig:
        """詳細模式配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("detailed")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    @staticmethod
    def simple() -> LoggerConfig:
        """簡單模式配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("simple")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    @staticmethod
    def daily() -> LoggerConfig:
        """每日轮换配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("daily")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    @staticmethod
    def hourly() -> LoggerConfig:
        """每小時轮换配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("hourly")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    @staticmethod
    def minute() -> LoggerConfig:
        """每分鐘轮换配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("minute")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    @staticmethod
    def weekly() -> LoggerConfig:
        """每週轮换配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("weekly")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    @staticmethod
    def monthly() -> LoggerConfig:
        """每月轮换配置"""
        from .presets import get_preset_config
        preset_config = get_preset_config("monthly")
        return LoggerConfig(
            level="INFO",
            log_path="logs",
            rotation=preset_config["rotation"],
            retention=preset_config["retention"],
            compression=preset_config["compression"]
        )
    
    # === 動態模板管理 ===
    @classmethod
    def register(cls, name: str, config: LoggerConfig) -> None:
        """註冊自定義模板"""
        cls._custom_templates[name] = config
    
    @classmethod
    def get(cls, name: str) -> Optional[LoggerConfig]:
        """獲取模板"""
        # 先檢查自定義模板
        if name in cls._custom_templates:
            return cls._custom_templates[name].clone()
        
        # 檢查內建模板
        if hasattr(cls, name):
            method = getattr(cls, name)
            if callable(method) and not name.startswith('_'):
                return method()
        
        return None
    
    @classmethod
    def list_all(cls) -> List[str]:
        """列出所有可用的模板"""
        # 內建模板
        builtin_templates = [
            name for name in dir(cls) 
            if not name.startswith('_') and callable(getattr(cls, name))
            and name not in ['register', 'get', 'list_all', 'unregister', 'clear']
        ]
        
        # 自定義模板
        custom_templates = list(cls._custom_templates.keys())
        
        return builtin_templates + custom_templates
    
    @classmethod
    def unregister(cls, name: str) -> bool:
        """取消註冊自定義模板"""
        if name in cls._custom_templates:
            del cls._custom_templates[name]
            return True
        return False
    
    @classmethod
    def clear(cls) -> None:
        """清除所有自定義模板"""
        cls._custom_templates.clear()


# 便利函數
def create_config(**kwargs) -> LoggerConfig:
    """創建配置的便利函數"""
    return LoggerConfig(**kwargs)


def config_from_template(template_name: str, **overrides) -> LoggerConfig:
    """從模板創建配置"""
    config = ConfigTemplates.get(template_name)
    if config is None:
        available = ConfigTemplates.list_all()
        raise ValueError(f"未知的配置模板 '{template_name}'，可用的有: {available}")
    
    if overrides:
        config.update(**overrides)
    
    return config


# 向後兼容的別名
config_from_preset = config_from_template