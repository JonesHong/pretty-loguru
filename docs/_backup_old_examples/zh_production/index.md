# 生產環境範例

在生產環境中使用 pretty-loguru 需要特別考慮效能、可靠性和維護性。本頁面展示如何在生產環境中最佳化配置和使用 pretty-loguru。

## 🏭 生產環境配置

### 基本生產配置

```python
from pretty_loguru import create_logger
import os
import sys
from pathlib import Path

def setup_production_logging():
    """設置生產環境日誌配置"""
    
    # 創建日誌目錄
    log_dir = Path("/var/log/myapp")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 生產環境配置
    create_logger(
        preset="production",
        folder=str(log_dir),
        file_name="app_{time:YYYY-MM-DD}.log",
        level="INFO",
        rotation="100 MB",      # 100MB 自動輪換
        retention="30 days",    # 保留 30 天
        compression="gz",       # 壓縮舊日誌
        backtrace=False,        # 生產環境關閉回溯
        diagnose=False          # 關閉診斷模式
    )
    
    logger.ascii_header("PRODUCTION", font="standard", border_style="blue")
    
    logger.block(
        "生產環境日誌系統啟動",
        [
            f"📁 日誌目錄: {log_dir}",
            f"📊 日誌級別: INFO",
            f"🔄 輪換大小: 100 MB",
            f"📅 保留期限: 30 天",
            f"🗜️  壓縮格式: gzip",
            f"🔒 安全模式: 啟用"
        ],
        border_style="green",
        log_level="SUCCESS"
    )

setup_production_logging()
```

### 環境感知配置

```python
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

def get_environment() -> Environment:
    """獲取當前環境"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    try:
        return Environment(env)
    except ValueError:
        return Environment.DEVELOPMENT

def setup_environment_logging():
    """根據環境設置日誌"""
    
    env = get_environment()
    
    configs = {
        Environment.DEVELOPMENT: {
            "preset": "development",
            "folder": "dev_logs",
            "level": "DEBUG",
            "rotation": None,
            "visual_mode": "full"
        },
        Environment.STAGING: {
            "preset": "production", 
            "folder": "/var/log/myapp/staging",
            "level": "INFO",
            "rotation": "50 MB",
            "retention": "7 days",
            "visual_mode": "minimal"
        },
        Environment.PRODUCTION: {
            "preset": "production",
            "folder": "/var/log/myapp/production", 
            "level": "WARNING",
            "rotation": "100 MB",
            "retention": "30 days",
            "compression": "gz",
            "visual_mode": "minimal"
        }
    }
    
    config = configs[env]
    create_logger(**config)
    
    logger.ascii_block(
        f"環境配置載入完成",
        [
            f"🌍 環境: {env.value.upper()}",
            f"📁 日誌路徑: {config['folder']}",
            f"📊 日誌級別: {config['level']}",
            f"🎨 視覺模式: {config.get('visual_mode', 'standard')}",
            f"⚙️  配置文件: 已載入"
        ],
        ascii_header=env.value.upper(),
        ascii_font="standard",
        border_style="cyan"
    )

setup_environment_logging()
```

## 📊 效能最佳化

### 異步日誌處理

