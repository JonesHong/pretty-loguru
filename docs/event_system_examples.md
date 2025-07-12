# Pretty Loguru 事件系統使用指南

## 概述

Pretty Loguru 提供了一個簡潔的發布/訂閱事件系統，允許不同模組間進行解耦通信。此系統是執行緒安全的，適用於複雜的應用場景。

## 核心功能

### 基本 API

```python
from pretty_loguru.core.event_system import subscribe, post_event, unsubscribe

# 訂閱事件
subscribe("event_name", callback_function)

# 發布事件
post_event("event_name", *args, **kwargs)

# 取消訂閱
unsubscribe("event_name", callback_function)
```

## 內建事件

### 1. Logger 註冊事件

當新的 Logger 被註冊到系統中時觸發。

```python
from pretty_loguru.core.event_system import subscribe
from pretty_loguru import create_logger

def on_logger_registered(name, logger):
    print(f"新的 Logger 已註冊: {name}")
    print(f"Logger 類型: {type(logger)}")

# 訂閱 logger 註冊事件
subscribe("logger_registered", on_logger_registered)

# 創建 logger 將觸發事件
logger = create_logger("my_app")
# 輸出: 新的 Logger 已註冊: my_app
```

### 2. Logger 更新事件

當現有的 Logger 被更新時觸發。

```python
def on_logger_updated(name, new_logger):
    print(f"Logger '{name}' 已更新")
    print(f"新的 Logger 實例: {id(new_logger)}")

subscribe("logger_updated", on_logger_updated)

# 重新創建同名 logger 將觸發更新事件
updated_logger = create_logger("my_app", force_new_instance=True)
```

## 使用範例

### 範例 1: Logger 監控系統

創建一個監控系統來追蹤所有 Logger 的創建和使用：

```python
from pretty_loguru.core.event_system import subscribe
from pretty_loguru import create_logger
from datetime import datetime
from typing import Dict, Any

class LoggerMonitor:
    def __init__(self):
        self.logger_registry: Dict[str, Dict[str, Any]] = {}
        
        # 訂閱相關事件
        subscribe("logger_registered", self.on_logger_registered)
        subscribe("logger_updated", self.on_logger_updated)
    
    def on_logger_registered(self, name: str, logger):
        """處理 Logger 註冊事件"""
        self.logger_registry[name] = {
            'logger': logger,
            'created_at': datetime.now(),
            'updated_at': None,
            'update_count': 0
        }
        print(f"📝 Logger '{name}' 已註冊於 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def on_logger_updated(self, name: str, new_logger):
        """處理 Logger 更新事件"""
        if name in self.logger_registry:
            self.logger_registry[name]['logger'] = new_logger
            self.logger_registry[name]['updated_at'] = datetime.now()
            self.logger_registry[name]['update_count'] += 1
            
            update_count = self.logger_registry[name]['update_count']
            print(f"🔄 Logger '{name}' 已更新 (第 {update_count} 次更新)")
    
    def get_stats(self):
        """獲取監控統計"""
        total_loggers = len(self.logger_registry)
        updated_loggers = sum(1 for info in self.logger_registry.values() if info['updated_at'])
        
        return {
            'total_loggers': total_loggers,
            'updated_loggers': updated_loggers,
            'logger_names': list(self.logger_registry.keys())
        }

# 使用監控系統
monitor = LoggerMonitor()

# 創建一些 logger
app_logger = create_logger("app")
db_logger = create_logger("database") 
cache_logger = create_logger("cache")

# 更新一個 logger
updated_app_logger = create_logger("app", force_new_instance=True)

# 查看統計
stats = monitor.get_stats()
print(f"統計: {stats}")
```

### 範例 2: 自定義事件系統

創建應用特定的事件：

```python
from pretty_loguru.core.event_system import subscribe, post_event
from pretty_loguru import create_logger

class DatabaseConnectionManager:
    def __init__(self):
        self.logger = create_logger("db_manager")
        
        # 訂閱連接事件
        subscribe("db_connected", self.on_db_connected)
        subscribe("db_disconnected", self.on_db_disconnected)
    
    def connect(self):
        """模擬資料庫連接"""
        # 執行連接邏輯...
        connection_info = {"host": "localhost", "port": 5432, "database": "myapp"}
        
        # 發布連接事件
        post_event("db_connected", connection_info)
    
    def disconnect(self):
        """模擬資料庫斷開"""
        # 執行斷開邏輯...
        post_event("db_disconnected", reason="manual_disconnect")
    
    def on_db_connected(self, connection_info):
        """處理資料庫連接事件"""
        self.logger.info(f"資料庫已連接: {connection_info}")
    
    def on_db_disconnected(self, reason):
        """處理資料庫斷開事件"""
        self.logger.warning(f"資料庫已斷開，原因: {reason}")

# 創建其他監聽器
def audit_db_events(event_type, **kwargs):
    audit_logger = create_logger("audit")
    audit_logger.info(f"資料庫審計: {event_type} - {kwargs}")

subscribe("db_connected", lambda info: audit_db_events("連接", info=info))
subscribe("db_disconnected", lambda reason: audit_db_events("斷開", reason=reason))

# 使用
db_manager = DatabaseConnectionManager()
db_manager.connect()    # 觸發連接事件
db_manager.disconnect() # 觸發斷開事件
```

