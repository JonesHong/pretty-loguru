# 03_presets - 預設配置和檔案管理

這個目錄展示 pretty-loguru 的預設配置系統和日誌檔案管理功能，遵循 KISS 原則，簡單易懂。

## 🎯 學習目標

- 理解不同輪替策略的適用場景
- 掌握預設配置的選擇和使用
- 學會創建自訂配置
- 了解生產環境的檔案管理最佳實踐

## 📚 範例列表

### 1. rotation_examples.py - 輪替策略範例
**學習重點**: 了解時間輪替 vs 大小輪替的差異

```bash
python rotation_examples.py
```

**功能展示**:
- 按大小輪替 (1KB 演示用)
- 按時間輪替 (daily, hourly, minute)
- 生產環境策略建議

### 2. preset_comparison.py - 預設配置對比
**學習重點**: 比較所有可用預設，選擇最適合的配置

```bash
python preset_comparison.py
```

**功能展示**:
- 所有預設的基本對比
- 壓縮檔名策略差異
- 場景化選擇建議

### 3. custom_presets.py - 自訂預設配置
**學習重點**: 創建符合特定需求的自訂配置

```bash
python custom_presets.py
```

**功能展示**:
- 環境配置 (dev/test/prod)
- 服務專用配置策略
- 動態配置管理

## 🔧 預設配置對比

| 預設名稱 | 輪替條件 | 保留期間 | 適用場景 |
|---------|---------|---------|---------|
| simple | 20 MB | 30 days | 開發測試 |
| detailed | 20 MB | 30 days | 完整功能 |
| daily | 1 day | 30 days | Web 應用 |
| hourly | 1 hour | 7 days | 高頻系統 |
| minute | 1 minute | 24 hours | 調試演示 |
| weekly | 1 week | 12 weeks | 週報系統 |
| monthly | 1 month | 12 months | 月度歸檔 |

## 🗜️ 檔名策略

每個預設都有特定的檔名模式和壓縮策略：

**當前檔名** → **輪替後檔名**

- **detailed**: `[component]_YYYYMMDD-HHMMSS.log` → `[component].YYYYMMDD-HHMMSS.log`
- **simple**: `[component]_YYYYMMDD-HHMMSS.log` → `component_rot_YYYYMMDD-HHMMSS.log`  
- **daily**: `[component]_YYYYMMDD-HHMMSS.log` → `[component]YYYYMMDD.log`
- **hourly**: `[component]_YYYYMMDD-HHMMSS.log` → `[component]YYYYMMDD_HH.log`
- **minute**: `[component]_YYYYMMDD-HHMMSS.log` → `[component]YYYYMMDD_HHMM.log`
- **weekly**: `[component]_YYYYMMDD-HHMMSS.log` → `[component]week_2025W26.log`
- **monthly**: `[component]_YYYYMMDD-HHMMSS.log` → `[component]202506.log`

**說明**: 所有預設在活動期間都使用 `[component]_YYYYMMDD-HHMMSS.log` 格式，當觸發輪替時，compression 函數會將檔案重新命名為對應的壓縮格式。

## 🏭 生產環境配置建議

### Web 應用服務
```python
web_logger = create_logger(
    "web_app",
    preset="daily",        # 每日歸檔
    retention="30 days",   # 保留一個月
    log_path="./logs/web"
)
```

### 數據處理管道
```python
etl_logger = create_logger(
    "etl_pipeline", 
    preset="hourly",       # 每小時歸檔
    retention="7 days",    # 保留一週
    log_path="./logs/etl"
)
```

### 監控系統
```python
monitor_logger = create_logger(
    "monitoring",
    rotation="10 MB",      # 按大小輪替
    retention="14 days",   # 保留兩週
    log_path="./logs/monitor"
)
```

## 📁 檔案組織策略

### 按環境隔離
```python
# 開發環境
dev_logger = create_logger("app", log_path="./logs/dev", rotation="5 MB")

# 測試環境  
test_logger = create_logger("app", log_path="./logs/test", preset="daily")

# 生產環境
prod_logger = create_logger("app", log_path="./logs/prod", retention="90 days")
```

## 🚀 快速開始

1. **了解輪替策略**:
   ```bash
   cd 03_presets
   python rotation_examples.py
   ```

2. **比較預設配置**:
   ```bash
   python preset_comparison.py
   ```

3. **創建自訂配置**:
   ```bash
   python custom_presets.py
   ```

4. **檢查生成的檔案**:
   ```bash
   ls -la logs/*/
   ```

## 💡 選擇指南

### 根據應用類型選擇

**Web 應用開發**
- 建議: `daily` 預設
- 原因: 每日歸檔便於追蹤，保留期間適中

**數據處理管道**
- 建議: `hourly` 預設  
- 原因: 處理頻繁，按小時分割便於分析

**開發測試**
- 建議: `simple` 預設
- 原因: 簡單配置，快速開始

### 根據負載選擇

**高頻率 (>1000 logs/sec)**
- 使用大的輪替檔案 (50MB+)
- 較短的保留期間 (7-14 days)

**中頻率 (100-1000 logs/sec)**
- 使用 `daily` 或 `hourly` 預設
- 適中的保留期間 (30 days)

**低頻率 (<100 logs/sec)**
- 使用 `simple` 或 `daily` 預設
- 較長的保留期間 (60+ days)

## 📊 生成的檔案結構

運行範例後，您會看到：
```
logs/
├── comparison_demo/        # 預設對比測試
├── rotation_demo/          # 輪替策略演示
├── environments/           # 環境配置
│   ├── dev/
│   ├── test/
│   └── prod/
├── services/              # 服務專用配置
│   ├── api_gateway/
│   └── user_service/
└── dynamic/               # 動態配置
    ├── dev/
    └── prod/
```

## 🔗 相關範例

- **01_basics/** - 了解基本日誌功能
- **04_fastapi/** - Web 應用中的日誌管理
- **05_production/** - 生產環境最佳實踐

## ❓ 常見問題

**Q: 如何選擇輪替策略？**
A: 時間輪替適合定期分析，大小輪替適合負載不均的應用。

**Q: 保留期間設定多長合適？**
A: 開發環境 3-7 天，測試環境 7-14 天，生產環境 30-90 天。

**Q: 可以同時使用多種預設嗎？**
A: 可以為不同的 logger 實例使用不同的預設配置。

**Q: 如何處理大量日誌檔案？**
A: 使用合適的保留策略，定期清理，考慮壓縮和歸檔。