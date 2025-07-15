# 基於目標的日誌

學習如何同時將日誌發送到多個目標，並為每個目的地設定不同的配置。

## 🎯 多目標概覽

基於目標的日誌允許您將相同的日誌訊息發送到不同的目的地（控制台、檔案、遠端服務），並為每個目標設定獨特的格式和過濾。

## 📤 基本多目標設定

### 控制台 + 檔案目標

```python
from pretty_loguru import create_logger

# 初始化基礎日誌記錄器
logger = create_logger(
    name="multi_target",
    level="DEBUG", 
    log_path="logs"
)

# 目標 1：控制台（INFO 及以上，彩色）
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

# 目標 2：除錯檔案（所有內容）
logger.add(
    "logs/debug.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="20MB"
)

# 目標 3：錯誤檔案（僅錯誤）
logger.add(
    "logs/errors.log",
    format="{time} | {level} | {name}:{function}:{line} - {message} | {extra}",
    level="ERROR",
    rotation="10MB",
    retention="90 days"
)

# 測試不同等級
logger.debug("除錯訊息 - 僅在 debug.log")
logger.info("資訊訊息 - 控制台 + debug.log")
logger.error("錯誤訊息 - 所有三個目標")
```

### 基於等級的目標分離

```python
from pretty_loguru import create_logger

# 建立日誌記錄器
logger = create_logger(
    name="level_separation",
    level="DEBUG"
)

# 移除預設處理器
logger.remove()

# 目標 1：除錯控制台（開發）
logger.add(
    sink=lambda msg: print(f"[除錯] {msg}", end=""),
    level="DEBUG",
    filter=lambda record: record["level"].name == "DEBUG"
)

# 目標 2：資訊控制台（一般輸出）
logger.add(
    sink=lambda msg: print(f"[資訊] {msg}", end=""),
    level="INFO",
    filter=lambda record: record["level"].name in ["INFO", "SUCCESS"]
)

# 目標 3：警告控制台（需要注意）
logger.add(
    sink=lambda msg: print(f"[警告] {msg}", end=""),
    level="WARNING",
    filter=lambda record: record["level"].name == "WARNING"
)

# 目標 4：錯誤控制台（問題）
logger.add(
    sink=lambda msg: print(f"[錯誤] {msg}", end=""),
    level="ERROR",
    filter=lambda record: record["level"].name in ["ERROR", "CRITICAL"]
)

# 測試等級分離
logger.debug("除錯資訊")
logger.info("一般資訊")
logger.success("成功訊息")
logger.warning("警告訊息")
logger.error("錯誤訊息")
```

## 🏢 企業級多目標設定

### 生產環境日誌架構

```python
from pretty_loguru import create_logger
import json
import socket

# 初始化基礎日誌記錄器
logger = create_logger(
    name="api_server",
    level="INFO", 
    log_path="logs"
)

# 目標 1：應用程式日誌（結構化 JSON）
logger.add(
    "logs/application.json",
    format=lambda record: json.dumps({
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "service": "api_server",
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
        "message": record["message"],
        "extra": record["extra"]
    }),
    level="INFO",
    rotation="50MB",
    retention="30 days"
)

# 目標 2：安全稽核日誌
logger.add(
    "logs/security.log",
    format="{time} | 安全 | {message} | {extra}",
    filter=lambda record: "security" in record["extra"],
    level="INFO",
    rotation="daily",
    retention="365 days"  # 保留安全日誌更長時間
)

# 目標 3：效能監控
logger.add(
    "logs/performance.log",
    format="{time} | 效能 | {message} | 持續時間: {extra[duration]} | {extra}",
    filter=lambda record: "performance" in record["extra"],
    level="INFO",
    rotation="daily"
)

# 目標 4：關鍵警報（立即通知）
def send_alert(message):
    """發送關鍵警報到監控系統"""
    try:
        # 範例：發送到監控服務
        alert_data = {
            "service": "api_server",
            "severity": "critical",
            "message": message,
            "timestamp": "now"
        }
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.sendto(json.dumps(alert_data).encode(), ('monitoring-server', 514))
        print(f"警報已發送: {message}")
    except Exception as e:
        print(f"發送警報失敗: {e}")

logger.add(
    send_alert,
    format="{message}",
    level="CRITICAL",
    filter=lambda record: record["level"].name == "CRITICAL"
)

# 使用範例
logger.info("伺服器已啟動")

# 安全日誌
logger.bind(security=True, user_id="user123", action="login").info("用戶認證成功")

# 效能日誌
logger.bind(performance=True, duration=0.245, endpoint="/api/users").info("API 請求已處理")

# 關鍵警報
logger.critical("資料庫連接中斷 - 需要立即處理")
```

