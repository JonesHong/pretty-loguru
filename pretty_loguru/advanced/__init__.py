"""
Advanced API Module - Direct Access to Underlying Libraries

This module provides direct access to the underlying libraries (loguru, rich, art, pyfiglet)
for advanced users who need more control and flexibility beyond pretty-loguru's simplified API.

Design Philosophy:
- KISS principle: Simple, clear, and maintainable
- Integration over replacement: Expose original APIs without modification
- Familiar learning curve: Keep original library patterns intact
- Optional enhancement: Add minimal helper functions only when truly beneficial

Usage:
    # Direct library access (maintains original API)
    from pretty_loguru.advanced import loguru, rich, art, pyfiglet
    
    # Use exactly like the original libraries
    console = rich.Console()
    logger = loguru.logger
    
    # Optional: Enhanced integration helpers
    from pretty_loguru.advanced.helpers import create_rich_logger
"""

# Core philosophy: Re-export original libraries with minimal modification
# This ensures 100% compatibility and familiar usage patterns

# Loguru - Core logging functionality
try:
    import loguru
    from loguru import logger as loguru_logger
    HAS_LOGURU = True
except ImportError:
    loguru = None
    loguru_logger = None
    HAS_LOGURU = False

# Rich - Terminal formatting and display
try:
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, track
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.columns import Columns
    from rich.layout import Layout
    from rich.live import Live
    from rich.prompt import Prompt
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    rich = None
    Console = Panel = Table = Progress = track = None
    Syntax = Tree = Columns = Layout = Live = Prompt = Text = None
    HAS_RICH = False

# Art - ASCII art generation
try:
    import art
    from art import text2art, tprint, FONT_NAMES
    HAS_ART = True
except ImportError:
    art = None
    text2art = tprint = FONT_NAMES = None
    HAS_ART = False

# PyFiglet - FIGlet font rendering
try:
    import pyfiglet
    from pyfiglet import Figlet, FigletFont
    HAS_PYFIGLET = True
except ImportError:
    pyfiglet = None
    Figlet = FigletFont = None
    HAS_PYFIGLET = False

# Availability flags for conditional usage
AVAILABLE_LIBRARIES = {
    'loguru': HAS_LOGURU,
    'rich': HAS_RICH,
    'art': HAS_ART,
    'pyfiglet': HAS_PYFIGLET
}

# Clean exports - only export what's available
__all__ = ['AVAILABLE_LIBRARIES']

if HAS_LOGURU:
    __all__.extend(['loguru', 'loguru_logger'])

if HAS_RICH:
    __all__.extend([
        'rich', 'Console', 'Panel', 'Table', 'Progress', 'track',
        'Syntax', 'Tree', 'Columns', 'Layout', 'Live', 'Prompt', 'Text'
    ])

if HAS_ART:
    __all__.extend(['art', 'text2art', 'tprint', 'FONT_NAMES'])

if HAS_PYFIGLET:
    __all__.extend(['pyfiglet', 'Figlet', 'FigletFont'])

def get_available_libraries():
    """
    Get a list of available libraries for advanced usage.
    
    Returns:
        dict: Dictionary with library names and their availability status
        
    Example:
        >>> from pretty_loguru.advanced import get_available_libraries
        >>> available = get_available_libraries()
        >>> if available['rich']:
        ...     from pretty_loguru.advanced import Console
        ...     console = Console()
    """
    return AVAILABLE_LIBRARIES.copy()

def check_library(library_name: str) -> bool:
    """
    Check if a specific library is available.
    
    Args:
        library_name: Name of the library ('loguru', 'rich', 'art', 'pyfiglet')
        
    Returns:
        bool: True if library is available, False otherwise
        
    Example:
        >>> from pretty_loguru.advanced import check_library
        >>> if check_library('rich'):
        ...     # Use rich components
        ...     pass
    """
    return AVAILABLE_LIBRARIES.get(library_name, False)

__all__.extend(['get_available_libraries', 'check_library'])

# Simple usage examples in docstring
__doc__ += """

Quick Examples:

1. Direct Rich Usage (exactly like original):
    >>> from pretty_loguru.advanced import Console, Table
    >>> console = Console()
    >>> table = Table(title="My Data")
    >>> table.add_column("Name")
    >>> table.add_column("Value")
    >>> table.add_row("CPU", "75%")
    >>> console.print(table)

2. Direct Loguru Usage (exactly like original):
    >>> from pretty_loguru.advanced import loguru_logger
    >>> loguru_logger.info("Direct loguru usage")
    >>> loguru_logger.add("file.log", rotation="1 MB")

3. Direct Art Usage (exactly like original):
    >>> from pretty_loguru.advanced import text2art, tprint
    >>> ascii_art = text2art("Hello", font="slant")
    >>> tprint("World", font="block")

4. Check Availability:
    >>> from pretty_loguru.advanced import check_library
    >>> if check_library('pyfiglet'):
    ...     from pretty_loguru.advanced import Figlet
    ...     f = Figlet(font='slant')
    ...     print(f.renderText('Hello'))
"""