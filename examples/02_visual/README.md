# 02_visual - 視覺化功能展示

這個目錄展示 pretty-loguru 的視覺化功能，讓您的日誌輸出更加美觀和直觀。

## 🎯 學習目標

- 掌握區塊格式化功能
- 學會使用 ASCII 藝術標題
- 掌握 FIGlet 文字藝術功能
- 了解 Rich 組件的強大功能
- 創建專業的監控儀表板

## 📚 範例列表

### 1. blocks.py - 區塊格式化展示
**學習重點**: 使用區塊讓重要資訊更突出

```bash
python blocks.py
```

**功能展示**:
- 基本區塊格式化
- 彩色邊框樣式 (green/yellow/red/blue)
- 系統狀態報告
- 部署流程可視化

**核心方法**:
```python
logger.block("標題", ["內容行1", "內容行2"], border_style="green")
```

### 2. ascii_art.py - ASCII 藝術標題
**學習重點**: 創建視覺衝擊力強的標題

```bash
python ascii_art.py
```

**功能展示**:
- ASCII 藝術標題
- 應用品牌化展示
- 狀態標題 (INIT/LOADING/READY/ERROR)
- 部署工作流程視覺化

**核心方法**:
```python
logger.ascii_header("SUCCESS", font="slant", border_style="green")
```

### 3. figlet_demo.py - FIGlet 文字藝術展示
**學習重點**: 使用 FIGlet 創建視覺衝擊力強的文字藝術

```bash
pip install pyfiglet  # 需要先安裝 pyfiglet
python figlet_demo.py
```

**功能展示**:
- FIGlet 文字藝術標題
- 多種字體效果展示
- 應用品牌化設計
- 狀態顯示 (INIT/LOAD/READY/ERROR)
- 創意數字和日期顯示
- 部署工作流程視覺化

**核心方法**:
```python
logger.figlet_header("WELCOME", font="slant", border_style="blue")
```

**注意**: 此功能需要安裝 `pyfiglet` 套件：`pip install pyfiglet`

### 4. rich_components.py - Rich 組件展示
**學習重點**: 使用 Rich 組件創建專業儀表板

```bash
python rich_components.py
```

**功能展示**:
- 數據表格展示
- 樹狀目錄結構
- 多欄位並排顯示
- 實時進度條
- 監控儀表板範例

**核心方法**:
```python
# 表格 (data 為字典列表)
user_data = [
    {"姓名": "Alice", "Email": "alice@example.com", "角色": "Admin"},
    {"姓名": "Bob", "Email": "bob@example.com", "角色": "User"}
]
logger.table(title="用戶統計", data=user_data)

# 樹狀圖
tree_structure = {
    "專案/": {
        "src/": {"app.py": None, "utils.py": None},
        "tests/": {"test_app.py": None}
    }
}
logger.tree("專案結構", tree_structure)

# 多欄位
services = ["🟢 API: 正常", "🟡 DB: 警告", "🔴 Cache: 異常"]
logger.columns(title="服務狀態", items=services)

# 進度條
items = list(range(100))
for item in logger.progress.track_list(items, "處理數據"):
    time.sleep(0.01)  # 模擬工作
```

## 🎨 視覺效果預覽

### 區塊格式化
```
┌─────────────────────────────────┐
│            系統狀態             │
├─────────────────────────────────┤
│ CPU: 45%                        │
│ 記憶體: 60%                     │
│ 磁碟: 120GB 可用                │
│ 狀態: 正常運行                  │
└─────────────────────────────────┘
```

### ASCII 藝術標題
```
   _____ __  __ ____________ _____ _____
  / ___// / / // ____/ ____// ___// ___/
  \__ \/ / / // /   / /     \__ \ \__ \ 
 ___/ / /_/ // /___/ /___  ___/ /___/ / 
/____/\____/ \____/\____/ /____//____/  
```

### FIGlet 文字藝術
```
 __        __ _____ _     ____  ___  __  __ _____
 \ \      / /| ____| |   / ___|/ _ \|  \/  | ____|
  \ \ /\ / / |  _| | |  | |   | | | | |\/| |  _|  
   \ V  V /  | |___| |__| |___| |_| | |  | | |___ 
    \_/\_/   |_____|_____\____|\___/|_|  |_|_____|
```

