"""
日誌系統配置模組

此模組定義了 Pretty Loguru 的配置常數、默認值和配置結構。
所有配置相關的常數和功能都集中在此模組中，便於集中管理和修改。
"""

import os
import re
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, Union, Literal

from ..types import LogLevelType, LogNameFormatType, LogRotationType, LogDirType


from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, Literal, Callable, Set, List
import warnings

from ..types import LogLevelType, LogRotationType, LogDirType


class UnsetType:
    """
    表示「未設定」的哨兵物件（sentinel）。

    用途：
    - 與 `None` 區分：`None` 可能是「刻意設為空值」，`UNSET` 則代表「不要覆寫/沿用既有值」。
    - 常用在 `LoggerConfig.update(...)` 這類「部分更新」API。
    """
    __slots__ = ()

    def __repr__(self) -> str:
        """回傳穩定的除錯表示字串（避免印出記憶體位址）。"""
        return "UNSET"


UNSET = UnsetType()


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

_ROTATION_TIME_RE = re.compile(r"^\d{2}:\d{2}$")
_ROTATION_WEEKDAY_RE = re.compile(
    r"^(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$",
    re.IGNORECASE,
)
_DURATION_RE = re.compile(
    r"^\d+\s*(second|minute|hour|day|week|month|year)s?$",
    re.IGNORECASE,
)
_SIZE_RE = re.compile(r"^\d+(\.\d+)?\s*(b|kb|mb|gb)$", re.IGNORECASE)
_RETENTION_FILES_RE = re.compile(r"^\d+\s*files?$", re.IGNORECASE)

