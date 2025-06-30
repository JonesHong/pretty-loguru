"""
Advanced Integration Helpers

Minimal helper functions that bridge pretty-loguru with underlying libraries.
These helpers maintain KISS principle and only add value where integration provides clear benefits.

Philosophy:
- Add helpers only when they solve real integration pain points
- Keep function signatures simple and predictable
- Maintain compatibility with original library patterns
- Provide clear value over manual integration
"""

from typing import Any, Optional, Dict, List, Union
from ..core.base import get_console
from . import (
    HAS_RICH, HAS_LOGURU, HAS_ART, HAS_PYFIGLET,
    Console, Table, Panel, loguru_logger
)

def create_rich_table_log(
    logger_instance: Any,
    title: str,
    data: List[Dict[str, Any]],
    log_level: str = "INFO",
    **table_kwargs
) -> None:
    """
    Create a Rich table and log it using pretty-loguru logger.
    
    This helper bridges Rich tables with pretty-loguru logging in a simple way.
    Uses original Rich Table API with minimal wrapper for logging integration.
    
    Args:
        logger_instance: Pretty-loguru logger instance
        title: Table title
        data: List of dictionaries representing table rows
        log_level: Log level for the table log entry
        **table_kwargs: Additional arguments passed directly to Rich Table
        
    Example:
        >>> from pretty_loguru import create_logger
        >>> from pretty_loguru.advanced.helpers import create_rich_table_log
        >>> 
        >>> logger = create_logger("app")
        >>> data = [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}]
        >>> create_rich_table_log(logger, "Scores", data, show_header=True)
    """
    if not HAS_RICH:
        logger_instance.warning("Rich library not available, skipping table display")
        return
        
    if not data:
        logger_instance.warning(f"Table '{title}' has no data to display")
        return
    
    # Use Rich Table API exactly as intended
    table = Table(title=title, **table_kwargs)
    
    # Auto-add columns from first row
    for key in data[0].keys():
        table.add_column(str(key))
    
    # Add all rows
    for row in data:
        table.add_row(*[str(v) for v in row.values()])
    
    # Display via pretty-loguru's console
    console = get_console()
    
    # Log the table creation
    logger_instance.log(log_level, f"Displaying table: {title}")
    
    # Print the actual table
    console.print(table)
    
    # Also create a simple text version for file logs
    table_text = f"Table: {title}\n"
    for row in data:
        table_text += " | ".join(f"{k}: {v}" for k, v in row.items()) + "\n"
    
    logger_instance.file_info(table_text)

def create_mixed_ascii_panel(
    logger_instance: Any,
    text: str,
    panel_title: Optional[str] = None,
    ascii_font: str = "standard",
    panel_style: str = "cyan",
    log_level: str = "INFO"
) -> None:
    """
    Create ASCII art inside a Rich panel and log it.
    
    Simple integration of art + rich + pretty-loguru logging.
    Uses original library APIs with minimal coordination.
    
    Args:
        logger_instance: Pretty-loguru logger instance
        text: Text to convert to ASCII art
        panel_title: Optional panel title
        ascii_font: Font for ASCII art (art library font)
        panel_style: Rich panel border style
        log_level: Log level for the log entry
        
    Example:
        >>> from pretty_loguru import create_logger
        >>> from pretty_loguru.advanced.helpers import create_mixed_ascii_panel
        >>> 
        >>> logger = create_logger("app")
        >>> create_mixed_ascii_panel(logger, "SUCCESS", "Status Report", "slant", "green")
    """
    if not HAS_ART:
        logger_instance.warning("Art library not available, falling back to plain text")
        ascii_text = text
    else:
        from . import text2art
        try:
            ascii_text = text2art(text, font=ascii_font)
        except Exception as e:
            logger_instance.warning(f"ASCII art generation failed: {e}, using plain text")
            ascii_text = text
    
    if not HAS_RICH:
        # Fallback to simple logging
        logger_instance.log(log_level, f"{panel_title or 'ASCII Art'}:\n{ascii_text}")
        return
    
    # Use Rich Panel API exactly as intended
    panel = Panel(
        ascii_text,
        title=panel_title,
        border_style=panel_style
    )
    
    # Display and log
    console = get_console()
    logger_instance.log(log_level, f"Displaying ASCII panel: {panel_title or text}")
    console.print(panel)
    
    # File log version
    file_content = f"{panel_title or 'ASCII Art'}:\n{ascii_text}"
    logger_instance.file_info(file_content)

def create_loguru_rich_sink(
    console: Optional[Console] = None,
    **sink_kwargs
) -> Console:
    """
    Create a Rich Console configured as a Loguru sink.
    
    This helper makes it easy to use Rich Console as a Loguru output target
    while maintaining both libraries' original patterns.
    
    Args:
        console: Optional existing Rich Console instance
        **sink_kwargs: Additional arguments for loguru.add()
        
    Returns:
        Console: The Rich Console instance that can be used as a Loguru sink
        
    Example:
        >>> from pretty_loguru.advanced import loguru_logger
        >>> from pretty_loguru.advanced.helpers import create_loguru_rich_sink
        >>> 
        >>> # Create Rich console for Loguru
        >>> rich_console = create_loguru_rich_sink()
        >>> 
        >>> # Add as Loguru sink (exactly like original Loguru API)
        >>> loguru_logger.add(rich_console.print, colorize=True, format="{message}")
        >>> loguru_logger.info("Rich formatted log")
    """
    if not HAS_RICH:
        raise ImportError("Rich library is required for this helper")
    
    if console is None:
        console = Console()
    
    return console

def quick_figlet_log(
    logger_instance: Any,
    text: str,
    font: str = "slant",
    log_level: str = "INFO"
) -> None:
    """
    Quick FIGlet text generation and logging.
    
    Simplest possible integration of pyfiglet with pretty-loguru logging.
    
    Args:
        logger_instance: Pretty-loguru logger instance
        text: Text to convert to FIGlet
        font: FIGlet font name
        log_level: Log level for the log entry
        
    Example:
        >>> from pretty_loguru import create_logger
        >>> from pretty_loguru.advanced.helpers import quick_figlet_log
        >>> 
        >>> logger = create_logger("app")
        >>> quick_figlet_log(logger, "READY", "big")
    """
    if not HAS_PYFIGLET:
        logger_instance.warning("PyFiglet library not available, using plain text")
        figlet_text = text
    else:
        from . import Figlet
        try:
            f = Figlet(font=font)
            figlet_text = f.renderText(text)
        except Exception as e:
            logger_instance.warning(f"FIGlet generation failed: {e}, using plain text")
            figlet_text = text
    
    logger_instance.log(log_level, f"FIGlet text:\n{figlet_text}")

# Keep the helper count minimal - only add helpers that provide clear integration value
__all__ = [
    'create_rich_table_log',
    'create_mixed_ascii_panel', 
    'create_loguru_rich_sink',
    'quick_figlet_log'
]