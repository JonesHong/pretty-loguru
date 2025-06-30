# 05_production - 生產環境最佳實踐

這個目錄展示 pretty-loguru 在生產環境中的專業應用，涵蓋部署、監控、錯誤追蹤等關鍵場景。

## 🎯 學習目標

- 掌握多環境配置管理
- 學會生產級性能監控
- 實施專業錯誤追蹤
- 了解安全和合規要求
- 建立運維最佳實踐

## 📚 範例列表

### 1. deployment_logging.py - 部署環境管理
**學習重點**: 多環境配置和部署流程日誌

```bash
# 不同環境運行
APP_ENV=development python deployment_logging.py
APP_ENV=staging python deployment_logging.py  
APP_ENV=production python deployment_logging.py
```

**功能展示**:
- 自動環境檢測和配置
- 部署工作流程追蹤
- 健康檢查和驗證
- 環境間配置對比
- 安全審計日誌

**核心配置**:
```python
# 環境自動配置
env = os.getenv('APP_ENV', 'development')
config = get_environment_config(env)
logger = create_logger(f"app_{env}", **config)

# 部署流程追蹤
logger.ascii_header("DEPLOYMENT", font="slant", border_style="blue")
logger.block("部署摘要", deployment_info, border_style="green")
```

### 2. performance_monitoring.py - 性能監控
**學習重點**: 全面的性能監控和優化

```bash
python performance_monitoring.py
```

**功能展示**:
- 系統資源監控 (CPU/記憶體/磁碟)
- 應用性能監控 (APM)
- 資料庫性能追蹤
- 實時監控模擬
- 性能優化建議

**監控範例**:
```python
# 系統指標收集
metrics = collect_system_metrics()
logger.info(f"系統指標 - CPU: {metrics['cpu_percent']:.1f}%")

# 性能問題告警
if metrics['cpu_percent'] > 80:
    logger.warning(f"⚠️ CPU 使用率過高: {metrics['cpu_percent']:.1f}%")

# 應用性能追蹤
with logger.LoggerProgress() as progress:
    task = progress.add_task("性能測試", total=100)
    # 執行性能測試
```

### 3. error_tracking.py - 錯誤追蹤系統
**學習重點**: 專業的錯誤管理和分析

```bash
python error_tracking.py
```

**功能展示**:
- 結構化錯誤記錄
- 錯誤分類和嚴重程度
- 重試機制實現
- 錯誤統計和分析
- 異常處理最佳實踐

**錯誤追蹤**:
```python
# 結構化錯誤記錄
error_data = {
    "timestamp": datetime.now().isoformat(),
    "error_type": "DatabaseTimeout",
    "severity": "critical",
    "context": {"timeout": 30, "query": "SELECT..."}
}
logger.error(f"🚨 錯誤: {json.dumps(error_data, ensure_ascii=False)}")

# 重試機制
def retry_operation(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            logger.warning(f"⚠️ 重試 {attempt+1}: {e}")
```

## 🏭 生產環境配置策略

### 環境配置對比

| 環境 | 日誌級別 | 輪替策略 | 保留期間 | 適用場景 |
|------|----------|----------|----------|----------|
| development | DEBUG | 5 MB | 3 days | 本地開發調試 |
| staging | INFO | daily | 14 days | 功能測試驗證 |
| production | WARNING | daily | 90 days | 生產環境運行 |

### 服務專用配置

```python
# Web 應用服務
web_logger = create_logger(
    "web_service",
    preset="daily",
    retention="30 days",
    log_path="./logs/web"
)

# 數據處理服務
etl_logger = create_logger(
    "etl_service", 
    preset="hourly",
    retention="7 days",
    log_path="./logs/etl"
)

# 支付服務 (合規要求)
payment_logger = create_logger(
    "payment_service",
    preset="daily",
    retention="365 days",  # 一年保留
    log_path="./logs/payment"
)
```

## 📊 監控指標體系

### 系統層面監控
- **資源使用率**: CPU、記憶體、磁碟、網路
- **系統負載**: 平均負載、進程數、文件描述符
- **存儲空間**: 日誌目錄空間使用情況

