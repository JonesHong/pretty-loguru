# 06_advanced - 進階功能和底層庫直接存取

這個目錄展示 pretty-loguru 的進階功能，包括底層庫的直接存取、自訂擴展和專業整合技巧。

## 🎯 學習目標

- 理解 Advanced API 模組的使用方式
- 掌握底層庫 (loguru, rich, art, pyfiglet) 的直接存取
- 學會創建自訂日誌擴展
- 了解事件系統和擴展系統的使用
- 掌握協議和類型系統的實際應用

## 📚 範例列表

### 1. direct_library_access.py - 底層庫直接存取
**學習重點**: 使用 Advanced API 直接存取 loguru, rich 等庫

```bash
python direct_library_access.py
```

**功能展示**:
- 直接使用 loguru 的進階功能
- 原生 Rich 組件使用
- Art 和 PyFiglet 的直接調用
- 庫可用性檢查和條件使用

### 2. custom_extensions.py - 自訂擴展開發
**學習重點**: 開發自己的 logger 擴展和自訂功能

```bash
python custom_extensions.py
```

**功能展示**:
- 自訂 logger 方法開發
- 擴展系統的使用
- 自訂格式化器
- 動態功能註冊

### 3. event_system.py - 事件系統使用
**學習重點**: 利用內建事件系統進行高級控制

```bash
python event_system.py
```

**功能展示**:
- 事件監聽和觸發
- 日誌生命週期事件
- 自訂事件處理器
- 事件驅動的功能

### 4. protocols_and_types.py - 協議和類型系統
**學習重點**: 使用類型系統進行安全的擴展開發

```bash
python protocols_and_types.py
```

**功能展示**:
- EnhancedLogger 協議使用
- 類型安全的擴展開發
- 協議實作範例
- 泛型日誌組件

## 🔧 Advanced API 概覽

### 底層庫直接存取
```python
from pretty_loguru.advanced import loguru, rich, art, pyfiglet
from pretty_loguru.advanced import get_available_libraries

# 檢查可用庫
available = get_available_libraries()
if available['rich']:
    from pretty_loguru.advanced import Console, Table
    console = Console()
    
if available['loguru']:
    from pretty_loguru.advanced import loguru_logger
    loguru_logger.add("custom.log", level="DEBUG")
```

### 進階整合助手
```python
from pretty_loguru.advanced.helpers import create_rich_table_log
from pretty_loguru import create_logger

logger = create_logger("advanced_app")
data = [{"name": "Alice", "score": 95}]
create_rich_table_log(logger, "Scores", data)
```

## 🎨 進階使用模式

### 1. 混合使用模式
結合 pretty-loguru 的簡便性和底層庫的靈活性：

```python
from pretty_loguru import create_logger
from pretty_loguru.advanced import Console, Table

# 使用 pretty-loguru 的簡便性
logger = create_logger("hybrid_app", log_path="./logs")

# 使用 Rich 的原生功能進行複雜顯示
console = Console()
table = Table(title="Advanced Data")
# ... 複雜的表格配置
console.print(table)

# 結合使用
logger.info("表格已顯示")
```

### 2. 自訂擴展模式
為特定需求開發專用功能：

```python
from pretty_loguru.core.extension_system import register_extension_method

def custom_audit_log(logger_instance, action, user_id, **data):
    """自訂審計日誌方法"""
    audit_data = {
        "action": action,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        **data
    }
    logger_instance.info(f"AUDIT: {json.dumps(audit_data, ensure_ascii=False)}")

# 註冊自訂方法
register_extension_method("audit_log", custom_audit_log)

# 在 logger 上使用
logger = create_logger("audit_system")
logger.audit_log("user_login", user_id="12345", ip="192.168.1.100")
```

### 3. 事件驅動模式
使用事件系統進行高級控制：

```python
from pretty_loguru.core.event_system import subscribe_event, emit_event

def on_log_created(event_data):
    """當新日誌檔案創建時觸發"""
    print(f"新日誌檔案: {event_data['file_path']}")

# 訂閱事件
subscribe_event("log_file_created", on_log_created)

# 創建 logger 時會自動觸發事件
logger = create_logger("event_demo", log_path="./logs")
```

