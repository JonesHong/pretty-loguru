#!/usr/bin/env python3
"""
📊 08_enterprise/monitoring_integration.py
監控系統整合範例

這個範例展示了如何將 pretty-loguru 與企業級監控系統整合，
包含 Prometheus 指標、Grafana 儀表板、ELK Stack 和報警通知系統。
"""

import time
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass
from pretty_loguru import create_logger

# 模擬 Prometheus 客戶端（在實際環境中使用 prometheus_client）
class PrometheusMetrics:
    """Prometheus 指標模擬類"""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.histograms = defaultdict(list)
        self.gauges = defaultdict(float)
    
    def counter_inc(self, name: str, labels: Dict[str, str] = None):
        """計數器增加"""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self.counters[key] += 1
    
    def histogram_observe(self, name: str, value: float, labels: Dict[str, str] = None):
        """直方圖觀察值"""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self.histograms[key].append(value)
    
    def gauge_set(self, name: str, value: float, labels: Dict[str, str] = None):
        """量表設置值"""
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self.gauges[key] = value
    
    def get_metrics(self) -> Dict[str, Any]:
        """獲取所有指標"""
        return {
            "counters": dict(self.counters),
            "histograms": {k: {
                "count": len(v),
                "sum": sum(v),
                "avg": sum(v) / len(v) if v else 0,
                "percentiles": self._calculate_percentiles(v)
            } for k, v in self.histograms.items()},
            "gauges": dict(self.gauges)
        }
    
    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """計算百分位數"""
        if not values:
            return {}
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return {
            "p50": sorted_values[int(n * 0.5)],
            "p90": sorted_values[int(n * 0.9)],
            "p95": sorted_values[int(n * 0.95)],
            "p99": sorted_values[int(n * 0.99)] if n > 1 else sorted_values[0]
        }

@dataclass
class ElasticsearchDocument:
    """Elasticsearch 文檔模型"""
    index: str
    doc_type: str
    body: Dict[str, Any]
    timestamp: datetime

