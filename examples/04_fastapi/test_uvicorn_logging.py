import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import uvicorn
from fastapi import FastAPI
from pretty_loguru.factory import create_logger
from pretty_loguru.integrations.uvicorn import integrate_uvicorn

# 創建一個 logger 實例
logger = create_logger(name="FastAPIApp", log_path="./test_logs")

# 將 Uvicorn 與 logger 集成
integrate_uvicorn(logger, level="INFO")

app = FastAPI()

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="127.0.0.1", port=8012)
