"""
Advanced Usage Examples - Direct Library Access

This example demonstrates how to use pretty-loguru's advanced module to access
underlying libraries (loguru, rich, art, pyfiglet) directly for power users.

Design Philosophy:
- Keep original library learning curves intact
- Provide direct access without modification
- Add minimal helpers only where integration adds clear value
"""

import sys
from pathlib import Path

# Use local libraries for testing
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import time
from typing import Dict, Any, List

# Basic pretty-loguru import
from pretty_loguru import create_logger

# Import advanced module for direct library access
from pretty_loguru import advanced

def example_1_check_availability():
    """Check which advanced libraries are available"""
    print("\n--- Example 1: Library Availability Check ---\n")
    
    # Simple availability check
    available = advanced.get_available_libraries()
    print("Available libraries:")
    for lib, status in available.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {lib}: {'Available' if status else 'Not installed'}")
    
    # Individual library checks
    if advanced.check_library('rich'):
        print("\nRich is available - can use rich components!")
    
    if advanced.check_library('loguru'):
        print("Loguru is available - can use raw loguru features!")

def example_2_direct_rich_usage():
    """Use Rich components exactly like the original library"""
    print("\n--- Example 2: Direct Rich Usage ---\n")
    
    if not advanced.check_library('rich'):
        print("Rich not available, skipping this example")
        return
    
    # Import Rich components - exactly like original Rich
    from pretty_loguru.advanced import Console, Table, Panel, Progress, track
    
    # Use Rich exactly as documented in Rich's own docs
    console = Console()
    
    # 1. Simple Rich console usage
    console.print("Hello from [bold red]Rich[/bold red]!", style="bold blue")
    
    # 2. Rich Table - exactly like Rich documentation
    table = Table(title="Server Stats", show_header=True, header_style="bold magenta")
    table.add_column("Service", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("CPU %", justify="right", style="green")
    table.add_column("Memory", justify="right", style="yellow")
    
    # Add some data
    services = [
        ("Web Server", "Running", "15%", "512MB"),
        ("Database", "Running", "45%", "2.1GB"),
        ("Cache", "Running", "8%", "256MB"),
        ("API Gateway", "Warning", "78%", "1.8GB")
    ]
    
    for service in services:
        table.add_row(*service)
    
    console.print(table)
    
    # 3. Rich Panel - exactly like Rich documentation
    panel = Panel.fit(
        "[bold yellow]System Alert[/bold yellow]\n\nHigh CPU usage detected on API Gateway",
        border_style="red"
    )
    console.print(panel)
    
    # 4. Rich Progress - exactly like Rich documentation
    console.print("\nProcessing data...")
    for i in track(range(20), description="Processing..."):
        time.sleep(0.05)  # Simulate work

def example_3_direct_loguru_usage():
    """Use Loguru exactly like the original library"""
    print("\n--- Example 3: Direct Loguru Usage ---\n")
    
    if not advanced.check_library('loguru'):
        print("Loguru not available, skipping this example")
        return
    
    # Import Loguru - exactly like original Loguru
    from pretty_loguru.advanced import loguru_logger
    
    # Use Loguru exactly as documented in Loguru's own docs
    # Configure exactly like original Loguru
    loguru_logger.add("advanced_example.log", rotation="1 MB", retention="10 days")
    
    # Log exactly like original Loguru
    loguru_logger.info("This is direct Loguru usage")
    loguru_logger.warning("Direct access to all Loguru features")
    
    # Advanced Loguru features - exactly like original
    logger_with_context = loguru_logger.bind(user_id="12345", request_id="abc-123")
    logger_with_context.info("Logged with context")
    
    # Custom format - exactly like original Loguru
    loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
        level="DEBUG"
    )
    loguru_logger.debug("Custom formatted message")

def example_4_direct_art_usage():
    """Use Art library exactly like the original"""
    print("\n--- Example 4: Direct Art Usage ---\n")
    
    if not advanced.check_library('art'):
        print("Art library not available, skipping this example")
        return
    
    # Import Art components - exactly like original Art
    from pretty_loguru.advanced import text2art, tprint, FONT_NAMES
    
    # Use Art exactly as documented in Art's own docs
    print("Available fonts:", len(FONT_NAMES))
    
    # Generate ASCII art - exactly like original Art
    ascii_text = text2art("DIRECT", font="slant")
    print(ascii_text)
    
    # Direct print - exactly like original Art
    tprint("ART", font="block")
    
    # Try different fonts
    for font in ["standard", "small", "big"][:2]:  # Limit for example
        print(f"\nFont: {font}")
        tprint("TEST", font=font)

