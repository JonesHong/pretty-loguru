# Performance Optimization

In most services, logging bottlenecks are usually not the logger itself, but:

- Unnecessary string building and heavy serialization
- Synchronous I/O (writes, compression, frequent rotations)
- High-volume low-value logs on hot paths

pretty-loguru wraps common loguru patterns, so performance tuning is mainly about reducing output and reducing I/O pressure.

## ✅ Key knobs in pretty-loguru

- `level`: simplest way to reduce cost (production often avoids `DEBUG`)
- `log_dir`: **directory** where log files are stored; if omitted, you get console-only
- `rotation` / `retention` / `compression`: overly frequent rotation increases I/O and CPU cost
- `use_native_format`: use loguru native format (less custom formatting / extra handling)
- `serialize`: write JSON logs to file (great for Filebeat/Promtail parsing)
- `start_cleaner` + `cleaner_include_patterns` / `cleaner_exclude_patterns`: avoid scanning unrelated files
- `loki_enabled`: optional direct Loki push (agent-based shipping is often preferred)

## ⚡ Simple benchmark (repeatable)

```python
import time
from pretty_loguru import create_logger

def bench(logger, iterations: int = 20000) -> None:
    start = time.perf_counter()
    for i in range(iterations):
        logger.info("bench message {i}", i=i)
    elapsed = time.perf_counter() - start
    print(f"{iterations} ops, {elapsed:.3f}s, {iterations/elapsed:.0f} ops/s")

# Console-only (no log_dir)
console_logger = create_logger("bench_console", level="INFO")

# File logging (log_dir is a directory)
file_logger = create_logger("bench_file", level="INFO", log_dir="logs/bench")

bench(console_logger)
bench(file_logger)
```

## 🧠 Code-level habits

### 1) Avoid expensive work for disabled levels

loguru supports lazy evaluation:

```python
import time
from pretty_loguru import create_logger

logger = create_logger("app", level="INFO")

def expensive():
    time.sleep(0.1)
    return {"heavy": "payload"}

logger.opt(lazy=True).debug("expensive payload: {payload}", payload=expensive)
```

### 2) Prefer structured fields over manual concatenation

```python
logger.info("user login: user_id={user_id} ip={ip}", user_id=123, ip="1.2.3.4")
```

For ELK/Loki pipelines, `serialize=True` plus an agent (Filebeat/Promtail) is usually the most robust approach.

## 💾 I/O and rotation strategy

- **Rotate less often**: bigger `rotation` (e.g. `"500 MB"`) reduces rotation/compression churn
- **Compression costs CPU**: for high-throughput services, consider disabling `compression`
- **Console-only is often cheaper**: keep hot-path logs minimal (or only WARNING/ERROR)

## 🧹 Cleaner notes

When `start_cleaner=True`, a background cleaner scans files under `log_dir`:

- Use `cleaner_include_patterns` (e.g. `["*.log", "*.log.*"]`) to limit scope
- Use `cleaner_exclude_patterns` (e.g. `["*.lock"]`) to skip temporary/lock files
- Keep `verbose=False` in production

## 🧩 Loki / ELK performance choice (recommended)

In most cases, prefer “file output + agent shipping”:

- ELK: `serialize=True` + Filebeat (or Fluent Bit)
- Loki: `serialize=True` + Promtail (or Grafana Agent)

Use `loki_enabled=True` direct push only if you are comfortable with network reliability, retry/backpressure behavior, and failure modes.
