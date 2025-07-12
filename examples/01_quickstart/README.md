# 🚀 01_quickstart - 5分鐘快速體驗

歡迎來到 pretty-loguru 的快速體驗！在這 5 分鐘內，您將體驗到 pretty-loguru 的核心魅力。

## 🎯 學習目標

完成本節後，您將：
- ✅ 了解 pretty-loguru 的基本價值
- ✅ 知道如何創建第一個 logger
- ✅ 體驗美化的日誌輸出效果
- ✅ 決定是否要繼續深入學習

## 📚 範例列表（按順序執行）

### 🌟 Step 1: hello_world.py - 第一印象
**⏱️ 預估時間：1分鐘**

```bash
python hello_world.py
```

**您將看到**：
- 最簡單的 pretty-loguru 使用方式
- 比標準 logging 更美觀的輸出
- 自動的顏色編碼和格式化

---

### 🎨 Step 2: console_logging.py - 視覺化魅力
**⏱️ 預估時間：2分鐘**

```bash
python console_logging.py
```

**您將體驗**：
- Rich 區塊日誌的視覺效果
- ASCII 藝術標題的震撼
- 多彩的控制台輸出

---

### 📁 Step 3: file_logging.py - 檔案輸出
**⏱️ 預估時間：2分鐘**

```bash
python file_logging.py
# 然後檢查生成的日誌檔案
ls ./logs/
cat ./logs/*.log
```

**您將學會**：
- 如何輸出到檔案
- 控制台與檔案的不同格式
- 自動檔案命名和組織

## 🎮 一鍵運行所有範例

```bash
# 如果您想一次體驗所有功能
python hello_world.py && python console_logging.py && python file_logging.py
```

## 💡 核心概念速覽

### 最簡單的使用方式
```python
from pretty_loguru import create_logger

# 創建 logger
logger = create_logger("my_app")

# 開始記錄
logger.info("Hello, Pretty-Loguru!")
logger.success("這就是成功的顏色！")
```

### 添加檔案輸出
```python
# 同時輸出到控制台和檔案
logger = create_logger("my_app", log_path="./logs")
```

### 視覺化日誌
```python
# Rich 區塊
logger.block("系統狀態", ["CPU: 45%", "記憶體: 60%"], border_style="green")

# ASCII 藝術
logger.ascii_header("READY", font="slant")
```

## ⭐ 體驗完成後的選擇

### 🎯 如果您覺得有趣想繼續
➡️ **下一步**：[02_basics](../02_basics/) - 深入學習核心功能

### 🌐 如果您是 Web 開發者
➡️ **建議**：快速瀏覽 [02_basics](../02_basics/) 後直接看 [05_integrations](../05_integrations/)

### 🏭 如果您需要生產環境部署
➡️ **建議**：學習完 [02_basics](../02_basics/) 後重點關注 [06_production](../06_production/)

### 🤔 如果您還有疑問
- 查看 [常見問題](../../docs/faq.md)
- 瀏覽 [完整文檔](../../docs/)
- 提交 [Issue](https://github.com/JonesHong/pretty-loguru/issues)

## 🔍 深入資源

- 📖 [API 文件](../../docs/api/) - 完整的函數參考
- 🎮 [所有範例](../) - 回到範例總覽
- 💬 [社群討論](https://github.com/JonesHong/pretty-loguru/discussions)

---

**🎉 恭喜！您已經踏出了優雅日誌的第一步！**

現在您可以決定是否要繼續這個學習之旅，或者直接在您的專案中開始使用 pretty-loguru！