### 應用層面監控  
- **響應時間**: API 端點響應時間分布
- **請求量**: 每秒請求數 (RPS)
- **錯誤率**: 4xx/5xx 錯誤比例
- **併發用戶**: 活躍用戶數量

### 業務層面監控
- **關鍵流程**: 註冊、登入、支付成功率
- **用戶行為**: 頁面瀏覽、功能使用統計
- **業務指標**: 轉換率、收入、用戶留存

## 🚨 告警策略

### 告警級別定義

```python
# 嚴重程度分級
ALERT_LEVELS = {
    "critical": {
        "color": "red",
        "response_time": "立即",
        "notification": ["phone", "email", "slack"]
    },
    "error": {
        "color": "red", 
        "response_time": "5分鐘內",
        "notification": ["email", "slack"]
    },
    "warning": {
        "color": "yellow",
        "response_time": "30分鐘內", 
        "notification": ["slack"]
    },
    "info": {
        "color": "blue",
        "response_time": "日常檢查",
        "notification": ["dashboard"]
    }
}
```

### 告警閾值設定

| 指標 | 警告閾值 | 嚴重閾值 | 檢查間隔 |
|------|----------|----------|----------|
| CPU 使用率 | 70% | 90% | 1分鐘 |
| 記憶體使用率 | 80% | 95% | 1分鐘 |
| 磁碟使用率 | 85% | 95% | 5分鐘 |
| 錯誤率 | 2% | 5% | 1分鐘 |
| 響應時間 | 500ms | 2000ms | 1分鐘 |

## 🔒 安全和合規

### 敏感資訊保護

```python
# 避免記錄敏感資訊
def safe_log_user_action(user_id, action, **kwargs):
    # 過濾敏感欄位
    safe_kwargs = {k: v for k, v in kwargs.items() 
                   if k not in ['password', 'token', 'credit_card']}
    
    logger.info(f"用戶操作: {user_id} - {action}", extra=safe_kwargs)

# 資料脫敏
def mask_sensitive_data(data):
    if 'email' in data:
        data['email'] = data['email'][:3] + "***@***.com"
    if 'phone' in data:
        data['phone'] = data['phone'][:3] + "****" + data['phone'][-2:]
    return data
```

### 合規性要求

**GDPR 合規**:
- 用戶資料訪問記錄
- 資料刪除操作追蹤
- 同意狀態變更日誌

**SOX 合規** (金融):
- 交易操作完整記錄
- 權限變更審計
- 系統配置變更追蹤

**HIPAA 合規** (醫療):
- 患者資料訪問記錄
- 醫療操作審計追蹤
- 安全事件記錄

## 📁 日誌組織結構

### 生產環境目錄規劃

```
logs/
├── applications/           # 應用服務日誌
│   ├── web/               # Web 服務
│   ├── api/               # API 服務
│   ├── worker/            # 後台任務
│   └── scheduler/         # 定時任務
├── infrastructure/        # 基礎設施日誌
│   ├── database/          # 資料庫相關
│   ├── cache/             # 快取服務
│   ├── mq/                # 訊息佇列
│   └── storage/           # 存儲服務
├── security/              # 安全審計日誌
│   ├── auth/              # 認證授權
│   ├── access/            # 訪問控制
│   └── audit/             # 安全審計
├── monitoring/            # 監控相關日誌
│   ├── performance/       # 性能監控
│   ├── alerts/            # 告警記錄
│   └── health/            # 健康檢查
└── business/              # 業務流程日誌
    ├── orders/            # 訂單處理
    ├── payments/          # 支付流程
    └── reports/           # 業務報表
```

### 檔案命名規範

```python
# 標準命名格式
"{service_name}_{env}_{date}_{sequence}.log"

# 範例
"web_service_prod_20240628_001.log"
"api_gateway_staging_20240628_14.log"  # 小時輪替
"payment_service_prod_20240628.log"     # 日輪替
```

## 🚀 部署和運維

### Docker 容器配置

