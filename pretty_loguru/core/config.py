"""
日誌系統配置模組

此模組定義了 Pretty Loguru 的配置常數、默認值和配置結構。
所有配置相關的常數和功能都集中在此模組中，便於集中管理和修改。
"""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, Union, Literal

from ..types import LogLevelType, LogNameFormatType, LogRotationType, LogPathType


# 日誌相關的全域變數
LOG_LEVEL: LogLevelType = "INFO"  # 預設日誌級別
LOG_ROTATION: LogRotationType = 20  # 日誌輪換大小，單位為 MB
LOG_PATH: Path = Path.cwd() / "logs"  # 預設日誌儲存路徑

# 預定義的日誌檔案名格式
LOG_NAME_FORMATS: Dict[str, str] = {
    "default": "[{process_id}]{timestamp}.log",  # 預設格式
    "daily": "{date}_{process_id}.log",  # 每日一檔
    "hourly": "{date}_{hour}_{process_id}.log",  # 每小時一檔
    "minute": "{date}_{hour}{minute}_{process_id}.log",  # 每分鐘一檔
    "simple": "{process_id}.log",  # 簡單格式，只包含進程 ID
    "detailed": "[{process_id}]_{date}_{time}.log",  # 詳細格式，包含日期和時間
}

# 輸出目標類型
OUTPUT_DESTINATIONS: Dict[str, str] = {
    "console_only": "to_console_only",    # 僅顯示在控制台
    "file_only": "to_log_file_only",      # 僅寫入文件 
}


class LogLevelEnum(Enum):
    """日誌級別枚舉類別

    定義了不同的日誌級別，用於設定和過濾日誌輸出。
    """
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# 日誌輸出的格式設定
LOGGER_FORMAT: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}{process}</level> | "
    "<cyan>{extra[folder]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


class LoggerConfig:
    """日誌配置類
    
    此類提供了統一的配置管理，可從環境變數或配置文件中載入配置。
    """
    
    def __init__(
        self,
        level: Optional[LogLevelType] = None,
        rotation: Optional[LogRotationType] = None,
        log_path: Optional[LogPathType] = None,
        logger_format: Optional[str] = None,
        env_prefix: str = "PRETTY_LOGURU_"
    ):
        """初始化日誌配置
        
        Args:
            level: 日誌級別，預設從環境變數或全局默認值獲取
            rotation: 日誌輪換設置，預設從環境變數或全局默認值獲取
            log_path: 日誌路徑，預設從環境變數或全局默認值獲取
            logger_format: 日誌格式，預設從環境變數或全局默認值獲取
            env_prefix: 環境變數前綴，用於區分不同應用的配置
        """
        # 從環境變數或傳入參數中獲取配置值
        self.level = level or os.environ.get(f"{env_prefix}LEVEL", LOG_LEVEL)
        
        # 處理 rotation 的特殊情況
        if rotation is None:
            rotation_env = os.environ.get(f"{env_prefix}ROTATION")
            if rotation_env:
                self.rotation = rotation_env
            else:
                self.rotation = LOG_ROTATION
        else:
            self.rotation = rotation
        
        # 處理日誌路徑
        if log_path is None:
            log_path_env = os.environ.get(f"{env_prefix}PATH")
            if log_path_env:
                self.log_path = Path(log_path_env)
            else:
                self.log_path = LOG_PATH
        else:
            self.log_path = Path(log_path)
        
        # 日誌格式
        self.format = logger_format or os.environ.get(f"{env_prefix}FORMAT", LOGGER_FORMAT)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'LoggerConfig':
        """從字典創建配置實例
        
        Args:
            config_dict: 包含配置值的字典
            
        Returns:
            LoggerConfig: 配置實例
        """
        return cls(
            level=config_dict.get("level"),
            rotation=config_dict.get("rotation"),
            log_path=config_dict.get("log_path"),
            logger_format=config_dict.get("format"),
            env_prefix=config_dict.get("env_prefix", "PRETTY_LOGURU_")
        )
    
    @classmethod
    def from_file(cls, file_path: Union[str, Path], format: Literal["json", "yaml"] = "json") -> 'LoggerConfig':
        """從文件載入配置
        
        Args:
            file_path: 配置文件路徑
            format: 文件格式，支援 "json" 或 "yaml"
            
        Returns:
            LoggerConfig: 配置實例
            
        Raises:
            ValueError: 不支援的文件格式
            FileNotFoundError: 文件不存在
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件 '{file_path}' 不存在")
        
        if format.lower() == "json":
            import json
            with open(path, "r", encoding="utf-8") as f:
                config_dict = json.load(f)
            return cls.from_dict(config_dict)
        
        elif format.lower() == "yaml":
            try:
                import yaml
            except ImportError:
                raise ImportError("使用 YAML 格式需要安裝 PyYAML 套件: pip install pyyaml")
            
            with open(path, "r", encoding="utf-8") as f:
                config_dict = yaml.safe_load(f)
            return cls.from_dict(config_dict)
        
        else:
            raise ValueError(f"不支援的文件格式: {format}，支援的格式為: json, yaml")
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典
        
        Returns:
            Dict[str, Any]: 包含配置值的字典
        """
        return {
            "level": self.level,
            "rotation": self.rotation,
            "log_path": str(self.log_path),
            "format": self.format
        }
    
    def save_to_file(self, file_path: Union[str, Path], format: Literal["json", "yaml"] = "json") -> None:
        """將配置保存到文件
        
        Args:
            file_path: 配置文件路徑
            format: 文件格式，支援 "json" 或 "yaml"
            
        Raises:
            ValueError: 不支援的文件格式
        """
        path = Path(file_path)
        # 確保目錄存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = self.to_dict()
        
        if format.lower() == "json":
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        elif format.lower() == "yaml":
            try:
                import yaml
            except ImportError:
                raise ImportError("使用 YAML 格式需要安裝 PyYAML 套件: pip install pyyaml")
            
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
        
        else:
            raise ValueError(f"不支援的文件格式: {format}，支援的格式為: json, yaml")


# 創建默認配置實例
default_config = LoggerConfig()