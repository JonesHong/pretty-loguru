import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import uvicorn
from fastapi import FastAPI
from pretty_loguru import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

# 創建一個 logger 實例
logger = create_logger(name="FastAPIApp", log_dir="./test_logs")

# 建立 uvicorn 的 log_config（non-monkeypatch，推薦）
log_config = integrate_uvicorn(logger, log_level="INFO")

app = FastAPI()

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="127.0.0.1", port=8012, log_config=log_config)
