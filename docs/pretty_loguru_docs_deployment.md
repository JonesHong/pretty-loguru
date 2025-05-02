# Pretty Loguru 文檔製作與 GitHub Pages 部署指南

本文檔提供了製作 Pretty Loguru 文檔以及將其部署至 GitHub Pages 的完整步驟指南，重點是以繁體中文為主，並提供英文版本。

## 1. 文檔結構概述

文檔系統基於 Sphinx，主要組件包括：

- 繁體中文版本的文檔 (預設)
- 英文版本的文檔 (需要翻譯)
- 版面和樣式設定
- API 自動文檔生成
- 語言切換功能

## 2. 環境設置與依賴安裝

確保安裝了所有必要的依賴：

```bash
# 安裝 Sphinx 和必要的擴展
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser

# 多語言支援
pip install sphinx-intl

# 若您需要 API 文檔生成
pip install sphinx-apidoc
```
## 3. 檢查與完善文檔內容

確保文檔內容完整：

- 檢查所有繁體中文 `.rst` 文件的內容是否完整
- 為 API 文檔更新內容
- 確保所有圖片和靜態檔案都在 `_static` 目錄中

使用以下命令生成 API 文檔：

```bash
# 基本 API 文檔生成
sphinx-apidoc -f -M -o "source/api" ../pretty_loguru

# 包括私有成員
sphinx-apidoc -f -M --private -o "source/api" ../pretty_loguru

# 排除指定模組
sphinx-apidoc -f -M -o "source/api" ../pretty_loguru --exclude=pretty_loguru.test

# 只包含指定模組
sphinx-apidoc -f -M -o "source/api" ../pretty_loguru pretty_loguru.core pretty_loguru.factory
```
## 4. 翻譯流程

將繁體中文文檔翻譯成英文的步驟：

```bash
# 1. 提取需要翻譯的字符串
cd docs
sphinx-build -b gettext source build/gettext

# 2. 為英文版本創建 .po 檔案
sphinx-intl update -p build/gettext -l en

# 3. 翻譯 locale/en/LC_MESSAGES/ 目錄下的 .po 檔案
# 這一步需要手動翻譯或使用翻譯工具

# 4. 編譯翻譯後的 .po 檔案
sphinx-intl build
```

## 5. 構建文檔

構建中文和英文版本的文檔：

```bash
# 構建中文文檔 (預設)
cd docs

# 構建默認版本到根目錄
sphinx-build -b html source build/html

# 構建繁體中文版本
sphinx-build -b html -D language=zh_TW source build/html/zh_TW

# 構建英文版本
sphinx-build -b html -D language=en source build/html/en

# 創建 .nojekyll 文件 powershell
echo $null > build/html/.nojekyll
```

## 6. 設置 GitHub Pages

### 6.1 創建一個 GitHub 儲存庫 (如果尚未創建)

```bash
# 初始化 git 儲存庫 (如果尚未初始化)
git init
git add .
git commit -m "Initial commit with documentation"

# 添加遠端儲存庫
git remote add origin https://github.com/your-username/pretty-loguru.git
git push -u origin main
```

### 6.2 使用 GitHub Actions 自動部署

創建 `.github/workflows/docs.yml` 文件，內容如下：

```yaml
name: Build and Deploy Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser sphinx-intl
        pip install -e .
    
    - name: Build Chinese docs
      run: |
        cd docs
        make html
    
    - name: Build English docs
      run: |
        cd docs
        sphinx-build -b gettext source build/gettext
        sphinx-intl update -p build/gettext -l en
        sphinx-intl build
        sphinx-build -b html -D language=en source build/html/en
    
    - name: Create .nojekyll file
      run: |
        cd docs/build/html
        touch .nojekyll
    
    - name: Deploy to GitHub Pages
      uses: JamesIves/github-pages-deploy-action@4.1.5
      with:
        branch: gh-pages
        folder: docs/build/html
```

### 6.3 設置儲存庫以使用 GitHub Pages

1. 前往您的 GitHub 儲存庫
2. 點擊 "Settings" 標籤
3. 點擊左側導航欄中的 "Pages"
4. 在 "Source" 下，選擇 "gh-pages" 分支
5. 點擊 "Save"

## 7. 使用 Makefile 的自定義目標

您的 Makefile 已經包含了用於自動生成 API 文檔和部署到 GitHub Pages 的自定義目標：

```makefile
# 添加 apidoc 目標
apidoc:
	sphinx-apidoc -f -M -o "$(SOURCEDIR)/api" ../pretty_loguru

# 添加 github 目標 (用於 GitHub Pages)
github: clean html
	touch "$(BUILDDIR)/html/.nojekyll"
```

使用這些目標：

```bash
# 生成 API 文檔
cd docs
make apidoc

# 準備 GitHub Pages 部署
make github
```

