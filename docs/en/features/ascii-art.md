# ASCII Art Headers

ASCII art headers are one of the signature features of pretty-loguru, allowing you to create eye-catching text art titles that add a professional touch and visual appeal to your log output.

## 🎯 Basic Usage

### Simple ASCII Header

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# The most basic ASCII header
logger.ascii_header("HELLO WORLD")
```

### ASCII Header with Parameters

```python
logger.ascii_header(
    "SYSTEM START",
    font="slant",           // Font style
    border_style="blue",    // Border color
    log_level="INFO"        // Log level
)
```

## 🎨 Font Styles

pretty-loguru supports multiple ASCII art fonts, each with a different visual effect:

### Standard Font Series

#### standard
```python
logger.ascii_header("STANDARD", font="standard")
```
Output:
```
 ____  _____  _     _   _  ____    _    ____  ____  
/ ___|_   _|/ \   | \ | |/ ___|  / \  |  _ \|  _ \ 
\___ \ | | / _ \  |  \| | |  _   / _ \ | |_) | | | |
 ___) || |/ ___ \ | |\  | |_| | / ___ \|  _ <| |_| |
|____/ |_/_/   \_\|_| \_|\____||_/   \_\_| \_\____/ 
```

#### slant
```python
logger.ascii_header("SLANT", font="slant")
```
Output:
```
   _____ __    ___    _   ________
  / ___// /   /   |  / | / /_  __/
  \__ \/ /   / /| | /  |/ / / /   
 ___/ / /___/ ___ |/ /|  / / /    
/____/_____/_/  |_/_/ |_/ /_/     
```

#### doom
```python
logger.ascii_header("DOOM", font="doom")
```
Output:
```
______   _____  _____ ___  ___ 
|  _  \ |  _  ||  _  ||  \/  |
| | | | | | | || | | || .  . |
| | | | | | | || | | || |\/| |
| |/ /  \ \_/ /\ \_/ /| |  | |
|___/    \___/  \___/ \_|  |_/
```

#### small
```python
logger.ascii_header("SMALL", font="small")
```
Output:
```
 __  __  __   __    
(_  |\/| / /  |  |   
__) |  | \__  |__|__ 
```

#### block
```python
logger.ascii_header("BLOCK", font="block")
```
Output:
```
_|_|_|    _|        _|_|      _|_|_|  _|    _|
_|    _|  _|      _|    _|  _|        _|  _|  
_|_|_|    _|      _|    _|  _|        _|_|    
_|    _|  _|      _|    _|  _|        _|  _|  
_|_|_|    _|_|_|    _|_|      _|_|_|  _|    _|
```

### Special Fonts

#### digital
```python
logger.ascii_header("12345", font="digital")
```
Output:
```
+-+-+ +-+-+ +-+-+ +-+-+ +-+-+
|1| | |2| | |3| | |4| | |5| |
+-+-+ +-+-+ +-+-+ +-+-+ +-+-+
```

#### banner
```python
logger.ascii_header("BANNER", font="banner")
```

## 🌈 Border Styles and Colors

### Border Colors

```python
# Borders with different colors
logger.ascii_header("SUCCESS", border_style="green")
logger.ascii_header("WARNING", border_style="yellow") 
logger.ascii_header("ERROR", border_style="red")
logger.ascii_header("INFO", border_style="blue")
logger.ascii_header("SPECIAL", border_style="magenta")
logger.ascii_header("NEUTRAL", border_style="cyan")
```

### Border Styles

```python
# Borders with different styles
logger.ascii_header("SOLID", border_style="solid")
logger.ascii_header("DOUBLE", border_style="double")
logger.ascii_header("ROUNDED", border_style="rounded")
logger.ascii_header("THICK", border_style="thick")
```

## 📊 Log Level Control

ASCII headers can be combined with different log levels:

```python
# ASCII headers at different levels
logger.ascii_header("DEBUG MODE", log_level="DEBUG")
logger.ascii_header("APP START", log_level="INFO")
logger.ascii_header("SUCCESS", log_level="SUCCESS")
logger.ascii_header("WARNING", log_level="WARNING")
logger.ascii_header("ERROR", log_level="ERROR")
logger.ascii_header("CRITICAL", log_level="CRITICAL")
```

## 🎮 Practical Application Scenarios

### Application Startup

```python
def startup_sequence():
    logger.ascii_header("APP STARTUP", font="slant", border_style="blue")
    
    logger.info("Loading configuration...")
    logger.success("Configuration loaded successfully")
    
    logger.info("Connecting to database...")
    logger.success("Database connection successful")
    
    logger.ascii_header("READY", font="block", border_style="green")
