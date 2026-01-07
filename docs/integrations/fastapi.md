# FastAPI 整合

pretty-loguru 提供 FastAPI 的請求/回應日誌整合，以及 Uvicorn 日誌統一（同格式輸出）。

## 🚀 快速開始（建議）

```python
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

app = FastAPI(title="My API")

logger = create_logger(
    name="api",
    component_name="my_api",
    log_dir="logs/api",      # 注意：log_dir 是目錄
    level="INFO",
    rotation="50 MB",
    retention="30 days",
    serialize=True,           # JSON 檔案輸出（便於 ELK/Loki/Promtail/Filebeat）
)

integrate_fastapi(app, logger, enable_uvicorn=True)
```

## 🧩 依賴注入（每個 route 取得 logger）

```python
from fastapi import FastAPI, Depends
from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import get_logger_dependency

app = FastAPI()

logger = create_logger("api_route", log_dir="logs/api", level="INFO")
get_logger = get_logger_dependency(logger)

@app.get("/health")
def health(logger=Depends(get_logger)):
    logger.info("health check")
    return {"status": "ok"}
```

## ⚙️ 控制要記錄的內容

`integrate_fastapi()` / `setup_fastapi_logging()` 支援常見控制項：

- `exclude_paths` / `exclude_methods`：排除噪音路徑（例如 `/health`）
- `log_headers`：是否記錄 request headers（預設 True）
- `sensitive_headers`：遮蔽敏感 headers
- `log_request_body` / `log_response_body`：是否記錄 body（預設 False）
- `max_body_bytes`：限制 body 的最大大小（bytes），避免巨大日誌

## 🔒 安全 / 隱私 / 效能注意事項（重要）

- **一般 logging（推薦）**：只記錄 method/path/status/latency/headers（遮蔽敏感欄位），風險最低。
- **body 記錄（高風險，需顯式啟用）**：`log_request_body/log_response_body=True` 可能把密碼、token、PII、檔案內容寫入 log。
- **請求大小與記憶體**：即使有 `max_body_bytes`，上游若一次送很大的 chunk，仍可能暫存較大的資料；建議在 server/proxy 層限制 request size。
- **unknown content-length**：預設不讀取 body；若你啟用 `log_request_body_if_unknown_length=True`，只會預覽前 `max_body_bytes`，且保留原始 body 供後續處理。

## 🧱 可組裝（低階 building blocks）

若你想自己掌控安裝步驟，可直接使用：

- `install_fastapi_middleware(...)`：只安裝 `LoggingMiddleware`
- `install_fastapi_route_class(...)`：只設定 `LoggingRoute`（`app.router.route_class`）

## 📦 Loki / ELK 建議

- ELK：`serialize=True` + Filebeat/Fluent Bit
- Loki：Promtail/Grafana Agent（或 `loki_enabled=True` 直推；best-effort：不重試、無離線緩衝、無 backpressure；失敗即丟棄）
