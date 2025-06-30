# Code Highlighting

Pretty-loguru provides powerful syntax highlighting capabilities through Rich integration, allowing you to display beautiful, colorized code snippets in your logs.

## Quick Start

```python
from pretty_loguru import create_logger

# Create logger with Rich components enabled
logger = create_logger(name="demo", use_rich_components=True)

# Display Python code with syntax highlighting
code = '''
def hello_world():
    print("Hello, World!")
    return True
'''

logger.code(code, language="python", title="Hello World Example")
```

## Core Methods

### `logger.code()` - Display Code Snippets

Display syntax-highlighted code directly from a string.

```python
logger.code(
    code=source_code,
    language="python",        # Programming language
    theme="monokai",         # Color theme
    line_numbers=True,       # Show line numbers
    title="My Function",     # Optional title
    word_wrap=False,         # Enable word wrapping
    indent_guides=True       # Show indentation guides
)
```

**Parameters:**
- `code` (str): The source code to display
- `language` (str): Programming language (python, javascript, sql, etc.)
- `theme` (str): Syntax highlighting theme
- `line_numbers` (bool): Whether to show line numbers
- `word_wrap` (bool): Enable automatic word wrapping
- `indent_guides` (bool): Show indentation guide lines
- `title` (str, optional): Display title for the code block

### `logger.code_file()` - Display Code from Files

Read and display code directly from files with automatic language detection.

```python
logger.code_file(
    file_path="script.py",
    start_line=10,           # Start from line 10
    end_line=25,             # End at line 25
    language=None,           # Auto-detect from extension
    theme="github-dark"
)
```

**Parameters:**
- `file_path` (str): Path to the source file
- `language` (str, optional): Override automatic language detection
- `start_line` (int, optional): First line to display (1-based)
- `end_line` (int, optional): Last line to display (1-based)
- `theme` (str): Syntax highlighting theme

### `logger.diff()` - Code Comparison

Display side-by-side code comparison with Git-style visual differentiation.

```python
logger.diff(
    old_code=old_version,
    new_code=new_version,
    old_title="Before",      # Title for old version (red border)
    new_title="After",       # Title for new version (green border)
    language="python"
)
```

**Parameters:**
- `old_code` (str): Original version of the code
- `new_code` (str): Updated version of the code
- `old_title` (str): Label for the old version (displayed with red border)
- `new_title` (str): Label for the new version (displayed with green border)
- `language` (str): Programming language for syntax highlighting

## Supported Languages

The code highlighting feature automatically detects and supports many programming languages:

| Language | File Extensions | Language Code |
|----------|----------------|---------------|
| Python | `.py` | `python` |
| JavaScript | `.js` | `javascript` |
| TypeScript | `.ts` | `typescript` |
| HTML | `.html` | `html` |
| CSS | `.css` | `css` |
| JSON | `.json` | `json` |
| SQL | `.sql` | `sql` |
| Markdown | `.md` | `markdown` |
| YAML | `.yaml`, `.yml` | `yaml` |
| XML | `.xml` | `xml` |
| Bash | `.sh` | `bash` |
| C/C++ | `.c`, `.cpp` | `c`, `cpp` |
| Java | `.java` | `java` |
| Go | `.go` | `go` |
| Rust | `.rs` | `rust` |
| PHP | `.php` | `php` |
| Ruby | `.rb` | `ruby` |

## Available Themes

Choose from a variety of syntax highlighting themes:

### Dark Themes
- `monokai` (default) - Popular dark theme with vibrant colors
- `github-dark` - GitHub's dark theme
- `one-dark` - Atom's One Dark theme
- `material` - Material design dark theme
- `dracula` - Popular vampire-themed dark colors
- `nord` - Arctic, north-bluish color palette
- `solarized-dark` - Low-contrast dark theme

### Light Themes
- `github-light` - GitHub's light theme
- `solarized-light` - Low-contrast light theme

## Advanced Examples

### Multi-Language Code Display

```python
def showcase_languages():
    """Display code in multiple languages"""
    
    # Python example
    python_code = '''
class UserManager:
    def __init__(self, database):
        self.db = database
        
    async def create_user(self, user_data):
        """Create a new user account"""
        user_id = await self.db.users.insert(user_data)
        return user_id
'''
    
    logger.code(python_code, language="python", title="Python Class")
    
    # JavaScript example  
    js_code = '''
const userManager = {
    async createUser(userData) {
        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });
            return await response.json();
        } catch (error) {
            console.error('Failed to create user:', error);
            throw error;
        }
    }
};
'''
    
    logger.code(js_code, language="javascript", title="JavaScript Object")
    
    # SQL example
    sql_code = '''
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
'''
    
    logger.code(sql_code, language="sql", title="Database Schema")
```

