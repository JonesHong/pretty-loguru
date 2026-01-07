# 企業級應用範例

展示在企業級環境中部署 Pretty-Loguru 的最佳實踐，包括微服務架構、安全性、合規性和大規模日誌管理。

## 微服務架構

在微服務環境中統一日誌管理：

```python
from pretty_loguru import create_logger, LoggerConfig
import os
import socket
from typing import Optional
import uuid

class MicroserviceLogger:
    """微服務專用 Logger"""
    
    def __init__(
        self,
        service_name: str,
        service_version: str,
        environment: str = "production"
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.instance_id = self._generate_instance_id()
        
        # 創建配置
        config = LoggerConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            log_dir=f"logs/{service_name}",
            rotation="100 MB",
            retention="30 days",
            compression="zip"
        )
        
        # 創建 logger
        self.logger = create_logger(service_name, config=config)
        
        # 綁定服務資訊
        self.logger = self.logger.bind(
            service=service_name,
            version=service_version,
            environment=environment,
            instance_id=self.instance_id,
            hostname=socket.gethostname()
        )
    
    def _generate_instance_id(self) -> str:
        """生成唯一的實例 ID"""
        return f"{self.service_name}-{uuid.uuid4().hex[:8]}"
    
    def log_request(self, request_id: str, method: str, path: str):
        """記錄請求"""
        return self.logger.bind(
            request_id=request_id,
            method=method,
            path=path
        )
    
    def log_response(self, request_id: str, status_code: int, duration: float):
        """記錄響應"""
        self.logger.bind(request_id=request_id).info(
            f"Response: {status_code} ({duration:.3f}s)",
            status_code=status_code,
            duration=duration
        )
    
    def log_inter_service_call(
        self,
        target_service: str,
        operation: str,
        request_id: str
    ):
        """記錄服務間調用"""
        self.logger.bind(
            request_id=request_id,
            target_service=target_service,
            operation=operation
        ).info(f"Calling {target_service}.{operation}")

# 使用範例
# 用戶服務
user_service = MicroserviceLogger(
    service_name="user-service",
    service_version="1.2.0",
    environment="production"
)

# 訂單服務
order_service = MicroserviceLogger(
    service_name="order-service",
    service_version="2.1.0",
    environment="production"
)

# 記錄服務間通信
request_id = str(uuid.uuid4())
order_service.log_inter_service_call(
    target_service="user-service",
    operation="get_user_details",
    request_id=request_id
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/08_enterprise/microservices_logging.py)

## 安全日誌

實施安全日誌記錄和敏感資訊保護：

```python
import re
import hashlib
from typing import Any, Dict, List
from pretty_loguru import create_logger

class SecurityLogger:
    """安全日誌記錄器"""
    
    # 敏感資料模式
    SENSITIVE_PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        'api_key': r'\b[A-Za-z0-9]{32,}\b',
        'password': r'password["\']?\s*[:=]\s*["\']?[^"\']+["\']?',
    }
    
    def __init__(self, service_name: str):
        self.logger = create_logger(
            f"security_{service_name}",
            log_dir="logs/security",
            level="INFO"
        )
        self.audit_logger = create_logger(
            f"audit_{service_name}",
            log_dir="logs/audit",
            level="INFO",
            rotation="1 day",
            retention="365 days"  # 審計日誌保留一年
        )
    
    def sanitize_data(self, data: Any) -> Any:
        """清理敏感資料"""
        if isinstance(data, str):
            return self._sanitize_string(data)
        elif isinstance(data, dict):
            return {k: self.sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        else:
            return data
    
    def _sanitize_string(self, text: str) -> str:
        """清理字串中的敏感資訊"""
        for pattern_name, pattern in self.SENSITIVE_PATTERNS.items():
            text = re.sub(
                pattern,
                f"[REDACTED-{pattern_name.upper()}]",
                text,
                flags=re.IGNORECASE
            )
        return text
    
    def log_security_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        details: Optional[Dict] = None,
        severity: str = "INFO"
    ):
        """記錄安全事件"""
        # 清理敏感資料
        safe_details = self.sanitize_data(details) if details else {}
        
        # 記錄到安全日誌
        log_method = getattr(self.logger, severity.lower())
        log_method(
            f"Security Event: {event_type}",
            event_type=event_type,
            user_id=user_id,
            details=safe_details
        )
        
        # 同時記錄到審計日誌
        self.audit_logger.info(
            f"AUDIT: {event_type}",
            event_type=event_type,
            user_id=user_id,
            user_hash=hashlib.sha256(str(user_id).encode()).hexdigest() if user_id else None,
            timestamp=time.time()
        )
    
    def log_authentication(
        self,
        user_id: str,
        success: bool,
        method: str,
        ip_address: str
    ):
        """記錄認證事件"""
        event_type = "AUTH_SUCCESS" if success else "AUTH_FAILURE"
        severity = "INFO" if success else "WARNING"
        
        self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            details={
                "method": method,
                "ip_address": ip_address,
                "success": success
            },
            severity=severity
        )
    
    def log_authorization(
        self,
        user_id: str,
        resource: str,
        action: str,
        allowed: bool
    ):
        """記錄授權事件"""
        event_type = "AUTHZ_GRANTED" if allowed else "AUTHZ_DENIED"
        severity = "INFO" if allowed else "WARNING"
        
        self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            details={
                "resource": resource,
                "action": action,
                "allowed": allowed
            },
            severity=severity
        )

