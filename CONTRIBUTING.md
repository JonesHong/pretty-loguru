# 貢獻 / 開發指南（uv）

本專案建議使用 `uv` 管理開發環境，並以 `uv.lock` 固定依賴，降低「在我電腦可以、在你電腦不行」的風險。

---

## 1) 建立開發環境

```bash
uv sync --group dev
```

---

## 2) 執行測試

```bash
uv run pytest -q
```

---

## 3) 重新產生快照（對照文件/API）

```bash
uv run python snapshot.py
```

---

## 4) 更新 lock（依賴升級）

```bash
uv lock --upgrade
```

