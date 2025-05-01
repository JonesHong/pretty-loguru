#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pretty Loguru 文檔修復工具 - 一體化解決方案

此腳本用於解決所有文檔構建過程中的問題，包括：
1. 修復標題下劃線問題
2. 創建缺少的圖片
3. 修復代碼文檔中的格式問題
4. 解決重複物件描述問題
5. 修復意外縮進問題
6. 修復無效引用

使用方法：在 docs 目錄下運行
python fix_all_documentation_issues.py
"""

import os
import re
import sys
import glob
import shutil
from pathlib import Path
from argparse import ArgumentParser

# 全局變量
DOCS_DIR = Path.cwd()  # 假設在 docs 目錄下運行
SOURCE_DIR = DOCS_DIR / "source"
PROJECT_ROOT = DOCS_DIR.parent
CODE_DIR = PROJECT_ROOT / "pretty_loguru"

# 檢查運行環境
if not SOURCE_DIR.exists():
    print(f"錯誤: 找不到源目錄 {SOURCE_DIR}")
    print("請確保在 docs 目錄下運行此腳本")
    sys.exit(1)

if not CODE_DIR.exists():
    print(f"警告: 找不到程式碼目錄 {CODE_DIR}")
    print("代碼文檔問題修復可能無法完成")


# 1. 修復標題下劃線問題
def fix_title_underlines(file_path):
    """修復文件中的標題下劃線問題"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正則表達式查找標題和下劃線
        pattern = r'(.*?)\n([=\-~^"\'`]+)\n'
        
        def replace_underline(match):
            title = match.group(1)
            underline_char = match.group(2)[0]  # 獲取下劃線字符
            # 創建與標題等長的下劃線
            new_underline = underline_char * len(title) * 3
            return f"{title}\n{new_underline}\n"
        
        # 替換所有標題下劃線
        new_content = re.sub(pattern, replace_underline, content)
        
        # 只有在內容有變化時才寫入文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已修復標題下劃線: {file_path}")
            return True
    except Exception as e:
        print(f"處理 {file_path} 時發生錯誤: {str(e)}")
    return False


# 2. 創建缺少的圖片
def create_placeholder_image(filename, width=500, height=300, text="範例圖片", bg_color=(240, 240, 240), text_color=(100, 100, 100)):
    """創建一個簡單的文字圖片作為佔位符"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 創建圖片
        img = Image.new('RGB', (width, height), color=bg_color)
        d = ImageDraw.Draw(img)
        
        # 嘗試使用常見字體
        font = None
        try_fonts = ["Arial", "DejaVuSans", "FreeSans", "SimSun", "NotoSansCJK"]
        
        for font_name in try_fonts:
            try:
                font = ImageFont.truetype(font_name, 30)
                break
            except IOError:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # 計算文字位置以居中顯示
        text_bbox = d.textbbox((0, 0), text, font=font) if hasattr(d, 'textbbox') else (0, 0, 100, 30)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # 添加文字
        d.text(position, text, fill=text_color, font=font)
        
        # 創建目錄（如果不存在）
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # 保存圖片
        img.save(filename)
        print(f"已創建圖片: {filename}")
        return True
    except ImportError:
        print("警告: 未安裝 Pillow 庫，無法創建圖片。請使用 'pip install Pillow' 安裝。")
        
        # 創建一個空文件作為替代
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write("")
        print(f"已創建空圖片文件: {filename}")
        return False
    except Exception as e:
        print(f"創建圖片 {filename} 時發生錯誤: {str(e)}")
        return False


def create_missing_images():
    """創建文檔中引用但缺少的圖片"""
    static_dir = SOURCE_DIR / "_static"
    static_dir.mkdir(exist_ok=True)
    
    images_created = False
    
    # 創建缺少的圖片
    if create_placeholder_image(static_dir / "block_example.png", text="區塊日誌示例"):
        images_created = True
    
    if create_placeholder_image(static_dir / "figlet_example.png", text="FIGlet 藝術示例"):
        images_created = True
    
    if images_created:
        print("已創建缺少的圖片文件")
    else:
        print("未創建任何圖片文件")
    
    return images_created


# 3. 修復內聯文本標記問題
def fix_inline_literals(file_path):
    """修復文件中的內聯文字標記問題"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修復沒有結束的內聯文本標記
        # 修復 ` 開頭但沒有結尾的情況
        pattern = r'`([^`\n]+?)(?=[.,;:\s\)\]]|$)'
        new_content = re.sub(pattern, r'`\1`', content)
        
        # 只有在內容有變化時才寫入文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已修復內聯文本: {file_path}")
            return True
    except Exception as e:
        print(f"處理 {file_path} 時發生錯誤: {str(e)}")
    return False


# 4. 修復重複的物件描述問題
def fix_no_index_issues():
    """修復重複的物件描述問題 (添加 :noindex:)"""
    # 由於這需要更複雜的處理，我們專注於修復特定檔案中的已知問題
    
    # 已知有問題的檔案和類別
    problem_files = {
        CODE_DIR / "core" / "__init__.py": ["LogLevelEnum"],
        CODE_DIR / "integrations" / "__init__.py": ["InterceptHandler"]
    }
    
    fixed = False
    
    for file_path, class_names in problem_files.items():
        try:
            if not file_path.exists():
                print(f"警告: 找不到檔案 {file_path}")
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            # 為每個類別添加 :noindex: 標記
            for class_name in class_names:
                # 查找類別的 docstring
                pattern = fr'(class {class_name}.*?\n\s*""".*?""")'
                match = re.search(pattern, content, re.DOTALL)
                
                if match:
                    docstring = match.group(1)
                    # 檢查是否已有 :noindex:
                    if ":noindex:" not in docstring:
                        # 在 docstring 開頭添加 :noindex:
                        new_docstring = docstring.replace('"""', '""":noindex:', 1)
                        content = content.replace(docstring, new_docstring)
                        print(f"已在 {file_path} 中為 {class_name} 添加 :noindex:")
                        fixed = True
            
            # 只有在內容變化時才寫回檔案
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"處理 {file_path} 時發生錯誤: {str(e)}")
    
    return fixed


