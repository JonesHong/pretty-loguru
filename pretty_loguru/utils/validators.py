"""
參數驗證統一模組

此模組提供統一的參數驗證功能，避免在多個地方重複相同的驗證邏輯。
"""

import re
from typing import Optional, Any

# ASCII 字符檢查的正則表達式
ASCII_PATTERN = re.compile(r'^[\x00-\x7F]+$')


def is_ascii_only(text: str) -> bool:
    """
    檢查文本是否只包含 ASCII 字符
    
    Args:
        text: 要檢查的文本
        
    Returns:
        bool: True 如果文本只包含 ASCII 字符，否則 False
    """
    return ASCII_PATTERN.match(text) is not None


def validate_ascii_text(text: str, text_type: str = "text", logger_instance: Optional[Any] = None) -> str:
    """
    驗證並清理 ASCII 文本
    
    Args:
        text: 要驗證的文本
        text_type: 文本類型，用於錯誤消息（如 "text", "header", "title"）
        logger_instance: 可選的 logger 實例，用於記錄警告
        
    Returns:
        str: 清理後的 ASCII 文本
        
    Raises:
        ValueError: 如果文本清理後為空
    """
    if is_ascii_only(text):
        return text
        
    # 包含非 ASCII 字符，發出警告並清理
    warning_msg = f"ASCII art only supports ASCII characters. The {text_type} '{text}' contains non-ASCII characters."
    if logger_instance:
        logger_instance.warning(warning_msg)
    
    # 移除非 ASCII 字符
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    if logger_instance:
        logger_instance.warning(f"Removed non-ASCII characters. Using: '{cleaned_text}'")
    
    if not cleaned_text:
        raise ValueError(f"The {text_type} contains only non-ASCII characters and cannot create ASCII art.")
    
    return cleaned_text


def validate_ascii_header(header_text: str, logger_instance: Optional[Any] = None) -> str:
    """
    專門用於驗證 ASCII 標題文本的便捷函數
    
    Args:
        header_text: 要驗證的標題文本
        logger_instance: 可選的 logger 實例，用於記錄警告
        
    Returns:
        str: 清理後的 ASCII 標題文本
        
    Raises:
        ValueError: 如果標題文本清理後為空
    """
    return validate_ascii_text(header_text, "ASCII header", logger_instance)


def validate_ascii_art_text(art_text: str, logger_instance: Optional[Any] = None) -> str:
    """
    專門用於驗證 ASCII 藝術文本的便捷函數
    
    Args:
        art_text: 要驗證的藝術文本
        logger_instance: 可選的 logger 實例，用於記錄警告
        
    Returns:
        str: 清理後的 ASCII 藝術文本
        
    Raises:
        ValueError: 如果藝術文本清理後為空
    """
    return validate_ascii_text(art_text, "text", logger_instance)