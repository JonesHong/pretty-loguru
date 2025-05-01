#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pretty Loguru 文檔構建腳本

這個腳本自動化以下流程：
1. 刪除現有的構建目錄
2. 從源碼重新生成 API 文檔
3. 提取繁體中文文檔並準備英文翻譯
4. 構建繁體中文(主)和英文(次)文檔
"""

import os
import sys
import shutil
import subprocess
import glob
from pathlib import Path
from argparse import ArgumentParser

# 定義常數
PROJECT_ROOT = Path(__file__).parent.parent  # 假設腳本在 docs 目錄下
DOCS_DIR = PROJECT_ROOT / "docs"
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"
API_DIR = SOURCE_DIR / "api"
LOCALE_DIR = SOURCE_DIR / "locale"
GETTEXT_DIR = BUILD_DIR / "gettext"


def run_command(cmd, cwd=None, check=True):
    """執行命令並輸出結果"""
    print(f"執行: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"警告/錯誤: {result.stderr}", file=sys.stderr)
    return result


def clean_build_directory():
    """清理構建目錄"""
    print("\n==== 清理構建目錄 ====")
    
    if BUILD_DIR.exists():
        print(f"刪除目錄: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)
    
    BUILD_DIR.mkdir(exist_ok=True)
    print("構建目錄已清理完成")


def regenerate_api_docs():
    """根據程式碼重新生成 API 文檔"""
    print("\n==== 重新生成 API 文檔 ====")
    
    # 確保 API 目錄存在
    API_DIR.mkdir(exist_ok=True)
    
    # 移除舊的 API 文檔
    for file in API_DIR.glob("*.rst"):
        file.unlink()
    
    # 使用 sphinx-apidoc 生成新的 API 文檔
    cmd = [
        "sphinx-apidoc",
        "-f",                      # 強制覆蓋現有文件
        "-M",                      # 把模組放在模組目錄下
        "-o", str(API_DIR),        # 輸出目錄
        str(PROJECT_ROOT / "pretty_loguru"),  # 源碼目錄
    ]
    
    run_command(cmd)
    print("API 文檔生成完成")


def prepare_translations():
    """準備翻譯文件"""
    print("\n==== 準備翻譯文件 ====")
    
    # 檢查 locale 目錄是否存在
    if not LOCALE_DIR.exists():
        LOCALE_DIR.mkdir(exist_ok=True)
    
    # 生成 .pot 文件
    cmd = [
        "sphinx-build",
        "-b", "gettext",
        str(SOURCE_DIR),
        str(GETTEXT_DIR),
    ]
    run_command(cmd)
    
    # 準備英文翻譯
    cmd = [
        "sphinx-intl",
        "update",
        "-p", str(GETTEXT_DIR),
        "-l", "en",
    ]
    run_command(cmd)
    
    print("翻譯文件準備完成")
    print("\n提示: 你現在可以編輯 'locale/en/LC_MESSAGES/' 目錄下的 .po 文件來提供英文翻譯")

def build_documentation(language=None):
    """構建指定語言的文檔"""
    lang_str = f"({language})" if language else "(繁體中文)"
    print(f"\n==== 構建文檔 {lang_str} ====")
    
    cmd = ["sphinx-build", "-b", "html"]
    
    # 添加語言選項
    if language:
        cmd.extend(["-D", f"language={language}"])
    
    # 源目錄和目標目錄
    output_dir = BUILD_DIR / "html"
    if language:
        output_dir = output_dir / language
    else:
        # 為繁體中文版本添加特定路徑
        output_dir = output_dir / "zh_TW"
    
    cmd.extend([str(SOURCE_DIR), str(output_dir)])
    
    run_command(cmd)
    print(f"文檔構建完成: {output_dir}")


def create_index_page():
    """創建重定向頁面"""
    index_html = BUILD_DIR / "html" / "index.html"
    if not index_html.parent.exists():
        index_html.parent.mkdir(parents=True, exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Pretty Loguru 文檔</title>
    <meta http-equiv="refresh" content="0; url=./zh_TW/index.html">
</head>
<body>
    <p>重定向到 <a href="./zh_TW/index.html">繁體中文文檔</a>.</p>
</body>
</html>
"""
    
    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已創建重定向頁面: {index_html}")


