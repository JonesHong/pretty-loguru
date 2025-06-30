# 快速開始

歡迎使用 pretty-loguru！這個頁面將帶你在 5 分鐘內體驗所有核心功能。

## 🚀 安裝

```bash
pip install pretty-loguru
```

## ⚡ 第一個程式

建立一個新的 Python 檔案，複製以下代碼：

```python
from pretty_loguru import logger, logger_start

# 初始化日誌系統
component_name = logger_start(folder="quick_start_logs")
print(f"日誌系統已初始化，元件 ID: {component_name}")

# 基本日誌輸出
logger.debug("這是除錯訊息")
logger.info("這是一般訊息") 
logger.success("這是成功訊息")
logger.warning("這是警告訊息")
logger.error("這是錯誤訊息")
logger.critical("這是嚴重錯誤訊息")
```

執行程式，你會看到：
- 控制台顯示彩色的日誌輸出
- `quick_start_logs/` 目錄下生成日誌檔案

## 🎨 體驗 Rich 區塊

```python
# Rich 區塊日誌 - 展示系統狀態
logger.block(
    "系統狀態檢查",
    [
        "CPU 使用率: 25%",
        "記憶體使用率: 45%", 
        "磁碟空間: 89GB 可用",
        "網路連接: 正常",
        "服務狀態: 運行中"
    ],
    border_style="green",
    log_level="INFO"
)

# 警告區塊
logger.block(
    "注意事項",
    [
        "記憶體使用率偏高",
        "目前增長率: 3%/分鐘",
        "預計 20 分鐘後達到閾值",
        "建議動作: 檢查記憶體洩漏"
    ],
    border_style="yellow", 
    log_level="WARNING"
)
```

## 🎯 體驗 ASCII 藝術

```python
# ASCII 藝術標題
logger.ascii_header(
    "SYSTEM STARTUP",
    font="slant",
    border_style="blue",
    log_level="INFO"
)

# 嘗試不同的字體
fonts = ["standard", "slant", "small", "block"]
for font in fonts:
    logger.ascii_header(
        f"Font: {font.upper()}",
        font=font,
        border_style="cyan"
    )
```

## 🔥 體驗 ASCII 區塊

```python
# ASCII 區塊 - 結合標題和內容
logger.ascii_block(
    "啟動報告", 
    [
        "初始化時間: 2.3 秒",
        "載入模組: 12 個",
        "記憶體使用: 45MB",
        "準備就緒: ✓"
    ],
    ascii_header="READY",
    ascii_font="small",
    border_style="green",
    log_level="SUCCESS"
)
```

## 🎮 完整範例

將以下代碼保存為 `quick_demo.py`：

```python
import time
import random
from pretty_loguru import logger, logger_start

def main():
    # 初始化
    component_name = logger_start(folder="demo_logs")
    
    # 應用啟動
    logger.ascii_header("APP STARTUP", font="slant", border_style="blue")
    
    logger.info("正在載入配置...")
    time.sleep(0.5)
    logger.success("配置載入完成")
    
    # 系統狀態
    logger.block(
        "系統初始化狀態",
        [
            "應用名稱: Quick Demo App",
            "版本: 1.0.0", 
            "環境: 開發環境",
            "日誌級別: DEBUG"
        ],
        border_style="cyan"
    )
    
    # 模擬工作流程
    logger.info("開始處理任務...")
    for i in range(3):
        logger.info(f"處理任務 #{i+1}")
        time.sleep(0.8)
        
        if random.random() > 0.7:  # 30% 機率警告
            logger.warning(f"任務 #{i+1} 處理較慢")
        else:
            logger.success(f"任務 #{i+1} 完成")
    
    # 完成報告
    logger.ascii_block(
        "執行摘要",
        [
            "總任務數: 3",
            "成功完成: 3", 
            "執行時間: 3.2 秒",
            "狀態: 正常"
        ],
        ascii_header="COMPLETE",
        ascii_font="block", 
        border_style="green"
    )

if __name__ == "__main__":
    main()
```

## 📁 檢查輸出

執行完程式後，檢查生成的檔案：

```bash
# 查看生成的日誌目錄
ls -la demo_logs/

# 查看日誌內容
cat demo_logs/[your_component_name]_*.log
```

你會發現：
- 控制台有豐富的彩色輸出
- 檔案中保存了完整的日誌記錄
- ASCII 藝術在檔案中以純文字形式保存

## 🎯 重點回顧

通過這個快速開始，你已經體驗了：

✅ **基本日誌功能** - 6 種日誌級別  
✅ **Rich 區塊** - 結構化的視覺日誌  
✅ **ASCII 標題** - 引人注目的標題  
✅ **ASCII 區塊** - 組合功能  
✅ **自動檔案管理** - 日誌輪換和保存  

## 🚀 下一步

現在你已經體驗了核心功能，可以：

- [深入了解基本用法](./basic-usage) - 詳細的配置選項
- [探索所有功能](../features/) - Rich 和 ASCII 的完整功能
- [查看更多範例](../examples/) - 從基礎到進階
- [整合到 Web 應用](../integrations/) - FastAPI 和 Uvicorn

準備好深入探索了嗎？ 🎮