## 🌐 遠端目標整合

### Syslog 整合

```python
import socket
import json
from pretty_loguru import create_logger

# 建立日誌記錄器
logger = create_logger(
    name="syslog_demo",
    level="INFO"
)

def syslog_handler(message):
    """發送日誌到 syslog 伺服器"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # RFC3164 格式: <priority>timestamp hostname tag: message
        syslog_msg = f"<134>{message}"  # 134 = facility 16 (local0) + severity 6 (info)
        sock.sendto(syslog_msg.encode(), ('syslog-server', 514))
        sock.close()
    except Exception as e:
        print(f"Syslog 錯誤: {e}")

# 添加 syslog 目標
logger.add(
    syslog_handler,
    format="{time:MMM DD HH:mm:ss} api-server pretty-loguru: {level} {message}",
    level="WARNING"  # 僅警告及以上發送到 syslog
)

logger.warning("這條訊息會發送到 syslog")
```

### ELK Stack 整合

```python
import json
import requests
from pretty_loguru import create_logger

# 建立日誌記錄器
logger = create_logger(
    name="elk_demo",
    level="INFO"
)

def elasticsearch_handler(record):
    """發送日誌到 Elasticsearch"""
    try:
        doc = {
            "@timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "service": "api_server",
            "module": record["name"],
            "function": record["function"],
            "line": record["line"],
            "message": record["message"],
            "extra": record["extra"]
        }
        
        # 發送到 Elasticsearch
        response = requests.post(
            'http://elasticsearch:9200/logs/_doc',
            json=doc,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Elasticsearch 錯誤: {e}")

# 添加 Elasticsearch 目標
logger.add(
    elasticsearch_handler,
    format="{message}",  # 我們在處理器中處理格式
    level="INFO"
)

logger.info("日誌已發送到 Elasticsearch")
```

## 🔄 動態目標管理

### 執行時期目標配置

```python
from pretty_loguru import create_logger
import os
from typing import Dict, Any

class TargetManager:
    def __init__(self):
        self.logger = create_logger(name="managed", level="INFO")
        self.targets: Dict[str, int] = {}
    
    def add_target(self, name: str, **config) -> bool:
        """添加新的日誌目標"""
        try:
            handler_id = self.logger.add(**config)
            self.targets[name] = handler_id
            self.logger.info(f"已添加日誌目標: {name}")
            return True
        except Exception as e:
            self.logger.error(f"添加目標 {name} 失敗: {e}")
            return False
    
    def remove_target(self, name: str) -> bool:
        """移除日誌目標"""
        if name in self.targets:
            try:
                self.logger.remove(self.targets[name])
                del self.targets[name]
                self.logger.info(f"已移除日誌目標: {name}")
                return True
            except Exception as e:
                self.logger.error(f"移除目標 {name} 失敗: {e}")
                return False
        return False
    
    def list_targets(self) -> list:
        """列出活動目標"""
        return list(self.targets.keys())

# 使用方式
target_manager = TargetManager()

# 根據環境添加目標
environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'development':
    target_manager.add_target(
        "dev_console",
        sink=lambda msg: print(f"[開發] {msg}", end=""),
        level="DEBUG",
        colorize=True
    )

if environment in ['staging', 'production']:
    target_manager.add_target(
        "app_file",
        sink="logs/app.log",
        level="INFO",
        rotation="50MB",
        retention="30 days"
    )
    
    target_manager.add_target(
        "error_file",
        sink="logs/errors.log",
        level="ERROR",
        rotation="10MB"
    )

# 執行時期目標管理
if os.getenv('ENABLE_DEBUG_LOG') == 'true':
    target_manager.add_target(
        "debug_file",
        sink="logs/debug.log",
        level="DEBUG",
        rotation="daily"
    )

target_manager.logger.info(f"活動目標: {target_manager.list_targets()}")
```

### 配置驅動的目標

