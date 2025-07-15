# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pretty-Loguru is an enhanced logging library built on top of Loguru, featuring Rich panels, ASCII art headers, visual blocks, and comprehensive integrations. The library provides beautiful, structured logging with both console and file output capabilities.

## Development Commands

### Python Environment
```bash
# Install dependencies
pip install -e .

# Install with all optional dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_refactoring.py -v

# Run specific test function
python -m pytest tests/test_refactoring.py::test_console_instance_unification -v

# Run performance benchmarks
python tests/performance/benchmark.py
```

### Documentation
```bash
# Serve documentation locally
cd docs
npm install
npm run dev     # Development server on localhost:3000
npm run build   # Build for production
npm run preview # Preview production build
```

### Quick Validation Commands
```bash
# Test core functionality
python -c "from pretty_loguru import create_logger; logger = create_logger('test'); logger.info('Test successful')"

# Test configuration system
python -c "from pretty_loguru import ConfigTemplates; config = ConfigTemplates.production(); logger = config.apply_to('test'); logger.info('Config test')"

# Test visual features (requires art/pyfiglet)
python examples/03_visual/ascii_art.py
```

## Architecture Overview

### Core Architecture
The library follows a layered architecture:

1. **Core Layer** (`pretty_loguru/core/`):
   - `config.py`: Unified LoggerConfig class with template support, multi-logger management
   - `templates.py`: Configuration template system (development, production, testing presets)
   - `base.py`: Base logger configuration and console management
   - `target_formatter.py`: Target-oriented formatting (console-only, file-only modes)
   - `presets.py`: Log rotation presets (daily, hourly, size-based)

2. **Factory Layer** (`pretty_loguru/factory/`):
   - `creator.py`: Logger creation and management (create_logger, get_logger, reinit_logger)
   - `methods.py`: Dynamic method injection for visual logging features

3. **Formats Layer** (`pretty_loguru/formats/`):
   - `block.py`: Rich panel-based logging blocks
   - `ascii_art.py`: ASCII art headers using art library
   - `rich_components.py`: Rich tables, trees, columns, progress bars

4. **Integration Layer** (`pretty_loguru/integrations/`):
   - `fastapi.py`: FastAPI logging setup and middleware
   - `uvicorn.py`: Uvicorn server logging integration

### Key Design Patterns

**Configuration System**: Uses a unified `LoggerConfig` class that supports:
- Template-based configuration (`ConfigTemplates.production()`)
- Multi-logger management (`config.apply_to("app1", "app2")`)
- Dynamic updates (`config.update(level="DEBUG")` updates all attached loggers)
- Chaining operations (`config.clone().update(level="INFO")`)

**Target-Oriented Logging**: Supports different output targets:
- `logger.info()` - outputs to both console and file
- `logger.console_block()` - console-only rich blocks
- `logger.file_ascii_header()` - file-only ASCII headers

**Visual Logging Methods**: Dynamically injected methods:
- `logger.block(title, content, border_style="green")` - Rich panels
- `logger.ascii_header("STARTUP", font="slant")` - ASCII art titles
- `logger.ascii_block(title, content, ascii_header="STATUS")` - Combined blocks

## Configuration System

### Modern Usage (Recommended)
```python
from pretty_loguru import LoggerConfig, ConfigTemplates

# Template-based configuration
config = ConfigTemplates.production()
logger = config.apply_to("app")

# Multi-logger management
config = LoggerConfig(level="INFO", log_path="logs")
loggers = config.apply_to("service1", "service2", "service3")

# Dynamic configuration updates
config.update(level="DEBUG")  # All attached loggers update automatically
```

### Legacy Usage (Still Supported)
```python
from pretty_loguru import create_logger

# Traditional single logger creation
logger = create_logger("app", level="INFO", log_path="logs")
```

### Configuration Templates
Available templates in `ConfigTemplates`:
- `development()` - DEBUG level, native format, 7-day retention
- `production()` - INFO level, compression, 30-day retention, cleaner enabled
- `testing()` - WARNING level, 3-day retention
- `performance()` - ERROR level, proxy mode, large rotation sizes
- Rotation templates: `daily()`, `hourly()`, `weekly()`, `monthly()`

## Core Dependencies

### Required Dependencies
- **Loguru**: Base logging functionality (>=0.6.0)
- **Rich**: Console formatting, panels, tables (>=12.0.0)
- **Art**: ASCII art generation (>=5.0.0)
- **PyFiglet**: Alternative ASCII art (>=1.1.2)
- **Matplotlib**: For visual components (>=3.7.0)
- **Python-dateutil**: Relative date calculations (>=2.8.2)

## Testing Strategy

### Test Structure
1. **Regression Tests** (`tests/test_refactoring.py`):
   - Console instance unification
   - Dependency management
   - API compatibility validation
   - Performance benchmarks

2. **Performance Tests** (`tests/performance/`):
   - Logger creation benchmarks
   - Memory usage validation
   - Console reuse performance

### Example Categories
- `01_quickstart/`: 5-minute introduction examples
- `02_basics/`: Core functionality and multiple loggers
- `03_visual/`: Rich blocks, ASCII art, visual components
- `04_configuration/`: Configuration templates, rotation, presets
- `05_integrations/`: FastAPI, Uvicorn, middleware examples
- `06_production/`: Deployment, error tracking, performance monitoring
- `07_advanced/`: Direct Loguru integration, performance testing
- `08_enterprise/`: Microservices, security, compliance logging

## Integration Guidelines

### FastAPI Integration
```python
from pretty_loguru.integrations.fastapi import setup_fastapi_logging

app = FastAPI()
setup_fastapi_logging(app, log_path="logs/api")
```

### Custom Integration Pattern
1. Create logger with appropriate configuration
2. Use target-oriented methods for different output needs
3. Leverage configuration templates for consistency
4. Use visual logging methods sparingly in production

## Common Development Patterns

### Adding New Visual Features
1. Create formatter in `formats/` module
2. Add method injection in `factory/methods.py`
3. Update target formatter for console/file separation
4. Add examples in appropriate example directory

### Adding Configuration Templates
1. Add static method to `ConfigTemplates` class in `templates.py`
2. Follow naming convention (environment or rotation-based)
3. Document in examples and update tests

### Performance Considerations
- Console instances are singleton-managed for performance
- Configuration objects support cloning to avoid mutation
- Target-oriented logging minimizes unnecessary formatting
- Log rotation uses efficient compression and naming strategies

## Important Implementation Details

### Singleton Console Management
The library uses a singleton pattern for Rich console instances to avoid performance issues. See `pretty_loguru/core/base.py` for the `SingletonConsole` implementation.

### Method Injection Pattern
Visual logging methods are dynamically injected into logger instances via `pretty_loguru/factory/methods.py`. This allows for clean separation of concerns while maintaining a simple API.

### Configuration Immutability
LoggerConfig objects in `pretty_loguru/core/config.py` support the `clone()` method to create independent copies, preventing unintended mutations when sharing configurations.

### Multi-Logger Management
The configuration system supports managing multiple loggers through a single config object. When `config.update()` is called, all attached loggers are automatically reconfigured.