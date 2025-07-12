"""
依賴檢查統一模組

此模組提供統一的依賴檢查功能，避免在多個地方重複相同的檢查邏輯。
"""

from typing import Optional, Any


def ensure_art_dependency(logger_instance: Optional[Any] = None) -> None:
    """
    確保 art 庫已安裝
    
    Args:
        logger_instance: 可選的 logger 實例，用於記錄錯誤
        
    Raises:
        ImportError: 如果 art 庫未安裝
    """
    try:
        import art
        return True
    except ImportError:
        error_msg = "The 'art' library is not installed. Please install it using 'pip install art'."
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)


def ensure_pyfiglet_dependency(logger_instance: Optional[Any] = None) -> None:
    """
    確保 pyfiglet 庫已安裝
    
    Args:
        logger_instance: 可選的 logger 實例，用於記錄錯誤
        
    Raises:
        ImportError: 如果 pyfiglet 庫未安裝
    """
    try:
        import pyfiglet
        return True
    except ImportError:
        error_msg = "The 'pyfiglet' library is not installed. Please install it using 'pip install pyfiglet'."
        if logger_instance:
            logger_instance.error(error_msg)
        raise ImportError(error_msg)


def check_art_availability() -> bool:
    """
    檢查 art 庫是否可用
    
    Returns:
        bool: True 如果 art 庫可用，否則 False
    """
    try:
        import art
        return True
    except ImportError:
        return False


def check_pyfiglet_availability() -> bool:
    """
    檢查 pyfiglet 庫是否可用
    
    Returns:
        bool: True 如果 pyfiglet 庫可用，否則 False
    """
    try:
        import pyfiglet
        return True
    except ImportError:
        return False


def warn_missing_dependency(
    dependency_name: str, 
    logger_instance: Optional[Any] = None, 
    return_value: bool = False
) -> bool:
    """
    對缺失的依賴發出警告
    
    Args:
        dependency_name: 依賴的名稱
        logger_instance: 可選的 logger 實例，用於記錄警告
        return_value: 要返回的布爾值
        
    Returns:
        bool: return_value 參數的值
    """
    warning_msg = f"'{dependency_name}' library is not installed. Skipping related functionality."
    if logger_instance and hasattr(logger_instance, "warning"):
        logger_instance.warning(warning_msg)
    return return_value


# 預先檢查依賴可用性（模組載入時執行一次）
_HAS_ART = check_art_availability()
_HAS_PYFIGLET = check_pyfiglet_availability()


def has_art() -> bool:
    """返回 art 庫是否可用"""
    return _HAS_ART


def has_pyfiglet() -> bool:
    """返回 pyfiglet 庫是否可用"""
    return _HAS_PYFIGLET