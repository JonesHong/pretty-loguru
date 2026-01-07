# 視覺化功能範例

展示 Pretty-Loguru 的視覺化功能，包括 Rich 區塊、ASCII 藝術和各種視覺元件。

## Rich 區塊與面板

### 使用 block() - 簡單區塊

```python
from pretty_loguru import create_logger

logger = create_logger("visual_demo")

# 基本區塊
logger.block(
    "系統資訊",
    [
        "作業系統: Ubuntu 22.04",
        "Python 版本: 3.10.5",
        "記憶體使用: 4.2GB / 16GB",
        "CPU 使用率: 35%"
    ]
)

# 自定義樣式
logger.block(
    "✅ 部署成功",
    [
        "版本號: v2.1.0",
        "部署時間: 2024-01-20 15:30:00",
        "環境: Production",
        "狀態: 健康運行"
    ],
    border_style="green",
    level="SUCCESS"
)

# 錯誤報告區塊
logger.block(
    "❌ 錯誤詳情",
    [
        "錯誤代碼: E001",
        "錯誤訊息: 資料庫連接超時",
        "發生時間: 2024-01-20 15:25:00",
        "影響範圍: 用戶登入功能",
        "建議動作: 檢查資料庫服務狀態"
    ],
    border_style="red",
    level="ERROR"
)
```

### 使用 panel() - 進階面板

```python
from pretty_loguru import create_logger
from rich.table import Table
from rich.text import Text

logger = create_logger("panel_demo")

# 基本 Panel
logger.panel("重要公告", title="通知", border_style="yellow")

# 帶副標題的 Panel
logger.panel(
    "系統維護將於今晚 10 點開始",
    title="維護通知",
    subtitle="預計 2 小時",
    border_style="orange1",
    box_style="double"
)

# 使用 Rich Text 對象
status = Text()
status.append("伺服器狀態：", style="bold")
status.append("正常運行\n", style="bold green")
status.append("上線時間：", style="bold")
status.append("72 小時 15 分鐘\n", style="cyan")
status.append("連接數：", style="bold")
status.append("1,234", style="yellow")

logger.panel(
    status,
    title="即時狀態",
    border_style="green",
    box_style="rounded",
    padding=(1, 2)
)

# 在 Panel 中顯示表格
error_table = Table(show_header=True, header_style="bold red")
error_table.add_column("時間", style="dim", width=20)
error_table.add_column("錯誤碼", style="red")
error_table.add_column("描述")

error_table.add_row("2025-01-13 19:45:00", "E001", "連接超時")
error_table.add_row("2025-01-13 19:46:15", "E002", "認證失敗")
error_table.add_row("2025-01-13 19:47:30", "E001", "連接超時")

logger.panel(
    error_table,
    title="最近錯誤",
    subtitle="最後更新：19:48",
    border_style="red",
    box_style="heavy",
    title_align="center",
    width=80
)

# 緊湊模式（無內邊距）
logger.panel(
    "緊急：系統即將重啟",
    title="⚠️ 警告",
    border_style="red",
    padding=0,
    expand=False
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/03_visual/blocks.py)

## ASCII 藝術

創建引人注目的 ASCII 藝術標題：

```python
from pretty_loguru import create_logger

logger = create_logger("ascii_demo")

# 基本 ASCII 標題
logger.ascii_header("WELCOME")
logger.ascii_header("SUCCESS", border_style="green")
logger.ascii_header("WARNING", border_style="yellow")

# 不同字體展示
fonts = ["standard", "slant", "small", "doom", "block"]
for font in fonts:
    logger.ascii_header(f"FONT {font.upper()}", font=font)

# 應用場景：啟動標題
logger.ascii_header("MyApp", font="slant", border_style="blue")
logger.info("應用程序啟動中...")
logger.success("✅ 所有服務已就緒")

# 應用場景：部署流程
logger.ascii_header("DEPLOY", font="doom", border_style="cyan")
logger.block(
    "部署資訊",
    [
        "環境: Production",
        "分支: main",
        "提交: abc123def"
    ]
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/03_visual/ascii_art.py)

## ASCII 區塊

結合 ASCII 藝術和 Rich 區塊：

