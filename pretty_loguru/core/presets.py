"""
簡化的日誌預設配置模組

按照KISS原則重新設計，使用簡單的配置字典替代複雜的類層次結構。
減少代碼重複，提升可維護性。
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Callable, Literal, List

# 預設類型
PresetType = Literal["detailed", "simple", "daily", "hourly", "minute", "weekly", "monthly"]

# 重命名函數模板
def _create_rename_function(pattern: str) -> Callable:
    """創建日誌重命名函數"""
    def rename_function(filepath: str):
        log_path = Path(filepath)
        current_time = datetime.now()
        
        # 格式化模式替換
        new_name = pattern.format(
            name=log_path.stem.replace('_latest.temp', ''),
            timestamp=current_time.strftime("%Y%m%d-%H%M%S"),
            date=current_time.strftime("%Y%m%d"),
            year=current_time.year,
            month=f"{current_time.month:02d}",
            day=f"{current_time.day:02d}",
            hour=f"{current_time.hour:02d}",
            minute=f"{current_time.minute:02d}",
            week=current_time.isocalendar()[1]
        )
        
        new_path = log_path.parent / f"{new_name}.log"
        if log_path.exists():
            os.rename(str(log_path), str(new_path))
        
        return str(new_path)
    
    return rename_function

# 預設配置定義 - 簡單的字典結構
PRESET_CONFIGS: Dict[PresetType, Dict[str, Any]] = {
    "detailed": {
        "rotation": "20 MB",
        "retention": "30 days", 
        "compression": _create_rename_function("[{name}]{timestamp}"),
        "name_format": "[{component_name}]{timestamp}.log"
    },
    "simple": {
        "rotation": "20 MB",
        "retention": "30 days",
        "compression": None,
        "name_format": "{component_name}.log"
    },
    "daily": {
        "rotation": "1 day",
        "retention": "30 days",
        "compression": _create_rename_function("[{name}]{date}"),
        "name_format": "[{component_name}]daily_latest.temp.log"
    },
    "hourly": {
        "rotation": "1 hour", 
        "retention": "7 days",
        "compression": _create_rename_function("[{name}]{date}_{hour}"),
        "name_format": "[{component_name}]hourly_latest.temp.log"
    },
    "minute": {
        "rotation": "1 minute",
        "retention": "24 hours", 
        "compression": _create_rename_function("[{name}]{date}_{hour}{minute}"),
        "name_format": "[{component_name}]minute_latest.temp.log"
    },
    "weekly": {
        "rotation": "1 week",
        "retention": "12 weeks",
        "compression": _create_rename_function("[{name}]week{week}_{year}"),
        "name_format": "[{component_name}]weekly_latest.temp.log"
    },
    "monthly": {
        "rotation": "1 month",
        "retention": "12 months", 
        "compression": _create_rename_function("[{name}]{year}{month}"),
        "name_format": "[{component_name}]monthly_latest.temp.log"
    }
}


def get_preset_config(preset_type: PresetType) -> Dict[str, Any]:
    """
    獲取預設配置
    
    Args:
        preset_type: 預設類型
        
    Returns:
        Dict[str, Any]: 預設配置字典
        
    Raises:
        ValueError: 當預設類型不存在時
    """
    if preset_type not in PRESET_CONFIGS:
        raise ValueError(f"Unknown preset type: {preset_type}")
    
    return PRESET_CONFIGS[preset_type].copy()


def list_available_presets() -> List[PresetType]:
    """
    列出所有可用的預設類型
    
    Returns:
        list[PresetType]: 可用的預設類型列表
    """
    return list(PRESET_CONFIGS.keys())


def register_custom_preset(name: str, config: Dict[str, Any]) -> None:
    """
    註冊自定義預設
    
    Args:
        name: 預設名稱
        config: 預設配置，需包含 rotation, retention, compression, name_format
    """
    required_keys = {"rotation", "retention", "compression", "name_format"}
    if not required_keys.issubset(config.keys()):
        missing = required_keys - config.keys()
        raise ValueError(f"Missing required config keys: {missing}")
    
    PRESET_CONFIGS[name] = config


# 為了向後兼容，保留原有的 PresetType 枚舉概念
class PresetFactory:
    """簡化的預設工廠類"""
    
    @staticmethod
    def get_preset(preset_type: PresetType) -> Dict[str, Any]:
        """獲取預設配置"""
        return get_preset_config(preset_type)
    
    @staticmethod  
    def list_presets() -> List[PresetType]:
        """列出可用預設"""
        return list_available_presets()