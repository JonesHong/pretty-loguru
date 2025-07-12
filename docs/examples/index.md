# 範例總覽

Pretty Loguru 提供豐富的範例，幫助您快速上手和掌握各種功能。所有範例都包含完整的 Python 代碼和詳細的中英文說明文檔。

## 🎯 學習路徑

### 1. 新手入門 (5分鐘)
**推薦順序**: 01_quickstart → 02_basics → 03_visual

- **[01_quickstart](../../examples/01_quickstart/README.md)** - 快速開始 (3分鐘上手)
  - 基本 logger 創建和使用
  - 控制台 vs 檔案輸出
  - Hello World 範例

- **[02_basics](../../examples/02_basics/README.md)** - 基礎功能展示
  - 多重日誌器使用
  - 錯誤處理和格式化
  - 簡單用法範例

- **[03_visual](../../examples/03_visual/README.md)** - 視覺化功能展示
  - 區塊格式化和 ASCII 藝術
  - Rich 組件和表格顯示
  - 代碼高亮範例

### 2. 配置管理 (10分鐘)
**推薦順序**: 04_configuration

- **[04_configuration](../../examples/04_configuration/README.md)** - 配置和輪替管理
  - 輪替策略選擇
  - 環境配置管理
  - 自訂配置和預設比較

### 3. 實戰應用 (15分鐘)
**推薦順序**: 05_integrations → 06_production

- **[05_integrations](../../examples/05_integrations/README.md)** - 框架整合範例
  - FastAPI 深度整合
  - 中間件自動日誌記錄
  - 微服務依賴注入

- **[06_production](../../examples/06_production/README.md)** - 生產環境最佳實踐
  - 多環境配置管理
  - 性能監控和錯誤追蹤
  - 安全合規要求

### 4. 進階探索 (30分鐘)
**適合**: 需要深度自訂功能的開發者

- **[07_advanced](../../examples/07_advanced/README.md)** - 進階功能和底層庫存取
  - 直接庫存取
  - 庫整合範例
  - 性能測試和比較

### 5. 企業級應用 (45分鐘)
**適合**: 大規模生產環境

- **[08_enterprise](../../examples/08_enterprise/README.md)** - 企業級場景
  - 微服務日誌架構
  - 安全和合規要求
  - 監控系統整合

## 🚀 快速開始

1. **克隆範例**:
   ```bash
   git clone https://github.com/JonesHong/pretty-loguru.git
   cd pretty-loguru/examples
   ```

2. **運行第一個範例**:
   ```bash
   cd 01_quickstart
   python hello_world.py
   ```

3. **查看生成的日誌**:
   ```bash
   ls ./logs/
   cat ./logs/*.log
   ```

## 📚 範例特色

### 完整可運行
- 所有範例都是完整的 Python 程式
- 包含必要的依賴和配置
- 提供詳細的運行說明

### 漸進式學習
- 從簡單到複雜的學習路徑
- 每個範例都有明確的學習目標
- 提供實際應用場景說明

### 多語言支持
- 每個範例都提供中英文文檔
- 代碼註解清楚易懂
- 適合不同語言背景的開發者

### 實戰導向
- 基於真實開發場景設計
- 提供生產環境最佳實踐
- 包含性能和安全考量

## 🎯 按功能瀏覽

### 快速開始
- **Hello World**: [01_quickstart/hello_world.py](../../examples/01_quickstart/hello_world.py)
- **控制台日誌**: [01_quickstart/console_logging.py](../../examples/01_quickstart/console_logging.py)
- **檔案日誌**: [01_quickstart/file_logging.py](../../examples/01_quickstart/file_logging.py)

### 基礎功能
- **簡單用法**: [02_basics/simple_usage.py](../../examples/02_basics/simple_usage.py)
- **輸出控制**: [02_basics/console_vs_file.py](../../examples/02_basics/console_vs_file.py)
- **錯誤處理**: [02_basics/error_handling.py](../../examples/02_basics/error_handling.py)

