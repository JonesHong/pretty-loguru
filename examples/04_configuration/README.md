# ⚙️ 04_configuration - 配置和檔案管理

歡迎來到配置管理學習！這個模組將教您如何精細控制 pretty-loguru 的行為，包括檔案輪替、壓縮和進階配置選項。

## 🎯 學習目標

完成本節後，您將：
- ✅ 掌握各種配置方式（字典、檔案、程式碼）
- ✅ 理解日誌輪替策略和最佳實踐
- ✅ 學會檔案壓縮和清理機制
- ✅ 能夠為不同環境設計配置方案

## 📚 範例列表（建議順序）

### 📝 Step 1: config_from_dict.py - 字典配置
**⏱️ 預估時間：8分鐘**

```bash
python config_from_dict.py
```

**學習重點**：
- 使用字典定義複雜配置
- 多環境配置管理
- 配置驗證和錯誤處理

### 📁 Step 2: config_from_file.py - 檔案配置管理
**⏱️ 預估時間：10分鐘**

```bash
python config_from_file.py
```

**學習重點**：
- JSON/YAML 配置檔案
- 配置檔案的載入和驗證
- 配置熱重載機制

### 🔄 Step 3: rotation_examples.py - 輪替策略
**⏱️ 預估時間：12分鐘**

```bash
python rotation_examples.py
```

**學習重點**：
- 大小基礎輪替
- 時間基礎輪替
- 保留策略和清理機制

### 📊 Step 4: preset_comparison.py - 預設配置對比
**⏱️ 預估時間：8分鐘**

```bash
python preset_comparison.py
```

**學習重點**：
- 開發、測試、生產環境預設
- 自定義預設的創建
- 預設配置的繼承和覆寫

## 🎮 配置測試

```bash
# 運行所有配置範例
python config_from_dict.py && \
python config_from_file.py && \
python rotation_examples.py && \
python preset_comparison.py

# 檢查生成的配置檔案和日誌
find ./logs -name "*.log" -type f | head -10
find ./config -name "*.json" -type f 2>/dev/null | head -5
```

## 💡 核心概念

### 配置層次結構
```python
# 優先順序：程式碼 > 環境變數 > 配置檔案 > 預設值
logger = create_logger(
    name="my_app",
    config_file="./config/production.json",  # 配置檔案
    level=os.getenv("LOG_LEVEL", "INFO"),    # 環境變數
    log_dir="./logs"                        # 程式碼指定
)
```

### 輪替策略
```python
# 大小輪替
logger = create_logger(
    name="size_rotation",
    log_dir="./logs",
    rotation="10MB",
    retention="5 files"
)

# 時間輪替
logger = create_logger(
    name="time_rotation", 
    log_dir="./logs",
    rotation="daily",
    retention="30 days"
)
```

## ➡️ 下一步選擇

### 🌐 框架整合
**建議路徑**：[05_integrations](../05_integrations/) - FastAPI/Uvicorn 整合

### 🏭 生產環境
**建議路徑**：[06_production](../06_production/) - 部署和維運

### 🔬 進階功能
**建議路徑**：[07_advanced](../07_advanced/) - 自定義開發

---

**⚙️ 掌握配置，讓 pretty-loguru 完全符合您的需求！**

透過靈活的配置系統，您可以輕鬆適應不同的部署環境和業務需求。