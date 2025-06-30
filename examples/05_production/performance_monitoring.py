#!/usr/bin/env python3
"""
Performance Monitoring - 性能監控和優化

這個範例展示：
1. 性能指標收集和記錄
2. 應用性能監控 (APM)
3. 資源使用情況追蹤
4. 性能瓶頸識別

運行方式：
    python performance_monitoring.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
import time
import psutil
import threading
from datetime import datetime, timedelta
import random

def system_performance_monitor():
    """系統性能監控"""
    print("=== 系統性能監控 ===\n")
    
    logger = create_logger("system_monitor", 
                          log_path="./logs/performance", 
                          preset="hourly",
                          retention="7 days")
    
    logger.ascii_header("SYSTEM PERF", font="slant", border_style="blue")
    
    logger.console_info("📊 開始系統性能監控...")
    
    # 收集系統指標
    def collect_system_metrics():
        try:
            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 記憶體使用情況
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # 磁碟使用情況
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_free_gb = disk.free / (1024**3)
            
            # 網路 I/O (如果可用)
            try:
                network = psutil.net_io_counters()
                network_sent_mb = network.bytes_sent / (1024**2)
                network_recv_mb = network.bytes_recv / (1024**2)
            except:
                network_sent_mb = network_recv_mb = 0
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_used_gb': memory_used_gb,
                'memory_total_gb': memory_total_gb,
                'disk_percent': disk_percent,
                'disk_free_gb': disk_free_gb,
                'network_sent_mb': network_sent_mb,
                'network_recv_mb': network_recv_mb
            }
        except Exception as e:
            # 如果無法獲取真實指標，返回模擬數據
            logger.warning(f"無法獲取系統指標，使用模擬數據: {e}")
            return {
                'cpu_percent': random.uniform(20, 80),
                'memory_percent': random.uniform(40, 85),
                'memory_used_gb': random.uniform(2, 8),
                'memory_total_gb': 16,
                'disk_percent': random.uniform(30, 70),
                'disk_free_gb': random.uniform(50, 200),
                'network_sent_mb': random.uniform(100, 1000),
                'network_recv_mb': random.uniform(80, 800)
            }
    
    # 監控週期
    monitoring_cycles = 5
    metrics_history = []
    
    for cycle in range(monitoring_cycles):
        logger.console_info(f"📈 收集第 {cycle + 1} 輪指標...")
        
        metrics = collect_system_metrics()
        metrics['timestamp'] = datetime.now().isoformat()
        metrics_history.append(metrics)
        
        # 記錄系統指標
        logger.info(f"系統指標 - CPU: {metrics['cpu_percent']:.1f}%, "
                   f"記憶體: {metrics['memory_percent']:.1f}%, "
                   f"磁碟: {metrics['disk_percent']:.1f}%")
        
        # 檢查是否有性能問題
        performance_issues = []
        
        if metrics['cpu_percent'] > 80:
            performance_issues.append(f"CPU 使用率過高: {metrics['cpu_percent']:.1f}%")
            logger.warning(f"⚠️ CPU 使用率過高: {metrics['cpu_percent']:.1f}%")
        
        if metrics['memory_percent'] > 85:
            performance_issues.append(f"記憶體使用率過高: {metrics['memory_percent']:.1f}%")
            logger.warning(f"⚠️ 記憶體使用率過高: {metrics['memory_percent']:.1f}%")
        
        if metrics['disk_percent'] > 90:
            performance_issues.append(f"磁碟使用率過高: {metrics['disk_percent']:.1f}%")
            logger.error(f"🚨 磁碟使用率過高: {metrics['disk_percent']:.1f}%")
        
        if not performance_issues:
            logger.debug("✓ 系統性能正常")
        
        time.sleep(2)  # 等待下一輪監控
    
    # 性能總結
    avg_cpu = sum(m['cpu_percent'] for m in metrics_history) / len(metrics_history)
    avg_memory = sum(m['memory_percent'] for m in metrics_history) / len(metrics_history)
    max_cpu = max(m['cpu_percent'] for m in metrics_history)
    max_memory = max(m['memory_percent'] for m in metrics_history)
    
    performance_summary = [
        f"監控週期: {monitoring_cycles} 輪",
        f"平均 CPU: {avg_cpu:.1f}%",
        f"平均記憶體: {avg_memory:.1f}%", 
        f"最高 CPU: {max_cpu:.1f}%",
        f"最高記憶體: {max_memory:.1f}%"
    ]
    
    logger.block("📊 性能監控總結", performance_summary, border_style="blue")
    
    return metrics_history

def application_performance_monitor():
    """應用性能監控 (APM)"""
    print("\n=== 應用性能監控 ===\n")
    
    logger = create_logger("apm_monitor",
                          log_path="./logs/performance",
                          preset="daily",
                          retention="30 days")
    
    logger.ascii_header("APM", font="slant", border_style="green")
    
    # 模擬不同類型的應用操作
    operations = [
        {"name": "database_query", "avg_time": 45, "variance": 20},
        {"name": "api_request", "avg_time": 180, "variance": 50},
        {"name": "cache_lookup", "avg_time": 5, "variance": 2},
        {"name": "file_upload", "avg_time": 1200, "variance": 300},
        {"name": "data_processing", "avg_time": 800, "variance": 200}
    ]
    
    performance_data = []
    
    logger.console_info("🔍 監控應用性能...")
    
    for operation in operations:
        logger.console_info(f"📏 測試操作: {operation['name']}")
        
        # 模擬多次操作
        times = []
        for i in range(10):
            # 模擬操作執行時間
            execution_time = max(1, random.gauss(operation['avg_time'], operation['variance'}))
            times.append(execution_time)
            
            # 記錄單次操作
            logger.debug(f"{operation['name']} 執行時間: {execution_time:.1f}ms")
            
            # 模擬操作間隔
            time.sleep(0.1)
        
        # 計算統計數據
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        # 判斷性能狀況
        if avg_time > operation['avg_time'] * 1.5:
            status = "慢"
            log_level = "warning"
        elif avg_time > operation['avg_time'] * 1.2:
            status = "偏慢"
            log_level = "info"
        else:
            status = "正常"
            log_level = "debug"
        
        # 記錄性能結果
        perf_msg = (f"{operation['name']} 性能 - "
                   f"平均: {avg_time:.1f}ms, "
                   f"最小: {min_time:.1f}ms, "
                   f"最大: {max_time:.1f}ms, "
                   f"狀態: {status}")
        
        if log_level == "warning":
            logger.warning(f"⚠️ {perf_msg}")
        elif log_level == "info":
            logger.info(f"ℹ️ {perf_msg}")
        else:
            logger.debug(f"✓ {perf_msg}")
        
        performance_data.append({
            operation['name'],
            f"{avg_time:.1f}ms", 
            f"{min_time:.1f}ms",
            f"{max_time:.1f}ms",
            status
        })
    
    # 性能摘要表格
    logger.table(
        title="⚡ 應用性能摘要",
        data=performance_data
    )

def database_performance_monitor():
    """資料庫性能監控"""
    print("\n=== 資料庫性能監控 ===\n")
    
    logger = create_logger("db_monitor",
                          log_path="./logs/performance",
                          rotation="20 MB",
                          retention="14 days")
    
    logger.ascii_header("DATABASE", font="slant", border_style="yellow")
    
    # 模擬資料庫操作
    db_operations = [
        {"type": "SELECT", "table": "users", "rows": 1247},
        {"type": "INSERT", "table": "orders", "rows": 1},
        {"type": "UPDATE", "table": "products", "rows": 5},
        {"type": "DELETE", "table": "logs", "rows": 1500},
        {"type": "JOIN", "table": "users_orders", "rows": 856}
    ]
    
    logger.console_info("🗄️ 監控資料庫性能...")
    
    db_performance_data = []
    total_queries = 0
    slow_queries = 0
    
    for operation in db_operations:
        # 模擬查詢執行
        query_time = random.uniform(10, 300)  # 10-300ms
        
        # 模擬連接池狀態
        active_connections = random.randint(5, 50)
        
        # 判斷是否為慢查詢 (>100ms)
        is_slow = query_time > 100
        if is_slow:
            slow_queries += 1
        
        total_queries += 1
        
        # 記錄查詢
        query_msg = (f"SQL {operation['type']} - "
                    f"表: {operation['table']}, "
                    f"影響行數: {operation['rows']}, "
                    f"執行時間: {query_time:.1f}ms, "
                    f"連接數: {active_connections}")
        
        if is_slow:
            logger.warning(f"🐌 慢查詢: {query_msg}")
        else:
            logger.debug(f"⚡ 快查詢: {query_msg}")
        
        # 記錄連接池狀態
        if active_connections > 40:
            logger.warning(f"⚠️ 連接池使用率高: {active_connections}/50")
        
        db_performance_data.append({
            operation['type'],
            operation['table'],
            str(operation['rows'}),
            f"{query_time:.1f}ms",
            "慢" if is_slow else "快"
        })
        
        time.sleep(0.2)
    
    # 資料庫性能摘要
    logger.table(
        title="🗄️ 資料庫性能摘要", 
        data=db_performance_data
    )
    
    # 資料庫統計
    slow_query_rate = (slow_queries / total_queries) * 100
    
    db_stats = [
        f"總查詢數: {total_queries}",
        f"慢查詢數: {slow_queries}",
        f"慢查詢率: {slow_query_rate:.1f}%",
        f"平均連接數: {random.randint(15, 35)}"
    ]
    
    logger.block("📈 資料庫統計", db_stats, border_style="yellow")
    
    if slow_query_rate > 20:
        logger.error(f"🚨 慢查詢率過高: {slow_query_rate:.1f}%")
    elif slow_query_rate > 10:
        logger.warning(f"⚠️ 慢查詢率偏高: {slow_query_rate:.1f}%")

def real_time_monitoring():
    """實時監控模擬"""
    print("\n=== 實時監控 ===\n")
    
    logger = create_logger("realtime_monitor",
                          log_path="./logs/performance",
                          preset="minute",
                          retention="24 hours")
    
    logger.ascii_header("REALTIME", font="slant", border_style="magenta")
    
    logger.console_info("🔴 啟動實時監控 (運行 10 秒)...")
    
    # 監控指標
    metrics = {
        'requests_per_second': 0,
        'response_time': 0,
        'error_rate': 0,
        'active_users': 0
    }
    
    start_time = time.time()
    monitor_duration = 10  # 監控 10 秒
    
    try:
        while time.time() - start_time < monitor_duration:
            # 模擬實時指標
            metrics['requests_per_second'] = random.randint(50, 200)
            metrics['response_time'] = random.uniform(80, 250)
            metrics['error_rate'] = random.uniform(0, 5)
            metrics['active_users'] = random.randint(100, 500)
            
            # 記錄實時指標
            logger.info(f"實時指標 - "
                       f"RPS: {metrics['requests_per_second']}, "
                       f"響應時間: {metrics['response_time']:.1f}ms, "
                       f"錯誤率: {metrics['error_rate']:.2f}%, "
                       f"活躍用戶: {metrics['active_users']}")
            
            # 檢查異常指標
            alerts = []
            
            if metrics['response_time'] > 200:
                alerts.append(f"響應時間過長: {metrics['response_time']:.1f}ms")
                
            if metrics['error_rate'] > 3:
                alerts.append(f"錯誤率過高: {metrics['error_rate']:.2f}%")
                
            if metrics['requests_per_second'] > 180:
                alerts.append(f"請求量激增: {metrics['requests_per_second']} RPS")
            
            # 記錄告警
            for alert in alerts:
                logger.warning(f"⚠️ 告警: {alert}")
            
            if not alerts:
                logger.debug("✓ 所有指標正常")
            
            time.sleep(1)  # 每秒監控一次
    
    except KeyboardInterrupt:
        logger.info("實時監控被用戶中斷")
    
    logger.success("🔴 實時監控結束")

def performance_optimization_tips():
    """性能優化建議"""
    print("\n=== 性能優化建議 ===\n")
    
    logger = create_logger("optimization_tips", log_path="./logs/performance")
    
    logger.ascii_header("OPTIMIZE", font="slant", border_style="cyan")
    
    # 分類優化建議
    optimization_categories = {
        "系統層面": [
            "監控 CPU 和記憶體使用率，避免資源瓶頸",
            "使用 SSD 硬碟提升 I/O 性能",
            "適當調整系統核心參數",
            "定期清理日誌和臨時檔案"
        ],
        "應用層面": [
            "實施應用性能監控 (APM)",
            "識別和優化慢查詢",
            "使用連接池管理資料庫連接",
            "實施適當的快取策略"
        ],
        "日誌層面": [
            "選擇適當的日誌級別",
            "使用非同步日誌寫入",
            "合理設定日誌輪替策略",
            "避免在高頻路徑記錄詳細日誌"
        ],
        "監控層面": [
            "建立核心指標監控",
            "設定適當的告警閾值",
            "實施實時監控和告警",
            "定期分析性能趨勢"
        ]
    }
    
    for category, tips in optimization_categories.items():
        logger.console_info(f"📋 {category}優化建議")
        logger.block(f"💡 {category}", tips, border_style="cyan")
        logger.info(f"提供 {category} 優化建議 - {len(tips)} 項")
        time.sleep(0.5)

def main():
    """主函數"""
    print("=== Pretty Loguru 性能監控完整指南 ===")
    
    # 1. 系統性能監控
    system_metrics = system_performance_monitor()
    
    # 2. 應用性能監控
    application_performance_monitor()
    
    # 3. 資料庫性能監控
    database_performance_monitor()
    
    # 4. 實時監控
    real_time_monitoring()
    
    # 5. 性能優化建議
    performance_optimization_tips()
    
    print("\n" + "="*50)
    print("性能監控演示完成!")
    print("檢查以下目錄查看性能監控日誌:")
    print("- ./logs/performance/")
    print("\n性能監控幫助您:")
    print("• 及早發現性能瓶頸")
    print("• 優化系統資源使用")
    print("• 提升用戶體驗")
    print("• 預防系統故障")

if __name__ == "__main__":
    main()