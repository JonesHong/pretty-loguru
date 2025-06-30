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


from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, Literal, Callable

from ..types import LogLevelType, LogRotationType, LogPathType


# 日誌相關的全域變數
LOG_LEVEL: LogLevelType = "INFO"
LOG_ROTATION: LogRotationType = "20 MB"
LOG_RETENTION: str = "30 days"
LOG_PATH: Path = Path.cwd() / "logs"
LOGGER_FORMAT: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}{process}</level> | "
    "<cyan>{extra[folder]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Loguru 原生格式，接近 loguru 預設格式
NATIVE_LOGGER_FORMAT: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{file.name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

@dataclass
class LoggerConfig:
    """
    統一的日誌配置類，作為所有 logger 創建的唯一事實來源。
    """
    # --- 核心配置 ---
    name: Optional[str] = None
    level: LogLevelType = LOG_LEVEL
    
    # --- 檔案輸出 (Sink) ---
    log_path: Optional[LogPathType] = None  # 預設不產生檔案，需要明確指定才會寫入檔案
    rotation: Optional[LogRotationType] = LOG_ROTATION
    retention: Optional[str] = LOG_RETENTION
    compression: Optional[Union[str, Callable]] = None
    compression_format: Optional[str] = None
    
    # --- 格式化 ---
    logger_format: Optional[str] = LOGGER_FORMAT
    component_name: Optional[str] = None
    subdirectory: Optional[str] = None
    
    # --- 行為控制 ---
    use_proxy: bool = False
    start_cleaner: bool = False
    use_native_format: bool = False  # 使用 loguru 原生 file:function:line 格式
    
    # --- 內部使用 ---
    # preset 用於載入預設配置，不直接參與 loguru 的 sink 設置
    preset: Optional[str] = field(default=None, metadata={"internal": True})

    def to_dict(self) -> Dict[str, Any]:
        """將配置轉換為字典，方便序列化。"""
        return {
            "name": self.name,
            "level": self.level,
            "log_path": str(self.log_path) if self.log_path else None,
            "rotation": self.rotation,
            "retention": self.retention,
            "compression": self.compression,
            "compression_format": self.compression_format,
            "logger_format": self.logger_format,
            "component_name": self.component_name,
            "subdirectory": self.subdirectory,
            "use_proxy": self.use_proxy,
            "start_cleaner": self.start_cleaner,
            "use_native_format": self.use_native_format,
            "preset": self.preset,
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "LoggerConfig":
        """從字典創建配置實例。"""
        # 過濾掉字典中不存在於 LoggerConfig 字段的鍵
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        return cls(**filtered_dict)

    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """將配置保存到 JSON 文件。"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "LoggerConfig":
        """從 JSON 文件載入配置。"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件 '{file_path}' 不存在")
        import json
        with open(path, "r", encoding="utf-8") as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)
