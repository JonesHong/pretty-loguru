#!/usr/bin/env python3
"""
Hello World - 最簡單的 Pretty-Loguru 使用範例

這是您使用 Pretty-Loguru 的第一個範例。
只需要一行代碼就能開始使用！

運行方式：
    python hello_world.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger

def main():
    """最簡單的使用方式 - 只需要一行代碼！"""
    print("🎯 Pretty-Loguru Hello World")
    print("=" * 40)
    
    # 創建一個最基本的 logger
    logger = create_logger("hello_world")
    
    # 開始使用！
    logger.info("Hello, Pretty-Loguru! 🌟")
    logger.success("恭喜！您已經成功使用 Pretty-Loguru")
    logger.warning("這是一個警告訊息")
    logger.error("這是一個錯誤訊息")
    
    print("\n✅ 完成！您已經學會了最基本的使用方式")
    print("💡 接下來可以學習：")
    print("   - console_logging.py：控制台輸出")
    print("   - file_logging.py：檔案輸出")

if __name__ == "__main__":
    main()