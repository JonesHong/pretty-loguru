#!/usr/bin/env python3
"""
Fix remaining API consistency issues in documentation
Handles both English and Chinese documentation files
"""

import os
import re
from pathlib import Path

def fix_api_inconsistencies():
    """Fix API inconsistencies in documentation files"""
    
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs directory not found")
        return
    
    # Find all markdown files with logger_start
    files_to_fix = []
    for md_file in docs_dir.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'logger_start' in content:
                    files_to_fix.append(md_file)
        except Exception as e:
            print(f"⚠️ Error reading {md_file}: {e}")
    
    print(f"📋 Found {len(files_to_fix)} files to fix")
    
    for file_path in files_to_fix:
        print(f"🔧 Fixing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Replace incorrect import statements
            patterns_to_fix = [
                # Import fixes
                (r'from pretty_loguru import logger, logger_start', 'from pretty_loguru import create_logger'),
                (r'from pretty_loguru import logger_start', 'from pretty_loguru import create_logger'),
                
                # Function call fixes
                (r'component_name = logger_start\(', 'logger = create_logger(\n    name="demo",\n    log_path='),
                (r'logger_start\(\s*folder="([^"]+)"', r'logger = create_logger(\n    name="demo",\n    log_path="\1"'),
                (r'logger_start\(\s*folder=\'([^\']+)\'', r'logger = create_logger(\n    name="demo",\n    log_path="\1"'),
                (r'logger_start\(\)', 'logger = create_logger(\n    name="demo",\n    log_path="logs",\n    level="INFO"\n)'),
                
                # Parameter section fixes in documentation
                (r'### `logger_start\(\)` Parameters', '### `create_logger()` Parameters'),
                (r'def logger_start\(', 'def create_logger(\n    name: str,'),
                
                # Variable assignment fixes
                (r'component_name = logger = create_logger\(', 'logger = create_logger('),
                (r'component_name = .*?create_logger\([^)]*\)', 'logger = create_logger(\n    name="demo",\n    log_path="logs",\n    level="INFO"\n)'),
                
                # Legacy API references in text
                (r'使用 `logger_start\(\)` ', '使用 `create_logger()` '),
                (r'Usage of `logger_start\(\)`', 'Usage of `create_logger()`'),
                (r'Understand the usage of `logger_start\(\)`', 'Understand the usage of `create_logger()`'),
                
                # Documentation specific fixes
                (r'`logger_start\(\)` automatically', '`create_logger()` creates'),
                (r'### `logger_start\(\)` - Quick Initialization', '### `create_logger()` - Create Custom Logger'),
                (r'The most commonly used initialization method', 'Create a logger instance with specific name and configuration'),
            ]
            
            # Apply all pattern fixes
            for pattern, replacement in patterns_to_fix:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # Additional specific fixes for complex cases
            # Fix broken parameter documentation
            content = re.sub(
                r'logger = create_logger\(\s*name="demo",\s*log_path=([^,\)]+)[^}]*\}\)',
                r'logger = create_logger(\n    name="demo",\n    log_path=\1,\n    level="INFO"\n)',
                content,
                flags=re.MULTILINE | re.DOTALL
            )
            
            # Fix malformed function calls
            content = re.sub(
                r'logger = create_logger\(\s*name="demo",\s*log_path="([^"]+)"[^)]*(\s*\))?',
                r'logger = create_logger(\n    name="demo",\n    log_path="\1",\n    level="INFO"\n)',
                content,
                flags=re.MULTILINE
            )
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed: {file_path}")
            else:
                print(f"⏭️  No changes needed: {file_path}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n🎉 API consistency fix completed!")

if __name__ == "__main__":
    fix_api_inconsistencies()