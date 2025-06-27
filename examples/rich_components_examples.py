"""
Rich Components Integration Examples

This example demonstrates the new Rich components integrated into pretty-loguru:
- Table: Display tabular data with rich formatting
- Tree: Show hierarchical data structures
- Columns: Display items in multiple columns
- Progress: Track progress of operations

These components maintain the same API patterns as other pretty-loguru features
while providing powerful Rich visualization capabilities.
"""

import sys
import time
import random
from pathlib import Path

# Use local libraries for testing
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pretty_loguru import (
    create_logger,
    print_table,
    print_tree, 
    print_columns,
    LoggerProgress
)

def example_1_table_displays():
    """Demonstrate table display functionality"""
    print("\n--- Example 1: Rich Table Displays ---\n")
    
    logger = create_logger(
        "table_demo",
        log_path="./logs",
        subdirectory="rich_examples"
    )
    
    # 1.1 Basic table
    users_data = [
        {"name": "Alice", "age": 30, "role": "Developer", "status": "Active"},
        {"name": "Bob", "age": 25, "role": "Designer", "status": "Active"},
        {"name": "Charlie", "age": 35, "role": "Manager", "status": "On Leave"},
        {"name": "Diana", "age": 28, "role": "Developer", "status": "Active"}
    ]
    
    logger.table("Team Members", users_data, show_lines=True)
    
    # 1.2 Table with custom headers
    performance_data = [
        {"cpu": "45%", "memory": "2.1GB", "disk": "85%"},
        {"cpu": "12%", "memory": "1.8GB", "disk": "92%"},
        {"cpu": "78%", "memory": "3.2GB", "disk": "67%"}
    ]
    
    logger.table(
        "Server Performance",
        performance_data,
        headers=["CPU Usage", "Memory", "Disk Usage"],
        show_header=True,
        show_lines=False
    )
    
    # 1.3 Console-only table
    debug_data = [
        {"endpoint": "/api/users", "method": "GET", "status": 200, "time": "45ms"},
        {"endpoint": "/api/login", "method": "POST", "status": 401, "time": "120ms"}
    ]
    
    logger.console_table("Debug API Calls", debug_data)
    
    # 1.4 File-only table
    logger.file_table("Internal Metrics", [
        {"metric": "requests_per_second", "value": 150},
        {"metric": "error_rate", "value": "0.02%"}
    ])
    
    # 1.5 Direct function usage (without logger)
    direct_data = [
        {"product": "Widget A", "price": "$29.99", "stock": 150},
        {"product": "Widget B", "price": "$39.99", "stock": 89}
    ]
    
    print_table("Direct Table Call", direct_data, show_lines=True)

def example_2_tree_structures():
    """Demonstrate tree structure display"""
    print("\n--- Example 2: Tree Structure Displays ---\n")
    
    logger = create_logger("tree_demo", log_path="./logs", subdirectory="rich_examples")
    
    # 2.1 System status tree
    system_status = {
        "Application": {
            "Web Server": "Running (Port 8000)",
            "API Server": "Running (Port 3000)",
            "Background Workers": {
                "Queue Processor": "Running",
                "Email Service": "Running",
                "Report Generator": "Stopped"
            }
        },
        "Infrastructure": {
            "Database": {
                "Primary": "Running",
                "Replica": "Syncing"
            },
            "Cache": "Running",
            "Load Balancer": "Running"
        }
    }
    
    logger.tree("System Overview", system_status)
    
    # 2.2 File system structure
    project_structure = {
        "pretty-loguru": {
            "src": {
                "core": "Logger core functionality",
                "formats": "Rich formatting modules",
                "integrations": "Framework integrations"
            },
            "examples": "Usage examples",
            "tests": "Test suites",
            "docs": "Documentation"
        }
    }
    
    logger.tree("Project Structure", project_structure)
    
    # 2.3 Error hierarchy
    error_breakdown = {
        "Errors (Last 24h)": {
            "Client Errors (4xx)": {
                "404 Not Found": "12 occurrences",
                "401 Unauthorized": "5 occurrences",
                "400 Bad Request": "8 occurrences"
            },
            "Server Errors (5xx)": {
                "500 Internal Error": "2 occurrences",
                "503 Service Unavailable": "1 occurrence"
            }
        }
    }
    
    logger.console_tree("Error Analysis", error_breakdown)

