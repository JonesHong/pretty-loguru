#!/usr/bin/env python3
"""
Formatting Basics - 格式化基礎

學習 Pretty-Loguru 的格式化功能，包括變數格式化、
結構化日誌和自定義格式。

運行方式：
    python formatting_basics.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import json
from datetime import datetime

def basic_formatting():
    """基本格式化"""
    print("📝 基本格式化")
    print("-" * 30)
    
    logger = create_logger("formatting_basic", log_path="./logs/basics")
    
    # 1. 字符串格式化
    user_name = "張三"
    user_age = 25
    logger.info(f"用戶資訊：姓名={user_name}, 年齡={user_age}")
    
    # 2. 百分比格式化
    logger.info("用戶資訊：姓名=%s, 年齡=%d" % (user_name, user_age))
    
    # 3. format 方法
    logger.info("用戶資訊：姓名={}, 年齡={}".format(user_name, user_age))
    
    # 4. 命名格式化
    logger.info("用戶資訊：姓名={name}, 年齡={age}".format(name=user_name, age=user_age))

def structured_logging():
    """結構化日誌"""
    print("\n🏗️ 結構化日誌")
    print("-" * 30)
    
    logger = create_logger("structured", log_path="./logs/basics")
    
    # 1. 字典格式化
    user_data = {
        "id": 12345,
        "name": "李四",
        "email": "lisi@example.com",
        "role": "admin",
        "last_login": datetime.now().isoformat()
    }
    
    logger.info(f"用戶登入：{json.dumps(user_data, ensure_ascii=False, indent=2)}")
    
    # 2. 事件記錄
    event = {
        "event_type": "user_action",
        "action": "file_upload",
        "user_id": 12345,
        "file_name": "document.pdf",
        "file_size": 1024000,
        "timestamp": datetime.now().isoformat(),
        "success": True
    }
    
    logger.success(f"事件記錄：{json.dumps(event, ensure_ascii=False)}")
    
    # 3. 錯誤上下文
    error_context = {
        "error_type": "ValidationError",
        "field": "email",
        "value": "invalid-email",
        "expected": "valid email format",
        "user_input": "not-an-email"
    }
    
    logger.error(f"驗證錯誤：{json.dumps(error_context, ensure_ascii=False)}")

def performance_logging():
    """性能相關日誌"""
    print("\n⚡ 性能相關日誌")
    print("-" * 30)
    
    logger = create_logger("performance", log_path="./logs/basics")
    
    # 1. 執行時間記錄
    import time
    start_time = time.time()
    
    # 模擬一些處理
    time.sleep(0.1)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    logger.info(f"操作執行時間：{execution_time:.3f} 秒")
    
    # 2. 資源使用記錄
    import os
    import psutil
    
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    performance_data = {
        "cpu_percent": process.cpu_percent(),
        "memory_rss": memory_info.rss,
        "memory_vms": memory_info.vms,
        "memory_percent": process.memory_percent()
    }
    
    logger.info(f"資源使用：{json.dumps(performance_data, ensure_ascii=False)}")
    
    # 3. 請求響應記錄
    request_data = {
        "method": "POST",
        "url": "/api/users",
        "status_code": 201,
        "response_time_ms": 45,
        "content_length": 256
    }
    
    logger.success(f"API 請求：{json.dumps(request_data, ensure_ascii=False)}")

def error_formatting():
    """錯誤格式化"""
    print("\n🚨 錯誤格式化")
    print("-" * 30)
    
    logger = create_logger("error_format", log_path="./logs/basics")
    
    def process_data(data):
        """模擬數據處理函數"""
        try:
            result = data["value"] / data["divisor"]
            return result
        except KeyError as e:
            # 格式化 KeyError
            error_info = {
                "error_type": "KeyError",
                "missing_key": str(e),
                "available_keys": list(data.keys()),
                "expected_keys": ["value", "divisor"]
            }
            logger.error(f"鍵值錯誤：{json.dumps(error_info, ensure_ascii=False)}")
            raise
        except ZeroDivisionError as e:
            # 格式化 ZeroDivisionError
            error_info = {
                "error_type": "ZeroDivisionError", 
                "operation": "division",
                "dividend": data.get("value"),
                "divisor": data.get("divisor")
            }
            logger.error(f"除零錯誤：{json.dumps(error_info, ensure_ascii=False)}")
            raise
    
    # 測試不同的錯誤情況
    test_cases = [
        {"value": 10, "divisor": 2},  # 正常情況
        {"value": 10},  # 缺少 divisor
        {"value": 10, "divisor": 0},  # 除零錯誤
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        try:
            result = process_data(test_data)
            logger.success(f"測試 {i} 成功：結果 = {result}")
        except Exception as e:
            logger.warning(f"測試 {i} 失敗：{type(e).__name__}")

def multiline_formatting():
    """多行格式化"""
    print("\n📄 多行格式化")
    print("-" * 30)
    
    logger = create_logger("multiline", log_path="./logs/basics")
    
    # 1. 多行字符串
    config_info = """
    數據庫配置：
    - 主機：localhost
    - 端口：5432
    - 數據庫：myapp
    - 用戶：admin
    """
    logger.info(f"配置信息：{config_info}")
    
    # 2. 列表格式化
    processing_steps = [
        "1. 驗證輸入數據",
        "2. 連接數據庫",
        "3. 執行查詢",
        "4. 處理結果",
        "5. 返回響應"
    ]
    
    steps_text = "\n".join(processing_steps)
    logger.info(f"處理步驟：\n{steps_text}")
    
    # 3. 表格式數據
    users = [
        {"id": 1, "name": "張三", "role": "admin"},
        {"id": 2, "name": "李四", "role": "user"},
        {"id": 3, "name": "王五", "role": "moderator"}
    ]
    
    table_text = "用戶列表：\n"
    table_text += "ID | 姓名 | 角色\n"
    table_text += "-" * 20 + "\n"
    for user in users:
        table_text += f"{user['id']:2} | {user['name']:4} | {user['role']}\n"
    
    logger.info(table_text)

def custom_formatting_functions():
    """自定義格式化函數"""
    print("\n🎨 自定義格式化函數")
    print("-" * 30)
    
    logger = create_logger("custom_format", log_path="./logs/basics")
    
    def format_bytes(bytes_value):
        """格式化位元組大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"
    
    def format_duration(seconds):
        """格式化持續時間"""
        if seconds < 60:
            return f"{seconds:.2f} 秒"
        elif seconds < 3600:
            return f"{seconds/60:.2f} 分鐘"
        else:
            return f"{seconds/3600:.2f} 小時"
    
    # 使用自定義格式化函數
    file_size = 1024 * 1024 * 2.5  # 2.5 MB
    process_time = 156.78  # 秒
    
    logger.info(f"文件處理完成：大小 {format_bytes(file_size)}, 耗時 {format_duration(process_time)}")
    
    # 複雜格式化示例
    operation_result = {
        "operation": "file_processing",
        "file_count": 25,
        "total_size": format_bytes(file_size * 25),
        "total_time": format_duration(process_time * 25),
        "average_time": format_duration(process_time),
        "success_rate": "96.0%"
    }
    
    logger.success(f"批次處理結果：{json.dumps(operation_result, ensure_ascii=False, indent=2)}")

def main():
    """主函數"""
    print("🎯 Pretty-Loguru 格式化基礎範例")
    print("=" * 50)
    
    # 1. 基本格式化
    basic_formatting()
    
    # 2. 結構化日誌
    structured_logging()
    
    # 3. 性能相關日誌
    performance_logging()
    
    # 4. 錯誤格式化
    error_formatting()
    
    # 5. 多行格式化
    multiline_formatting()
    
    # 6. 自定義格式化函數
    custom_formatting_functions()
    
    print("\n" + "=" * 50)
    print("✅ 格式化基礎範例完成！")
    print("💡 格式化最佳實踐：")
    print("   - 使用 f-string 進行基本格式化")
    print("   - 結構化數據使用 JSON 格式")
    print("   - 自定義格式化函數提高可讀性")
    print("   - 多行文本保持良好的縮進")

if __name__ == "__main__":
    main()