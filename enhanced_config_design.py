#!/usr/bin/env python3
"""
Enhanced LoggerConfig Design - 增強版配置設計

這個設計讓 LoggerConfig 成為一個可重用的配置模板，
並且能夠直接管理和修改 logger 實例。

理念：
1. LoggerConfig 可以作為模板套用到多個 logger
2. 修改 LoggerConfig 可以自動更新所有使用該配置的 logger
3. 支援配置繼承和擴展
4. 提供優雅的 API，避免醜陋的方法名稱
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any, Set
from pathlib import Path
import weakref
import warnings

# 假設的導入，實際應該從 pretty_loguru 導入
from pretty_loguru.types import LogLevelType, LogRotationType, LogPathType
from pretty_loguru import create_logger, reinit_logger, get_logger

@dataclass
class EnhancedLoggerConfig:
    """
    增強版 LoggerConfig - 可重用的配置模板
    """
    # --- 核心配置 ---
    level: LogLevelType = "INFO"
    
    # --- 檔案輸出 ---
    log_path: Optional[LogPathType] = None
    rotation: Optional[LogRotationType] = "20 MB"
    retention: Optional[str] = "30 days"
    compression: Optional[str] = None
    compression_format: Optional[str] = None
    
    # --- 格式化 ---
    logger_format: Optional[str] = None
    component_name: Optional[str] = None
    subdirectory: Optional[str] = None
    
    # --- 行為控制 ---
    use_proxy: bool = False
    start_cleaner: bool = False
    use_native_format: bool = False
    preset: Optional[str] = None
    
    # --- 內部管理 ---
    _attached_loggers: Set[str] = field(default_factory=set, init=False, repr=False)
    _config_name: Optional[str] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """初始化後處理"""
        if not hasattr(self, '_attached_loggers'):
            self._attached_loggers = set()
    
    def apply_to(self, *logger_names: str) -> List[object]:
        """
        將配置套用到指定的 logger(s)
        
        Args:
            *logger_names: 要套用配置的 logger 名稱
            
        Returns:
            List[EnhancedLogger]: 創建或更新的 logger 實例列表
        """
        loggers = []
        
        for name in logger_names:
            # 檢查 logger 是否已存在
            existing_logger = get_logger(name)
            
            if existing_logger:
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
                    use_proxy=self.use_proxy,
                    start_cleaner=self.start_cleaner,
                    use_native_format=self.use_native_format,
                    preset=self.preset
                )
                loggers.append(updated_logger)
            else:
                # 創建新 logger
                new_logger = create_logger(
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
                    use_proxy=self.use_proxy,
                    start_cleaner=self.start_cleaner,
                    use_native_format=self.use_native_format,
                    preset=self.preset
                )
                loggers.append(new_logger)
            
            # 追蹤附加的 logger
            self._attached_loggers.add(name)
        
        return loggers
    
    def update(self, **kwargs) -> 'EnhancedLoggerConfig':
        """
        更新配置並自動套用到所有附加的 logger
        
        Args:
            **kwargs: 要更新的配置參數
            
        Returns:
            self: 支援鏈式調用
        """
        # 更新配置參數
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                warnings.warn(f"未知的配置參數: {key}")
        
        # 自動更新所有附加的 logger
        if self._attached_loggers:
            self._update_attached_loggers()
        
        return self
    
    def _update_attached_loggers(self):
        """更新所有附加的 logger"""
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
    
    def detach(self, *logger_names: str) -> 'EnhancedLoggerConfig':
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
    
    def detach_all(self) -> 'EnhancedLoggerConfig':
        """分離所有附加的 logger"""
        self._attached_loggers.clear()
        return self
    
    def get_attached_loggers(self) -> Set[str]:
        """獲取所有附加的 logger 名稱"""
        return self._attached_loggers.copy()
    
    def clone(self, **overrides) -> 'EnhancedLoggerConfig':
        """
        克隆配置並可選擇性覆蓋參數
        
        Args:
            **overrides: 要覆蓋的配置參數
            
        Returns:
            EnhancedLoggerConfig: 新的配置實例
        """
        # 獲取當前配置
        current_config = {
            'level': self.level,
            'log_path': self.log_path,
            'rotation': self.rotation,
            'retention': self.retention,
            'compression': self.compression,
            'compression_format': self.compression_format,
            'logger_format': self.logger_format,
            'component_name': self.component_name,
            'subdirectory': self.subdirectory,
            'use_proxy': self.use_proxy,
            'start_cleaner': self.start_cleaner,
            'use_native_format': self.use_native_format,
            'preset': self.preset,
        }
        
        # 應用覆蓋參數
        current_config.update(overrides)
        
        return EnhancedLoggerConfig(**current_config)
    
    def inherit_from(self, parent_config: 'EnhancedLoggerConfig', **overrides) -> 'EnhancedLoggerConfig':
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
            if hasattr(self, key):
                setattr(self, key, value)
        
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__
            if not field_name.startswith('_')
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'EnhancedLoggerConfig':
        """從字典創建配置"""
        valid_keys = {f for f in cls.__dataclass_fields__ if not f.startswith('_')}
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        return cls(**filtered_dict)
    
    def save(self, file_path: Union[str, Path]) -> 'EnhancedLoggerConfig':
        """保存配置到文件"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        
        return self
    
    @classmethod
    def load(cls, file_path: Union[str, Path]) -> 'EnhancedLoggerConfig':
        """從文件載入配置"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"配置文件 '{file_path}' 不存在")
        
        import json
        with open(path, "r", encoding="utf-8") as f:
            config_dict = json.load(f)
        
        return cls.from_dict(config_dict)


# === 預設配置模板 ===

class ConfigTemplates:
    """預設配置模板"""
    
    @staticmethod
    def development() -> EnhancedLoggerConfig:
        """開發環境配置"""
        return EnhancedLoggerConfig(
            level="DEBUG",
            log_path="logs/dev",
            rotation="10 MB",
            retention="7 days",
            use_native_format=True
        )
    
    @staticmethod
    def production() -> EnhancedLoggerConfig:
        """生產環境配置"""
        return EnhancedLoggerConfig(
            level="INFO",
            log_path="/var/log/app",
            rotation="100 MB",
            retention="30 days",
            compression="gzip",
            start_cleaner=True
        )
    
    @staticmethod
    def testing() -> EnhancedLoggerConfig:
        """測試環境配置"""
        return EnhancedLoggerConfig(
            level="WARNING",
            log_path="logs/test",
            rotation="5 MB",
            retention="3 days"
        )
    
    @staticmethod
    def high_performance() -> EnhancedLoggerConfig:
        """高效能配置"""
        return EnhancedLoggerConfig(
            level="ERROR",
            log_path="logs/hp",
            rotation="500 MB",
            retention="7 days",
            compression="gzip",
            use_proxy=True
        )


# === 使用範例 ===

def demonstration():
    """使用範例演示"""
    print("🎯 Enhanced LoggerConfig 使用演示")
    print("=" * 50)
    
    # 1. 創建配置模板
    print("\n1. 創建開發環境配置模板")
    dev_config = ConfigTemplates.development()
    print(f"   開發配置: level={dev_config.level}, path={dev_config.log_path}")
    
    # 2. 套用配置到多個 logger
    print("\n2. 套用配置到多個 logger")
    loggers = dev_config.apply_to("app", "database", "cache")
    print(f"   已創建 {len(loggers)} 個 logger")
    
    # 3. 修改配置，自動更新所有 logger
    print("\n3. 修改配置，自動更新所有 logger")
    dev_config.update(level="INFO", rotation="20 MB")
    print(f"   配置已更新: level={dev_config.level}, rotation={dev_config.rotation}")
    print(f"   附加的 logger: {dev_config.get_attached_loggers()}")
    
    # 4. 克隆配置用於其他用途
    print("\n4. 克隆配置用於生產環境")
    prod_config = dev_config.clone(
        level="ERROR", 
        log_path="/var/log/prod",
        compression="gzip"
    )
    print(f"   生產配置: level={prod_config.level}, path={prod_config.log_path}")
    
    # 5. 配置繼承
    print("\n5. 配置繼承範例")
    api_config = EnhancedLoggerConfig().inherit_from(
        prod_config, 
        component_name="api",
        subdirectory="api_logs"
    )
    print(f"   API 配置: component={api_config.component_name}, subdir={api_config.subdirectory}")
    
    # 6. 分離和重新附加
    print("\n6. 管理 logger 附加關係")
    dev_config.detach("cache")
    print(f"   分離 cache 後: {dev_config.get_attached_loggers()}")
    
    # 7. 配置持久化
    print("\n7. 配置持久化")
    dev_config.save("configs/dev_config.json")
    loaded_config = EnhancedLoggerConfig.load("configs/dev_config.json")
    print(f"   載入的配置: level={loaded_config.level}")
    
    # 8. 鏈式調用
    print("\n8. 鏈式調用範例")
    (ConfigTemplates.production()
     .update(level="DEBUG", compression=None)
     .apply_to("debug_app")
     .save("configs/debug_prod.json"))
    print("   鏈式調用完成")


if __name__ == "__main__":
    demonstration()