# Installation

This page will guide you through the installation process of pretty-loguru.

## 🚀 Quick Install

### Using pip (Recommended)

```bash
pip install pretty-loguru
```

### Using conda

```bash
conda install -c conda-forge pretty-loguru
```

## 📋 System Requirements

### Python Version
- **Minimum Requirement**: Python 3.8+
- **Recommended Version**: Python 3.9+ or newer

### Operating System Support
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+, etc.)

## 📦 Dependencies

pretty-loguru will automatically install the following dependencies:

- **[loguru](https://github.com/Delgan/loguru)** - Core logging functionality
- **[rich](https://github.com/Textualize/rich)** - Rich console output
- **[art](https://github.com/sepandhaghighi/art)** - ASCII art generation
- **[pyfiglet](https://github.com/pwaller/pyfiglet)** - Text art fonts

## 🔧 Installation Verification

After installation, run the following code to verify:

```python
# test_installation.py
from pretty_loguru import logger, logger_start

# Test basic functionality
component_name = logger_start(folder="test_logs")
logger.info("✅ pretty-loguru installed successfully!")
logger.success("🎉 All features are working correctly!")

# Test Rich block
logger.block(
    "Installation Verification",
    [
        "✅ loguru: OK",
        "✅ rich: OK", 
        "✅ art: OK",
        "✅ pyfiglet: OK"
    ],
    border_style="green"
)

# Test ASCII art
logger.ascii_header("SUCCESS", font="slant")
```

If you see colorful output without errors, the installation was successful!

## 🛠️ Advanced Installation Options

### Installing the Development Version

If you want to use the latest development version:

```bash
pip install git+https://github.com/JonesHong/pretty-loguru.git
```

### Installing from Source

```bash
# Clone the repository
git clone https://github.com/JonesHong/pretty-loguru.git
cd pretty-loguru

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Installing in a Virtual Environment (Recommended)

Using a virtual environment can prevent package conflicts:

```bash
# Create a virtual environment
python -m venv pretty_loguru_env

# Activate the virtual environment
# Windows:
pretty_loguru_env\Scripts\activate
# macOS/Linux:
source pretty_loguru_env/bin/activate

# Install pretty-loguru
pip install pretty-loguru
```

## 🐳 Docker Environment

If you use Docker, you can add this to your Dockerfile:

```dockerfile
FROM python:3.9-slim

# Install pretty-loguru
RUN pip install pretty-loguru

# Other settings...
```

## ⚠️ Troubleshooting

### Common Issues

#### 1. Installation Failed: Insufficient Permissions

```bash
# Solution: Use --user to install
pip install --user pretty-loguru
```

#### 2. Dependency Conflict

```bash
# Solution: Use a virtual environment
python -m venv new_env
source new_env/bin/activate  # Linux/Mac
# or new_env\Scripts\activate  # Windows
pip install pretty-loguru
```

#### 3. Outdated Python Version

```bash
# Check Python version
python --version

# If version < 3.8, please upgrade Python
```

#### 4. Some Features Not Working

If ASCII art features are problematic, it might be a font package issue:

```bash
# Reinstall related packages
pip uninstall art pyfiglet
pip install art pyfiglet
```

### Detailed Diagnostics

If you encounter problems, run the diagnostic script:

```python
# diagnose.py
import sys
import subprocess

def check_installation():
    print("🔍 pretty-loguru Installation Diagnostics")
    print("=" * 40)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Check main dependencies
    packages = ['loguru', 'rich', 'art', 'pyfiglet']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: Not installed")
    
    # Check pretty-loguru
    try:
        from pretty_loguru import logger, logger_start
        print("✅ pretty-loguru: Installed")
        
        # Basic functionality test
        component_name = logger_start(folder="diagnose_test")
        logger.info("Basic functionality test passed")
        print("✅ Basic functionality: OK")
        
    except Exception as e:
        print(f"❌ pretty-loguru: Error - {e}")

if __name__ == "__main__":
    check_installation()
```

## 📱 IDE Integration

### VS Code

After installing the Python extension, VS Code will automatically recognize pretty-loguru:

```json
// settings.json
{
    "python.analysis.extraPaths": ["./pretty_loguru_env/lib/python3.9/site-packages"]
}
```

### PyCharm

In PyCharm, set the interpreter to point to your virtual environment.

## 🔄 Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade pretty-loguru
```

To check the version:

```python
import pretty_loguru
print(pretty_loguru.__version__)
```

## ✅ Checklist

After installation, confirm the following:

- [ ] Python version >= 3.8
- [ ] pretty-loguru installed successfully
- [ ] Basic logging functions work correctly
- [ ] Rich blocks display correctly
- [ ] ASCII art functions work correctly
- [ ] File output works correctly

## 🚀 Next Steps

After installation:

1. **[Quick Start](./quick-start)** - Experience all features in 5 minutes
2. **[Basic Usage](./basic-usage)** - Understand core concepts in detail
3. **[Example Collection](../examples/)** - Real-world application scenarios

Congratulations! You have successfully installed pretty-loguru and are ready to start your elegant logging journey! 🎉
