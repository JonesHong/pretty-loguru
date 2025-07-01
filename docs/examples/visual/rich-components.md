# Rich 組件範例

pretty-loguru 透過整合 Rich 庫，提供了豐富的視覺化組件。本頁面展示如何使用各種 Rich 組件來增強日誌輸出的視覺效果。

## 📊 表格組件

### 基本表格

```python
from pretty_loguru import create_logger
from rich.table import Table
from rich.console import Console

# 初始化日誌系統
logger = create_logger(
    name="rich-components_demo",
    log_path="rich_components_demo",
    level="INFO"
)

def system_status_table():
    """使用表格展示系統狀態"""
    
    # 建立表格
    table = Table(title="系統服務狀態", show_header=True, header_style="bold magenta")
    table.add_column("服務名稱", style="cyan", width=12)
    table.add_column("狀態", style="green", width=8)
    table.add_column("記憶體使用", style="yellow", width=10)
    table.add_column("CPU 使用", style="red", width=8)
    table.add_column("運行時間", style="blue", width=12)
    
    # 添加資料
    table.add_row("Web Server", "✅ 運行中", "245MB", "12%", "2天3小時")
    table.add_row("Database", "✅ 運行中", "1.2GB", "8%", "5天1小時")
    table.add_row("Redis", "✅ 運行中", "128MB", "3%", "2天3小時")
    table.add_row("Queue Worker", "⚠️ 警告", "456MB", "25%", "1天5小時")
    table.add_row("Log Service", "❌ 停止", "0MB", "0%", "已停止")
    
    # 使用 Rich console 輸出
    console = Console()
    console.print(table)
    
    logger.info("系統狀態表格已顯示")

system_status_table()
```

### 動態表格生成

```python
def create_performance_table(metrics):
    """根據性能指標動態建立表格"""
    
    table = Table(title="性能指標監控", show_header=True)
    table.add_column("指標名稱", style="cyan")
    table.add_column("當前值", style="magenta")
    table.add_column("閾值", style="yellow")
    table.add_column("狀態", style="bold")
    
    for metric_name, data in metrics.items():
        current = data['current']
        threshold = data['threshold']
        
        # 根據值決定狀態和顏色
        if current > threshold:
            status = "[red]❌ 超標[/red]"
        elif current > threshold * 0.8:
            status = "[yellow]⚠️ 警告[/yellow]"
        else:
            status = "[green]✅ 正常[/green]"
        
        table.add_row(
            metric_name,
            f"{current}{data.get('unit', '')}",
            f"{threshold}{data.get('unit', '')}",
            status
        )
    
    console = Console()
    console.print(table)

# 使用範例
metrics = {
    "CPU 使用率": {"current": 75, "threshold": 80, "unit": "%"},
    "記憶體使用": {"current": 6.5, "threshold": 8.0, "unit": "GB"},
    "磁碟使用": {"current": 45, "threshold": 90, "unit": "%"},
    "網路延遲": {"current": 25, "threshold": 100, "unit": "ms"}
}

create_performance_table(metrics)
```

## 🌳 樹狀結構

### 檔案系統結構

```python
from rich.tree import Tree

def show_project_structure():
    """顯示專案目錄結構"""
    
    tree = Tree("📁 my-project/", style="bold blue")
    
    # 原始碼目錄
    src = tree.add("📁 src/", style="cyan")
    src.add("📄 __init__.py")
    src.add("📄 main.py")
    src.add("📄 config.py")
    
    # 模組目錄
    modules = src.add("📁 modules/", style="cyan")
    modules.add("📄 auth.py")
    modules.add("📄 database.py")
    modules.add("📄 api.py")
    
    # 測試目錄
    tests = tree.add("📁 tests/", style="green")
    tests.add("📄 test_auth.py")
    tests.add("📄 test_database.py")
    tests.add("📄 test_api.py")
    
    # 文件
    docs = tree.add("📁 docs/", style="yellow")
    docs.add("📄 README.md")
    docs.add("📄 API.md")
    
    # 設定檔
    tree.add("📄 requirements.txt")
    tree.add("📄 .env")
    tree.add("📄 docker-compose.yml")
    
    console = Console()
    console.print(tree)
    
    logger.info("專案結構樹狀圖已顯示")

show_project_structure()
```

### 組織架構圖

