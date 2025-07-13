# 日誌輪換

日誌輪換是管理日誌檔案大小和數量的重要機制，pretty-loguru 提供靈活且強大的輪換策略。

## 🎯 配置模板輪換預設

Pretty-Loguru 提供了預定義的輪換配置模板，透過 `ConfigTemplates` 快速設定常用的時間輪換策略：

### 每日輪換 (daily)

```python
from pretty_loguru import ConfigTemplates

# 每日輪換配置
config = ConfigTemplates.daily()
logger = config.apply_to("daily_app")

# 配置內容：
# - rotation: "00:00" (每天午夜輪換)
# - retention: "30 days" (保留 30 天)
# - 當前檔名: [component]daily_latest.temp.log
# - 輪換後壓縮檔名: [component]YYYYMMDD.log
```

### 每小時輪換 (hourly)

```python
# 每小時輪換配置
config = ConfigTemplates.hourly()
logger = config.apply_to("hourly_app")

# 配置內容：
# - rotation: "1 hour" (每小時輪換)
# - retention: "7 days" (保留 7 天)
# - 當前檔名: [component]hourly_latest.temp.log
# - 輪換後壓縮檔名: [component]YYYYMMDD_HH.log
```

### 每週輪換 (weekly)

```python
# 每週輪換配置
config = ConfigTemplates.weekly()
logger = config.apply_to("weekly_app")

# 配置內容：
# - rotation: "monday" (每週一輪換)
# - retention: "12 weeks" (保留 12 週)
# - 當前檔名: [component]weekly_latest.temp.log
# - 輪換後壓縮檔名: [component]week_YYYYWNN.log
```

### 每月輪換 (monthly)

```python
# 每月輪換配置
config = ConfigTemplates.monthly()
logger = config.apply_to("monthly_app")

# 配置內容：
# - rotation: "1 month" (每月輪換)
# - retention: "12 months" (保留 12 個月)
# - 當前檔名: [component]monthly_latest.temp.log
# - 輪換後壓縮檔名: [component]YYYYMM.log
```

### 每分鐘輪換 (minute)

```python
# 每分鐘輪換配置（適用於高頻測試）
config = ConfigTemplates.minute()
logger = config.apply_to("minute_app")

# 配置內容：
# - rotation: "1 minute" (每分鐘輪換)
# - retention: "24 hours" (保留 24 小時)
# - 當前檔名: [component]minute_latest.temp.log
# - 輪換後壓縮檔名: [component]YYYYMMDD_HHMM.log
```

### 檔案命名規則

時間類輪換預設使用固定的檔名，在輪換時才根據時間範圍重新命名：

| 預設類型 | 當前檔名 | 輪換後檔名格式 | 輪換後範例 |
|---------|---------|--------------|-----------|
| daily | `[{name}]daily_latest.temp.log` | `[{name}]{date}.log` | `[myapp]20250113.log` |
| hourly | `[{name}]hourly_latest.temp.log` | `[{name}]{date}_{hour}.log` | `[myapp]20250113_14.log` |
| weekly | `[{name}]weekly_latest.temp.log` | `[{name}]week_{year}W{week_num}.log` | `[myapp]week_2025W03.log` |
| monthly | `[{name}]monthly_latest.temp.log` | `[{name}]{year}{month}.log` | `[myapp]202501.log` |
| minute | `[{name}]minute_latest.temp.log` | `[{name}]{date}_{hour}{minute}.log` | `[myapp]20250113_1430.log` |

**說明**：
- 當前正在寫入的日誌檔案使用 `xxx_latest.temp.log` 格式
- 當觸發輪換時，檔案會根據該檔案記錄的時間範圍重新命名
- 例如：`[myapp]daily_latest.temp.log` 在次日午夜輪換時會變成 `[myapp]20250113.log`

### 自訂輪換配置

可以基於預設配置進行自訂：