```python
import asyncio
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

class AsyncLogger:
    """異步日誌處理器"""
    
    def __init__(self, max_workers=2):
        self.log_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_logs)
        self.worker_thread.daemon = True
        self.worker_thread.start()
    
    def _process_logs(self):
        """處理日誌隊列"""
        while self.running:
            try:
                log_item = self.log_queue.get(timeout=1)
                if log_item is None:
                    break
                
                # 實際寫入日誌
                level, message, data = log_item
                getattr(logger, level)(message)
                
                if data:
                    logger.block(
                        "詳細資訊",
                        [f"{k}: {v}" for k, v in data.items()],
                        border_style="blue"
                    )
                
                self.log_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"日誌處理錯誤: {e}")
    
    def log_async(self, level: str, message: str, data: dict = None):
        """異步記錄日誌"""
        if not self.running:
            return
        
        try:
            self.log_queue.put((level, message, data), block=False)
        except queue.Full:
            # 如果隊列滿了，直接同步記錄
            logger.warning("日誌隊列已滿，改為同步記錄")
            getattr(logger, level)(message)
    
    def shutdown(self):
        """關閉異步日誌處理器"""
        self.running = False
        self.log_queue.put(None)
        self.worker_thread.join()
        self.executor.shutdown(wait=True)

# 全域異步日誌器
async_logger = AsyncLogger()

def log_request_async(method: str, url: str, status_code: int, duration: float):
    """異步記錄請求"""
    async_logger.log_async(
        "info",
        f"API 請求: {method} {url}",
        {
            "status_code": status_code,
            "duration": f"{duration:.3f}s",
            "timestamp": time.time()
        }
    )

# 使用範例
log_request_async("GET", "/api/users", 200, 0.15)
```

### 條件式視覺化

```python
import os

class ProductionLogger:
    """生產環境最佳化日誌器"""
    
    def __init__(self):
        self.visual_enabled = os.getenv("LOG_VISUAL", "false").lower() == "true"
        self.performance_mode = os.getenv("LOG_PERFORMANCE", "true").lower() == "true"
    
    def smart_block(self, title: str, content: list, level: str = "INFO", **kwargs):
        """智能區塊日誌"""
        if self.visual_enabled:
            # 開發/除錯環境使用完整視覺效果
            logger.block(title, content, **kwargs)
        else:
            # 生產環境使用簡化輸出
            logger.info(f"{title}: {', '.join(content)}")
    
    def smart_ascii_header(self, text: str, **kwargs):
        """智能 ASCII 標題"""
        if self.visual_enabled:
            logger.ascii_header(text, **kwargs)
        else:
            logger.info(f"=== {text} ===")
    
    def performance_log(self, operation: str, duration: float, details: dict = None):
        """效能日誌記錄"""
        if not self.performance_mode:
            return
        
        # 只記錄慢請求
        if duration > 1.0:
            level = "WARNING" if duration > 2.0 else "INFO"
            
            content = [
                f"⏱️  執行時間: {duration:.3f}s",
                f"🎯 操作: {operation}"
            ]
            
            if details:
                content.extend([f"{k}: {v}" for k, v in details.items()])
            
            if duration > 2.0:
                self.smart_block(
                    "慢操作警告",
                    content,
                    border_style="yellow",
                    log_level=level
                )
            else:
                logger.info(f"操作完成: {operation} ({duration:.3f}s)")

# 全域生產日誌器
prod_logger = ProductionLogger()

# 使用範例
def expensive_operation():
    start_time = time.time()
    
    # 模擬耗時操作
    time.sleep(1.5)
    
    duration = time.time() - start_time
    prod_logger.performance_log(
        "expensive_operation",
        duration,
        {"cpu_usage": "45%", "memory": "2.1GB"}
    )

expensive_operation()
```

## 🔐 安全性考量

### 敏感資訊過濾