```python
def show_team_structure():
    """顯示團隊組織架構"""
    
    team = Tree("👥 開發團隊", style="bold magenta")
    
    # 前端團隊
    frontend = team.add("🎨 前端團隊", style="cyan")
    frontend.add("👤 張三 (組長)")
    frontend.add("👤 李四 (React 開發)")
    frontend.add("👤 王五 (UI/UX)")
    
    # 後端團隊
    backend = team.add("⚙️ 後端團隊", style="green")
    backend.add("👤 趙六 (組長)")
    backend.add("👤 錢七 (API 開發)")
    backend.add("👤 孫八 (資料庫)")
    
    # DevOps 團隊
    devops = team.add("🚀 DevOps 團隊", style="yellow")
    devops.add("👤 周九 (組長)")
    devops.add("👤 吳十 (CI/CD)")
    
    console = Console()
    console.print(team)

show_team_structure()
```

## 📈 進度條

### 任務進度顯示

```python
from rich.progress import Progress, TaskID
import time

def show_deployment_progress():
    """顯示部署進度"""
    
    with Progress() as progress:
        # 建立多個任務
        build_task = progress.add_task("🔨 建構應用...", total=100)
        test_task = progress.add_task("🧪 執行測試...", total=100)
        deploy_task = progress.add_task("🚀 部署到生產...", total=100)
        
        # 模擬建構過程
        for i in range(100):
            time.sleep(0.02)
            progress.update(build_task, advance=1)
        
        logger.success("應用建構完成")
        
        # 模擬測試過程
        for i in range(100):
            time.sleep(0.01)
            progress.update(test_task, advance=1)
        
        logger.success("測試執行完成")
        
        # 模擬部署過程
        for i in range(100):
            time.sleep(0.03)
            progress.update(deploy_task, advance=1)
        
        logger.success("部署完成")

show_deployment_progress()
```

### 資料處理進度

```python
def process_data_with_progress(data_items):
    """帶進度條的資料處理"""
    
    with Progress() as progress:
        task = progress.add_task("📊 處理資料中...", total=len(data_items))
        
        processed_count = 0
        error_count = 0
        
        for item in data_items:
            try:
                # 模擬資料處理
                time.sleep(0.1)
                # process_item(item)
                processed_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f"處理失敗: {item}")
            
            progress.update(task, advance=1)
        
        # 完成後顯示統計
        logger.block(
            "資料處理完成",
            [
                f"📊 總計: {len(data_items)} 項",
                f"✅ 成功: {processed_count} 項",
                f"❌ 失敗: {error_count} 項",
                f"📈 成功率: {(processed_count/len(data_items)*100):.1f}%"
            ],
            border_style="green" if error_count == 0 else "yellow"
        )

# 使用範例
data = list(range(50))  # 模擬 50 個資料項目
process_data_with_progress(data)
```

## 📋 面板

### 資訊面板

```python
from rich.panel import Panel
from rich.align import Align

def show_system_info():
    """顯示系統資訊面板"""
    
    system_info = """
🖥️  作業系統: Linux Ubuntu 20.04
🐍 Python 版本: 3.9.7
💾 記憶體: 16GB DDR4
💿 儲存空間: 512GB SSD
🌐 網路: 1Gbps 乙太網路
    """
    
    panel = Panel(
        Align.center(system_info),
        title="💻 系統資訊",
        title_align="center",
        border_style="blue",
        padding=(1, 2)
    )
    
    console = Console()
    console.print(panel)

show_system_info()
```

### 警告面板

```python
def show_warning_panel(message, details):
    """顯示警告面板"""
    
    warning_content = f"""
⚠️  {message}

詳細資訊:
{chr(10).join(f"• {detail}" for detail in details)}
    """
    
    panel = Panel(
        warning_content,
        title="🚨 系統警告",
        border_style="yellow",
        padding=(1, 2)
    )
    
    console = Console()
    console.print(panel)

# 使用範例
show_warning_panel(
    "系統資源使用率偏高",
    [
        "CPU 使用率達到 87%",
        "記憶體使用率達到 92%", 
        "建議關閉不必要的程序",
        "考慮升級硬體配置"
    ]
)
```

## 📊 統計圖表

### 簡單長條圖

```python
from rich.console import Console
from rich.table import Table

def show_usage_statistics(stats):
    """顯示使用量統計的長條圖"""
    
    table = Table(title="📊 API 端點使用統計", show_header=True)
    table.add_column("端點", style="cyan", width=20)
    table.add_column("使用次數", style="green", width=10)
    table.add_column("使用率圖表", style="yellow", width=30)
    
    max_count = max(stats.values())
    
    for endpoint, count in stats.items():
        # 建立簡單的長條圖
        bar_length = int((count / max_count) * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        table.add_row(
            endpoint,
            f"{count:,}",
            f"{bar} {count/sum(stats.values())*100:.1f}%"
        )
    
    console = Console()
    console.print(table)

# 使用範例
api_stats = {
    "/api/users": 15420,
    "/api/orders": 8965,
    "/api/products": 12350,
    "/api/auth": 25680,
    "/api/payments": 4520
}

show_usage_statistics(api_stats)
```