def example_3_column_layouts():
    """Demonstrate column layout functionality"""
    print("\n--- Example 3: Column Layouts ---\n")
    
    logger = create_logger("columns_demo", log_path="./logs", subdirectory="rich_examples")
    
    # 3.1 Available features
    features = [
        "Rich Tables", "ASCII Art", "Progress Bars", "Tree Views",
        "Block Formatting", "FIGlet Text", "Color Support", "File Logging",
        "Multiple Loggers", "Proxy Pattern", "Uvicorn Integration", "FastAPI Support"
    ]
    
    logger.columns("Available Features", features, columns=3)
    
    # 3.2 Configuration options
    config_options = [
        "log_path", "rotation", "retention", "level", "format",
        "subdirectory", "preset", "compression", "use_proxy", "start_cleaner"
    ]
    
    logger.columns("Configuration Options", config_options, columns=2)
    
    # 3.3 Supported log levels
    log_levels = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
    
    logger.columns("Log Levels", log_levels, columns=4)
    
    # 3.4 File-only columns
    dependencies = ["loguru", "rich", "art", "pyfiglet", "matplotlib"]
    logger.file_columns("Dependencies", dependencies, columns=3)

def example_4_progress_tracking():
    """Demonstrate progress tracking functionality"""
    print("\n--- Example 4: Progress Tracking ---\n")
    
    logger = create_logger("progress_demo", log_path="./logs", subdirectory="rich_examples")
    
    # 4.1 Basic progress context
    logger.info("Starting data processing simulation...")
    
    with logger.progress.progress_context("Processing data files", 50) as update:
        for i in range(50):
            # Simulate varying processing time
            time.sleep(random.uniform(0.01, 0.05))
            update(1)
    
    # 4.2 Batch processing with track_list
    logger.info("Starting batch processing simulation...")
    
    batch_items = [f"item_{i:03d}" for i in range(25)]
    processed_items = []
    
    for item in logger.progress.track_list(batch_items, "Processing batch items"):
        # Simulate item processing
        time.sleep(random.uniform(0.02, 0.08))
        processed_items.append(f"processed_{item}")
    
    logger.success(f"Batch processing completed: {len(processed_items)} items processed")
    
    # 4.3 Multi-step process
    steps = ["Initialize", "Load Config", "Connect DB", "Process Data", "Generate Report"]
    
    with logger.progress.progress_context("Multi-step Process", len(steps)) as update:
        for step in steps:
            logger.info(f"Executing: {step}")
            time.sleep(random.uniform(0.1, 0.3))
            update(1)
    
    # 4.4 File download simulation
    with logger.progress.progress_context("Downloading files", 100) as update:
        downloaded = 0
        while downloaded < 100:
            # Simulate download chunks
            chunk_size = random.randint(1, 10)
            chunk_size = min(chunk_size, 100 - downloaded)
            downloaded += chunk_size
            
            time.sleep(0.02)
            update(chunk_size)

def example_5_mixed_rich_features():
    """Combine different Rich features in real-world scenarios"""
    print("\n--- Example 5: Mixed Rich Features ---\n")
    
    logger = create_logger("mixed_demo", log_path="./logs", subdirectory="rich_examples")
    
    # 5.1 Application startup report
    logger.info("Application startup initiated")
    
    # Show configuration as tree
    config_tree = {
        "Application Config": {
            "Environment": "production",
            "Debug Mode": "disabled",
            "Database": {
                "Host": "db.example.com",
                "Port": "5432",
                "SSL": "enabled"
            },
            "Cache": {
                "Redis": "redis.example.com:6379",
                "TTL": "3600 seconds"
            }
        }
    }
    
    logger.tree("Startup Configuration", config_tree)
    
    # Simulate initialization steps with progress
    init_steps = ["Loading config", "Connecting to DB", "Starting cache", "Loading routes", "Ready"]
    
    with logger.progress.progress_context("Initializing application", len(init_steps)) as update:
        for step in init_steps:
            logger.info(f"Step: {step}")
            time.sleep(0.2)
            update(1)
    
    # Show performance metrics as table
    metrics_data = [
        {"component": "Web Server", "status": "Healthy", "response_time": "45ms", "cpu": "15%"},
        {"component": "Database", "status": "Healthy", "response_time": "12ms", "cpu": "8%"},
        {"component": "Cache", "status": "Healthy", "response_time": "2ms", "cpu": "3%"},
        {"component": "Queue", "status": "Warning", "response_time": "250ms", "cpu": "25%"}
    ]
    
    logger.table("System Health Check", metrics_data, show_lines=True)
    
    # Show available endpoints in columns
    endpoints = [
        "/api/users", "/api/auth/login", "/api/auth/logout", "/api/products",
        "/api/orders", "/api/reports", "/api/health", "/api/metrics"
    ]
    
    logger.columns("Available API Endpoints", endpoints, columns=2)
    
    logger.success("Application startup completed successfully")

