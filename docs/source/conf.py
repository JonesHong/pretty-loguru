# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))  # 將專案根目錄添加到路徑中

# 專案信息
project = "Pretty Loguru"
copyright = "2025, JonesHong"
author = "JonesHong"
version = "0.2.11"
release = "0.2.11"

# 常規設置
extensions = [
    "sphinx.ext.autodoc",  # 自動生成API文檔
    "sphinx.ext.napoleon",  # 支援Google風格的docstrings
    "sphinx.ext.viewcode",  # 添加查看源碼的連結
    "sphinx.ext.todo",  # 支援TODO標記
    "sphinx.ext.autosummary",  # 自動生成摘要
    "sphinx_autodoc_typehints",  # 從類型註解生成文檔
    "myst_parser",  # 支援Markdown
    "sphinx_copybutton",  # 支援複製按鈕
    "sphinx_rtd_dark_mode",  # 支援深色模式
]

# 主題設置
html_theme = "furo"
html_static_path = ["_static"]
html_js_files = ["js/language_switcher.js", "js/code_buttons.js"]
html_css_files = ["css/custom.css","css/code_buttons.css"]


# 多語言支援設置
language = "zh_TW"  # 默認為繁體中文
locale_dirs = ["locale/"]  # 翻譯文件存放目錄
gettext_compact = False  # 每個.rst文件生成一個.pot文件
gettext_uuid = True  # 為每個段落添加唯一ID，便於翻譯維護

# 語言切換器相關設置
html_context = {
    "languages": [
        ("zh_TW", "繁體中文"),
        ("en", "English"),
    ],
    "language": language,
    "root_url": "",          # 根目錄下就是 zh_TW/、en/ 這兩個子資料夾
}

# API 文檔設置
autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}


# 自動在所有 RST 檔案底部插入這段
# Epilog：定義 |locale| 取代字串
rst_epilog = f"""
.. |locale| replace:: {language}
"""


# 添加自定義跳過函數，避免記錄內部API
def skip_internal(app, what, name, obj, skip, options):
    # 跳過以下模式的項目:
    # 1. 以單下劃線開頭的內部方法和函數（但不包括__init__等特殊方法）
    # 2. 明確標記為內部使用的方法和函數
    internal_markers = ["_internal", "_helper", "_factory", "_core"]

    if name.startswith("_") and not name.startswith("__"):
        return True

    if any(marker in name for marker in internal_markers):
        return True

    # 檢查是否是明確標記為私有的方法(docstring中含有:private:標記)
    if hasattr(obj, "__doc__") and obj.__doc__ and ":private:" in obj.__doc__:
        return True

    return skip

# conf.py 裡面，放在最下方的 setup() 裡或跟 skip_internal 同一個 setup()
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective

class LocaleImage(SphinxDirective):
    required_arguments = 1  # 檔名，比如 fastAPI_example.png
    option_spec = {
        'alt': lambda x: x,
        'width': lambda x: x,
    }

    def run(self):
        # 取得目前語系
        lang = self.config.language or ''
        # 組出對應路徑
        img_rel = f"_static/{lang}/{self.arguments[0]}"
        # 建立 image node
        node = nodes.image(uri=img_rel, **self.options)
        return [node]

def setup(app):
    app.connect("autodoc-skip-member", skip_internal)
    app.add_directive("locale-image", LocaleImage)