# 使用範例
security = SecurityLogger("api-gateway")

# 記錄認證
security.log_authentication(
    user_id="user123",
    success=True,
    method="oauth2",
    ip_address="192.168.1.100"
)

# 記錄授權
security.log_authorization(
    user_id="user123",
    resource="/api/admin",
    action="DELETE",
    allowed=False
)

# 自動清理敏感資訊
sensitive_data = {
    "user_email": "john@example.com",
    "phone": "123-456-7890",
    "api_key": "sk_test_abcdef123456789",
    "message": "User password: secretpass123"
}
security.logger.info("User data", data=security.sanitize_data(sensitive_data))
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/08_enterprise/security_logging.py)

## 合規性管理

滿足合規要求的日誌管理：

```python
from pretty_loguru import create_logger
from datetime import datetime, timedelta
import json
from cryptography.fernet import Fernet

class ComplianceLogger:
    """合規性日誌管理器"""
    
    def __init__(self, service_name: str, compliance_standards: List[str]):
        self.service_name = service_name
        self.compliance_standards = compliance_standards
        
        # 根據合規標準配置
        config = self._get_compliance_config()
        self.logger = create_logger(f"compliance_{service_name}", config=config)
        
        # 加密金鑰（實際應用中應安全存儲）
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_compliance_config(self) -> LoggerConfig:
        """根據合規標準獲取配置"""
        config = LoggerConfig(
            level="INFO",
            log_dir="logs/compliance",
            rotation="1 day"
        )
        
        # GDPR 要求
        if "GDPR" in self.compliance_standards:
            config.retention = "90 days"  # 資料最小化原則
            
        # HIPAA 要求
        if "HIPAA" in self.compliance_standards:
            config.retention = "6 years"  # 醫療記錄保留要求
            
        # PCI-DSS 要求
        if "PCI-DSS" in self.compliance_standards:
            config.retention = "1 year"
            config.compression = "zip"  # 節省存儲空間
        
        return config
    
    def log_data_access(
        self,
        user_id: str,
        data_type: str,
        operation: str,
        purpose: str,
        lawful_basis: Optional[str] = None
    ):
        """記錄資料存取（GDPR 要求）"""
        self.logger.info(
            "Data Access",
            user_id=user_id,
            data_type=data_type,
            operation=operation,
            purpose=purpose,
            lawful_basis=lawful_basis,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def log_consent(
        self,
        user_id: str,
        consent_type: str,
        granted: bool,
        version: str
    ):
        """記錄用戶同意（GDPR 要求）"""
        self.logger.info(
            "User Consent",
            user_id=user_id,
            consent_type=consent_type,
            granted=granted,
            consent_version=version,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def log_data_retention(
        self,
        data_type: str,
        records_processed: int,
        action: str
    ):
        """記錄資料保留活動"""
        self.logger.info(
            "Data Retention Activity",
            data_type=data_type,
            records_processed=records_processed,
            action=action,
            compliance_standards=self.compliance_standards
        )
    
    def encrypt_sensitive_log(self, message: str, data: Dict) -> str:
        """加密敏感日誌資料"""
        # 將資料轉換為 JSON
        json_data = json.dumps(data)
        
        # 加密
        encrypted = self.cipher.encrypt(json_data.encode())
        
        # 記錄加密的資料
        self.logger.info(
            message,
            encrypted_data=encrypted.decode(),
            encryption_method="Fernet"
        )
        
        return encrypted.decode()
    
    def generate_compliance_report(self):
        """生成合規報告"""
        report = {
            "service": self.service_name,
            "compliance_standards": self.compliance_standards,
            "report_date": datetime.utcnow().isoformat(),
            "log_retention": self._get_retention_policy(),
            "encryption_enabled": True,
            "audit_trail": "Enabled",
            "data_minimization": "GDPR" in self.compliance_standards
        }
        
        self.logger.block(
            "📊 合規性報告",
            [
                f"服務: {report['service']}",
                f"標準: {', '.join(report['compliance_standards'])}",
                f"報告日期: {report['report_date']}",
                f"日誌保留: {report['log_retention']}",
                f"加密: {'啟用' if report['encryption_enabled'] else '禁用'}",
                f"審計追蹤: {report['audit_trail']}",
                f"資料最小化: {'是' if report['data_minimization'] else '否'}"
            ],
            border_style="blue"
        )
        
        return report

# 使用範例
# GDPR 合規
gdpr_logger = ComplianceLogger("user-service", ["GDPR"])
gdpr_logger.log_data_access(
    user_id="user123",
    data_type="personal_data",
    operation="READ",
    purpose="service_provision",
    lawful_basis="contract"
)

# HIPAA 合規
hipaa_logger = ComplianceLogger("health-service", ["HIPAA"])
hipaa_logger.encrypt_sensitive_log(
    "Patient Record Access",
    {
        "patient_id": "P12345",
        "diagnosis": "Confidential",
        "treatment": "Confidential"
    }
)

# 多標準合規
multi_logger = ComplianceLogger("payment-service", ["PCI-DSS", "GDPR"])
multi_logger.generate_compliance_report()
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/08_enterprise/compliance.py)

## 集中式日誌管理

與 ELK Stack 或其他日誌聚合系統整合：

```python
from pretty_loguru import create_logger
import requests
import json
from typing import List, Dict
import queue
import threading

