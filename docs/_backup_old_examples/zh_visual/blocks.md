# Rich 區塊範例

Rich 區塊是 pretty-loguru 最實用的視覺化功能，本頁面將展示各種 Rich 區塊的實際應用。

## 🎯 基本用法

### 簡單區塊

```python
from pretty_loguru import create_logger

# 初始化日誌系統
logger = create_logger(
    name="blocks_demo",
    log_path="blocks_demo",
    level="INFO"
)

# 最基本的區塊
logger.block(
    "基本資訊",
    [
        "應用名稱: MyApp",
        "版本: 1.1.0",
        "作者: 開發團隊"
    ]
)
```

### 帶樣式的區塊

```python
# 成功狀態的綠色區塊
logger.block(
    "啟動成功",
    [
        "✅ 配置載入完成",
        "✅ 資料庫連接成功",
        "✅ 服務已啟動"
    ],
    border_style="green",
    log_level="SUCCESS"
)
```

## 🎨 邊框樣式展示

### 不同顏色的邊框

```python
def demo_border_colors():
    """展示不同顏色的邊框效果"""
    
    # 綠色 - 成功狀態
    logger.block(
        "成功狀態",
        [
            "✅ 所有檢查通過",
            "✅ 系統運行正常",
            "✅ 準備就緒"
        ],
        border_style="green"
    )
    
    # 黃色 - 警告狀態  
    logger.block(
        "警告狀態",
        [
            "⚠️  記憶體使用率 75%",
            "⚠️  建議監控負載",
            "💡 考慮擴展資源"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    # 紅色 - 錯誤狀態
    logger.block(
        "錯誤狀態", 
        [
            "❌ 服務連接失敗",
            "❌ 資料庫無回應",
            "🔧 需要立即處理"
        ],
        border_style="red",
        log_level="ERROR"
    )
    
    # 藍色 - 資訊狀態
    logger.block(
        "系統資訊",
        [
            "🖥️  作業系統: Linux",
            "🐍 Python 版本: 3.9",
            "📦 套件版本: 1.1.0"
        ],
        border_style="blue"
    )
    
    # 紫色 - 特殊狀態
    logger.block(
        "特殊事件",
        [
            "🎉 達成里程碑",
            "📊 性能提升 20%",
            "🚀 準備發布"
        ],
        border_style="magenta"
    )
    
    # 青色 - 開發狀態
    logger.block(
        "開發資訊",
        [
            "🔧 除錯模式: 開啟",
            "📝 日誌級別: DEBUG",
            "🌐 環境: Development"
        ],
        border_style="cyan"
    )
```

### 不同邊框樣式

```python
def demo_border_styles():
    """展示不同的邊框樣式"""
    
    # 實線邊框
    logger.block(
        "實線邊框",
        ["這是實線邊框的效果"],
        border_style="solid"
    )
    
    # 雙線邊框
    logger.block(
        "雙線邊框",
        ["這是雙線邊框的效果"],
        border_style="double"
    )
    
    # 圓角邊框
    logger.block(
        "圓角邊框",
        ["這是圓角邊框的效果"],
        border_style="rounded"
    )
    
    # 粗線邊框
    logger.block(
        "粗線邊框",
        ["這是粗線邊框的效果"],
        border_style="thick"
    )
```

## 📊 實際應用場景

### 系統監控儀表板

```python
import psutil
import datetime

def system_monitoring_dashboard():
    """系統監控儀表板"""
    
    # 獲取系統資訊
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # CPU 監控
    cpu_color = "red" if cpu_percent > 80 else "yellow" if cpu_percent > 60 else "green"
    logger.block(
        "CPU 監控",
        [
            f"🖥️  使用率: {cpu_percent:.1f}%",
            f"⚡ 核心數: {psutil.cpu_count()}",
            f"🌡️  狀態: {'過載' if cpu_percent > 80 else '正常'}"
        ],
        border_style=cpu_color
    )
    
    # 記憶體監控
    memory_color = "red" if memory.percent > 80 else "yellow" if memory.percent > 60 else "green"
    logger.block(
        "記憶體監控",
        [
            f"💾 使用率: {memory.percent:.1f}%",
            f"📊 已使用: {memory.used // 1024 // 1024 // 1024}GB",
            f"📈 總容量: {memory.total // 1024 // 1024 // 1024}GB",
            f"🔄 可用: {memory.available // 1024 // 1024 // 1024}GB"
        ],
        border_style=memory_color
    )
    
    # 磁碟監控
    disk_color = "red" if disk.percent > 90 else "yellow" if disk.percent > 70 else "green"
    logger.block(
        "磁碟監控",
        [
            f"💿 使用率: {disk.percent:.1f}%",
            f"📦 已使用: {disk.used // 1024 // 1024 // 1024}GB",
            f"📂 總容量: {disk.total // 1024 // 1024 // 1024}GB",
            f"🆓 可用: {disk.free // 1024 // 1024 // 1024}GB"
        ],
        border_style=disk_color
    )
    
    # 監控摘要
    overall_status = "green" if all([
        cpu_percent < 70,
        memory.percent < 70, 
        disk.percent < 80
    ]) else "yellow"
    
    logger.block(
        "監控摘要",
        [
            f"🕐 檢查時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"📊 整體狀態: {'健康' if overall_status == 'green' else '需要關注'}",
            f"🔄 下次檢查: 5 分鐘後"
        ],
        border_style=overall_status
    )
```

