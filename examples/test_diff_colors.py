#!/usr/bin/env python3
"""
測試改進後的 diff 功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pretty_loguru import create_logger

def main():
    """測試 diff 功能的顏色區分"""
    
    # 創建 logger
    logger = create_logger(
        name="diff_test",
        level="INFO",
        use_rich_components=True
    )
    
    logger.info("=== 測試改進後的程式碼差異顯示 ===")
    
    # 測試 1: Python 函數重構
    logger.info("\n1. Python 函數重構範例")
    
    old_python = '''def calculate_total(items):
    total = 0
    for item in items:
        if item['active']:
            total += item['price']
    return total'''
    
    new_python = '''def calculate_total(items):
    """計算有效項目的總價格"""
    return sum(
        item['price'] 
        for item in items 
        if item.get('active', False)
    )'''
    
    logger.diff(
        old_code=old_python,
        new_code=new_python,
        old_title="重構前",
        new_title="重構後",
        language="python"
    )
    
    # 測試 2: JavaScript 功能改進
    logger.info("\n2. JavaScript 功能改進範例")
    
    old_js = '''function fetchData(url) {
    return fetch(url)
        .then(response => response.json())
        .catch(error => {
            console.log(error);
            return null;
        });
}'''
    
    new_js = '''async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch data:', error);
        throw error;
    }
}'''
    
    logger.diff(
        old_code=old_js,
        new_code=new_js,
        old_title="Promise 版本",
        new_title="Async/Await 版本",
        language="javascript"
    )
    
    # 測試 3: SQL 查詢優化
    logger.info("\n3. SQL 查詢優化範例")
    
    old_sql = '''SELECT u.*, o.*
FROM users u, orders o
WHERE u.id = o.user_id
AND u.status = 'active';'''
    
    new_sql = '''SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id, u.name, u.email
ORDER BY total_amount DESC;'''
    
    logger.diff(
        old_code=old_sql,
        new_code=new_sql,
        old_title="原始查詢",
        new_title="優化查詢",
        language="sql"
    )
    
    # 測試 4: 配置檔更新
    logger.info("\n4. 配置檔更新範例")
    
    old_config = '''{
  "database": {
    "host": "localhost",
    "port": 5432
  },
  "cache": false
}'''
    
    new_config = '''{
  "database": {
    "host": "localhost",
    "port": 5432,
    "pool_size": 10,
    "timeout": 30
  },
  "cache": {
    "enabled": true,
    "provider": "redis",
    "ttl": 3600
  },
  "logging": {
    "level": "info",
    "format": "json"
  }
}'''
    
    logger.diff(
        old_code=old_config,
        new_code=new_config,
        old_title="舊配置",
        new_title="新配置",
        language="json"
    )
    
    logger.success("程式碼差異顯示測試完成！")

if __name__ == "__main__":
    main()