def add_language_switcher():
    """添加語言切換器"""
    print("\n==== 添加語言切換器 ====")
    
    # 創建自定義 JS 文件
    static_dir = SOURCE_DIR / "_static"
    static_dir.mkdir(exist_ok=True)
    
    js_file = static_dir / "language_switcher.js"
    
    js_content = """
// 語言切換器腳本
document.addEventListener('DOMContentLoaded', function() {
    // 創建語言切換器元素
    var switcher = document.createElement('div');
    switcher.className = 'language-switcher';
    switcher.style.cssText = 'text-align: right; padding: 10px 0; margin-bottom: 20px; border-bottom: 1px solid #e1e4e5;';
    
    // 獲取當前路徑
    var path = window.location.pathname;
    var inEnglishVersion = path.includes('/en/');
    
    // 創建語言切換器內容
    if (inEnglishVersion) {
        var chinesePath = path.replace('/en/', '/');
        switcher.innerHTML = '<a href="' + chinesePath + '">繁體中文</a> | English';
    } else {
        var englishPath = path.replace('/html/', '/html/en/');
        if (path.endsWith('/html/')) {
            englishPath = path + 'en/';
        }
        switcher.innerHTML = '繁體中文 | <a href="' + englishPath + '">English</a>';
    }
    
    // 將切換器添加到頁面
    var headerElem = document.querySelector('.wy-nav-content-wrap');
    if (headerElem) {
        headerElem.insertBefore(switcher, headerElem.firstChild);
    }
});
"""
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # 確保在 conf.py 中添加 JS 文件
    conf_file = SOURCE_DIR / "conf.py"
    with open(conf_file, 'r', encoding='utf-8') as f:
        conf_content = f.read()
    
    # 檢查並添加必要的配置
    modified = False
    
    if "html_static_path = ['_static']" not in conf_content:
        conf_content = conf_content.replace(
            "# -- Options for HTML output -----------------------------------------",
            "# -- Options for HTML output -----------------------------------------\n\nhtml_static_path = ['_static']"
        )
        modified = True
    
    if "html_js_files = ['language_switcher.js']" not in conf_content:
        if "html_static_path = ['_static']" in conf_content:
            conf_content = conf_content.replace(
                "html_static_path = ['_static']",
                "html_static_path = ['_static']\nhtml_js_files = ['language_switcher.js']"
            )
        else:
            conf_content += "\n\nhtml_js_files = ['language_switcher.js']\n"
        modified = True
    
    if modified:
        with open(conf_file, 'w', encoding='utf-8') as f:
            f.write(conf_content)
        print("已更新 conf.py 添加語言切換器設置")
    else:
        print("conf.py 已包含必要設置")
    
    print("語言切換器已添加")


def create_index_page():
    """創建重定向頁面"""
    index_html = BUILD_DIR / "html" / "index.html"
    if not index_html.parent.exists():
        index_html.parent.mkdir(parents=True, exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Pretty Loguru 文檔</title>
    <meta http-equiv="refresh" content="0; url=./zh_TW/index.html">
</head>
<body>
    <p>重定向到 <a href="./zh_TW/index.html">繁體中文文檔</a>.</p>
</body>
</html>
"""
    
    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已創建重定向頁面: {index_html}")


def main():
    """主函數"""
    print("===== Pretty Loguru 文檔構建工具 =====")
    
    parser = ArgumentParser(description="構建 Pretty Loguru 文檔")
    parser.add_argument("--clean", action="store_true", help="清理構建目錄")
    parser.add_argument("--api", action="store_true", help="重新生成 API 文檔")
    parser.add_argument("--translate", action="store_true", help="準備翻譯文件")
    parser.add_argument("--build", action="store_true", help="構建文檔")
    parser.add_argument("--language-switcher", action="store_true", help="添加語言切換器")
    parser.add_argument("--all", action="store_true", help="執行所有步驟")
    
    args = parser.parse_args()
    
    # 如果沒有提供任何參數，顯示幫助
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # 執行所選操作
    if args.all or args.clean:
        clean_build_directory()
    
    if args.all or args.api:
        regenerate_api_docs()
    
    if args.all or args.translate:
        prepare_translations()
    
    if args.all or args.language_switcher:
        add_language_switcher()
    
    if args.all or args.build:
        # 構建繁體中文文檔
        build_documentation()
        
        # 構建英文文檔
        build_documentation(language="en")
        
        # 創建重定向頁面
        create_index_page()
    
    print("\n===== 文檔處理完成 =====")


if __name__ == "__main__":
    main()
    
    
# # 查看幫助
# python build_docs.py

# # 執行所有步驟
# python build_docs.py --all

# # 或者單獨執行特定步驟
# python build_docs.py --clean  # 清理構建目錄
# python build_docs.py --api    # 重新生成API文檔
# python build_docs.py --translate  # 準備翻譯文件
# python build_docs.py --build  # 構建文檔