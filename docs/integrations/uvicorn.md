# Uvicorn 整合

pretty-loguru 與 Uvicorn ASGI 伺服器的整合，提供統一的日誌管理和進階配置選項。

## 🚀 基本設定

### 替換 Uvicorn 預設日誌

```python
# main.py
from fastapi import FastAPI
from pretty_loguru import create_logger, setup_uvicorn_logging
import uvicorn

app = FastAPI()

# 建立應用日誌記錄器
app_logger = create_logger(
    name="uvicorn_app",
    level="INFO",
    log_path="logs/app.log",
    rotation="daily",
    retention="30 days"
)

# 建立訪問日誌記錄器
access_logger = create_logger(
    name="uvicorn_access",
    level="INFO",
    log_path="logs/access.log",
    rotation="daily",
    retention="90 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    serialize=True
)

@app.get("/")
async def root():
    app_logger.info("根路徑被訪問")
    return {"message": "Hello World"}

if __name__ == "__main__":
    # 設定 Uvicorn 整合
    setup_uvicorn_logging(
        app_logger=app_logger,
        access_logger=access_logger,
        disable_existing=True  # 停用 Uvicorn 預設日誌
    )
    
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # 生產環境建議關閉
        log_config=None  # 使用 pretty-loguru 配置
    )
```

### 程式化配置

```python
import uvicorn
from pretty_loguru import create_logger
import logging

# 建立 pretty-loguru 記錄器
uvicorn_logger = create_logger(
    name="uvicorn",
    level="INFO",
    log_path="logs/uvicorn.log",
    rotation="100 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | uvicorn | {message}"
)

# 自訂 Uvicorn 日誌處理器
class PrettyLoguruHandler(logging.Handler):
    """將標準日誌重導向到 pretty-loguru"""
    
    def __init__(self, logger_instance):
        super().__init__()
        self.logger_instance = logger_instance
    
    def emit(self, record):
        # 將 logging 記錄轉換為 pretty-loguru
        message = self.format(record)
        level = record.levelname.lower()
        
        # 根據級別調用相應的方法
        if hasattr(self.logger_instance, level):
            getattr(self.logger_instance, level)(message)
        else:
            self.logger_instance.info(message)

# 配置 Uvicorn 日誌
def configure_uvicorn_logging():
    """配置 Uvicorn 使用 pretty-loguru"""
    
    # 獲取 Uvicorn 日誌記錄器
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_root = logging.getLogger("uvicorn")
    
    # 移除現有處理器
    for logger in [uvicorn_access, uvicorn_error, uvicorn_root]:
        logger.handlers.clear()
        logger.addHandler(PrettyLoguruHandler(uvicorn_logger))
        logger.setLevel(logging.INFO)
        logger.propagate = False

# 啟動配置
configure_uvicorn_logging()
```

## 🔧 進階配置

### 自訂日誌格式

```python
from pretty_loguru import create_logger
import uvicorn
import time
from typing import Dict, Any

class UvicornLogConfig:
    """Uvicorn 日誌配置類"""
    
    def __init__(self, app_name: str = "api"):
        self.app_name = app_name
        self.start_time = time.time()
        
        # 建立不同類型的日誌記錄器
        self.access_logger = self._create_access_logger()
        self.error_logger = self._create_error_logger()
        self.server_logger = self._create_server_logger()
    
    def _create_access_logger(self):
        """建立訪問日誌記錄器"""
        return create_logger(
            name=f"{self.app_name}_access",
            level="INFO",
            log_path=f"logs/{self.app_name}_access.log",
            rotation="daily",
            retention="90 days",
            # 訪問日誌專用格式
            format='{{time:YYYY-MM-DD HH:mm:ss.SSS}} | ACCESS | {message}',
            serialize=True
        )
    
    def _create_error_logger(self):
        """建立錯誤日誌記錄器"""
        return create_logger(
            name=f"{self.app_name}_error",
            level="WARNING",
            log_path=f"logs/{self.app_name}_error.log",
            rotation="50 MB",
            retention="90 days",
            backtrace=True,
            diagnose=True
        )
    
    def _create_server_logger(self):
        """建立伺服器日誌記錄器"""
        return create_logger(
            name=f"{self.app_name}_server",
            level="INFO",
            log_path=f"logs/{self.app_name}_server.log",
            rotation="daily",
            retention="30 days"
        )
    
    def log_access(self, client_ip: str, method: str, path: str, 
                   status_code: int, process_time: float, **kwargs):
        """記錄訪問日誌"""
        self.access_logger.info(
            f'{client_ip} - "{method} {path}" {status_code}',
            extra={
                "client_ip": client_ip,
                "method": method,
                "path": path,
                "status_code": status_code,
                "process_time_ms": round(process_time * 1000, 2),
                "app_name": self.app_name,
                **kwargs
            }
        )
    
    def log_server_event(self, event: str, **kwargs):
        """記錄伺服器事件"""
        uptime = time.time() - self.start_time
        
        self.server_logger.info(
            f"Server event: {event}",
            extra={
                "event": event,
                "app_name": self.app_name,
                "uptime_seconds": round(uptime, 2),
                **kwargs
            }
        )
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """記錄錯誤"""
        self.error_logger.error(
            f"Server error: {type(error).__name__}: {str(error)}",
            extra={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context or {},
                "app_name": self.app_name
            }
        )

# 使用自訂配置
log_config = UvicornLogConfig("my_api")

# 記錄不同類型的事件
log_config.log_server_event("server_started", port=8000, workers=4)
log_config.log_access("192.168.1.100", "GET", "/api/users", 200, 0.045)
log_config.log_error(ConnectionError("Database connection failed"))
```

