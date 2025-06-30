# ASCII Art Examples

ASCII art is a signature feature of pretty-loguru, capable of creating impressive text art titles. This page showcases various practical applications of ASCII art.

## 🎯 Basic ASCII Headers

### Application Startup Header

```python
from pretty_loguru import logger, logger_start

# Initialize the logging system
logger_start(folder="ascii_demo")

# Application startup
logger.ascii_header("APP START", font="slant", border_style="blue")
logger.info("Loading configuration...")
logger.success("Application started successfully")
```

### Font Showcase

```python
def font_showcase():
    """Showcase all available fonts"""
    
    # Standard font - classic style
    logger.ascii_header("STANDARD", font="standard", border_style="blue")
    
    # Slant font - italic effect
    logger.ascii_header("SLANT", font="slant", border_style="green")
    
    # Doom font - bold effect
    logger.ascii_header("DOOM", font="doom", border_style="red")
    
    # Small font - compact style
    logger.ascii_header("SMALL", font="small", border_style="yellow")
    
    # Block font - blocky style
    logger.ascii_header("BLOCK", font="block", border_style="magenta")
    
    # Digital font - digital style
    logger.ascii_header("DIGITAL", font="digital", border_style="cyan")

font_showcase()
```

## 🌈 Color Theme Showcase

### Status Indication Colors

```python
def status_colors_demo():
    """Use different colors to represent different statuses"""
    
    # Success status - green
    logger.ascii_header("SUCCESS", font="block", border_style="green")
    logger.success("Operation completed successfully")
    
    # Warning status - yellow
    logger.ascii_header("WARNING", font="doom", border_style="yellow")
    logger.warning("Potential issue detected")
    
    # Error status - red
    logger.ascii_header("ERROR", font="doom", border_style="red")
    logger.error("A critical error occurred")
    
    # Info status - blue
    logger.ascii_header("INFO", font="slant", border_style="blue")
    logger.info("Providing important information")
    
    # Special status - purple
    logger.ascii_header("SPECIAL", font="standard", border_style="magenta")
    logger.info("A special event occurred")
    
    # Debug status - cyan
    logger.ascii_header("DEBUG", font="small", border_style="cyan")
    logger.debug("Debug information")

status_colors_demo()
```

## 🚀 Practical Application Scenarios

### System Startup Sequence

```python
def system_startup_sequence():
    """Simulate a system startup process"""
    import time
    
    # Startup title
    logger.ascii_header("SYSTEM BOOT", font="slant", border_style="blue")
    
    logger.info("Initializing system...")
    time.sleep(1)
    
    # Loading phase
    logger.ascii_header("LOADING", font="small", border_style="cyan")
    logger.info("Loading core modules...")
    logger.info("Loading device drivers...")
    logger.info("Loading network stack...")
    time.sleep(2)
    
    # Checking phase
    logger.ascii_header("CHECKING", font="small", border_style="yellow")
    logger.info("Checking hardware status...")
    logger.success("CPU: OK")
    logger.success("Memory: OK")
    logger.success("Disk: OK")
    time.sleep(1)
    
    # Completion title
    logger.ascii_header("READY", font="block", border_style="green")
    logger.success("System startup complete")
    logger.info("Ready to accept user requests")

system_startup_sequence()
```

### Deployment Workflow Stages

```python
def deployment_workflow():
    """Marking stages of a deployment workflow"""
    import time
    
    # Start deployment
    logger.ascii_header("DEPLOY", font="slant", border_style="blue")
    logger.info("Starting deployment process...")
    
    # Build phase
    logger.ascii_header("BUILD", font="small", border_style="cyan")
    logger.info("Compiling code...")
    logger.info("Packaging application...")
    logger.success("Build complete")
    time.sleep(1)
    
    # Test phase
    logger.ascii_header("TEST", font="small", border_style="yellow")
    logger.info("Running unit tests...")
    logger.info("Running integration tests...")
    logger.success("All tests passed")
    time.sleep(1)
    
    # Deploy phase
    logger.ascii_header("DEPLOY", font="small", border_style="magenta")
    logger.info("Uploading to server...")
    logger.info("Updating service...")
    logger.info("Restarting application...")
    time.sleep(1)
    
    # Verify phase
    logger.ascii_header("VERIFY", font="small", border_style="green")
    logger.info("Health check...")
    logger.success("Service is running normally")
    
    # Complete
    logger.ascii_header("COMPLETE", font="block", border_style="green")
    logger.success("Deployment completed successfully")

deployment_workflow()
```

## ⚠️ Usage Notes

### ASCII Character Limitation

```python
from pretty_loguru import is_ascii_only

def ascii_validation_demo():
    """Demonstrate ASCII character validation"""
    
    test_strings = [
        "HELLO WORLD",    # Correct
        "TEST 123",       # Correct  
        "HELLO 世界",      # Incorrect - contains Chinese characters
        "CAFÉ",           # Incorrect - contains accented characters
        "ASCII ONLY"      # Correct
    ]
    
    for text in test_strings:
        if is_ascii_only(text):
            logger.ascii_header(text, font="standard", border_style="green")
            logger.success(f"'{text}' can be used for ASCII art")
        else:
            logger.warning(f"'{text}' contains non-ASCII characters and cannot be used for ASCII art")
            logger.info(f"=== {text} ===")  # Use a normal header instead

ascii_validation_demo()
```

### Length Recommendation

```python
def length_guidelines_demo():
    """Guidelines for text length"""
    
    # Recommended length - looks good
    short_titles = ["START", "OK", "ERROR", "DONE", "READY"]
    
    for title in short_titles:
        logger.ascii_header(title, font="slant", border_style="green")
    
    # Medium length - acceptable
    medium_titles = ["STARTUP", "SUCCESS", "WARNING", "COMPLETE"]
    
    for title in medium_titles:
        logger.ascii_header(title, font="standard", border_style="blue")
    
    # Longer text - be mindful of the effect
    logger.ascii_header("DEPLOYMENT", font="small", border_style="yellow")
    logger.warning("For longer text, it is recommended to use a smaller font")

length_guidelines_demo()
```

## 🎨 Creative Applications

### Simulating Animation Effects

```python
def animation_effect_demo():
    """Simulate an animation effect"""
    import time
    
    # Countdown effect
    for i in range(3, 0, -1):
        logger.ascii_header(str(i), font="doom", border_style="yellow")
        time.sleep(1)
    
    logger.ascii_header("GO", font="doom", border_style="green")
    logger.success("Countdown complete!")

animation_effect_demo()
```

### Branding

```python
def branding_demo():
    """Showcase branding"""
    
    # Company logo
    logger.ascii_header("COMPANY", font="block", border_style="blue")
    logger.info("This is the company's brand logo")
    
    # Product logo
    logger.ascii_header("PRODUCT", font="slant", border_style="magenta")
    logger.info("This is the product's brand logo")
    
    # Version identifier
    logger.ascii_header("V2.0", font="digital", border_style="cyan")
    logger.info("Version information identifier")

branding_demo()
```
This complete example showcases all the main features and creative applications of ASCII art. Run this code, and you will see impressive visual effects!
