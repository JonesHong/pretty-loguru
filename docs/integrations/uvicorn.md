# Uvicorn 整合

pretty-loguru 可以攔截 Uvicorn 使用的標準 `logging` 輸出，並轉送到你的 pretty-loguru logger，讓整個服務（含 Uvicorn）都用同一套格式與輸出策略。

## 🚀 基本用法

```python
# main.py
from fastapi import FastAPI
import uvicorn

from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

app = FastAPI()

logger = create_logger(
    name="my_app",
    component_name="my_app",
    log_dir="logs/my_app",   # 注意：log_dir 是目錄
    level="INFO",
)

# 建立 uvicorn 的 log_config（non-monkeypatch，推薦）
log_config = integrate_uvicorn(logger)

@app.get("/health")
def health():
    logger.info("health check")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
```

## ⚙️ 常用選項

- `integrate_uvicorn(logger, log_level="INFO")`：調整攔截等級（回傳 log_config）
- `integrate_uvicorn(logger, logger_names=[...])`：自訂要攔截哪些 `logging` logger（回傳 log_config）
- `integrate_uvicorn(logger, monkeypatch=True)`：顯式啟用 monkeypatch（不需要傳 log_config，但會修改 uvicorn 內部方法）

