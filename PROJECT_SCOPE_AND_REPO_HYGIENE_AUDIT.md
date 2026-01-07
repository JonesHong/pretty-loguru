# 專案範圍與 Repo 內容健檢（以 PyPI library 角度）

> 依據：目前 repo 實際內容 + `snapshot.md` 的結構快照  
> 目標：釐清哪些應屬於「library 核心」、哪些應屬於「範例/工具/網站」，避免 PyPI 專案看起來像一個「雜物倉庫」，也降低使用者誤解與維護成本。

---

## 0. TL;DR（先給結論）

1) `examples/observability/` 建議明確定位為 **examples**（而不是 core contract），並且在發佈/打包時不要把它當成 library 的一部分（避免使用者以為這是 runtime 依賴）。
2) 目前 repo 裡有幾組「重複或偏產物」的內容，會增加維護/理解成本：
   - `assets/images/*` 與 `docs/public/*` 過去曾完全重複；已選擇 `docs/public/` 作為單一來源
   - `configs/*.json` 與 `examples/04_configuration/configs/*.json` **完全重複**
   - `assets/logs/**/*.log` 是「輸出產物」性質（雖然很小），放在 PyPI 專案會讓人困惑
3) 若你想把 repo 做得更像「正規 PyPI lib」，建議採用明確分層：
   - `pretty_loguru/`：唯一 runtime 核心
   - `examples/`：使用範例（可保留在 repo）
   - `docs/`：文件網站（可保留在 repo）
   - `tools/`：開發工具/一鍵 demo（建議把 `observability/`、`snapshot.py` 這類東西歸類到這裡）

---

## 1. `examples/observability/` 到底該不該留在 PyPI 專案？

### 1.1 它「對 PyPI 使用者」的價值

`examples/observability/` 的內容（Docker compose、Loki/Grafana provisioning、Filebeat config、demo scripts）是**可執行的驗證環境**，對「想快速驗證你整合方案」的人很有幫助。

但它不屬於 library 的 runtime contract：
- 不是 import 後就會用到的功能
- 更像「運維 demo / 整合 cookbook」

### 1.2 建議定位（擇一）

**方案 A（推薦）：保留在 repo，但改成 tools 定位**
- 將 `observability/` 視為 `tools/observability/`（或 `tools/obs/`）  
- 在 `tools/observability/README.md` 明確寫：
  - 這是 demo/ops 工具
  - 需要 Docker
  - 不屬於 core library contract

**方案 B：保留在 repo 當 examples（目前採用）**
- 讓使用者把它當成範例環境：`examples/observability/`

**方案 C：獨立 repo（最乾淨，但管理成本更高）**
- 這通常適合團隊有專門 ops/infra repo 的情境

> 你的現況（公司內部團隊使用 + 想一鍵驗證）其實很適合方案 A。

---

## 2. 類似需要調整的內容（依 snapshot.md + repo 現況盤點）

### 2.1 重複資產：圖片

現況（已修正）：
- 已選擇 `docs/public/*` 作為唯一來源
- `assets/images/*` 已移除以避免重複維護

問題：
- 任何改圖都要改兩份，容易不同步

結果：
- README 圖片 URL 已改為引用 `docs/public/logo.png`

### 2.2 重複資產：config JSON

現況：
- `configs/app.json` == `examples/04_configuration/configs/app.json`（一致）
- `configs/logging.json` == `examples/04_configuration/configs/logging.json`（一致）

問題：
- config template 若未來改一邊，範例會悄悄過期

建議：
- 選一個 canonical location（通常 `configs/` 比較合理）
- examples 端不要複製檔案：用相對路徑引用、或在範例啟動時 copy 到暫存目錄

### 2.3 輸出產物：`assets/logs/**/*.log`

現況：
- `assets/logs/` 下有多個 `.log`（約 13 個檔案、總大小約 17KB）

問題（不是大小問題，是「語意問題」）：
- 這種檔案在 PyPI 專案看起來像 build artifact / demo output
- 容易造成使用者誤會：「這是你套件的一部分？還是你忘了清？」

建議（擇一）：
- 若只是展示 output：改成 `docs/` 的截圖/文字片段（例如 `.md` 內貼上精簡片段）
- 若要保留作為 fixture：放到 `tests/fixtures/`（並清楚命名/用途）
- 若只是歷史產物：建議刪除，透過 examples 跑一次就能生成

### 2.4 備份文件：`docs/_backup_old_examples/`

現況：
- snapshot 顯示此資料夾存在（備份舊寫法）

問題：
- 舊寫法會跟新 contract 混在一起（你已多次強調「不要向後相容，只保留最新」）
- Git 本來就能回溯歷史，這種「備份目錄」通常是多餘的長期負擔

建議：
- 直接移除（需要時用 Git 查歷史）

### 2.5 開發環境產物：`docs/node_modules/`

現況：
- snapshot 顯示 `docs/node_modules/` 存在（多半是本機安裝產物）

建議：
- 不要 commit（你 `.gitignore` 已有 `node_modules/`，很好）
- 若你擔心有人誤 commit，可在 CI 加檢查（例如檔案數/大小門檻）

### 2.6 內部審查/生成檔：`snapshot.md`, `snapshot.py`, 多份 review/plan `.md`

現況：
- repo 根目錄存在 `snapshot.*` 與多份「審查報告/計畫書」md（例如我們這段對話產出的多份）

問題：
- 對外部使用者來說容易困惑：哪份是官方文件？哪份是內部筆記？

建議：
- 統一歸檔到 `notes/` 或 `internal/` 或 `tools/`（例如 `tools/snapshot/`）
- 根目錄只保留：`README*`, `CHANGELOG.md`, `LICENSE`, `pyproject.toml`, `CONTRIBUTING.md`

---

## 3. 對 PyPI 發佈的「最低成本止血」建議（不改功能）

即使你不搬資料夾，也建議做兩件事來降低 PyPI 使用者看到的「雜訊」：

1) **明確在文件中標註 scope**
   - 在 `examples/observability/README.md` 開頭寫清楚：這是 examples，不是 core
2) **整理 repo 入口**
   - 根目錄保持乾淨，把「生成/審查/快照」移到 `notes/` 或 `tools/`

> 這兩件事不會改你的 API，也不會影響使用者 import，但會顯著提升專案的專業觀感。

---

## 4. 建議的下一步（若你要我開始動手改）

已套用的決策：

1) `observability`：採用 **examples**（`examples/observability/`）
2) 圖片唯一來源：採用 `docs/public/`
3) `.log`：維持 `.gitignore` 規則（`*.log` 已忽略）