## 8. 手動部署到 GitHub Pages (如果不使用 GitHub Actions)

如果不使用 GitHub Actions，可以手動部署：

```bash
# 構建文檔
cd docs
make clean
make apidoc
make github

# 構建英文文檔
sphinx-build -b html -D language=en source build/html/en

# 部署到 gh-pages 分支
git add -f build/html
git commit -m "Deploy documentation to GitHub Pages"
git subtree push --prefix docs/build/html origin gh-pages
```

## 9. 語言切換器確認

確保語言切換功能正常運作：

- 在 `conf.py` 中已正確設定 `language` 為 `zh_TW` 和 `locale_dirs`
- JavaScript 代碼能夠正確切換語言路徑
- CSS 樣式正確顯示切換器

修改 `_templates/layout.html` 中的語言切換代碼，確保使用 `zh_TW` 而非 `zh-TW`：

```html
{% raw %}
{% block sidebar1 %}
{{ super() }}
<div class="sidebar-block">
    <div class="sidebar-wrapper">
        <h2>{{ _('Languages') }}</h2>
        <div class="language-switcher">
            <ul>
                {% if language == 'en' %}
                    <li><a href="#">繁體中文</a></li>
                    <li class="active">English</li>
                {% else %}
                    <li class="active">繁體中文</li>
                    <li><a href="#">English</a></li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}
{% endraw %}
```

同時確保 JavaScript 部分也使用 `zh_TW`：

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // 語言切換器 JavaScript
    function setupLanguageSwitcher() {
        // 獲取當前URL路徑
        const path = window.location.pathname;
        
        // 檢查當前是哪種語言
        const isEnglish = path.includes('/en/');
        
        // 獲取語言切換器中的連結
        const links = document.querySelectorAll('.language-switcher a');
        
        if (links.length > 0) {
            links.forEach(function(link) {
                if (link.textContent.trim() === 'English' && !isEnglish) {
                    // 修改英文連結
                    const basePath = path.replace('/zh_TW/', '/');
                    link.href = basePath.replace('/html/', '/html/en/');
                } else if (link.textContent.trim() === '繁體中文' && isEnglish) {
                    // 修改中文連結
                    const basePath = path.replace('/en/', '/');
                    link.href = basePath.replace('/html/', '/html/zh_TW/');
                }
            });
        }
    }
    
    // 執行語言切換器設置
    setupLanguageSwitcher();
});
```

## 10. 修改 conf.py 中的語言設定

確保 `conf.py` 中的語言設定使用 `zh_TW`：

```python
# 多語言支援設置
language = 'zh_TW'  # 默認為繁體中文
locale_dirs = ['locale/']  # 翻譯文件存放目錄
gettext_compact = False    # 每個.rst文件生成一個.pot文件
gettext_uuid = True        # 為每個段落添加唯一ID，便於翻譯維護

# 語言切換器相關設置
html_context = {
    'languages': [
        ('zh_TW', '繁體中文'),
        ('en', 'English'),
    ],
    'language': language,
    'root_url': '../../'
}
```

## 11. GitHub Pages 生效後的查看方式

部署完成後，您可以通過以下 URL 查看您的文檔：

```
https://your-username.github.io/pretty-loguru/
```

英文版本將位於：

```
https://your-username.github.io/pretty-loguru/en/
```

繁體中文版本將位於：

```
https://your-username.github.io/pretty-loguru/zh_TW/
```

## 12. 疑難排解

如果遇到問題，以下是一些常見問題的解決方法：

### 文檔無法正確顯示

- 確保 `.nojekyll` 文件已經添加到 `build/html` 目錄
- 檢查 GitHub Pages 設置是否正確指向 `gh-pages` 分支

### 語言切換不正常

- 檢查 URL 路徑是否正確 (應該使用 `/zh_TW/` 而非 `/zh-TW/`)
- 確保 JavaScript 代碼能夠正確解析當前路徑

### 樣式或圖片無法顯示

- 確保所有靜態文件都在 `_static` 目錄中
- 檢查 HTML 中的路徑是否正確指向這些文件

## 13. 維護與更新

當需要更新文檔時，請遵循以下步驟：

1. 更新源文件 (`.rst` 或 `.md` 文件)
2. 重新生成翻譯檔案
3. 更新翻譯
4. 重新構建文檔
5. 部署到 GitHub Pages

```bash
# 更新翻譯檔案
cd docs
sphinx-build -b gettext source build/gettext
sphinx-intl update -p build/gettext -l en

# 翻譯更新的字符串

# 重新構建文檔
make clean
make apidoc
make github
sphinx-build -b html -D language=en source build/html/en

# 部署
git add -f build/html
git commit -m "Update documentation"
git subtree push --prefix docs/build/html origin gh-pages
```

或者，如果使用 GitHub Actions，只需推送更改到主分支，自動部署將會處理剩下的工作。
