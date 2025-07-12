#!/usr/bin/env python3
"""
全面測試所有改動
"""

import sys
import traceback
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from pretty_loguru import (
    create_logger, LoggerConfig, ConfigTemplates, 
    cleanup_loggers, list_loggers, get_logger
)

def test_basic_functionality():
    """測試基本功能"""
    print("\n🧪 測試 1: 基本功能")
    print("-" * 50)
    
    try:
        # 創建基本 logger
        logger = create_logger("test_basic", level="INFO")
        logger.info("基本功能測試 - INFO 訊息")
        logger.debug("這個不應該顯示 - DEBUG 訊息")
        print("✅ 基本 logger 創建成功")
        
        # 使用 LoggerConfig
        config = LoggerConfig(level="DEBUG", log_path="logs/test")
        logger2 = create_logger("test_config", config=config)
        logger2.debug("使用 LoggerConfig - DEBUG 訊息")
        print("✅ LoggerConfig 功能正常")
        
        # 測試 apply_to 只更新現有 logger
        try:
            config.apply_to("non_existent")
            print("❌ apply_to 應該拋出錯誤")
        except ValueError as e:
            print(f"✅ apply_to 正確拋出錯誤: {str(e)[:50]}...")
            
        # 更新現有 logger
        new_config = LoggerConfig(level="WARNING")
        updated = new_config.apply_to("test_basic")
        print(f"✅ 成功更新現有 logger (是新實例: {logger is not updated})")
        
        return True
    except Exception as e:
        print(f"❌ 基本功能測試失敗: {e}")
        traceback.print_exc()
        return False

def test_production_config():
    """測試 production 配置的跨平台路徑"""
    print("\n🧪 測試 2: Production 配置跨平台路徑")
    print("-" * 50)
    
    try:
        import platform
        prod_config = ConfigTemplates.production()
        print(f"系統: {platform.system()}")
        print(f"Production 路徑: {prod_config.log_path}")
        
        # 確認不是硬編碼的 /var/log
        if prod_config.log_path == "/var/log/app":
            print("❌ 仍然使用硬編碼的 /var/log 路徑")
            return False
        
        # 確認路徑包含用戶目錄
        if "~" not in str(prod_config.log_path) and not Path(prod_config.log_path).is_absolute():
            print("❌ 路徑似乎不是用戶特定的")
            return False
            
        print("✅ Production 配置使用用戶特定路徑")
        return True
    except Exception as e:
        print(f"❌ Production 配置測試失敗: {e}")
        traceback.print_exc()
        return False

def test_cleanup_functionality():
    """測試清理功能"""
    print("\n🧪 測試 3: Registry 清理功能")
    print("-" * 50)
    
    try:
        # 清理之前的 logger
        cleanup_loggers()
        
        initial_count = len(list_loggers())
        print(f"初始 logger 數量: {initial_count}")
        
        # 創建多個 logger
        for i in range(3):
            create_logger(f"cleanup_test_{i}")
        
        after_create = len(list_loggers())
        print(f"創建 3 個 logger 後: {after_create}")
        
        if after_create != initial_count + 3:
            print("❌ Logger 數量不正確")
            return False
        
        # 清理
        cleaned = cleanup_loggers()
        final_count = len(list_loggers())
        
        print(f"清理了 {cleaned} 個 logger")
        print(f"最終 logger 數量: {final_count}")
        
        if final_count != 0:
            print("❌ 清理不完全")
            return False
            
        print("✅ 清理功能正常")
        return True
    except Exception as e:
        print(f"❌ 清理功能測試失敗: {e}")
        traceback.print_exc()
        return False

def test_visual_features():
    """測試視覺功能"""
    print("\n🧪 測試 4: 視覺功能")
    print("-" * 50)
    
    try:
        logger = create_logger("visual_test", level="INFO")
        
        # 測試 block
        logger.block("測試區塊", "這是區塊內容", border_style="green")
        print("✅ Block 功能正常")
        
        # 測試 ASCII art
        logger.ascii_header("TEST", font="slant")
        print("✅ ASCII header 功能正常")
        
        # 測試 ASCII block
        logger.ascii_block("標題", ["內容"], ascii_header="BLOCK")
        print("✅ ASCII block 功能正常")
        
        return True
    except Exception as e:
        print(f"❌ 視覺功能測試失敗: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """執行所有測試"""
    print("=" * 60)
    print("🚀 開始執行所有測試")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_production_config,
        test_cleanup_functionality,
        test_visual_features
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 測試崩潰: {e}")
            results.append(False)
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試總結")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通過: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有測試通過！")
        return True
    else:
        print("❌ 有測試失敗")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)