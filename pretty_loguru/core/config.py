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
from typing import Dict, Any, Optional, Union, Literal, Callable, Set
import warnings

from ..types import LogLevelType, LogRotationType, LogPathType


# 日誌相關的全域變數
LOG_LEVEL: LogLevelType = "INFO"
LOG_ROTATION: LogRotationType = "20 MB"
LOG_RETENTION: str = "30 days"
LOG_PATH: Path = Path.cwd() / "logs"
LOGGER_FORMAT: str = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}{process}</level> | "
    "<cyan>{extra[name]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Loguru 原生格式，接近 loguru 預設格式
NATIVE_LOGGER_FORMAT: str = (
    # "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}{process}</level> | "
    "<cyan>{file.name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

@dataclass
class LoggerConfig:
    """
    統一的日誌配置類，支持可重用配置模板和多logger管理
    """
    
    # --- 核心配置 ---
    level: LogLevelType = LOG_LEVEL
    
    # --- 檔案輸出 ---
    log_path: Optional[LogPathType] = None
    rotation: Optional[LogRotationType] = LOG_ROTATION
    retention: Optional[str] = LOG_RETENTION
    compression: Optional[Union[str, Callable]] = None
    compression_format: Optional[str] = None
    
    # --- 格式化 ---
    logger_format: Optional[str] = LOGGER_FORMAT
    component_name: Optional[str] = None
    subdirectory: Optional[str] = None
    
    # --- 行為控制 ---
    start_cleaner: bool = False
    use_native_format: bool = False
    preset: Optional[str] = None
    
    # --- 傳統參數（向後兼容） ---
    name: Optional[str] = field(default=None, metadata={"legacy": True})
    
    # --- 內部管理 ---
    _attached_loggers: Set[str] = field(default_factory=set, init=False, repr=False)
    _config_name: Optional[str] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """初始化後處理"""
        if not hasattr(self, '_attached_loggers'):
            self._attached_loggers = set()
    
    def apply_to(self, *logger_names: str):
        """
        將配置套用到已存在的 logger(s)
        
        Args:
            *logger_names: 要套用配置的 logger 名稱
            
        Returns:
            List[Logger] 或 Logger: 如果只有一個名稱則返回單個 logger
            
        Raises:
            ValueError: 如果指定的 logger 不存在
        """
        from ..factory.creator import reinit_logger, get_logger
        
        loggers = []
        
        for name in logger_names:
            # 檢查 logger 是否已存在
            existing_logger = get_logger(name)
            
            if not existing_logger:
                raise ValueError(
                    f"Logger '{name}' does not exist. "
                    f"Use create_logger('{name}', config=config) to create it first."
                )
            
            # 更新現有 logger
            updated_logger = reinit_logger(
                name=name,
                level=self.level,
                log_path=self.log_path,
                rotation=self.rotation,
                retention=self.retention,
                compression=self.compression,
                compression_format=self.compression_format,
                logger_format=self.logger_format,
                component_name=self.component_name,
                subdirectory=self.subdirectory,
                start_cleaner=self.start_cleaner,
                use_native_format=self.use_native_format,
                preset=self.preset
            )
            loggers.append(updated_logger)
            
            # 追蹤附加的 logger
            self._attached_loggers.add(name)
        
        # 如果只有一個 logger，直接返回而不是列表
        if len(loggers) == 1:
            return loggers[0]
        return loggers
    
    def update(self, **kwargs) -> 'LoggerConfig':
        """
        更新配置並自動套用到所有附加的 logger
        
        Args:
            **kwargs: 要更新的配置參數
            
        Returns:
            self: 支援鏈式調用
        """
        # 更新配置參數
        for key, value in kwargs.items():
            if hasattr(self, key) and not key.startswith('_'):
                setattr(self, key, value)
            else:
                warnings.warn(f"未知的配置參數: {key}")
        
        # 自動更新所有附加的 logger
        if self._attached_loggers:
            self._update_attached_loggers()
        
        return self
    
    def _update_attached_loggers(self):
        """更新所有附加的 logger"""
        from ..factory.creator import reinit_logger
        
        for logger_name in self._attached_loggers.copy():
            try:
                reinit_logger(
                    name=logger_name,
                    level=self.level,
                    log_path=self.log_path,
                    rotation=self.rotation,
                    retention=self.retention,
                    compression=self.compression,
                    compression_format=self.compression_format,
                    logger_format=self.logger_format,
                    component_name=self.component_name,
                    subdirectory=self.subdirectory,
                    use_proxy=self.use_proxy,
                    start_cleaner=self.start_cleaner,
                    use_native_format=self.use_native_format,
                    preset=self.preset
                )
            except Exception as e:
                warnings.warn(f"更新 logger '{logger_name}' 失敗: {e}")
                # 移除失效的 logger
                self._attached_loggers.discard(logger_name)
    
    def detach(self, *logger_names: str) -> 'LoggerConfig':
        """
        從配置中分離指定的 logger
        
        Args:
            *logger_names: 要分離的 logger 名稱
            
        Returns:
            self: 支援鏈式調用
        """
        for name in logger_names:
            self._attached_loggers.discard(name)
        return self
    
    def detach_all(self) -> 'LoggerConfig':
        """分離所有附加的 logger"""
        self._attached_loggers.clear()
        return self
    
    def get_attached_loggers(self) -> Set[str]:
        """獲取所有附加的 logger 名稱"""
        return self._attached_loggers.copy()
    
    def clone(self, **overrides) -> 'LoggerConfig':
        """
        克隆配置並可選擇性覆蓋參數
        
        Args:
            **overrides: 要覆蓋的配置參數
            
        Returns:
            LoggerConfig: 新的配置實例
        """
        # 獲取當前配置
        current_config = self.to_dict()
        
        # 應用覆蓋參數
        current_config.update(overrides)
        
        # 移除內部字段
        filtered_config = {k: v for k, v in current_config.items() if not k.startswith('_')}
        
        return LoggerConfig(**filtered_config)
    
    def inherit_from(self, parent_config: 'LoggerConfig', **overrides) -> 'LoggerConfig':
        """
        從父配置繼承並可選擇性覆蓋參數
        
        Args:
            parent_config: 父配置
            **overrides: 要覆蓋的參數
            
        Returns:
            self: 支援鏈式調用
        """
        # 從父配置複製所有非 None 的值
        for field_name in self.__dataclass_fields__:
            if field_name.startswith('_'):  # 跳過內部字段
                continue
            
            parent_value = getattr(parent_config, field_name)
            if parent_value is not None:
                setattr(self, field_name, parent_value)
        
        # 應用覆蓋參數
        for key, value in overrides.items():
            if hasattr(self, key) and not key.startswith('_'):
                setattr(self, key, value)
        
        return self
    def to_dict(self) -> Dict[str, Any]:
        """將配置轉換為字典，方便序列化。"""
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__
            if not field_name.startswith('_')
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "LoggerConfig":
        """從字典創建配置實例。"""
        # 過濾有效的鍵
        valid_keys = {f for f in cls.__dataclass_fields__ if not f.startswith('_')}
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
    
    def save(self, file_path: Union[str, Path]) -> 'LoggerConfig':
        """保存配置到文件"""
        self.save_to_file(file_path)
        return self
    
    @classmethod
    def load(cls, file_path: Union[str, Path]) -> 'LoggerConfig':
        """從文件載入配置"""
        return cls.from_file(file_path)
    
    @staticmethod
    def logger_exists(name: str) -> bool:
        """
        檢查指定名稱的 logger 是否存在
        
        Args:
            name: logger 名稱
            
        Returns:
            bool: 如果 logger 存在則返回 True
        """
        from ..factory.creator import get_logger
        return get_logger(name) is not None
    
    def __repr__(self) -> str:
        """字符串表示"""
        attached_count = len(self._attached_loggers)
        name_info = f"name={self.name}, " if self.name else ""
        return f"LoggerConfig({name_info}level={self.level}, attached_loggers={attached_count})"
