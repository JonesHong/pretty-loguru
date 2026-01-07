# Observability Cookbook（Loki / Grafana / ELK）

此資料夾是「可跑的範例環境」與「操作手冊」，目的在於快速驗證：

- pretty-loguru 寫檔 / JSON 序列化是否能被收集
- Loki / Grafana 是否能看到結果
- ELK（Filebeat）是否能吃到 log 檔

> 注意：`examples/observability/` 不屬於 core contract（它是範例/工具環境），這裡的 compose/config 可以自由演進。

---

## 1) Loki + Grafana（推薦先跑這個）

### 啟動

在專案根目錄執行：

```bash
docker compose -f examples/observability/docker-compose.yml up -d
```

### Grafana

- 預設網址：`http://localhost:3000`
- 預設帳密（依 compose 而定）：常見為 `admin / admin`

資料來源：

- `examples/observability/grafana/provisioning/datasources/loki.yml` 會自動把 Loki datasource provision 進去

---

## 2) 送出/產生日誌

### Loki 直推（示意）

```bash
python examples/observability/demo_send_logs.py
```

### ELK（示意）

```bash
python examples/observability/demo_send_logs_elk.py
```

---

## 3) ELK（進階/示意）

啟動（示意）：

```bash
docker compose -f examples/observability/elk/docker-compose.yml up -d
```

Filebeat 設定：

- `examples/observability/elk/filebeat.yml`

小提醒：
- `examples/observability/elk/filebeat.yml` 預設只收集 `/logs/elk-events/**/*.log`，用來降低雜訊（避免把所有 `.log` 全部送進 ES）。
