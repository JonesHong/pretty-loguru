import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# 建立 logger
from pretty_loguru import create_logger
def main():
    """
    主函數，創建 logger 實例並執行日誌輸出
    """
    logger = create_logger("my_app")
    # Standard methods (output to both console and file)
    logger.block("Title", ["Content1", "Content2"])
    logger.ascii_header("Title")
    logger.figlet_block("Title", ["Content1", "Content2"])

    # Console output only
    logger.console_block("Title", ["Displayed only on console"])
    logger.console_ascii_header("Displayed only on console")
    logger.console_figlet_block("Title", ["Displayed only on console"])

    # File output only
    logger.file_block("Title", ["Logged only to file"])
    logger.file_ascii_header("Logged only to file")
    logger.file_figlet_block("Title", ["Logged only to file"])

if __name__ == "__main__":
    main()