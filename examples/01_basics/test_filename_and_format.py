import sys
from pathlib import Path
from loguru import logger as loguru_logger
from pretty_loguru.factory import create_logger
from pretty_loguru.core.config import LoggerConfig

# # Remove all default loguru handlers to ensure clean slate
# loguru_logger.remove()

# Scenario 1: Logger with explicit name
print("--- Scenario 1: Logger with explicit name ---")
explicit_logger = create_logger(name="MyServiceLogger", log_path="./test_logs")
explicit_logger.info("This is a log message from the explicit logger.")
explicit_logger.debug("A debug message from explicit logger.")
explicit_logger.error("An error from explicit logger.")

# Scenario 2: Logger without explicit name (inferred from filename)
print("\n--- Scenario 2: Logger without explicit name ---")
# To simulate a logger without an explicit name, we'll create a new logger
# and let it infer its name from this script's filename.
# We need to ensure it's a new instance to avoid conflicts with the first logger.
inferred_logger = create_logger(log_path="./test_logs")
inferred_logger.info("This is a log message from the inferred logger.")
inferred_logger.warning("A warning message from inferred logger.")

# Clean up loguru handlers to avoid interference in subsequent runs
# loguru_logger.remove()

test_logger = create_logger(log_path="./test_logs")
test_logger.info("This is a test log message from the test logger.")
test_logger.warning("This is a test warning message from the test logger.")


new_logger = create_logger( log_path="./test_logs",force_new_instance=True)
new_logger.info("This is a test log message from the new logger.")
new_logger.warning("This is a test warning message from the new logger.")

print("\nVerification steps:")
print("1. Check terminal output for format: 'name:function:line' or 'file:function:line'.")
print("2. Check 'test_logs' directory for log files:")
print("   - For Scenario 1: A file like '[MyServiceLogger]_YYYYMMDD-HHMMSS.log'")
print("   - For Scenario 2: A file like '[test_filename_and_format.py]_YYYYMMDD-HHMMSS.log'")
print("   (Note: The timestamp will vary)")
