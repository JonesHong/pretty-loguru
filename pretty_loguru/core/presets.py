"""
簡化的日誌預設配置模組

按照KISS原則重新設計，使用簡單的配置字典替代複雜的類層次結構。
減少代碼重複，提升可維護性。
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Callable, Literal, List
import warnings
from dateutil.relativedelta import relativedelta # Added for relative date calculations
import re # Added for regex in filename parsing

# 預設類型
PresetType = Literal["detailed", "simple", "daily", "hourly", "minute", "weekly", "monthly"]

# 重命名函數模板
def _create_rename_function(
    pattern: str,
    custom_format: Optional[str] = None,
    time_source: Literal['current', 'loguru_suffix', 'yesterday', 'last_hour', 'last_minute', 'last_week', 'last_month'] = 'current'
) -> Callable:
    """
    創建日誌重命名函數
    
    Args:
        pattern: 默認的命名模式
        custom_format: 自定義壓縮檔名格式，如果提供則優先使用
        time_source: 時間戳的來源 ('current', 'loguru_suffix', 'yesterday', 'last_hour', 'last_minute', 'last_week', 'last_month')
    """
    def rename_function(filepath: str) -> str:
        log_path = Path(filepath)
        
        # 1. 確定用於命名檔案的時間
        target_time = datetime.now()
        if time_source == 'loguru_suffix':
            # 從 Loguru 附加的後綴中提取時間戳
            suffixes = log_path.suffixes
            if len(suffixes) >= 2:
                raw_ts = suffixes[-2].lstrip('.') # e.g., "2025-05-05_23-29-33_084163"
                try:
                    # 嘗試解析 Loguru 的時間戳格式
                    target_time = datetime.strptime(raw_ts.split('_')[0] + '_' + raw_ts.split('_')[1], "%Y-%m-%d_%H-%M-%S")
                except ValueError:
                    warnings.warn(f"Could not parse timestamp from loguru suffix: {raw_ts}. Using current time.", UserWarning)
            else:
                warnings.warn(f"Loguru suffix not found in {filepath}. Using current time for compression.", UserWarning)
        elif time_source == 'yesterday':
            target_time = datetime.now() - timedelta(days=1)
        elif time_source == 'last_hour':
            target_time = datetime.now() - timedelta(hours=1)
        elif time_source == 'last_minute':
            target_time = datetime.now() - timedelta(minutes=1)
        elif time_source == 'last_week':
            target_time = datetime.now() - timedelta(weeks=1)
        elif time_source == 'last_month':
            target_time = datetime.now() - relativedelta(months=1)
        # else: 'current' is default

        # 2. 提取 component_name (例如 "[fastapi_app]")
        # 移除 Loguru 的時間戳後綴和 .log 擴展名
        clean_stem = log_path.stem
        match = re.match(r"(\[.*?\])", clean_stem) # 匹配 [component_name]
        if match:
            component_name = match.group(1).strip('[]')
            # 移除原始檔名中的時間戳部分，只保留 [component_name]
            # 例如 "[fastapi_app]20250505-232933" -> "[fastapi_app]"
            clean_stem_parts = clean_stem.split(']')
            if len(clean_stem_parts) > 1:
                clean_stem = f"[{component_name}]"
            else:
                clean_stem = component_name # 如果沒有方括號，就直接用 component_name
        else:
            # 如果沒有 [component_name] 格式，則使用整個 stem 作為 component_name
            component_name = clean_stem.split('.')[0] # 移除可能的 .loguru_suffix
            clean_stem = component_name


        # 3. 準備替換變數
        format_vars = {
            "name": component_name, # 使用提取的 component_name 作為 {name}
            "component_name": component_name, # 兼容舊的 component_name 變數
            "timestamp": target_time.strftime("%Y%m%d-%H%M%S"),
            "date": target_time.strftime("%Y%m%d"),
            "time": target_time.strftime("%H%M%S"),
            "year": target_time.year,
            "month": f"{target_time.month:02d}",
            "day": f"{target_time.day:02d}",
            "hour": f"{target_time.hour:02d}",
            "minute": f"{target_time.minute:02d}",
            "second": f"{target_time.second:02d}",
            "week": target_time.isocalendar()[1], # ISO 週數
            "week_num": f"{target_time.isocalendar()[1]:02d}" # 帶前導零的週數
        }
        
        # 使用自定義格式或默認模式
        actual_pattern = custom_format if custom_format else pattern
        
        # 格式化模式替換
        try:
            new_name_stem = actual_pattern.format(**format_vars)
        except KeyError as e:
            missing_key = str(e).strip("''")
            raise KeyError(f"日誌檔案名格式 '{actual_pattern}' 使用了未提供的變數 '{missing_key}'")
        
        new_path = log_path.parent / f"{new_name_stem}.log"

        # 4. 避免同名，加上序號
        counter = 1
        while new_path.exists():
            new_path = log_path.parent / f"{new_name_stem}.{counter}.log"
            counter += 1

        os.rename(filepath, new_path)
        return str(new_path)
    
    return rename_function

def create_custom_compression_function(compression_format: str) -> Callable:
    """
    創建自定義壓縮函數
    
    Args:
        compression_format: 自定義的壓縮檔名格式
        
    Returns:
        Callable: 壓縮函數
        
    Examples:
        >>> func = create_custom_compression_function("backup_{name}_{date}")
        >>> # 會產生如 backup_my_app_20250627.log 的檔名
    """
    return _create_rename_function(pattern="", custom_format=compression_format, time_source='current')

# 預設配置定義 - 簡單的字典結構，每個preset有不同的compression策略
PRESET_CONFIGS: Dict[PresetType, Dict[str, Any]] = {
    "detailed": {
        "rotation": "20 MB",
        "retention": "30 days", 
        "compression": _create_rename_function(
            pattern="[{name}].{timestamp}",  # 詳細模式：[component].YYYYMMDD-HHMMSS.log
            time_source='loguru_suffix'
        ),
        "name_format": "[{component_name}]{timestamp}.log"
    },
    "simple": {
        "rotation": "20 MB",
        "retention": "30 days",
        "compression": _create_rename_function(
            pattern="{name}_rot_{timestamp}",  # 簡單模式：component_rot_YYYYMMDD-HHMMSS.log
            time_source='loguru_suffix'
        ),
        "name_format": "{component_name}.log"
    },
    "daily": {
        "rotation": "00:00",  # 每天凌晨輪換
        "retention": "30 days",
        "compression": _create_rename_function(
            pattern="[{name}]{date}",  # 每日模式：[component]YYYYMMDD.log
            time_source='yesterday'
        ),
        "name_format": "[{component_name}]daily_latest.temp.log"
    },
    "hourly": {
        "rotation": "1 hour", 
        "retention": "7 days",
        "compression": _create_rename_function(
            pattern="[{name}]{date}_{hour}",  # 每小時模式：[component]YYYYMMDD_HH.log
            time_source='last_hour'
        ),
        "name_format": "[{component_name}]hourly_latest.temp.log"
    },
    "minute": {
        "rotation": "1 minute",
        "retention": "24 hours", 
        "compression": _create_rename_function(
            pattern="[{name}]{date}_{hour}{minute}",  # 每分鐘模式：[component]YYYYMMDD_HHMM.log
            time_source='last_minute'
        ),
        "name_format": "[{component_name}]minute_latest.temp.log"
    },
    "weekly": {
        "rotation": "monday",  # 每週一輪換
        "retention": "12 weeks",
        "compression": _create_rename_function(
            pattern="[{name}]week_{year}W{week_num}",  # 每週模式：[component]week_2025W26.log
            time_source='last_week'
        ),
        "name_format": "[{component_name}]weekly_latest.temp.log"
    },
    "monthly": {
        "rotation": "1 month",
        "retention": "12 months", 
        "compression": _create_rename_function(
            pattern="[{name}]{year}{month}",  # 每月模式：[component]202506.log
            time_source='last_month'
        ),
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