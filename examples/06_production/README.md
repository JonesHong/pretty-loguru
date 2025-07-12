# 🏭 06_production - 生產環境最佳實踐

歡迎來到生產環境學習！這個模組將教您如何在真實的生產環境中部署和維運 pretty-loguru，包括性能優化、錯誤監控和維運自動化。

## 🎯 學習目標

完成本節後，您將：
- ✅ 掌握生產環境的日誌配置策略
- ✅ 學會性能監控和調優技巧
- ✅ 建立完整的錯誤追蹤體系
- ✅ 實現日誌聚合和分析流程

## 📚 範例列表（建議順序）

### 🚀 Step 1: deployment_logging.py - 部署環境配置
**⏱️ 預估時間：15分鐘**

```bash
python deployment_logging.py
```

**學習重點**：
- 不同環境的配置差異
- 安全性和權限管理
- 部署流程的日誌記錄
- 配置驗證和健康檢查

### 📊 Step 2: performance_monitoring.py - 性能監控
**⏱️ 預估時間：20分鐘**

```bash
python performance_monitoring.py
```

**學習重點**：
- 應用性能指標記錄
- 資源使用監控
- 回應時間追蹤
- 瓶頸識別和分析

### 🚨 Step 3: error_tracking.py - 錯誤追蹤系統
**⏱️ 預估時間：18分鐘**

```bash
python error_tracking.py
```

**學習重點**：
- 結構化錯誤記錄
- 錯誤分級和報警
- 錯誤趨勢分析
- 自動化錯誤處理

### 📈 Step 4: log_aggregation.py - 日誌聚合
**⏱️ 預估時間：25分鐘**

```bash
python log_aggregation.py
```

**學習重點**：
- 多服務日誌聚合
- 日誌格式標準化
- 搜索和分析工具
- 數據導出和備份

## 🎮 生產環境模擬

```bash
# 模擬生產環境負載
python deployment_logging.py &
python performance_monitoring.py &
python error_tracking.py &

# 生成測試負載
for i in {1..100}; do
    curl -s http://localhost:8000/api/test > /dev/null &
done

# 檢查日誌輸出
tail -f ./logs/production/*.log
```

## 💡 生產環境核心原則

### 配置分離
```python
import os
from pretty_loguru import create_logger

# 環境變數驅動配置
logger = create_logger(
    name=os.getenv("SERVICE_NAME", "myapp"),
    log_path=os.getenv("LOG_PATH", "/var/log/myapp"),
    level=os.getenv("LOG_LEVEL", "INFO"),
    rotation=os.getenv("LOG_ROTATION", "100MB"),
    retention=os.getenv("LOG_RETENTION", "30 days"),
    compression=os.getenv("LOG_COMPRESSION", "gz")
)
```

### 結構化日誌
```python
# 生產環境必須使用結構化日誌
logger.info(
    "用戶登入",
    extra={
        "user_id": user.id,
        "ip_address": request.client.host,
        "user_agent": request.headers.get("User-Agent"),
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session.id
    }
)
```

### 敏感資訊處理
```python
def sanitize_log_data(data):
    """清理敏感資訊"""
    sensitive_fields = ['password', 'token', 'secret', 'key']
    
    if isinstance(data, dict):
        return {
            k: '[REDACTED]' if k.lower() in sensitive_fields else v
            for k, v in data.items()
        }
    return data

logger.info("API 請求", extra=sanitize_log_data(request_data))
```

## 🔧 維運自動化

### 日誌輪替監控
```python
import psutil
import shutil

def monitor_log_space():
    """監控日誌空間使用"""
    log_path = "/var/log/myapp"
    usage = shutil.disk_usage(log_path)
    
    used_percent = (usage.used / usage.total) * 100
    
    if used_percent > 80:
        logger.warning(
            "磁碟空間不足",
            extra={
                "path": log_path,
                "used_percent": used_percent,
                "free_gb": usage.free / (1024**3)
            }
        )
```

### 健康檢查端點
```python
from fastapi import FastAPI

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    try:
        # 檢查日誌系統
        logger.info("健康檢查", extra={"check_type": "health"})
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error("健康檢查失敗", extra={"error": str(e)})
        return {"status": "unhealthy", "error": str(e)}
```

## 📊 監控和報警

### 關鍵指標監控
```python
# 錯誤率監控
error_count = 0
total_requests = 0

@app.middleware("http")
async def monitor_errors(request, call_next):
    global error_count, total_requests
    total_requests += 1
    
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            error_count += 1
            
        # 每 100 個請求記錄一次統計
        if total_requests % 100 == 0:
            error_rate = (error_count / total_requests) * 100
            logger.info(
                "錯誤率統計",
                extra={
                    "error_rate": error_rate,
                    "total_requests": total_requests,
                    "error_count": error_count
                }
            )
            
        return response
    except Exception as e:
        error_count += 1
        logger.error("請求處理失敗", extra={"error": str(e)})
        raise
```

## ➡️ 下一步選擇

### 🔬 進階功能
**建議路徑**：[07_advanced](../07_advanced/) - 自定義開發和優化

### 💼 企業場景
**建議路徑**：[08_enterprise](../08_enterprise/) - 微服務和大規模部署

### 📚 深入學習
**建議閱讀**：[生產環境指南](../../docs/guide/production.md)

## 📖 相關資源

- 🔧 [Docker 部署指南](../../docs/deployment/docker.md)
- ☸️ [Kubernetes 配置](../../docs/deployment/kubernetes.md)
- 📊 [監控系統整合](../../docs/integrations/monitoring.md)

---

**🏭 讓您的應用在生產環境中穩定可靠！**

完善的日誌體系是生產環境穩定運行的重要保障。