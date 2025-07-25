# Pretty-Loguru 文檔編寫指南

本文檔定義了 Pretty-Loguru 文檔的統一標準和組織原則，確保所有文檔的一致性。

## 📚 文檔層級結構

### 1. README.md（入口點）
- **目標讀者**：第一次接觸的使用者
- **內容原則**：
  - 只展示最簡單的使用方式
  - 使用 `create_logger()` 直接參數方式
  - 不介紹配置物件或進階功能
  - 引導讀者到詳細文檔

**範例模板**：
```python
from pretty_loguru import create_logger

# 最簡單的方式
logger = create_logger("my_app")
logger.info("Hello World")

# 帶檔案輸出
logger = create_logger("my_app", log_path="logs", level="INFO")
```

### 2. Quick Start / 快速開始
- **目標讀者**：想要快速上手的使用者
- **內容原則**：
  - 只使用 `create_logger()` 直接參數方式
  - 展示基本功能（日誌級別、視覺化）
  - 5-10 分鐘內能完成的範例
  - 不介紹配置管理

### 3. Basic Usage / 基本使用
- **目標讀者**：需要了解常用功能的使用者
- **內容原則**：
  - 介紹 `create_logger()` 的各種參數
  - 介紹 `ConfigTemplates` 預設模板
  - 展示日誌級別、格式化、異常處理
  - 不介紹 LoggerConfig 類

**ConfigTemplates 介紹模板**：
```python
from pretty_loguru import ConfigTemplates

# 使用預設配置模板
config = ConfigTemplates.production()
logger = config.apply_to("my_app")
```

### 4. Advanced / Custom Config / 進階配置
- **目標讀者**：需要深度自定義的使用者
- **內容原則**：
  - 介紹 `LoggerConfig` 類
  - 展示配置管理、動態更新
  - 複雜場景的解決方案
  - 效能優化技巧

**LoggerConfig 介紹模板**：
```python
from pretty_loguru import LoggerConfig

# 創建自定義配置
config = LoggerConfig(
    level="INFO",
    log_path="logs",
    rotation="100 MB",
    retention="30 days"
)

# 管理多個 logger
loggers = config.apply_to("api", "database", "cache")

# 動態更新
config.update(level="DEBUG")
```

## 🎯 統一原則

### 1. 漸進式學習路徑
```
簡單 → 模板 → 自定義
create_logger() → ConfigTemplates → LoggerConfig
```

### 2. 一致的術語
- **初始化**：統一使用「初始化」而非「創建」或「建立」
- **配置模板**：指 ConfigTemplates
- **配置物件**：指 LoggerConfig 實例
- **視覺化功能**：指 block、ascii_header 等方法

### 3. 程式碼範例規範
- 使用有意義的變數名稱
- 加入適當的註解說明
- 避免過度複雜的範例
- 每個範例聚焦單一概念

### 4. 錯誤範例
避免以下混淆的寫法：

❌ **不要混用初始化方式**：
```python
# 錯誤：同時展示多種方式會混淆初學者
config = ConfigTemplates.production()
logger1 = create_logger("app", config=config)  # 方式一
logger2 = config.apply_to("app")  # 方式二
```

❌ **不要在入門文檔介紹進階功能**：
```python
# 錯誤：在 quickstart 中介紹 LoggerConfig
config = LoggerConfig(...)
config.inherit_from(...)
```

## 📋 文檔檢查清單

在編寫或修改文檔時，請確認：

- [ ] 符合對應層級的內容原則
- [ ] 使用統一的術語和命名
- [ ] 程式碼範例可正常執行
- [ ] 與其他文檔保持一致性
- [ ] 包含適當的跨文檔連結

## 🔄 遷移指南

如果發現不符合規範的文檔：

1. 確定文檔的目標層級
2. 移除不適合該層級的內容
3. 使用對應的範例模板
4. 更新跨文檔連結

---

*本指南用於維護 Pretty-Loguru 文檔的一致性和品質*