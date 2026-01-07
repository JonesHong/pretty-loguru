# 核心模組 API

本頁文件描述 pretty-loguru **最新版**的核心合約（core contract）。

## `LoggerConfig`

`LoggerConfig` 是 pretty-loguru 的標準配置物件，可用於 `create_logger(...)` 與 `LoggerConfig.apply_to(...)`。

核心心智模型：**一份 config 可以管理多個 logger**；一旦附加後，後續 `update(...)` 會同步更新所有已附加的 logger。

```python
from pretty_loguru import LoggerConfig, create_logger

config = LoggerConfig(
    level="INFO",
    log_dir="logs/app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
    serialize=True,
)

logger = create_logger("my_app", config=config, component_name="my_app")
config.apply_to("my_app")
```

### 常用欄位

- `level`：最低日誌級別
- `log_dir`：檔案輸出目錄（`None` 代表只輸出到 console）
- `rotation` / `retention` / `compression` / `compression_format`：loguru 風格的輪替/保留/壓縮
- `format` / `component_name` / `subdirectory`：格式與命名控制
- `serialize`：檔案輸出改為 JSON line（建議用於 ELK/Filebeat/Promtail）
- `loki_enabled` + `loki_*`：可選 Loki 直推（best-effort：不重試、無離線緩衝、無 backpressure；失敗即丟棄）

注意：
- `name` 是 legacy 欄位（僅為舊設定保留）；請用 `create_logger("name", ...)` 指定 logger 名稱。

### 更新配置

`update(...)` 採顯式欄位（IDE 友善）。若你的覆寫來源是動態 dict（JSON/ENV），請用 `update_from_dict(...)`：

```python
config.update_from_dict({"level": "DEBUG", "serialize": True})
```

## `configure_logger(logger_instance, config, reset_handlers=False)`

用 `LoggerConfig` 配置 loguru logger instance。

預設只會移除 **pretty-loguru 自己管理的** handlers；若你希望連同使用者手動 `logger.add(...)` 新增的 sinks 也一起移除，請顯式傳 `reset_handlers=True`。

## 目標導向（console/file routing）

pretty-loguru 使用 record extra 控制每筆訊息的輸出去向：

- `to_console_only=True`：只輸出到 console
- `to_file_only=True`：只輸出到 file

建議用 helper `log_to_targets()`：

```python
from pretty_loguru.addons import log_to_targets

log_to_targets(logger, "both")
log_to_targets(logger, "console only", console_only=True)
log_to_targets(logger, "file only", file_only=True)
```