### 範例 3: 效能監控事件

```python
from pretty_loguru.core.event_system import subscribe, post_event
import time
import functools

def performance_monitor(func):
    """效能監控裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            raise
        finally:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            # 發布效能事件
            post_event("function_executed", {
                'function_name': func.__name__,
                'execution_time': execution_time,
                'success': success,
                'error': error,
                'args_count': len(args),
                'kwargs_count': len(kwargs)
            })
        
        return result
    return wrapper

# 效能事件監聽器
def log_performance_event(event_data):
    perf_logger = create_logger("performance")
    
    func_name = event_data['function_name']
    exec_time = event_data['execution_time']
    success = event_data['success']
    
    if success:
        perf_logger.info(f"✅ {func_name} 執行完成，耗時: {exec_time:.4f}秒")
    else:
        perf_logger.error(f"❌ {func_name} 執行失敗，耗時: {exec_time:.4f}秒，錯誤: {event_data['error']}")

subscribe("function_executed", log_performance_event)

# 使用範例
@performance_monitor
def slow_function():
    time.sleep(0.1)  # 模擬耗時操作
    return "完成"

@performance_monitor
def failing_function():
    raise ValueError("模擬錯誤")

# 測試
slow_function()     # 觸發效能事件
try:
    failing_function()  # 觸發錯誤事件
except ValueError:
    pass
```

## 最佳實踐

### 1. 事件命名慣例

```python
# ✅ 好的事件命名
"logger_registered"     # 明確的動作
"db_connection_lost"    # 具體的狀態變化
"user_login_success"    # 包含結果

# ❌ 避免的命名
"event1"               # 不具描述性
"stuff_happened"       # 太模糊
"update"              # 太通用
```

### 2. 錯誤處理

```python
def safe_event_handler(data):
    """安全的事件處理器，包含錯誤處理"""
    try:
        # 處理事件的邏輯
        process_event_data(data)
    except Exception as e:
        # 記錄錯誤但不拋出，避免影響其他監聽器
        error_logger = create_logger("event_errors")
        error_logger.error(f"事件處理失敗: {e}")

subscribe("my_event", safe_event_handler)
```

### 3. 避免記憶體洩漏

```python
class EventSubscriber:
    def __init__(self):
        self.callbacks = []
        
    def subscribe_to_events(self):
        """訂閱事件時記錄回調函數"""
        callback = self.handle_event
        subscribe("my_event", callback)
        self.callbacks.append(("my_event", callback))
    
    def cleanup(self):
        """清理時取消所有訂閱"""
        for event_name, callback in self.callbacks:
            unsubscribe(event_name, callback)
        self.callbacks.clear()
    
    def handle_event(self, data):
        # 處理事件...
        pass
```

### 4. 執行緒安全考慮

事件系統本身是執行緒安全的，但事件處理器需要注意執行緒安全：

```python
import threading

class ThreadSafeEventHandler:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}
    
    def handle_event(self, event_data):
        """執行緒安全的事件處理"""
        with self.lock:
            # 安全地修改共享資料
            self.data.update(event_data)

subscribe("shared_data_update", ThreadSafeEventHandler().handle_event)
```

## 注意事項

1. **避免循環依賴**: 確保事件處理器不會觸發導致無限循環的事件
2. **保持處理器輕量**: 事件處理器應該快速執行，避免阻塞系統
3. **錯誤隔離**: 一個處理器的錯誤不應該影響其他處理器
4. **資源清理**: 長期運行的應用應該適當清理不再需要的事件訂閱

## 調試事件系統

```python
from pretty_loguru.core.event_system import list_events, list_listeners

# 查看所有註冊的事件
events = list_events()
print(f"已註冊的事件: {events}")

# 查看特定事件的監聽器數量
listeners = list_listeners("logger_registered")
print(f"logger_registered 事件有 {len(listeners)} 個監聽器")
```

事件系統為 Pretty Loguru 提供了強大的擴展能力，允許用戶在不修改核心代碼的情況下添加自定義功能。合理使用事件系統可以讓您的應用更加模組化和可維護。