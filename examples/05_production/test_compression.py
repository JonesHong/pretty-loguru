import sys
import time
from pathlib import Path
from pretty_loguru.factory import create_logger
from pretty_loguru.core.presets import get_preset_config

# Add project root to sys.path for module discovery
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# Create a logger with a small rotation to trigger compression quickly
# Using 'detailed' preset which now has the loguru_suffix time_source
logger = create_logger(
    name="CompressionTest",
    log_path="./test_logs",
    rotation="1 KB",  # Small size to force rotation
    retention="1 day",
    preset="detailed"
)

logger.info("Starting compression test...")

# Log many messages to trigger rotation
for i in range(1000):
    logger.info(f"Test message {i}: This is a long line to quickly fill up the log file and trigger rotation.")
    time.sleep(0.001) # Small delay to ensure distinct timestamps if needed

logger.info("Compression test finished. Check test_logs directory.")

# Give some time for Loguru to process the last rotation/compression
time.sleep(2)

print("\nVerification steps:")
print("1. Check 'test_logs' directory for compressed log files.")
print("2. Expected file names should be like: '[CompressionTest]YYYYMMDD-HHMMSS.log'")
print("   (The YYYYMMDD-HHMMSS part should correspond to the timestamp when the file was rotated by Loguru)")