```python
import json
from pretty_loguru import create_logger

def load_logging_config(config_file: str):
    """從 JSON 檔案載入並應用日誌配置"""
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    logger = create_logger(name="configured", level="INFO")
    
    # 移除現有處理器
    logger.remove()
    
    # 從配置添加目標
    for target_name, target_config in config.get('targets', {}).items():
        try:
            logger.add(**target_config)
            logger.info(f"已配置目標: {target_name}")
        except Exception as e:
            print(f"配置目標 {target_name} 失敗: {e}")
    
    return logger

# 範例配置檔案 (logging_config.json):
config_example = {
    "targets": {
        "console": {
            "sink": "sys.stderr",
            "format": "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
            "level": "INFO",
            "colorize": True
        },
        "application_log": {
            "sink": "logs/app.log",
            "format": "{time} | {level} | {name}:{function}:{line} - {message}",
            "level": "DEBUG",
            "rotation": "50MB",
            "retention": "14 days"
        },
        "error_log": {
            "sink": "logs/errors.log",
            "format": "{time} | {level} | {name}:{function}:{line} - {message} | {extra}",
            "level": "ERROR",
            "rotation": "daily",
            "retention": "90 days"
        }
    }
}

# 儲存範例配置
with open('logging_config.json', 'w') as f:
    json.dump(config_example, f, indent=2)

# 載入配置
logger = load_logging_config('logging_config.json')

logger.debug("除錯訊息")
logger.info("資訊訊息")
logger.error("錯誤訊息")
```

## 📊 目標效能監控

### 測量目標效能

```python
import time
from pretty_loguru import create_logger
from contextlib import contextmanager

class PerformanceTarget:
    def __init__(self, sink, **kwargs):
        self.sink = sink
        self.kwargs = kwargs
        self.message_count = 0
        self.total_time = 0
        
    def __call__(self, message):
        start_time = time.time()
        
        if callable(self.sink):
            result = self.sink(message)
        else:
            # 處理檔案 sinks
            with open(self.sink, 'a') as f:
                f.write(str(message) + '\n')
            result = None
            
        self.total_time += time.time() - start_time
        self.message_count += 1
        
        return result
    
    @property
    def average_time(self):
        return self.total_time / self.message_count if self.message_count > 0 else 0

# 建立效能監控的目標
console_target = PerformanceTarget(lambda msg: print(msg, end=""))
file_target = PerformanceTarget("logs/perf_test.log")

# 建立日誌記錄器並添加目標
logger = create_logger(name="perf_test", level="INFO")
logger.add(console_target, level="INFO")
logger.add(file_target, level="DEBUG")

# 產生測試日誌
for i in range(100):
    logger.info(f"測試訊息 {i}")

print(f"控制台平均時間: {console_target.average_time:.6f}s")
print(f"檔案平均時間: {file_target.average_time:.6f}s")
```

## 🎭 條件式目標路由

### 基於內容的路由

```python
from pretty_loguru import create_logger

# 建立日誌記錄器
logger = create_logger(
    name="content_routing",
    level="INFO"
)

# 定義路由函式
def route_database_logs(record):
    """將資料庫相關日誌路由到特定檔案"""
    return "database" in record["message"].lower() or "db" in record.get("extra", {})

def route_api_logs(record):
    """將 API 相關日誌路由到特定檔案"""
    return "api" in record["message"].lower() or "endpoint" in record.get("extra", {})

def route_security_logs(record):
    """將安全相關日誌路由到特定檔案"""
    return any(keyword in record["message"].lower() for keyword in ["auth", "login", "security", "unauthorized"])

# 添加條件式目標
logger.add(
    "logs/database.log",
    filter=route_database_logs,
    level="DEBUG",
    rotation="daily"
)

logger.add(
    "logs/api.log",
    filter=route_api_logs,
    level="INFO",
    rotation="50MB"
)

logger.add(
    "logs/security.log",
    filter=route_security_logs,
    level="WARNING",
    rotation="daily",
    retention="365 days"
)

# 測試路由
logger.info("資料庫連接已建立")           # → database.log
logger.info("API 端點 /users 被呼叫")     # → api.log
logger.warning("未授權的存取嘗試")        # → security.log
logger.info("一般應用程式訊息")           # → 一般日誌（如果有配置）
```

基於目標的日誌為需要複雜日誌管理策略的複雜應用程式提供了最大的靈活性！