### 狀態分佈圖

```python
def show_response_status_distribution(status_counts):
    """顯示 HTTP 響應狀態分佈"""
    
    table = Table(title="📈 HTTP 響應狀態分佈", show_header=True)
    table.add_column("狀態碼", style="cyan")
    table.add_column("描述", style="white")
    table.add_column("數量", style="green")
    table.add_column("百分比", style="yellow")
    table.add_column("視覺化", style="blue")
    
    total = sum(status_counts.values())
    status_descriptions = {
        200: "成功",
        404: "未找到",
        500: "伺服器錯誤",
        401: "未授權",
        403: "禁止訪問"
    }
    
    for status, count in sorted(status_counts.items()):
        percentage = (count / total) * 100
        bar_length = int(percentage / 5)  # 每 5% 一個方塊
        bar = "█" * bar_length
        
        # 根據狀態碼選擇顏色
        if status < 300:
            bar = f"[green]{bar}[/green]"
        elif status < 400:
            bar = f"[yellow]{bar}[/yellow]"
        else:
            bar = f"[red]{bar}[/red]"
        
        table.add_row(
            str(status),
            status_descriptions.get(status, "其他"),
            f"{count:,}",
            f"{percentage:.1f}%",
            bar
        )
    
    console = Console()
    console.print(table)

# 使用範例
response_stats = {
    200: 45230,
    404: 1250,
    500: 89,
    401: 520,
    403: 156
}

show_response_status_distribution(response_stats)
```

## 🎨 樣式和主題

### 自定義樣式

```python
from rich.style import Style
from rich.text import Text

def show_styled_output():
    """展示各種樣式效果"""
    
    console = Console()
    
    # 文字樣式
    console.print("這是 [bold]粗體[/bold] 文字")
    console.print("這是 [italic]斜體[/italic] 文字")
    console.print("這是 [underline]底線[/underline] 文字")
    console.print("這是 [strike]刪除線[/strike] 文字")
    
    # 顏色樣式
    console.print("這是 [red]紅色[/red] 文字")
    console.print("這是 [green]綠色[/green] 文字")
    console.print("這是 [blue]藍色[/blue] 文字")
    console.print("這是 [yellow]黃色[/yellow] 文字")
    
    # 背景顏色
    console.print("這是 [white on red]白字紅底[/white on red] 文字")
    console.print("這是 [black on yellow]黑字黃底[/black on yellow] 文字")
    
    # 組合樣式
    console.print("這是 [bold red on white]粗體紅字白底[/bold red on white] 文字")

show_styled_output()
```

### 狀態指示器

```python
def show_status_indicators():
    """顯示各種狀態指示器"""
    
    console = Console()
    
    # 成功狀態
    console.print("[green]✅ 服務運行正常[/green]")
    console.print("[green]🚀 部署成功完成[/green]")
    console.print("[green]💚 健康檢查通過[/green]")
    
    # 警告狀態
    console.print("[yellow]⚠️  記憶體使用率偏高[/yellow]")
    console.print("[yellow]🔶 建議監控系統負載[/yellow]")
    console.print("[yellow]💛 需要注意的問題[/yellow]")
    
    # 錯誤狀態
    console.print("[red]❌ 服務連接失敗[/red]")
    console.print("[red]🔥 發生嚴重錯誤[/red]")
    console.print("[red]💔 系統故障[/red]")
    
    # 資訊狀態
    console.print("[blue]ℹ️  系統資訊[/blue]")
    console.print("[blue]📊 統計資料[/blue]")
    console.print("[blue]💙 一般資訊[/blue]")

show_status_indicators()
```

## 🚀 組合應用

### 綜合儀表板

