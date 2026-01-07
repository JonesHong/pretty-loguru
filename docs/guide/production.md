# 生產環境建議（Production）

本頁聚焦在「可落地」的生產設定：可控、可追蹤、可擴展到 ELK/Loki，同時避免常見的 I/O 與檔案鎖問題（特別是 Windows）。

## ✅ 生產環境基本建議

- `level`：通常至少 `INFO`，並保留 `WARNING/ERROR`；避免長期 `DEBUG`
- `log_dir`：請使用**目錄**（例：`logs/my_service`），並確保有寫入權限
- `rotation`：避免太小（高流量服務建議 `"100 MB"` 以上）
- `retention`：用時間字串控制（例：`"30 days"`）
- `compression`：壓縮省空間但吃 CPU，流量大時可先關閉再評估
- `serialize=True`：輸出 JSON，利於 agent 收集與解析
- `start_cleaner=True`：若啟用清理器，請用 include/exclude patterns 限定掃描範圍

## 🚀 參考配置（單服務）

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="my_service",
    component_name="my_service",
    level="INFO",
    log_dir="logs/my_service",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
    serialize=True,
    start_cleaner=True,
    cleaner_include_patterns=["*.log", "*.log.*"],
    cleaner_exclude_patterns=["*.lock"],
)
```

## 🧩 多服務（微服務 / 多模組）

建議用同一套模板快速建立，再視需求分拆：

```python
from pretty_loguru import LoggerConfig, create_logger

base = LoggerConfig(
    level="INFO",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
    serialize=True,
)

for service in ["api", "worker", "scheduler"]:
    create_logger(service, config=base, log_dir=f"logs/{service}", component_name=service)
    base.apply_to(service)
```

## 📦 ELK / Loki（建議路線）

大多數情況建議「檔案輸出 + agent」：

- ELK：`serialize=True` + Filebeat/Fluent Bit
- Loki：`serialize=True` + Promtail/Grafana Agent

若要直接推送 Loki（可選）：

```python
logger = create_logger(
    "my_service",
    log_dir="logs/my_service",
    serialize=True,
    loki_enabled=True,
    loki_base_url="http://localhost:3100",
    loki_labels={"app": "my_service"},
)
```

注意：
- `loki_enabled=True` 是 best-effort 直推：**不做重試、沒有離線緩衝、也不提供 backpressure**；送出失敗會直接丟棄該批次。
- `loki_labels` 請避免高基數（例如 user_id / request_id），否則會讓 Loki 的 index 成本飆升。

## 🪟 Windows 注意事項

- Windows 對檔案鎖更敏感：重新初始化/關閉 logger 前，確保 handler 已被 `remove()`（pretty-loguru 已做處理）
- 若你在開發時頻繁重啟服務，請避免把 `log_dir` 指向會被其他程式鎖住的目錄（例如正在被監控/同步的資料夾）
