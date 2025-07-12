# Pretty Loguru 重構遷移指南

## 版本變更說明

本次重構包含以下重要變更：

### 1. 移除 Proxy 模式

**原因**：Proxy 模式存在遞歸 bug 且增加了不必要的複雜度。

**影響**：
- `use_proxy` 參數已被移除
- 無法自動更新 logger 變數引用

**遷移方案**：

```python
# ❌ 舊方式（已移除）
logger = create_logger("app", use_proxy=True)
config.apply_to("app")  # Proxy 會自動更新

# ✅ 新方式
logger = create_logger("app")
logger = config.apply_to("app")  # 需要手動更新變數
```

### 2. LoggerConfig.apply_to() 行為變更

**變更**：`apply_to()` 現在只能更新現有 logger，不再自動創建新 logger。

```python
# ❌ 舊行為
config = LoggerConfig(level="INFO")
logger = config.apply_to("new_logger")  # 自動創建

# ✅ 新行為
config = LoggerConfig(level="INFO")
logger = create_logger("new_logger", config=config)  # 明確創建
config.apply_to("new_logger")  # 只能更新現有的
```

### 3. create_logger() 支援 LoggerConfig

**新功能**：`create_logger()` 現在可以直接接受 `LoggerConfig` 物件。

```python
# ✅ 新功能
config = LoggerConfig(level="INFO", log_path="logs")
logger = create_logger("app", config=config)

# ✅ 配置 + 覆寫
logger = create_logger("debug_app", config=config, level="DEBUG")
```

## 遷移步驟

### 步驟 1：移除 use_proxy 參數

搜尋並替換所有使用 `use_proxy` 的程式碼：

```python
# 搜尋
create_logger(..., use_proxy=True)

# 替換為
create_logger(...)
```

### 步驟 2：更新 apply_to() 使用方式

```python
# 舊方式
logger = config.apply_to("logger_name")

# 新方式（如果 logger 不存在）
logger = create_logger("logger_name", config=config)

# 新方式（如果 logger 已存在）
logger = config.apply_to("logger_name")  # 記得更新變數
```

### 步驟 3：檢查 logger 是否存在

使用新的輔助方法：

```python
if LoggerConfig.logger_exists("logger_name"):
    logger = config.apply_to("logger_name")
else:
    logger = create_logger("logger_name", config=config)
```

## 最佳實踐

### 1. 一次性配置

如果不需要動態更新配置，建議一次性設定：

```python
config = ConfigTemplates.production()
logger = create_logger("app", config=config)
```

### 2. 手動管理引用

當需要更新配置時，記得更新變數引用：

```python
# 更新配置
new_config = LoggerConfig(level="DEBUG")
logger = new_config.apply_to("app")  # 重新賦值
```

### 3. 使用配置模板

利用內建的配置模板簡化設定：

```python
# 開發環境
dev_logger = create_logger("dev", config=ConfigTemplates.development())

# 生產環境
prod_logger = create_logger("prod", config=ConfigTemplates.production())
```

## 常見問題

### Q: 為什麼移除 Proxy 模式？

A: Proxy 模式存在以下問題：
1. 遞歸 bug 導致無法正常工作
2. 增加了不必要的複雜度
3. 使用場景很少

### Q: 如何動態更新 logger 配置？

A: 使用 `apply_to()` 並手動更新變數引用：

```python
logger = config.apply_to("logger_name")
```

### Q: apply_to() 為什麼不能創建新 logger？

A: 為了遵循單一職責原則：
- `create_logger()` 負責創建
- `apply_to()` 負責更新
- 避免方法行為的歧義

## 範例程式碼

完整範例請參考：
- `examples/04_configuration/using_logger_config.py`

## 需要協助？

如有問題，請查閱：
- API 文檔
- GitHub Issues
- 範例程式碼