### 應用程式配置報告

```python
def application_config_report(config):
    """應用程式配置報告"""
    
    logger.block(
        "應用程式配置",
        [
            f"📱 應用名稱: {config.get('app_name', 'Unknown')}",
            f"🏷️  版本: {config.get('version', '1.1.0')}",
            f"🌍 環境: {config.get('environment', 'development')}",
            f"🔧 除錯模式: {'開啟' if config.get('debug', False) else '關閉'}"
        ],
        border_style="blue"
    )
    
    logger.block(
        "伺服器配置",
        [
            f"🌐 主機: {config.get('host', 'localhost')}",
            f"🚪 埠號: {config.get('port', 8000)}",
            f"👥 工作進程: {config.get('workers', 1)}",
            f"⏱️  超時: {config.get('timeout', 30)}秒"
        ],
        border_style="cyan"
    )
    
    logger.block(
        "資料庫配置",
        [
            f"🗄️  類型: {config.get('db_type', 'PostgreSQL')}",
            f"🔗 主機: {config.get('db_host', 'localhost')}",
            f"📊 資料庫: {config.get('db_name', 'app_db')}",
            f"🔐 連接池: {config.get('db_pool_size', 10)}"
        ],
        border_style="green"
    )
```

### 部署流程報告

```python
def deployment_progress_report(deployment_steps):
    """部署流程進度報告"""
    
    completed_steps = []
    failed_steps = []
    pending_steps = []
    
    for step_name, status in deployment_steps.items():
        if status == "completed":
            completed_steps.append(f"✅ {step_name}")
        elif status == "failed":
            failed_steps.append(f"❌ {step_name}")
        else:
            pending_steps.append(f"⏳ {step_name}")
    
    # 已完成的步驟
    if completed_steps:
        logger.block(
            "已完成步驟",
            completed_steps,
            border_style="green"
        )
    
    # 失敗的步驟
    if failed_steps:
        logger.block(
            "失敗步驟",
            failed_steps,
            border_style="red",
            log_level="ERROR"
        )
    
    # 待執行的步驟
    if pending_steps:
        logger.block(
            "待執行步驟",
            pending_steps,
            border_style="yellow"
        )
    
    # 部署摘要
    total_steps = len(deployment_steps)
    completed_count = len(completed_steps)
    failed_count = len(failed_steps)
    
    summary_color = "green" if failed_count == 0 else "red"
    logger.block(
        "部署摘要",
        [
            f"📊 總步驟: {total_steps}",
            f"✅ 已完成: {completed_count}",
            f"❌ 失敗: {failed_count}",
            f"📈 成功率: {(completed_count/total_steps)*100:.1f}%"
        ],
        border_style=summary_color
    )
```

### API 請求統計

```python
def api_request_statistics(stats):
    """API 請求統計報告"""
    
    # 請求概覽
    logger.block(
        "請求概覽",
        [
            f"📊 總請求數: {stats['total_requests']:,}",
            f"✅ 成功請求: {stats['successful_requests']:,}",
            f"❌ 失敗請求: {stats['failed_requests']:,}",
            f"📈 成功率: {stats['success_rate']:.2f}%"
        ],
        border_style="blue"
    )
    
    # 響應時間統計
    response_time_color = "red" if stats['avg_response_time'] > 1000 else "yellow" if stats['avg_response_time'] > 500 else "green"
    logger.block(
        "響應時間統計",
        [
            f"⚡ 平均響應時間: {stats['avg_response_time']:.2f}ms",
            f"🚀 最快響應: {stats['min_response_time']:.2f}ms",
            f"🐌 最慢響應: {stats['max_response_time']:.2f}ms",
            f"📊 中位數: {stats['median_response_time']:.2f}ms"
        ],
        border_style=response_time_color
    )
    
    # 錯誤統計
    if stats['failed_requests'] > 0:
        logger.block(
            "錯誤分析",
            [
                f"🔴 4xx 錯誤: {stats['client_errors']:,}",
                f"🔴 5xx 錯誤: {stats['server_errors']:,}",
                f"📊 錯誤率: {stats['error_rate']:.2f}%",
                f"🔍 主要錯誤: {stats['top_error']}"
            ],
            border_style="red",
            log_level="WARNING"
        )
```

## 🔧 進階技巧

### 動態內容生成

