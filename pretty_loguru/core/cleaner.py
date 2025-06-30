"""
日誌清理模組

此模組提供 Pretty Loguru 的日誌清理功能，用於定期清理過期的日誌檔案，
避免磁碟空間被長期占用。
"""

import os
import time
import atexit
import re
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread, Event
from typing import Union, Optional, Any

from ..types import LogPathType, LogRotationType


class LoggerCleaner:
    """日誌清理器類別

    用於定期清理過舊的日誌檔案，避免磁碟空間被佔滿。
    """

    def __init__(
        self,
        log_retention: Union[int, str] = "30 days",
        log_path: Optional[LogPathType] = None,
        check_interval: int = 3600,  # 預設每小時檢查一次
        logger_instance: Any = None,
        recursive: bool = True,  # 是否遞歸清理子目錄
    ) -> None:
        """
        初始化日誌清理器

        Args:
            log_retention: 日誌保留期限。可以是整數（天數），或字串（例如 "10 days", "1 week", "6 months"）。
                           支援單位: seconds, minutes, hours, days, weeks, months, years.
            log_path: 日誌儲存路徑，預設為當��目錄下的 logs 資料夾
            check_interval: 檢查間隔，單位為秒，預設為 3600（1小時）
            logger_instance: 記錄清理操作的日誌實例，如果為 None 則使用 print
            recursive: 是否遞歸清理子目錄，預設為 True
        """
        self.log_path = Path(log_path) if log_path else Path.cwd() / "logs"
        self.check_interval = check_interval
        self.logger = logger_instance
        self.recursive = recursive

        try:
            self.retention_delta = self._parse_retention(log_retention)
            self.retention_str = str(log_retention)
        except (ValueError, TypeError) as e:
            self.retention_delta = timedelta(days=30)
            self.retention_str = "30 days"
            self._log_message(
                f"LoggerCleaner: 無效的保留時間格式 '{log_retention}'，將使用預設值 '30 days'。錯誤: {e}",
                "WARNING",
            )

        self._stop_event = Event()
        self.cleaner_thread = Thread(
            target=self._clean_logs_loop,
            args=(),
            daemon=False,
        )
        self._is_running = False
        atexit.register(self.stop)

    def _parse_retention(self, retention: Union[int, str]) -> timedelta:
        """解析保留時間參數，轉換為 timedelta 物件"""
        if isinstance(retention, int):
            return timedelta(days=retention)
        if not isinstance(retention, str):
            raise TypeError("Retention must be an integer (days) or a string.")

        # 使用正則表達式來解析 "value unit" 格式
        match = re.match(r"(\d+)\s*([a-z]+)", retention.lower())
        if not match:
            raise ValueError(
                f"Invalid retention format: '{retention}'. "
                "Expected format like '10 days', '1 week'."
            )

        value = int(match.group(1))
        unit = match.group(2).rstrip("s")  # 移除複數 's'

        unit_map = {
            "second": "seconds",
            "minute": "minutes",
            "hour": "hours",
            "day": "days",
            "week": "weeks",
        }

        if unit in unit_map:
            return timedelta(**{unit_map[unit]: value})
        elif unit == "month":
            # 近似值：一個月約為 30.5 天
            return timedelta(days=value * 30.5)
        elif unit == "year":
            # 近似值：一年約為 365.25 天
            return timedelta(days=value * 365.25)
        else:
            raise ValueError(f"Unknown time unit: '{unit}'")

    def start(self) -> None:
        """啟動日誌清理線程"""
        if self._is_running:
            self._log_message("LoggerCleaner: 已經在運行中")
        else:
            self.cleaner_thread.start()
            self._log_message(f"LoggerCleaner: 清理線程已啟動，保留 {self.retention_str} 內的日誌")
            self._is_running = True

    def stop(self) -> None:
        """優雅地停止清理線程"""
        if self._is_running:
            self._log_message("LoggerCleaner: 正在停止清理線程...")
            self._stop_event.set()
            if self.cleaner_thread.is_alive():
                self.cleaner_thread.join(timeout=30)
            self._is_running = False
            self._log_message("LoggerCleaner: 清理線程已停止")

    def _log_message(self, message: str, level: str = "INFO") -> None:
        """記錄日誌消息"""
        if self.logger:
            getattr(self.logger, level.lower(), self.logger.info)(message)
        else:
            print(message)

    def _clean_logs_loop(self) -> None:
        """清理日誌的循環執行函數"""
        while not self._stop_event.is_set():
            try:
                self._clean_old_logs()
            except Exception as e:
                self._log_message(f"LoggerCleaner: 清理日誌時發生錯誤: {e}", "ERROR")
            self._stop_event.wait(self.check_interval)

    def _clean_old_logs(self) -> None:
        """執行實際的日誌清理操作"""
        if not self.log_path.exists():
            self.log_path.mkdir(parents=True, exist_ok=True)
            self._log_message(f"LoggerCleaner: 創建日誌目錄 {self.log_path}", "DEBUG")
            return

        # 使用 self.retention_delta 來計算截止日期
        cutoff_date = datetime.now() - self.retention_delta
        cutoff_timestamp = cutoff_date.timestamp()

        paths_to_check = []
        if self.recursive:
            for root, _, files in os.walk(self.log_path):
                for file in files:
                    paths_to_check.append(Path(root) / file)
        else:
            for file_path in self.log_path.iterdir():
                if file_path.is_file():
                    paths_to_check.append(file_path)

        for file_path in paths_to_check:
            try:
                if file_path.name.startswith('.'):
                    continue

                file_mtime = file_path.stat().st_mtime
                if file_mtime < cutoff_timestamp:
                    file_path.unlink()
                    self._log_message(f"LoggerCleaner: 已刪除過期日誌文件 {file_path}", "INFO")
            except FileNotFoundError:
                # 檔案可能在檢查和刪除之間被其他程序移除（例如壓縮），這不是錯誤
                continue
            except (PermissionError, OSError) as e:
                self._log_message(f"LoggerCleaner: 無法刪除文件 {file_path}: {e}", "WARNING")
            except Exception as e:
                self._log_message(f"LoggerCleaner: 處理文件 {file_path} 時發生錯誤: {e}", "ERROR")
