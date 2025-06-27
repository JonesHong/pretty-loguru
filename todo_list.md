# pretty-loguru 重構待辦清單 (TODO List)

這份待辦清單基於 `report.md` 的分析建議，旨在將重構工作拆解為可管理的、可追蹤的任務。

---

## ☑ 階段一：核心解耦與職責分離 (P1)

*這個階段的目標是解決最核心的架構問題，為專案的長期健康打下基礎。*

### ☑ 階段細項 1.1: 引入 `LoggerConfig` 作為配置的唯一事實來源

- [x] **名稱**: 標準化 `LoggerConfig`
    - **說明**: 確保 `core.config.LoggerConfig` 類別包含所有必要的配置項，並提供清晰的驗證邏輯。

- [x] **名稱**: 重構 `create_logger` 核心邏輯
    - **說明**: 修改 `factory.creator.create_logger` 的核心部分，使其接收一個 `LoggerConfig` 物件作為主要參數來源。

- [x] **名稱**: 建立 `create_logger` 的語法糖介面
    - **說明**: 保留 `create_logger` 現有的多參數介面，但在內部將這些參數轉換為一個 `LoggerConfig` 物件。

- [x] **名稱**: 遷移 `preset` 邏輯
    - **說明**: 將 `preset` 的載入邏輯修改為回傳一個預先配置好的 `LoggerConfig` 實例。

### ☑ 階段細項 1.2: 使用「發布/訂閱」模式解耦 `creator` 和 `proxy`

- [x] **名稱**: 建立 `LoggerRegistry` 模組
    - **說明**: 建立一個新的、獨立的 `core.registry` 模組，包含一個全局的 logger 字典和一個簡單的事件通知器 (可以使用 `blinker` 或標準庫 `queue` 實現)。

- [x] **名稱**: 修改 `reinit_logger` 以發布事件
    - **說明**: 重構 `reinit_logger`，使其在更新 logger 實例後，透過 `LoggerRegistry` 發出一個 `logger_updated` 事件。

- [x] **名稱**: 修改 `LoggerProxy` 以訂閱事件
    - **說明**: 重構 `LoggerProxy`，使其在初始化時向 `LoggerRegistry` 訂閱更新事件，並在收到事件時更新其 `_target_logger`。

- [x] **名稱**: 移除舊的循環依賴
    - **說明**: 在完成發布/訂閱的重構後，安全地移除 `proxy.py` 中的延遲導入 `getter` 函式。

---

## ☑ 階段二：程式碼精簡與品質提升 (P2)

*這個階段專注於改善程式碼品質，消除重複，並提升函式庫的靈活性。*

### ☑ 階段細項 2.1: 動態生成 `LoggerProxy` 中的便利方法

- [x] **名稱**: 建立 `_log_to_target` 輔助方法
    - **說明**: 在 `LoggerProxy` 中實作一個私有的輔助方法，用於統一處理 `bind` 和 `opt` 的邏輯。

- [x] **名稱**: 重構 `console_*` 和 `file_*` 方法
    - **說明**: 將 `console_debug`, `file_error` 等 12 個方法的實作，改為呼叫新的 `_log_to_target` 輔助方法，以消除程式碼重複。

### ☑ 階段細項 2.2: 允許自訂日誌壓縮檔名格式

- [x] **名稱**: 在 `LoggerConfig` 中增加新參數
    - **說明**: 為 `LoggerConfig` 類別增加一個 `compression_format: Optional[str]` 參數。

- [x] **名稱**: 修改 `_create_rename_function`
    - **說明**: 更新 `core.presets._create_rename_function`，使其能夠根據 `compression_format` 參數來決定使用的命名樣板。

---

## ☑ 階段三：文檔與易用性改進 (P3)

*這個階段是持續性的工作，目標是讓使用者更容易理解和使用這個函式庫。*

### ☑ 階段細項 3.1: 撰寫「配置指南」

- [x] **名稱**: 撰寫配置關係說明
    - **說明**: 在 `README.md` 或專門的文檔頁面中，詳細解釋 `LoggerConfig`, `preset` 和 `create_logger` 參數之間的優先級關係。

- [x] **名稱**: 解釋檔名生成機制
    - **說明**: 清晰地說明 `name`, `subdirectory`, `component_name` 和 `preset` 如何共同影響最終的日誌檔案路徑和名稱。

- [x] **名稱**: 提供日誌檔案共享的範例與警告
    - **說明**: 透過範例展示多個 logger 如何寫入同一個檔案，並說明如何避免這種非預期的行為。
