# 視覺化功能範例

pretty-loguru 的視覺化功能是其最大特色，本章節將展示所有視覺化功能的實際應用和效果。

## 📖 本章內容

- **[Rich 區塊範例](./blocks)** - 結構化的美觀日誌區塊  
- **[ASCII 藝術範例](./ascii-art)** - 引人注目的文字藝術標題
- **[Rich 組件範例](./rich-components)** - 完整的 Rich 功能展示
- **[組合效果範例](./combined-effects)** - 多種功能的組合使用

## 🎨 視覺化功能總覽

### Rich 區塊 - 結構化日誌

Rich 區塊提供帶邊框的結構化內容展示：

```python
from pretty_loguru import create_logger

logger.block(
    "系統狀態檢查",
    [
        "CPU 使用率: 25%",
        "記憶體使用: 60%",
        "磁碟空間: 120GB 可用",
        "網路連接: 正常"
    ],
    border_style="green",
    log_level="INFO"
)
```

### ASCII 藝術 - 引人注目的標題

使用多種字體建立視覺震撼的標題：

```python
logger.ascii_header("SYSTEM READY", font="slant", border_style="blue")
logger.ascii_header("WARNING", font="doom", border_style="yellow")
logger.ascii_header("ERROR", font="block", border_style="red")
```

### ASCII 區塊 - 完整的報告格式

結合 ASCII 標題和 Rich 區塊的強大功能：

```python
logger.ascii_block(
    "部署完成報告",
    [
        "版本: v2.1.0",
        "部署時間: 3分45秒", 
        "服務檢查: 全部通過",
        "負載均衡: 已啟用"
    ],
    ascii_header="DEPLOYED",
    ascii_font="block",
    border_style="green"
)
```

## 🎯 學習路徑

### 🚀 快速體驗 (5 分鐘)
適合想要快速了解視覺化效果的開發者：