## 📁 實際應用場景

### 1. 企業級審計系統
```python
# 結合 pretty-loguru 和原生庫的企業審計方案
from pretty_loguru import create_logger
from pretty_loguru.advanced import loguru_logger, Console, Table

class EnterpriseAuditLogger:
    def __init__(self):
        self.logger = create_logger("audit", log_path="./audit_logs")
        self.console = Console()
        
        # 添加結構化日誌
        loguru_logger.add(
            "./audit_logs/structured_{time}.json",
            format="{time} | {level} | {message}",
            serialize=True,
            rotation="daily"
        )
    
    def log_user_action(self, action, user_data):
        # 結構化記錄
        self.logger.info(f"USER_ACTION: {action}", extra=user_data)
        
        # 即時顯示
        table = Table(title=f"用戶行為: {action}")
        for key, value in user_data.items():
            table.add_row(key, str(value))
        self.console.print(table)
```

### 2. 高性能監控系統
```python
# 使用底層庫的高性能監控
from pretty_loguru.advanced import loguru_logger, Live, Layout
from pretty_loguru import create_logger

class PerformanceMonitor:
    def __init__(self):
        self.logger = create_logger("monitor")
        self.live = Live()
        
        # 高性能異步日誌
        loguru_logger.add(
            "performance_{time}.log",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}",
            enqueue=True,  # 異步處理
            backtrace=True,
            diagnose=True
        )
    
    def start_monitoring(self):
        with self.live:
            # 實時性能監控顯示
            while True:
                metrics = self.collect_metrics()
                self.live.update(self.create_dashboard(metrics))
                self.logger.info(f"METRICS: {metrics}")
                time.sleep(1)
```

## 🚀 快速開始

1. **檢查進階功能可用性**:
   ```bash
   cd 06_advanced
   python direct_library_access.py
   ```

2. **開發自訂擴展**:
   ```bash
   python custom_extensions.py
   ```

3. **探索事件系統**:
   ```bash
   python event_system.py
   ```

4. **使用類型系統**:
   ```bash
   python protocols_and_types.py
   ```

## 💡 最佳實踐

### 1. 何時使用 Advanced API
- **需要底層庫的完整功能時**
- **開發可重用的日誌組件時**
- **需要最大性能和控制時**
- **整合第三方系統時**

### 2. 混合使用策略
- **日常操作**: 使用 pretty-loguru 的簡化 API
- **複雜顯示**: 使用 Rich 的原生功能
- **性能關鍵**: 直接使用 loguru 的高性能特性
- **特殊需求**: 開發自訂擴展

### 3. 擴展開發指南
- **保持 KISS 原則**: 擴展應該簡單易用
- **遵循現有模式**: 與 pretty-loguru 的 API 風格一致
- **提供文檔**: 清楚說明擴展的用途和使用方法
- **測試充分**: 確保擴展的穩定性和兼容性

## 🔗 相關範例

- **01_basics/** - 了解基本概念後再探索進階功能
- **02_visual/** - 視覺化功能的進階自訂
- **05_production/** - 生產環境的進階配置

## ❓ 常見問題

**Q: 何時應該使用 Advanced API？**
A: 當 pretty-loguru 的簡化 API 無法滿足特定需求時，如需要複雜的自訂格式化、高性能異步處理，或整合特殊系統。

**Q: Advanced API 會影響 pretty-loguru 的簡便性嗎？**
A: 不會。Advanced API 是可選的，不使用時不會影響正常的 pretty-loguru 使用體驗。

**Q: 如何確保自訂擴展的兼容性？**
A: 遵循 pretty-loguru 的擴展系統，使用提供的協議和類型系統，並進行充分測試。

**Q: 能否在同一個應用中混合使用簡化 API 和 Advanced API？**
A: 完全可以。這正是 Advanced API 的設計目標 - 在需要時提供更多控制，同時保持簡化 API 的便利性。