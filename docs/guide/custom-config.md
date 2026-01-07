# 自訂配置

本頁聚焦在「最新版」pretty-loguru 的可落地做法：盡量沿用 loguru 原生心智模型，避免自創太多參數與路徑。

## ✅ 優先使用 `LoggerConfig`（可重用、可同步更新）

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(
    level="INFO",
    log_dir="logs/app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
)

logger = create_logger("my_app", config=config, component_name="my_app")
config.apply_to("my_app")
```

`apply_to()` 會把 config 附加到 logger，之後 `config.update(...)` 會同步更新已附加的 logger。

## 📦 JSON 檔案日誌（ELK/Filebeat 建議）

只要開啟 `serialize=True`，pretty-loguru 的檔案輸出就會是 JSON line（利於 agent 收集與解析）：

```python
from pretty_loguru import create_logger

logger = create_logger(
    "json_app",
    log_dir="logs/json_app",
    serialize=True,
)
logger.info("structured message: user_id={user_id}", user_id=123)
```

## 🔧 追加 sinks（loguru 原生）

pretty-loguru 回傳的是 loguru logger，所以你可以直接用 `logger.add(...)` 加自己想要的 sink（這是最貼近 loguru 的方式）。

```python
from pretty_loguru import create_logger

logger = create_logger("app", log_dir="logs/app")

# 額外寫一份 warning 以上到另一個檔案
logger.add("logs/app/extra.log", level="WARNING")
```

注意：預設（`reset_handlers=False`）下，`reinit_logger()` 只會重建 pretty-loguru 自己管理的 handlers，保留你手動 `logger.add(...)` 的 sinks。  
若你希望連同手動 sinks 也一起移除，請顯式傳 `reset_handlers=True`。

## 🧩 Loki 直推（可選）

大多數生產環境更建議「`serialize=True` + Promtail/Grafana Agent」；若你無法部署 agent，才考慮直推：

- best-effort：不重試、無離線緩衝、無 backpressure；失敗即丟棄
- `loki_labels` 請避免高基數（例如 user_id / request_id）

```python
from pretty_loguru import create_logger

logger = create_logger(
    "loki_app",
    log_dir="logs/loki_app",
    serialize=True,
    loki_enabled=True,
    loki_base_url="http://localhost:3100",
    loki_labels={"app": "loki_app"},
)
logger.info("hello loki")
```

## 💾 從 JSON 檔案載入 / 保存配置

pretty-loguru 使用 `LoggerConfig.save()` / `LoggerConfig.load()`：

```python
from pretty_loguru import LoggerConfig

config = LoggerConfig(level="INFO", log_dir="logs/app", serialize=True)
config.save("configs/logging.json")

loaded = LoggerConfig.load("configs/logging.json")
```

如果你的覆寫來源是 dict（例如讀取 JSON/ENV），請用 `update_from_dict()`：

```python
loaded.update_from_dict({"level": "DEBUG", "serialize": True})
```

