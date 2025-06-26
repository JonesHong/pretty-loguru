# pretty-loguru 架構分析與重構建議報告

## 1. 總體評價

`pretty-loguru` 是一個目標明確、設計優良的日誌函式庫。它成功地在 Loguru 的基礎上整合了 Rich、Art 等工具，並圍繞 KISS 原則進行了封裝，極大地簡化了開發者在真實場景下的日誌配置工作。特別是 `LoggerProxy` 的設計和對 Loguru Cleaner 的替代方案，顯示了對核心痛點的深刻理解。

本報告旨在現有優秀基礎上，提出一些可以使其架構更健壯、可維護性更高、擴展性更強的建議。

---

## 2. 架構與設計分析

### 2.1. 存在的問題與潛在風險

#### a. 耦合過緊：`factory.creator` 與 `factory.proxy`

- **問題描述**：`creator` 模組負責建立 logger 實例，而 `proxy` 模組負責代理這些實例。兩者之間存在著緊密的雙向依賴。
  - `creator.py` 在建立代理時需要導入 `LoggerProxy`。
  - `proxy.py` 為了能獲取最新的 logger 實例，需要透過一個延遲導入的 `getter` 函式來反向查找 `creator._logger_registry`。
- **潛在風險**：
  - **循環依賴**：雖然透過延遲導入解決了直接的啟動錯誤，但這是一種脆弱的設計。未來任何微小的修改都可能破壞這個平衡。
  - **維護困難**：理解這兩個模組的互動需要同時在兩個檔案中來回跳轉，增加了心智負擔。它們幾乎無法被獨立修改或測試。

#### b. 職責不清：`create_logger` 函式過於龐大

- **問題描述**：`factory.creator.create_logger` 函式是整個函式庫的核心，但它承擔了過多的職責。它接收大量的參數，內部處理了配置合併、預設載入、Sink 建立、過濾器設定、Proxy 建立等多種邏輯。
- **潛在風險**：
  - **違反單一職責原則**：函式變得難以閱讀、理解和修改。
  - **擴展困難**：如果想增加一種新的配置方式或 Sink 類型，就需要修改這個已經很複雜的函式，風險很高。

#### c. 配置管理靈活性不足

- **問題描述**：`core.presets.py` 中的 `_create_rename_function` 函式將日誌檔案的重命名邏輯寫死在程式碼中。使用者無法自訂壓縮後檔案的命名格式，除非直接修改原始碼。
- **潛在風險**：無法滿足所有使用者的個性化需求，降低了函式庫的通用性。

### 2.2. 程式碼重複性

#### a. `LoggerProxy` 中的便利方法

- **問題描述**：在 `factory.proxy.py` 中，我們為 `console_*` 和 `file_*` 系列新增了 12 個方法 (`console_debug`, `file_error` 等)。這些方法的內部實作幾乎完全相同，只有 `bind` 的參數和呼叫的日誌級別不同。
- **影響**：
  - **維護成本高**：如果未來需要修改這個邏輯（例如，增加新的 `bind` 參數），需要在 12 個地方進行修改。
  - **程式碼冗長**：不必要的程式碼重複。

---

## 3. 可擴展性與可維護性評估

- **可擴展性**：
  - **優點**：
    - **格式擴展**：在 `formats/` 目錄下增加新模組來擴展日誌格式（如 `ascii_art`）的模式是清晰且有效的。
    - **預設擴展**：`register_custom_preset` 函式讓使用者可以方便地註冊自己的配置預設，擴展性良好。
  - **弱點**：
    - **核心功能擴展**：如前所述，由於 `create_logger` 函式職責過重，擴展其核心創建邏輯會非常困難。
    - **日誌目標 (Sink) 擴展**：目前主要針對控制台和檔案。若要原生支援如 `syslog`, `database` 或第三方服務 (Sentry, Datadog)，需要對 `creator` 進行較大改動。

- **可維護性**：
  - **優點**：
    - **模組化清晰**：專案結構（core, factory, formats, integrations）清晰明瞭。
    - **KISS 原則**：大部分模組都遵循了簡單原則，易於理解。
  - **弱點**：
    - **高耦合點**：`creator` 和 `proxy` 的耦合是最大的維護難點。
    - **隱式約定**：`component_name` 參數會影響最終檔名，導致多個 logger 實例寫入同一個檔案。這個行為對於初學者來說可能不直觀，屬於一種隱式約定，需要更好的文檔或更清晰的參數名來彌補。

---

## 4. 重構建議與優先級

我將建議分為三個優先級，建議從 P1 開始，因為它們能帶來最大的結構性改善。