### 與 Gunicorn 整合

```python
# gunicorn_config.py
"""
Gunicorn + Uvicorn 配置檔案
使用 pretty-loguru 統一日誌管理
"""

import multiprocessing
from pretty_loguru import create_logger
import logging
import sys

# Gunicorn 基本配置
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5

# 建立日誌記錄器
access_logger = create_logger(
    name="gunicorn_access",
    level="INFO",
    log_path="logs/gunicorn_access.log",
    rotation="daily",
    retention="90 days",
    serialize=True
)

error_logger = create_logger(
    name="gunicorn_error",
    level="INFO",
    log_path="logs/gunicorn_error.log",
    rotation="50 MB",
    retention="90 days"
)

# 自訂日誌處理
class GunicornLogger:
    """Gunicorn 日誌處理器"""
    
    def __init__(self):
        self.access_logger = access_logger
        self.error_logger = error_logger
    
    def access(self, resp, req, environ, request_time):
        """處理訪問日誌"""
        self.access_logger.info(
            f'{environ.get("REMOTE_ADDR", "-")} '
            f'"{req.method} {req.path}" '
            f'{resp.status} {getattr(resp, "sent", "-")}',
            extra={
                "remote_addr": environ.get("REMOTE_ADDR"),
                "method": req.method,
                "path": req.path,
                "query_string": req.query,
                "status": resp.status,
                "response_length": getattr(resp, "sent", 0),
                "request_time": request_time,
                "user_agent": environ.get("HTTP_USER_AGENT", "-"),
                "referer": environ.get("HTTP_REFERER", "-")
            }
        )
    
    def error(self, msg, *args, **kwargs):
        """處理錯誤日誌"""
        self.error_logger.error(msg % args if args else msg, extra=kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """處理警告日誌"""
        self.error_logger.warning(msg % args if args else msg, extra=kwargs)
    
    def info(self, msg, *args, **kwargs):
        """處理資訊日誌"""
        self.error_logger.info(msg % args if args else msg, extra=kwargs)

# 設定日誌配置
logger_class = GunicornLogger

# 關閉預設日誌
disable_redirect_access_to_syslog = True
accesslog = None
errorlog = None

# 伺服器鉤子
def on_starting(server):
    """伺服器啟動時"""
    error_logger.info("Gunicorn 伺服器啟動", extra={
        "bind": server.address,
        "workers": server.cfg.workers,
        "worker_class": server.cfg.worker_class
    })

def on_reload(server):
    """伺服器重載時"""
    error_logger.info("Gunicorn 伺服器重載")

def worker_int(worker):
    """Worker 中斷時"""
    error_logger.warning(f"Worker {worker.pid} 收到中斷信號")

def on_exit(server):
    """伺服器退出時"""
    error_logger.info("Gunicorn 伺服器關閉")
```

### 效能監控整合