class CentralizedLogger:
    """集中式日誌管理器"""
    
    def __init__(
        self,
        service_name: str,
        elasticsearch_url: str,
        buffer_size: int = 1000
    ):
        self.service_name = service_name
        self.es_url = elasticsearch_url
        self.buffer = queue.Queue(maxsize=buffer_size)
        
        # 本地 logger
        self.logger = create_logger(
            service_name,
            log_dir="logs/local",
            format='{{
                "time": "{time:YYYY-MM-DD HH:mm:ss}",
                "level": "{level}",
                "service": "' + service_name + '",
                "message": "{message}",
                "extra": {extra}
            }}'
        )
        
        # 啟動背景工作線程
        self.worker_thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.worker_thread.start()
    
    def _worker(self):
        """背景工作線程，負責發送日誌到 Elasticsearch"""
        batch = []
        while True:
            try:
                # 收集批量日誌
                log_entry = self.buffer.get(timeout=1)
                batch.append(log_entry)
                
                # 批量發送
                if len(batch) >= 100 or self.buffer.empty():
                    self._send_to_elasticsearch(batch)
                    batch = []
                    
            except queue.Empty:
                if batch:
                    self._send_to_elasticsearch(batch)
                    batch = []
            except Exception as e:
                self.logger.error(f"Log worker error: {e}")
    
    def _send_to_elasticsearch(self, logs: List[Dict]):
        """發送日誌到 Elasticsearch"""
        if not logs:
            return
        
        # 準備批量請求
        bulk_data = []
        for log in logs:
            # 索引元資料
            bulk_data.append(json.dumps({
                "index": {
                    "_index": f"logs-{self.service_name}",
                    "_type": "_doc"
                }
            }))
            # 日誌資料
            bulk_data.append(json.dumps(log))
        
        # 發送請求
        try:
            response = requests.post(
                f"{self.es_url}/_bulk",
                headers={"Content-Type": "application/x-ndjson"},
                data="\n".join(bulk_data) + "\n"
            )
            
            if response.status_code != 200:
                self.logger.error(
                    f"Failed to send logs to Elasticsearch: {response.status_code}"
                )
        except Exception as e:
            self.logger.error(f"Elasticsearch connection error: {e}")
            # 可以實施重試邏輯或將日誌寫入本地檔案
    
    def log(self, level: str, message: str, **extra):
        """記錄日誌"""
        # 本地記錄
        getattr(self.logger, level)(message, **extra)
        
        # 準備發送到集中式系統
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "level": level.upper(),
            "message": message,
            **extra
        }
        
        # 添加到緩衝區
        try:
            self.buffer.put_nowait(log_entry)
        except queue.Full:
            self.logger.warning("Log buffer full, dropping log entry")

