# 本次 Git 變更檢視（變更意義與影響分析）

> 本文件以「目前工作目錄相對於 HEAD 的差異」為準（含已追蹤檔案的修改/刪除，以及尚未加入版本控制的新增檔案）。  
> 你先前要求多次「不追求向後相容、以最新版本為準」與「預設重載 addons」；本次變更即以此方向落地。

## 1) 我們做了哪些事（總覽）

### A. 主要目標（你當時的核心需求）
1. **終端機輸出與檔案輸出語意一致**：同一筆事件走同一套 payload/extra，console 以 Rich render、file 以 pretty_text 附加，避免雙路徑漂移。
2. **保持 loguru 使用體驗**：以 loguru public API（`patch/bind/filters/add/remove`）為主，不依賴私有 API；使用者仍可用熟悉的 `logger.bind()/logger.opt()`。
3. **預設重載（一次綁定 rich/art/figlet/整合）**：以「內部團隊開箱即用」優先，並補上降級路徑與效能優化。
4. **可更新與可控副作用**：`reinit_logger()` 改成可預期（不會意外丟失原設定）、整合（uvicorn/fastapi）提供還原或較低副作用路徑。
5. **品質與信心**：測試覆蓋率提升到 90%+，避免重構後不確定性。

### B. 變更範圍（以 git 類型分類）
- **大量修改**：`pretty_loguru/`（核心邏輯、formats、integrations、config/registry）、`pyproject.toml`、README/Docs/Examples（同步新 API）。
- **刪除過時內容**：`docs/_backup_old_examples/*`、部分舊 examples（例如 enhanced/native 對比舊腳本）。
- **新增檔案（目前多數仍未 git add）**：
  - 新增核心模組：例如 `pretty_loguru/utils/warn_once.py`、`pretty_loguru/core/diagnostics.py`
  - 新增整合/觀測：`pretty_loguru/integrations/loki.py`、`examples/observability/`（觀測環境範例）
  - 大量新增測試：`tests/*`（用於把 coverage 拉到 90%）
  - 其他：`.github/workflows/tests.yml`、`uv.lock`、`.coverage`（其中 `.coverage` 多半應該加入 `.gitignore`）

## 2) 這些改動的意義是什麼（設計層面的「為什麼」）

### 2.1 以 shared core 為前提，建立「隔離合約」
loguru 的 logger 預設共享 core（handlers/queue）。你要的「一包整合」意味著同一程序裡可能建立多個 logger（不同 component/service），若沒有隔離機制就會互相干擾（重複輸出、串 sink、console/file 路由混亂）。

因此本次把隔離核心落在：
- `patch_record` 強制補齊/保護 `extra.logger_id` 與必要的 `pretty_*` 欄位
- 透過 `filters` 讓每個 handler 只吃對應 `logger_id`

意義：**你可以保留重載 addons 與整合功能，同時維持多 logger 的可預期性。**

### 2.2 把「副作用」變成可被控制與可還原
重載 + 整合（uvicorn/fastapi）必然帶副作用（patch logging、注入 middleware/route_class）。本次的價值在於：副作用不再「不可逆、不可見」。

代表性落地：
- `pretty_loguru/integrations/uvicorn.py`：monkeypatch 路徑提供 `restore_uvicorn_logging()`，並可選擇 snapshot 範圍（含 `snapshot_all_loggers`）。
- `pretty_loguru/integrations/fastapi.py`：提供 `restore_fastapi_logging()`（至少還原 route_class），並額外提供 `build_fastapi_logging_options()` 讓使用者走「不直接改 app」的組裝方式。

意義：**在內部大型服務/測試環境中，你可以更安全地做整合，並可在需要時回復狀態。**

### 2.3 把「可用性」和「穩定性」拉到可發版水位
你希望「不要討好、要能真的用」，因此本次對於「會讓使用者踩坑的默默失效」做了補強：
- `reinit_logger()` 不再輕易把原本配置掉回預設（改為以既有 `_pretty_loguru_config` 為 base 再覆寫顯式參數）。
- cleaner 行為開始對齊 config（例如 retention 被帶入），避免「配置寫了但永遠沒生效」。
- 依賴缺失的告警不再污染 logger sink（避免寫入檔案/console，反而破壞主要輸出）。

意義：**行為可預期、錯誤可見、且不會在生產中默默壞掉。**

## 3) pretty_loguru/ 的重點改動（按模組分解）

> 以下只抓「與核心邏輯/使用者行為」高度相關者；細節以 diff 為準。

### 3.1 `pretty_loguru/factory/creator.py`（logger 建立/更新的核心）
主要改動意義：
- **統一 shared-core 隔離策略**：建立 logger 時透過 `patch_record` 強制 `logger_id` 穩定，並確保必要 extra 存在。
- **追蹤使用者 handler ids**：包裝 `logger.add()`，紀錄由該 logger 實例建立的 handler，讓 `reset_handlers=True` 能「只移除自己的」。
- **清理器（cleaner）管理**：以路徑為 key 管理清理器實例，並加入 lock 避免多執行緒競態；並把 retention 帶入 cleaner。
- **reinit_logger 語意修正**：以既有 `_pretty_loguru_config` 合併，避免只改一個參數卻讓其他設定掉回預設。
- **提供顯式清空能力**：新增 `clear_fields`，解決「只覆寫非 None」導致無法清空 log_dir 等設定的問題。
- **addons 預設策略可控**：`enable_addons` 仍預設為重載，但可用環境變數做全域預設控制。

