# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# # 建立 logger
# from pretty_loguru import create_logger
# def main():
#     """
#     主函數，創建 logger 實例並執行日誌輸出
#     """
#     logger = create_logger("my_app")
#     # Standard methods (output to both console and file)
#     logger.block("Title", ["Content1", "Content2"])
#     logger.ascii_header("Title")
#     logger.figlet_block("Title", ["Content1", "Content2"])

#     # Console output only
#     logger.console_block("Title", ["Displayed only on console"])
#     logger.console_ascii_header("Displayed only on console")
#     logger.console_figlet_block("Title", ["Displayed only on console"])

#     # File output only
#     logger.file_block("Title", ["Logged only to file"])
#     logger.file_ascii_header("Logged only to file")
#     logger.file_figlet_block("Title", ["Logged only to file"])

# if __name__ == "__main__":
#     main()

from pathlib import Path
import sys
from fastapi import FastAPI

lib_path = Path(__file__).resolve().parents[1] 
sys.path.insert(0, str(lib_path))
print(f"Adding {lib_path} to sys.path")


from pretty_loguru import configure_uvicorn, create_logger
from pretty_loguru.core.presets import PresetType
from pretty_loguru.integrations.fastapi import setup_fastapi_logging


app = FastAPI()
logger = create_logger(
    service_tag="fastapi_app",
    level="DEBUG",  # 添加這行
    log_name_preset=PresetType.DAILY,
    # log_file_settings={
    #     "serialize": True,
    #     "rotation": "10 KB",
    # }
    )
setup_fastapi_logging(app, logger_instance=logger)

@app.get("/")
def read_root():
   logger.info("處理首頁請求")
   return {"Hello": "World"}

if __name__ == "__main__":
   import uvicorn
   # 先設定好 Loguru 攔截
   configure_uvicorn(logger_instance=logger)
   uvicorn.run(
      app,
      host="localhost",
      port=8000,
      log_config=None,  # 禁用 uvicorn 的日誌配置
   )