```python
from pretty_loguru import create_logger

logger = create_logger("combined_visual")

# ASCII 標題 + 內容區塊
logger.ascii_block(
    "系統狀態報告",
    [
        "🟢 Web 服務: 正常運行",
        "🟢 資料庫: 連接正常",
        "🟡 快取服務: 效能降低",
        "🔴 郵件服務: 離線"
    ],
    header_text="STATUS",
    font="small",
    border_style="cyan"
)

# 部署完成報告
logger.ascii_block(
    "部署結果",
    [
        "✅ 程式碼更新完成",
        "✅ 資料庫遷移成功",
        "✅ 服務重啟完成",
        "✅ 健康檢查通過",
        "",
        "部署耗時: 3分15秒",
        "版本號: v2.1.0 → v2.2.0"
    ],
    header_text="DEPLOY",
    font="block",
    border_style="green",
    level="SUCCESS"
)
```

## Rich 組件

使用 Rich 的進階組件：

```python
from pretty_loguru import create_logger

logger = create_logger("rich_components")

# 表格
table_data = [
    {"服務名稱": "Web Server", "狀態": "🟢 運行中", "記憶體": "125MB", "CPU": "12%"},
    {"服務名稱": "Database", "狀態": "🟢 運行中", "記憶體": "512MB", "CPU": "25%"},
    {"服務名稱": "Cache", "狀態": "🟡 警告", "記憶體": "256MB", "CPU": "45%"},
    {"服務名稱": "Queue", "狀態": "🔴 停止", "記憶體": "0MB", "CPU": "0%"},
]
logger.table("服務監控", table_data, style="blue")

# 樹狀結構
tree_data = {
    "專案結構": {
        "src": {
            "models": ["user.py", "product.py"],
            "views": ["home.py", "api.py"],
            "utils": ["helpers.py", "validators.py"]
        },
        "tests": ["test_models.py", "test_views.py"],
        "docs": ["README.md", "API.md"]
    }
}
logger.tree("目錄結構", tree_data, style="green")

# 進度條
with logger.progress.progress_context("處理檔案", total=100) as update:
    for i in range(100):
        update(1)
        time.sleep(0.01)

# 多欄顯示
columns_data = [
    "功能 A：✅ 完成（測試通過）",
    "功能 B：🚧 進行中（完成度 70%）",
    "功能 C：📅 計劃中（預計下週）",
]
logger.columns("開發進度", columns_data, padding=(0, 2))
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/03_visual/rich_components.py)

## 程式碼高亮

顯示語法高亮的程式碼：

```python
from pretty_loguru import create_logger

logger = create_logger("code_demo")

# Python 程式碼
python_code = '''
def fibonacci(n):
    """計算費氏數列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
logger.code("Python 範例", python_code, language="python")

# SQL 查詢
sql_code = '''
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
HAVING order_count > 5
ORDER BY order_count DESC;
'''
logger.code("SQL 查詢", sql_code, language="sql")

# JSON 配置
json_code = '''{
    "name": "pretty-loguru",
    "version": "1.0.0",
    "features": {
        "visual": true,
        "colors": ["red", "green", "blue"]
    }
}'''
logger.code("配置檔案", json_code, language="json")
```

## Figlet 展示（如果安裝了 pyfiglet）

使用 Figlet 字體創建大型 ASCII 藝術：

```python
from pretty_loguru import create_logger, has_figlet

if has_figlet():
    from pretty_loguru.addons import print_figlet_header, get_figlet_fonts
    
    logger = create_logger("figlet_demo")
    
    # 顯示可用字體
    fonts = get_figlet_fonts()
    logger.info(f"可用的 Figlet 字體數量: {len(fonts)}")
    
    # 使用 Figlet 標題
    logger.figlet_header("BIG", font="3-d")
    logger.figlet_header("BANNER", font="banner3")
    
    # Figlet 區塊
    logger.figlet_block(
        "狀態報告",
        ["系統運行正常", "所有測試通過"],
        figlet_text="OK",
        font="bubble"
    )
```

## 下一步

- [配置管理](./configuration.md) - LoggerConfig 和預設配置
- [框架整合](./integrations.md) - FastAPI/Uvicorn 整合
- [生產環境](./production.md) - 部署和監控
