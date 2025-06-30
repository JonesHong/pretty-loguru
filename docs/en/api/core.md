# Core Module API

The `pretty_loguru` core module provides the foundational infrastructure for the logging system, including configuration management, handler setup, and underlying initialization logic. These components work together to ensure the stability and scalability of the logging system.

## Overview

The core module consists of the following main parts:

- **`config.py`**: Defines the `LoggerConfig` data class for storing all logging-related configurations.
- **`base.py`**: Contains core functions like `configure_logger`, responsible for initializing the logger based on configuration.
- **`handlers.py`**: Manages log destination (console/file) filtering and filename formatting.
- **`presets.py`**: Provides preset configuration templates to simplify common scenario setups.

---

## `config.py` - Logging Configuration

### `LoggerConfig`

This is a `dataclass` that centrally manages all configuration options for a single logger instance.

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable

@dataclass
class LoggerConfig:
    name: str
    level: str
    logger_format: str
    log_path: Optional[str] = None
    component_name: Optional[str] = None
    rotation: Optional[str] = None
    retention: Optional[str] = None
    compression: Optional[Union[str, Callable]] = None
    compression_format: Optional[str] = None
    subdirectory: Optional[str] = None
    preset: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
```

**Attribute Descriptions:**

| Attribute | Type | Description |
| --- | --- | --- |
| `name` | `str` | Unique identifier name for the logger. |
| `level` | `str` | Minimum log level, such as "DEBUG", "INFO". |
| `logger_format` | `str` | Loguru log formatting string. |
| `log_path` | `Optional[str]` | Directory for storing log files. If `None`, outputs only to console. |
| `component_name` | `Optional[str]` | Component name, typically used for log filenames. |
| `rotation` | `Optional[str]` | File rotation strategy, such as "10 MB", "1 day". |
| `retention` | `Optional[str]` | File retention strategy, such as "7 days", 10 (files). |
| `compression` | `Optional[Union[str, Callable]]` | Compression format like "zip", "gz", or custom compression function. |
| `compression_format` | `Optional[str]` | Custom naming format for compressed files. |
| `subdirectory` | `Optional[str]` | Subdirectory to create under `log_path`. |
| `preset` | `Optional[str]` | Name of the preset configuration to use. |
| `extra` | `Dict[str, Any]` | Additional parameters passed to `logger.configure`. |

---

## `base.py` - Base Functionality

This module provides the core logic for configuring loggers.

### `configure_logger()`

Configures a specified logger instance based on a `LoggerConfig` object. This function removes old handlers, sets new format and level, and adds console and file handlers.

```python
def configure_logger(logger_instance: EnhancedLogger, config: LoggerConfig) -> None:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `logger_instance` | `EnhancedLogger` | The `loguru` logger instance to configure. |
| `config` | `LoggerConfig` | Object containing all configuration information. |

### `get_console()`

Gets the globally shared `rich.console.Console` instance used for rendering all Rich components.

```python
def get_console() -> Console:
    ...
```

**Return Value:**
- `rich.console.Console`: Rich Console instance for enhanced output.

---

## `handlers.py` - Handler Management

This module is responsible for creating and managing log output destinations.

### `create_destination_filters()`

Creates a set of filters used to route log records to the correct destinations (console-only, file-only, or both).

```python
def create_destination_filters() -> Dict[str, Callable]:
    ...
```

**Return Value:**
- `Dict[str, Callable]`: A dictionary containing `"console"` and `"file"` keys with corresponding filter functions as values.

### `format_filename()`

Generates log filenames based on specified format templates.

```python
def format_filename(component_name: str, name_format: Optional[str] = None) -> str:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `component_name` | `str` | Component name used to populate filename templates. |
| `name_format` | `Optional[str]` | Filename format template. Defaults to `"{name}_{time:YYYY-MM-DD}.log"`. |

**Examples:**

```python
# Default format
format_filename("my_app") 
# -> "my_app_2023-10-27.log"

# Custom format
format_filename("worker", name_format="{name}.log") 
# -> "worker.log"
```

---

## `presets.py` - Preset Configurations

This module provides predefined logger configurations for quick setup.

### `get_preset_config()`

Gets a preset configuration dictionary by name.

```python
def get_preset_config(name: str) -> Dict[str, Any]:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `str` | Name of the preset configuration, such as `"default"`, `"production"`, `"development"`. |

**Return Value:**
- `Dict[str, Any]`: Dictionary containing the preset configuration.

### `create_custom_compression_function()`

When you need to customize the naming format for compressed files, use this function to create a `compression` parameter to pass to `logger.add`.

```python
def create_custom_compression_function(format_str: str) -> Callable[[str], str]:
    ...
```

**Parameter Descriptions:**

| Parameter | Type | Description |
| --- | --- | --- |
| `format_str` | `str` | Custom filename format, e.g., `"{path}.{time:YYYY-MM}.zip"`. |

**Return Value:**
- `Callable[[str], str]`: A function that Loguru will call during compression to determine the compressed filename.

---

[Back to API Overview](./index.md)