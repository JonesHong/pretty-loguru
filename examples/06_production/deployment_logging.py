#!/usr/bin/env python3
"""
Deployment Logging - 部署環境日誌管理

這個範例展示：
1. 多環境配置管理 (dev/staging/prod)
2. 環境自動檢測和配置
3. 部署流程日誌記錄
4. 服務健康檢查日誌

運行方式：
    # 指定環境運行
    APP_ENV=production python deployment_logging.py
    APP_ENV=staging python deployment_logging.py
    APP_ENV=development python deployment_logging.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets
import os
import time
import json
from datetime import datetime

def get_environment_config():
    """根據環境變數獲取配置"""
    env = os.getenv('APP_ENV', 'development')
    
    configs = {
        'development': {
            'log_dir': './logs/deployment/dev',
            'rotation': '5 MB',
            'retention': '3 days',
            'level': 'DEBUG',
            'use_native_format': True,  # 開發環境使用原生格式便於調試
            'description': '開發環境 - 詳細調試信息 (Native Format)'
        },
        'staging': {
            'log_dir': './logs/deployment/staging', 
            'preset': 'daily',
            'retention': '14 days',
            'level': 'INFO',
            'description': '測試環境 - 功能驗證'
        },
        'production': {
            'log_dir': './logs/deployment/prod',
            'preset': 'daily',
            'retention': '90 days', 
            'level': 'WARNING',
            'description': '生產環境 - 關鍵信息'
        }
    }
    
    return env, configs.get(env, configs['development'])

def deployment_workflow():
    """部署工作流程"""
    print("=== 部署工作流程 ===\n")
    
    env, config = get_environment_config()
    
    # 提取描述，不傳遞給 create_logger
    description = config.pop('description')
    
    logger = create_logger(f"deployment_{env}", **config)
    
    logger.ascii_header("DEPLOYMENT", font="slant", border_style="blue")
    
    log_to_targets(logger, f"🌍 當前環境: {env.upper()}", level="INFO", console_only=True)
    log_to_targets(logger, f"📋 配置說明: {description}", level="INFO", console_only=True)
    
    # 部署步驟
    deployment_steps = [
        ("Pre-deployment checks", "檢查系統資源和依賴"),
        ("Build application", "編譯應用程式和資源"),
        ("Run tests", "執行測試套件"), 
        ("Deploy to environment", f"部署到 {env} 環境"),
        ("Health checks", "服務健康檢查"),
        ("Post-deployment validation", "部署後驗證")
    ]
    
    logger.info(f"開始部署流程 - 環境: {env}")
    
    for i, (step_name, step_desc) in enumerate(deployment_steps, 1):
        log_to_targets(logger, f"📦 步驟 {i}: {step_name}", level="INFO", console_only=True)
        
        # 模擬步驟執行時間
        time.sleep(0.5)
        
        if step_name == "Run tests" and env == "development":
            # 開發環境顯示詳細測試信息
            logger.debug(f"單元測試: 通過 45/45")
            logger.debug(f"整合測試: 通過 12/12")
            logger.debug(f"代碼覆蓋率: 87%")
        
        if step_name == "Health checks":
            # 健康檢查詳情
            health_status = simulate_health_check(logger, env)
            if health_status['status'] == 'healthy':
                logger.success(f"✓ {step_desc} - 通過")
            else:
                logger.warning(f"⚠ {step_desc} - 發現問題")
        else:
            logger.success(f"✓ {step_desc} - 完成")
    
    logger.success(f"🚀 部署到 {env} 環境完成!")
    
    # 部署摘要
    deployment_summary = [
        f"環境: {env}",
        f"部署時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"步驟數: {len(deployment_steps)}",
        "狀態: 成功"
    ]
    
    logger.block("📋 部署摘要", deployment_summary, border_style="green")

def simulate_health_check(logger, env):
    """模擬服務健康檢查"""
    log_to_targets(logger, "🔍 執行健康檢查...", level="INFO", console_only=True)
    
    # 模擬不同環境的健康檢查結果
    checks = [
        ("Database connection", "database"),
        ("Redis cache", "cache"),
        ("External API", "api"),
        ("File system", "filesystem"),
        ("Memory usage", "memory")
    ]
    
    health_results = []
    overall_healthy = True
    
    for check_name, check_type in checks:
        # 模擬檢查結果（生產環境更嚴格）
        if env == "production":
            # 生產環境偶爾有警告
            is_healthy = check_type != "memory"  # 記憶體使用稍高
            status = "healthy" if is_healthy else "warning"
            details = "正常" if is_healthy else "使用率 78%"
        else:
            # 開發/測試環境通常正常
            is_healthy = True
            status = "healthy"
            details = "正常"
        
        if not is_healthy:
            overall_healthy = False
        
        health_results.append({"檢查項目": check_name, "狀態": status, "詳情": details})
        
        # 記錄詳細檢查結果
        if is_healthy:
            logger.debug(f"✓ {check_name}: {details}")
        else:
            logger.warning(f"⚠ {check_name}: {details}")
    
    # 健康檢查摘要表格
    logger.table(
        title="🔍 健康檢查結果",
        data=health_results
    )
    
    return {
        'status': 'healthy' if overall_healthy else 'warning',
        'checks': health_results
    }

def environment_comparison():
    """環境配置對比"""
    print("\n=== 環境配置對比 ===\n")
    
    logger = create_logger("env_comparison", log_dir="./logs/deployment")
    
    logger.ascii_header("ENVIRONMENTS", font="slant", border_style="cyan")
    
    # 獲取所有環境配置
    environments = ['development', 'staging', 'production']
    env_data = []
    
    for env_name in environments:
        # 臨時設定環境變數來獲取配置
        original_env = os.getenv('APP_ENV')
        os.environ['APP_ENV'] = env_name
        
        env, config = get_environment_config()
        
        # 恢復原始環境變數
        if original_env:
            os.environ['APP_ENV'] = original_env
        elif 'APP_ENV' in os.environ:
            del os.environ['APP_ENV']
        
        rotation = config.get('rotation', config.get('preset', '預設'))
        retention = config.get('retention', '預設')
        level = config.get('level', 'INFO')
        
        env_data.append({"環境": env_name, "輪替策略": rotation, "保留期間": retention, "日誌級別": level})
    
    logger.table(
        title="🌍 環境配置對比",
        data=env_data
    )
    
    # 環境選擇建議
    env_recommendations = [
        "開發環境: 詳細日誌，短保留期間，便於調試",
        "測試環境: 平衡配置，中等保留期間，功能驗證",
        "生產環境: 關鍵日誌，長保留期間，性能優先"
    ]
    
    logger.block("💡 環境配置建議", env_recommendations, border_style="blue")

def monitoring_integration():
    """監控系統整合"""
    print("\n=== 監控系統整合 ===\n")
    
    logger = create_logger("monitoring", log_dir="./logs/deployment")
    
    logger.ascii_header("MONITORING", font="slant", border_style="yellow")
    
    # 模擬監控指標
    metrics = {
        "system": {
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "disk_usage": 34.1,
            "network_io": 125.6
        },
        "application": {
            "response_time": 180,
            "requests_per_second": 234,
            "error_rate": 0.05,
            "active_users": 1247
        },
        "database": {
            "connections": 45,
            "query_time": 23.4,
            "cache_hit_rate": 89.2,
            "disk_io": 67.3
        }
    }
    
    log_to_targets(logger, "📊 收集監控指標...", level="INFO", console_only=True)
    
    # 記錄各類指標
    for category, category_metrics in metrics.items():
        logger.info(f"監控類別: {category}")
        
        metric_data = []
        for metric_name, value in category_metrics.items():
            # 判斷指標狀態
            if category == "system":
                status = "正常" if value < 80 else "警告"
                unit = "%" if "usage" in metric_name else "MB/s"
            elif category == "application":
                if metric_name == "response_time":
                    status = "正常" if value < 200 else "警告"
                    unit = "ms"
                elif metric_name == "error_rate":
                    status = "正常" if value < 1.0 else "警告"
                    unit = "%"
                else:
                    status = "正常"
                    unit = "" if metric_name == "active_users" else "/s"
            else:  # database
                status = "正常" if value < 100 else "警告"
                unit = "ms" if "time" in metric_name else ""
            
            metric_data.append({"指標名稱": metric_name, "數值": f"{value}{unit}", "狀態": status})
            
            # 根據狀態記錄不同級別的日誌
            if status == "警告":
                logger.warning(f"{category}.{metric_name}: {value}{unit} - {status}")
            else:
                logger.debug(f"{category}.{metric_name}: {value}{unit} - {status}")
        
        # 顯示分類指標表格
        logger.table(
            title=f"📈 {category.title()} 指標",
            data=metric_data
        )
    
    # 監控告警模擬
    alerts = [
        ("系統記憶體使用率偏高", "warning", "67.8% > 60%"),
        ("資料庫連接數正常", "info", "45 < 100"),
        ("應用響應時間正常", "info", "180ms < 200ms")
    ]
    
    log_to_targets(logger, "🚨 處理監控告警...", level="INFO", console_only=True)
    
    for alert_msg, alert_level, alert_detail in alerts:
        if alert_level == "warning":
            logger.warning(f"⚠️ {alert_msg} - {alert_detail}")
        else:
            logger.info(f"ℹ️ {alert_msg} - {alert_detail}")

def security_audit_logging():
    """安全審計日誌"""
    print("\n=== 安全審計日誌 ===\n")
    
    logger = create_logger("security_audit", log_dir="./logs/deployment/security")
    
    logger.ascii_header("SECURITY", font="slant", border_style="red")
    
    # 模擬安全事件
    security_events = [
        {
            "event_type": "login_success",
            "user_id": "user123",
            "ip_address": "192.168.1.100",
            "timestamp": datetime.now().isoformat(),
            "severity": "info"
        },
        {
            "event_type": "failed_login_attempt", 
            "user_id": "unknown",
            "ip_address": "10.0.0.50",
            "timestamp": datetime.now().isoformat(),
            "severity": "warning"
        },
        {
            "event_type": "permission_denied",
            "user_id": "user456", 
            "resource": "/admin/users",
            "ip_address": "192.168.1.101",
            "timestamp": datetime.now().isoformat(),
            "severity": "warning"
        },
        {
            "event_type": "suspicious_activity",
            "user_id": "user789",
            "details": "異常大量API調用",
            "ip_address": "203.0.113.45",
            "timestamp": datetime.now().isoformat(),
            "severity": "critical"
        }
    ]
    
    log_to_targets(logger, "🔐 記錄安全審計事件...", level="INFO", console_only=True)
    
    security_data = []
    
    for event in security_events:
        event_json = json.dumps(event, ensure_ascii=False, indent=2)
        
        # 根據嚴重程度記錄不同級別的日誌
        if event['severity'] == "critical":
            logger.error(f"🚨 安全事件: {event['event_type']} - {event_json}")
        elif event['severity'] == "warning":
            logger.warning(f"⚠️ 安全事件: {event['event_type']} - {event_json}")
        else:
            logger.info(f"ℹ️ 安全事件: {event['event_type']} - {event_json}")
        
        # 準備表格數據
        security_data.append({
            "事件類型": event['event_type'],
            "用戶ID": event.get('user_id', 'N/A'),
            "IP地址": event.get('ip_address', 'N/A'),
            "嚴重程度": event['severity']
        })
    
    # 安全事件摘要表格
    logger.table(
        title="🔒 安全事件摘要",
        data=security_data
    )
    
    # 安全建議
    security_tips = [
        "定期審查失敗登入記錄",
        "監控異常 API 調用模式", 
        "追蹤權限拒絕事件",
        "建立自動告警機制",
        "保留足夠長的審計日誌"
    ]
    
    logger.block("🛡️ 安全最佳實踐", security_tips, border_style="red")

def main():
    """主函數"""
    current_env = os.getenv('APP_ENV', 'development')
    
    print(f"=== Pretty Loguru 生產環境日誌管理 (環境: {current_env.upper()}) ===")
    
    # 1. 部署工作流程
    deployment_workflow()
    
    # 2. 環境配置對比
    environment_comparison()
    
    # 3. 監控系統整合
    monitoring_integration()
    
    # 4. 安全審計日誌
    security_audit_logging()
    
    print("\n" + "="*50)
    print("生產環境日誌管理演示完成!")
    print("檢查以下目錄查看不同類型的日誌:")
    print("- ./logs/deployment/dev/")
    print("- ./logs/deployment/staging/")
    print("- ./logs/deployment/prod/") 
    print("- ./logs/deployment/security/")
    print(f"\n當前環境: {current_env}")
    print("使用 APP_ENV=production python deployment_logging.py 切換環境")

if __name__ == "__main__":
    main()