# 監控整合
class MonitoringIntegration:
    """與監控系統整合"""
    
    def __init__(self, logger, prometheus_gateway: str):
        self.logger = logger
        self.prometheus_gateway = prometheus_gateway
        
        # Prometheus 指標
        from prometheus_client import CollectorRegistry, Counter, Histogram, push_to_gateway
        
        self.registry = CollectorRegistry()
        self.log_count = Counter(
            'app_logs_total',
            'Total number of log entries',
            ['service', 'level'],
            registry=self.registry
        )
        self.error_count = Counter(
            'app_errors_total',
            'Total number of errors',
            ['service', 'error_type'],
            registry=self.registry
        )
    
    def log_with_metrics(self, level: str, message: str, **kwargs):
        """記錄日誌並更新指標"""
        # 記錄日誌
        self.logger.log(level, message, **kwargs)
        
        # 更新指標
        self.log_count.labels(
            service=self.logger.service_name,
            level=level
        ).inc()
        
        # 如果是錯誤，更新錯誤計數
        if level in ["error", "critical"]:
            error_type = kwargs.get("error_type", "unknown")
            self.error_count.labels(
                service=self.logger.service_name,
                error_type=error_type
            ).inc()
        
        # 推送指標
        try:
            push_to_gateway(
                self.prometheus_gateway,
                job=self.logger.service_name,
                registry=self.registry
            )
        except Exception as e:
            self.logger.error(f"Failed to push metrics: {e}")

# 使用範例
# 集中式日誌
central_logger = CentralizedLogger(
    service_name="api-gateway",
    elasticsearch_url="http://localhost:9200"
)

# 記錄各種級別的日誌
central_logger.log("info", "Service started", version="1.0.0")
central_logger.log("warning", "High memory usage", memory_percent=85)
central_logger.log("error", "Database connection failed", 
    error_type="ConnectionError",
    database="users_db"
)
```

[查看完整程式碼](https://github.com/JonesHong/pretty-loguru/blob/master/examples/08_enterprise/monitoring_integration.py)

## 災難恢復

實施日誌備份和恢復策略：

```python
import shutil
import tarfile
from pathlib import Path

class LogBackupManager:
    """日誌備份管理器"""
    
    def __init__(self, log_dir: str, backup_dir: str):
        self.log_dir = Path(log_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = create_logger(
            "backup_manager",
            log_dir="logs/backup"
        )
    
    def backup_logs(self, retention_days: int = 7):
        """備份日誌檔案"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"logs_backup_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name
        
        try:
            # 創建壓縮備份
            with tarfile.open(backup_path, "w:gz") as tar:
                tar.add(self.log_dir, arcname="logs")
            
            self.logger.success(
                f"Backup created: {backup_name}",
                size=f"{backup_path.stat().st_size / 1024**2:.1f}MB"
            )
            
            # 清理舊備份
            self._cleanup_old_backups(retention_days)
            
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            raise
    
    def restore_logs(self, backup_file: str, target_dir: str):
        """恢復日誌檔案"""
        backup_path = self.backup_dir / backup_file
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        try:
            # 解壓備份
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(target_dir)
            
            self.logger.success(
                f"Logs restored from: {backup_file}",
                target=target_dir
            )
            
        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            raise
```

## 下一步

- [配置管理](./configuration.md) - 深入了解配置選項
- [生產環境](./production.md) - 部署最佳實踐
- [API 文檔](../api/) - 完整 API 參考