```

### Error Handling

```python
def handle_critical_error(error):
    logger.ascii_header("ERROR", font="doom", border_style="red")
    logger.error(f"A critical error occurred: {error}")
    logger.ascii_header("SHUTDOWN", font="standard", border_style="red")
```

### Phase Marking

```python
def data_processing_pipeline():
    logger.ascii_header("PHASE 1", font="small", border_style="cyan")
    logger.info("Starting data extraction...")
    
    logger.ascii_header("PHASE 2", font="small", border_style="cyan")
    logger.info("Starting data transformation...")
    
    logger.ascii_header("PHASE 3", font="small", border_style="cyan")  
    logger.info("Starting data loading...")
    
    logger.ascii_header("COMPLETE", font="slant", border_style="green")
```

### System Monitoring

```python
def system_status_check():
    logger.ascii_header("HEALTH CHECK", font="standard", border_style="blue")
    
    # Check various services
    services = ["Database", "Redis", "API", "Queue"]
    
    for service in services:
        status = check_service(service) # Assume check_service is defined
        if status:
            logger.success(f"{service}: Running normally")
        else:
            logger.error(f"{service}: Service abnormal")
    
    logger.ascii_header("CHECK COMPLETE", font="small", border_style="green")
```

## ⚠️ Usage Notes

### Text Limitations

ASCII art only supports ASCII characters. Using non-ASCII characters will result in an error:

```python
# Correct - ASCII characters only
logger.ascii_header("HELLO WORLD")

# Incorrect - Contains non-ASCII characters
try:
    logger.ascii_header("你好世界")  # This will throw an error
except ValueError as e:
    logger.error(f"ASCII Error: {e}")
```

### Checking if a String is ASCII

```python
from pretty_loguru import is_ascii_only

text = "HELLO WORLD"
if is_ascii_only(text):
    logger.ascii_header(text)
else:
    logger.warning("Text contains non-ASCII characters, using a normal header")
    logger.info(f"=== {text} ===")
```

### Length Recommendations

For the best visual effect, it is recommended to:
- Keep the header length within 20 characters
- Avoid using overly long text
- Use concise and powerful words

```python
# Recommended - Concise and clear
logger.ascii_header("START")
logger.ascii_header("COMPLETE")
logger.ascii_header("ERROR")

# Not recommended - Too long
logger.ascii_header("VERY LONG TITLE THAT MIGHT NOT LOOK GOOD")
```

## 🔧 Advanced Techniques

### Dynamic Font Selection

```python
import random

def random_header(text):
    fonts = ["standard", "slant", "doom", "small", "block"]
    colors = ["blue", "green", "cyan", "magenta"]
    
    font = random.choice(fonts)
    color = random.choice(colors)
    
    logger.ascii_header(text, font=font, border_style=color)

# Each execution will have a different effect
random_header("SURPRISE")
```

### Combined Usage

```python
def deployment_complete():
    # Start header
    logger.ascii_header("DEPLOY", font="slant", border_style="blue")
    
    # Processing...
    logger.info("Deploying...")
    
    # Success header
    logger.ascii_header("SUCCESS", font="block", border_style="green")
```

### Conditional Headers

```python
def status_header(success: bool):
    if success:
        logger.ascii_header("SUCCESS", font="block", border_style="green")
    else:
        logger.ascii_header("FAILED", font="doom", border_style="red")

# Display different headers based on the result
# result = some_operation()
# status_header(result.success)
```

## 🚀 Next Steps

Now that you have mastered the usage of ASCII art headers, you can:

- [Explore ASCII Art Blocks](./ascii-blocks) - The powerful feature combining headers and content
- [Learn about Rich Blocks](./rich-blocks) - Structured visual logs
- [View Complete Examples](../examples/visual/) - Practical applications of visualization features

Make your log output more eye-catching!