```python
from pretty_loguru import ConfigTemplates

# 基於每日輪換，但修改保留時間
config = ConfigTemplates.daily()
config.update(retention="60 days")  # 保留 60 天而非預設的 30 天

# 基於每小時輪換，但修改壓縮格式
config = ConfigTemplates.hourly()
config.update(compression_format="backup_{name}_{date}_{hour}")
```

## 🔄 輪換策略

### 大小基礎輪換

根據檔案大小自動輪換：

```python
from pretty_loguru import create_logger

# 10MB 輪換
logger = create_logger(
    name="size_rotation",
    log_path="logs/app.log",
    rotation="10 MB"
)

# 其他大小單位
logger = create_logger(rotation="500 KB")  # 500 KB
logger = create_logger(rotation="1 GB")    # 1 GB
logger = create_logger(rotation=1048576)   # 1MB (位元組)
```

### 時間基礎輪換

根據時間間隔自動輪換：

```python
# 每日輪換（午夜）
logger = create_logger(
    name="daily_rotation",
    rotation="daily"
)

# 每週輪換
logger = create_logger(rotation="weekly")

# 每月輪換
logger = create_logger(rotation="monthly")

# 自訂時間間隔
logger = create_logger(rotation="2 hours")   # 每2小時
logger = create_logger(rotation="30 minutes") # 每30分鐘
logger = create_logger(rotation="1 week")    # 每週
```

### 特定時間輪換

在特定時間點進行輪換：

```python
# 每天凌晨2點輪換
logger = create_logger(rotation="daily at 02:00")

# 每週一凌晨輪換
logger = create_logger(rotation="weekly on monday at 00:00")

# 每月1號輪換
logger = create_logger(rotation="monthly on 1st at 00:00")
```

## 🗂️ 保留策略

### 數量保留

```python
# 保留最近 10 個檔案
logger = create_logger(
    name="count_retention",
    rotation="10 MB",
    retention=10
)
```

### 時間保留

```python
# 保留 30 天內的檔案
logger = create_logger(
    name="time_retention",
    rotation="daily",
    retention="30 days"
)

# 其他時間單位
logger = create_logger(retention="1 week")   # 1週
logger = create_logger(retention="6 months") # 6個月
logger = create_logger(retention="2 years")  # 2年
```

### 複合保留策略

```python
# 保留7天內的檔案，或最多50個檔案
logger = create_logger(
    name="hybrid_retention",
    rotation="daily",
    retention=["7 days", 50]
)
```

## 🗜️ 壓縮選項

### 啟用壓縮

```python
# gzip 壓縮（推薦）
logger = create_logger(
    name="compressed",
    rotation="daily",
    retention="30 days",
    compression="gz"
)

# zip 壓縮
logger = create_logger(compression="zip")

# bz2 壓縮（高壓縮率）
logger = create_logger(compression="bz2")

# xz 壓縮（最高壓縮率）
logger = create_logger(compression="xz")
```

### 壓縮效益

不同壓縮方式的特性：

- **gzip (.gz)**: 平衡的壓縮率和速度，推薦使用
- **zip (.zip)**: 相容性好，壓縮率中等
- **bz2 (.bz2)**: 高壓縮率，但較慢
- **xz (.xz)**: 最高壓縮率，最慢

## 📁 檔案命名模式

### 預設命名

```python
# 預設模式：app_2023-12-07_12-30-45_123456.log
logger = create_logger(
    name="app",
    rotation="1 hour"
)
```

### 自訂命名

```python
# 自訂檔案名稱模式
logger = create_logger(
    name="custom_naming",
    log_path="logs/app_{time:YYYY-MM-DD}.log",
    rotation="daily"
)

# 結果：app_2023-12-07.log, app_2023-12-08.log, ...
```

## 🎯 實際應用場景

### 開發環境

```python
# 開發環境：快速輪換，短期保留
dev_logger = create_logger(
    name="development",
    log_path="logs/dev/app.log",
    rotation="50 MB",      # 適中的檔案大小
    retention="3 days",    # 短期保留
    compression=None       # 不壓縮，便於即時查看
)
```

### 測試環境

