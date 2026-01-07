#!/usr/bin/env python3
"""
use_native_format 功能演示

展示如何使用 use_native_format 參數在 pretty-loguru 的 Pretty（預設）格式與原生（接近 loguru）格式之間切換。

Key Features:
- Pretty（預設）格式：自定義名稱顯示，帶 process ID
- Native 格式：接近 loguru 原生的 file:function:line 格式
- 檔案命名差異：Pretty 格式使用時間戳，Native 格式使用簡單命名
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pretty_loguru import create_logger

def demo_format_comparison():
    """比較兩種格式的差異"""
    print("🎨 Pretty Loguru - Native Format 功能演示")
    print("=" * 60)
    
    # 1. Pretty Format (Default)
    print("\n📋 Pretty Format (預設):")
    logger_pretty = create_logger(
        name="pretty_example",
        use_native_format=False,  # 可省略，預設值
        log_dir="logs",
        level="INFO"
    )
    
    # 2. Native Format 
    print("📋 Native Format (原生):")
    logger_native = create_logger(
        name="native_example",
        use_native_format=True,
        log_dir="logs", 
        level="INFO"
    )
    
    print("\n" + "="*50)
    print("🔍 格式差異比較")
    print("="*50)
    
    def log_examples():
        print("\n🔸 Pretty Format 輸出:")
        logger_pretty.info("用戶登入成功")
        logger_pretty.warning("記憶體使用率偏高")
        logger_pretty.error("資料庫連線失敗")
        
        print("\n🔸 Native Format 輸出:")
        logger_native.info("用戶登入成功")
        logger_native.warning("記憶體使用率偏高") 
        logger_native.error("資料庫連線失敗")
    
    log_examples()

def demo_use_cases():
    """展示不同使用情境"""
    print("\n" + "="*50)
    print("💡 使用情境建議")
    print("="*50)
    
    # Use Case 1: Service Applications (Pretty Format)
    print("\n🏢 服務型應用 (建議 Pretty Format):")
    service_logger = create_logger(
        name="user_service",
        use_native_format=False,
        log_dir="logs",
        preset="detailed"
    )
    service_logger.info("服務啟動完成")
    service_logger.info("處理用戶請求", user_id=123, action="login")
    
    # Use Case 2: Development/Debugging (Native Format)
    print("\n🔧 開發調試 (建議 Native Format):")
    debug_logger = create_logger(
        name="debug_session",
        use_native_format=True,
        log_dir="logs",
        level="DEBUG"
    )
    debug_logger.debug("變數檢查", var_name="user_data", value={"id": 123, "name": "Alice"})
    debug_logger.debug("執行流程追蹤")
    
    # Use Case 3: Migration from Loguru (Native Format)
    print("\n🔄 從 Loguru 遷移 (使用 Native Format):")
    migration_logger = create_logger(
        name="legacy_app",
        use_native_format=True,  # 保持與 loguru 一致的格式
        log_dir="logs"
    )
    migration_logger.info("保持原有 loguru 格式體驗")

def demo_file_naming():
    """展示檔案命名差異"""
    print("\n" + "="*50)
    print("📁 檔案命名差異")
    print("="*50)
    
    # Pretty Format - Complex naming
    pretty = create_logger(
        name="file_test_pretty",
        use_native_format=False,
        log_dir="logs",
        preset="detailed"
    )
    pretty.info("Pretty 格式的檔案命名")
    
    # Native Format - Simple naming  
    native = create_logger(
        name="file_test_native",
        use_native_format=True,
        log_dir="logs"
    )
    native.info("Native 格式的檔案命名")
    
    print("\n💡 檔案命名規則:")
    print("  🔸 Pretty: [name]_timestamp.log")
    print("  🔸 Native: name.log")

if __name__ == "__main__":
    demo_format_comparison()
    demo_use_cases()
    demo_file_naming()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("📁 請檢查 logs/ 目錄查看不同格式的日誌檔案")
    print("🔍 注意觀察檔案命名和內容格式的差異")
