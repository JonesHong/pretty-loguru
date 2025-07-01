#!/usr/bin/env python3
"""
Final cleanup of API inconsistencies in documentation
Focus on examples and actual usage, preserve API documentation references
"""

import os
import re
from pathlib import Path

def final_cleanup():
    """Clean up remaining API usage in examples and guides"""
    
    docs_dir = Path("docs")
    
    # Files that need specific attention
    target_files = [
        "docs/en/examples/basics/console-vs-file.md",
        "docs/en/examples/presets/index.md",
        "docs/examples/presets/index.md",
    ]
    
    for file_path_str in target_files:
        file_path = Path(file_path_str)
        if not file_path.exists():
            print(f"⚠️ File not found: {file_path}")
            continue
            
        print(f"🔧 Processing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix preset examples to use create_logger
            if "presets" in str(file_path):
                # Replace preset-specific logger_start calls
                content = re.sub(
                    r'logger_start\(preset="([^"]+)"\)',
                    r'logger = create_logger(\n    name="\1_demo",\n    log_path="\1_logs",\n    level="INFO"\n)',
                    content
                )
                content = re.sub(
                    r'logger_start\(preset="([^"]+)", folder="([^"]+)"\)',
                    r'logger = create_logger(\n    name="\1_demo",\n    log_path="\2",\n    level="INFO"\n)',
                    content
                )
                
            # Fix console-only examples
            if "console-vs-file" in str(file_path):
                content = re.sub(
                    r'logger_start\(console_only=True\)',
                    r'logger = create_logger(\n    name="console_demo",\n    log_path=None,  # Console only\n    level="INFO"\n)',
                    content
                )
                content = re.sub(
                    r'logger_start\(file_only=True\)',
                    r'logger = create_logger(\n    name="file_demo",\n    log_path="file_logs",\n    level="INFO",\n    console_output=False\n)',
                    content
                )
            
            # Update import statements if needed
            content = re.sub(
                r'from pretty_loguru import logger_start',
                'from pretty_loguru import create_logger',
                content
            )
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Updated: {file_path}")
            else:
                print(f"⏭️  No changes needed: {file_path}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    final_cleanup()
    print("\n🎉 Final API cleanup completed!")