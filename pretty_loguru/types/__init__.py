"""
類型定義模組入口

此模組導出所有與 Pretty Loguru 相關的類型定義，
提供統一的類型註解支援，便於 IDE 自動完成和類型檢查。
"""

from .protocols import (
    EnhancedLoggerProtocol,
    EnhancedLogger,
    LogLevelType,
    LogHandlerIdType,
    LogFilterType,
    LogConfigType,
    LogPathType,
    LogNameFormatType,
    LogRotationType,
)

__all__ = [
    # 基本類型
    "EnhancedLoggerProtocol",
    "EnhancedLogger",
    
    # 特定類型
    "LogLevelType",
    "LogHandlerIdType",
    "LogFilterType",
    "LogConfigType",
    "LogPathType",
    "LogNameFormatType",
    "LogRotationType",
]