```python
import re
import json
from typing import Any, Dict

class SecureLogger:
    """安全日誌記錄器"""
    
    # 敏感資訊模式
    SENSITIVE_PATTERNS = {
        'password': re.compile(r'(password|pwd|pass)["\s]*[:=]["\s]*([^"\\s,}]+)', re.IGNORECASE),
        'token': re.compile(r'(token|jwt|bearer)["\s]*[:=]["\s]*([^"\\s,}]+)', re.IGNORECASE),
        'api_key': re.compile(r'(api[_-]?key|apikey)["\s]*[:=]["\s]*([^"\\s,}]+)', re.IGNORECASE),
        'credit_card': re.compile(r'\b\d{4}[\\s-]?\d{4}[\\s-]?\d{4}[\\s-]?\d{4}\b'),
        'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        'ip_address': re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    }
    
    def sanitize_data(self, data: Any) -> Any:
        """清理敏感資訊"""
        if isinstance(data, str):
            return self._sanitize_string(data)
        elif isinstance(data, dict):
            return {k: self.sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        else:
            return data
    
    def _sanitize_string(self, text: str) -> str:
        """清理字符串中的敏感資訊"""
        for pattern_name, pattern in self.SENSITIVE_PATTERNS.items():
            if pattern_name in ['password', 'token', 'api_key']:
                text = pattern.sub(r'\1: ***', text)
            elif pattern_name == 'credit_card':
                text = pattern.sub('****-****-****-****', text)
            elif pattern_name == 'email':
                text = pattern.sub(lambda m: f"{m.group()[:3]}***@***", text)
            elif pattern_name == 'ip_address':
                text = pattern.sub('***.***.***.***', text)
        
        return text
    
    def secure_log(self, level: str, message: str, data: Dict = None):
        """安全日誌記錄"""
        # 清理訊息
        clean_message = self.sanitize_data(message)
        
        # 清理數據
        clean_data = self.sanitize_data(data) if data else None
        
        # 記錄日誌
        getattr(logger, level)(clean_message)
        
        if clean_data:
            logger.block(
                "請求詳情",
                [f"{k}: {v}" for k, v in clean_data.items()],
                border_style="blue"
            )
    
    def audit_log(self, action: str, user_id: str, details: Dict):
        """審計日誌"""
        audit_data = {
            "action": action,
            "user_id": user_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "details": self.sanitize_data(details)
        }
        
        logger.ascii_block(
            "安全審計記錄",
            [
                f"👤 用戶 ID: {user_id}",
                f"🎯 操作: {action}",
                f"⏰ 時間: {audit_data['timestamp']}",
                f"📊 詳情: {json.dumps(audit_data['details'], ensure_ascii=False)}"
            ],
            ascii_header="AUDIT",
            ascii_font="standard",
            border_style="magenta",
            log_level="INFO"
        )

secure_logger = SecureLogger()

# 使用範例
def login_attempt(username: str, password: str, ip_address: str):
    """登入嘗試記錄"""
    login_data = {
        "username": username,
        "password": password,  # 將被自動清理
        "ip_address": ip_address,  # 將被自動清理
        "user_agent": "Mozilla/5.0..."
    }
    
    secure_logger.secure_log(
        "info",
        f"用戶登入嘗試: {username}",
        login_data
    )
    
    # 審計記錄
    secure_logger.audit_log(
        "login_attempt",
        username,
        {"ip": ip_address, "success": True}
    )

login_attempt("john_doe", "secret123", "192.168.1.100")
```

## 📈 監控和警報

### 系統監控

