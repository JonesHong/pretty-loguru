# 02_visual - Visual Features Showcase

This directory showcases the visual features of pretty-loguru, making your log output more beautiful and intuitive.

## 🎯 Learning Objectives

- Master block formatting functionality
- Learn to use ASCII art titles
- Master FIGlet text art features
- Understand the powerful Rich components
- Create professional monitoring dashboards

## 📚 Example List

### 1. blocks.py - Block Formatting Showcase
**Learning Focus**: Using blocks to highlight important information

```bash
python blocks.py
```

**Features Demonstrated**:
- Basic block formatting
- Colored border styles (green/yellow/red/blue)
- System status reporting
- Deployment process visualization

**Core Methods**:
```python
logger.block("Title", ["Content line 1", "Content line 2"], border_style="green")
```

### 2. ascii_art.py - ASCII Art Titles
**Learning Focus**: Creating visually impactful titles

```bash
python ascii_art.py
```

**Features Demonstrated**:
- ASCII art titles
- Application branding display
- Status titles (INIT/LOADING/READY/ERROR)
- Deployment workflow visualization

**Core Methods**:
```python
logger.ascii_header("SUCCESS", font="slant", border_style="green")
```

### 3. figlet_demo.py - FIGlet Text Art Showcase
**Learning Focus**: Using FIGlet to create visually impactful text art

```bash
pip install pyfiglet  # Install pyfiglet first
python figlet_demo.py
```

**Features Demonstrated**:
- FIGlet text art titles
- Multiple font effects showcase
- Application branding design
- Status display (INIT/LOAD/READY/ERROR)
- Creative number and date displays
- Deployment workflow visualization

**Core Methods**:
```python
logger.figlet_header("WELCOME", font="slant", border_style="blue")
```

**Note**: This feature requires installing the `pyfiglet` package: `pip install pyfiglet`

### 4. rich_components.py - Rich Component Showcase
**Learning Focus**: Using Rich components to create professional dashboards

```bash
python rich_components.py
```

**Features Demonstrated**:
- Data table display
- Tree directory structure
- Multi-column side-by-side display
- Real-time progress bars
- Monitoring dashboard examples

**Core Methods**:
```python
# Table (data is a list of dictionaries)
user_data = [
    {"Name": "Alice", "Email": "alice@example.com", "Role": "Admin"},
    {"Name": "Bob", "Email": "bob@example.com", "Role": "User"}
]
logger.table(title="User Statistics", data=user_data)

# Tree structure
tree_structure = {
    "Project/": {
        "src/": {"app.py": None, "utils.py": None},
        "tests/": {"test_app.py": None}
    }
}
logger.tree("Project Structure", tree_structure)

# Multi-column
services = ["🟢 API: Normal", "🟡 DB: Warning", "🔴 Cache: Error"]
logger.columns(title="Service Status", items=services)

# Progress bar
items = list(range(100))
for item in logger.progress.track_list(items, "Processing data"):
    time.sleep(0.01)  # Simulate work
```

### 5. code_highlighting_examples.py - Code Highlighting Showcase
**Learning Focus**: Using syntax highlighting to display code snippets

```bash
python code_highlighting_examples.py
```

**Features Demonstrated**:
- Multi-language code syntax highlighting (Python, JavaScript, SQL, JSON, HTML)
- Different theme support (monokai, github-dark, one-dark, material)
- Code difference comparison
- Reading code snippets from files
- Target output control

**Core Methods**:
```python
# Code highlighting
code = '''
def hello_world():
    print("Hello, World!")
    return True
'''
logger.code(code=code, language="python", title="Hello World", theme="monokai")

# Code difference comparison
logger.diff(old_code=old_code, new_code=new_code, language="python")

# Read code from file
logger.code_file(file_path="example.py", start_line=1, end_line=20)
```

## 🎨 Visual Effects Preview

### Block Formatting
```
┌─────────────────────────────────┐
│          System Status          │
├─────────────────────────────────┤
│ CPU: 45%                        │
│ Memory: 60%                     │
│ Disk: 120GB available          │
│ Status: Running normally        │
└─────────────────────────────────┘
```

