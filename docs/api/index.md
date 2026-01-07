# API 參考（總覽）

本頁提供 pretty-loguru 的公共 API 總覽與常用用法。若你需要完整、逐參數的最新清單，請以專案根目錄的 `snapshot.md` 為準。

## ✅ 核心規則

- `log_dir` 是**日誌檔案保存目的地目錄**（不是檔案路徑）
- 不指定 `log_dir` 時為 console-only（檔案輪轉/保留/壓縮不生效）

## 🚀 核心 API

### `create_logger()`

建立或取得註冊在內部 registry 的 logger。

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="my_app",
    component_name="my_app",
    level="INFO",
    log_dir="logs/my_app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
)
```

**參數備註：**

- `enable_addons`（預設 `True`）：是否注入 addons（例如 targets / Rich / ASCII 等加值方法）。若你只需要純 core（或想避免載入 Rich/art 等相依），可設為 `False`。

### `reinit_logger()`

更新**已存在**的 logger（維持同一個 registry 實例），用於動態調整設定：

```python
from pretty_loguru import create_logger, reinit_logger

logger = create_logger("service", log_dir="logs/service", level="INFO")
reinit_logger("service", level="DEBUG", rotation="10 MB")
logger.debug("DEBUG enabled")
```

**handler 行為（很重要）：**

- 預設（`reset_handlers=False`）只會重建 pretty-loguru 自己管理的 handlers，不會移除你自行 `logger.add()` 的 sinks
- 若你想把同一個 logger 上「包含你自己 add 的 sinks」也一起重置，請傳 `reset_handlers=True`（顯式選擇）

### 取得/列出/清理 logger

```python
from pretty_loguru import get_logger, list_loggers, cleanup_loggers

logger = get_logger("service")
names = list_loggers()
cleanup_loggers()
```

## 🧩 配置系統

### `LoggerConfig`

可重用的配置模板。`apply_to()` 會套用到指定名稱的 logger，並把它們加入追蹤，使後續 `update()` 能自動同步更新。  
最新版預設 `create_if_missing=True`：當指定的 logger 不存在時會自動建立；若你希望嚴格只操作已存在 logger，請設 `create_if_missing=False`。

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(level="INFO", log_dir="logs/app", rotation="00:00", retention="14 days")

create_logger("api", config=config)
create_logger("worker", config=config)
config.apply_to("api", "worker")

config.update(level="DEBUG")
```

### `ConfigTemplates`

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

prod = ConfigTemplates.production()
create_logger("my_app", config=prod)
prod.apply_to("my_app")
```

## 🎯 目標導向輸出

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets

logger = create_logger("targets", log_dir="logs/targets")
log_to_targets(logger, "both")
log_to_targets(logger, "console only", console_only=True)
log_to_targets(logger, "file only", file_only=True)
```

## 🔌 整合（Integrations）

- FastAPI：`pretty_loguru.integrations.fastapi.integrate_fastapi()` / `setup_fastapi_logging()` / `get_logger_dependency()`
- Uvicorn：`pretty_loguru.integrations.uvicorn.integrate_uvicorn()`

## 📦 ELK / Loki（可觀測性）

- ELK：`serialize=True`（JSON 檔案）+ Filebeat/Fluent Bit 收集
- Loki：建議 Promtail/Grafana Agent；或使用 `loki_enabled=True` 直接推送（best-effort：不重試、無離線緩衝、無 backpressure；失敗即丟棄）
