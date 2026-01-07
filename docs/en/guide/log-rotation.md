# Log Rotation

pretty-loguru delegates file rotation to loguru’s file sink. Rotation/retention/compression only apply when file output is enabled (i.e. `log_dir` is set).

## ✅ Key rule: `log_dir` is a directory

- `log_dir` is the **destination directory** for log files
- If `log_dir` is not set, you get console-only output and rotation settings do not apply

## 🚀 Basic usage

### Size-based rotation

```python
from pretty_loguru import create_logger

logger = create_logger(
    name="size_rotation",
    log_dir="logs/app",
    rotation="100 MB",
    retention="30 days",
    compression="gz",
)
```

### Time-based rotation (common)

For example, rotate daily at midnight:

```python
logger = create_logger(
    name="daily_midnight",
    log_dir="logs/app",
    rotation="00:00",
    retention="30 days",
    compression="gz",
)
```

## 🧩 Use `ConfigTemplates` (recommended)

pretty-loguru ships rotation templates that also include a naming/renaming strategy:

```python
from pretty_loguru import create_logger
from pretty_loguru.addons import ConfigTemplates

config = ConfigTemplates.daily()  # daily/hourly/weekly/monthly/minute
create_logger("my_app", config=config, component_name="my_app")
config.apply_to("my_app")
```

### Template naming concept

- The “current” file is typically a stable name (e.g. `[{component}]daily_latest.temp.log`)
- When rotation happens, the rotated file is renamed to a date/week/month-based filename (e.g. `[{component}]20250113.log`)

## 📁 File naming and `component_name`

Without a preset, the default filename is roughly:

- `[{name}]_{timestamp}.log`

Use `component_name` to make filenames reflect your service identity:

```python
logger = create_logger(
    name="worker",
    component_name="payment-worker",
    log_dir="logs/payment",
    rotation="50 MB",
)
```

## ⚠️ Practical tips

- Avoid very small `rotation` for high-volume services (rotation/compression churn)
- Compression costs CPU; disable `compression` if CPU/IO is constrained
- For ELK/Loki pipelines, consider `serialize=True` + an agent (Filebeat/Promtail)
