# pretty_loguru/core/presets.py
"""
日誌預設配置模組

此模組定義了所有預設的日誌配置類型，包括檔名格式、輪換設定、保留時長和重命名函數。
"""

import os
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Dict, Any, Callable

from .config import LOG_NAME_FORMATS  # 導入 LOG_NAME_FORMATS


class PresetType(Enum):
    """日誌預設類型枚舉"""
    DETAILED = auto()  # 預設類型
    SIMPLE = auto()
    MONTHLY = auto()
    WEEKLY = auto()
    DAILY = auto()
    HOURLY = auto()
    MINUTE = auto()


class LogPreset(ABC):
    """日誌預設基類"""
    
    @property
    @abstractmethod
    def rotation(self) -> str:
        """輪換設定"""
        pass
    
    @property
    @abstractmethod
    def retention(self) -> str:
        """保留設定"""
        pass
    
    @property
    @abstractmethod
    def compression(self) -> Optional[Callable]:
        """壓縮/重命名函數"""
        pass
    
    @property
    @abstractmethod
    def name_format(self) -> str:
        """日誌檔名格式"""
        pass
    
    def get_settings(self) -> Dict[str, Any]:
        """取得完整的預設設定"""
        return {
            "rotation": self.rotation,
            "retention": self.retention,
            "compression": self.compression,
            "name_format": self.name_format
        }


class DetailedPreset(LogPreset):
    """詳細模式"""
    
    @property
    def rotation(self) -> str:
        return "20 MB"
    
    @property
    def retention(self) -> str:
        return "30 days"
    
    @property
    def compression(self) -> Optional[Callable]:
        return None
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["detailed"]


class SimplePreset(LogPreset):
    """簡單模式"""
    
    @property
    def rotation(self) -> str:
        return "20 MB"
    
    @property
    def retention(self) -> str:
        return "30 days"
    
    @property
    def compression(self) -> Optional[Callable]:
        return None
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["simple"]

class MonthlyPreset(LogPreset):
    """每月日誌模式"""
    
    @property
    def rotation(self) -> str:
        return "1 month"
    
    @property
    def retention(self) -> str:
        return "1 year"
    
    @property
    def compression(self) -> Optional[Callable]:
        def monthly_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            base_name = path.stem
            
            now = datetime.now()
            month_str = now.strftime("%Y%m")
            
            new_name = f"{month_str}_{base_name}.log"
            new_path = directory / new_name
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return monthly_rename_log
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["monthly"]


class WeeklyPreset(LogPreset):
    """每週日誌模式"""
    
    @property
    def rotation(self) -> str:
        return "monday"  # 每週一輪換
    
    @property
    def retention(self) -> str:
        return "12 weeks"
    
    @property
    def compression(self) -> Optional[Callable]:
        def weekly_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            base_name = path.stem
            
            now = datetime.now()
            year = now.year
            week_num = now.isocalendar()[1]
            week_str = f"{year}W{week_num:02d}"
            
            new_name = f"{week_str}_{base_name}.log"
            new_path = directory / new_name
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return weekly_rename_log
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["weekly"]

class DailyPreset(LogPreset):
    """每日日誌模式"""
    
    @property
    def rotation(self) -> str:
        return "00:00"  # 每天凌晨輪換
    
    @property
    def retention(self) -> str:
        return "30 days"
    
    @property
    def compression(self) -> Optional[Callable]:
        def daily_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            base_name = path.stem
            
            today = datetime.now()
            date_str = today.strftime("%Y%m%d")
            
            # 智能處理檔名（如果已包含日期則保持原樣）
            has_date_pattern = any(
                part.isdigit() and len(part) == 8 and part.startswith('20')
                for part in base_name.split('_')
            )
            
            if has_date_pattern:
                new_name = f"{base_name}.log"
            else:
                new_name = f"{date_str}_{base_name}.log"
            
            new_path = directory / new_name
            
            # 處理檔名衝突
            if new_path.exists():
                timestamp = today.strftime("%H%M%S")
                new_name = f"{date_str}_{base_name}_{timestamp}.log"
                new_path = directory / new_name
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return daily_rename_log
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["daily"]


class HourlyPreset(LogPreset):
    """每小時日誌模式"""
    
    @property
    def rotation(self) -> str:
        return "1 hour"
    
    @property
    def retention(self) -> str:
        return "7 days"
    
    @property
    def compression(self) -> Optional[Callable]:
        def hourly_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            base_name = path.stem
            
            now = datetime.now()
            datetime_str = now.strftime("%Y%m%d_%H00")
            
            # 構建新的檔名
            new_name = f"{datetime_str}_{base_name}.log"
            new_path = directory / new_name
            
            # 處理檔名衝突
            if new_path.exists():
                minute_str = now.strftime("%M")
                new_name = f"{datetime_str}{minute_str}_{base_name}.log"
                new_path = directory / new_name
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return hourly_rename_log
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["hourly"]


class MinutePreset(LogPreset):
    """每分鐘日誌模式"""
    
    @property
    def rotation(self) -> str:
        return "1 minute"
    
    @property
    def retention(self) -> str:
        return "1 day"
    
    @property
    def compression(self) -> Optional[Callable]:
        def minute_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            base_name = path.stem
            
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M")
            
            new_name = f"{timestamp}_{base_name}.log"
            new_path = directory / new_name
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return minute_rename_log
    
    @property
    def name_format(self) -> str:
        return LOG_NAME_FORMATS["minute"]




class PresetFactory:
    """預設配置工廠"""
    
    _presets = {
        PresetType.DETAILED: DetailedPreset,
        PresetType.SIMPLE: SimplePreset,
        PresetType.MONTHLY: MonthlyPreset,
        PresetType.WEEKLY: WeeklyPreset,
        PresetType.DAILY: DailyPreset,
        PresetType.HOURLY: HourlyPreset,
        PresetType.MINUTE: MinutePreset,
    }
    
    @classmethod
    def get_preset(cls, preset_type: PresetType, **kwargs) -> LogPreset:
        """取得指定類型的預設配置"""
        if preset_type not in cls._presets :
            raise ValueError(f"Unknown preset type: {preset_type}")
        
        preset_class = cls._presets[preset_type]
        return preset_class()
    
    @classmethod
    def register_preset(cls, preset_type: PresetType, preset_class: type[LogPreset]):
        """註冊自定義預設配置"""
        cls._presets[preset_type] = preset_class