def example_5_direct_pyfiglet_usage():
    """Use PyFiglet exactly like the original library"""
    print("\n--- Example 5: Direct PyFiglet Usage ---\n")
    
    if not advanced.check_library('pyfiglet'):
        print("PyFiglet not available, skipping this example")
        return
    
    # Import PyFiglet - exactly like original PyFiglet
    from pretty_loguru.advanced import Figlet, pyfiglet
    
    # Use PyFiglet exactly as documented in PyFiglet's own docs
    f = Figlet(font='slant')
    figlet_text = f.renderText('FIGLET')
    print(figlet_text)
    
    # Different fonts - exactly like original PyFiglet
    for font_name in ['standard', 'big', 'small']:
        try:
            f = Figlet(font=font_name)
            print(f"Font: {font_name}")
            print(f.renderText('TEST'))
        except Exception as e:
            print(f"Font {font_name} failed: {e}")

def example_6_integration_helpers():
    """Use the minimal integration helpers"""
    print("\n--- Example 6: Integration Helpers ---\n")
    
    # Create a pretty-loguru logger
    logger = create_logger("advanced_demo", log_path="./logs", subdirectory="advanced")
    
    # Use integration helpers
    from pretty_loguru.advanced.helpers import (
        create_rich_table_log,
        create_mixed_ascii_panel,
        quick_figlet_log
    )
    
    # 1. Rich table integrated with logging
    if advanced.check_library('rich'):
        data = [
            {"name": "Alice", "score": 95, "status": "Active"},
            {"name": "Bob", "score": 87, "status": "Active"},
            {"name": "Charlie", "score": 92, "status": "Inactive"}
        ]
        
        create_rich_table_log(
            logger, 
            "User Scores", 
            data, 
            log_level="INFO",
            show_header=True,
            show_lines=True
        )
    
    # 2. ASCII art in Rich panel
    if advanced.check_library('art') and advanced.check_library('rich'):
        create_mixed_ascii_panel(
            logger,
            "SUCCESS",
            panel_title="Operation Status",
            ascii_font="slant",
            panel_style="green"
        )
    
    # 3. Quick FIGlet logging
    if advanced.check_library('pyfiglet'):
        quick_figlet_log(logger, "DONE", font="big")

def example_7_mixed_advanced_usage():
    """Combine pretty-loguru with direct library access"""
    print("\n--- Example 7: Mixed Advanced Usage ---\n")
    
    # Use pretty-loguru for basic logging
    logger = create_logger("mixed_demo", log_path="./logs")
    logger.info("Starting mixed usage example")
    
    # Use Rich directly for complex layouts
    if advanced.check_library('rich'):
        from pretty_loguru.advanced import Console, Layout, Panel
        
        console = Console()
        layout = Layout()
        
        layout.split_column(
            Layout(Panel("Top Panel", border_style="red"), name="top"),
            Layout(Panel("Bottom Panel", border_style="blue"), name="bottom")
        )
        
        console.print(layout)
        logger.info("Displayed complex Rich layout")
    
    # Use Loguru directly for advanced filtering
    if advanced.check_library('loguru'):
        from pretty_loguru.advanced import loguru_logger
        
        # Advanced Loguru feature not available in pretty-loguru
        def custom_filter(record):
            return record["level"].name == "ERROR"
        
        loguru_logger.add("errors_only.log", filter=custom_filter)
        loguru_logger.error("This will be logged to errors_only.log")
        loguru_logger.info("This will NOT be logged to errors_only.log")
    
    logger.success("Mixed usage example completed")

def main():
    """Run all advanced usage examples"""
    print("=== Pretty-Loguru Advanced Usage Examples ===")
    print("Direct access to underlying libraries for power users\n")
    
    # Run examples
    example_1_check_availability()
    example_2_direct_rich_usage()
    example_3_direct_loguru_usage()
    example_4_direct_art_usage()
    example_5_direct_pyfiglet_usage()
    example_6_integration_helpers()
    example_7_mixed_advanced_usage()
    
    print("\n=== Advanced Examples Complete ===")
    print("Check ./logs directory for log files")

if __name__ == "__main__":
    main()