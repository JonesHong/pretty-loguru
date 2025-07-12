#!/usr/bin/env python3
"""
use_native_format 功能演示

展示如何使用 use_native_format 參數在 pretty-loguru 增強格式和原生 loguru 格式之間切換。

Key Features:
- 預設格式：自定義名稱顯示，帶 process ID
- 原生格式：接近 loguru 原生的 file:function:line 格式
- 檔案命名差異：增強格式使用時間戳，原生格式使用簡單命名
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
    
    # 1. Enhanced Format (Default)
    print("\n📋 Enhanced Format (預設):")
    logger_enhanced = create_logger(
        name="enhanced_example",
        use_native_format=False,  # 可省略，預設值
        log_path="logs",
        level="INFO"
    )
    
    # 2. Native Format 
    print("📋 Native Format (原生):")
    logger_native = create_logger(
        name="native_example",
        use_native_format=True,
        log_path="logs", 
        level="INFO"
    )
    
    print("\n" + "="*50)
    print("🔍 格式差異比較")
    print("="*50)
    
    def log_examples():
        print("\n🔸 Enhanced Format 輸出:")
        logger_enhanced.info("用戶登入成功")
        logger_enhanced.warning("記憶體使用率偏高")
        logger_enhanced.error("資料庫連線失敗")
        
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
    
    # Use Case 1: Service Applications (Enhanced Format)
    print("\n🏢 服務型應用 (建議 Enhanced Format):")
    service_logger = create_logger(
        name="user_service",
        use_native_format=False,
        log_path="logs",
        preset="detailed"
    )
    service_logger.info("服務啟動完成")
    service_logger.info("處理用戶請求", user_id=123, action="login")
    
    # Use Case 2: Development/Debugging (Native Format)
    print("\n🔧 開發調試 (建議 Native Format):")
    debug_logger = create_logger(
        name="debug_session",
        use_native_format=True,
        log_path="logs",
        level="DEBUG"
    )
    debug_logger.debug("變數檢查", var_name="user_data", value={"id": 123, "name": "Alice"})
    debug_logger.debug("執行流程追蹤")
    
    # Use Case 3: Migration from Loguru (Native Format)
    print("\n🔄 從 Loguru 遷移 (使用 Native Format):")
    migration_logger = create_logger(
        name="legacy_app",
        use_native_format=True,  # 保持與 loguru 一致的格式
        log_path="logs"
    )
    migration_logger.info("保持原有 loguru 格式體驗")

def demo_file_naming():
    """展示檔案命名差異"""
    print("\n" + "="*50)
    print("📁 檔案命名差異")
    print("="*50)
    
    # Enhanced Format - Complex naming
    enhanced = create_logger(
        name="file_test_enhanced",
        use_native_format=False,
        log_path="logs",
        preset="detailed"
    )
    enhanced.info("Enhanced 格式的檔案命名")
    
    # Native Format - Simple naming  
    native = create_logger(
        name="file_test_native",
        use_native_format=True,
        log_path="logs"
    )
    native.info("Native 格式的檔案命名")
    
    print("\n💡 檔案命名規則:")
    print("  🔸 Enhanced: [name]_timestamp.log")
    print("  🔸 Native: name.log")

if __name__ == "__main__":
    demo_format_comparison()
    demo_use_cases()
    demo_file_naming()
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("📁 請檢查 logs/ 目錄查看不同格式的日誌檔案")
    print("🔍 注意觀察檔案命名和內容格式的差異")