# 日誌輪轉（Rotation）

pretty-loguru 的檔案輪轉是交由 loguru 的檔案 sink 處理；你需要先啟用檔案輸出（設定 `log_dir`）才會發生輪轉、保留與壓縮。

## ✅ 重要前提：`log_dir` 是目錄

- `log_dir` 是**日誌檔案保存目的地目錄**
- 不指定 `log_dir` 時為 console-only，`rotation/retention/compression` 不會生效

## 🚀 基本用法

### 依檔案大小輪轉

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="size_rotation",
    log_dir="logs/app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
)
```

### 依時間輪轉（常見）

loguru 支援用時間字串，例如每天午夜輪轉可用 `"00:00"`：

```python
logger = create_logger(
    name="daily_midnight",
    log_dir="logs/app",
    rotation="00:00",
    retention="30 days",
    compression="gz",
)
```

## 🧩 使用 `ConfigTemplates`（建議）

pretty-loguru 內建多組輪轉模板（同時包含「檔名規則」與「輪轉後重命名」策略）：

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

config = ConfigTemplates.daily()   # daily/hourly/weekly/monthly/minute
create_logger("my_app", config=config, component_name="my_app")
config.apply_to("my_app")
```

### 這些模板的檔名設計（概念）

- 「當前正在寫入」通常是固定檔名（例如 `[{component}]daily_latest.temp.log`）
- 觸發輪轉時，會把輪轉出的檔案「重命名」成依日期/週/月的檔名（例如 `[{component}]20250113.log`）

這樣的好處是：

- 你永遠知道「現在」在哪個檔案寫入（latest）
- 輪轉出的檔案名稱適合歸檔、查詢與壓縮

## 📁 檔名規則與 `component_name`

pretty-loguru 預設的檔名（未指定 preset 時）大致是：

- `[{name}]_{timestamp}.log`

你可以用 `component_name` 讓檔名更符合服務識別：

```python
logger = create_logger(
    name="worker",
    component_name="payment-worker",
    log_dir="logs/payment",
    rotation="50 MB",
)
```

## ⚠️ 實務建議

- 高流量服務請避免過小 `rotation`（會造成頻繁輪轉與壓縮）
- 壓縮會消耗 CPU；若 CPU/IO 壓力大，可先關閉 `compression`
- 想接 ELK/Loki 建議搭配 `serialize=True` 輸出 JSON，再用 agent 收集