```python
from fastapi import FastAPI, Request
from pretty_loguru import create_logger
import uvicorn
import time
import psutil
import asyncio
from contextlib import asynccontextmanager

# 建立效能監控日誌記錄器
perf_logger = create_logger(
    name="performance",
    level="INFO",
    log_path="logs/performance.log",
    rotation="hourly",
    serialize=True
)

class PerformanceMonitor:
    """效能監控器"""
    
    def __init__(self):
        self.request_count = 0
        self.total_response_time = 0
        self.start_time = time.time()
        self.cpu_samples = []
        self.memory_samples = []
    
    async def start_monitoring(self):
        """啟動系統監控"""
        while True:
            try:
                # 收集系統指標
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_info = psutil.virtual_memory()
                
                self.cpu_samples.append(cpu_percent)
                self.memory_samples.append(memory_info.percent)
                
                # 保持最近 60 個樣本（約 1 分鐘）
                if len(self.cpu_samples) > 60:
                    self.cpu_samples.pop(0)
                    self.memory_samples.pop(0)
                
                # 每分鐘記錄一次系統狀態
                if len(self.cpu_samples) % 60 == 0:
                    await self.log_system_metrics()
                
                await asyncio.sleep(1)
                
            except Exception as e:
                perf_logger.error(f"系統監控錯誤: {e}")
                await asyncio.sleep(5)
    
    async def log_system_metrics(self):
        """記錄系統指標"""
        if not self.cpu_samples or not self.memory_samples:
            return
        
        uptime = time.time() - self.start_time
        avg_response_time = (self.total_response_time / self.request_count 
                           if self.request_count > 0 else 0)
        
        perf_logger.info(
            "系統效能指標",
            extra={
                "uptime_seconds": round(uptime, 2),
                "total_requests": self.request_count,
                "avg_response_time_ms": round(avg_response_time * 1000, 2),
                "requests_per_second": round(self.request_count / uptime, 2),
                "cpu_usage": {
                    "current": self.cpu_samples[-1],
                    "average": round(sum(self.cpu_samples) / len(self.cpu_samples), 2),
                    "max": max(self.cpu_samples)
                },
                "memory_usage": {
                    "current": self.memory_samples[-1],
                    "average": round(sum(self.memory_samples) / len(self.memory_samples), 2),
                    "max": max(self.memory_samples)
                }
            }
        )
    
    def record_request(self, response_time: float):
        """記錄請求指標"""
        self.request_count += 1
        self.total_response_time += response_time

# 全域監控實例
monitor = PerformanceMonitor()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 啟動時
    perf_logger.info("應用程式啟動")
    
    # 啟動效能監控
    monitor_task = asyncio.create_task(monitor.start_monitoring())
    
    yield
    
    # 關閉時
    monitor_task.cancel()
    perf_logger.info("應用程式關閉")

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    """效能監控中間件"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    monitor.record_request(process_time)
    
    # 記錄慢請求
    if process_time > 1.0:
        perf_logger.warning(
            f"慢請求: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "process_time_ms": round(process_time * 1000, 2),
                "status_code": response.status_code
            }
        )
    
    return response

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "uptime": time.time() - monitor.start_time}

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        log_config=None
    )
```

## 🐳 容器化部署

### Docker 配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 建立非 root 用戶
RUN useradd -m -u 1000 appuser

# 建立日誌目錄
RUN mkdir -p /var/log/app && \
    chown -R appuser:appuser /var/log/app

# 複製應用程式
WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 啟動腳本
COPY --chown=appuser:appuser start.sh .
RUN chmod +x start.sh

EXPOSE 8000
CMD ["./start.sh"]
```

```bash
#!/bin/bash
# start.sh - 啟動腳本

set -e

echo "🚀 啟動應用程式..."

# 設定環境變數
export PYTHONPATH=/app
export LOG_LEVEL=${LOG_LEVEL:-INFO}
export WORKERS=${WORKERS:-4}

# 建立日誌目錄
mkdir -p /var/log/app

# 啟動 Uvicorn
exec uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers $WORKERS \
    --access-log \
    --log-config=null
```

### Kubernetes 部署

```yaml
# k8s-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: uvicorn-config
data:
  LOG_LEVEL: "INFO"
  WORKERS: "4"
  LOG_PATH: "/var/log/app"

---
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: uvicorn-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: uvicorn-app
  template:
    metadata:
      labels:
        app: uvicorn-app
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: uvicorn-config
        volumeMounts:
        - name: logs
          mountPath: /var/log/app
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: logs
        emptyDir: {}
```

## 🔗 相關資源

- [FastAPI 整合](./fastapi) - FastAPI 框架整合
- [自定義配置](../guide/custom-config) - 進階配置選項
- [效能最佳化](../guide/performance) - 性能調優
- [生產環境部署](../guide/production) - 部署最佳實踐
- [範例集合](../examples/integrations/) - Uvicorn 整合範例