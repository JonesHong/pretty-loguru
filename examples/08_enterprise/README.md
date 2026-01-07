# 💼 08_enterprise - 企業級場景

歡迎來到企業級應用學習！這個模組專為大規模生產環境設計，涵蓋微服務架構、安全合規、監控整合等企業級需求。

## 🎯 學習目標

完成本節後，您將：
- ✅ 掌握微服務日誌架構設計
- ✅ 理解安全和合規要求
- ✅ 學會監控系統整合
- ✅ 能夠設計企業級日誌解決方案

## 📚 範例列表（建議順序）

### 🏗️ Step 1: microservices_logging.py - 微服務日誌架構
**⏱️ 預估時間：30分鐘**

```bash
python microservices_logging.py
```

**學習重點**：
- 分散式日誌追蹤
- 服務間日誌關聯
- 統一日誌格式標準
- 日誌聚合策略

### 🔒 Step 2: security_logging.py - 安全相關日誌
**⏱️ 預估時間：25分鐘**

```bash
python security_logging.py
```

**學習重點**：
- 安全事件記錄
- 審計日誌要求
- 敏感資訊處理
- 入侵檢測日誌

### 📋 Step 3: compliance.py - 合規性要求
**⏱️ 預估時間：20分鐘**

```bash
python compliance.py
```

**學習重點**：
- GDPR/CCPA 合規
- 日誌保留政策
- 數據匿名化
- 合規審計支援

### 📊 Step 4: monitoring_integration.py - 監控系統整合
**⏱️ 預估時間：35分鐘**

```bash
python monitoring_integration.py
```

**學習重點**：
- Prometheus 指標整合
- Grafana 儀表板
- ELK Stack 整合
- 報警和通知系統

## 🎮 企業環境模擬

```bash
# 啟動微服務集群模擬
docker-compose up -d

# 運行企業級範例
python microservices_logging.py &
python security_logging.py &
python compliance.py &
python monitoring_integration.py &

# 生成企業級負載
./scripts/generate_enterprise_load.sh

# 檢查企業級監控
curl http://localhost:3000/metrics  # Prometheus 指標
curl http://localhost:9200/_search  # Elasticsearch 查詢
```

## 💡 企業級架構模式

### 分散式追蹤
```python
import uuid
from contextvars import ContextVar
from typing import Optional

# 全局追蹤上下文
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
span_id_var: ContextVar[Optional[str]] = ContextVar('span_id', default=None)

class DistributedTracing:
    """分散式追蹤管理"""
    
    @staticmethod
    def start_trace() -> str:
        """開始新的追蹤"""
        trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)
        return trace_id
    
    @staticmethod
    def start_span(operation: str) -> str:
        """開始新的 span"""
        span_id = str(uuid.uuid4())
        span_id_var.set(span_id)
        
        logger.info(
            f"開始操作: {operation}",
            extra={
                "trace_id": trace_id_var.get(),
                "span_id": span_id,
                "operation": operation,
                "event_type": "span_start"
            }
        )
        return span_id
    
    @staticmethod
    def end_span(operation: str, status: str = "success"):
        """結束 span"""
        logger.info(
            f"完成操作: {operation}",
            extra={
                "trace_id": trace_id_var.get(),
                "span_id": span_id_var.get(),
                "operation": operation,
                "status": status,
                "event_type": "span_end"
            }
        )

# 使用分散式追蹤
async def process_user_request(user_id: int):
    trace_id = DistributedTracing.start_trace()
    
    try:
        # 用戶驗證服務
        DistributedTracing.start_span("user_authentication")
        await authenticate_user(user_id)
        DistributedTracing.end_span("user_authentication")
        
        # 業務邏輯服務
        DistributedTracing.start_span("business_logic")
        result = await process_business_logic(user_id)
        DistributedTracing.end_span("business_logic")
        
        # 數據持久化服務
        DistributedTracing.start_span("data_persistence")
        await save_result(result)
        DistributedTracing.end_span("data_persistence")
        
    except Exception as e:
        logger.error(
            "請求處理失敗",
            extra={
                "trace_id": trace_id,
                "user_id": user_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        raise
```

