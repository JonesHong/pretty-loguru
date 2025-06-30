# Pretty-Loguru 範例導覽

歡迎來到 pretty-loguru 的完整範例集！這些範例遵循 KISS 原則，提供由淺入深的漸進式學習路徑。

## 🎯 快速導覽

### 🚀 新手必看（建議順序）
1. **[01_basics/](01_basics/)** - 核心功能 (3分鐘上手)
2. **[04_fastapi/](04_fastapi/)** - Web 應用整合 (如果你開發 Web 應用)

### 📚 完整學習路徑

```
01_basics/          ← 從這裡開始！核心功能
    ↓
02_visual/          ← 視覺化功能
    ↓
03_presets/         ← 預設配置和檔案管理
    ↓
04_fastapi/         ← Web 應用整合
    ↓
05_production/      ← 生產環境最佳實踐
```

## 📁 範例目錄結構

### ✅ 已完成
- **[01_basics/](01_basics/)** - 核心功能 (3分鐘上手)
  - `simple_usage.py` - 最基本使用方式
  - `console_vs_file.py` - 輸出目標對比
  - `target_logging.py` - 目標導向方法

- **[02_visual/](02_visual/)** - 視覺化功能展示
  - `blocks.py` - 區塊格式化
  - `ascii_art.py` - ASCII 藝術標題
  - `rich_components.py` - Rich 組件展示

- **[03_presets/](03_presets/)** - 預設配置和檔案管理
  - `rotation_examples.py` - 輪替策略演示
  - `preset_comparison.py` - 預設配置對比
  - `custom_presets.py` - 自訂配置管理

- **[04_fastapi/](04_fastapi/)** - 真實 Web 應用範例
  - `simple_api.py` - 基本 FastAPI 整合
  - `middleware_demo.py` - 中間件功能展示
  - `dependency_injection.py` - Logger 依賴注入

- **[05_production/](05_production/)** - 生產環境最佳實踐
  - `deployment_logging.py` - 部署環境管理
  - `performance_monitoring.py` - 性能監控
  - `error_tracking.py` - 錯誤追蹤系統

## 🚀 立即開始

### 1. 基本使用 (1分鐘)
```bash
cd 01_basics
python simple_usage.py
```

### 2. 視覺化功能 (2分鐘)
```bash
cd 02_visual
python blocks.py
```

### 3. 配置管理 (3分鐘)
```bash
cd 03_presets
python rotation_examples.py
```

### 4. Web 應用範例 (需要 FastAPI)
```bash
# 安裝依賴
pip install fastapi uvicorn

# 運行範例
cd 04_fastapi
python simple_api.py
```

### 5. 生產環境實踐 (進階)
```bash
cd 05_production
# 不同環境配置
APP_ENV=development python deployment_logging.py
APP_ENV=production python deployment_logging.py
```

## 💡 核心概念速覽

### 創建 Logger
```python
from pretty_loguru import create_logger

# 最簡單的方式
logger = create_logger("my_app")

# 添加檔案輸出
logger = create_logger("my_app", log_path="./logs")
```

### 基本日誌記錄
```python
logger.info("一般資訊")
logger.success("操作成功")
logger.warning("警告訊息")
logger.error("錯誤訊息")
```

### 目標導向輸出
```python
# 僅控制台 - 給用戶看的
logger.console_info("處理中...")

# 僅檔案 - 系統記錄
logger.file_debug("詳細除錯資訊")
```

### FastAPI 整合
```python
from pretty_loguru import create_logger
from fastapi import FastAPI

logger = create_logger("api", log_path="./logs")
app = FastAPI()

@app.get("/")
async def root():
    logger.info("收到請求")
    return {"message": "Hello World"}
```

## 📊 學習進度追蹤

- [ ] 完成 01_basics 所有範例
- [ ] 理解控制台 vs 檔案輸出的差異
- [ ] 掌握目標導向日誌方法
- [ ] (Web 開發者) 運行 FastAPI 範例
- [ ] (Web 開發者) 理解中間件和依賴注入

## 🔧 常見問題

### Q: 從哪個範例開始？
A: 建議從 `01_basics/simple_usage.py` 開始，這是最基礎的範例。

### Q: 我開發 Web 應用，應該看哪些範例？
A: 完成 01_basics 後，直接看 04_fastapi 目錄的所有範例。

### Q: 日誌檔案儲存在哪裡？
A: 預設在 `./logs/` 目錄，每個範例會生成對應的日誌檔案。

### Q: 為什麼要分控制台和檔案輸出？
A: 控制台適合給用戶看的簡潔訊息，檔案適合系統記錄的詳細資訊。

## 📖 詳細文檔

每個目錄都包含詳細的 README.md：
- [01_basics/README.md](01_basics/README.md) - 核心功能詳細說明
- [02_visual/README.md](02_visual/README.md) - 視覺化功能指南
- [03_presets/README.md](03_presets/README.md) - 配置和檔案管理
- [04_fastapi/README.md](04_fastapi/README.md) - Web 應用整合指南
- [05_production/README.md](05_production/README.md) - 生產環境最佳實踐

## 🎁 額外資源

### 舊版範例 (參考用)
如果需要參考舊版範例，可查看 `examples_backup/` 目錄。

### 依賴安裝
```bash
# 基本功能 (01_basics)
pip install pretty-loguru

# Web 應用功能 (04_fastapi)  
pip install pretty-loguru fastapi uvicorn
```

## 🤝 貢獻指南

如果您有好的使用場景或範例想要分享：
1. 遵循 KISS 原則
2. 專注單一概念
3. 提供真實可用的代碼
4. 包含清晰的註解說明

---

**開始您的 pretty-loguru 之旅吧！從 [01_basics/](01_basics/) 開始** 🚀