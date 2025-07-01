# 範例集合

歡迎來到 pretty-loguru 的範例集合！這裡提供了從基礎到進階的完整學習路徑，幫助你快速掌握所有功能。

## 🎯 學習路徑

### 🚀 新手必看（5-10分鐘）
從這裡開始，了解核心概念：

1. **[基礎用法](./basics/)** - 日誌初始化、基本輸出、檔案管理
2. **[視覺化功能](./visual/)** - Rich 區塊、ASCII 藝術的基本用法

### 🎨 功能探索（15-20分鐘）
深入了解每個功能的詳細用法：

3. **[預設配置](./presets/)** - 日誌輪換、清理、壓縮等進階功能
4. **[Web 應用整合](./fastapi/)** - FastAPI、Uvicorn 的完整整合

### 🚀 生產實踐（20-30分鐘）
了解真實專案中的最佳實踐：

5. **[生產環境](./production/)** - 部署、監控、錯誤追蹤等企業級功能

## 📚 範例分類

### 🔰 基礎範例
<div class="vp-card-container">

**[簡單用法](./basics/simple-usage)**  
最基本的 logger 初始化和使用方法

**[控制台 vs 檔案](./basics/console-vs-file)**  
了解不同輸出目標的差異

**[目標導向日誌](./basics/target-logging)**  
使用 `console_*` 和 `file_*` 方法控制輸出

</div>

### 🎨 視覺化範例
<div class="vp-card-container">

**[Rich 區塊](./visual/blocks)**  
結構化的美觀日誌區塊

**[ASCII 藝術](./visual/ascii-art)**  
引人注目的文字藝術標題

**[Rich 組件](./visual/rich-components)**  
完整的 Rich 功能展示

</div>

### ⚙️ 預設配置範例
<div class="vp-card-container">

**[日誌輪換](./presets/rotation-examples)**  
按時間、大小自動輪換日誌檔案

**[預設比較](./presets/preset-comparison)**  
不同環境的最佳實踐配置

**[自定義預設](./presets/custom-presets)**  
建立你自己的預設配置

</div>

### 🌐 Web 應用範例
<div class="vp-card-container">

**[簡單 API](./fastapi/simple-api)**  
FastAPI 基本整合

**[中介軟體](./fastapi/middleware-demo)**  
在中介軟體中使用 pretty-loguru

**[依賴注入](./fastapi/dependency-injection)**  
FastAPI 依賴注入模式

</div>

### 🏭 生產環境範例
<div class="vp-card-container">

**[部署日誌](./production/deployment-logging)**  
部署過程的完整日誌記錄

**[效能監控](./production/performance-monitoring)**  
系統效能的持續監控

**[錯誤追蹤](./production/error-tracking)**  
完整的錯誤處理和追蹤

</div>

## 🎮 互動式體驗

### 快速體驗
想要立即看到效果？複製以下代碼到你的 Python 環境：

```python
# 安裝: pip install pretty-loguru
from pretty_loguru import create_logger

# 一行初始化
logger  
    name="examples_demo",
    log_path="demo",
    level="INFO"
)

# 基本日誌
logger.info("歡迎使用 pretty-loguru!")
logger.success("安裝成功!")

# Rich 區塊
logger.block(
    "快速體驗",
    [
        "✅ 安裝完成",
        "✅ 初始化成功", 
        "🎯 準備探索更多功能"
    ],
    border_style="green"
)

# ASCII 標題
logger.ascii_header("WELCOME", font="slant")
```

### 完整示範程式
我們準備了一個完整的示範程式，展示所有主要功能：

```python
# demo_complete.py
import time
import random
from pretty_loguru import create_logger

def complete_demo():
    """完整功能示範"""
    # 初始化
    logger = create_logger(
    name="examples_demo",
    log_path="complete_demo",
    level="INFO"
)
    
    # 啟動序列
    logger.ascii_header("DEMO START", font="slant", border_style="blue")
    
    # 系統檢查
    logger.block(
        "系統檢查",
        [
            "🖥️  作業系統: 檢查中...",
            "🐍 Python 環境: 檢查中...",
            "📦 依賴套件: 檢查中..."
        ],
        border_style="yellow"
    )
    
    time.sleep(1)
    
    # 檢查結果
    logger.block(
        "檢查結果", 
        [
            "✅ 作業系統: Linux/Windows/Mac",
            "✅ Python 環境: 3.8+",
            "✅ 依賴套件: 已安裝"
        ],
        border_style="green"
    )
    
    # 功能展示
    features = [
        ("Rich 區塊", "結構化日誌"),
        ("ASCII 標題", "藝術字標題"),
        ("檔案輪換", "自動管理"),
        ("多重輸出", "控制台+檔案")
    ]
    
    for i, (feature, desc) in enumerate(features):
        logger.info(f"展示功能 {i+1}: {feature}")
        logger.success(f"{desc} - 完成!")
        time.sleep(0.5)
    
    # 完成報告
    logger.ascii_block(
        "示範摘要",
        [
            f"📊 展示功能: {len(features)} 項",
            "⏱️  執行時間: 3.2 秒",
            "✨ 狀態: 完美運行",
            "🎯 下一步: 查看完整文件"
        ],
        ascii_header="COMPLETE",
        ascii_font="block",
        border_style="green"
    )

if __name__ == "__main__":
    complete_demo()
```

## 📖 如何使用這些範例

### 1. 依序學習
按照學習路徑依序進行，每個範例都建立在前一個的基礎上。

### 2. 動手實踐
每個範例都提供完整的可執行代碼，建議實際運行並查看輸出效果。

### 3. 修改實驗
在理解基本用法後，嘗試修改範例代碼，探索不同的參數和效果。

### 4. 查看輸出
特別注意：
- **控制台輸出** - 彩色、格式化的即時顯示
- **檔案輸出** - 完整的日誌記錄，適合後續分析

## 💡 學習建議

### 對於初學者
- 從 [基礎用法](./basics/) 開始
- 重點關注 `logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)` 的使用
- 理解控制台和檔案輸出的差異

### 對於有經驗的開發者
- 直接跳到 [視覺化功能](./visual/)
- 查看 [Web 應用整合](./fastapi/)
- 研究 [生產環境](./production/) 的最佳實踐

### 對於系統管理員
- 重點查看 [預設配置](./presets/)
- 了解 [日誌輪換和管理](./presets/rotation-examples)
- 學習 [部署和監控](./production/)

## 🚀 開始探索

選擇一個適合你水準的起點，開始你的 pretty-loguru 學習之旅：

- 🔰 **新手**: [基礎用法 →](./basics/)
- 🎨 **探索者**: [視覺化功能 →](./visual/)  
- 🚀 **實踐者**: [生產環境 →](./production/)

每個範例都包含詳細的說明、完整的代碼和預期的輸出效果。讓我們開始吧！ 🎯