@dataclass
class LoggerConfig:
    """
    統一的日誌配置類，支持可重用配置模板和多logger管理
    """
    
    # --- 核心配置 ---
    level: LogLevelType = LOG_LEVEL
    
    # --- 檔案輸出 ---
    log_dir: Optional[LogDirType] = None
    rotation: Optional[LogRotationType] = LOG_ROTATION
    retention: Optional[str] = LOG_RETENTION
    # loguru 的 compression 支援 str（例如 "gz"/"zip"）或 Callable；
    # 這裡保留 bool 以向後兼容（True 會在配置時轉換為預設壓縮格式）。
    compression: Optional[Union[str, bool, Callable]] = None
    compression_format: Optional[str] = None
    
    # --- 格式化 ---
    format: Optional[str] = LOGGER_FORMAT
    component_name: Optional[str] = None
    subdirectory: Optional[str] = None
    
    # --- 行為控制 ---
    start_cleaner: bool = False
    use_native_format: bool = False
    use_proxy: bool = False
    preset: Optional[str] = None
    verbose: bool = False
    strict_validation: bool = True
    cleaner_include_patterns: Optional[List[str]] = None
    cleaner_exclude_patterns: Optional[List[str]] = None

    # --- 輸出格式（便於 ELK / Loki 解析）---
    serialize: bool = False

    # --- 遠端收集（Loki 直推）---
    loki_enabled: bool = False
    loki_base_url: Optional[str] = None
    loki_labels: Optional[Dict[str, str]] = None
    loki_batch_size: int = 50
    loki_flush_interval_seconds: float = 1.0
    loki_timeout_seconds: float = 2.0
    loki_tenant_id: Optional[str] = None
    loki_username: Optional[str] = None
    loki_password: Optional[str] = None
    
    # --- 傳統參數（向後兼容） ---
    name: Optional[str] = field(default=None, metadata={"legacy": True})
    
    # --- 內部管理 ---
    _attached_loggers: Set[str] = field(default_factory=set, init=False, repr=False)
    _config_name: Optional[str] = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """初始化後處理"""
        if not hasattr(self, '_attached_loggers'):
            self._attached_loggers = set()

    def validate(self) -> None:
        """輕量配置驗證，避免錯誤延後爆出"""
        if self.log_dir is not None and not isinstance(self.log_dir, (str, Path)):
            raise TypeError("log_dir must be a str or Path")
        if self.log_dir is not None:
            p = Path(self.log_dir)
            if str(p.name).lower().endswith((".log", ".json", ".ndjson", ".txt")):
                raise ValueError("log_dir must be a directory path, not a file path")
        if self.rotation is not None and not isinstance(self.rotation, (str, int)):
            raise TypeError("rotation must be a str or int")
        if self.retention is not None and not isinstance(self.retention, (str, int)):
            raise TypeError("retention must be a str or int")
        if self.compression is not None and not (
            isinstance(self.compression, (str, bool)) or callable(self.compression)
        ):
            raise TypeError("compression must be a str, bool, callable, or None")
        if self.start_cleaner is not None and not isinstance(self.start_cleaner, bool):
            raise TypeError("start_cleaner must be a bool")
        if self.use_native_format is not None and not isinstance(self.use_native_format, bool):
            raise TypeError("use_native_format must be a bool")
        if self.verbose is not None and not isinstance(self.verbose, bool):
            raise TypeError("verbose must be a bool")
        if self.strict_validation is not None and not isinstance(self.strict_validation, bool):
            raise TypeError("strict_validation must be a bool")
        if self.cleaner_include_patterns is not None:
            if not isinstance(self.cleaner_include_patterns, list) or not all(
                isinstance(item, str) for item in self.cleaner_include_patterns
            ):
                raise TypeError("cleaner_include_patterns must be a list of str")
        if self.cleaner_exclude_patterns is not None:
            if not isinstance(self.cleaner_exclude_patterns, list) or not all(
                isinstance(item, str) for item in self.cleaner_exclude_patterns
            ):
                raise TypeError("cleaner_exclude_patterns must be a list of str")
        if self.serialize is not None and not isinstance(self.serialize, bool):
            raise TypeError("serialize must be a bool")

        if self.loki_enabled is not None and not isinstance(self.loki_enabled, bool):
            raise TypeError("loki_enabled must be a bool")
        if self.loki_base_url is not None and not isinstance(self.loki_base_url, str):
            raise TypeError("loki_base_url must be a str")
        if self.loki_labels is not None:
            if not isinstance(self.loki_labels, dict) or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in self.loki_labels.items()
            ):
                raise TypeError("loki_labels must be a dict[str, str]")
        if not isinstance(self.loki_batch_size, int) or self.loki_batch_size < 1:
            raise TypeError("loki_batch_size must be an int >= 1")
        if not isinstance(self.loki_flush_interval_seconds, (int, float)) or self.loki_flush_interval_seconds < 0:
            raise TypeError("loki_flush_interval_seconds must be a number >= 0")
        if not isinstance(self.loki_timeout_seconds, (int, float)) or self.loki_timeout_seconds <= 0:
            raise TypeError("loki_timeout_seconds must be a number > 0")
        if self.loki_tenant_id is not None and not isinstance(self.loki_tenant_id, str):
            raise TypeError("loki_tenant_id must be a str")
        if self.loki_username is not None and not isinstance(self.loki_username, str):
            raise TypeError("loki_username must be a str")
        if self.loki_password is not None and not isinstance(self.loki_password, str):
            raise TypeError("loki_password must be a str")

    def validate_strict(self) -> None:
        """更嚴格的配置驗證，包含常見格式檢查"""
        self.validate()

        if isinstance(self.rotation, str):
            rotation = self.rotation.strip()
            if not (
                _DURATION_RE.match(rotation)
                or _SIZE_RE.match(rotation)
                or _ROTATION_TIME_RE.match(rotation)
                or _ROTATION_WEEKDAY_RE.match(rotation)
            ):
                raise ValueError(f"rotation format not recognized: '{self.rotation}'")

        if isinstance(self.retention, str):
            retention = self.retention.strip()
            if not (_DURATION_RE.match(retention) or _RETENTION_FILES_RE.match(retention)):
                raise ValueError(f"retention format not recognized: '{self.retention}'")

        if self.loki_enabled and not self.loki_base_url:
            raise ValueError("loki_enabled=True but loki_base_url is not set")
    
    def apply_to(self, *logger_names: str, create_if_missing: bool = True):
        """
        將配置套用到 logger(s)
        
        Args:
            *logger_names: 要套用配置的 logger 名稱
            create_if_missing: logger 不存在時是否自動建立（最新版預設 True）
            
        Returns:
            List[Logger] 或 Logger: 如果只有一個名稱則返回單個 logger
            
        Raises:
            ValueError: 如果指定的 logger 不存在且 create_if_missing=False
        """
        from ..factory.creator import reinit_logger, get_logger, create_logger
        
        loggers = []
        
        for name in logger_names:
            # 檢查 logger 是否已存在
            existing_logger = get_logger(name)
            
            if not existing_logger:
                if not create_if_missing:
                    raise ValueError(
                        f"Logger '{name}' does not exist. "
                        "Pass create_if_missing=True, or call create_logger() first."
                    )
                created_logger = create_logger(name, config=self)
                loggers.append(created_logger)
                self._attached_loggers.add(name)
                continue
            
            # 更新現有 logger
            updated_logger = reinit_logger(
                name=name,
                level=self.level,
                log_dir=self.log_dir,
                rotation=self.rotation,
                retention=self.retention,
                compression=self.compression,
                compression_format=self.compression_format,
                format=self.format,
                component_name=self.component_name,
                subdirectory=self.subdirectory,
                start_cleaner=self.start_cleaner,
                verbose=self.verbose,
                cleaner_include_patterns=self.cleaner_include_patterns,
                cleaner_exclude_patterns=self.cleaner_exclude_patterns,
                strict_validation=self.strict_validation,
                serialize=self.serialize,
                loki_enabled=self.loki_enabled,
                loki_base_url=self.loki_base_url,
                loki_labels=self.loki_labels,
                loki_batch_size=self.loki_batch_size,
                loki_flush_interval_seconds=self.loki_flush_interval_seconds,
                loki_timeout_seconds=self.loki_timeout_seconds,
                loki_tenant_id=self.loki_tenant_id,
                loki_username=self.loki_username,
                loki_password=self.loki_password,
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
    
    def update(
        self,
        *,
        restart_cleaner: bool = False,
        level: Union[LogLevelType, UnsetType] = UNSET,
        log_dir: Union[Optional[LogDirType], UnsetType] = UNSET,
        rotation: Union[Optional[LogRotationType], UnsetType] = UNSET,
        retention: Union[Optional[Union[str, int]], UnsetType] = UNSET,
        compression: Union[Optional[Union[str, bool, Callable]], UnsetType] = UNSET,
        compression_format: Union[Optional[str], UnsetType] = UNSET,
        format: Union[Optional[str], UnsetType] = UNSET,
        component_name: Union[Optional[str], UnsetType] = UNSET,
        subdirectory: Union[Optional[str], UnsetType] = UNSET,
        start_cleaner: Union[bool, UnsetType] = UNSET,
        use_native_format: Union[bool, UnsetType] = UNSET,
        use_proxy: Union[bool, UnsetType] = UNSET,
        preset: Union[Optional[str], UnsetType] = UNSET,
        verbose: Union[bool, UnsetType] = UNSET,
        strict_validation: Union[bool, UnsetType] = UNSET,
        cleaner_include_patterns: Union[Optional[List[str]], UnsetType] = UNSET,
        cleaner_exclude_patterns: Union[Optional[List[str]], UnsetType] = UNSET,
        serialize: Union[bool, UnsetType] = UNSET,
        loki_enabled: Union[bool, UnsetType] = UNSET,
        loki_base_url: Union[Optional[str], UnsetType] = UNSET,
        loki_labels: Union[Optional[Dict[str, str]], UnsetType] = UNSET,
        loki_batch_size: Union[int, UnsetType] = UNSET,
        loki_flush_interval_seconds: Union[float, UnsetType] = UNSET,
        loki_timeout_seconds: Union[float, UnsetType] = UNSET,
        loki_tenant_id: Union[Optional[str], UnsetType] = UNSET,
        loki_username: Union[Optional[str], UnsetType] = UNSET,
        loki_password: Union[Optional[str], UnsetType] = UNSET,
    ) -> 'LoggerConfig':
        """
        更新配置並自動套用到所有附加的 logger
        
        Args:
            restart_cleaner: 是否重啟清理器以套用清理設定
            其餘參數：要更新的配置欄位（採顯式欄位，避免黑盒 `**kwargs`）
            
        Returns:
            self: 支援鏈式調用
        """
        updates = {
            "level": level,
            "log_dir": log_dir,
            "rotation": rotation,
            "retention": retention,
            "compression": compression,
            "compression_format": compression_format,
            "format": format,
            "component_name": component_name,
            "subdirectory": subdirectory,
            "start_cleaner": start_cleaner,
            "use_native_format": use_native_format,
            "use_proxy": use_proxy,
            "preset": preset,
            "verbose": verbose,
            "strict_validation": strict_validation,
            "cleaner_include_patterns": cleaner_include_patterns,
            "cleaner_exclude_patterns": cleaner_exclude_patterns,
            "serialize": serialize,
            "loki_enabled": loki_enabled,
            "loki_base_url": loki_base_url,
            "loki_labels": loki_labels,
            "loki_batch_size": loki_batch_size,
            "loki_flush_interval_seconds": loki_flush_interval_seconds,
            "loki_timeout_seconds": loki_timeout_seconds,
            "loki_tenant_id": loki_tenant_id,
            "loki_username": loki_username,
            "loki_password": loki_password,
        }

        for key, value in updates.items():
            if value is UNSET:
                continue
            setattr(self, key, value)
        
        # 自動更新所有附加的 logger
        if self._attached_loggers:
            self._update_attached_loggers(restart_cleaner=restart_cleaner)
        
        return self
    
    def _update_attached_loggers(self, restart_cleaner: bool = False):
        """更新所有附加的 logger"""
        from ..factory.updater import update_logger_config
        
        for logger_name in self._attached_loggers.copy():
            try:
                # 使用新的更新方法，直接更新現有 logger
                success = update_logger_config(
                    logger_name,
                    self,
                    restart_cleaner=restart_cleaner,
                )
                if not success:
                    warnings.warn(f"更新 logger '{logger_name}' 失敗")
                    self._attached_loggers.discard(logger_name)
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

    def update_from_dict(
        self, overrides: Dict[str, Any], *, restart_cleaner: bool = False
    ) -> "LoggerConfig":
        """
        以 dict 形式更新配置並自動套用到所有附加的 logger。

        適用情境：配置來源是動態 dict（例如讀取 JSON/ENV），而不是在程式碼中顯式列出參數。
        """
        if not isinstance(overrides, dict):
            raise TypeError("overrides must be a dict")

        for key, value in overrides.items():
            if key.startswith("_") or key not in self.__dataclass_fields__:
                raise ValueError(f"未知的配置欄位: {key}")
            setattr(self, key, value)

        if self._attached_loggers:
            self._update_attached_loggers(restart_cleaner=restart_cleaner)

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
