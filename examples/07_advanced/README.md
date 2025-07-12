# 🔬 07_advanced - 進階功能

歡迎來到進階功能學習！這個模組針對有經驗的開發者，教您如何深度自定義 pretty-loguru，開發插件，並進行性能調優。

## 🎯 學習目標

完成本節後，您將：
- ✅ 掌握自定義格式器開發
- ✅ 學會性能調優和優化技巧
- ✅ 理解事件系統和插件架構
- ✅ 能夠開發自己的日誌擴展

## 📚 範例列表（建議順序）

### 🎨 Step 1: custom_formatters.py - 自定義格式器
**⏱️ 預估時間：20分鐘**

```bash
python custom_formatters.py
```

**學習重點**：
- 格式器接口和實現
- 自定義日誌格式設計
- 動態格式切換
- 格式器鏈式處理

### ⚡ Step 2: performance_tuning.py - 性能調優
**⏱️ 預估時間：25分鐘**

```bash
python performance_tuning.py
```

**學習重點**：
- 日誌性能瓶頸分析
- 非同步日誌處理
- 內存和 I/O 優化
- 大量日誌場景處理

### 🎪 Step 3: event_system.py - 事件系統
**⏱️ 預估時間：18分鐘**

```bash
python event_system.py
```

**學習重點**：
- 日誌事件監聽
- 自定義事件觸發
- 事件驅動的日誌處理
- 回調函數設計

### 🔌 Step 4: plugin_development.py - 插件開發
**⏱️ 預估時間：30分鐘**

```bash
python plugin_development.py
```

**學習重點**：
- 插件架構設計
- 插件接口定義
- 插件載入和管理
- 社群插件開發

## 🎮 進階開發測試

```bash
# 運行所有進階範例
python custom_formatters.py && \
python performance_tuning.py && \
python event_system.py && \
python plugin_development.py

# 性能基準測試
python -m timeit -s "from custom_formatters import *" "test_performance()"
```

## 💡 進階開發模式

### 自定義格式器
```python
from pretty_loguru.formats import BaseFormatter
from datetime import datetime

class CustomJSONFormatter(BaseFormatter):
    """自定義 JSON 格式器"""
    
    def format(self, record):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.level.name,
            "message": record.message,
            "module": record.module,
            "function": record.function,
            "line": record.line,
            "extra": record.extra
        }
    
    def serialize(self, data):
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)

# 使用自定義格式器
logger = create_logger(
    name="custom_format",
    formatter=CustomJSONFormatter()
)
```

### 性能優化策略
```python
import asyncio
from collections import deque
from threading import Thread
import queue

class AsyncLogHandler:
    """非同步日誌處理器"""
    
    def __init__(self, batch_size=100, flush_interval=5.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.log_queue = queue.Queue()
        self.buffer = deque()
        self.running = True
        
        # 啟動後台處理線程
        self.worker = Thread(target=self._process_logs)
        self.worker.start()
    
    def _process_logs(self):
        """後台處理日誌"""
        import time
        last_flush = time.time()
        
        while self.running:
            try:
                # 批次處理日誌
                log_record = self.log_queue.get(timeout=1.0)
                self.buffer.append(log_record)
                
                # 達到批次大小或時間間隔則刷新
                now = time.time()
                if (len(self.buffer) >= self.batch_size or 
                    now - last_flush >= self.flush_interval):
                    self._flush_buffer()
                    last_flush = now
                    
            except queue.Empty:
                continue
    
    def _flush_buffer(self):
        """刷新緩衝區"""
        if self.buffer:
            # 批次寫入日誌
            batch = list(self.buffer)
            self.buffer.clear()
            self._write_batch(batch)
```