帶來的價值：
- 多 logger 共用 core 的穩定性提升
- 更新設定（reinit）不會默默停寫檔案
- Windows 檔案鎖/handler 釋放更可控

### 3.2 `pretty_loguru/core/base.py`（handlers/filters/console+file pipeline）
主要改動意義：
- console 分成 plain + pretty sink，pretty sink 透過 `pretty_kind/payload` 走 Rich render，確保終端視覺化與檔案可重現（via pretty_text）。
- filter 以 `logger_id` 做隔離，並補上「缺 logger_id 時允許通過」的 fallback（避免公開 API 在非標準用法下完全沒輸出）。
- Loki sink 初始化改為 best-effort：失敗只警告不炸主 logger。
- reset_handlers 行為更清楚：移除 managed/user handler 時失敗會警告，不再靜默吞掉。

帶來的價值：
- 「console 與 file 語意一致」落地
- 共享 core 時不互相干擾
- 整合失敗不影響主流程

### 3.3 `pretty_loguru/formats/*`（block/rich/ascii/figlet）
主要改動意義：
- `ascii_art.py` / `figlet.py`：加入渲染快取（LRU cache）與 `strict` 模式；缺依賴時降噪（warn_once）並安全返回。
- `formats/__init__.py`：figlet 初始化失敗改用 warn_once，移除 import 階段的 print 汙染。
- rich components 與 block 的行為同步：讓 pretty payload 更一致、減少重複渲染成本（細節依實際 diff）。

帶來的價值：
- 重載 addons 下仍能控制啟動成本（lazy import + cache）
- 缺依賴不會把 warning 寫進 log 檔、也不會刷爆 console
- 提供 strict 模式給「想要 fail-fast」的場景

### 3.4 `pretty_loguru/integrations/*`（fastapi/uvicorn/loki）
主要改動意義：
- `uvicorn.py`：monkeypatch 支援還原，且可選擇 snapshot 範圍，避免污染整個 logging 系統。
- `fastapi.py`：提供更低副作用的 options builder，並提供部分 restore；缺依賴時告警更聚焦。
- `loki.py`（新增）：提供 best-effort 的 Loki sink（Grafana/Loki pipeline 的基礎）。

帶來的價值：
- 內部服務整合更安全、可回復、可測試

### 3.5 `pretty_loguru/utils/*`（依賴檢查與警告）
主要改動意義：
- `warn_once.py`：同一類警告只提醒一次，避免在大量 logger/多執行緒情境造成噪音與 IO 成本。
- `dependencies.py`：依賴缺失警告改集中處理，fallback 路徑補齊 `warnings` import，避免 NameError。

帶來的價值：
- 降噪 + 穩定性（避免把 warning 當成 log 事件寫入檔案）

### 3.6 `pretty_loguru/core/diagnostics.py`（新增觀測/排障 API）
提供：
- active cleaners 路徑
- managed/user handler ids
- default logger 是否初始化

意義：**更容易排查「為什麼重複輸出/為什麼沒寫檔/為什麼 handler 沒釋放」。**

## 4) 測試與品質（為什麼要做這麼多 tests）
本次變更屬於「重構 + 行為合約化 + 整合副作用」的大改，最容易發生：
- shared core 串音（重複輸出/跨 logger 互相影響）
- handler 沒釋放（Windows 檔案鎖）
- monkeypatch 影響其他測試/程序

因此新增大量測試與隔離機制（`tests/conftest.py`）的意義是：
- 把「核心行為」鎖死，避免未來改到又壞回去
- 讓你可以更放心地繼續迭代（尤其是你很在意事業風險）

## 5) 打包與依賴（pyproject.toml 的意義）
`pyproject.toml` 的主要意義：
- 把你「一包整合」的依賴（loguru/rich/art/fastapi/uvicorn 等）明確化
- 提供 extras（例如 figlet/all）讓外部使用者可選擇增量安裝（即使預設仍走全裝策略）
- dev dependencies 具體化（pytest 等），支援 CI

## 6) 風險與需要你決策的點
1) **變更量非常大**：建議你最後 commit 前拆成多個 commit（core / integrations / formats / tests / docs）以利回溯。
2) **未追蹤檔案需決策**：
   - 建議加入 git：`pretty_loguru/utils/warn_once.py`、`pretty_loguru/core/diagnostics.py`、新增的 tests、workflow
   - 建議忽略：`.coverage`（測試產物）、可能還有 logs/temporary files
   - 需決策：`examples/observability/`、`uv.lock` 是否納入 repo（取決於你是否要固定解析出的依賴鎖定）
3) **CRLF/LF 警告**：目前 git 提示多個檔案行尾將被轉換，若你團隊跨平台，建議明確設定 `.gitattributes`（避免 PR 出現大量行尾噪音）。

## 7) 建議的下一步（如果你要把這次變更發版）
1) 清理工作目錄產物：將 `.coverage` 加入 `.gitignore`，確認 logs/temp 不會被誤提交。
2) 決定是否提交 `uv.lock` 與 `examples/observability/`（若要 reproducible build/本機一鍵啟動可提交；否則放到 ops repo）。
3) 把「重大行為變更」整理到 release notes（例如 `reinit_logger` 合約、cleaner retention 生效、integrations restore）。
