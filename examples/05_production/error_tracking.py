#!/usr/bin/env python3
"""
Error Tracking - 錯誤追蹤和處理

這個範例展示：
1. 結構化錯誤記錄
2. 錯誤分類和嚴重程度
3. 錯誤恢復和重試機制
4. 錯誤分析和報告

運行方式：
    python error_tracking.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
import json
import traceback
import random
from datetime import datetime
from typing import Dict, Any, Optional

class ErrorTracker:
    """錯誤追蹤器"""
    
    def __init__(self):
        self.logger = create_logger("error_tracker",
                                   log_path="./logs/errors",
                                   preset="daily",
                                   retention="90 days")
        self.error_counts = {}
        self.error_history = []
    
    def log_error(self, error_type: str, error_msg: str, 
                  context: Dict[str, Any] = None,
                  severity: str = "error",
                  user_id: str = None,
                  request_id: str = None):
        """記錄錯誤"""
        
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "message": error_msg,
            "severity": severity,
            "user_id": user_id,
            "request_id": request_id,
            "context": context or {}
        }
        
        # 更新錯誤計數
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        self.error_history.append(error_data)
        
        # 格式化錯誤信息
        error_json = json.dumps(error_data, ensure_ascii=False, indent=2)
        
        # 根據嚴重程度記錄
        if severity == "critical":
            self.logger.error(f"🚨 嚴重錯誤: {error_type} - {error_json}")
        elif severity == "error":
            self.logger.error(f"❌ 錯誤: {error_type} - {error_json}")
        elif severity == "warning":
            self.logger.warning(f"⚠️ 警告: {error_type} - {error_json}")
        else:
            self.logger.info(f"ℹ️ 信息: {error_type} - {error_json}")
    
    def get_error_summary(self):
        """獲取錯誤摘要"""
        return {
            "total_errors": len(self.error_history),
            "error_types": len(self.error_counts),
            "top_errors": sorted(self.error_counts.items(), 
                               key=lambda x: x[1], reverse=True)[:5]
        }

def database_error_simulation():
    """資料庫錯誤模擬"""
    print("=== 資料庫錯誤追蹤 ===\n")
    
    tracker = ErrorTracker()
    
    tracker.logger.ascii_header("DB ERRORS", font="slant", border_style="red")
    
    # 模擬不同類型的資料庫錯誤
    db_errors = [
        {
            "type": "ConnectionTimeout",
            "message": "資料庫連接超時",
            "context": {"timeout": 30, "host": "db.example.com", "port": 5432},
            "severity": "error"
        },
        {
            "type": "QuerySyntaxError", 
            "message": "SQL 語法錯誤",
            "context": {"query": "SELECT * FROM user WHERE", "line": 1},
            "severity": "error"
        },
        {
            "type": "DuplicateKeyError",
            "message": "主鍵重複",
            "context": {"table": "users", "key": "email", "value": "test@example.com"},
            "severity": "warning"
        },
        {
            "type": "ConnectionPoolExhausted",
            "message": "連接池耗盡",
            "context": {"max_connections": 50, "active_connections": 50},
            "severity": "critical"
        },
        {
            "type": "SlowQuery",
            "message": "慢查詢檢測",
            "context": {"execution_time": 5.2, "threshold": 1.0, "table": "orders"},
            "severity": "warning"
        }
    ]
    
    tracker.logger.console_info("🗄️ 模擬資料庫錯誤...")
    
    for i, error in enumerate(db_errors):
        tracker.logger.console_info(f"📝 記錄錯誤 {i+1}: {error['type']}")
        
        tracker.log_error(
            error_type=error["type"],
            error_msg=error["message"], 
            context=error["context"],
            severity=error["severity"],
            user_id=f"user_{random.randint(100, 999)}",
            request_id=f"req_{random.randint(10000, 99999)}"
        )
        
        time.sleep(0.5)
    
    # 錯誤摘要
    summary = tracker.get_error_summary()
    tracker.logger.console_info(f"📊 記錄了 {summary['total_errors']} 個錯誤")
    
    return tracker

def api_error_simulation():
    """API 錯誤模擬"""
    print("\n=== API 錯誤追蹤 ===\n")
    
    tracker = ErrorTracker()
    
    tracker.logger.ascii_header("API ERRORS", font="slant", border_style="yellow")
    
    # 模擬 API 錯誤場景
    api_scenarios = [
        {
            "endpoint": "/api/users",
            "method": "GET", 
            "status_code": 500,
            "error": "InternalServerError",
            "message": "內部伺服器錯誤",
            "user_id": "user_123"
        },
        {
            "endpoint": "/api/auth/login",
            "method": "POST",
            "status_code": 401,
            "error": "UnauthorizedError", 
            "message": "認證失敗",
            "user_id": "user_456"
        },
        {
            "endpoint": "/api/orders",
            "method": "POST",
            "status_code": 422,
            "error": "ValidationError",
            "message": "請求參數驗證失敗",
            "user_id": "user_789"
        },
        {
            "endpoint": "/api/products",
            "method": "GET",
            "status_code": 429,
            "error": "RateLimitError",
            "message": "請求頻率過高",
            "user_id": "user_101"
        },
        {
            "endpoint": "/api/payments",
            "method": "POST", 
            "status_code": 503,
            "error": "ServiceUnavailableError",
            "message": "支付服務不可用",
            "user_id": "user_202"
        }
    ]
    
    tracker.logger.console_info("🌐 模擬 API 錯誤...")
    
    api_error_data = []
    
    for scenario in api_scenarios:
        # 模擬請求處理時間
        response_time = random.uniform(100, 2000)
        
        context = {
            "endpoint": scenario["endpoint"],
            "method": scenario["method"],
            "status_code": scenario["status_code"],
            "response_time_ms": response_time,
            "user_agent": "Mozilla/5.0 (compatible; API Client)",
            "ip_address": f"192.168.1.{random.randint(1, 254)}"
        }
        
        # 根據狀態碼確定嚴重程度
        if scenario["status_code"] >= 500:
            severity = "error"
        elif scenario["status_code"] >= 400:
            severity = "warning"
        else:
            severity = "info"
        
        tracker.log_error(
            error_type=scenario["error"],
            error_msg=scenario["message"],
            context=context,
            severity=severity,
            user_id=scenario["user_id"],
            request_id=f"req_{random.randint(10000, 99999)}"
        )
        
        # 準備表格數據
        api_error_data.append({
            scenario["endpoint"],
            scenario["method"],
            str(scenario["status_code"]),
            scenario["error"],
            f"{response_time:.1f}ms"
        })
        
        time.sleep(0.3)
    
    # API 錯誤摘要表格
    tracker.logger.table(
        title="🌐 API 錯誤摘要",
        data=api_error_data
    )
    
    return tracker

def retry_mechanism_demo():
    """重試機制演示"""
    print("\n=== 錯誤重試機制 ===\n")
    
    logger = create_logger("retry_demo", log_path="./logs/errors")
    
    logger.ascii_header("RETRY", font="slant", border_style="blue")
    
    def simulate_unreliable_operation(operation_name: str, success_rate: float = 0.3):
        """模擬不穩定的操作"""
        return random.random() < success_rate
    
    def retry_operation(operation_name: str, max_retries: int = 3, 
                       delay: float = 1.0, success_rate: float = 0.3):
        """重試操作"""
        
        for attempt in range(max_retries + 1):
            try:
                logger.console_info(f"🔄 嘗試 {operation_name} (第 {attempt + 1} 次)")
                
                # 模擬操作
                time.sleep(0.5)
                
                if simulate_unreliable_operation(operation_name, success_rate):
                    logger.success(f"✅ {operation_name} 成功 (第 {attempt + 1} 次嘗試)")
                    return True
                else:
                    raise Exception(f"{operation_name} 操作失敗")
                    
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"⚠️ {operation_name} 失敗，{delay} 秒後重試: {e}")
                    time.sleep(delay)
                    delay *= 2  # 指數退避
                else:
                    logger.error(f"❌ {operation_name} 最終失敗，已達最大重試次數: {e}")
                    return False
    
    # 測試不同的重試場景
    retry_scenarios = [
        {"name": "資料庫連接", "success_rate": 0.4, "max_retries": 3},
        {"name": "API 調用", "success_rate": 0.6, "max_retries": 2},
        {"name": "檔案上傳", "success_rate": 0.3, "max_retries": 4},
        {"name": "訊息發送", "success_rate": 0.8, "max_retries": 2}
    ]
    
    retry_results = []
    
    for scenario in retry_scenarios:
        logger.console_info(f"🎯 測試 {scenario['name']} 重試機制...")
        
        success = retry_operation(
            scenario["name"],
            scenario["max_retries"],
            success_rate=scenario["success_rate"]
        )
        
        retry_results.append({
            scenario["name"],
            str(scenario["max_retries"}),
            f"{scenario['success_rate']*100:.0f}%",
            "成功" if success else "失敗"
        })
        
        time.sleep(1)
    
    # 重試結果摘要
    logger.table(
        title="🔄 重試機制測試結果",
        data=retry_results
    )

def error_analysis_and_reporting():
    """錯誤分析和報告"""
    print("\n=== 錯誤分析和報告 ===\n")
    
    logger = create_logger("error_analysis", log_path="./logs/errors")
    
    logger.ascii_header("ANALYSIS", font="slant", border_style="magenta")
    
    # 模擬錯誤統計數據
    error_stats = {
        "last_24h": {
            "total_errors": 1247,
            "critical_errors": 12,
            "error_rate": 2.3
        },
        "top_errors": [
            {"type": "DatabaseTimeout", "count": 234, "trend": "增加"},
            {"type": "APIRateLimit", "count": 189, "trend": "穩定"},
            {"type": "ValidationError", "count": 156, "trend": "減少"},
            {"type": "AuthenticationError", "count": 98, "trend": "穩定"},
            {"type": "ServiceUnavailable", "count": 67, "trend": "增加"}
        ],
        "error_distribution": {
            "database": 45.2,
            "api": 28.7,
            "authentication": 15.6,
            "validation": 7.8,
            "other": 2.7
        }
    }
    
    logger.console_info("📊 生成錯誤分析報告...")
    
    # 基本統計
    basic_stats = [
        f"24 小時內錯誤總數: {error_stats['last_24h']['total_errors']}",
        f"嚴重錯誤數量: {error_stats['last_24h']['critical_errors']}",
        f"錯誤率: {error_stats['last_24h']['error_rate']}%",
        f"錯誤類型數: {len(error_stats['top_errors'})}"
    ]
    
    logger.block("📈 錯誤統計概覽", basic_stats, border_style="blue")
    
    # 頂級錯誤表格
    top_errors_data = []
    for error in error_stats["top_errors"]:
        top_errors_data.append({
            error["type"],
            str(error["count"}),
            error["trend"]
        })
    
    logger.table(
        title="🔝 頂級錯誤類型",
        data=top_errors_data
    )
    
    # 錯誤分布
    distribution_data = []
    for category, percentage in error_stats["error_distribution"].items():
        distribution_data.append({category, f"{percentage}%"})
    
    logger.table(
        title="📊 錯誤分布",
        data=distribution_data
    )
    
    # 分析建議
    recommendations = [
        "資料庫錯誤占比最高 (45.2%)，建議優化連接池配置",
        "API 錯誤次之 (28.7%)，考慮實施熔斷器模式",
        "認證錯誤 (15.6%) 可能表示安全問題，需要調查",
        "DatabaseTimeout 趨勢增加，建議檢查查詢性能",
        "ServiceUnavailable 增加，檢查外部服務依賴"
    ]
    
    logger.block("💡 錯誤分析建議", recommendations, border_style="yellow")
    
    # 記錄分析完成
    logger.info("錯誤分析報告生成完成")

def exception_handling_best_practices():
    """異常處理最佳實踐"""
    print("\n=== 異常處理最佳實踐 ===\n")
    
    logger = create_logger("best_practices", log_path="./logs/errors")
    
    logger.ascii_header("BEST PRACTICES", font="slant", border_style="cyan")
    
    # 最佳實踐示例
    def demonstrate_good_error_handling():
        """演示良好的錯誤處理"""
        
        logger.console_info("📋 演示異常處理最佳實踐...")
        
        # 1. 具體的異常捕獲
        try:
            # 模擬可能失敗的操作
            if random.random() < 0.3:
                raise ValueError("無效的輸入參數")
            if random.random() < 0.3:
                raise ConnectionError("網路連接失敗")
            if random.random() < 0.3:
                raise TimeoutError("操作超時")
                
            logger.success("✅ 操作成功完成")
            
        except ValueError as e:
            logger.error(f"❌ 參數錯誤: {e}")
            # 記錄詳細上下文
            logger.error(f"錯誤追蹤: {traceback.format_exc()}")
            
        except ConnectionError as e:
            logger.error(f"❌ 連接錯誤: {e}")
            # 可能的恢復操作
            logger.info("嘗試重新建立連接...")
            
        except TimeoutError as e:
            logger.warning(f"⚠️ 超時錯誤: {e}")
            # 增加超時配置建議
            logger.info("建議增加超時時間或優化操作")
            
        except Exception as e:
            logger.error(f"❌ 未預期的錯誤: {e}")
            logger.error(f"完整追蹤: {traceback.format_exc()}")
        
        finally:
            logger.debug("🧹 執行清理操作")
    
    # 執行演示
    for i in range(3):
        logger.console_info(f"🎯 執行演示 {i+1}")
        demonstrate_good_error_handling()
        time.sleep(0.5)
    
    # 最佳實踐指南
    best_practices = {
        "錯誤記錄": [
            "記錄足夠的上下文信息",
            "包含錯誤發生的時間戳",
            "記錄用戶和請求標識",
            "避免記錄敏感信息"
        ],
        "異常分類": [
            "使用具體的異常類型",
            "避免捕獲過於寬泛的異常",
            "為業務邏輯創建自定義異常",
            "區分可恢復和不可恢復錯誤"
        ],
        "錯誤恢復": [
            "實施適當的重試機制",
            "使用熔斷器模式",
            "提供降級功能",
            "清理資源和狀態"
        ],
        "監控告警": [
            "設定錯誤率閾值",
            "監控關鍵錯誤類型",
            "建立錯誤趨勢分析",
            "及時通知相關人員"
        ]
    }
    
    for category, practices in best_practices.items():
        logger.console_info(f"📚 {category}最佳實踐")
        logger.block(f"💡 {category}", practices, border_style="cyan")
        time.sleep(0.5)

def main():
    """主函數"""
    print("=== Pretty Loguru 錯誤追蹤完整指南 ===")
    
    # 1. 資料庫錯誤模擬
    db_tracker = database_error_simulation()
    
    # 2. API 錯誤模擬
    api_tracker = api_error_simulation()
    
    # 3. 重試機制演示
    retry_mechanism_demo()
    
    # 4. 錯誤分析和報告
    error_analysis_and_reporting()
    
    # 5. 異常處理最佳實踐
    exception_handling_best_practices()
    
    print("\n" + "="*50)
    print("錯誤追蹤演示完成!")
    print("檢查以下目錄查看錯誤追蹤日誌:")
    print("- ./logs/errors/")
    print("\n有效的錯誤追蹤幫助您:")
    print("• 快速定位和解決問題")
    print("• 提高系統穩定性")
    print("• 改善用戶體驗")
    print("• 預防類似錯誤再次發生")

if __name__ == "__main__":
    main()