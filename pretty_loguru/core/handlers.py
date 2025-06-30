"""
日誌處理器模組

此模組提供 Pretty Loguru 的處理器相關功能，包括過濾器創建、
文件名格式化，以及各種日誌輸出處理方法。
"""

from datetime import datetime
import os
from typing import Dict, Callable, Optional, Any
from ..types import LogFilterType

def create_destination_filters() -> Dict[str, LogFilterType]:
    """
    創建基於目標的過濾器函數，用於控制日誌輸出目標

    Returns:
        Dict[str, LogFilterType]: 包含控制台和文件過濾器的字典
    """
    # 控制台過濾器
    def console_filter(record: Dict[str, Any]) -> bool:
        """
        控制台過濾器，決定記錄是否顯示在控制台
        
        Args:
            record: 日誌記錄字典
            
        Returns:
            bool: 如果應該顯示在控制台則返回 True，否則返回 False
        """
        # 如果記錄明確標記為只輸出到文件，則不在控制台顯示
        if record["extra"].get("to_log_file_only", False):
            return False
        return True

    # 文件過濾器
    def file_filter(record: Dict[str, Any]) -> bool:
        """
        文件過濾器，決定記錄是否寫入日誌文件
        
        Args:
            record: 日誌記錄字典
            
        Returns:
            bool: 如果應該寫入文件則返回 True，否則返回 False
        """
        # 如果記錄明確標記為只輸出到控制台，則不寫入文件
        if record["extra"].get("to_console_only", False):
            return False
        return True

    return {
        "console": console_filter,
        "file": file_filter
    }


def format_filename(
    component_name: str,
    log_name_format: Optional[str] = None,
    name: Optional[str] = None,
) -> str:
    """
    根據提供的格式生成日誌檔案名，並處理不合法的文件名字符
    
    Args:
        component_name: 進程 ID 或服務名稱
        log_name_format: 日誌檔案名格式字串，例如 "{name}_{date}.log"。
                         如果為 None，則則使用預設格式 "[{name}]_{timestamp}.log"。
        name: 服務或組件名稱，用於在日誌檔案名中使用變數替換
        
    Returns:
        str: 格式化後的日誌檔案名，已移除不合法字符
        
    Raises:
        KeyError: 當日誌檔案名格式使用了未提供的變數時
    """
    now = datetime.now()
    
    # 如果沒有提供格式，使用預設格式
    if log_name_format is None:
        log_name_format = "[{name}]_{timestamp}.log"
    
    # 準備替換變數
    format_vars = {
        "name": component_name, # 使用 component_name 作為 {name} 佔位符的值
        "component_name": component_name, # 保留以兼容其他可能使用它的部分
        "timestamp": now.strftime("%Y%m%d-%H%M%S"),
        "date": now.strftime("%Y%m%d"),
        "time": now.strftime("%H%M%S"),
        "year": now.strftime("%Y"),
        "month": now.strftime("%m"),
        "day": now.strftime("%d"),
        "hour": now.strftime("%H"),
        "minute": now.strftime("%M"),
        "second": now.strftime("%S"),
    }
    
    # 替換格式中的變數
    try:
        filename = log_name_format.format(**format_vars)
    except KeyError as e:
        # 處理缺少的變數，使用更友好的錯誤訊息
        missing_key = str(e).strip("''")
        raise KeyError(f"日誌檔案名格式 '{log_name_format}' 使用了未提供的變數 '{missing_key}'")
    
    # 替換文件名中的不合法字符
    illegal_chars = ['/', ':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    
    return filename


def create_formatter(fmt: Optional[str] = None) -> Callable[[Dict[str, Any]], str]:
    """
    創建日誌格式化函數
    
    Args:
        fmt: 格式字符串，如果為 None 則使用默認格式
        
    Returns:
        Callable: 格式化函數，接受日誌記錄並返回格式化字符串
    """
    default_fmt = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
    
    def formatter(record: Dict[str, Any]) -> str:
        """
        格式化日誌記錄
        
        Args:
            record: 日誌記錄字典
            
        Returns:
            str: 格式化後的日誌字符串
        """
        # 使用傳入的格式或默認格式
        format_str = fmt or default_fmt
        
        # 根據記錄中的值進行替換
        # 這裡可以實現更複雜的格式化邏輯
        return format_str.format(**record)
    
    return formatter


def adapt_rotation_value(rotation: Any) -> str:
    """
    調整輪換值的格式，確保正確設置
    
    Args:
        rotation: 輪換設置，可以是數字或字符串
        
    Returns:
        str: 格式化後的輪換值
    """
    if isinstance(rotation, (int, float)):
        # 如果是數字，直接轉換為 MB 格式
        return f"{rotation} MB"
    
    if isinstance(rotation, str):
        # 如果是純數字字符串，添加 MB 單位
        if rotation.strip().isdigit():
            return f"{rotation.strip()} MB"
            
        # 檢查是否已經包含單位
        units = ["kb", "mb", "gb", "b", "day", "month", "week", "hour", "minute", "second"]
        if any(unit in rotation.lower() for unit in units):
            return rotation  # 已經有單位，保持不變
        
        # 嘗試轉換為數字，如果成功則添加 MB 單位
        try:
            float(rotation)
            return f"{rotation} MB"
        except ValueError:
            pass
    
    # 其他情況，原樣返回
    return str(rotation)