1. **[Rich 區塊基礎](./blocks#基本用法)** - 了解基本的區塊格式
2. **[ASCII 標題體驗](./ascii-art#基本用法)** - 建立第一個 ASCII 標題

### 🎨 深度探索 (15 分鐘)  
適合想要掌握所有視覺功能的開發者：

3. **[邊框樣式和顏色](./blocks#邊框樣式)** - 掌握各種視覺效果
4. **[ASCII 字體大全](./ascii-art#字體樣式)** - 了解所有可用字體
5. **[Rich 組件整合](./rich-components)** - 表格、樹狀圖等高級功能

### 🚀 實戰應用 (20 分鐘)
適合想要在實際專案中應用的開發者：

6. **[ASCII 區塊應用](./ascii-blocks)** - 完整的報告格式
7. **[組合效果設計](./combined-effects)** - 建立專業級的視覺輸出
8. **[實際場景應用](./real-world-scenarios)** - 真實專案中的使用案例

## 🎮 互動式範例

### 完整的視覺化展示

以下是一個綜合展示所有視覺功能的範例：

```python
import time
from pretty_loguru import create_logger

def visual_showcase():
    """視覺化功能完整展示"""
    
    # 初始化日誌系統
    logger = create_logger(
    name="visual_demo",
    log_path="visual_demo",
    level="INFO"
)
    
    # 1. 啟動標題
    logger.ascii_header("VISUAL DEMO", font="slant", border_style="blue")
    
    # 2. 基本日誌級別展示
    logger.debug("這是除錯訊息")
    logger.info("這是一般訊息")
    logger.success("這是成功訊息")
    logger.warning("這是警告訊息")
    logger.error("這是錯誤訊息")
    
    time.sleep(1)
    
    # 3. Rich 區塊展示
    logger.block(
        "系統資源監控",
        [
            "🖥️  CPU 使用率: 23%",
            "💾 記憶體使用: 1.2GB / 8GB",
            "💿 磁碟空間: 156GB 可用",
            "🌐 網路狀態: 連接正常",
            "⚡ 服務狀態: 全部運行"
        ],
        border_style="green"
    )
    
    time.sleep(1)
    
    # 4. 不同顏色的區塊
    logger.block(
        "注意事項",
        [
            "⚠️  記憶體使用率偏高",
            "⚠️  建議監控系統負載",
            "💡 考慮擴展硬體資源"
        ],
        border_style="yellow",
        log_level="WARNING"
    )
    
    time.sleep(1)
    
    # 5. ASCII 藝術區塊
    logger.ascii_block(
        "演示完成摘要",
        [
            "✅ 基本日誌: 已展示",
            "✅ Rich 區塊: 已展示", 
            "✅ ASCII 標題: 已展示",
            "✅ ASCII 區塊: 已展示",
            "🎉 狀態: 演示完成"
        ],
        ascii_header="COMPLETE",
        ascii_font="block",
        border_style="green",
        log_level="SUCCESS"
    )
    
    # 6. 結束標題
    logger.ascii_header("DEMO END", font="standard", border_style="magenta")

if __name__ == "__main__":
    visual_showcase()
```

### 系統監控儀表板範例

```python
def system_dashboard():
    """模擬系統監控儀表板"""
    
    logger.ascii_header("MONITOR", font="digital", border_style="cyan")
    
    # CPU 狀態
    logger.block(
        "處理器狀態",
        [
            "型號: Intel Core i7-9700K",
            "核心數: 8 核心 8 線程",
            "使用率: 45%",
            "溫度: 58°C"
        ],
        border_style="blue"
    )
    
    # 記憶體狀態
    logger.block(
        "記憶體狀態", 
        [
            "總容量: 16GB DDR4",
            "已使用: 7.2GB (45%)",
            "可用: 8.8GB",
            "快取: 2.1GB"
        ],
        border_style="green"
    )
    
    # 磁碟狀態
    logger.block(
        "儲存狀態",
        [
            "系統碟 (C:): 256GB SSD",
            "已使用: 180GB (70%)",
            "可用: 76GB",
            "資料碟 (D:): 1TB HDD"
        ],
        border_style="yellow"
    )
    
    logger.ascii_header("STATUS OK", font="small", border_style="green")
```

## 📊 視覺效果對比

### 傳統日誌 vs pretty-loguru

**傳統日誌輸出：**
```
2024-06-30 15:30:22 INFO Application started
2024-06-30 15:30:23 INFO Database connected
2024-06-30 15:30:24 WARNING High memory usage
2024-06-30 15:30:25 ERROR Connection failed
```

**pretty-loguru 視覺化輸出：**
```
 ____  _____  _     ____  _____ 
/ ___|_   _|/ \   |  _ \|_   _|
\___ \ | | / _ \  | |_) || |   
 ___) || |/ ___ \ |  _ < | |   
|____/ |_/_/   \_\|_| \_\|_|   

┌─ 系統啟動狀態 ─┐
│ ✅ 應用程式啟動  │
│ ✅ 資料庫連接    │
│ ⚠️  記憶體使用高  │
│ ❌ 連接失敗      │
└─────────────┘
```

## 🔧 自定義指南

### 建立一致的視覺風格

```python
class VisualLogger:
    """統一的視覺化日誌類別"""
    
    def __init__(self):
        self.success_color = "green"
        self.warning_color = "yellow"
        self.error_color = "red"
        self.info_color = "blue"
        self.header_font = "slant"
    
    def success_report(self, title, items):
        logger.ascii_block(
            title, items,
            ascii_header="SUCCESS",
            ascii_font=self.header_font,
            border_style=self.success_color,
            log_level="SUCCESS"
        )
    
    def warning_report(self, title, items):
        logger.ascii_block(
            title, items,
            ascii_header="WARNING", 
            ascii_font=self.header_font,
            border_style=self.warning_color,
            log_level="WARNING"
        )
    
    def error_report(self, title, items):
        logger.ascii_block(
            title, items,
            ascii_header="ERROR",
            ascii_font="doom",
            border_style=self.error_color,
            log_level="ERROR"
        )

# 使用範例
visual = VisualLogger()
visual.success_report("部署完成", ["版本: v1.0", "狀態: 正常"])
```

## 💡 最佳實踐建議

### 1. 適度使用視覺效果
```python
# 推薦 - 重要事件使用視覺化
logger.ascii_header("APP START", font="slant")  # 應用啟動
logger.block("配置資訊", config_items)          # 重要資訊

# 不推薦 - 過度使用視覺效果
logger.ascii_header("DEBUG", font="doom")       # 一般除錯訊息
```

### 2. 保持一致的風格
```python
# 建立風格指南
SUCCESS_STYLE = {"border_style": "green", "ascii_font": "slant"}
WARNING_STYLE = {"border_style": "yellow", "ascii_font": "standard"}
ERROR_STYLE = {"border_style": "red", "ascii_font": "doom"}
```

### 3. 考慮輸出環境
```python
import os

def adaptive_logging(message):
    """根據環境調整日誌樣式"""
    if os.getenv("ENVIRONMENT") == "production":
        # 生產環境使用簡潔樣式
        logger.info(message)
    else:
        # 開發環境使用豐富樣式
        logger.block("開發訊息", [message], border_style="blue")
```

## 🚀 下一步

選擇一個感興趣的範例開始深入學習：

- **新手**：從 [Rich 區塊範例](./blocks) 開始
- **進階**：直接查看 [ASCII 區塊範例](./ascii-blocks)
- **專家**：探索 [組合效果範例](./combined-effects)

讓你的日誌輸出變得更加專業和吸引人！