### 安全日誌管理
```python
import hashlib
from enum import Enum
from datetime import datetime, timedelta

class SecurityEventType(Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_ACCESS = "data_access"
    CONFIGURATION_CHANGE = "config_change"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"

class SecurityLogger:
    """安全事件專用日誌記錄器"""
    
    def __init__(self):
        self.failed_attempts = {}
        self.logger = create_logger(
            "security",
            log_dir="/var/log/security",
            level="INFO",
            rotation="daily",
            retention="7 years"  # 合規要求
        )
    
    def log_security_event(
        self,
        event_type: SecurityEventType,
        user_id: str,
        ip_address: str,
        details: dict = None
    ):
        """記錄安全事件"""
        
        # 匿名化用戶 ID（合規要求）
        anonymous_user_id = self._anonymize_user_id(user_id)
        
        security_log = {
            "event_type": event_type.value,
            "user_id": anonymous_user_id,
            "ip_address": self._anonymize_ip(ip_address),
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {},
            "severity": self._get_severity(event_type)
        }
        
        # 檢查是否為可疑活動
        if self._is_suspicious_activity(user_id, ip_address, event_type):
            security_log["alert"] = True
            self._trigger_security_alert(security_log)
        
        self.logger.info("安全事件", extra=security_log)
    
    def _anonymize_user_id(self, user_id: str) -> str:
        """匿名化用戶 ID"""
        return hashlib.sha256(f"{user_id}:salt".encode()).hexdigest()[:16]
    
    def _anonymize_ip(self, ip_address: str) -> str:
        """匿名化 IP 地址"""
        parts = ip_address.split('.')
        return f"{parts[0]}.{parts[1]}.*.* "
    
    def _is_suspicious_activity(
        self,
        user_id: str,
        ip_address: str,
        event_type: SecurityEventType
    ) -> bool:
        """檢測可疑活動"""
        
        if event_type == SecurityEventType.LOGIN_FAILURE:
            # 追蹤失敗嘗試
            key = f"{user_id}:{ip_address}"
            now = datetime.utcnow()
            
            if key not in self.failed_attempts:
                self.failed_attempts[key] = []
            
            # 清理舊記錄
            self.failed_attempts[key] = [
                timestamp for timestamp in self.failed_attempts[key]
                if now - timestamp < timedelta(minutes=15)
            ]
            
            self.failed_attempts[key].append(now)
            
            # 15分鐘內超過5次失敗嘗試
            return len(self.failed_attempts[key]) > 5
        
        return False
    
    def _trigger_security_alert(self, security_log: dict):
        """觸發安全警報"""
        # 整合監控系統
        alert_manager.send_alert(
            severity="critical",
            message=f"安全事件檢測: {security_log['event_type']}",
            details=security_log
        )
```

### 合規性管理
```python
from datetime import datetime, timedelta
import json
from typing import List, Dict

class ComplianceManager:
    """合規性管理器"""
    
    def __init__(self):
        self.retention_policies = {
            "financial": timedelta(days=2555),  # 7 年
            "personal_data": timedelta(days=365),  # 1 年
            "system_logs": timedelta(days=90),   # 3 個月
            "security_logs": timedelta(days=2555)  # 7 年
        }
    
    def apply_data_retention(self, log_category: str):
        """應用數據保留政策"""
        if log_category in self.retention_policies:
            retention_period = self.retention_policies[log_category]
            cutoff_date = datetime.utcnow() - retention_period
            
            logger.info(
                "應用數據保留政策",
                extra={
                    "category": log_category,
                    "retention_period_days": retention_period.days,
                    "cutoff_date": cutoff_date.isoformat(),
                    "compliance_action": "data_retention"
                }
            )
    
    def anonymize_personal_data(self, log_record: dict) -> dict:
        """匿名化個人數據"""
        personal_fields = [
            'email', 'phone', 'address', 'name',
            'ssn', 'passport', 'credit_card'
        ]
        
        for field in personal_fields:
            if field in log_record:
                log_record[field] = self._anonymize_field(
                    log_record[field], field
                )
        
        log_record['_anonymized'] = True
        log_record['_anonymization_date'] = datetime.utcnow().isoformat()
        
        return log_record
    
    def generate_compliance_report(self) -> Dict:
        """生成合規報告"""
        report = {
            "report_date": datetime.utcnow().isoformat(),
            "compliance_framework": ["GDPR", "CCPA", "SOX"],
            "data_categories": list(self.retention_policies.keys()),
            "retention_policies": {
                k: v.days for k, v in self.retention_policies.items()
            },
            "anonymization_status": "active",
            "audit_trail": "enabled"
        }
        
        logger.info("合規報告生成", extra=report)
        return report
```

