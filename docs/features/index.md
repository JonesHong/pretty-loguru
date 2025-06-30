# 功能特色

pretty-loguru 的核心優勢在於其豐富的視覺化功能。這裡將詳細介紹每個特色功能，讓你充分發揮這個日誌庫的潛力。

## 🎨 視覺化功能總覽

### Rich 區塊日誌
使用 Rich 庫提供的強大面板功能，建立結構化、有邊框的日誌區塊。

- ✨ 多種邊框樣式和顏色
- 📋 清晰的資訊層次結構  
- 🎯 適合狀態報告和摘要

[了解 Rich 區塊 →](./rich-blocks)

### ASCII 藝術標題
利用 art 和 pyfiglet 庫生成引人注目的文字藝術標題。

- 🎯 多種字體選擇
- 🌈 彩色邊框支援
- 🚀 突出重要事件

[了解 ASCII 標題 →](./ascii-art)

### ASCII 藝術區塊
結合 ASCII 藝術標題和 Rich 區塊的強大功能。

- 🔥 最佳視覺效果
- 📊 完整的報告格式
- 🎨 高度自定義

[了解 ASCII 區塊 →](./ascii-blocks)

### Native 格式 (v2.1.0+)
提供接近 loguru 原生的日誌格式，便於遷移和開發。

- 🔄 無縫遷移支援
- 🎯 開發調試友好
- ⚡ 簡潔檔案命名

[了解 Native 格式 →](./native-format)

## 🚀 快速預覽

### Rich 區塊範例

```python
logger.block(
    "系統監控報告",
    [
        "🖥️  CPU 使用率: 23%",
        "💾  記憶體使用: 1.2GB / 8GB",
        "💿  磁碟空間: 156GB 可用",
        "🌐  網路狀態: 連接正常",
        "⚡  服務狀態: 全部運行"
    ],
    border_style="green",
    log_level="INFO"
)
```

### ASCII 標題範例

```python
logger.ascii_header(
    "SYSTEM READY",
    font="slant",
    border_style="blue"
)
```

### ASCII 區塊範例

```python
logger.ascii_block(
    "部署完成報告",
    [
        "⏱️  部署時間: 2分30秒",
        "✅  服務檢查: 通過",
        "🔄  健康檢查: 正常", 
        "📡  負載均衡: 已啟用"
    ],
    ascii_header="DEPLOYED",
    ascii_font="block",
    border_style="green"
)
```

## 🎯 使用場景

### 🖥️ 系統監控
使用 Rich 區塊展示系統狀態、效能指標、資源使用情況。

### 🚀 應用啟動
使用 ASCII 標題標記重要的應用生命週期事件。

### 📊 報告生成
使用 ASCII 區塊建立完整的狀態報告和摘要。

### ⚠️ 錯誤追蹤
使用不同的邊框顏色和樣式區分錯誤嚴重程度。

### 🔄 工作流程
在長時間運行的任務中使用視覺化日誌標記進度。

## 🎮 互動式學習

想要立即體驗？

1. **[安裝 pretty-loguru](../guide/installation)**
2. **[跟隨快速開始](../guide/quick-start)** 
3. **[查看完整範例](../examples/visual/)**

## 🔧 高級功能

### 目標導向日誌
pretty-loguru 還提供目標導向的日誌方法：

```python
# 僅輸出到控制台
logger.console_info("這只會在控制台顯示")

# 僅寫入檔案
logger.file_debug("這只會寫入日誌檔案") 

# 同時輸出（預設行為）
logger.info("這會同時顯示在控制台和檔案")
```

### 自定義樣式
所有視覺功能都支援自定義：

- **邊框樣式**: `"solid"`, `"double"`, `"rounded"`, `"thick"` 等
- **顏色主題**: `"red"`, `"green"`, `"blue"`, `"yellow"`, `"magenta"`, `"cyan"` 等
- **字體選擇**: 數十種 ASCII 藝術字體
- **日誌級別**: 自由控制輸出的重要性

準備好深入探索每個功能了嗎？選擇一個功能開始你的旅程！ 🎯