### 事件系統
```python
from typing import Callable, Dict, List
import asyncio

class LogEventSystem:
    """日誌事件系統"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable):
        """註冊事件監聽器"""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    async def emit(self, event: str, data: dict):
        """觸發事件"""
        if event in self.listeners:
            tasks = []
            for callback in self.listeners[event]:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(data))
                else:
                    callback(data)
            
            if tasks:
                await asyncio.gather(*tasks)

# 使用事件系統
event_system = LogEventSystem()

@event_system.on('error_logged')
async def send_alert(data):
    """錯誤日誌警報"""
    if data.get('level') == 'ERROR':
        # 發送警報通知
        await send_notification(f"錯誤發生: {data['message']}")

@event_system.on('log_written')
def update_metrics(data):
    """更新日誌指標"""
    metrics.increment('logs_written', tags={'level': data['level']})
```

### 插件架構
```python
from abc import ABC, abstractmethod
import importlib
from pathlib import Path

class LogPlugin(ABC):
    """日誌插件基類"""
    
    @abstractmethod
    def initialize(self, logger):
        """初始化插件"""
        pass
    
    @abstractmethod
    def process_log(self, record):
        """處理日誌記錄"""
        pass
    
    def cleanup(self):
        """清理資源"""
        pass

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: List[LogPlugin] = []
    
    def load_plugin(self, plugin_path: str):
        """載入插件"""
        module = importlib.import_module(plugin_path)
        plugin_class = getattr(module, 'Plugin')
        plugin = plugin_class()
        self.plugins.append(plugin)
        return plugin
    
    def load_plugins_from_directory(self, directory: Path):
        """從目錄載入所有插件"""
        for plugin_file in directory.glob("*.py"):
            if plugin_file.name.startswith("plugin_"):
                module_name = plugin_file.stem
                self.load_plugin(f"plugins.{module_name}")
    
    def process_log_with_plugins(self, record):
        """使用所有插件處理日誌"""
        for plugin in self.plugins:
            record = plugin.process_log(record)
        return record

# 範例插件
class SentimentAnalysisPlugin(LogPlugin):
    """情感分析插件"""
    
    def initialize(self, logger):
        self.sentiment_analyzer = load_sentiment_model()
    
    def process_log(self, record):
        if record.level.name in ['ERROR', 'WARNING']:
            sentiment = self.sentiment_analyzer.analyze(record.message)
            record.extra['sentiment'] = sentiment
        return record
```

## 🔧 進階優化技巧

### 內存優化
```python
import sys
from pympler import tracker

def memory_efficient_logging():
    """內存高效的日誌記錄"""
    # 使用物件池
    log_record_pool = []
    
    def get_log_record():
        if log_record_pool:
            return log_record_pool.pop()
        return LogRecord()
    
    def return_log_record(record):
        record.reset()
        log_record_pool.append(record)
    
    # 監控內存使用
    memory_tracker = tracker.SummaryTracker()
    
    def log_memory_usage():
        memory_tracker.print_diff()
```

### 並發優化
```python
import threading
from concurrent.futures import ThreadPoolExecutor

class ConcurrentLogger:
    """並發安全的日誌記錄器"""
    
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.RLock()
    
    def log_async(self, level, message, **kwargs):
        """非同步日誌記錄"""
        future = self.executor.submit(self._log_sync, level, message, **kwargs)
        return future
    
    def _log_sync(self, level, message, **kwargs):
        """同步日誌記錄"""
        with self.lock:
            logger.log(level, message, **kwargs)
```

## ➡️ 下一步選擇

### 💼 企業級應用
**建議路徑**：[08_enterprise](../08_enterprise/) - 微服務和大規模部署

### 📚 深度學習
**建議閱讀**：[架構設計文件](../../docs/architecture/)

### 🤝 社群貢獻
**參與方式**：[貢獻指南](../../CONTRIBUTING.md)

## 📖 相關資源

- 🏗️ [架構設計](../../docs/architecture/design.md)
- ⚡ [性能指南](../../docs/performance/optimization.md)
- 🔌 [插件開發](../../docs/plugins/development.md)

---

**🔬 釋放 pretty-loguru 的全部潛力！**

進階功能讓您能夠創造出完全符合特定需求的日誌解決方案。