def example_6_target_specific_outputs():
    """Demonstrate console-only and file-only Rich components"""
    print("\n--- Example 6: Target-Specific Rich Outputs ---\n")
    
    logger = create_logger("targets_demo", log_path="./logs", subdirectory="rich_examples")
    
    # 6.1 Console-only rich displays (for debugging)
    debug_data = [
        {"variable": "user_count", "value": 1520, "type": "int"},
        {"variable": "cache_hit_rate", "value": "94.5%", "type": "float"},
        {"variable": "last_update", "value": "2025-06-27 10:30:45", "type": "datetime"}
    ]
    
    logger.console_table("Debug Variables", debug_data)
    
    debug_tree = {
        "Debug Info": {
            "Memory Usage": "2.1GB / 8GB",
            "Active Connections": "45",
            "Queue Status": {
                "Pending": "12 jobs",
                "Processing": "3 jobs"
            }
        }
    }
    
    logger.console_tree("Runtime Debug Info", debug_tree)
    
    # 6.2 File-only rich data (for reports)
    report_data = [
        {"date": "2025-06-26", "users": 1450, "revenue": "$12,450", "errors": 3},
        {"date": "2025-06-25", "users": 1380, "revenue": "$11,200", "errors": 1},
        {"date": "2025-06-24", "users": 1520, "revenue": "$13,100", "errors": 5}
    ]
    
    logger.file_table("Daily Report Summary", report_data)
    
    # 6.3 Mixed output demonstration
    logger.info("Generating daily report...")
    
    # Progress shown on console
    with logger.progress.progress_context("Collecting metrics", 20) as update:
        for i in range(20):
            time.sleep(0.05)
            update(1)
    
    # Detailed data saved to file only
    detailed_metrics = [
        {"hour": f"{h:02d}:00", "requests": random.randint(100, 500), "errors": random.randint(0, 5)}
        for h in range(24)
    ]
    
    logger.file_table("Hourly Metrics (Detailed)", detailed_metrics)
    
    # Summary shown on both console and file
    summary_data = [
        {"metric": "Total Requests", "value": sum(m["requests"] for m in detailed_metrics)},
        {"metric": "Total Errors", "value": sum(m["errors"] for m in detailed_metrics)},
        {"metric": "Error Rate", "value": f"{(sum(m['errors'] for m in detailed_metrics) / sum(m['requests'] for m in detailed_metrics) * 100):.2f}%"}
    ]
    
    logger.table("Daily Summary", summary_data)

def main():
    """Run all Rich components examples"""
    print("=== Pretty-Loguru Rich Components Examples ===")
    print("Demonstrating integrated Rich functionality\n")
    
    # Run examples
    example_1_table_displays()
    example_2_tree_structures() 
    example_3_column_layouts()
    example_4_progress_tracking()
    example_5_mixed_rich_features()
    example_6_target_specific_outputs()
    
    print("\n=== Rich Components Examples Complete ===")
    print("Check ./logs/rich_examples/ for log files")
    print("\nNew logger methods available:")
    print("- logger.table(title, data, **kwargs)")
    print("- logger.tree(title, tree_data, **kwargs)")  
    print("- logger.columns(title, items, columns=3, **kwargs)")
    print("- logger.progress.progress_context(description, total)")
    print("- logger.progress.track_list(items, description)")
    print("\nAll methods support console-only and file-only variants:")
    print("- logger.console_table(), logger.file_table()")
    print("- logger.console_tree(), logger.file_tree()")
    print("- logger.console_columns(), logger.file_columns()")

if __name__ == "__main__":
    main()