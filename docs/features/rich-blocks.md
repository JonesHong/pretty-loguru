# Rich 區塊日誌

Rich 區塊是 pretty-loguru 最實用的功能之一，它讓你能夠建立結構化、美觀的日誌輸出，特別適合展示系統狀態、配置資訊或錯誤報告。

## 🎯 基本用法

### 簡單區塊

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_dir="logs",
    level="INFO"
)

logger.block(
    "基本資訊",
    [
        "應用名稱: MyApp",
        "版本: 1.1.2",
        "啟動時間: 2024-06-30 10:30:00"
    ]
)
```

### 帶樣式的區塊

```python
logger.block(
    "系統狀態",
    [
        "CPU: 25%",
        "記憶體: 2.1GB / 8GB", 
        "磁碟: 150GB 可用"
    ],
    border_style="green",    # 綠色邊框
    level="INFO"             # 日誌級別
)
```

## 🎨 邊框樣式

Rich 支援多種邊框樣式，每種都有不同的視覺效果：

### 實線邊框

```python
logger.block(
    "實線邊框",
    ["這是實線邊框的範例"],
    border_style="solid"
)
```

### 雙線邊框

```python
logger.block(
    "雙線邊框", 
    ["這是雙線邊框的範例"],
    border_style="double"
)
```

### 圓角邊框

```python
logger.block(
    "圓角邊框",
    ["這是圓角邊框的範例"], 
    border_style="rounded"
)
```

### 粗線邊框

```python
logger.block(
    "粗線邊框",
    ["這是粗線邊框的範例"],
    border_style="thick"
)
```

## 🌈 顏色主題

使用不同顏色來表達不同的含義：

### 成功狀態（綠色）

```python
logger.block(
    "部署成功",
    [
        "✅ 程式碼部署完成",
        "✅ 資料庫遷移完成", 
        "✅ 服務健康檢查通過",
        "✅ 負載均衡器已更新"
    ],
    border_style="green",
    level="SUCCESS"
)
```

### 警告狀態（黃色）

```python
logger.block(
    "性能警告",
    [
        "⚠️  CPU 使用率: 85%",
        "⚠️  記憶體使用率: 90%",
        "⚠️  回應時間: 2.5秒",
        "💡 建議: 擴展服務實例"
    ],
    border_style="yellow",
    level="WARNING"
)
```

### 錯誤狀態（紅色）

```python
logger.block(
    "系統錯誤",
    [
        "❌ 資料庫連接失敗",
        "❌ Redis 服務無回應",
        "❌ 外部 API 超時",
        "🔧 修復建議: 檢查網路連接"
    ],
    border_style="red", 
    level="ERROR"
)
```

### 資訊狀態（藍色）

```python
logger.block(
    "系統資訊",
    [
        "🖥️  作業系統: Ubuntu 20.04",
        "🐍 Python 版本: 3.9.7",
        "📦 套件版本: pretty-loguru 1.1.2",
        "🌐 網路介面: eth0"
    ],
    border_style="blue",
    level="INFO"
)
```

## 📊 實際應用場景

### 應用啟動報告

```python
def log_startup_info():
    import os
    import psutil
    
    logger.block(
        "應用啟動報告",
        [
            f"🚀 應用名稱: {os.environ.get('APP_NAME', 'MyApp')}",
            f"📅 啟動時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🆔 程序 ID: {os.getpid()}", 
            f"💾 可用記憶體: {psutil.virtual_memory().available // 1024 // 1024}MB",
            f"🖥️  CPU 核心數: {psutil.cpu_count()}",
            f"🌐 工作目錄: {os.getcwd()}"
        ],
        border_style="cyan",
        level="INFO"
    )
```

### 資料庫連接狀態

```python
def log_database_status(connections):
    status_items = []
    overall_status = "green"
    
    for db_name, is_connected in connections.items():
        if is_connected:
            status_items.append(f"✅ {db_name}: 連接正常")
        else:
            status_items.append(f"❌ {db_name}: 連接失敗")
            overall_status = "red"
    
    logger.block(
        "資料庫連接狀態",
        status_items,
        border_style=overall_status,
        level="INFO" if overall_status == "green" else "ERROR"
    )
```

### 效能監控報告

```python
def log_performance_metrics():
    import psutil
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # 根據使用率決定顏色
    if cpu_percent > 80 or memory.percent > 80:
        border_color = "red"
        level = "WARNING"
    elif cpu_percent > 60 or memory.percent > 60:
        border_color = "yellow" 
        level = "WARNING"
    else:
        border_color = "green"
        level = "INFO"
    
    logger.block(
        "系統效能監控",
        [
            f"🖥️  CPU 使用率: {cpu_percent:.1f}%",
            f"💾 記憶體使用: {memory.percent:.1f}% ({memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB)",
            f"💿 磁碟使用: {disk.percent:.1f}% ({disk.free // 1024 // 1024 // 1024}GB 可用)",
            f"📊 負載平均: {', '.join(map(str, os.getloadavg()))}" if hasattr(os, 'getloadavg') else "📊 負載平均: N/A"
        ],
        border_style=border_color,
        level=level
    )
```

## 🔧 進階技巧

### 動態內容

```python
def log_user_activity(users_online, recent_actions):
    content = [
        f"👥 線上使用者: {users_online}",
        "📈 最近活動:"
    ]
    
    # 動態添加最近動作
    for action in recent_actions[-5:]:  # 只顯示最近5個
        content.append(f"   • {action}")
    
    logger.block(
        "使用者活動摘要",
        content,
        border_style="cyan"
    )
```

### 條件式樣式

```python
def log_service_health(services):
    all_healthy = all(status == "healthy" for status in services.values())
    
    content = []
    for service, status in services.items():
        icon = "✅" if status == "healthy" else "❌"
        content.append(f"{icon} {service}: {status}")
    
    logger.block(
        "服務健康檢查",
        content,
        border_style="green" if all_healthy else "red",
        level="INFO" if all_healthy else "ERROR"
    )
```

## 📝 最佳實踐

### 1. 保持內容簡潔
每行內容應該簡潔明瞭，避免過長的文字。

### 2. 使用適當的顏色
- 🟢 綠色：成功、正常狀態
- 🟡 黃色：警告、需要注意
- 🔴 紅色：錯誤、失敗狀態  
- 🔵 藍色：一般資訊
- 🟣 紫色：特殊事件
- 🟠 橙色：進行中的操作

### 3. 使用表情符號增強可讀性
適當使用表情符號可以讓日誌更加直觀易讀。

### 4. 群組相關資訊
將相關的資訊放在同一個區塊中，提高資訊的組織性。

## 🚀 下一步

- [探索 ASCII 藝術標題](./ascii-art) - 更加引人注目的標題
- [了解 ASCII 藝術區塊](./ascii-blocks) - 結合兩種功能的強大效果
- [查看完整範例](../examples/visual/blocks) - 更多實際應用場景

Rich 區塊讓你的日誌不再單調，開始建立專業級的日誌輸出吧！ 🎨
