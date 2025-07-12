# 🎨 03_visual - 視覺化功能掌握

歡迎來到視覺化功能學習！這是 pretty-loguru 最迷人的部分 - 讓您的日誌不再單調，變成真正的藝術品。

## 🎯 學習目標

完成本節後，您將：
- ✅ 掌握 Rich 區塊日誌的各種應用
- ✅ 創造引人注目的 ASCII 藝術標題
- ✅ 學會程式碼語法高亮顯示
- ✅ 整合多種視覺元素創造專業效果
- ✅ 了解視覺化日誌的效能考量

## 📚 範例列表（建議順序）

### 🏗️ Step 1: blocks.py - Rich 區塊基礎
**⏱️ 預估時間：7分鐘**

```bash
python blocks.py
```

**學習重點**：
- 基本 Rich 區塊的創建和樣式
- 不同邊框樣式和顏色搭配
- 結構化資訊的呈現技巧
- 系統狀態展示的最佳實踐

**視覺效果預覽**：
```
╭─ 系統狀態 ─────────────────╮
│ CPU 使用率: 45%            │
│ 記憶體使用率: 60%          │
│ 磁碟空間: 120GB 可用       │
│ 網路連接: 正常             │
╰────────────────────────────╯
```

---

### 🎭 Step 2: ascii_art.py - ASCII 藝術標題
**⏱️ 預估時間：8分鐘**

```bash
python ascii_art.py
```

**學習重點**：
- ASCII 藝術字體的選擇和應用
- 不同場景的標題設計
- 與 Rich 區塊的組合使用
- 啟動、關閉、錯誤等場景的視覺設計

**視覺效果預覽**：
```
   _____ _______       _____ _______ 
  / ____|__   __|/\   |  __ \__   __|
 | (___    | |  /  \  | |__) | | |   
  \___ \   | | / /\ \ |  _  /  | |   
  ____) |  | |/ ____ \| | \ \  | |   
 |_____/   |_/_/    \_\_|  \_\ |_|   
```

---

### 🎨 Step 3: rich_components.py - Rich 組件整合
**⏱️ 預估時間：10分鐘**

```bash
python rich_components.py
```

**學習重點**：
- 表格、進度條、樹狀圖等 Rich 組件
- 複雜資料的視覺化呈現
- 即時監控界面的構建
- 互動式日誌界面設計

**視覺效果預覽**：
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                監控面板                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Progress: ████████████████░░░░  80%

├── 系統服務
│   ├── ✅ Web Server (Running)
│   ├── ✅ Database (Running)  
│   └── ⚠️  Cache (Warning)
└── 應用程序
    ├── ✅ API Gateway
    └── ❌ Message Queue
```

---

### 💻 Step 4: code_highlighting_examples.py - 程式碼語法高亮
**⏱️ 預估時間：6分鐘**

```bash
python code_highlighting_examples.py
```

**學習重點**：
- 程式碼片段的語法高亮
- 錯誤程式碼的突出顯示
- 日誌中嵌入程式碼的最佳實踐
- 不同程式語言的支援

---

### 🎆 Step 5: figlet_demo.py - FIGlet 文字藝術（可選）
**⏱️ 預估時間：5分鐘**

```bash
# 需要先安裝 pyfiglet
pip install pyfiglet
python figlet_demo.py
```

**學習重點**：
- FIGlet 文字藝術的創建
- 多種字體效果展示
- 品牌化設計應用

## 🎮 視覺化展示

```bash
# 一次體驗所有視覺效果
python blocks.py && \
python ascii_art.py && \
python rich_components.py && \
python code_highlighting_examples.py
```

## 💡 視覺化設計指南

### 🎨 顏色和樣式選擇
```python
# 根據日誌級別選擇顏色
logger.block("成功訊息", [...], border_style="green")    # 成功
logger.block("警告訊息", [...], border_style="yellow")   # 警告  
logger.block("錯誤訊息", [...], border_style="red")      # 錯誤
logger.block("資訊訊息", [...], border_style="blue")     # 一般資訊
```

### 🏗️ 結構化資訊設計
```python
# 系統狀態展示
logger.block(
    "🖥️ 系統監控",
    [
        "🔋 CPU: 45% (正常)",
        "💾 記憶體: 2.1GB / 8GB (26%)",
        "💿 磁碟: 45GB / 100GB (45%)",
        "🌐 網路: ↑ 1.2MB/s ↓ 3.4MB/s"
    ],
    border_style="cyan"
)
```

### 🎯 場景化應用
```python
# 應用啟動
logger.ascii_header("STARTING", font="slant", border_style="green")

