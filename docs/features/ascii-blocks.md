# ASCII 藝術區塊

ASCII 藝術區塊是 pretty-loguru 最強大的視覺化功能，它結合了 ASCII 藝術標題和 Rich 區塊的優勢，建立出既引人注目又資訊豐富的完整報告格式。

## 🎯 基本概念

ASCII 藝術區塊 = ASCII 藝術標題 + Rich 區塊內容

這種組合提供了：
- 醒目的 ASCII 藝術標題
- 結構化的內容展示
- 統一的視覺風格
- 完整的報告格式

## 🚀 基本用法

### 簡單的 ASCII 區塊

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_dir="logs",
    level="INFO"
)

logger.ascii_block(
    "系統狀態報告",           # 區塊標題
    [                      # 內容列表
        "CPU 使用率: 25%",
        "記憶體使用: 2.1GB", 
        "磁碟空間: 120GB 可用"
    ],
    header_text="STATUS",   # ASCII 標題文字
    font="standard",   # ASCII 字體
    border_style="green",    # 邊框顏色
    level="INFO"         # 日誌級別
)
```

### 完整參數範例

```python
logger.ascii_block(
    title="部署完成報告",
    content=[
        "應用版本: v2.1.0",
        "部署時間: 3分45秒",
        "服務檢查: 全部通過",
        "負載均衡: 已啟用"
    ],
    header_text="DEPLOYED",
    font="block",
    border_style="green",
    level="SUCCESS"
)
```

## 🎨 視覺效果展示

### 成功場景

```python
logger.ascii_block(
    "啟動完成報告",
    [
        "✅ 配置檔載入成功",
        "✅ 資料庫連接正常",
        "✅ Redis 快取就緒",
        "✅ API 服務啟動",
        "✅ 健康檢查通過"
    ],
    header_text="READY",
    font="slant",
    border_style="green",
    level="SUCCESS"
)
```

### 警告場景

```python
logger.ascii_block(
    "系統效能警告",
    [
        "⚠️  CPU 使用率: 87%",
        "⚠️  記憶體使用: 92%",
        "⚠️  磁碟 I/O: 高負載",
        "💡 建議: 擴展資源或優化程序"
    ],
    header_text="WARNING",
    font="doom",
    border_style="yellow",
    level="WARNING"
)
```

### 錯誤場景

```python
logger.ascii_block(
    "系統故障報告",
    [
        "❌ 資料庫連接失敗",
        "❌ Redis 服務無回應",
        "❌ API 健康檢查失敗",
        "🔧 修復動作: 重啟相關服務"
    ],
    header_text="ERROR",
    font="doom", 
    border_style="red",
    level="ERROR"
)
```

## 📊 實際應用場景

### 應用程式啟動序列

```python
def application_startup():
    logger.ascii_block(
        "啟動檢查清單",
        [
            "🔧 載入環境變數",
            "🔧 解析配置檔",
            "🔧 初始化日誌系統", 
            "🔧 建立資料庫連接池"
        ],
        header_text="STARTUP",
        font="slant",
        border_style="blue"
    )
    
    # 執行啟動邏輯...
    
    logger.ascii_block(
        "啟動完成摘要",
        [
            f"🚀 應用名稱: {app_name}",
            f"📦 版本: {app_version}",
            f"🌐 監聽埠: {port}",
            f"⏱️  啟動耗時: {startup_time}秒"
        ],
        header_text="ONLINE",
        font="block",
        border_style="green",
        level="SUCCESS"
    )
```

### 部署流程報告

```python
def deployment_report(deployment_info):
    logger.ascii_block(
        "部署執行報告",
        [
            f"📦 版本: {deployment_info['version']}",
            f"🌍 環境: {deployment_info['environment']}", 
            f"⏱️  部署時間: {deployment_info['duration']}",
            f"🔄 滾動更新: {deployment_info['rolling_update']}",
            f"✅ 健康檢查: {deployment_info['health_check']}",
            f"📊 成功率: {deployment_info['success_rate']}%"
        ],
        header_text="DEPLOYED",
        font="standard",
        border_style="green" if deployment_info['success_rate'] == 100 else "yellow",
        level="SUCCESS" if deployment_info['success_rate'] == 100 else "WARNING"
    )
