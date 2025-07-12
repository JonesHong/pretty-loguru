# 生產環境部署

將 pretty-loguru 部署到生產環境需要考慮可靠性、效能、安全性和可維護性。本指南提供企業級部署的最佳實踐。

## 🏗️ 部署架構

### 單機部署

```python
# production_config.py
import os
from pretty_loguru import create_logger

def create_production_logger(service_name):
    """建立生產環境日誌配置"""
    
    # 環境變數配置
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_path = os.getenv("LOG_PATH", f"/var/log/{service_name}")
    environment = os.getenv("ENVIRONMENT", "production")
    
    # 生產環境配置
    logger = create_logger(
        name=f"{service_name}_{environment}",
        level=log_level,
        log_path=f"{log_path}/{service_name}.log",
        rotation="100 MB",          # 適中的檔案大小
        retention="30 days",        # 合規要求的保留期
        compression="gzip",         # 壓縮節省空間
        enqueue=True,              # 非同步處理提升效能
        backtrace=False,           # 生產環境不需要完整追蹤
        diagnose=False,            # 關閉診斷資訊
        catch=True,                # 捕獲例外避免崩潰
        # 生產環境格式
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {process} | {name} | {function}:{line} - {message}",
        serialize=True             # JSON 格式便於日誌聚合
    )
    
    return logger

# 使用範例
app_logger = create_production_logger("webapp")
db_logger = create_production_logger("database")
cache_logger = create_production_logger("redis")
```

### 微服務部署

```python
# microservice_logging.py
import os
import socket
from pretty_loguru import create_logger

class MicroserviceLogger:
    """微服務日誌管理器"""
    
    def __init__(self, service_name, version="1.0.0"):
        self.service_name = service_name
        self.version = version
        self.instance_id = self._get_instance_id()
        self.logger = self._create_logger()
    
    def _get_instance_id(self):
        """獲取服務實例 ID"""
        hostname = socket.gethostname()
        pod_name = os.getenv("POD_NAME", hostname)
        return f"{self.service_name}-{pod_name}"
    
    def _create_logger(self):
        """建立微服務專用日誌記錄器"""
        return create_logger(
            name=self.service_name,
            level=os.getenv("LOG_LEVEL", "INFO"),
            log_path=f"/var/log/{self.service_name}/{self.service_name}.log",
            rotation="daily",
            retention="7 days",
            compression="gzip",
            enqueue=True,
            # 微服務標準格式
            format='{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", "level": "{level}", "service": "' + self.service_name + '", "instance": "' + self.instance_id + '", "version": "' + self.version + '", "message": "{message}", "extra": {extra}}',
            serialize=True
        )
    
    def info(self, message, **kwargs):
        """資訊日誌"""
        self.logger.info(message, extra=self._add_context(kwargs))
    
    def error(self, message, **kwargs):
        """錯誤日誌"""
        self.logger.error(message, extra=self._add_context(kwargs))
    
    def warning(self, message, **kwargs):
        """警告日誌"""
        self.logger.warning(message, extra=self._add_context(kwargs))
    
    def _add_context(self, extra_data):
        """添加服務上下文"""
        context = {
            "service": self.service_name,
            "instance": self.instance_id,
            "version": self.version,
            "environment": os.getenv("ENVIRONMENT", "production")
        }
        context.update(extra_data)
        return context

# 使用微服務日誌器
logger = MicroserviceLogger("user-service", "2.1.0")
logger.info("服務啟動", port=8080, health_check="/health")
```

## 🐳 容器化部署

