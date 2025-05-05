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
        def detailed_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 產生新的時間戳
            new_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            # 根據 LOG_NAME_FORMATS["detailed"] = "[{component_name}]{date}_{time}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用詳細格式
            new_name = f"[{component_name}]{new_timestamp}.log"
            new_path = directory / new_name
            
            # 如果新檔名已存在，在時間戳後加上數字
            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{new_timestamp}.{counter}.log"
                new_path = directory / new_name
                counter += 1
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return detailed_rename_log
    
    
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
        def simple_rename_log(filepath: str) -> str:
            path = Path(filepath)
            directory = path.parent
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 找到下一個可用的數字後綴
            counter = 1
            while True:
                new_name = f"{original_name}.{counter}"
                new_path = directory / new_name
                if not new_path.exists():
                    break
                counter += 1
            
            os.rename(filepath, new_path)
            return str(new_path)
        
        return simple_rename_log
    
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
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 產生新的月份標記
            now = datetime.now()
            month_str = now.strftime("%Y%m")
            
            # 根據 LOG_NAME_FORMATS["monthly"] = "[{component_name}]{year}{month}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用月份格式
            new_name = f"[{component_name}]{month_str}.log"
            new_path = directory / new_name
            
            # 如果新檔名已存在，在月份後加上數字
            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{month_str}.{counter}.log"
                new_path = directory / new_name
                counter += 1
            
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
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 產生新的週數標記
            now = datetime.now()
            year = now.year
            week_num = now.isocalendar()[1]
            week_str = f"{year}W{week_num:02d}"
            
            # 根據 LOG_NAME_FORMATS["weekly"] = "[{component_name}]week{week}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用週數格式
            new_name = f"[{component_name}]week{week_str}.log"
            new_path = directory / new_name
            
            # 如果新檔名已存在，在週數後加上數字
            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]week{week_str}.{counter}.log"
                new_path = directory / new_name
                counter += 1
            
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
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 產生新的日期標記
            date_str = datetime.now().strftime("%Y%m%d")
            
            # 根據 LOG_NAME_FORMATS["daily"] = "[{component_name}]{date}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用日期格式
            new_name = f"[{component_name}]{date_str}.log"
            new_path = directory / new_name
            
            # 如果新檔名已存在，在日期後加上數字
            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{date_str}.{counter}.log"
                new_path = directory / new_name
                counter += 1
            
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
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 產生新的日期和小時標記
            now = datetime.now()
            datetime_str = now.strftime("%Y%m%d_%H")
            
            # 根據 LOG_NAME_FORMATS["hourly"] = "[{component_name}]{date}_{hour}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用小時格式
            new_name = f"[{component_name}]{datetime_str}.log"
            new_path = directory / new_name
            
            # 如果新檔名已存在，在時間後加上數字
            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{datetime_str}.{counter}.log"
                new_path = directory / new_name
                counter += 1
            
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
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            # 產生新的日期、小時和分鐘標記
            now = datetime.now()
            datetime_str = now.strftime("%Y%m%d_%H%M")
            
            # 根據 LOG_NAME_FORMATS["minute"] = "[{component_name}]{date}_{hour}{minute}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用分鐘格式
            new_name = f"[{component_name}]{datetime_str}.log"
            new_path = directory / new_name
            
            # 如果新檔名已存在，在時間後加上數字
            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{datetime_str}.{counter}.log"
                new_path = directory / new_name
                counter += 1
            
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