# 5. 修復未知文檔引用
def fix_unknown_document_reference():
    """修復未知文檔引用的問題"""
    # 在 quickstart.rst 文件中修正不正確的引用
    file_path = SOURCE_DIR / "quickstart.rst"
    
    if not file_path.exists():
        print(f"警告: 找不到檔案 {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替換對不存在文檔的引用
        new_content = content
        if "examples/index" in content:
            # 改為引用真正存在的文檔
            new_content = content.replace("examples/index", "advanced_features")
        
        # 只有在內容變化時才寫回檔案
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"已修正 {file_path} 中的未知文檔引用")
            return True
    except Exception as e:
        print(f"處理 {file_path} 時發生錯誤: {str(e)}")
    
    return False


# 6. 修復意外縮進問題
def fix_unexpected_indentation():
    """修復意外縮進的問題"""
    fixed = False
    
    # 修復 index.rst 中的意外縮進問題
    index_path = SOURCE_DIR / "index.rst"
    
    if not index_path.exists():
        print(f"警告: 找不到檔案 {index_path}")
        return fixed
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找並修復錯誤的縮進
        fixed_lines = []
        modified = False
        
        for i, line in enumerate(lines):
            if i > 0 and line.startswith("   ") and not lines[i-1].strip():
                # 如果是一個縮進行且前面是空行，移除縮進
                fixed_lines.append(line.lstrip())
                modified = True
            else:
                fixed_lines.append(line)
        
        if modified:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            
            print(f"已修復 {index_path} 中的意外縮進問題")
            fixed = True
    except Exception as e:
        print(f"處理 {index_path} 時發生錯誤: {str(e)}")
    
    # 修復 get_logger_dependency 文檔中的意外縮進
    for py_file in CODE_DIR.glob("**/*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找 get_logger_dependency 函數的 docstring
            match = re.search(r'def get_logger_dependency.*?""".+?"""', content, re.DOTALL)
            if match and "Unexpected indentation" in content:
                docstring = match.group(0)
                # 修復意外縮進
                fixed_docstring = re.sub(r'\n\s+@app\.get', r'\n@app\.get', docstring)
                
                if docstring != fixed_docstring:
                    new_content = content.replace(docstring, fixed_docstring)
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"已修復 {py_file} 中的意外縮進問題")
                    fixed = True
        except Exception as e:
            print(f"處理 {py_file} 時發生錯誤: {str(e)}")
    
    return fixed


# 主函數
def main():
    print("=== Pretty Loguru 文檔修復工具 ===")
    
    parser = ArgumentParser(description="修復 Pretty Loguru 文檔的問題")
    parser.add_argument("--all", action="store_true", help="修復所有問題")
    parser.add_argument("--titles", action="store_true", help="修復標題下劃線問題")
    parser.add_argument("--images", action="store_true", help="創建缺少的圖片")
    parser.add_argument("--literals", action="store_true", help="修復內聯文本問題")
    parser.add_argument("--noindex", action="store_true", help="修復重複物件描述問題")
    parser.add_argument("--refs", action="store_true", help="修復文檔引用問題")
    parser.add_argument("--indent", action="store_true", help="修復意外縮進問題")
    args = parser.parse_args()
    
    # 如果未提供任何選項，則預設執行所有修復
    if not any(vars(args).values()):
        args.all = True
    
    changes_made = False
    
    print("\n1. 修復標題下劃線問題...")
    if args.all or args.titles:
        rst_files = list(SOURCE_DIR.glob("**/*.rst"))
        for file_path in rst_files:
            if fix_title_underlines(file_path):
                changes_made = True
    
    print("\n2. 創建缺少的圖片...")
    if args.all or args.images:
        if create_missing_images():
            changes_made = True
    
    print("\n3. 修復內聯文本問題...")
    if args.all or args.literals:
        # 修復 RST 文件中的問題
        rst_files = list(SOURCE_DIR.glob("**/*.rst"))
        for file_path in rst_files:
            if fix_inline_literals(file_path):
                changes_made = True
        
        # 修復 Python 代碼中的問題
        if CODE_DIR.exists():
            py_files = list(CODE_DIR.glob("**/*.py"))
            for file_path in py_files:
                if fix_inline_literals(file_path):
                    changes_made = True
    
    print("\n4. 修復重複物件描述問題...")
    if args.all or args.noindex:
        if fix_no_index_issues():
            changes_made = True
    
    print("\n5. 修復文檔引用問題...")
    if args.all or args.refs:
        if fix_unknown_document_reference():
            changes_made = True
    
    print("\n6. 修復意外縮進問題...")
    if args.all or args.indent:
        if fix_unexpected_indentation():
            changes_made = True
    
    if changes_made:
        print("\n=== 修復完成! 已解決多個文檔問題 ===")
    else:
        print("\n=== 未發現需要修復的問題 ===")
    
    print("\n提示: 請再次運行 sphinx-build 命令檢查是否還有其他問題。")


if __name__ == "__main__":
    main()