### P1：核心解耦與職責分離 (高影響力，中等複雜度)

#### 建議 1.1：引入 `LoggerConfig` 作為配置的唯一事實來源 (Single Source of Truth)

- **問題**：`create_logger` 函式參數過多，配置來源混亂。
- **方案**：
  1.  將 `core.config.LoggerConfig` 類別作為所有日誌配置的標準化容器。
  2.  重構 `create_logger`，使其主要接收一個 `LoggerConfig` 物件作為參數。
  3.  保留現有的多參數介面，但將其作為一個便利的「語法糖」。在內部，它會將這些參數轉換為一個 `LoggerConfig` 物件，然後再呼叫核心的創建邏輯。
  4.  `preset` 的概念也應轉換為載入一個預定義的 `LoggerConfig` 實例。
- **好處**：
  - **職責單一**：`create_logger` 只負責根據標準化配置進行創建，而 `LoggerConfig` 負責承載和驗證配置。
  - **API 清晰**：對外 API 變得更加簡潔和一致。
  - **擴展性增強**：未來增加新配置項只需修改 `LoggerConfig` 類別。

#### 建議 1.2：使用「發布/訂閱」模式解耦 `creator` 和 `proxy`

- **問題**：`creator` 和 `proxy` 之間的循環依賴。
- **方案**：
  1.  建立一個獨立的、全局的 `LoggerRegistry` 模組，包含一個簡單的字典和事件通知器 (event emitter)。
  2.  當 `reinit_logger` 被呼叫時，它在 `LoggerRegistry` 中更新 logger 實例，並發出一個事件，如 `logger_updated(name)`。
  3.  `LoggerProxy` 在初始化時，向 `LoggerRegistry` 訂閱這個事件。當接收到對應名稱的更新事件時，它會自動更新內部的 `_target_logger`。
- **好處**：
  - **完全解耦**：`creator` 不再需要知道 `proxy` 的存在，反之亦然。它們只與中介者 `LoggerRegistry` 互動。
  - **架構穩健**：移除了脆弱的循環依賴，使系統更加穩定和可預測。

### P2：程式碼精簡與品質提升 (中影響力，低複雜度)

#### 建議 2.1：動態生成 `LoggerProxy` 中的便利方法

- **問題**：`console_*` 和 `file_*` 方法大量重複。
- **方案**：利用 Python 的 `__getattr__` 或一個輔助方法來消除重複。
  ```python
  # 方案示例：
  class LoggerProxy:
      # ...
      def _log_to_target(self, level, target_only, message, *args, **kwargs):
          bind_key = f"to_{target_only}_only"
          logger = self._get_current_logger().bind(**{bind_key: True}).opt(depth=2) # depth 需要調整
          getattr(logger, level)(message, *args, **kwargs)

      def file_error(self, message, *args, **kwargs):
          self._log_to_target("error", "log_file", message, *args, **kwargs)

      def console_info(self, message, *args, **kwargs):
          self._log_to_target("info", "console", message, *args, **kwargs)
      # ... 其他方法可以類似地簡化
  ```
- **好處**：
  - **DRY (Don't Repeat Yourself)**：程式碼更簡潔，更易於維護。

#### 建議 2.2：允許自訂日誌壓縮檔名格式

- **問題**：日誌重命名邏輯寫死。
- **方案**：
  1.  在 `LoggerConfig` 中增加一個 `compression_format: Optional[str]` 參數。
  2.  修改 `_create_rename_function`，如果 `compression_format` 被設定，則使用它作為命名樣板，否則使用預設樣板。
- **好處**：
  - **提升靈活性**：將控制權交給使用者，滿足更多場景需求。

### P3：文檔與易用性改進 (持續進行)

#### 建議 3.1：撰寫「配置指南」

- **問題**：使用者可能不清楚 `component_name` 等參數的隱含行為。
- **方案**：在 `README.md` 或文檔中增加一個「配置指南」章節，清晰地解釋：
  - `LoggerConfig`, `preset` 和 `create_logger` 參數三者之間的關係和優先級。
  - `name` 和 `subdirectory` 如何共同決定最終的檔案路徑。
  - `component_name` 如何影響檔名，以及它如何導致日誌檔案被共享。
- **好處**：
  - **降低學習曲線**：幫助使用者快速理解並避免常見的配置陷阱。

---

## 5. 結論

`pretty-loguru` 已經是一個非常實用的函式庫。透過上述重構，特別是 P1 的核心解耦，可以將其從一個「優秀的個人專案」提升為一個「工業級、高度可維護的開源函式庫」，為未來的社群貢獻和功能擴展打下堅實的基礎。
