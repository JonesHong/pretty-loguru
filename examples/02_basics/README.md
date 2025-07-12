# 📚 02_basics - 核心功能掌握

歡迎來到核心功能學習！完成這個模組後，您將完全掌握 pretty-loguru 的基礎能力，能夠在實際專案中自信地使用。

## 🎯 學習目標

完成本節後，您將：
- ✅ 掌握 logger 創建的各種方式
- ✅ 理解控制台與檔案輸出的最佳實踐
- ✅ 學會管理多個 logger
- ✅ 掌握錯誤處理和日誌格式化
- ✅ 準備好學習視覺化或框架整合

## 📚 範例列表（建議順序）

### 📖 Step 1: simple_usage.py - 基礎穩固
**⏱️ 預估時間：5分鐘**

```bash
python simple_usage.py
```

**學習重點**：
- `create_logger()` 的詳細參數
- 不同日誌級別的實際用途
- 檔案輸出的配置方法
- logger 名稱和路徑的規劃

---

### 🎭 Step 2: console_vs_file.py - 輸出策略
**⏱️ 預估時間：5分鐘**

```bash
python console_vs_file.py
# 檢查生成的日誌檔案
ls ./logs/
cat ./logs/demo_app*.log
```

**學習重點**：
- 何時使用控制台輸出 vs 檔案輸出
- 目標導向方法：`console_*()` 和 `file_*()`
- 實際業務場景的日誌策略
- 用戶體驗 vs 系統記錄的平衡

---

### 🏗️ Step 3: multiple_loggers.py - 多 Logger 管理
**⏱️ 預估時間：7分鐘**

```bash
python multiple_loggers.py
```

**學習重點**：
- 為不同服務創建專用 logger
- logger 命名和組織策略
- 檔案分離和管理
- 微服務架構中的日誌設計

---

### 🛠️ Step 4: error_handling.py - 錯誤處理最佳實踐
**⏱️ 預估時間：8分鐘**

```bash
python error_handling.py
```

**學習重點**：
- 異常捕獲和日誌記錄
- 錯誤分級和處理策略
- 重試機制的日誌實作
- 用戶友善 vs 開發者友善的錯誤訊息

---

### 🎨 Step 5: formatting_basics.py - 格式化基礎
**⏱️ 預估時間：10分鐘**

```bash
python formatting_basics.py
```

**學習重點**：
- 自定義日誌格式
- 結構化日誌記錄
- 性能考量和最佳實踐
- 不同環境的格式策略

## 🎮 批次測試

```bash
# 運行所有基礎範例
python simple_usage.py && \
python console_vs_file.py && \
python multiple_loggers.py && \
python error_handling.py && \
python formatting_basics.py

# 檢查生成的所有日誌檔案
find ./logs -name "*.log" -type f -exec echo "=== {} ===" \; -exec head -5 {} \;
```

## 💡 核心概念深入

### Logger 創建最佳實踐
```python
from pretty_loguru import create_logger

# 開發環境
dev_logger = create_logger(
    name="myapp_dev",
    log_path="./logs/dev",
    level="DEBUG"
)

# 生產環境
prod_logger = create_logger(
    name="myapp_prod", 
    log_path="/var/log/myapp",
    level="INFO",
    rotation="100MB",
    retention="30 days"
)
```

### 多服務日誌架構
```python
# 服務分離
auth_logger = create_logger("auth_service", log_path="./logs/auth")
api_logger = create_logger("api_service", log_path="./logs/api")
db_logger = create_logger("db_service", log_path="./logs/db")

# 使用範例
auth_logger.info("用戶登入成功")
api_logger.warning("API 請求超時")
db_logger.error("資料庫連接失敗")
```

### 錯誤處理模式
```python
try:
    risky_operation()
    logger.success("操作成功完成")
except ValidationError as e:
    logger.warning(f"輸入驗證失敗: {e}")
    # 用戶可以重試
except SystemError as e:
    logger.error(f"系統錯誤: {e}")
    # 需要技術支援
except Exception as e:
    logger.critical(f"未預期錯誤: {e}")
    # 緊急處理
```

## 🧪 自我檢測

完成所有範例後，確認您能回答：

### 基礎概念 ✅
- [ ] 什麼時候應該使用 `console_info()` vs `info()`？
- [ ] 如何為不同的服務配置不同的 logger？
- [ ] 日誌級別的選擇原則是什麼？

### 實際應用 ✅
- [ ] 如何在 try-except 中合理使用日誌？
- [ ] 多人協作專案中的日誌命名策略？
- [ ] 如何平衡日誌詳細度和性能？

### 最佳實踐 ✅
- [ ] 生產環境和開發環境的日誌配置差異？
- [ ] 如何設計便於除錯的日誌格式？
- [ ] 敏感資訊的日誌處理原則？

## ➡️ 下一步選擇

### 🎨 視覺化愛好者
**建議路徑**：[03_visual](../03_visual/) - 學習 Rich 區塊和 ASCII 藝術

### 🌐 Web 開發者
**建議路徑**：[05_integrations](../05_integrations/) - FastAPI/Uvicorn 整合

### ⚙️ 配置控制者
**建議路徑**：[04_configuration](../04_configuration/) - 深入檔案管理和輪替

### 🏭 運維工程師
**建議路徑**：[06_production](../06_production/) - 生產環境最佳實踐

## 📖 延伸閱讀

- 📋 [API 參考文件](../../docs/api/) - 所有函數的詳細說明
- 🎯 [最佳實踐指南](../../docs/guide/best-practices.md) - 進階使用建議
- 🔧 [故障排除](../../docs/troubleshooting.md) - 常見問題解決

## 🆘 遇到問題？

### 常見問題
1. **日誌檔案沒有生成？** → 檢查檔案權限和路徑存在性
2. **控制台輸出格式異常？** → 確認終端支持顏色輸出
3. **多個 logger 衝突？** → 檢查 logger 名稱是否重複

### 獲得幫助
- 💬 [社群討論](https://github.com/JonesHong/pretty-loguru/discussions)
- 🐛 [提交 Bug](https://github.com/JonesHong/pretty-loguru/issues)
- 📧 [聯繫維護者](mailto:support@pretty-loguru.com)

---

**🎓 恭喜！您已經掌握了 pretty-loguru 的核心技能！**

現在您可以自信地在任何 Python 專案中使用 pretty-loguru，並準備好學習更進階的功能了！