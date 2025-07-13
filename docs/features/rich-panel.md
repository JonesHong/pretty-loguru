# Rich Panel - 進階面板顯示

Pretty-Loguru 提供了兩種面板顯示方式：簡單的 `block()` 方法和功能完整的 `panel()` 方法。本頁詳細介紹 `panel()` 方法的進階功能。

## 🎯 Panel vs Block 比較

| 功能特性 | `logger.block()` | `logger.panel()` |
|---------|-----------------|------------------|
| **內容格式** | 只接受字符串列表 | 接受任何 Rich 可渲染對象 |
| **副標題** | ❌ 不支援 | ✅ 支援 |
| **標題對齊** | 固定左對齊 | ✅ 可自定義（左/中/右） |
| **尺寸控制** | ❌ 不支援 | ✅ 支援 width/height |
| **內邊距** | 固定值 | ✅ 可自定義 |
| **Rich 對象** | ❌ 不支援 | ✅ 完整支援 |
| **使用場景** | 簡單文字訊息 | 複雜資料展示 |

## 📦 基本使用

### 簡單面板

```python
from pretty_loguru import create_logger

logger = create_logger("demo")

# 基本面板
logger.panel("這是一個基本的 Panel", title="訊息")

# 帶副標題
logger.panel(
    "系統運行正常",
    title="狀態",
    subtitle="最後檢查：2025-01-13 20:00"
)
```

### 邊框樣式

```python
# 不同的邊框樣式
logger.panel("雙線邊框", title="Double", box_style="double")
logger.panel("粗線邊框", title="Heavy", box_style="heavy")
logger.panel("ASCII 邊框", title="ASCII", box_style="ascii")
logger.panel("最小邊框", title="Minimal", box_style="minimal")

# 邊框顏色
logger.panel("紅色邊框", title="警告", border_style="red")
logger.panel("綠色邊框", title="成功", border_style="green")
logger.panel("藍色邊框", title="資訊", border_style="blue")
```

## 🎨 進階功能

### 標題對齊

```python
# 標題置中
logger.panel(
    "置中對齊的標題",
    title="標題",
    title_align="center"
)

# 副標題也可以對齊
logger.panel(
    "內容",
    title="左對齊標題",
    subtitle="右對齊副標題",
    title_align="left",
    subtitle_align="right"
)
```

### 尺寸控制

```python
# 固定寬度
logger.panel(
    "固定 60 字符寬",
    title="寬度控制",
    width=60
)

# 固定高度（適合固定格式輸出）
logger.panel(
    "固定高度面板",
    title="高度控制",
    height=10,
    width=40
)

# 不擴展（使用內容實際寬度）
logger.panel(
    "緊湊顯示",
    expand=False
)
```

### 內邊距控制

```python
# 無內邊距（緊湊模式）
logger.panel("無內邊距", padding=0)

# 自定義內邊距：(垂直, 水平)
logger.panel(
    "上下留白較多",
    padding=(3, 1)  # 上下 3 格，左右 1 格
)

# 完整控制：(上, 右, 下, 左)
logger.panel(
    "不對稱內邊距",
    padding=(1, 2, 3, 4)
)
```

## 🚀 Rich 對象整合

### 使用 Table

```python
from rich.table import Table

# 創建表格
table = Table(title="銷售統計")
table.add_column("月份", style="cyan", no_wrap=True)
table.add_column("銷售額", style="magenta")
table.add_column("成長率", justify="right", style="green")

table.add_row("一月", "$10,000", "+5%")
table.add_row("二月", "$12,000", "+20%")
table.add_row("三月", "$11,500", "-4%")

# 在面板中顯示表格
logger.panel(
    table,
    title="季度報告",
    subtitle="Q1 2025",
    border_style="blue",
    box_style="double"
)
```

### 使用 Tree

```python
from rich.tree import Tree

# 創建樹狀結構
tree = Tree("📁 專案結構")
src = tree.add("📁 src")
src.add("📄 main.py")
src.add("📄 config.py")
models = src.add("📁 models")
models.add("📄 user.py")
models.add("📄 product.py")

# 在面板中顯示
logger.panel(
    tree,
    title="目錄結構",
    border_style="green"
)
```

### 使用 Syntax（程式碼高亮）

```python
from rich.syntax import Syntax

code = '''
def calculate_fibonacci(n):
    """計算費波那契數列"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)

logger.panel(
    syntax,
    title="範例程式碼",
    subtitle="fibonacci.py",
    border_style="yellow"
)
```

### 使用 Rich Text

```python
from rich.text import Text

# 創建格式化文字
text = Text()
text.append("系統狀態：", style="bold white")
text.append("正常運行\n", style="bold green")
text.append("CPU 使用率：", style="white")
text.append("45%\n", style="yellow")
text.append("記憶體：", style="white")
text.append("2.3GB / 8GB", style="cyan")

logger.panel(
    text,
    title="系統監控",
    border_style="blue",
    box_style="rounded"
)
```

