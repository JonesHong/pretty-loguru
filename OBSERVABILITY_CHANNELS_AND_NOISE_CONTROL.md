# Loki / ELK：目前資料流與「降低雜訊」的設計調整建議（報告）

> 範圍：以 `pretty_loguru/` 目前行為為準，說明 Loki/ELK 的資料進出路徑與問題，並提出新增「特殊管道」(例如 `logger.loki()` / `logger.elasticsearch()`) 的設計方案。  
> 目標：保留現有方式（寫檔 + agent 收集 / Loki 直推），但提供一個 **更高訊噪比**、**使用者顯式選擇** 的遠端管道，避免把所有 `.log` 內容都送到 Loki/ES 造成雜訊與成本。

---

## 1. 結論先講清楚（你問的那句）

### 1) Loki：目前是「可直推」，不是只能讀 `.log`

- 程式碼已內建 Loki 直推 sink：`pretty_loguru/integrations/loki.py`
- `create_logger(..., loki_enabled=True, loki_base_url=...)` 會在 `pretty_loguru/core/base.py:268` 幫你把 Loki sink `logger.add(...)` 掛上去。
- 目前的 Loki 直推是 **best-effort**（掉包就掉包）：不重試、無離線緩衝、無 backpressure（檔案與 docs 也有描述）。

### 2) ELK：目前 core 是「讀 `.log`（檔案收集）」導向

- `pretty_loguru/` 目前沒有 Elasticsearch/Logstash 的「內建直推 sink」。
- 目前 ELK 的設計是：
  - **應用端**：寫檔，並建議 `serialize=True` 產生 NDJSON（每行一筆 JSON）
  - **收集端**：Filebeat 讀取 `.log` 再送 ES  
    參考：`examples/observability/elk/filebeat.yml`

> 所以你現在的直覺是對的：**ELK 目前就是讀 log 檔**；Loki 則同時具備「讀檔(建議 promtail/agent)」與「程式直推」兩條路。

---

## 2. 目前設計的核心問題：為什麼「直接讀 log」會讓你不放心

你提到「直接讀 log 太多雜訊」——這其實是 observability 常見的結構性問題，根源通常不是 Loki/ELK，而是 **log 的用途混在一起**：

1) **開發用噪音**與**營運用訊號**混在同一條流  
   - debug、retry、heartbeat、框架 access log、第三方庫 log… 都會被收走
2) **查詢/成本會爆**  
   - Loki/ES 都不是「免費的檔案硬碟」，它們的索引、儲存、查詢會放大成本  
3) **語意不清楚**  
   - 一般 log 與「安全/稽核事件」「商業事件」「告警事件」混在一起，後續很難治理
4) **在 Loki 上尤其容易踩到 label 高基數**（即便你不想）  
   - 例如把 `user_id`、`request_id` 放到 labels 會直接讓 Loki 成本爆炸（你文件也已提醒避免高基數）。

因此你想要的「特殊管道」其實是在做一件對的事：**把高訊噪比事件跟一般 log 拆開**，讓 Grafana/ES 上看到的是「你刻意送去的訊號」，而不是整包 `.log`。

---

## 3. 目前 Loki 直推的「隱性雜訊來源」（程式碼層面）

在 `pretty_loguru/core/base.py`，Loki handler 目前使用：

- `serialize=True`（很好，利於解析）
- 但 `filter=filters["file"]`
  - 這表示：**只要不是 `to_console_only=True` 的 log，都會被視為「要進 file」→ 同時也會進 Loki**  
  - 換句話說：Loki 目前是「mirror 檔案流」的概念，而不是「只送你指定的訊息」

這就是你說的「雜訊太多」的直接原因之一：即便你開了 loki 直推，本質上是在把「file 的全部 log」也推走。

---

## 4. 你想要的能力：兩種模式其實都該保留

你說「當然現在方式仍可保留，但希望有特殊管道」——我會把需求翻譯成兩種模式（都合理）：

### A. 全收集（現況）：檔案/直推都收「全部 log」

優點：
- 最簡單：不需要使用者多想
- 對 incident/troubleshooting 有幫助：完整時間序列

缺點：
- 雜訊大、成本高、治理難

### B. 高訊號管道（你要的）：只收「你顯式選擇」的 log/event

優點：
- 成本可控、查詢乾淨、Grafana/ES 上看到的就是你要看的
- 可用來做：security audit、business event、SLO anomaly、監控告警

缺點：
- 需要一個明確 API/合約，否則使用者會誤用

**我的建議：A 保留、B 新增，且 B 應該是可預期且可測的合約。**

---

## 5. 建議的設計調整（核心）

### 5.1 建立「輸出目標 routing 合約」（不要只靠檔案 filter）

目前你已經有兩個 routing flag：
- `to_console_only`
- `to_file_only`

建議新增兩個（或更多）明確旗標：
- `to_loki_only`
- `to_elasticsearch_only`

然後把 filter 擴充成四種目的地：
- `filters["console"]`
- `filters["file"]`
- `filters["loki"]`（預設：只有 `to_loki_only=True` 才會進）
- `filters["elasticsearch"]`（預設：只有 `to_elasticsearch_only=True` 才會進）

> 這樣就能做到：「一般 log 照樣寫檔/顯示；只有指定 log 才會送 Loki/ES」。

### 5.2 提供你要的 API：`logger.loki()` / `logger.elasticsearch()`

我建議把 API 設計成「顯式且不含糊」，避免 `logger.loki("...")` 到底是 INFO 還是 ERROR 的語意不清。