# 錯誤警報
logger.ascii_header("ERROR", font="doom", border_style="red")

# 部署完成
logger.ascii_header("DEPLOYED", font="block", border_style="blue")
```

## 🛠️ 實用範本

### 📊 系統監控面板
```python
def show_system_status(logger, cpu, memory, disk, network):
    logger.block(
        "🖥️ 系統狀態",
        [
            f"CPU: {cpu}%",
            f"記憶體: {memory}%", 
            f"磁碟: {disk}%",
            f"網路: {network}"
        ],
        border_style="green" if all(x < 80 for x in [cpu, memory, disk]) else "yellow"
    )
```

### 🚀 部署進度展示
```python
def deployment_progress(logger, step, total, current_task):
    progress = f"[{step}/{total}] {current_task}"
    logger.block(
        "🚀 部署進度", 
        [progress, "─" * 30, f"完成度: {step/total*100:.1f}%"],
        border_style="blue"
    )
```

### ❌ 錯誤報告格式
```python
def error_report(logger, error_type, message, suggestion):
    logger.ascii_header("ERROR", font="doom", border_style="red")
    logger.block(
        "❌ 錯誤詳情",
        [
            f"類型: {error_type}",
            f"訊息: {message}",
            f"建議: {suggestion}",
            f"時間: {datetime.now()}"
        ],
        border_style="red"
    )
```

## 🔧 效能考量

### ⚡ 最佳實踐
- **適度使用**：視覺化效果很棒，但不要過度使用
- **條件渲染**：在生產環境可以考慮關閉某些視覺效果
- **快取字體**：ASCII 藝術字體可以快取以提升效能

### 🎛️ 效能優化範例
```python
# 根據環境調整視覺化
import os

ENABLE_ASCII_ART = os.getenv("LOG_ASCII", "true").lower() == "true"
ENABLE_RICH_BLOCKS = os.getenv("LOG_RICH", "true").lower() == "true"

def conditional_ascii_header(logger, text, **kwargs):
    if ENABLE_ASCII_ART:
        logger.ascii_header(text, **kwargs)
    else:
        logger.info(f"=== {text} ===")
```

## 🧪 創意挑戰

完成基礎學習後，嘗試這些創意應用：

### 🎨 設計挑戰
- [ ] 創建您專案的專屬啟動畫面
- [ ] 設計一個即時監控面板
- [ ] 製作錯誤報告的標準格式
- [ ] 建立部署進度的視覺化展示

### 🏆 進階挑戰
- [ ] 整合多種視覺元素創造複雜界面
- [ ] 設計適配不同終端大小的響應式日誌
- [ ] 創建可配置的視覺化主題系統

## ➡️ 下一步選擇

### ⚙️ 深入配置
**建議路徑**：[04_configuration](../04_configuration/) - 學習檔案管理和輪替

### 🌐 框架整合
**建議路徑**：[05_integrations](../05_integrations/) - FastAPI/Uvicorn 整合

### 🏭 生產環境
**建議路徑**：[06_production](../06_production/) - 了解視覺化在生產環境的應用

## 🎨 靈感畫廊

瀏覽社群分享的精美日誌設計：
- 🌟 [精選範例集](../../gallery/visual-examples.md)
- 🎨 [設計靈感](../../gallery/design-inspiration.md)
- 🏆 [最佳實踐案例](../../gallery/best-practices.md)

---

**🎨 創造屬於您的日誌藝術！**

視覺化不僅讓日誌更美觀，更重要的是提升了資訊的可讀性和實用性。現在開始發揮您的創意吧！