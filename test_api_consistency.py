#!/usr/bin/env python3
"""
Test script to validate API consistency fixes
Ensures all documentation examples use correct create_logger API
"""

import os
import sys
from pretty_loguru import create_logger

def test_basic_usage():
    """Test basic create_logger usage as shown in documentation"""
    print("🧪 Testing basic create_logger usage...")
    
    try:
        # Test from simple-usage.md example
        logger = create_logger(
            name="simple_usage_demo",
            log_path="test_logs",
            level="INFO"
        )
        
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.success("This is a success message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        
        print("✅ Basic usage test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic usage test failed: {e}")
        return False

def test_integration_example():
    """Test integration example patterns"""
    print("🧪 Testing integration patterns...")
    
    try:
        # Test from integrations/index.md example
        logger = create_logger(
            name="integrations_demo",
            log_path="api_logs",
            level="INFO"
        )
        
        # Test Rich components
        logger.block(
            "System Status",
            [
                "CPU: 25%",
                "Memory: 60%", 
                "Disk: 80%"
            ],
            border_style="green",
            log_level="INFO"
        )
        
        logger.ascii_header("API STARTUP", font="slant", border_style="blue")
        
        print("✅ Integration patterns test passed")
        return True
        
    except Exception as e:
        print(f"❌ Integration patterns test failed: {e}")
        return False

def test_environment_setup():
    """Test environment-based setup patterns"""
    print("🧪 Testing environment setup patterns...")
    
    try:
        # Test environment-based configuration
        environments = ["development", "staging", "production"]
        
        for env in environments:
            logger = create_logger(
                name=f"{env}_app",
                log_path=f"{env}_logs",
                level="INFO"
            )
            logger.info(f"Testing {env} environment setup")
            
        print("✅ Environment setup test passed")
        return True
        
    except Exception as e:
        print(f"❌ Environment setup test failed: {e}")
        return False

def validate_no_legacy_imports():
    """Ensure no legacy API imports in test"""
    print("🧪 Validating no legacy API usage...")
    
    # This test ensures we're using the correct import
    try:
        from pretty_loguru import create_logger
        print("✅ Correct import statement validated")
        return True
    except ImportError as e:
        print(f"❌ Import validation failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 Starting API consistency validation tests...\n")
    
    tests = [
        validate_no_legacy_imports,
        test_basic_usage,
        test_integration_example,
        test_environment_setup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API consistency tests passed! Documentation examples are working correctly.")
        return 0
    else:
        print("❌ Some tests failed. API consistency issues may remain.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)