### 視覺化功能
- **區塊格式**: [03_visual/blocks.py](../../examples/03_visual/blocks.py)
- **ASCII 藝術**: [03_visual/ascii_art.py](../../examples/03_visual/ascii_art.py)
- **Rich 組件**: [03_visual/rich_components.py](../../examples/03_visual/rich_components.py)
- **代碼高亮**: [03_visual/code_highlighting_examples.py](../../examples/03_visual/code_highlighting_examples.py)

### 配置管理
- **輪替策略**: [04_configuration/rotation_examples.py](../../examples/04_configuration/rotation_examples.py)
- **預設比較**: [04_configuration/preset_comparison.py](../../examples/04_configuration/preset_comparison.py)
- **自訂配置**: [04_configuration/custom_presets.py](../../examples/04_configuration/custom_presets.py)
- **檔案配置**: [04_configuration/config_from_file.py](../../examples/04_configuration/config_from_file.py)

### Web 應用整合
- **基本整合**: [05_integrations/simple_api.py](../../examples/05_integrations/simple_api.py)
- **中間件**: [05_integrations/middleware_demo.py](../../examples/05_integrations/middleware_demo.py)
- **依賴注入**: [05_integrations/dependency_injection.py](../../examples/05_integrations/dependency_injection.py)
- **Uvicorn 測試**: [05_integrations/test_uvicorn_logging.py](../../examples/05_integrations/test_uvicorn_logging.py)

### 生產環境
- **部署日誌**: [06_production/deployment_logging.py](../../examples/06_production/deployment_logging.py)
- **性能監控**: [06_production/performance_monitoring.py](../../examples/06_production/performance_monitoring.py)
- **錯誤追蹤**: [06_production/error_tracking.py](../../examples/06_production/error_tracking.py)
- **壓縮測試**: [06_production/test_compression.py](../../examples/06_production/test_compression.py)

### 進階功能
- **直接庫存取**: [07_advanced/direct_library_access.py](../../examples/07_advanced/direct_library_access.py)
- **庫整合**: [07_advanced/library_integration.py](../../examples/07_advanced/library_integration.py)

### 企業級功能
- **微服務日誌**: [08_enterprise/microservices_logging.py](../../examples/08_enterprise/microservices_logging.py)
- **安全日誌**: [08_enterprise/security_logging.py](../../examples/08_enterprise/security_logging.py)
- **合規管理**: [08_enterprise/compliance.py](../../examples/08_enterprise/compliance.py)
- **監控整合**: [08_enterprise/monitoring_integration.py](../../examples/08_enterprise/monitoring_integration.py)

## 💡 使用技巧

### 1. 開發階段
建議使用 `01_quickstart` 和 `02_basics` 範例，專注於功能實現和調試。

### 2. 視覺化階段
參考 `03_visual` 範例，了解豐富的視覺化功能。

### 3. 配置階段
使用 `04_configuration` 範例，建立適合的日誌管理策略。

### 4. 整合階段
探索 `05_integrations` 範例，實現框架整合。

### 5. 部署階段
使用 `06_production` 範例，實施生產級配置。

### 6. 優化階段
探索 `07_advanced` 和 `08_enterprise` 範例，實現深度自訂和企業級功能。

## 🔗 相關資源

- **[安裝指南](../guide/installation)** - 安裝和配置說明
- **[API 文檔](../api/)** - 完整的 API 參考
- **[整合指南](../integrations/)** - 框架整合說明
- **[GitHub 儲存庫](https://github.com/JonesHong/pretty-loguru)** - 最新代碼和問題追蹤

## ❓ 需要幫助？

- 查看各範例目錄中的詳細 README 文檔
- 運行範例代碼並觀察輸出
- 參考 [常見問題](../guide/faq) 章節
- 在 [GitHub Issues](https://github.com/JonesHong/pretty-loguru/issues) 提問

開始您的 Pretty Loguru 學習之旅吧！ 🎉