class ElasticsearchClient:
    """Elasticsearch 客戶端模擬類"""
    
    def __init__(self):
        self.documents = []
        self.indices = set()
    
    def index(self, index: str, doc_type: str, body: Dict[str, Any]):
        """索引文檔"""
        doc = ElasticsearchDocument(
            index=index,
            doc_type=doc_type,
            body=body,
            timestamp=datetime.utcnow()
        )
        self.documents.append(doc)
        self.indices.add(index)
    
    def search(self, index: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """搜尋文檔"""
        results = []
        for doc in self.documents:
            if doc.index == index:
                results.append({
                    "_index": doc.index,
                    "_type": doc.doc_type,
                    "_source": doc.body,
                    "@timestamp": doc.timestamp.isoformat()
                })
        return results[:100]  # 限制返回結果數量
    
    def get_indices(self) -> List[str]:
        """獲取所有索引"""
        return list(self.indices)

class AlertManager:
    """報警管理器"""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = {}
        self.notification_channels = []
    
    def add_alert_rule(self, name: str, condition: str, severity: str, 
                       threshold: float = None):
        """添加報警規則"""
        self.alert_rules[name] = {
            "condition": condition,
            "severity": severity,
            "threshold": threshold,
            "created_at": datetime.utcnow().isoformat()
        }
    
    def trigger_alert(self, rule_name: str, message: str, details: Dict[str, Any] = None):
        """觸發報警"""
        if rule_name not in self.alert_rules:
            return
        
        alert = {
            "id": f"alert_{len(self.alerts) + 1}",
            "rule_name": rule_name,
            "message": message,
            "severity": self.alert_rules[rule_name]["severity"],
            "details": details or {},
            "triggered_at": datetime.utcnow().isoformat(),
            "status": "firing"
        }
        
        self.alerts.append(alert)
        self._send_notification(alert)
    
    def _send_notification(self, alert: Dict[str, Any]):
        """發送通知"""
        print(f"🚨 ALERT [{alert['severity'].upper()}]: {alert['message']}")
        print(f"   Rule: {alert['rule_name']}")
        print(f"   Time: {alert['triggered_at']}")

class MonitoringIntegration:
    """監控系統整合器"""
    
    def __init__(self):
        # 初始化各種監控組件
        self.prometheus = PrometheusMetrics()
        self.elasticsearch = ElasticsearchClient()
        self.alert_manager = AlertManager()
        
        # 效能指標追蹤
        self.performance_metrics = {
            "log_processing_times": deque(maxlen=1000),
            "log_volume": defaultdict(int),
            "error_rates": defaultdict(int),
            "response_times": deque(maxlen=1000)
        }
        
        # 建立監控日誌記錄器
        self.logger = create_logger(
            name="monitoring_integration",
            log_dir="logs/monitoring",
            level="INFO",
            rotation="hourly",
            retention="30 days"
        )
        
        # 設置報警規則
        self._setup_alert_rules()
        
        self.logger.info("📊 監控系統整合器啟動")
    
    def _setup_alert_rules(self):
        """設置報警規則"""
        self.alert_manager.add_alert_rule(
            name="high_error_rate",
            condition="error_rate > 5%",
            severity="critical",
            threshold=0.05
        )
        
        self.alert_manager.add_alert_rule(
            name="slow_response_time",
            condition="avg_response_time > 2s",
            severity="warning",
            threshold=2.0
        )
        
        self.alert_manager.add_alert_rule(
            name="log_volume_spike",
            condition="log_volume > 1000/min",
            severity="warning",
            threshold=1000
        )
    
    def track_log_event(self, level: str, service: str, duration: float = None):
        """追蹤日誌事件"""
        # 更新 Prometheus 指標
        self.prometheus.counter_inc("logs_total", {"level": level, "service": service})
        
        if duration is not None:
            self.prometheus.histogram_observe("log_processing_duration_seconds", duration, {"service": service})
            self.performance_metrics["log_processing_times"].append(duration)
        
        # 更新內部指標
        self.performance_metrics["log_volume"][service] += 1
        
        # 檢查是否需要觸發報警
        self._check_volume_alerts(service)
    
    def track_application_metrics(self, service: str, response_time: float, 
                                error_occurred: bool = False):
        """追蹤應用程式指標"""
        # 記錄回應時間
        self.prometheus.histogram_observe("http_request_duration_seconds", response_time, {"service": service})
        self.performance_metrics["response_times"].append(response_time)
        
        # 記錄錯誤率
        if error_occurred:
            self.prometheus.counter_inc("http_requests_errors_total", {"service": service})
            self.performance_metrics["error_rates"][service] += 1
        
        # 記錄總請求數
        self.prometheus.counter_inc("http_requests_total", {"service": service})
        
        # 檢查效能報警
        self._check_performance_alerts(service, response_time, error_occurred)
    
    def send_to_elasticsearch(self, log_record: Dict[str, Any], index_prefix: str = "logs"):
        """發送日誌到 Elasticsearch"""
        # 格式化為 ELK 標準格式
        elk_document = {
            "@timestamp": datetime.utcnow().isoformat(),
            "@version": "1",
            "message": log_record.get("message", ""),
            "level": log_record.get("level", "INFO"),
            "logger": log_record.get("name", "default"),
            "service": log_record.get("service", "unknown"),
            "host": "localhost",
            "fields": log_record.get("extra", {}),
            "tags": ["pretty-loguru", "enterprise"],
            "timestamp": log_record.get("time", datetime.utcnow().isoformat())
        }
        
        # 根據日期建立索引
        index_name = f"{index_prefix}-{datetime.utcnow().strftime('%Y.%m.%d')}"
        
        try:
            self.elasticsearch.index(
                index=index_name,
                doc_type="_doc",
                body=elk_document
            )
            
            self.track_log_event("INFO", "elasticsearch")
            
        except Exception as e:
            self.logger.error(f"發送到 Elasticsearch 失敗: {e}")
    
    def _check_volume_alerts(self, service: str):
        """檢查日誌量報警"""
        current_volume = self.performance_metrics["log_volume"][service]
        
        # 簡單的報警邏輯：每分鐘檢查一次
        if current_volume > 100:  # 模擬閾值
            self.alert_manager.trigger_alert(
                rule_name="log_volume_spike",
                message=f"服務 {service} 日誌量異常增加",
                details={"service": service, "volume": current_volume}
            )
    
    def _check_performance_alerts(self, service: str, response_time: float, error_occurred: bool):
        """檢查效能報警"""
        # 檢查回應時間
        if response_time > 2.0:
            self.alert_manager.trigger_alert(
                rule_name="slow_response_time",
                message=f"服務 {service} 回應時間過慢",
                details={"service": service, "response_time": response_time}
            )
        
        # 檢查錯誤率（簡化版）
        if error_occurred:
            error_count = self.performance_metrics["error_rates"][service]
            if error_count > 5:  # 簡單閾值
                self.alert_manager.trigger_alert(
                    rule_name="high_error_rate",
                    message=f"服務 {service} 錯誤率過高",
                    details={"service": service, "error_count": error_count}
                )
    
    def create_grafana_dashboard_config(self) -> Dict[str, Any]:
        """建立 Grafana 儀表板配置"""
        dashboard_config = {
            "dashboard": {
                "id": None,
                "title": "Pretty-Loguru Enterprise Monitoring",
                "description": "企業級日誌監控儀表板",
                "tags": ["logging", "monitoring", "enterprise"],
                "timezone": "UTC",
                "refresh": "30s",
                "time": {
                    "from": "now-1h",
                    "to": "now"
                },
                "panels": [
                    {
                        "id": 1,
                        "title": "Log Volume by Service",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                        "targets": [
                            {
                                "expr": "rate(logs_total[5m])",
                                "legendFormat": "{{service}} - {{level}}",
                                "refId": "A"
                            }
                        ],
                        "yAxes": [
                            {"label": "Logs per second", "min": 0}
                        ]
                    },
                    {
                        "id": 2,
                        "title": "Log Processing Time",
                        "type": "graph",
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                        "targets": [
                            {
                                "expr": "histogram_quantile(0.95, log_processing_duration_seconds)",
                                "legendFormat": "95th percentile",
                                "refId": "A"
                            },
                            {
                                "expr": "histogram_quantile(0.50, log_processing_duration_seconds)",
                                "legendFormat": "50th percentile",
                                "refId": "B"
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "title": "Error Rate by Service",
                        "type": "singlestat",
                        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 8},
                        "targets": [
                            {
                                "expr": "rate(http_requests_errors_total[5m]) / rate(http_requests_total[5m]) * 100",
                                "refId": "A"
                            }
                        ],
                        "valueName": "current",
                        "format": "percent",
                        "thresholds": "1,5"
                    },
                    {
                        "id": 4,
                        "title": "Active Alerts",
                        "type": "table",
                        "gridPos": {"h": 6, "w": 12, "x": 0, "y": 12},
                        "targets": [
                            {
                                "expr": "ALERTS",
                                "refId": "A"
                            }
                        ]
                    }
                ]
            }
        }
        
        self.logger.info("📊 Grafana 儀表板配置已建立", extra={"dashboard_panels": len(dashboard_config["dashboard"]["panels"])})
        return dashboard_config
    
    def generate_monitoring_report(self) -> Dict[str, Any]:
        """生成監控報告"""
        # 計算統計數據
        processing_times = list(self.performance_metrics["log_processing_times"])
        response_times = list(self.performance_metrics["response_times"])
        
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        report = {
            "report_timestamp": datetime.utcnow().isoformat(),
            "monitoring_period": "last_hour",
            "metrics_summary": {
                "total_logs_processed": sum(self.performance_metrics["log_volume"].values()),
                "avg_log_processing_time_ms": round(avg_processing_time * 1000, 2),
                "avg_response_time_ms": round(avg_response_time * 1000, 2),
                "total_errors": sum(self.performance_metrics["error_rates"].values()),
                "elasticsearch_indices": len(self.elasticsearch.get_indices()),
                "active_alerts": len([a for a in self.alert_manager.alerts if a["status"] == "firing"])
            },
            "prometheus_metrics": self.prometheus.get_metrics(),
            "top_services_by_volume": dict(sorted(
                self.performance_metrics["log_volume"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]),
            "recent_alerts": self.alert_manager.alerts[-10:],  # 最近10個報警
            "health_status": "healthy" if avg_response_time < 1.0 else "degraded"
        }
        
        self.logger.info("📈 監控報告生成完成", extra=report)
        return report

async def simulate_monitored_application():
    """模擬被監控的應用程式"""
    monitoring = MonitoringIntegration()
    
    print("📊 監控系統整合演示")
    print("=" * 50)
    
    # 模擬各種應用程式活動
    services = ["user-service", "order-service", "payment-service", "notification-service"]
    
    for i in range(50):  # 模擬50個請求
        service = services[i % len(services)]
        
        # 模擬請求處理
        start_time = time.time()
        
        # 模擬一些請求會比較慢
        processing_time = 0.1 + (0.5 if i % 10 == 0 else 0)
        await asyncio.sleep(processing_time)
        
        response_time = time.time() - start_time
        
        # 模擬一些請求會失敗
        error_occurred = i % 15 == 0
        
        # 追蹤指標
        monitoring.track_application_metrics(service, response_time, error_occurred)
        monitoring.track_log_event("INFO" if not error_occurred else "ERROR", service, processing_time)
        
        # 發送日誌到 Elasticsearch
        log_record = {
            "message": f"處理請求 {i+1}",
            "level": "ERROR" if error_occurred else "INFO",
            "service": service,
            "request_id": f"req_{i+1}",
            "response_time": response_time,
            "extra": {
                "user_id": f"user_{(i % 10) + 1}",
                "endpoint": f"/api/{service.split('-')[0]}",
                "status_code": 500 if error_occurred else 200
            }
        }
        
        monitoring.send_to_elasticsearch(log_record)
        
        # 每10個請求輸出一次進度
        if (i + 1) % 10 == 0:
            print(f"   處理了 {i + 1} 個請求...")
    
    # 生成 Grafana 儀表板配置
    print("\n📊 建立 Grafana 儀表板...")
    dashboard_config = monitoring.create_grafana_dashboard_config()
    print(f"   儀表板包含 {len(dashboard_config['dashboard']['panels'])} 個面板")
    
    # 生成監控報告
    print("\n📈 生成監控報告...")
    report = monitoring.generate_monitoring_report()
    print(f"   處理日誌總數: {report['metrics_summary']['total_logs_processed']}")
    print(f"   平均處理時間: {report['metrics_summary']['avg_log_processing_time_ms']} ms")
    print(f"   平均回應時間: {report['metrics_summary']['avg_response_time_ms']} ms")
    print(f"   錯誤總數: {report['metrics_summary']['total_errors']}")
    print(f"   活躍報警數: {report['metrics_summary']['active_alerts']}")
    print(f"   系統健康狀態: {report['health_status']}")
    
    print("\n📁 監控日誌檔案位置:")
    print("   - logs/monitoring/ (監控系統日誌)")
    
    return monitoring

if __name__ == "__main__":
    asyncio.run(simulate_monitored_application())