**推薦（最貼近 loguru 習慣）：回傳一個 bound logger**

- `logger.loki()` 回傳 `logger.bind(to_loki_only=True)`  
  使用者可以照 loguru 原生方式使用 level：
  - `logger.loki().info("...")`
  - `logger.loki().error("...")`
- `logger.elasticsearch()` 同理

這樣的優點：
- **不發明新語法**：仍是 loguru 的 `.info/.error/.log` 那套
- 語意清楚：`.loki()` 只是在「選路由」，不是決定 level

**也可額外提供糖衣（你偏好的一行式）：**

- `logger.loki_log(message, level="INFO", **kwargs)`
- `logger.elasticsearch_log(message, level="INFO", index=..., **kwargs)`

但核心最好還是用 `.bind(...)` 的方式，因為它跟 loguru 的心智模型一致，學習曲線最低。

### 5.3 Loki 端的設計調整：把它從「mirror file」改成「專用通道」

現在 Loki handler 的 filter 用的是 `filters["file"]`。  
若要做出「高訊號管道」，應改成 `filters["loki"]`（只吃 `to_loki_only=True` 的 record）。

另外，Loki 直推現在用 `serialize=True` 很好，但仍需注意：
- labels 必須避免高基數（你已經知道）
- message 的 JSON 結構要固定（最好是 loguru serialize 結構 + 你自己 extra 的 schema）

### 5.4 Elasticsearch/ELK：建議先用「filebeat 讀檔」保底，再做「選擇性直推」

你目前的 `examples/observability/elk/filebeat.yml` 已經是「檔案收集」路線，這條路應保留（可靠、成熟）。

但若你要 `logger.elasticsearch()`：

- 我建議做成 **可選的 direct sink**（類似 LokiSink），支援：
  - Bulk API (`POST /_bulk`)
  - 批次/flush interval
  - best-effort（跟 Loki 一致）或可選 retry（看你要不要承擔複雜度）
- 並且預設只吃 `to_elasticsearch_only=True` 的 record

> 這樣你可以同時擁有：
> - 全量：檔案 → filebeat → ES（背景全收集）
> - 高訊號：`logger.elasticsearch()` → ES（只送你刻意挑的事件）

---

## 6. 可靠性與工程複雜度：你必須先做的取捨（很重要）

如果你要「程式直推」到 Loki/ES，你其實在自己做一個 log shipper，會遇到這些議題：

1) 網路不穩怎麼辦？（timeout / retry / backoff）
2) 程式退出時 flush 不完整怎麼辦？
3) queue 滿了怎麼辦？（backpressure vs drop）
4) 多進程/多執行緒時的安全性？
5) 敏感資料治理（PII mask）在哪一層做？

你現在 Loki 直推採 best-effort（我同意這個取捨，KISS），那麼 `logger.elasticsearch()` 若要加，也建議同樣 best-effort，**避免把可靠性工程塞進 logging lib**。

若你的目標是「可營運、可追責」的可靠管道，那就應該交給 agent（promtail/filebeat/fluent-bit），而不是 library。

---

## 7. 我建議的「下一步調整計畫」（不含實作細節的設計步驟）

1) **定義 routing 合約（核心）**
   - 新增 `to_loki_only`、`to_elasticsearch_only`
   - 擴充 destination filters：`loki`、`elasticsearch`

2) **Loki：調整成專用通道**
   - Loki handler filter 改用 `filters["loki"]`
   - 增加可選模式（若你仍想保留 mirror-file 行為）：例如 `loki_mode = "mirror_file" | "explicit_only"`

3) **注入 logger 方法（你要的 API）**
   - `logger.loki()` → 回傳 bound logger（最貼近 loguru）
   - `logger.elasticsearch()` → 回傳 bound logger

4) **ELK：新增 direct sink（可選）**
   - 先以 stdlib HTTP 實作最小 Bulk API（避免強依賴）
   - 或明確加一個可選依賴（但你目前策略是「一包全裝」，就看你是否接受額外依賴成本）

5) **示範與治理**
   - 提供範例：什麼該用 `logger.info()`，什麼該用 `logger.loki().info()`（例如 security/business/audit）
   - 提供 anti-pattern：不要把 request_id/user_id 放到 loki labels

---

## 8. 你現在最關心的「雜訊」：我會如何定義與止血

我建議你把「送到 Loki/ES 的內容」定位成 **event stream（事件流）**：

- 預設不送「一般 log」到 Loki/ES（或至少不直推）
- 只有符合以下條件之一才送：
  - 明確使用 `logger.loki()` / `logger.elasticsearch()`
  - 或 `pretty_kind`/`pretty_payload` 這種結構化事件（若你想把它合約化）

這樣 Grafana/ES 的內容會「乾淨得像 metrics」，而檔案 log 仍保留全量供 debugging。

---

## 9. 你下一步要我做什麼（確認點）

如果你同意上述方向，我下一步可以直接開始做實作，順序建議：

1) 先做 routing flags + `logger.loki()`（只改 Loki，不碰 ES）
2) 把 Loki handler 改成只吃 `to_loki_only=True`（或加 `loki_mode`）
3) 再設計 `logger.elasticsearch()`（先做「檔案收集」的 best practice，再決定要不要做 direct push sink）

你只要回覆我：
- `loki_enabled=True` 的預設行為要不要改成「只送 explicit」（會改變目前行為），或要用 `loki_mode` 兼容兩種模式？
