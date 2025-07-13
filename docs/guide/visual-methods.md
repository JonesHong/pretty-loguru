# 視覺化方法指南

Pretty-Loguru 提供多種視覺化方法來美化你的日誌輸出。本指南將幫助你選擇最適合的方法。

## 📊 方法概覽

| 方法 | 用途 | 複雜度 | 適用場景 |
|------|------|--------|---------|
| `logger.block()` | 簡單文字區塊 | ⭐ | 基本訊息、列表 |
| `logger.panel()` | 進階面板顯示 | ⭐⭐⭐ | 複雜內容、Rich 對象 |
| `logger.ascii_header()` | ASCII 藝術標題 | ⭐ | 啟動畫面、分隔標題 |
| `logger.table()` | 表格數據 | ⭐⭐ | 結構化數據 |
| `logger.tree()` | 樹狀結構 | ⭐⭐ | 層級關係 |
| `logger.code()` | 程式碼高亮 | ⭐ | 顯示程式碼 |

## 🎯 Block vs Panel 詳細比較

### 何時使用 `block()`

`block()` 是最簡單的區塊顯示方法，適合快速顯示文字列表。

**優點：**
- ✅ 簡單易用
- ✅ 參數少，學習成本低
- ✅ 適合純文字內容
- ✅ 性能較好

**限制：**
- ❌ 只能顯示字符串列表
- ❌ 不支援副標題
- ❌ 標題只能左對齊
- ❌ 無法控制尺寸和內邊距

**使用範例：**
```python
# 適合的場景
logger.block("系統資訊", [
    "CPU: Intel i7",
    "RAM: 16GB",
    "Disk: 512GB SSD"
])

# 狀態報告
logger.block("部署檢查", [
    "✓ 程式碼更新",
    "✓ 資料庫遷移",
    "✓ 服務重啟",
    "✓ 健康檢查"
], border_style="green")
```

### 何時使用 `panel()`

`panel()` 是功能完整的面板顯示方法，支援所有 Rich Panel 的特性。

**優點：**
- ✅ 支援任何 Rich 可渲染對象
- ✅ 可自定義標題、副標題
- ✅ 靈活的對齊選項
- ✅ 精確的尺寸和內邊距控制
- ✅ 支援複雜的視覺效果

**適用場景：**
- ❌ 需要學習更多參數
- ❌ 對於簡單文字略顯過度

**使用範例：**
```python
# 顯示 Rich 對象
from rich.table import Table

table = Table(title="性能指標")
table.add_column("指標")
table.add_column("數值")
table.add_row("QPS", "10,000")
table.add_row("延遲", "15ms")

logger.panel(
    table,
    title="系統性能",
    subtitle="5分鐘平均",
    border_style="cyan",
    box_style="double"
)

# 複雜佈局
from rich.text import Text

content = Text()
content.append("狀態: ", style="bold")
content.append("運行中\n", style="green")
content.append("版本: ", style="bold")
content.append("v2.0.0", style="blue")

logger.panel(
    content,
    title="應用程式",
    padding=(2, 4),
    width=60
)
```

## 🔄 選擇指南

### 1. 簡單文字訊息
```python
# ✅ 使用 block
logger.block("錯誤摘要", [
    "檔案未找到",
    "權限不足",
    "網路超時"
])

# ❌ 不需要 panel
logger.panel("\n".join([...]))  # 過度設計
```

### 2. 需要副標題
```python
# ❌ block 不支援副標題
# logger.block("標題", [...], subtitle="副標題")  # 不存在

# ✅ 使用 panel
logger.panel(
    "內容",
    title="主標題",
    subtitle="最後更新: 15:30"
)
```

### 3. 顯示 Rich 對象
```python
# ❌ block 不能顯示 Rich 對象
# logger.block("表格", table)  # 錯誤

# ✅ 使用 panel
logger.panel(table, title="數據表格")
```

### 4. 需要精確控制
```python
# ✅ panel 提供完整控制
logger.panel(
    content,
    title="報告",
    title_align="center",
    width=80,
    padding=(1, 3),
    box_style="heavy"
)
```

## 🎨 邊框樣式指南

### 顏色語意
使用一致的顏色來傳達訊息類型：

```python
# 成功 - 綠色
logger.block("✅ 操作成功", [...], border_style="green")
logger.panel(success_msg, border_style="green")

# 錯誤 - 紅色
logger.block("❌ 錯誤", [...], border_style="red")
logger.panel(error_msg, border_style="red")

# 警告 - 黃色
logger.block("⚠️ 警告", [...], border_style="yellow")
logger.panel(warning_msg, border_style="yellow")

# 資訊 - 藍色
logger.block("ℹ️ 提示", [...], border_style="blue")
logger.panel(info_msg, border_style="blue")
```

### Box 樣式選擇
不同的 box 樣式傳達不同的重要性：

```python
# 一般訊息 - 圓角（默認）
logger.panel(msg, box_style="rounded")

# 重要訊息 - 雙線
logger.panel(important_msg, box_style="double")

# 關鍵訊息 - 粗線
logger.panel(critical_msg, box_style="heavy")

# 技術內容 - ASCII
logger.panel(technical_msg, box_style="ascii")
```

## 📋 其他視覺化方法

### 表格 - `logger.table()`
適合顯示結構化數據：
```python
data = [
    {"名稱": "服務A", "狀態": "運行中", "CPU": "25%"},
    {"名稱": "服務B", "狀態": "停止", "CPU": "0%"}
]
logger.table("服務狀態", data)
```

### 樹狀結構 - `logger.tree()`
適合顯示層級關係：
```python
structure = {
    "應用程式": {
        "前端": ["React", "Redux"],
        "後端": ["FastAPI", "PostgreSQL"],
        "部署": ["Docker", "Kubernetes"]
    }
}
logger.tree("技術棧", structure)
```

### ASCII 藝術 - `logger.ascii_header()`
適合創建視覺分隔：
```python
# 應用啟動
logger.ascii_header("STARTUP", font="slant", border_style="green")

# 章節分隔
logger.ascii_header("PHASE 1", font="small")
```

## 🔧 性能考量

1. **簡單優先**：如果 `block()` 能滿足需求，不要使用 `panel()`
2. **批量顯示**：避免在循環中頻繁調用視覺化方法
3. **目標導向**：使用 `console_*` 和 `file_*` 前綴來控制輸出目標

```python
# 控制台顯示進度，文件記錄結果
logger.console_panel(progress_table, title="進度")
logger.file_panel(final_results, title="最終結果")
```

## 📚 最佳實踐

1. **一致性**：在整個應用中保持顏色和樣式的一致使用
2. **適度使用**：視覺元素應該增強而不是干擾資訊傳遞
3. **考慮環境**：某些終端可能不支援所有視覺效果
4. **文檔化**：記錄你的顏色和樣式約定

## 🔗 相關資源

- [API 文檔 - 視覺化方法](../api/#_2)
- [Rich Panel 功能詳解](../features/rich-panel)
- [範例集合](../examples/visual)