```

### 資料處理管道

```python
def data_pipeline_summary(stats):
    logger.ascii_block(
        "資料處理完成報告",
        [
            f"📥 輸入記錄: {stats['input_records']:,}",
            f"✅ 處理成功: {stats['processed']:,}",
            f"❌ 處理失敗: {stats['failed']:,}",
            f"⏱️  處理時間: {stats['duration']}",
            f"🚀 處理速度: {stats['records_per_second']:,} 記錄/秒",
            f"💾 輸出大小: {stats['output_size']}"
        ],
        header_text="COMPLETE",
        font="block",
        border_style="green",
        level="SUCCESS"
    )
```

### 系統監控儀表板

```python
def system_health_dashboard():
    import psutil
    import datetime
    
    # 獲取系統資訊
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # 決定狀態顏色
    if cpu_percent > 80 or memory.percent > 80:
        color = "red"
        level = "WARNING"
        header = "ALERT"
    elif cpu_percent > 60 or memory.percent > 60:
        color = "yellow" 
        level = "WARNING"
        header = "CAUTION"
    else:
        color = "green"
        level = "INFO"
        header = "HEALTHY"
    
    logger.ascii_block(
        "系統健康監控",
        [
            f"🖥️  CPU 使用率: {cpu_percent:.1f}%",
            f"💾 記憶體使用: {memory.percent:.1f}% ({memory.used//1024//1024//1024}GB/{memory.total//1024//1024//1024}GB)",
            f"💿 磁碟使用: {disk.percent:.1f}% ({disk.free//1024//1024//1024}GB 可用)",
            f"⏰ 檢查時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🔄 系統運行時間: {get_uptime()}"
        ],
        header_text=header,
        font="standard",
        border_style=color,
        level=level
    )
```

### API 請求摘要

```python
def api_request_summary(request_stats):
    logger.ascii_block(
        "API 請求統計報告",
        [
            f"📊 總請求數: {request_stats['total']:,}",
            f"✅ 成功請求: {request_stats['success']:,} ({request_stats['success_rate']:.1f}%)",
            f"❌ 失敗請求: {request_stats['failed']:,} ({request_stats['error_rate']:.1f}%)",
            f"⚡ 平均響應時間: {request_stats['avg_response_time']:.2f}ms",
            f"🚀 最快響應: {request_stats['min_response_time']:.2f}ms",
            f"🐌 最慢響應: {request_stats['max_response_time']:.2f}ms"
        ],
        header_text="API STATS",
        font="small",
        border_style="blue",
        level="INFO"
    )
```

## 🔧 進階技巧

### 動態內容生成

```python
def dynamic_status_report(services):
    content = []
    all_healthy = True
    
    for service, status in services.items():
        if status['healthy']:
            content.append(f"✅ {service}: 正常運行")
        else:
            content.append(f"❌ {service}: {status['error']}")
            all_healthy = False
    
    # 添加統計資訊
    healthy_count = sum(1 for s in services.values() if s['healthy'])
    total_count = len(services)
    content.append(f"📊 健康服務: {healthy_count}/{total_count}")
    
    logger.ascii_block(
        "服務健康檢查",
        content,
        header_text="HEALTHY" if all_healthy else "ISSUES",
        font="slant",
        border_style="green" if all_healthy else "red",
        level="SUCCESS" if all_healthy else "ERROR"
    )