### 監控系統整合
```python
from prometheus_client import Counter, Histogram, Gauge
import json
import time

class MonitoringIntegration:
    """監控系統整合"""
    
    def __init__(self):
        # Prometheus 指標
        self.log_counter = Counter(
            'logs_total',
            'Total number of logs',
            ['level', 'service']
        )
        
        self.log_processing_time = Histogram(
            'log_processing_seconds',
            'Time spent processing logs'
        )
        
        self.active_connections = Gauge(
            'active_connections',
            'Number of active connections'
        )
    
    def track_log_metrics(self, level: str, service: str):
        """追蹤日誌指標"""
        self.log_counter.labels(level=level, service=service).inc()
    
    def track_processing_time(self, duration: float):
        """追蹤處理時間"""
        self.log_processing_time.observe(duration)
    
    def send_to_elasticsearch(self, log_record: dict):
        """發送到 Elasticsearch"""
        try:
            start_time = time.time()
            
            # 格式化為 ELK 格式
            elk_record = {
                "@timestamp": datetime.utcnow().isoformat(),
                "@version": "1",
                "host": "localhost",
                "message": log_record.get("message", ""),
                "level": log_record.get("level", "INFO"),
                "logger": log_record.get("logger", "default"),
                "thread": log_record.get("thread", "main"),
                "fields": log_record.get("extra", {})
            }
            
            # 發送到 Elasticsearch
            # elasticsearch_client.index(
            #     index=f"logs-{datetime.utcnow().strftime('%Y-%m-%d')}",
            #     body=elk_record
            # )
            
            processing_time = time.time() - start_time
            self.track_processing_time(processing_time)
            
        except Exception as e:
            logger.error(f"Elasticsearch 發送失敗: {e}")
    
    def setup_grafana_dashboard(self):
        """設置 Grafana 儀表板"""
        dashboard_config = {
            "dashboard": {
                "title": "Pretty-Loguru Monitoring",
                "panels": [
                    {
                        "title": "Log Volume",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "rate(logs_total[5m])",
                                "legendFormat": "{{level}} - {{service}}"
                            }
                        ]
                    },
                    {
                        "title": "Processing Time",
                        "type": "graph", 
                        "targets": [
                            {
                                "expr": "histogram_quantile(0.95, log_processing_seconds)",
                                "legendFormat": "95th percentile"
                            }
                        ]
                    }
                ]
            }
        }
        
        logger.info("Grafana 儀表板配置", extra=dashboard_config)
```

## 🏗️ 企業級部署架構

### Docker Compose 範例
```yaml
version: '3.8'
services:
  app:
    build: .
      environment:
        - LOG_LEVEL=INFO
      - LOG_PATH=/var/log/app
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    volumes:
      - ./logs:/var/log/app
    depends_on:
      - elasticsearch
      - prometheus
  
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## ➡️ 實施指南

### 階段性部署
1. **第一階段**：基礎架構建立（1-2週）
2. **第二階段**：安全和合規實施（2-3週）
3. **第三階段**：監控和報警整合（1-2週）
4. **第四階段**：優化和調優（持續進行）

### 團隊培訓
- 🎓 [企業級日誌最佳實踐培訓](../../docs/training/enterprise.md)
- 📚 [運維團隊操作手冊](../../docs/operations/manual.md)
- 🔧 [故障排除指南](../../docs/troubleshooting/enterprise.md)

---

**💼 構建企業級的日誌基礎設施！**

完善的企業級日誌系統是現代化 IT 基礎設施的核心組件。
