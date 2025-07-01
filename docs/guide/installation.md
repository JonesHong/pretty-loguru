# 安裝

本頁面將指導你完成 pretty-loguru 的安裝過程。

## 🚀 快速安裝

### 使用 pip（推薦）

```bash
pip install pretty-loguru
```

### 使用 conda

```bash
conda install -c conda-forge pretty-loguru
```

## 📋 系統需求

### Python 版本
- **最低需求**: Python 3.8+
- **推薦版本**: Python 3.9+ 或更新版本

### 作業系統支援
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+, 等)

## 📦 依賴套件

pretty-loguru 會自動安裝以下依賴：

- **[loguru](https://github.com/Delgan/loguru)** - 核心日誌功能
- **[rich](https://github.com/Textualize/rich)** - 豐富的控制台輸出
- **[art](https://github.com/sepandhaghighi/art)** - ASCII 藝術生成
- **[pyfiglet](https://github.com/pwaller/pyfiglet)** - 文字藝術字體

## 🔧 安裝驗證

安裝完成後，運行以下代碼驗證：

```python
# test_installation.py
from pretty_loguru import create_logger

# 測試基本功能
logger  = create_logger(
    name="installation_demo",
    log_path="test_logs",
    level="INFO"
)
logger.info("✅ pretty-loguru 安裝成功！")
logger.success("🎉 所有功能正常運作！")

# 測試 Rich 區塊
logger.block(
    "安裝驗證",
    [
        "✅ loguru: 正常",
        "✅ rich: 正常", 
        "✅ art: 正常",
        "✅ pyfiglet: 正常"
    ],
    border_style="green"
)

# 測試 ASCII 藝術
logger.ascii_header("SUCCESS", font="slant")
```

如果看到彩色輸出且沒有錯誤，表示安裝成功！

## 🛠️ 進階安裝選項

### 開發版本安裝

如果你想使用最新的開發版本：

```bash
pip install git+https://github.com/JonesHong/pretty-loguru.git
```

### 從原始碼安裝

```bash
# 克隆倉庫
git clone https://github.com/JonesHong/pretty-loguru.git
cd pretty-loguru

# 安裝依賴
pip install -r requirements.txt

# 安裝套件
pip install -e .
```

### 虛擬環境安裝（推薦）

使用虛擬環境可以避免套件衝突：

```bash
# 建立虛擬環境
python -m venv pretty_loguru_env

# 啟動虛擬環境
# Windows:
pretty_loguru_env\Scripts\activate
# macOS/Linux:
source pretty_loguru_env/bin/activate

# 安裝 pretty-loguru
pip install pretty-loguru
```

## 🐳 Docker 環境

如果你使用 Docker，可以在 Dockerfile 中添加：

```dockerfile
FROM python:3.9-slim

# 安裝 pretty-loguru
RUN pip install pretty-loguru

# 其他設定...
```

## ⚠️ 故障排除

### 常見問題

#### 1. 安裝失敗：權限不足

```bash
# 解決方案：使用 --user 安裝
pip install --user pretty-loguru
```

#### 2. 依賴衝突

```bash
# 解決方案：使用虛擬環境
python -m venv new_env
source new_env/bin/activate  # Linux/Mac
# 或 new_env\Scripts\activate  # Windows
pip install pretty-loguru
```

#### 3. Python 版本過舊

```bash
# 檢查 Python 版本
python --version

# 如果版本 < 3.8，請升級 Python
```

#### 4. 某些功能無法使用

如果 ASCII 藝術功能有問題，可能是字體套件問題：

```bash
# 重新安裝相關套件
pip uninstall art pyfiglet
pip install art pyfiglet
```

### 詳細診斷

如果遇到問題，運行診斷腳本：

```python
# diagnose.py
import sys
import subprocess

def check_installation():
    print("🔍 pretty-loguru 安裝診斷")
    print("=" * 40)
    
    # 檢查 Python 版本
    print(f"Python 版本: {sys.version}")
    
    # 檢查主要依賴
    packages = ['loguru', 'rich', 'art', 'pyfiglet']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}: 已安裝")
        except ImportError:
            print(f"❌ {package}: 未安裝")
    
    # 檢查 pretty-loguru
    try:
        from pretty_loguru import create_logger
        print("✅ pretty-loguru: 已安裝")
        
        # 基本功能測試
        logger  = create_logger(
    name="installation_demo",
    log_path="diagnose_test",
    level="INFO"
)
        logger.info("基本功能測試通過")
        print("✅ 基本功能: 正常")
        
    except Exception as e:
        print(f"❌ pretty-loguru: 錯誤 - {e}")

if __name__ == "__main__":
    check_installation()
```

## 📱 IDE 整合

### VS Code

安裝 Python 擴展後，VS Code 會自動識別 pretty-loguru：

```json
// settings.json
{
    "python.analysis.extraPaths": ["./pretty_loguru_env/lib/python3.9/site-packages"]
}
```

### PyCharm

在 PyCharm 中設定解釋器指向你的虛擬環境。

## 🔄 升級

升級到最新版本：

```bash
pip install --upgrade pretty-loguru
```

檢查版本：

```python
import pretty_loguru
print(pretty_loguru.__version__)
```

## ✅ 驗證清單

安裝完成後，確認以下項目：

- [ ] Python 版本 >= 3.8
- [ ] pretty-loguru 安裝成功
- [ ] 基本日誌功能正常
- [ ] Rich 區塊顯示正常
- [ ] ASCII 藝術功能正常
- [ ] 檔案輸出正常

## 🚀 下一步

安裝完成後：

1. **[快速開始](./quick-start)** - 5分鐘體驗所有功能
2. **[基本用法](./basic-usage)** - 詳細了解核心概念
3. **[範例集合](../examples/)** - 實際應用場景

恭喜！你已經成功安裝 pretty-loguru，準備開始優雅的日誌之旅！ 🎉