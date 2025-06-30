#!/usr/bin/env python3
"""
Rich 程式碼高亮功能示例

此範例展示了如何使用 pretty-loguru 的程式碼高亮功能，包括：
1. 直接顯示程式碼片段
2. 從文件讀取並顯示程式碼
3. 程式碼差異對比
4. 不同語言和主題的支持
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pretty_loguru import create_logger

def main():
    """主函數 - 展示程式碼高亮功能"""
    
    # 創建 logger
    logger = create_logger(
        name="code_highlight_demo",
        log_path="./logs",
        level="INFO"
    )
    
    logger.info("=== Pretty-Loguru 程式碼高亮功能示例 ===")
    
    # 1. 基本程式碼高亮
    logger.info("\n1. 基本 Python 程式碼高亮")
    
    python_code = '''
def fibonacci(n):
    """計算斐波那契數列的第 n 項"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# 測試函數
for i in range(10):
    print(f"fibonacci({i}) = {fibonacci(i)}")
'''
    
    logger.code(
        code=python_code,
        language="python",
        title="斐波那契數列範例",
        theme="monokai"
    )
    
    # 2. JavaScript 程式碼高亮
    logger.info("\n2. JavaScript 程式碼高亮")
    
    js_code = '''
// 異步函數範例
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        
        return {
            success: true,
            data: userData
        };
    } catch (error) {
        console.error('獲取用戶數據失敗:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// 使用函數
fetchUserData(123).then(result => {
    if (result.success) {
        console.log('用戶數據:', result.data);
    }
});
'''
    
    logger.code(
        code=js_code,
        language="javascript",
        title="JavaScript 異步處理範例",
        theme="github-dark"
    )
    
    # 3. SQL 程式碼高亮
    logger.info("\n3. SQL 程式碼高亮")
    
    sql_code = '''
-- 查詢用戶訂單統計
SELECT 
    u.user_id,
    u.username,
    u.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE u.created_at >= '2023-01-01'
    AND u.status = 'active'
GROUP BY u.user_id, u.username, u.email
HAVING COUNT(o.order_id) > 0
ORDER BY total_spent DESC
LIMIT 100;
'''
    
    logger.code(
        code=sql_code,
        language="sql",
        title="用戶訂單統計查詢",
        theme="one-dark",
        line_numbers=True
    )
    
    # 4. JSON 配置檔高亮
    logger.info("\n4. JSON 配置檔高亮")
    
    json_code = '''
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "my_app_db",
    "username": "app_user",
    "pool": {
      "min": 5,
      "max": 20,
      "timeout": 30000
    }
  },
  "cache": {
    "provider": "redis",
    "host": "redis.example.com",
    "port": 6379,
    "ttl": 3600
  },
  "logging": {
    "level": "info",
    "format": "json",
    "outputs": ["console", "file"]
  }
}
'''
    
    logger.code(
        code=json_code,
        language="json",
        title="應用程式配置檔",
        theme="material"
    )
    
    # 5. 程式碼差異對比
    logger.info("\n5. 程式碼差異對比")
    
    old_function = '''
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
'''
    
    new_function = '''
def process_data(data):
    """處理數據，對正數進行雙倍處理並過濾負數"""
    return [item * 2 for item in data if item > 0]
'''
    
    logger.diff(
        old_code=old_function,
        new_code=new_function,
        old_title="重構前",
        new_title="重構後",
        language="python"
    )
    
    # 6. 從當前文件讀取程式碼片段
    logger.info("\n6. 從文件讀取程式碼片段")
    
    current_file = __file__
    logger.code_file(
        file_path=current_file,
        start_line=1,
        end_line=15,
        title=f"當前文件開頭部分: {os.path.basename(current_file)}"
    )
    
    # 7. 不同主題對比
    logger.info("\n7. 不同主題對比")
    
    sample_code = '''
class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.processed_count = 0
    
    def process(self, data):
        # 處理邏輯
        self.processed_count += 1
        return f"Processed: {data}"
'''
    
    themes = ["monokai", "github-dark", "one-dark", "material"]
    for theme in themes:
        logger.info(f"\n主題: {theme}")
        logger.code(
            code=sample_code,
            language="python",
            title=f"DataProcessor 類別 ({theme} 主題)",
            theme=theme,
            to_console_only=True  # 只在控制台顯示，避免日誌文件過於冗長
        )
    
    # 8. HTML 程式碼範例
    logger.info("\n8. HTML 程式碼高亮")
    
    html_code = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pretty Loguru Demo</title>
    <style>
        .highlight {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>歡迎使用 Pretty Loguru</h1>
    <div class="highlight">
        <p>這是一個程式碼高亮示例</p>
    </div>
    <script>
        console.log("頁面載入完成");
    </script>
</body>
</html>
'''
    
    logger.code(
        code=html_code,
        language="html",
        title="HTML 頁面範例",
        theme="github-dark"
    )
    
    logger.success("程式碼高亮功能示例完成！")
    
    # 9. 測試目標輸出功能
    logger.info("\n9. 測試目標輸出功能")
    
    test_code = '''
def hello_world():
    print("Hello, World!")
    return "success"
'''
    
    # 只輸出到控制台
    logger.info("只輸出到控制台:")
    logger.code(
        code=test_code,
        title="控制台專用",
        to_console_only=True
    )
    
    # 只輸出到文件
    logger.info("只輸出到文件 (查看日誌文件):")
    logger.code(
        code=test_code,
        title="文件專用",
        to_log_file_only=True
    )
    
    logger.info("所有程式碼高亮功能測試完成！")

if __name__ == "__main__":
    main()
    