```python
import psutil
import time
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SystemMetrics:
    """系統指標"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict
    process_count: int
    uptime: float

class SystemMonitor:
    """系統監控器"""
    
    def __init__(self):
        self.alert_thresholds = {
            'cpu': 80.0,
            'memory': 85.0,
            'disk': 90.0
        }
        self.last_alert_time = {}
        self.alert_cooldown = 300  # 5分鐘冷卻時間
    
    def collect_metrics(self) -> SystemMetrics:
        """收集系統指標"""
        try:
            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 記憶體使用率
            memory = psutil.virtual_memory()
            
            # 磁碟使用率
            disk = psutil.disk_usage('/')
            
            # 網路 I/O
            network = psutil.net_io_counters()
            
            # 進程數量
            process_count = len(psutil.pids())
            
            # 系統運行時間
            uptime = time.time() - psutil.boot_time()
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                network_io={
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                },
                process_count=process_count,
                uptime=uptime
            )
            
        except Exception as e:
            logger.error(f"收集系統指標失敗: {e}")
            return None
    
    def check_alerts(self, metrics: SystemMetrics):
        """檢查警報條件"""
        current_time = time.time()
        
        alerts = []
        
        # CPU 警報
        if metrics.cpu_percent > self.alert_thresholds['cpu']:
            if self._should_alert('cpu', current_time):
                alerts.append({
                    'type': 'cpu',
                    'value': metrics.cpu_percent,
                    'threshold': self.alert_thresholds['cpu'],
                    'severity': 'high' if metrics.cpu_percent > 95 else 'medium'
                })
        
        # 記憶體警報
        if metrics.memory_percent > self.alert_thresholds['memory']:
            if self._should_alert('memory', current_time):
                alerts.append({
                    'type': 'memory',
                    'value': metrics.memory_percent,
                    'threshold': self.alert_thresholds['memory'],
                    'severity': 'high' if metrics.memory_percent > 95 else 'medium'
                })
        
        # 磁碟警報
        if metrics.disk_percent > self.alert_thresholds['disk']:
            if self._should_alert('disk', current_time):
                alerts.append({
                    'type': 'disk',
                    'value': metrics.disk_percent,
                    'threshold': self.alert_thresholds['disk'],
                    'severity': 'critical' if metrics.disk_percent > 98 else 'high'
                })
        
        return alerts
    
    def _should_alert(self, alert_type: str, current_time: float) -> bool:
        """檢查是否應該發送警報（考慮冷卻時間）"""
        last_time = self.last_alert_time.get(alert_type, 0)
        if current_time - last_time > self.alert_cooldown:
            self.last_alert_time[alert_type] = current_time
            return True
        return False
    
    def log_metrics(self, metrics: SystemMetrics):
        """記錄系統指標"""
        
        # 決定整體狀態顏色
        max_usage = max(metrics.cpu_percent, metrics.memory_percent, metrics.disk_percent)
        
        if max_usage > 90:
            color = "red"
            status = "🔴 危險"
        elif max_usage > 75:
            color = "yellow"
            status = "🟡 警告"
        else:
            color = "green"
            status = "🟢 正常"
        
        logger.block(
            "系統資源監控",
            [
                f"🖥️  CPU 使用率: {metrics.cpu_percent:.1f}%",
                f"💾 記憶體使用: {metrics.memory_percent:.1f}%",
                f"💿 磁碟使用: {metrics.disk_percent:.1f}%",
                f"⚙️  進程數量: {metrics.process_count}",
                f"⏰ 運行時間: {self._format_uptime(metrics.uptime)}",
                f"📊 整體狀態: {status}"
            ],
            border_style=color
        )
        
        # 檢查並處理警報
        alerts = self.check_alerts(metrics)
        for alert in alerts:
            self._handle_alert(alert)
    
    def _handle_alert(self, alert: Dict):
        """處理警報"""
        severity_colors = {
            'low': 'blue',
            'medium': 'yellow',
            'high': 'red',
            'critical': 'red'
        }
        
        severity_fonts = {
            'low': 'standard',
            'medium': 'standard',
            'high': 'doom',
            'critical': 'doom'
        }
        
        color = severity_colors.get(alert['severity'], 'yellow')
        font = severity_fonts.get(alert['severity'], 'standard')
        
        logger.ascii_block(
            f"系統資源警報",
            [
                f"⚠️  警報類型: {alert['type'].upper()}",
                f"📊 當前值: {alert['value']:.1f}%",
                f"🎯 閾值: {alert['threshold']:.1f}%",
                f"🚨 嚴重程度: {alert['severity'].upper()}",
                f"⏰ 警報時間: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"🔧 建議: 檢查系統負載並採取相應措施"
            ],
            ascii_header="ALERT",
            ascii_font=font,
            border_style=color,
            log_level="WARNING" if alert['severity'] in ['low', 'medium'] else "ERROR"
        )
    
    def _format_uptime(self, uptime_seconds: float) -> str:
        """格式化運行時間"""
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        return f"{days}天 {hours}小時 {minutes}分鐘"

# 系統監控器實例
monitor = SystemMonitor()

def run_system_monitoring():
    """運行系統監控"""
    logger.ascii_header("MONITORING", font="standard", border_style="cyan")
    
    while True:
        try:
            metrics = monitor.collect_metrics()
            if metrics:
                monitor.log_metrics(metrics)
            
            # 每30秒監控一次
            time.sleep(30)
            
        except KeyboardInterrupt:
            logger.ascii_header("STOP MONITOR", font="standard", border_style="yellow")
            break
        except Exception as e:
            logger.error(f"監控過程中發生錯誤: {e}")
            time.sleep(60)  # 發生錯誤時等待更長時間

# 使用範例（背景執行）
# run_system_monitoring()
```

