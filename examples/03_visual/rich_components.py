#!/usr/bin/env python3
"""
Rich Components Demo - Rich 組件展示

這個範例展示：
1. 表格 (Tables)
2. 樹狀圖 (Trees)
3. 多欄位顯示 (Columns)
4. 進度條 (Progress)

運行方式：
    python rich_components.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time

def tables_demo():
    """表格展示"""
    logger = create_logger("tables_demo", log_dir="./logs")
    
    print("=== Rich 表格展示 ===\n")
    
    logger.info("展示用戶統計表格")
    
    # 1. 用戶統計表格
    user_data = [
        {"姓名": "Alice", "Email": "alice@example.com", "角色": "Admin", "註冊日期": "2024-01-15", "狀態": "活躍"},
        {"姓名": "Bob", "Email": "bob@example.com", "角色": "User", "註冊日期": "2024-02-20", "狀態": "活躍"},  
        {"姓名": "Charlie", "Email": "charlie@example.com", "角色": "User", "註冊日期": "2024-03-10", "狀態": "停用"},
        {"姓名": "Diana", "Email": "diana@example.com", "角色": "Moderator", "註冊日期": "2024-03-25", "狀態": "活躍"}
    ]
    
    logger.table(
        title="📊 用戶統計",
        data=user_data
    )
    
    # 2. 系統資源表格
    logger.info("展示系統資源使用表格")
    
    resource_data = [
        {"組件": "CPU", "規格": "Intel i7-8565U", "使用率": "45%", "狀態": "正常"},
        {"組件": "記憶體", "規格": "16GB DDR4", "使用率": "68%", "狀態": "正常"},
        {"組件": "磁碟", "規格": "512GB SSD", "使用率": "78%", "狀態": "警告"},
        {"組件": "網路", "規格": "1Gbps", "使用率": "23%", "狀態": "正常"}
    ]
    
    logger.table(
        title="🖥️ 系統資源",
        data=resource_data
    )

def trees_demo():
    """樹狀圖展示"""
    logger = create_logger("trees_demo", log_dir="./logs")
    
    print("\n=== Rich 樹狀圖展示 ===\n")
    
    logger.info("展示專案目錄結構")
    
    # 專案目錄結構
    project_tree = {
        "MyWebApp/": {
            "src/": {
                "components/": {
                    "Header.jsx": None,
                    "Footer.jsx": None,
                    "UserList.jsx": None
                },
                "utils/": {
                    "api.js": None,
                    "helpers.js": None
                },
                "App.jsx": None,
                "index.js": None
            },
            "public/": {
                "index.html": None,
                "favicon.ico": None
            },
            "tests/": {
                "unit/": {
                    "components.test.js": None
                },
                "integration/": {
                    "api.test.js": None
                }
            },
            "package.json": None,
            "README.md": None
        }
    }
    
    logger.tree("📁 專案結構", project_tree)
    
    # 組織架構
    logger.info("展示公司組織架構")
    
    org_tree = {
        "公司": {
            "技術部": {
                "前端組": {
                    "React 開發者": None,
                    "Vue 開發者": None
                },
                "後端組": {
                    "Python 開發者": None, 
                    "Java 開發者": None
                },
                "DevOps 組": {
                    "系統管理員": None,
                    "監控專員": None
                }
            },
            "產品部": {
                "產品經理": None,
                "UI/UX 設計師": None
            }
        }
    }
    
    logger.tree("🏢 組織架構", org_tree)

def columns_demo():
    """多欄位展示"""
    logger = create_logger("columns_demo", log_dir="./logs")
    
    print("\n=== Rich 多欄位展示 ===\n")
    
    logger.info("展示服務狀態多欄位顯示")
    
    # 服務狀態多欄位
    web_services = [
        "🟢 API Gateway: 正常",
        "🟢 Auth Service: 正常", 
        "🟢 User Service: 正常",
        "🟡 Payment Service: 警告",
        "🔴 Email Service: 異常"
    ]
    
    databases = [
        "🟢 主資料庫: 正常",
        "🟢 Redis 快取: 正常",
        "🟢 日誌資料庫: 正常", 
        "🟡 備份資料庫: 同步中",
        "🟢 搜尋引擎: 正常"
    ]
    
    infrastructure = [
        "🟢 Load Balancer: 正常",
        "🟢 CDN: 正常",
        "🟢 監控系統: 正常",
        "🟢 安全防護: 正常",
        "🟡 備份系統: 執行中"
    ]
    
    # 使用 columns 方法展示 Web 服務
    logger.columns(
        title="🌐 Web 服務狀態",
        items=web_services
    )
    
    # 展示資料庫狀態
    logger.columns(
        title="🗄️ 資料庫狀態",
        items=databases
    )
    
    # 展示基礎設施狀態
    logger.columns(
        title="🏗️ 基礎設施狀態",
        items=infrastructure
    )

def progress_demo():
    """進度條展示"""
    logger = create_logger("progress_demo", log_dir="./logs")
    
    print("\n=== Rich 進度條展示 ===\n")
    
    logger.info("展示資料處理進度")
    
    # 模擬資料處理流程
    tasks = [
        ("讀取原始資料", 100),
        ("資料清理", 80),
        ("資料轉換", 60), 
        ("資料驗證", 40),
        ("寫入資料庫", 20)
    ]
    
    # 使用 progress 屬性進行進度追蹤
    for task_name, total in tasks:
        logger.info(f"開始 {task_name}")
        
        # 使用 track_list 進行進度追蹤
        items = list(range(total))
        tracked_items = logger.progress.track_list(items, f"{task_name}")
        
        for i in tracked_items:
            time.sleep(0.01)  # 模擬處理時間
        
        logger.success(f"{task_name} 完成")
    
    logger.success("所有資料處理任務完成!")

def real_world_dashboard():
    """真實儀表板範例"""
    logger = create_logger("dashboard", log_dir="./logs")
    
    print("\n=== 真實監控儀表板 ===\n")
    
    # 1. 系統概覽標題
    logger.ascii_header("DASHBOARD", font="slant", border_style="blue")
    
    # 2. 關鍵指標表格
    metrics_data = [
        {"指標": "日活躍用戶", "當前值": "12,847", "變化": "+5.2%", "狀態": "🟢"},
        {"指標": "每秒請求數", "當前值": "289", "變化": "+12.1%", "狀態": "🟢"},
        {"指標": "平均響應時間", "當前值": "245ms", "變化": "-8.3%", "狀態": "🟢"},
        {"指標": "錯誤率", "當前值": "0.02%", "變化": "+0.01%", "狀態": "🟡"},
        {"指標": "系統負載", "當前值": "2.1", "變化": "+15.2%", "狀態": "🟡"}
    ]
    
    logger.table(
        title="📊 關鍵性能指標 (KPI)",
        data=metrics_data
    )
    
    # 3. 服務健康狀態
    api_status = [
        "🟢 GET /api/users",
        "🟢 POST /api/auth", 
        "🟢 GET /api/orders",
        "🟡 POST /api/payment",
        "🔴 GET /api/reports"
    ]
    
    db_status = [
        "🟢 主資料庫連接",
        "🟢 讀取副本",
        "🟢 Redis 快取",
        "🟡 備份任務",
        "🟢 搜尋索引"
    ]
    
    infra_status = [
        "🟢 負載均衡器",
        "🟢 Auto Scaling",
        "🟢 CDN 分發",
        "🟢 SSL 憑證",
        "🟡 備份恢復"
    ]
    
    # 展示 API 端點狀態
    logger.columns(
        title="🔗 API 端點狀態",
        items=api_status
    )
    
    # 展示資料庫狀態 
    logger.columns(
        title="🗄️ 資料庫狀態",
        items=db_status
    )
    
    # 展示基礎設施狀態
    logger.columns(
        title="🏗️ 基礎設施狀態",
        items=infra_status
    )
    
    # 4. 資源使用樹狀圖
    resource_tree = {
        "系統資源": {
            "計算資源": {
                "CPU 使用率: 65%": None,
                "記憶體使用: 4.2GB/8GB": None,
                "活躍連接: 1,247": None
            },
            "儲存資源": {
                "磁碟使用: 78%": None,
                "資料庫大小: 12.5GB": None,
                "日誌大小: 2.1GB": None
            },
            "網路資源": {
                "帶寬使用: 45%": None,
                "延遲: 23ms": None,
                "封包遺失: 0.01%": None
            }
        }
    }
    
    logger.tree("🖥️ 資源使用詳情", resource_tree)

def main():
    """主函數"""
    print("=== Pretty Loguru Rich 組件完整演示 ===")
    
    # 1. 表格展示
    tables_demo()
    
    # 2. 樹狀圖展示
    trees_demo()
    
    # 3. 多欄位展示
    columns_demo()
    
    # 4. 進度條展示
    progress_demo()
    
    # 5. 真實儀表板
    real_world_dashboard()
    
    print("\n" + "="*50)
    print("Rich 組件演示完成!")
    print("查看 ./logs/ 目錄中的日誌檔案")
    print("Rich 組件讓數據展示更加直觀美觀!")

if __name__ == "__main__":
    main()