```python
def show_comprehensive_dashboard():
    """顯示綜合系統儀表板"""
    
    console = Console()
    
    # 標題
    title_panel = Panel(
        Align.center("[bold magenta]🖥️  系統監控儀表板[/bold magenta]"),
        border_style="magenta"
    )
    console.print(title_panel)
    console.print()
    
    # 系統資源表格
    resource_table = Table(title="系統資源使用", show_header=True)
    resource_table.add_column("資源", style="cyan")
    resource_table.add_column("使用量", style="green")
    resource_table.add_column("總量", style="blue")
    resource_table.add_column("使用率", style="yellow")
    resource_table.add_column("狀態", style="white")
    
    resources = [
        ("CPU", "3.2GHz", "4.0GHz", "80%", "[yellow]⚠️[/yellow]"),
        ("記憶體", "12GB", "16GB", "75%", "[green]✅[/green]"),
        ("磁碟", "180GB", "256GB", "70%", "[green]✅[/green]"),
        ("網路", "450Mbps", "1Gbps", "45%", "[green]✅[/green]")
    ]
    
    for resource in resources:
        resource_table.add_row(*resource)
    
    console.print(resource_table)
    console.print()
    
    # 服務狀態樹
    services_tree = Tree("🏢 服務狀態", style="bold blue")
    
    web_services = services_tree.add("🌐 Web 服務", style="green")
    web_services.add("[green]✅ Nginx (正常)[/green]")
    web_services.add("[green]✅ Apache (正常)[/green]")
    
    db_services = services_tree.add("🗄️  資料庫服務", style="green")
    db_services.add("[green]✅ PostgreSQL (正常)[/green]")
    db_services.add("[yellow]⚠️  Redis (高負載)[/yellow]")
    
    app_services = services_tree.add("📱 應用服務", style="red")
    app_services.add("[green]✅ API Server (正常)[/green]")
    app_services.add("[red]❌ Background Worker (故障)[/red]")
    
    console.print(services_tree)
    console.print()
    
    # 警告面板
    if True:  # 有警告時顯示
        warning_panel = Panel(
            """⚠️  發現以下需要注意的問題：

• CPU 使用率偏高 (80%)
• Redis 服務高負載
• Background Worker 服務故障

🔧 建議採取的行動：
• 檢查並最佳化高 CPU 使用的程序
• 重啟 Background Worker 服務
• 監控 Redis 服務效能""",
            title="🚨 系統警告",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print(warning_panel)

show_comprehensive_dashboard()
```

## 💡 最佳實踐

### 1. 選擇合適的組件

```python
# 資料展示 - 使用表格
def show_data():
    table = Table()
    # ... 表格內容

# 階層關係 - 使用樹狀圖
def show_hierarchy():
    tree = Tree()
    # ... 樹狀結構

# 進度追蹤 - 使用進度條
def show_progress():
    with Progress() as progress:
        # ... 進度顯示

# 重要資訊 - 使用面板
def show_important_info():
    panel = Panel()
    # ... 面板內容
```

### 2. 保持一致的樣式

```python
# 建立樣式常數
SUCCESS_STYLE = "green"
WARNING_STYLE = "yellow" 
ERROR_STYLE = "red"
INFO_STYLE = "blue"

def consistent_styling():
    console = Console()
    console.print(f"[{SUCCESS_STYLE}]✅ 操作成功[/{SUCCESS_STYLE}]")
    console.print(f"[{WARNING_STYLE}]⚠️  注意事項[/{WARNING_STYLE}]")
    console.print(f"[{ERROR_STYLE}]❌ 發生錯誤[/{ERROR_STYLE}]")
```

### 3. 適度使用視覺元素

```python
# 推薦 - 重點突出
logger.info("處理開始")
show_progress_table(data)  # 使用表格顯示重要進度
logger.success("處理完成")

# 不推薦 - 過度使用
show_fancy_panel("開始處理")  # 一般訊息不需要特殊顯示
show_animated_progress()     # 過度的動畫效果
show_complex_chart()         # 複雜但無必要的圖表
```

## 🚀 完整範例

把所有 Rich 組件結合的完整範例：

```python
def complete_rich_components_demo():
    """Rich 組件功能完整展示"""
    
    logger = create_logger(
    name="rich-components_demo",
    log_path="complete_rich_demo",
    level="INFO"
)
    console = Console()
    
    # 1. 歡迎面板
    welcome_panel = Panel(
        Align.center("[bold blue]🎨 Rich 組件展示系統[/bold blue]"),
        border_style="blue",
        padding=(1, 2)
    )
    console.print(welcome_panel)
    console.print()
    
    # 2. 系統資源表格
    logger.info("顯示系統資源表格...")
    system_status_table()
    console.print()
    
    # 3. 專案結構樹
    logger.info("顯示專案結構...")
    show_project_structure()
    console.print()
    
    # 4. 處理進度
    logger.info("模擬資料處理進度...")
    process_data_with_progress(list(range(20)))
    console.print()
    
    # 5. 統計圖表
    logger.info("顯示 API 使用統計...")
    show_usage_statistics(api_stats)
    console.print()
    
    # 6. 完成面板
    completion_panel = Panel(
        """🎉 Rich 組件展示完成！

展示的組件包括：
✅ 表格 (Table)
✅ 樹狀圖 (Tree)
✅ 進度條 (Progress)
✅ 面板 (Panel)
✅ 樣式文字 (Styled Text)

感謝您的觀看！""",
        title="✨ 展示完成",
        border_style="green",
        padding=(1, 2)
    )
    console.print(completion_panel)
    
    logger.success("Rich 組件展示完成")

if __name__ == "__main__":
    complete_rich_components_demo()
```

Rich 組件為 pretty-loguru 提供了強大的視覺化能力，讓日誌輸出更加專業和易讀！