```

### 條件式格式

```python
def build_result_report(build_success, test_results, deployment_ready):
    # 根據結果決定整體狀態
    if build_success and all(test_results.values()) and deployment_ready:
        header = "SUCCESS"
        color = "green"
        level = "SUCCESS"
    elif build_success:
        header = "PARTIAL"
        color = "yellow"
        level = "WARNING"  
    else:
        header = "FAILED"
        color = "red"
        level = "ERROR"
    
    content = [
        f"🔨 建構狀態: {'成功' if build_success else '失敗'}",
        f"🧪 單元測試: {'通過' if test_results.get('unit', False) else '失敗'}",
        f"🔗 整合測試: {'通過' if test_results.get('integration', False) else '失敗'}",
        f"🚀 部署就緒: {'是' if deployment_ready else '否'}"
    ]
    
    logger.ascii_block(
        "建構與測試報告",
        content,
        header_text=header,
        font="doom",
        border_style=color,
        level=level
    )
```

### 多階段進度報告

```python
class ProgressTracker:
    def __init__(self, total_stages):
        self.total_stages = total_stages
        self.current_stage = 0
        self.completed_stages = []
    
    def complete_stage(self, stage_name, details):
        self.current_stage += 1
        self.completed_stages.append(stage_name)
        
        progress_content = []
        
        # 顯示已完成的階段
        for completed in self.completed_stages:
            progress_content.append(f"✅ {completed}")
        
        # 顯示當前進度
        progress_content.append(f"📊 進度: {self.current_stage}/{self.total_stages}")
        
        # 添加詳細資訊
        if details:
            progress_content.extend(details)
        
        logger.ascii_block(
            f"階段 {self.current_stage} 完成",
            progress_content,
            header_text=f"STAGE {self.current_stage}",
            font="small",
            border_style="cyan",
            level="SUCCESS"
        )
        
        # 如果全部完成
        if self.current_stage == self.total_stages:
            logger.ascii_block(
                "所有階段完成",
                [f"🎉 {stage} 已完成" for stage in self.completed_stages],
                header_text="COMPLETE",
                font="block",
                border_style="green",
                level="SUCCESS"
            )

# 使用範例
tracker = ProgressTracker(3)
tracker.complete_stage("資料載入", ["載入 10,000 筆記錄", "驗證資料格式"])
tracker.complete_stage("資料處理", ["轉換格式", "清理重複項"])
tracker.complete_stage("資料輸出", ["匯出 CSV", "生成報告"])
```

## ⚠️ 使用建議

### 內容組織

```python
# 推薦 - 內容簡潔有條理
logger.ascii_block(
    "部署狀態",
    [
        "版本: v1.2.0",
        "環境: Production", 
        "狀態: 成功"
    ],
    header_text="DEPLOY",
    font="slant"
)

# 不推薦 - 內容過於冗長
logger.ascii_block(
    "非常詳細的部署狀態報告包含所有可能的資訊",
    [
        "這是一個非常長的內容行，包含了太多的資訊，可能會影響視覺效果...",
        "又是一行很長的內容..."
    ],
    header_text="VERY LONG HEADER",
    font="standard"
)
```

### 顏色使用原則

```python
# 成功 - 綠色
logger.ascii_block(..., border_style="green", level="SUCCESS")

# 警告 - 黃色
logger.ascii_block(..., border_style="yellow", level="WARNING")

# 錯誤 - 紅色  
logger.ascii_block(..., border_style="red", level="ERROR")

# 資訊 - 藍色
logger.ascii_block(..., border_style="blue", level="INFO")

# 特殊 - 紫色/青色
logger.ascii_block(..., border_style="magenta", level="INFO")
```

## 🚀 下一步

ASCII 藝術區塊是 pretty-loguru 最強大的功能，現在你可以：

- [查看完整的視覺化範例](../examples/visual/) - 所有視覺功能的實際應用
- [了解 Rich 區塊](./rich-blocks) - 純 Rich 區塊的詳細用法  
- [探索整合應用](../integrations/) - 在 Web 應用中使用這些功能
- [深入 API 文件](../api/) - 完整的參數和選項說明

開始建立專業級的日誌報告系統吧！