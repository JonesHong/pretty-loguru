# 效能最佳化

在大多數服務中，日誌的效能瓶頸通常不在「logger 本身」，而是在：

- 不必要的字串組合與資料序列化
- 同步 I/O（寫檔、壓縮、頻繁輪轉）
- 在熱路徑（hot path）大量記錄低價值訊息

pretty-loguru 的定位是「把常見、可預期的 loguru 使用方式做封裝」，因此效能調整也建議以「降低不必要輸出」與「降低 I/O 壓力」為優先。

## ✅ 你在 pretty-loguru 能調的重點

- `level`：最直接的降噪／降成本手段（生產環境通常避免 `DEBUG`）
- `log_dir`：**日誌檔案輸出目的地目錄**；不指定就是 console-only
- `rotation` / `retention` / `compression`：輪轉太頻繁會造成大量 I/O 與壓縮成本
- `use_native_format`：使用 loguru 原生格式（較少自訂 extra 介入）
- `serialize`：檔案輸出改為 JSON（利於 Filebeat/Promtail 等 agent 解析）
- `start_cleaner` + `cleaner_include_patterns` / `cleaner_exclude_patterns`：避免掃描不必要的檔案
- `loki_enabled`：可選擇直接推送 Loki（通常更建議用 agent 方式集中收集）

## ⚡ 基準測試（簡化且可重現）

```python
import time
from pretty_loguru import create_logger

def bench(logger, iterations: int = 20000) -> None:
    start = time.perf_counter()
    for i in range(iterations):
        logger.info("bench message {i}", i=i)
    elapsed = time.perf_counter() - start
    print(f"{iterations} ops, {elapsed:.3f}s, {iterations/elapsed:.0f} ops/s")

# 只輸出到控制台（不指定 log_dir）
console_logger = create_logger("bench_console", level="INFO")

# 輸出到檔案（log_dir 是目錄）
file_logger = create_logger("bench_file", level="INFO", log_dir="logs/bench")

bench(console_logger)
bench(file_logger)
```

## 🧠 程式碼層面的效能習慣

### 1) 避免在低等級日誌做昂貴計算

loguru 支援 lazy evaluation：

```python
from pretty_loguru import create_logger

logger = create_logger("app", level="INFO")

def expensive():
    time.sleep(0.1)
    return {"heavy": "payload"}

# 只有在 DEBUG 真的會被輸出時才計算 expensive()
logger.opt(lazy=True).debug("expensive payload: {payload}", payload=expensive)
```

### 2) 優先用結構化欄位，而不是拼字串

```python
logger.info("user login: user_id={user_id} ip={ip}", user_id=123, ip="1.2.3.4")
```

如果你要把 log 串接到 ELK/Loki，建議搭配 `serialize=True`（JSON 檔案輸出）與 agent（Filebeat/Promtail）解析與轉送。

## 💾 I/O 與輪轉策略

- **減少輪轉頻率**：增大 `rotation`（例如 `"500 MB"`）可顯著降低輪轉與壓縮開銷
- **壓縮不是免費**：高流量服務若 CPU/IO 壓力大，可考慮關閉 `compression`
- **console-only 的成本通常更低**：對熱路徑可用 console-only + 上層收集（或只留 WARNING/ERROR）

## 🧹 Cleaner（清理器）注意事項

`start_cleaner=True` 會啟動背景清理；在大量檔案目錄、或 log 目錄混雜其他檔案時：

- 請用 `cleaner_include_patterns` 限定清理範圍（例如 `["*.log", "*.log.*"]`）
- 用 `cleaner_exclude_patterns` 排除 lock/暫存檔（例如 `["*.lock"]`）
- 生產環境建議 `verbose=False`，避免額外輸出

## 🧩 Loki / ELK 的效能選擇（建議）

通常建議用「檔案輸出 + agent」：

- ELK：`serialize=True` + Filebeat（或 Fluent Bit）
- Loki：`serialize=True` + Promtail（或 Grafana Agent）

只有在你非常確定網路可用性、重試策略、與 backpressure 行為時，才建議使用 `loki_enabled=True` 直接推送；pretty-loguru 的直推是 **best-effort**：不重試、沒有離線緩衝、也不提供 backpressure，送出失敗會直接丟棄。
