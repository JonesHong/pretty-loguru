# pretty-loguru 程式邏輯複評 v3（不含 docs/examples/tests）

## 總體評分
- **評分：8 / 10（重載 addons 前提下的邏輯與可用性）**
- 理由：核心設計成熟（loguru shared core + logger_id 隔離）、外掛整合完整（rich/art/figlet/loki/fastapi/uvicorn）、並已補上鎖/降噪/還原能力。現存問題多為「邊界行為、預設策略與 API 合約清晰度」，不至於影響主流程，但在進階/大規模情境會放大。

## 核心優點
- **共享 core 隔離設計正確**：透過 `logger_id` + filters 分流，配合 `patch_record` 保證多 logger 共用同一 loguru core 的隔離。
- **addons 重載目標清晰**：create_logger 仍維持 loguru 風格 API，同時一次性注入 rich/art/figlet 的便捷方法，符合你「開箱即用」的設計意圖。
- **降級路徑已補齊**：缺依賴（pyfiglet/art）與 Loki sink 失敗都會以 warn_once 告警、不中斷主 logger。
- **整合還原能力提升**：`uvicorn` 提供 restore，`fastapi` 提供部分 restore（route_class 可還原）。
- **觀測性增加**：新增 diagnostics API（active cleaners / handler ids / default logger 狀態）。

## 主要風險 / 缺漏 / 錯誤
1) **reinit_logger 合約不保留原設定**
   - `reinit_logger` 重新組合 `LoggerConfig` 時只用顯式參數；未套用現有 `_pretty_loguru_config`。
   - 影響：使用者只想改 `level`，但 `log_dir/rotation/compression/start_cleaner` 會掉回預設，檔案 sink 可能被關掉。
   - 位置：`pretty_loguru/factory/creator.py`

2) **cleaner 未使用 LoggerConfig.retention**
   - `LoggerCleaner` 支援 `log_retention` / `check_interval`，但 `_start_cleaner_for_path` 未帶入。
   - 影響：設定 retention 無效，清理永遠是預設 30 天，易造成誤判。
   - 位置：`pretty_loguru/factory/creator.py`, `pretty_loguru/core/cleaner.py`

3) **warn_missing_dependency fallback 仍可能 NameError**
   - `pretty_loguru/utils/dependencies.py` 在 warn_once import 失敗時會呼叫 `warnings.warn`，但檔案未 import warnings。
   - 影響：特定錯誤路徑會拋出 NameError，吞掉原本的友善警告。

4) **configure_logger 對 logger_id 過嚴**
   - `configure_logger` 的 filter 嚴格要求 `record.extra.logger_id == config.name`。
   - 影響：如果外部用「原生 loguru logger + configure_logger」而未經 `patch_record/bind`，所有輸出被過濾掉。
   - 位置：`pretty_loguru/core/base.py`

5) **顯式清空（None）行為仍不清楚**
   - create/reinit 的「只覆寫非 None」策略，使得「我要把 log_dir 設為 None」無法表達。
   - 影響：使用者難以用 API 清空既有設定，造成行為隱晦。
   - 位置：`pretty_loguru/factory/creator.py`

6) **formats/__init__.py 仍有 stdout/stderr 汙染**
   - figlet 初始化失敗時仍使用 `print(...)`。
   - 影響：在 import 階段輸出雜訊，影響測試與 CLI 體驗。
   - 位置：`pretty_loguru/formats/__init__.py`

7) **warn_once 文檔與實作不一致**
   - docstring 提到 `PRETTY_LOGURU_WARNINGS_DEBUG`，但實作未使用。
   - 影響：環境變數行為與文件不一致，降低可預期性。
   - 位置：`pretty_loguru/utils/warn_once.py`

8) **fastapi restore 仍是部分還原**
   - middleware 無法移除，僅 route_class 可還原且會警告。
   - 影響：若需要完全回復，仍需重建 app。
   - 位置：`pretty_loguru/integrations/fastapi.py`

## 改進建議（優先順序）
1) **修正 reinit_logger 合約**  
   - 以 `_pretty_loguru_config` 作為 base，再覆寫顯式參數；或提供 `keep_existing=True` 模式。
2) **cleaner 使用 retention / check_interval**  
   - `_start_cleaner_for_path` 接受並傳遞 `log_retention` 與 `check_interval`。
3) **補齊 dependencies fallback import**  
   - `utils/dependencies.py` 加 `import warnings`，避免 fallback 分支 NameError。
4) **放寬 configure_logger 的 logger_id 條件**  
   - 缺少 logger_id 時 fallback：自動注入或允許通過，並發出警告提示。
5) **顯式清空語意（None）**  
   - 使用 `UNSET` sentinel 或 `clear_log_dir=True` 旗標，解決「我想清空」的需求。
6) **formats/__init__ 警告統一**  
   - 移除 print，改用 warn_once / warnings。
7) **warn_once 行為一致化**  
   - 實作 `PRETTY_LOGURU_WARNINGS_DEBUG` 或移除 docstring 描述。
8) **fastapi 完整還原的替代路徑**  
   - 提供「純 log_config / 中間件清單」模式，或 context manager 來明確管理副作用。

## 總結
在「預設重載 addons」的前提下，目前邏輯已達穩定可用水位。若補齊 reinit/cleaner/依賴警告等邊界問題，評分可提升至 **8.5+**。這些改動屬於「合約與邊界」層級，對核心設計無需大改。***