## 📊 實際應用案例

### 錯誤訊息面板

```python
from rich.text import Text
from rich.table import Table

def display_error_details(error_type, message, traceback_info):
    # 創建錯誤內容
    content = Text()
    content.append("錯誤類型：", style="bold red")
    content.append(f"{error_type}\n\n", style="red")
    content.append("錯誤訊息：", style="bold")
    content.append(f"{message}\n\n", style="white")
    
    # 添加追蹤資訊表格
    trace_table = Table(show_header=False, box=None)
    trace_table.add_column("File", style="cyan")
    trace_table.add_column("Line", style="yellow")
    trace_table.add_column("Function", style="green")
    
    for trace in traceback_info:
        trace_table.add_row(trace['file'], str(trace['line']), trace['function'])
    
    # 顯示錯誤面板
    logger.panel(
        content,
        title="❌ 錯誤發生",
        subtitle="請檢查以下資訊",
        border_style="red",
        box_style="double",
        padding=(1, 2)
    )
    
    # 顯示追蹤資訊
    logger.panel(
        trace_table,
        title="呼叫堆疊",
        border_style="yellow"
    )
```

### 配置摘要面板

```python
from rich.tree import Tree
from rich.text import Text

def display_config_summary(config):
    # 創建配置樹
    tree = Tree("⚙️ 應用程式配置")
    
    # 基本設定
    basic = tree.add("📋 基本設定")
    basic.add(f"環境: {config['env']}")
    basic.add(f"調試模式: {'✅' if config['debug'] else '❌'}")
    basic.add(f"日誌級別: {config['log_level']}")
    
    # 資料庫設定
    db = tree.add("🗄️ 資料庫")
    db.add(f"類型: {config['db']['type']}")
    db.add(f"主機: {config['db']['host']}")
    db.add(f"端口: {config['db']['port']}")
    
    # API 設定
    api = tree.add("🌐 API")
    api.add(f"版本: {config['api']['version']}")
    api.add(f"限流: {config['api']['rate_limit']}/分鐘")
    
    # 顯示配置面板
    logger.panel(
        tree,
        title="啟動配置",
        subtitle=f"載入自: {config['config_file']}",
        border_style="cyan",
        box_style="rounded",
        title_align="center"
    )
```

### 進度報告面板

```python
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table

def display_task_progress(tasks):
    # 創建進度表格
    table = Table(title="任務進度")
    table.add_column("任務名稱", style="cyan", width=20)
    table.add_column("狀態", style="yellow")
    table.add_column("進度", style="green")
    table.add_column("剩餘時間", style="magenta")
    
    for task in tasks:
        status = "🟢 進行中" if task['active'] else "⏸️ 暫停"
        progress = f"{task['completed']}/{task['total']} ({task['percentage']}%)"
        eta = task.get('eta', 'N/A')
        
        table.add_row(task['name'], status, progress, eta)
    
    # 顯示進度面板
    logger.panel(
        table,
        title="批次處理進度",
        subtitle="自動更新中...",
        border_style="green",
        box_style="heavy",
        width=80
    )
```

## 🎯 最佳實踐

### 1. 選擇適當的方法

```python
# 簡單文字訊息用 block()
logger.block("簡單訊息", ["第一行", "第二行"])

# 複雜內容用 panel()
logger.panel(rich_table, title="資料展示")
```

### 2. 善用顏色區分

```python
# 錯誤 - 紅色
logger.panel(error_msg, title="錯誤", border_style="red")

# 成功 - 綠色
logger.panel(success_msg, title="成功", border_style="green")

# 警告 - 黃色
logger.panel(warning_msg, title="警告", border_style="yellow")

# 資訊 - 藍色
logger.panel(info_msg, title="資訊", border_style="blue")
```

### 3. 目標導向輸出

```python
# 僅在控制台顯示進度
logger.console_panel(
    progress_table,
    title="即時進度",
    border_style="cyan"
)

# 僅在檔案記錄詳細資訊
logger.file_panel(
    detailed_report,
    title="完整報告",
    subtitle=f"產生時間: {datetime.now()}"
)
```

### 4. 組合使用

```python
# 先用 panel 顯示摘要
logger.panel(
    summary_text,
    title="執行摘要",
    border_style="blue"
)

# 再用其他 Rich 組件顯示詳情
logger.table("詳細數據", data_list)
logger.tree("處理流程", process_tree)
```

## 📚 參考資源

- [Rich Panel 文檔](https://rich.readthedocs.io/en/latest/panel.html)
- [Pretty-Loguru API 文檔](../api/#loggerpanel-rich-panel)
- [視覺化方法比較](../guide/visual-methods)