## 🔄 日誌輪換和維護

### 高級日誌輪換

```python
import os
import gzip
import shutil
from pathlib import Path
from datetime import datetime, timedelta

class LogManager:
    """日誌管理器"""
    
    def __init__(self, log_dir: str):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_advanced_rotation(self):
        """設置高級日誌輪換"""
        create_logger(
            folder=str(self.log_dir),
            file_name="app_{time:YYYY-MM-DD_HH}.log",  # 每小時一個檔案
            rotation="1 hour",                          # 每小時輪換
            retention="168 hours",                      # 保留7天
            compression="gz",                           # 壓縮舊檔案
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level="INFO"
        )
        
        logger.ascii_block(
            "高級日誌輪換配置",
            [
                f"📁 日誌目錄: {self.log_dir}",
                f"🔄 輪換頻率: 每小時",
                f"📅 保留期限: 7 天",
                f"🗜️  壓縮: gzip",
                f"📝 格式: 詳細時間戳",
                f"📊 級別: INFO+"
            ],
            ascii_header="LOG SETUP",
            ascii_font="standard",
            border_style="green"
        )
    
    def manual_cleanup(self, days_to_keep: int = 7):
        """手動清理舊日誌"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        removed_files = []
        total_size_freed = 0
        
        for log_file in self.log_dir.glob("*.log*"):
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            
            if file_time < cutoff_date:
                file_size = log_file.stat().st_size
                log_file.unlink()
                removed_files.append(log_file.name)
                total_size_freed += file_size
        
        if removed_files:
            logger.ascii_block(
                "日誌清理完成",
                [
                    f"🗑️  刪除檔案: {len(removed_files)} 個",
                    f"💾 釋放空間: {total_size_freed / 1024 / 1024:.2f} MB",
                    f"📅 清理期限: {days_to_keep} 天前",
                    f"📊 剩餘檔案: {len(list(self.log_dir.glob('*.log*')))} 個"
                ],
                ascii_header="CLEANUP",
                ascii_font="standard",
                border_style="yellow"
            )
        else:
            logger.info("沒有需要清理的舊日誌檔案")
    
    def compress_old_logs(self):
        """壓縮舊的日誌檔案"""
        compressed_count = 0
        
        for log_file in self.log_dir.glob("*.log"):
            # 檢查檔案是否超過24小時
            file_age = time.time() - log_file.stat().st_mtime
            
            if file_age > 86400:  # 24小時
                compressed_file = log_file.with_suffix('.log.gz')
                
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                log_file.unlink()
                compressed_count += 1
        
        if compressed_count > 0:
            logger.success(f"已壓縮 {compressed_count} 個舊日誌檔案")

# 日誌管理器
log_manager = LogManager("/var/log/myapp")
log_manager.setup_advanced_rotation()
```

## 🚀 完整生產範例

結合所有生產環境最佳實踐的完整範例：

