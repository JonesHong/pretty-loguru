# Pretty Loguru Examples / 範例集

這個目錄包含了 Pretty Loguru 的各種使用範例，從基本用法到高級功能，涵蓋了95%用戶的實際需求。

## 📚 範例列表

### 🚀 快速開始
- **[quickstart_example.py](quickstart_example.py)** - 3分鐘快速上手指南
  - 最簡單的使用方式
  - 基本的檔案輸出
  - 預設配置使用
  - 區塊和ASCII藝術示例

### 🏗️ 詳細功能展示  
- **[detailed_example_en.py](detailed_example_en.py)** - 完整功能展示
  - 所有功能的詳細示例
  - 多種配置選項
  - 集成功能演示
  - 進階自定義功能

### 🌐 真實業務場景
- **[real_world_scenarios.py](real_world_scenarios.py)** - 實際開發中的使用場景
  - Web API 服務日誌
  - 數據處理管道
  - 錯誤監控和告警
  - 用戶行為追蹤
  - 性能監控

### ⚙️ 環境配置管理
- **[environment_config.py](environment_config.py)** - 不同環境的配置管理
  - 開發/測試/生產環境配置
  - 動態配置重載
  - 條件式日誌記錄
  - 配置文件管理

### 🔄 遷移指南
- **[migration_from_logging.py](migration_from_logging.py)** - 從標準 logging 遷移
  - 功能對比
  - 遷移策略
  - 實際範例對比
  - 性能比較

### 📋 最佳實踐
- **[best_practices.py](best_practices.py)** - 最佳實踐和常見陷阱
  - 正確的使用方式
  - 常見錯誤避免
  - 性能優化建議
  - 生產環境建議

### 🔧 其他範例
- **[example.py](example.py)** - 基本範例
- **[retention_by_loguru.py](retention_by_loguru.py)** - Loguru 原生保留策略
- **[retention_with_cleaner.py](retention_with_cleaner.py)** - 自定義清理器

## 🎯 推薦學習順序

### 對於新手：
1. **quickstart_example.py** - 先了解基本用法
2. **environment_config.py** - 學習環境配置
3. **real_world_scenarios.py** - 查看實際應用
4. **best_practices.py** - 掌握最佳實踐

### 對於從 logging 遷移的用戶：
1. **migration_from_logging.py** - 理解差異和優勢
2. **quickstart_example.py** - 快速上手
3. **environment_config.py** - 配置管理
4. **best_practices.py** - 最佳實踐

### 對於高級用戶：
1. **detailed_example_en.py** - 完整功能
2. **real_world_scenarios.py** - 複雜場景
3. **best_practices.py** - 優化指南

## 🏃 快速運行

```bash
# 快速開始
python examples/quickstart_example.py

# 真實場景
python examples/real_world_scenarios.py

# 環境配置（可設置環境變量）
APP_ENV=production python examples/environment_config.py

# 最佳實踐
python examples/best_practices.py
```

## 📁 生成的日誌文件

運行範例後，你會在以下位置找到日誌文件：
```
logs/
├── dev/                    # 開發環境日誌
├── test/                   # 測試環境日誌  
├── production/             # 生產環境日誌
├── api/                    # API 服務日誌
├── etl/                    # 數據處理日誌
├── monitoring/             # 監控日誌
├── analytics/              # 分析日誌
└── performance/            # 性能日誌
```

## 💡 提示

- 所有範例都是獨立的，可以單獨運行
- 範例會自動創建必要的日誌目錄
- 建議先在開發環境測試各種配置
- 查看生成的日誌文件以理解輸出格式

## 🤝 貢獻

如果你有好的使用場景或最佳實踐想要分享，歡迎提交 PR 添加新的範例！