"""
日誌清理模組

此模組提供 Pretty Loguru 的日誌清理功能，用於定期清理過期的日誌檔案，
避免磁碟空間被長期占用。
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread
from typing import Union, Optional, Any

from ..types import LogPathType, LogRotationType


class LoggerCleaner:
    """日誌清理器類別

    用於定期清理過舊的日誌檔案，避免磁碟空間被佔滿。
    """
    
    def __init__(
        self,
        log_retention: Union[int, str] = 30,
        log_path: Optional[LogPathType] = None,
        check_interval: int = 3600,  # 預設每小時檢查一次
        logger_instance: Any = None,
        recursive: bool = True,  # 是否遞歸清理子目錄
    ) -> None:
        """
        初始化日誌清理器

        Args:
            log_retention: 日誌保留天數，預設為 30 天
            log_path: 日誌儲存路徑，預設為當前目錄下的 logs 資料夾
            check_interval: 檢查間隔，單位為秒，預設為 3600（1小時）
            logger_instance: 記錄清理操作的日誌實例，如果為 None 則使用 print
            recursive: 是否遞歸清理子目錄，預設為 True
        """
        # 設置日誌路徑
        self.log_path = Path(log_path) if log_path else Path.cwd() / "logs"
        
        # 解析保留天數
        if isinstance(log_retention, str):
            try:
                self.retention_days = int(log_retention)
            except ValueError:
                # 如果無法轉換為整數，則使用預設值
                self.retention_days = 30
                if logger_instance:
                    logger_instance.warning(f"Unable to convert '{log_retention}' to an integer, using the default value of 30 days")
                else:
                    print(f"Warning: Unable to convert '{log_retention}' to an integer, using the default value of 30 days")
        else:
            self.retention_days = log_retention
        
        # 設置檢查間隔
        self.check_interval = check_interval
        
        # 設置日誌實例
        self.logger = logger_instance
        
        # 設置遞歸清理標誌
        self.recursive = recursive
        
        # 創建清理線程
        self.cleaner_thread = Thread(
            target=self._clean_logs_loop,
            args=(),
            daemon=True,  # 設定為守護線程
        )
        
        # 初始化執行狀態
        self._is_running = False
    
    def start(self) -> None:
        """
        啟動日誌清理線程
        
        如果清理器已經在運行，則不會重複啟動。
        """
        if self._is_running:
            self._log_message(f"LoggerCleaner: 已經在運行中")
        else:
            self.cleaner_thread.start()
            self._log_message(f"LoggerCleaner: 清理線程已啟動，保留 {self.retention_days} 天內的日誌")
            self._is_running = True
    
    def _log_message(self, message: str, level: str = "INFO") -> None:
        """
        記錄日誌消息
        
        Args:
            message: 日誌消息
            level: 日誌級別，預設為 INFO
        """
        if self.logger:
            # 根據不同級別記錄日誌
            if level == "INFO":
                self.logger.info(message)
            elif level == "WARNING":
                self.logger.warning(message)
            elif level == "ERROR":
                self.logger.error(message)
            elif level == "DEBUG":
                self.logger.debug(message)
            else:
                self.logger.info(message)
        else:
            # 如果沒有提供日誌實例，則使用 print
            print(message)
    
    def _clean_logs_loop(self) -> None:
        """
        清理日誌的循環執行函數
        
        此方法會在單獨的線程中運行，定期檢查並清理過期日誌
        """
        while True:
            try:
                self._clean_old_logs()
            except Exception as e:
                self._log_message(f"LoggerCleaner: 清理日誌時發生錯誤: {str(e)}", "ERROR")
            
            # 等待一段時間再次執行
            time.sleep(self.check_interval)
    
    def _clean_old_logs(self) -> None:
        """
        執行實際的日誌清理操作
        
        根據設置的保留天數，刪除過期的日誌文件
        """
        if not os.path.exists(self.log_path):
            # 如果日誌路徑不存在，則創建它
            os.makedirs(self.log_path, exist_ok=True)
            self._log_message(f"LoggerCleaner: 創建日誌目錄 {self.log_path}", "DEBUG")
            return
        
        # 計算截止日期
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        cutoff_timestamp = cutoff_date.timestamp()
        
        # 決定要遍歷的路徑
        paths_to_check = []
        if self.recursive:
            # 遞歸遍歷所有子目錄
            for root, dirs, files in os.walk(self.log_path):
                for file in files:
                    paths_to_check.append(os.path.join(root, file))
        else:
            # 只檢查指定目錄下的文件
            for file in os.listdir(self.log_path):
                file_path = os.path.join(self.log_path, file)
                if os.path.isfile(file_path):
                    paths_to_check.append(file_path)
        
        # 清理過期日誌
        for file_path in paths_to_check:
            try:
                # 忽略隱藏文件
                if os.path.basename(file_path).startswith('.'):
                    continue
                
                # 檢查文件的創建時間是否早於截止日期
                file_ctime = os.path.getctime(file_path)
                if file_ctime < cutoff_timestamp:
                    # 刪除過期文件
                    os.remove(file_path)
                    self._log_message(f"LoggerCleaner: 已刪除過期日誌文件 {file_path}", "INFO")
            except (PermissionError, OSError) as e:
                # 處理權限錯誤或其他 IO 錯誤
                self._log_message(f"LoggerCleaner: 無法刪除文件 {file_path}: {str(e)}", "WARNING")
            except Exception as e:
                # 處理其他未預期的錯誤
                self._log_message(f"LoggerCleaner: 處理文件 {file_path} 時發生錯誤: {str(e)}", "ERROR")