### File Content Display with Line Ranges

```python
def show_specific_functions():
    """Display specific functions from source files"""
    
    # Show only the main function
    logger.code_file(
        file_path="main.py",
        start_line=45,
        end_line=70,
        title="Main Function Implementation"
    )
    
    # Show configuration section
    logger.code_file(
        file_path="config.py",
        start_line=1,
        end_line=25,
        title="Configuration Settings"
    )
```

### Code Refactoring Comparison

```python
def show_refactoring_example():
    """Demonstrate code improvement with before/after comparison"""
    
    # Original implementation
    old_code = '''
def process_user_data(users):
    results = []
    for user in users:
        if user['active']:
            user_info = {}
            user_info['id'] = user['id']
            user_info['name'] = user['first_name'] + ' ' + user['last_name']
            user_info['email'] = user['email']
            if user['premium']:
                user_info['tier'] = 'premium'
            else:
                user_info['tier'] = 'standard'
            results.append(user_info)
    return results
'''
    
    # Refactored implementation
    new_code = '''
def process_user_data(users):
    """Process active users and format their data"""
    return [
        {
            'id': user['id'],
            'name': f"{user['first_name']} {user['last_name']}",
            'email': user['email'],
            'tier': 'premium' if user.get('premium', False) else 'standard'
        }
        for user in users
        if user.get('active', False)
    ]
'''
    
    logger.diff(
        old_code=old_code,
        new_code=new_code,
        old_title="Original Implementation",
        new_title="Refactored Implementation",
        language="python"
    )
```

### Theme Comparison

```python
def compare_themes():
    """Show the same code in different themes"""
    
    sample_code = '''
import asyncio
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False

async def start_server(config: Config) -> None:
    """Start the application server"""
    print(f"Starting server on {config.host}:{config.port}")
    if config.debug:
        print("Debug mode enabled")
'''
    
    themes = [
        ("monokai", "Monokai Theme"),
        ("github-dark", "GitHub Dark Theme"),
        ("one-dark", "One Dark Theme"),
        ("material", "Material Theme")
    ]
    
    for theme_name, theme_title in themes:
        logger.code(
            code=sample_code,
            language="python",
            theme=theme_name,
            title=theme_title,
            to_console_only=True  # Only show in console for comparison
        )
```

## Output Control

### Target-Specific Display

```python
# Display only in console (not in log files)
logger.code(
    code=debug_code,
    title="Debug Information",
    to_console_only=True
)

# Save only to log files (not displayed in console)
logger.code(
    code=config_dump,
    title="Configuration Dump",
    to_log_file_only=True
)
```

## Best Practices

### 1. Choose Appropriate Themes
- Use **dark themes** (`monokai`, `github-dark`) for development environments
- Use **light themes** (`github-light`, `solarized-light`) for documentation

### 2. Use Descriptive Titles
```python
# Good: Descriptive title
logger.code(code, title="User Authentication Function")

# Better: Include context
logger.code(code, title="User Authentication Function (v2.1 - OAuth2 Support)")
```

### 3. Leverage Line Ranges for Large Files
```python
# Show only relevant sections
logger.code_file(
    file_path="large_module.py",
    start_line=150,
    end_line=180,
    title="Error Handling Section"
)
```

### 4. Use Diff for Code Reviews
```python
# Perfect for code review logs
logger.diff(
    old_code=before_fix,
    new_code=after_fix,
    old_title="Bug Present",
    new_title="Bug Fixed",
    language="python"
)
```

### 5. Control Output Destination
```python
# Debug code only in console during development
logger.code(debug_snippet, to_console_only=True)

# Important code snapshots saved to files
logger.code(production_config, to_log_file_only=True)
```

## Integration with Existing Features

Code highlighting works seamlessly with pretty-loguru's existing features:

```python
# Works with different log levels
logger.info("Displaying critical function:")
logger.code(critical_code, language="python")

# Works with target-specific logging
logger.console.code(console_code, to_console_only=True)
logger.file.code(file_code, to_log_file_only=True)

# Integrates with Rich components
logger.code(api_code, language="python", title="API Handler")
logger.table("API Endpoints", endpoint_data)  # Show related table
```

The code highlighting feature makes pretty-loguru an excellent choice for development logging, code documentation, debugging sessions, and technical documentation generation.