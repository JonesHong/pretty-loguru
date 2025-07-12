# Examples Overview

Pretty Loguru provides comprehensive examples to help you quickly get started and master various features. All examples include complete Python code and detailed bilingual documentation.

## 🎯 Learning Path

### 1. Beginner Start (5 minutes)
**Recommended Sequence**: 01_basics → 02_visual → 03_presets

- **[01_basics](../../../examples/01_basics/README.en.md)** - Core Features (3-minute Quick Start)
  - Basic logger creation and usage
  - Console vs file output
  - Target-oriented logging methods
  - [中文版本](../../../examples/01_basics/README.md)

- **[02_visual](../../../examples/02_visual/README.en.md)** - Visual Features Showcase
  - Block formatting and ASCII art
  - Rich components and table display
  - Monitoring dashboard examples
  - [中文版本](../../../examples/02_visual/README.md)

- **[03_presets](../../../examples/03_presets/README.en.md)** - Preset Configurations and File Management
  - Rotation strategy selection
  - Environment configuration management
  - Production environment best practices
  - [中文版本](../../../examples/03_presets/README.md)

### 2. Practical Application (15 minutes)
**Recommended Sequence**: 04_fastapi → 05_production

- **[04_fastapi](../../../examples/04_fastapi/README.en.md)** - Real Web Application Examples
  - FastAPI deep integration
  - Middleware automatic logging
  - Microservice dependency injection
  - [中文版本](../../../examples/04_fastapi/README.md)

- **[05_production](../../../examples/05_production/README.en.md)** - Production Environment Best Practices
  - Multi-environment configuration management
  - Performance monitoring and error tracking
  - Security compliance requirements
  - [中文版本](../../../examples/05_production/README.md)

### 3. Advanced Exploration (30 minutes)
**Suitable for**: Developers who need deep customization features

- **[06_advanced](../../../examples/06_advanced/README.en.md)** - Advanced Features and Direct Library Access
  - Advanced API module usage
  - Custom extension development
  - Event system and protocols
  - [中文版本](../../../examples/06_advanced/README.md)

## 🚀 Quick Start

1. **Clone examples**:
   ```bash
   git clone https://github.com/JonesHong/pretty-loguru.git
   cd pretty-loguru/examples
   ```

2. **Run first example**:
   ```bash
   cd 01_basics
   python simple_usage.py
   ```

3. **Check generated logs**:
   ```bash
   ls ./logs/
   cat ./logs/*.log
   ```

## 📚 Example Features

### Fully Runnable
- All examples are complete Python programs
- Include necessary dependencies and configurations
- Provide detailed running instructions

### Progressive Learning
- Learning path from simple to complex
- Each example has clear learning objectives
- Provide real-world application scenarios

### Multilingual Support
- Each example provides bilingual documentation
- Clear and understandable code comments
- Suitable for developers with different language backgrounds

### Practical Oriented
- Designed based on real development scenarios
- Provide production environment best practices
- Include performance and security considerations

## 🎯 Browse by Features

### Basic Features
- **Logger Creation**: [01_basics/simple_usage.py](../../../examples/01_basics/simple_usage.py)
- **Output Control**: [01_basics/console_vs_file.py](../../../examples/01_basics/console_vs_file.py)
- **Target-Oriented**: [01_basics/target_logging.py](../../../examples/01_basics/target_logging.py)

### Visualization Features
- **Block Formatting**: [02_visual/blocks.py](../../../examples/02_visual/blocks.py)
- **ASCII Art**: [02_visual/ascii_art.py](../../../examples/02_visual/ascii_art.py)
- **Rich Components**: [02_visual/rich_components.py](../../../examples/02_visual/rich_components.py)

### Configuration Management
- **Rotation Strategy**: [03_presets/rotation_examples.py](../../../examples/03_presets/rotation_examples.py)
- **Preset Comparison**: [03_presets/preset_comparison.py](../../../examples/03_presets/preset_comparison.py)
- **Custom Configuration**: [03_presets/custom_presets.py](../../../examples/03_presets/custom_presets.py)

### Web Application Integration
- **Basic Integration**: [04_fastapi/simple_api.py](../../../examples/04_fastapi/simple_api.py)
- **Middleware**: [04_fastapi/middleware_demo.py](../../../examples/04_fastapi/middleware_demo.py)
- **Dependency Injection**: [04_fastapi/dependency_injection.py](../../../examples/04_fastapi/dependency_injection.py)

### Production Environment
- **Environment Management**: [05_production/deployment_logging.py](../../../examples/05_production/deployment_logging.py)
- **Performance Monitoring**: [05_production/performance_monitoring.py](../../../examples/05_production/performance_monitoring.py)
- **Error Tracking**: [05_production/error_tracking.py](../../../examples/05_production/error_tracking.py)

### Advanced Features
- **Direct Access**: [06_advanced/direct_library_access.py](../../../examples/06_advanced/direct_library_access.py)
- **Custom Extensions**: [06_advanced/custom_extensions.py](../../../examples/06_advanced/custom_extensions.py)
- **Event System**: [06_advanced/event_system.py](../../../examples/06_advanced/event_system.py)

## 💡 Usage Tips

### 1. Development Phase
Recommend using `01_basics` and `02_visual` examples, focusing on feature implementation and debugging.

### 2. Testing Phase
Refer to `03_presets` examples to establish appropriate log management strategies.

### 3. Deployment Phase
Use `04_fastapi` and `05_production` examples to implement production-grade configurations.

### 4. Optimization Phase
Explore `06_advanced` examples to achieve deep customization and performance optimization.

## 🔗 Related Resources

- **[Installation Guide](../guide/installation)** - Installation and configuration instructions
- **[API Documentation](../api/)** - Complete API reference
- **[Integration Guide](../integrations/)** - Framework integration instructions
- **[GitHub Repository](https://github.com/JonesHong/pretty-loguru)** - Latest code and issue tracking

## ❓ Need Help?

- Check detailed README documentation in each example directory
- Run example code and observe output
- Refer to [FAQ](../guide/faq) section
- Ask questions on [GitHub Issues](https://github.com/JonesHong/pretty-loguru/issues)

Start your Pretty Loguru learning journey! 🎉