### ASCII Art Titles
```
   _____ __  __ ____________ _____ _____
  / ___// / / // ____/ ____// ___// ___/
  \__ \/ / / // /   / /     \__ \ \__ \ 
 ___/ / /_/ // /___/ /___  ___/ /___/ / 
/____/\____/ \____/\____/ /____//____/  
```

### FIGlet Text Art
```
 __        __ _____ _     ____  ___  __  __ _____
 \ \      / /| ____| |   / ___|/ _ \|  \/  | ____|
  \ \ /\ / / |  _| | |  | |   | | | | |\/| |  _|  
   \ V  V /  | |___| |__| |___| |_| | |  | | |___ 
    \_/\_/   |_____|_____\____|\___/|_|  |_|_____|
```

### Rich Table
```
                    📊 User Statistics                    
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Name    ┃ Email             ┃ Role      ┃ Status    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Alice   │ alice@example.com │ Admin     │ Active    │
│ Bob     │ bob@example.com   │ User      │ Active    │
└─────────┴───────────────────┴───────────┴───────────┘
```

## 🚀 Quick Start

1. **Run visual examples**:
   ```bash
   cd 02_visual
   python blocks.py
   ```

2. **View output effects**:
   - Console will display colorful visual content
   - Check log files in `./logs/` directory

3. **Try other examples**:
   ```bash
   python ascii_art.py
   
   # FIGlet example (install pyfiglet first)
   pip install pyfiglet
   python figlet_demo.py
   
   python rich_components.py
   ```

## 💡 Practical Scenarios

### 1. System Monitoring Dashboard
```python
# System status overview
logger.ascii_header("MONITOR", font="slant", border_style="blue")

# Key metrics table
metrics_data = [
    ["CPU Usage", "45%", "Normal"],
    ["Memory", "68%", "Normal"],
    ["Disk Space", "78%", "Warning"]
]
logger.table("System Metrics", data=metrics_data)
```

### 2. Deployment Process Report
```python
# Deployment stage title
logger.ascii_header("DEPLOY", font="slant", border_style="blue")

# Deployment steps block
steps = [
    "✓ Code compilation completed",
    "✓ All tests passed", 
    "→ Deploying to production environment"
]
logger.block("🚀 Deployment Progress", steps, border_style="green")
```

### 3. Error Report
```python
# Error title
logger.ascii_header("ERROR", font="slant", border_style="red")

# Error details
error_info = [
    "Error Type: DatabaseConnectionError",
    "Error Code: DB001", 
    "Occurred: 2024-06-28 10:30:25",
    "Impact: User login functionality"
]
logger.block("⚠️ Error Details", error_info, border_style="red")
```

## 🎯 Best Practices

### 1. Choose Appropriate Visualization Methods
- **Blocks**: Important status and reports
- **ASCII Titles**: Stage separation and branding
- **Tables**: Structured data display
- **Tree**: Hierarchical structure display
- **Multi-column**: Side-by-side comparison information

### 2. Color Usage Guidelines
- **Green**: Success, normal status
- **Yellow**: Warning, in progress
- **Red**: Error, abnormal status
- **Blue**: Information, general status

### 3. Performance Considerations
```python
# Show complex visualizations only in console
logger.console_info("Displaying detailed dashboard...")
logger.table(...)  # Complex table

# Keep file records concise
logger.file_info("System status: CPU 45%, Memory 68%")
```

## 📁 Generated Log Files

After running examples, you will see:
```
logs/
├── blocks_demo_YYYYMMDD-HHMMSS.log
├── ascii_demo_YYYYMMDD-HHMMSS.log
├── tables_demo_YYYYMMDD-HHMMSS.log
└── dashboard_YYYYMMDD-HHMMSS.log
```

## 🔗 Related Examples

- **01_basics/** - Learn basic logging functionality
- **04_fastapi/** - Use visualization in web applications
- **05_production/** - Production environment monitoring practices

## ❓ Frequently Asked Questions

**Q: Will visual content affect performance?**
A: Mainly displayed in console, simplified version recorded in files, minimal impact on performance.

**Q: How to use in production environment?**
A: Recommended for monitoring dashboards, deployment reports and other important scenarios, avoid overuse.

**Q: Can visual content be customized?**
A: Supports multiple border styles and colors, choose appropriate visual effects according to needs.