### Rich 表格
```
                    📊 用戶統計                    
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ 姓名    ┃ Email             ┃ 角色      ┃ 狀態      ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Alice   │ alice@example.com │ Admin     │ 活躍      │
│ Bob     │ bob@example.com   │ User      │ 活躍      │
└─────────┴───────────────────┴───────────┴───────────┘
```

## 🚀 快速開始

1. **運行視覺化範例**:
   ```bash
   cd 02_visual
   python blocks.py
   ```

2. **查看輸出效果**:
   - 控制台會顯示彩色的視覺化內容
   - 檢查 `./logs/` 目錄中的日誌檔案

3. **嘗試其他範例**:
   ```bash
   python ascii_art.py
   
   # FIGlet 範例 (需要先安裝 pyfiglet)
   pip install pyfiglet
   python figlet_demo.py
   
   python rich_components.py
   ```

## 💡 實用場景

### 1. 系統監控儀表板
```python
# 系統狀態概覽
logger.ascii_header("MONITOR", font="slant", border_style="blue")

# 關鍵指標表格
metrics_data = [
    ["CPU使用率", "45%", "正常"],
    ["記憶體", "68%", "正常"],
    ["磁碟空間", "78%", "警告"]
]
logger.print_table("系統指標", ["項目", "使用率", "狀態"], metrics_data)
```

### 2. 部署流程報告
```python
# 部署階段標題
logger.ascii_header("DEPLOY", font="slant", border_style="blue")

# 部署步驟區塊
steps = [
    "✓ 代碼編譯完成",
    "✓ 測試全部通過", 
    "→ 正在部署到生產環境"
]
logger.block("🚀 部署進度", steps, border_style="green")
```

### 3. 錯誤報告
```python
# 錯誤標題
logger.ascii_header("ERROR", font="slant", border_style="red")

# 錯誤詳情
error_info = [
    "錯誤類型: DatabaseConnectionError",
    "錯誤代碼: DB001", 
    "發生時間: 2024-06-28 10:30:25",
    "影響範圍: 用戶登入功能"
]
logger.block("⚠️ 錯誤詳情", error_info, border_style="red")
```

## 🎯 最佳實踐

### 1. 選擇適當的視覺化方式
- **區塊**: 重要狀態和報告
- **ASCII 標題**: 階段分隔和品牌化
- **表格**: 結構化數據展示
- **樹狀圖**: 層次結構展示
- **多欄位**: 並排對比資訊

### 2. 顏色使用規範
- **綠色**: 成功、正常狀態
- **黃色**: 警告、進行中
- **紅色**: 錯誤、異常狀態
- **藍色**: 資訊、一般狀態

### 3. 性能考慮
```python
# 僅在控制台顯示複雜視覺化
logger.console_info("顯示詳細儀表板...")
logger.print_table(...)  # 複雜表格

# 檔案記錄保持簡潔
logger.file_info("系統狀態: CPU 45%, 記憶體 68%")
```

## 📁 生成的日誌檔案

運行範例後，您會看到：
```
logs/
├── blocks_demo_YYYYMMDD-HHMMSS.log
├── ascii_demo_YYYYMMDD-HHMMSS.log
├── tables_demo_YYYYMMDD-HHMMSS.log
└── dashboard_YYYYMMDD-HHMMSS.log
```

## 🔗 相關範例

- **01_basics/** - 了解基本日誌功能
- **04_fastapi/** - 在 Web 應用中使用視覺化
- **05_production/** - 生產環境的監控實踐

## ❓ 常見問題

**Q: 視覺化內容會影響性能嗎？**
A: 主要在控制台顯示，檔案中記錄簡化版本，對性能影響很小。

**Q: 如何在生產環境使用？**
A: 建議用於監控儀表板、部署報告等重要場景，避免過度使用。

**Q: 視覺化內容能自定義樣式嗎？**
A: 支援多種邊框樣式和顏色，可根據需求選擇合適的視覺效果。