```python
# 測試環境：按測試週期輪換
test_logger = create_logger(
    name="testing",
    log_path="logs/test/app.log",
    rotation="daily",      # 每日輪換
    retention="1 week",    # 保留一週
    compression="gz"       # 輕量壓縮
)
```

### 生產環境

```python
# 生產環境：嚴格的輪換和保留策略
prod_logger = create_logger(
    name="production",
    log_path="/var/log/app/app.log",
    rotation="100 MB",     # 較大檔案減少輪換頻率
    retention="90 days",   # 長期保留
    compression="gz"       # 壓縮節省空間
)
```

### 高流量應用

```python
# 高流量：頻繁輪換，自動清理
high_traffic_logger = create_logger(
    name="high_traffic",
    log_path="logs/traffic/app.log",
    rotation="1 hour",     # 每小時輪換
    retention="7 days",    # 一週內的數據
    compression="gz"       # 必須壓縮
)
```

## 📊 監控和維護

### 輪換狀態監控

```python
import os
from pathlib import Path

def monitor_log_files(log_dir):
    """監控日誌檔案狀態"""
    log_path = Path(log_dir)
    
    if not log_path.exists():
        return
    
    files = list(log_path.glob("*.log*"))
    total_size = sum(f.stat().st_size for f in files)
    
    print(f"日誌檔案數量: {len(files)}")
    print(f"總大小: {total_size / 1024 / 1024:.2f} MB")
    
    # 檢查最舊的檔案
    if files:
        oldest = min(files, key=lambda f: f.stat().st_mtime)
        print(f"最舊檔案: {oldest.name}")

# 使用監控
monitor_log_files("logs/app")
```

### 清理腳本

```bash
#!/bin/bash
# cleanup_logs.sh - 手動清理腳本

LOG_DIR="/var/log/myapp"
DAYS=30

# 刪除 30 天前的壓縮檔案
find $LOG_DIR -name "*.gz" -mtime +$DAYS -delete

# 刪除空目錄
find $LOG_DIR -type d -empty -delete

echo "日誌清理完成"
```

## ⚠️ 注意事項

### 磁碟空間管理

```python
# 監控磁碟空間，調整保留策略
import shutil

def get_disk_usage(path):
    """獲取磁碟使用情況"""
    total, used, free = shutil.disk_usage(path)
    return {
        'total_gb': total // (1024**3),
        'used_gb': used // (1024**3),
        'free_gb': free // (1024**3),
        'usage_percent': (used / total) * 100
    }

# 根據磁碟空間調整策略
disk_info = get_disk_usage("/var/log")
if disk_info['usage_percent'] > 80:
    # 磁碟空間不足，縮短保留期
    logger = create_logger(retention="7 days")
else:
    # 空間充足，正常保留
    logger = create_logger(retention="30 days")
```

### 權限設定

```python
import os

# 確保日誌目錄權限正確
log_dir = "/var/log/myapp"
os.makedirs(log_dir, mode=0o755, exist_ok=True)

# 設定檔案權限
logger = create_logger(
    name="secure_app",
    log_path=f"{log_dir}/app.log",
    rotation="daily",
    # 確保日誌檔案安全
    enqueue=True  # 避免多程序衝突
)
```

## 📚 最佳實踐

1. **選擇合適的輪換策略**：
   - 低流量應用：大小基礎輪換
   - 高流量應用：時間基礎輪換
   - 調試階段：頻繁輪換，短期保留

2. **壓縮策略**：
   - 生產環境必須啟用壓縮
   - 開發環境可選擇不壓縮

3. **保留期限**：
   - 根據合規要求設定保留期
   - 考慮磁碟空間限制

4. **監控維護**：
   - 定期檢查日誌檔案大小
   - 監控磁碟空間使用情況
   - 設定自動化清理任務

## 🔗 相關資源

- [自定義配置](./custom-config) - 完整配置選項
- [效能最佳化](./performance) - 性能調優
- [範例集合](../examples/) - 實際使用範例