```python
import os
import sys
import signal
import asyncio
from contextlib import asynccontextmanager

class ProductionApp:
    """生產環境應用"""
    
    def __init__(self):
        self.running = True
        self.setup_signal_handlers()
        self.setup_logging()
        self.async_logger = AsyncLogger()
        self.monitor = SystemMonitor()
        self.secure_logger = SecureLogger()
        self.log_manager = LogManager("/var/log/myapp")
    
    def setup_signal_handlers(self):
        """設置信號處理器"""
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信號處理器"""
        logger.ascii_block(
            "收到關閉信號",
            [
                f"📡 信號: {signum}",
                f"🛑 開始優雅關閉...",
                f"💾 保存狀態中...",
                f"🔒 清理資源中..."
            ],
            ascii_header="SHUTDOWN",
            ascii_font="standard",
            border_style="yellow",
            log_level="WARNING"
        )
        
        self.running = False
    
    def setup_logging(self):
        """設置日誌系統"""
        env = get_environment()
        
        if env == Environment.PRODUCTION:
            setup_production_logging()
        else:
            setup_environment_logging()
    
    async def start(self):
        """啟動應用"""
        logger.ascii_block(
            "生產環境應用啟動",
            [
                f"🌍 環境: {get_environment().value.upper()}",
                f"📊 進程 ID: {os.getpid()}",
                f"👤 用戶: {os.getenv('USER', 'unknown')}",
                f"💾 工作目錄: {os.getcwd()}",
                f"🐍 Python 版本: {sys.version.split()[0]}",
                f"⚡ 狀態: 完全啟動"
            ],
            ascii_header="STARTUP",
            ascii_font="block",
            border_style="green",
            log_level="SUCCESS"
        )
        
        # 啟動監控任務
        monitoring_task = asyncio.create_task(self._monitoring_loop())
        
        # 啟動日誌清理任務
        cleanup_task = asyncio.create_task(self._cleanup_loop())
        
        try:
            # 主應用邏輯
            await self._main_loop()
        finally:
            # 取消背景任務
            monitoring_task.cancel()
            cleanup_task.cancel()
            
            # 清理資源
            await self._cleanup()
    
    async def _main_loop(self):
        """主應用循環"""
        while self.running:
            try:
                # 模擬應用工作
                await asyncio.sleep(1)
                
                # 異步記錄日誌
                self.async_logger.log_async(
                    "info",
                    "應用正常運行",
                    {"timestamp": time.time(), "status": "healthy"}
                )
                
            except Exception as e:
                logger.error(f"主循環錯誤: {e}")
                await asyncio.sleep(5)
    
    async def _monitoring_loop(self):
        """監控循環"""
        while self.running:
            try:
                metrics = self.monitor.collect_metrics()
                if metrics:
                    self.monitor.log_metrics(metrics)
                
                await asyncio.sleep(30)  # 每30秒監控一次
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"監控錯誤: {e}")
                await asyncio.sleep(60)
    
    async def _cleanup_loop(self):
        """清理循環"""
        while self.running:
            try:
                # 每天清理一次日誌
                self.log_manager.manual_cleanup()
                self.log_manager.compress_old_logs()
                
                await asyncio.sleep(86400)  # 24小時
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"清理錯誤: {e}")
                await asyncio.sleep(3600)  # 錯誤時等待1小時
    
    async def _cleanup(self):
        """應用清理"""
        logger.ascii_block(
            "應用清理完成",
            [
                "🛑 主循環已停止",
                "📊 監控系統已關閉", 
                "🗑️  清理任務已停止",
                "💾 日誌狀態已保存",
                "🔒 資源已釋放",
                "✅ 優雅關閉完成"
            ],
            ascii_header="CLEANED",
            ascii_font="standard",
            border_style="blue",
            log_level="SUCCESS"
        )
        
        # 關閉異步日誌器
        self.async_logger.shutdown()

async def main():
    """主函數"""
    app = ProductionApp()
    await app.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("應用被用戶中斷")
    except Exception as e:
        logger.critical(f"應用啟動失敗: {e}")
        sys.exit(1)
```

這個完整的生產環境範例展示了如何在實際產品中使用 pretty-loguru，包括效能最佳化、安全性、監控和維護等各個方面的最佳實踐！