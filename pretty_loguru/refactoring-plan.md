# Pretty Loguru 重構計劃

## 現有問題
1. 檔案結構不夠清晰，導致程式碼難以維護
2. `logger_base.py` 和 `logger_factory.py` 過於龐大
3. 程式碼中存在重複邏輯和方法
4. 命名不一致，有的使用 `logger_` 前綴，有的功能從使用角度難以找到

## 新的目錄結構
```
pretty_loguru/
│
├── __init__.py                 # 包入口點，簡潔的公開 API
├── core/                       # 核心功能
│   ├── __init__.py             # 核心模組入口
│   ├── config.py               # 常數和配置
│   ├── base.py                 # 基本日誌功能
│   ├── handlers.py             # 日誌處理器
│   └── cleaner.py              # 日誌清理功能
│
├── formats/                    # 格式化功能
│   ├── __init__.py             # 格式化模組入口
│   ├── block.py                # 區塊格式化
│   ├── ascii_art.py            # ASCII 藝術
│   └── figlet.py               # FIGlet 實現（可選）
│
├── factory/                    # 工廠功能
│   ├── __init__.py             # 工廠模組入口
│   ├── creator.py              # Logger 創建功能
│   └── methods.py              # 方法擴展功能
│
├── integrations/               # 第三方整合
│   ├── __init__.py             # 整合模組入口
│   └── uvicorn.py              # Uvicorn 整合
│
└── types/                      # 類型定義
    ├── __init__.py             # 類型模組入口
    └── protocols.py            # Logger 協議定義
```

## 核心檔案重構

### 1. 從 `logger_base.py` 拆分

#### `core/config.py`
- 所有常數定義 (`log_level`, `log_rotation`, `log_path`)
- 配置結構 (`LOG_NAME_FORMATS`, `OUTPUT_DESTINATIONS`)
- 日誌格式 (`logger_format`)

#### `core/base.py`
- 基本日誌功能
- 初始化函數 `init_logger`（精簡版）
- 基本 logger 實例

#### `core/handlers.py`
- 目標過濾器功能 (`create_destination_filters`)
- 文件名格式化 (`format_log_filename`)
- 各種日誌輸出方法（控制台、文件等）

#### `core/cleaner.py`
- `LoggerClear` 類和相關功能

### 2. 從 `logger_factory.py` 拆分

#### `factory/creator.py`
- `create_logger` 函數（精簡版）
- Logger 實例管理

#### `factory/methods.py`
- `_add_custom_methods` 函數
- 擴展方法的定義

## 函數重命名建議

| 舊函數名 | 建議新函數名 |
|----------|------------|
| `init_logger` | `configure_logger` |
| `logger_start` | `initialize_logging` |
| `format_log_filename` | `format_filename` |

## 重構步驟

1. 創建新的目錄結構
2. 重構 `core/config.py`，將配置相關常數和函數從 `logger_base.py` 遷移
3. 重構 `core/base.py`，保留基本日誌功能
4. 重構 `core/handlers.py`，移動處理器相關功能
5. 重構 `core/cleaner.py`，隔離日誌清理功能
6. 重構 `formats/` 目錄的檔案，統一格式化函數
7. 重構 `factory/` 目錄的檔案，分離創建和方法擴展
8. 更新 `__init__.py` 以保持公開 API 兼容性
9. 更新類型定義

## 模組設計原則

1. **單一職責原則**：每個模組只負責一個功能
2. **開放封閉原則**：擴展功能不修改現有代碼
3. **依賴倒置原則**：高層模組不依賴低層模組的實現細節
4. **接口隔離原則**：使用者只看到它們需要的接口
5. **顯式優於隱式**：明確的命名和文檔

## 未來擴展考慮

1. 新增更多的格式化選項
2. 支援更多的第三方集成
3. 性能優化
4. 更豐富的範例檔案