### Docker 配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    logrotate \
    && rm -rf /var/lib/apt/lists/*

# 建立應用用戶
RUN useradd -m -u 1000 appuser

# 建立日誌目錄
RUN mkdir -p /var/log/app && \
    chown -R appuser:appuser /var/log/app

# 安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式
WORKDIR /app
COPY --chown=appuser:appuser . .

# 切換到非 root 用戶
USER appuser

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# 啟動應用
EXPOSE 8080
CMD ["python", "app.py"]
```

### Kubernetes 部署

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  labels:
    app: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: ENVIRONMENT
          value: "production"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: logs
          mountPath: /var/log/app
        - name: config
          mountPath: /app/config
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: logs
        emptyDir: {}
      - name: config
        configMap:
          name: webapp-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: webapp-config
data:
  logging.json: |
    {
      "log_level": "INFO",
      "rotation": "100 MB",
      "retention": "7 days",
      "compression": "gzip"
    }
```

## 📊 監控與觀測

### 日誌聚合

```python
# log_aggregation.py
import json
from datetime import datetime
from pretty_loguru import create_logger

class LogAggregator:
    """日誌聚合器 - 與 ELK Stack 整合"""
    
    def __init__(self, service_name):
        self.service_name = service_name
        self.logger = create_logger(
            name=f"aggregated_{service_name}",
            level="INFO",
            log_path=f"/var/log/aggregated/{service_name}.log",
            rotation="hourly",
            retention="24 hours",
            # ELK 友好的格式
            format='{"@timestamp": "{time:YYYY-MM-DDTHH:mm:ss.SSSZ}", "@version": "1", "host": "{host}", "level": "{level}", "logger_name": "{name}", "thread": "{thread}", "message": "{message}", "fields": {extra}}',
            serialize=True
        )
    
    def log_request(self, method, path, status_code, response_time, user_id=None):
        """記錄 HTTP 請求"""
        self.logger.info(
            f"{method} {path} - {status_code}",
            extra={
                "event_type": "http_request",
                "http": {
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "response_time_ms": round(response_time * 1000, 2)
                },
                "user_id": user_id,
                "service": self.service_name
            }
        )
    
    def log_database_query(self, query_type, table, duration, rows_affected=None):
        """記錄資料庫查詢"""
        self.logger.info(
            f"DB {query_type} on {table}",
            extra={
                "event_type": "database_query",
                "database": {
                    "query_type": query_type,
                    "table": table,
                    "duration_ms": round(duration * 1000, 2),
                    "rows_affected": rows_affected
                },
                "service": self.service_name
            }
        )
    
    def log_business_event(self, event_name, event_data=None):
        """記錄業務事件"""
        self.logger.info(
            f"Business event: {event_name}",
            extra={
                "event_type": "business_event",
                "event_name": event_name,
                "event_data": event_data or {},
                "service": self.service_name
            }
        )

# 使用日誌聚合器
aggregator = LogAggregator("user-service")

# 記錄不同類型的事件
aggregator.log_request("GET", "/api/users/123", 200, 0.045, user_id="user_123")
aggregator.log_database_query("SELECT", "users", 0.023, rows_affected=1)
aggregator.log_business_event("user_login", {"login_method": "oauth", "provider": "google"})
```

### 指標收集

```python
# metrics_collection.py
import time
from collections import defaultdict, Counter
from pretty_loguru import create_logger

class MetricsCollector:
    """指標收集器"""
    
    def __init__(self):
        self.logger = create_logger(
            name="metrics",
            level="INFO",
            log_path="/var/log/metrics/metrics.log",
            rotation="hourly",
            format='{"timestamp": "{time:YYYY-MM-DDTHH:mm:ss.SSSZ}", "metric_type": "application", "data": {extra}}',
            serialize=True
        )
        
        # 指標存儲
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.timers = {}
    
    def increment_counter(self, name, labels=None, value=1):
        """增加計數器"""
        key = f"{name}:{labels or {}}"
        self.counters[key] += value
        
        self.logger.info(
            f"Counter {name} incremented",
            extra={
                "metric_name": name,
                "metric_type": "counter",
                "value": value,
                "labels": labels or {},
                "total": self.counters[key]
            }
        )
    
    def set_gauge(self, name, value, labels=None):
        """設定量表值"""
        key = f"{name}:{labels or {}}"
        self.gauges[key] = value
        
        self.logger.info(
            f"Gauge {name} set",
            extra={
                "metric_name": name,
                "metric_type": "gauge",
                "value": value,
                "labels": labels or {}
            }
        )
    
    def record_histogram(self, name, value, labels=None):
        """記錄直方圖值"""
        key = f"{name}:{labels or {}}"
        self.histograms[key].append(value)
        
        # 計算統計值
        values = self.histograms[key]
        count = len(values)
        sum_val = sum(values)
        avg_val = sum_val / count
        
        self.logger.info(
            f"Histogram {name} recorded",
            extra={
                "metric_name": name,
                "metric_type": "histogram",
                "value": value,
                "count": count,
                "sum": sum_val,
                "average": avg_val,
                "labels": labels or {}
            }
        )
    
    def start_timer(self, name, labels=None):
        """開始計時"""
        key = f"{name}:{labels or {}}"
        self.timers[key] = time.time()
    
    def end_timer(self, name, labels=None):
        """結束計時並記錄"""
        key = f"{name}:{labels or {}}"
        if key in self.timers:
            duration = time.time() - self.timers[key]
            del self.timers[key]
            self.record_histogram(f"{name}_duration", duration, labels)
            return duration
        return None

# 使用指標收集器
metrics = MetricsCollector()

# 記錄各種指標
metrics.increment_counter("http_requests_total", {"method": "GET", "status": "200"})
metrics.set_gauge("active_connections", 42)
metrics.start_timer("request_processing", {"endpoint": "/api/users"})
time.sleep(0.1)  # 模擬處理時間
metrics.end_timer("request_processing", {"endpoint": "/api/users"})
```

## 🔒 安全配置

### 日誌安全

```python
# secure_logging.py
import hashlib
import re
from pretty_loguru import create_logger

class SecureLogger:
    """安全日誌記錄器"""
    
    def __init__(self, service_name):
        self.service_name = service_name
        self.sensitive_patterns = [
            r'password\s*[=:]\s*["\']([^"\']+)["\']',
            r'token\s*[=:]\s*["\']([^"\']+)["\']',
            r'api[_-]?key\s*[=:]\s*["\']([^"\']+)["\']',
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # 信用卡號
            r'\b\d{3}-\d{2}-\d{4}\b'  # SSN
        ]
        
        self.logger = create_logger(
            name=f"secure_{service_name}",
            level="INFO",
            log_path=f"/var/log/secure/{service_name}.log",
            rotation="daily",
            retention="90 days",  # 安全日誌長期保留
            compression="gzip",
            # 確保檔案權限安全
            enqueue=True
        )
    
    def sanitize_message(self, message):
        """清理敏感資訊"""
        sanitized = message
        
        for pattern in self.sensitive_patterns:
            sanitized = re.sub(pattern, r'***REDACTED***', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def hash_pii(self, data):
        """雜湊個人識別資訊"""
        if isinstance(data, str):
            return hashlib.sha256(data.encode()).hexdigest()[:16]
        return data
    
    def log_security_event(self, event_type, user_id, details=None):
        """記錄安全事件"""
        sanitized_details = {}
        if details:
            for key, value in details.items():
                if key in ['user_id', 'email', 'ip_address']:
                    sanitized_details[key] = self.hash_pii(str(value))
                else:
                    sanitized_details[key] = self.sanitize_message(str(value))
        
        self.logger.warning(
            f"Security event: {event_type}",
            extra={
                "event_type": event_type,
                "user_id": self.hash_pii(user_id),
                "details": sanitized_details,
                "service": self.service_name
            }
        )
    
    def log_audit_event(self, action, resource, user_id, before_state=None, after_state=None):
        """記錄審計事件"""
        self.logger.info(
            f"Audit: {action} on {resource}",
            extra={
                "event_type": "audit",
                "action": action,
                "resource": resource,
                "user_id": self.hash_pii(user_id),
                "before_state": before_state,
                "after_state": after_state,
                "service": self.service_name
            }
        )

# 使用安全日誌記錄器
secure_logger = SecureLogger("auth-service")

secure_logger.log_security_event(
    "login_attempt",
    "user@example.com",
    {"ip_address": "192.168.1.100", "user_agent": "Mozilla/5.0..."}
)

secure_logger.log_audit_event(
    "update_profile",
    "user_profile",
    "user@example.com",
    before_state={"name": "John"},
    after_state={"name": "John Doe"}
)
```

## 🚨 錯誤處理與恢復

### 容錯機制

```python
# fault_tolerance.py
import time
import threading
from queue import Queue, Empty
from pretty_loguru import create_logger

class FaultTolerantLogger:
    """容錯日誌記錄器"""
    
    def __init__(self, service_name, backup_enabled=True):
        self.service_name = service_name
        self.backup_enabled = backup_enabled
        self.failed_logs = Queue()
        self.retry_thread = None
        
        # 主要日誌記錄器
        try:
            self.primary_logger = create_logger(
                name=f"primary_{service_name}",
                level="INFO",
                log_path=f"/var/log/{service_name}/{service_name}.log",
                rotation="100 MB",
                retention="30 days",
                compression="gzip",
                enqueue=True
            )
        except Exception as e:
            print(f"主要日誌記錄器初始化失敗: {e}")
            self.primary_logger = None
        
        # 備份日誌記錄器（記憶體或備用位置）
        if backup_enabled:
            try:
                self.backup_logger = create_logger(
                    name=f"backup_{service_name}",
                    level="INFO",
                    log_path=f"/tmp/{service_name}_backup.log",
                    rotation="50 MB",
                    retention="7 days"
                )
            except Exception as e:
                print(f"備份日誌記錄器初始化失敗: {e}")
                self.backup_logger = None
        
        # 啟動重試機制
        self._start_retry_mechanism()
    
    def log(self, level, message, **kwargs):
        """容錯日誌記錄"""
        log_entry = {
            "level": level,
            "message": message,
            "extra": kwargs,
            "timestamp": time.time()
        }
        
        try:
            # 嘗試使用主要日誌記錄器
            if self.primary_logger:
                getattr(self.primary_logger, level.lower())(message, **kwargs)
                return True
        except Exception as e:
            print(f"主要日誌記錄失敗: {e}")
            # 將失敗的日誌加入重試佇列
            self.failed_logs.put(log_entry)
        
        try:
            # 使用備份日誌記錄器
            if self.backup_logger:
                getattr(self.backup_logger, level.lower())(
                    f"[BACKUP] {message}",
                    **kwargs
                )
                return True
        except Exception as e:
            print(f"備份日誌記錄失敗: {e}")
        
        # 所有日誌記錄器都失敗，輸出到控制台
        print(f"[{level}] {message} | Extra: {kwargs}")
        return False
    
    def info(self, message, **kwargs):
        return self.log("INFO", message, **kwargs)
    
    def error(self, message, **kwargs):
        return self.log("ERROR", message, **kwargs)
    
    def warning(self, message, **kwargs):
        return self.log("WARNING", message, **kwargs)
    
    def _start_retry_mechanism(self):
        """啟動重試機制"""
        def retry_worker():
            while True:
                try:
                    # 從失敗佇列中取出日誌
                    log_entry = self.failed_logs.get(timeout=30)
                    
                    # 重試記錄日誌
                    if self.primary_logger:
                        try:
                            getattr(self.primary_logger, log_entry["level"].lower())(
                                f"[RETRY] {log_entry['message']}",
                                **log_entry["extra"]
                            )
                        except Exception:
                            # 重試失敗，重新加入佇列（限制重試次數）
                            retry_count = log_entry.get("retry_count", 0)
                            if retry_count < 3:
                                log_entry["retry_count"] = retry_count + 1
                                self.failed_logs.put(log_entry)
                
                except Empty:
                    # 沒有待重試的日誌，繼續等待
                    continue
                except Exception as e:
                    print(f"重試機制錯誤: {e}")
        
        self.retry_thread = threading.Thread(target=retry_worker, daemon=True)
        self.retry_thread.start()

# 使用容錯日誌記錄器
fault_tolerant_logger = FaultTolerantLogger("critical-service")

# 即使在磁碟空間不足或權限問題時也能記錄日誌
fault_tolerant_logger.info("應用程式啟動", version="2.0.0")
fault_tolerant_logger.error("處理請求時發生錯誤", error_code=500, user_id="user123")
```

## 📋 部署檢查清單

### 部署前檢查

```bash
#!/bin/bash
# pre_deployment_check.sh

echo "🔍 生產環境部署檢查"
echo "===================="

# 1. 檢查磁碟空間
echo "1. 檢查磁碟空間..."
df -h /var/log
if [ $(df /var/log | tail -1 | awk '{print $5}' | sed 's/%//') -gt 80 ]; then
    echo "❌ 警告：日誌磁碟空間使用率超過 80%"
else
    echo "✅ 磁碟空間充足"
fi

# 2. 檢查日誌目錄權限
echo "2. 檢查日誌目錄權限..."
if [ -w /var/log/app ]; then
    echo "✅ 日誌目錄可寫"
else
    echo "❌ 警告：日誌目錄不可寫"
fi

# 3. 檢查環境變數
echo "3. 檢查環境變數..."
required_vars=("LOG_LEVEL" "ENVIRONMENT" "SERVICE_NAME")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ 警告：缺少環境變數 $var"
    else
        echo "✅ $var = ${!var}"
    fi
done

# 4. 檢查日誌輪換配置
echo "4. 檢查 logrotate 配置..."
if [ -f /etc/logrotate.d/app ]; then
    echo "✅ logrotate 配置存在"
else
    echo "❌ 警告：缺少 logrotate 配置"
fi

# 5. 測試日誌寫入
echo "5. 測試日誌寫入..."
python3 -c "
from pretty_loguru import create_logger
try:
    logger = create_logger('test', log_path='/var/log/app/test.log')
    logger.info('部署測試')
    print('✅ 日誌寫入測試成功')
except Exception as e:
    print(f'❌ 日誌寫入測試失敗: {e}')
"

echo "===================="
echo "部署檢查完成"
```

### 生產環境配置範本

```python
# production_template.py
"""
生產環境配置範本
適用於大多數 Web 應用程式和微服務
"""

import os
from pretty_loguru import create_logger

class ProductionConfig:
    """生產環境配置類"""
    
    def __init__(self):
        self.service_name = os.getenv("SERVICE_NAME", "app")
        self.environment = os.getenv("ENVIRONMENT", "production")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_path = os.getenv("LOG_PATH", f"/var/log/{self.service_name}")
        
    def create_application_logger(self):
        """建立應用程式日誌記錄器"""
        return create_logger(
            name=f"{self.service_name}_app",
            level=self.log_level,
            log_path=f"{self.log_path}/application.log",
            rotation="100 MB",
            retention="30 days",
            compression="gzip",
            enqueue=True,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name} | {function}:{line} - {message}",
            catch=True
        )
    
    def create_access_logger(self):
        """建立訪問日誌記錄器"""
        return create_logger(
            name=f"{self.service_name}_access",
            level="INFO",
            log_path=f"{self.log_path}/access.log",
            rotation="daily",
            retention="90 days",
            compression="gzip",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}",
            serialize=True
        )
    
    def create_error_logger(self):
        """建立錯誤日誌記錄器"""
        return create_logger(
            name=f"{self.service_name}_error",
            level="WARNING",
            log_path=f"{self.log_path}/error.log",
            rotation="50 MB",
            retention="90 days",
            compression="gzip",
            backtrace=True,
            diagnose=True
        )
    
    def create_audit_logger(self):
        """建立審計日誌記錄器"""
        return create_logger(
            name=f"{self.service_name}_audit",
            level="INFO",
            log_path=f"{self.log_path}/audit.log",
            rotation="daily",
            retention="2555 days",  # 7年合規要求
            compression="gzip",
            format='{"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", "service": "' + self.service_name + '", "event": "audit", "message": "{message}", "data": {extra}}',
            serialize=True
        )

# 使用配置
config = ProductionConfig()
app_logger = config.create_application_logger()
access_logger = config.create_access_logger()
error_logger = config.create_error_logger()
audit_logger = config.create_audit_logger()

# 記錄不同類型的日誌
app_logger.info("應用程式啟動完成")
access_logger.info("用戶訪問", extra={"user_id": "123", "endpoint": "/api/users"})
error_logger.error("資料庫連接失敗", extra={"database": "postgres", "error": "timeout"})
audit_logger.info("用戶資料更新", extra={"user_id": "123", "action": "update_profile"})
```

## 🔗 相關資源

- [效能最佳化](./performance) - 性能調優指南
- [自定義配置](./custom-config) - 詳細配置選項
- [日誌輪換](./log-rotation) - 檔案管理策略
- [範例集合](../examples/production/) - 生產環境範例