```python
def dynamic_service_status(services):
    """動態生成服務狀態報告"""
    
    healthy_services = []
    unhealthy_services = []
    
    for service, health in services.items():
        if health['status'] == 'healthy':
            healthy_services.append(f"✅ {service}: {health['uptime']}")
        else:
            unhealthy_services.append(f"❌ {service}: {health['error']}")
    
    # 健康服務
    if healthy_services:
        logger.block(
            "健康服務",
            healthy_services,
            border_style="green"
        )
    
    # 異常服務
    if unhealthy_services:
        logger.block(
            "異常服務",
            unhealthy_services,
            border_style="red",
            log_level="ERROR"
        )
    
    # 服務摘要
    total_services = len(services)
    healthy_count = len(healthy_services)
    
    logger.block(
        "服務摘要",
        [
            f"📊 服務總數: {total_services}",
            f"✅ 健康服務: {healthy_count}",
            f"❌ 異常服務: {total_services - healthy_count}",
            f"📈 健康率: {(healthy_count/total_services)*100:.1f}%"
        ],
        border_style="green" if healthy_count == total_services else "yellow"
    )
```

### 條件式樣式

```python
def conditional_styling_example(metrics):
    """根據指標值動態調整樣式"""
    
    # 根據 CPU 使用率選擇顏色
    cpu_usage = metrics['cpu_usage']
    if cpu_usage > 90:
        cpu_color = "red"
        cpu_level = "CRITICAL"
    elif cpu_usage > 70:
        cpu_color = "yellow"
        cpu_level = "WARNING"
    else:
        cpu_color = "green"
        cpu_level = "INFO"
    
    logger.block(
        f"CPU 狀態 ({cpu_level})",
        [
            f"使用率: {cpu_usage}%",
            f"負載: {metrics['load_average']}",
            f"進程數: {metrics['process_count']}"
        ],
        border_style=cpu_color,
        log_level=cpu_level
    )
```

## 💡 最佳實踐

### 1. 保持內容簡潔

```python
# 推薦 - 簡潔明瞭
logger.block(
    "狀態檢查",
    [
        "API: 正常",
        "DB: 正常", 
        "Redis: 正常"
    ],
    border_style="green"
)

# 避免 - 內容過於冗長
logger.block(
    "非常詳細的系統狀態檢查報告",
    [
        "API 服務運行狀態正常，響應時間在可接受範圍內...",
        "資料庫連接池狀態良好，所有連接都可用..."
    ]
)
```

### 2. 使用有意義的顏色

```python
# 建立色彩規範
STATUS_COLORS = {
    "success": "green",
    "warning": "yellow", 
    "error": "red",
    "info": "blue",
    "debug": "cyan"
}

def status_report(status, message_list):
    logger.block(
        f"{status.upper()} 報告",
        message_list,
        border_style=STATUS_COLORS.get(status, "blue")
    )
```

### 3. 結合表情符號增強可讀性

```python
logger.block(
    "系統健康檢查",
    [
        "🖥️  CPU: 正常",
        "💾 記憶體: 正常",
        "💿 磁碟: 警告",
        "🌐 網路: 正常"
    ],
    border_style="yellow"  # 因為有警告項目
)
```

## 🚀 完整範例

把所有技巧結合在一起的完整範例：

```python
def complete_blocks_demo():
    """Rich 區塊功能完整展示"""
    
    logger = create_logger(
    name="blocks_demo",
    log_path="complete_blocks_demo",
    level="INFO"
)
    
    # 1. 基本資訊
    logger.block(
        "應用程式資訊",
        [
            "名稱: Pretty Loguru Demo",
            "版本: 1.1.0",
            "作者: 開發團隊"
        ],
        border_style="blue"
    )
    
    # 2. 系統狀態
    logger.block(
        "系統狀態",
        [
            "✅ CPU: 25% (正常)",
            "✅ 記憶體: 60% (正常)", 
            "⚠️  磁碟: 85% (接近滿載)",
            "✅ 網路: 正常"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    # 3. 服務檢查
    logger.block(
        "服務檢查",
        [
            "✅ Web Server: 運行中",
            "✅ Database: 連接正常",
            "✅ Redis: 快取可用",
            "✅ Queue: 處理中"
        ],
        border_style="green",
        log_level="SUCCESS"
    )
    
    # 4. 錯誤報告 (如果有的話)
    logger.block(
        "最近錯誤",
        [
            "❌ 2024-06-30 15:30: 連接超時",
            "❌ 2024-06-30 15:25: 記憶體不足",
            "🔧 建議: 檢查網路和擴展記憶體"
        ],
        border_style="red",
        log_level="ERROR"
    )

if __name__ == "__main__":
    complete_blocks_demo()
```

這個完整的範例展示了 Rich 區塊的所有主要功能和最佳實踐。你可以直接運行這些程式碼來查看實際效果！