```dockerfile
# Dockerfile 日誌配置
ENV LOG_PATH=/app/logs
ENV LOG_LEVEL=INFO
ENV APP_ENV=production

# 日誌目錄掛載
VOLUME ["/app/logs"]

# 日誌輪替配置
COPY logrotate.conf /etc/logrotate.d/app
```

### Kubernetes 配置

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: APP_ENV
          value: "production"
        - name: LOG_PATH
          value: "/app/logs"
        volumeMounts:
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: logs-volume
        persistentVolumeClaim:
          claimName: logs-pvc
```

### 監控集成

```python
# Prometheus 指標暴露
from prometheus_client import Counter, Histogram

# 日誌指標統計
log_counter = Counter('app_logs_total', 'Total logs', ['level', 'service'])
response_time = Histogram('app_response_time', 'Response time')

# 在日誌記錄時更新指標
def log_with_metrics(level, message, service='default'):
    logger.log(level, message)
    log_counter.labels(level=level, service=service).inc()
```

## 💡 最佳實踐總結

### 1. 配置管理
- **環境隔離**: 不同環境使用不同配置
- **配置外部化**: 使用環境變數或配置檔案
- **安全配置**: 避免硬編碼敏感資訊
- **版本控制**: 配置變更可追蹤

### 2. 性能優化
- **適當日誌級別**: 生產環境避免過多 DEBUG 日誌
- **非同步寫入**: 高頻應用使用非同步日誌
- **適當輪替**: 平衡檔案大小和 I/O 性能
- **資源監控**: 持續監控日誌對系統資源的影響

### 3. 可靠性保證
- **冗餘設計**: 關鍵日誌多重備份
- **故障恢復**: 日誌寫入失敗的降級策略
- **完整性檢查**: 定期驗證日誌檔案完整性
- **災難恢復**: 建立日誌災難恢復計劃

### 4. 運維自動化
- **自動輪替**: 使用 logrotate 或內建輪替
- **自動清理**: 定期清理過期日誌
- **自動告警**: 基於日誌的自動告警系統
- **自動分析**: 定期生成日誌分析報告

## 🔍 故障排除

### 常見問題和解決方案

**問題 1: 日誌檔案過大導致磁碟空間不足**
```python
# 解決方案: 調整輪替策略
logger = create_logger(
    "app",
    rotation="50 MB",      # 減小檔案大小
    retention="7 days"     # 縮短保留期間
)
```

**問題 2: 高頻日誌影響應用性能**
```python
# 解決方案: 使用非同步日誌和適當級別
logger = create_logger(
    "app", 
    async_mode=True,       # 非同步寫入
    level="INFO"           # 提高日誌級別
)
```

**問題 3: 日誌丟失或不完整**
```python
# 解決方案: 實施冗餘和完整性檢查
logger = create_logger(
    "app",
    backup_count=3,        # 備份檔案
    integrity_check=True   # 完整性檢查
)
```

## 📖 進階主題

### 1. 分散式日誌追蹤
- 實施 trace ID 跨服務追蹤
- 使用 ELK Stack 集中化日誌
- 建立服務拓撲視圖

### 2. 實時日誌分析
- 使用 Stream Processing 實時分析
- 實施異常檢測算法
- 建立實時告警系統

### 3. 合規性自動化
- 自動化合規性檢查
- 生成合規性報告
- 建立審計追蹤鏈

## 🔗 相關資源

- **01_basics/** - 了解基本功能
- **02_visual/** - 視覺化監控儀表板
- **03_presets/** - 配置策略選擇
- **04_fastapi/** - Web 應用集成

## ❓ 常見問題

**Q: 生產環境應該使用什麼日誌級別？**
A: 建議使用 INFO 或 WARNING，避免 DEBUG 級別影響性能。

**Q: 如何處理敏感資訊？**
A: 實施資料脫敏，避免記錄密碼、金鑰等敏感資訊。

**Q: 多長時間保留日誌合適？**
A: 根據合規要求，一般 30-90 天，金融等行業可能需要更長。

**Q: 如何實現高可用的日誌系統？**
A: 實施多重備份、冗餘存儲和故障自動恢復機制。