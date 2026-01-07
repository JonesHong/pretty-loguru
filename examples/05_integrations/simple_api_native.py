#!/usr/bin/env python3
"""
FastAPI + Native Format - 使用原生格式的 FastAPI 整合

展示在 FastAPI 應用中使用 use_native_format=True 的效果，
適合從 loguru 遷移過來的開發者保持熟悉的格式體驗。

運行方式：
    pip install fastapi uvicorn
    python simple_api_native.py
    
然後訪問：
    http://localhost:8013
    http://localhost:8013/docs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from fastapi import FastAPI, HTTPException
    import uvicorn
except ImportError:
    print("請先安裝依賴：pip install fastapi uvicorn")
    exit(1)

from pretty_loguru import create_logger
from pretty_loguru.integrations.fastapi import integrate_fastapi

# 創建 FastAPI 應用
app = FastAPI(
    title="Pretty Loguru Native Format Demo",
    description="展示使用原生格式的 FastAPI 整合",
    version="1.1.2"
)

# 創建使用原生格式的 logger
logger = create_logger(
    "simple_api_native", 
    use_native_format=True,  # 使用原生 loguru 格式
    log_dir="./logs",
    level="INFO"
)
integrate_fastapi(app, logger)

# 同時創建一個 Pretty（預設）格式的 logger 做比較
pretty_logger = create_logger(
    "simple_api_pretty",
    use_native_format=False,  # Pretty（預設）格式
    log_dir="./logs",
    level="INFO"
)

@app.get("/")
async def root():
    """首頁 - 展示兩種格式差異"""
    # 原生格式日誌
    logger.info("收到首頁請求 (Native Format)")
    # Pretty（預設）格式日誌
    pretty_logger.info("收到首頁請求 (Pretty Format)")
    
    return {
        "message": "Native Format FastAPI Demo",
        "format": "使用 use_native_format=True",
        "note": "查看控制台和日誌檔案觀察格式差異"
    }

@app.get("/format-demo")
async def format_demo():
    """格式演示端點"""
    print("\n=== 格式比較演示 ===")
    
    # Native format 輸出
    print("🔸 Native Format 輸出:")
    logger.info("這是原生格式的訊息")
    logger.warning("原生格式警告訊息")
    
    # Pretty format 輸出
    print("\n🔸 Pretty Format 輸出:")
    pretty_logger.info("這是 Pretty 格式的訊息")
    pretty_logger.warning("Pretty 格式警告訊息")
    
    return {
        "demo": "format_comparison",
        "native_features": [
            "使用 file.name:function:line 格式",
            "包含毫秒時間戳",
            "簡化檔案命名: name.log"
        ],
        "pretty_features": [
            "使用自定義名稱:function:line 格式",
            "包含 process ID",
            "自定義檔案命名: [name]_timestamp.log"
        ]
    }

@app.get("/migration-tips")
async def migration_tips():
    """遷移建議"""
    logger.info("提供從 loguru 遷移的建議")
    
    return {
        "migration_guide": {
            "step1": "使用 use_native_format=True 保持原有格式",
            "step2": "逐步過渡到增強功能",
            "step3": "享受 pretty-loguru 的額外功能"
        },
        "benefits": [
            "保持熟悉的 loguru 格式",
            "無縫遷移體驗", 
            "可隨時切換格式"
        ]
    }

@app.get("/health")
async def health_check():
    """健康檢查 - 使用原生格式記錄"""
    logger.debug("健康檢查請求 (Native Format)")
    return {"status": "healthy", "format": "native"}

def main():
    """啟動應用"""
    print("=== FastAPI + Native Format 範例 ===")
    print("🎯 此範例展示 use_native_format=True 的效果")
    print("📊 同時對比增強格式與原生格式的差異")
    print("啟動服務中...")
    
    uvicorn.run(
        "simple_api_native:app",
        host="127.0.0.1", 
        port=8013,
        reload=False,
        log_level="warning"
    )

if __name__ == "__main__":
    main()
