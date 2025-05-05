# pretty_loguru/core/presets.py
"""
日誌預設配置模組

此模組定義了所有預設的日誌配置類型，包括檔名格式、輪換設定、保留時長和重命名函數。
"""

import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
import re
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
            original_stem = path.stem  # [default_service]20250430-171706
            
            # 取得當下時間
            now_str = datetime.now().strftime("%Y%m%d-%H%M%S")

            # 組合新檔名
            new_name = f"{original_stem}_to_{now_str}.log"
            new_path = directory / new_name

            # 若新檔案已存在，則加數字避免衝突
            counter = 1
            while new_path.exists():
                new_name = f"{original_stem}_to_{now_str}.{counter}.log"
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
            stem = path.stem  # 如：component

            # 找出所有已存在的序號檔案，找到最大序號
            existing_numbers = []
            pattern = re.compile(rf"^{re.escape(stem)}\.(\d+)\.log$")
            for file in directory.glob(f"{stem}.*.log"):
                match = pattern.match(file.name)
                if match:
                    existing_numbers.append(int(match.group(1)))

            next_number = max(existing_numbers, default=0) + 1

            # 建立新檔案名稱
            new_name = f"{stem}.{next_number}.log"
            new_path = directory / new_name

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
            original_name = path.stem

            # 固定使用「上個月」的年月
            last_month = datetime.now() - relativedelta(months=1)
            month_str = last_month.strftime("%Y%m")

            component_name = original_name.split(']')[0].lstrip('[')

            new_name = f"[{component_name}]{month_str}.log"
            new_path = directory / new_name

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
            original_name = path.stem

            # 固定使用「上週」的週數
            last_week = datetime.now() - timedelta(weeks=1)
            year, week_num, _ = last_week.isocalendar()
            week_str = f"{year}W{week_num:02d}"

            component_name = original_name.split(']')[0].lstrip('[')

            new_name = f"[{component_name}]week{week_str}.log"
            new_path = directory / new_name

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
            print(f"filepath: {filepath}")
            path = Path(filepath)
            directory = path.parent
            original_name = path.stem.split('.')[0]  # 取得原始檔名（不含時間戳）
            
            print(f"original_name: {original_name}")
            # 固定使用「昨天」的日期
            date_str = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            print(f"date_str: {date_str}")
            
            # 根據 LOG_NAME_FORMATS["daily"] = "[{component_name}]{date}.log"
            # 提取 component_name 部分
            if original_name.startswith('[') and ']' in original_name:
                component_name = original_name[1:original_name.index(']')]
            else:
                component_name = original_name
            
            # 構建新的檔名，使用「昨天」日期
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
            original_name = path.stem

            # 固定使用「上一小時」
            last_hour = datetime.now() - timedelta(hours=1)
            hour_str = last_hour.strftime("%Y%m%d_%H")

            component_name = original_name.split(']')[0].lstrip('[')

            new_name = f"[{component_name}]{hour_str}.log"
            new_path = directory / new_name

            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{hour_str}.{counter}.log"
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
            original_name = path.stem

            # 固定使用「上一分鐘」
            last_minute = datetime.now() - timedelta(minutes=1)
            minute_str = last_minute.strftime("%Y%m%d_%H%M")

            component_name = original_name.split(']')[0].lstrip('[')

            new_name = f"[{component_name}]{minute_str}.log"
            new_path = directory / new_name

            counter = 1
            while new_path.exists():
                new_name = f"[{component_name}]{minute_str}.{counter}.log"
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
