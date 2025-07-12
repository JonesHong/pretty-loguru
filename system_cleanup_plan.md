# Pretty-Loguru 系統重複組件清理計劃

## 🔍 發現的重複組件

### 1. 配置系統重複
- **LoggerConfig** (基本配置類)
- **EnhancedLoggerConfig** (增強配置類，支持重用模板)

### 2. 格式化系統重複
- **simple_formatter.py** (簡化版格式化)
- **target_formatter.py** (複雜版，但依賴 simple_formatter)

### 3. 預設配置重複
- **presets.py** 中的預設類型
- **ConfigTemplates** 在 enhanced_config.py 中的預設

### 4. 其他潛在重複
- 多個創建 logger 的入口點
- 重複的工具函數

## 🎯 整理建議

### 統一配置系統
**保留：EnhancedLoggerConfig**
- 功能更強大（支持重用模板）
- 向後兼容性好
- API 更優雅

**移除：LoggerConfig**
- 功能被 EnhancedLoggerConfig 完全包含
- 可以通過 EnhancedLoggerConfig 轉換

### 統一格式化系統
**保留：target_formatter.py**
- 功能更完整
- 已經優化過的版本

**移除：simple_formatter.py**
- 功能被 target_formatter 包含
- 避免維護兩套類似的代碼

### 統一預設配置
**保留：ConfigTemplates**
- 更現代的設計
- 與 EnhancedLoggerConfig 完美配合

**移除：presets.py 中的重複部分**
- 保留核心功能，移除重複的預設定義

## 🔄 遷移計劃

### Phase 1: 統一配置系統
1. 擴展 EnhancedLoggerConfig 以支持所有 LoggerConfig 功能
2. 創建兼容性包裝器
3. 更新所有引用

### Phase 2: 統一格式化系統
1. 將 simple_formatter 的獨特功能合併到 target_formatter
2. 移除 simple_formatter.py
3. 更新導入引用

### Phase 3: 統一預設配置
1. 將 presets.py 的有用功能合併到 ConfigTemplates
2. 簡化預設配置接口
3. 更新文檔

### Phase 4: 清理和優化
1. 移除廢棄的文件
2. 更新 __init__.py 導出
3. 更新文檔和範例

## 🎨 統一後的架構

```
pretty_loguru/
├── core/
│   ├── config.py          # 統一的配置系統（EnhancedLoggerConfig）
│   ├── formatter.py       # 統一的格式化系統
│   ├── templates.py       # 統一的預設配置
│   └── ...
├── factory/
│   └── creator.py         # 統一的創建器
└── ...
```

## 🚀 用戶體驗改進

### 統一後的 API
```python
from pretty_loguru import LoggerConfig, ConfigTemplates

# 統一的配置方式
config = LoggerConfig(level="INFO", log_path="logs/app")
logger = config.apply_to("app")

# 統一的預設配置
prod_config = ConfigTemplates.production()
logger = prod_config.apply_to("prod_app")
```

### 簡化的導入
```python
# 之前：多個導入
from pretty_loguru import LoggerConfig, EnhancedLoggerConfig, ConfigTemplates
from pretty_loguru.core.presets import get_preset_config

# 之後：統一導入
from pretty_loguru import LoggerConfig, ConfigTemplates
```

## 📊 清理效果

### 減少的文件數量
- 移除 `simple_formatter.py`
- 合併 `presets.py` 的功能
- 統一配置相關的文件

### 減少的代碼重複
- 配置系統重複代碼 ~200 行
- 格式化系統重複代碼 ~150 行
- 預設配置重複代碼 ~100 行

### 提升的維護性
- 單一真相來源
- 更清晰的職責分離
- 更簡潔的 API

## ⚠️ 注意事項

### 向後兼容性
- 提供別名和包裝器
- 漸進式遷移
- 保留關鍵 API

### 測試更新
- 更新所有測試用例
- 確保功能完整性
- 性能回歸測試

### 文檔更新
- 更新 API 文檔
- 更新使用範例
- 遷移指南