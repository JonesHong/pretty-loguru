# 程式碼高亮

Pretty-loguru 通過與 Rich 庫的集成提供強大的語法高亮功能，讓你能在日誌中顯示美觀、彩色的程式碼片段。

## 快速開始

```python
from pretty_loguru import create_logger

# 創建啟用 Rich 組件的 logger
logger = create_logger(name="demo", use_rich_components=True)

# 顯示帶語法高亮的 Python 程式碼
code = '''
def hello_world():
    print("Hello, World!")
    return True
'''

logger.code(code, language="python", title="Hello World 範例")
```

## 核心方法

### `logger.code()` - 顯示程式碼片段

直接從字符串顯示語法高亮的程式碼。

```python
logger.code(
    code=source_code,
    language="python",        # 程式語言
    theme="monokai",         # 顏色主題
    line_numbers=True,       # 顯示行號
    title="我的函數",         # 可選標題
    word_wrap=False,         # 啟用自動換行
    indent_guides=True       # 顯示縮排引導線
)
```

**參數說明：**
- `code` (str): 要顯示的原始程式碼
- `language` (str): 程式語言 (python, javascript, sql 等)
- `theme` (str): 語法高亮主題
- `line_numbers` (bool): 是否顯示行號
- `word_wrap` (bool): 啟用自動換行
- `indent_guides` (bool): 顯示縮排引導線
- `title` (str, 可選): 程式碼區塊的顯示標題

### `logger.code_file()` - 從文件顯示程式碼

直接從文件讀取並顯示程式碼，具有自動語言檢測功能。

```python
logger.code_file(
    file_path="script.py",
    start_line=10,           # 從第 10 行開始
    end_line=25,             # 到第 25 行結束
    language=None,           # 從擴展名自動檢測
    theme="github-dark"
)
```

**參數說明：**
- `file_path` (str): 原始文件路徑
- `language` (str, 可選): 覆蓋自動語言檢測
- `start_line` (int, 可選): 顯示的起始行號 (從 1 開始)
- `end_line` (int, 可選): 顯示的結束行號 (從 1 開始)
- `theme` (str): 語法高亮主題

### `logger.diff()` - 程式碼對比

以並排方式顯示程式碼對比，具有 Git 風格的視覺區分。

```python
logger.diff(
    old_code=old_version,
    new_code=new_version,
    old_title="重構前",       # 舊版本標題 (紅色邊框)
    new_title="重構後",       # 新版本標題 (綠色邊框)
    language="python"
)
```

**參數說明：**
- `old_code` (str): 程式碼的原始版本
- `new_code` (str): 程式碼的更新版本
- `old_title` (str): 舊版本的標籤 (顯示紅色邊框)
- `new_title` (str): 新版本的標籤 (顯示綠色邊框)
- `language` (str): 語法高亮的程式語言

## 支援的程式語言

程式碼高亮功能自動檢測並支援多種程式語言：

| 語言 | 文件擴展名 | 語言代碼 |
|----------|----------------|---------------|
| Python | `.py` | `python` |
| JavaScript | `.js` | `javascript` |
| TypeScript | `.ts` | `typescript` |
| HTML | `.html` | `html` |
| CSS | `.css` | `css` |
| JSON | `.json` | `json` |
| SQL | `.sql` | `sql` |
| Markdown | `.md` | `markdown` |
| YAML | `.yaml`, `.yml` | `yaml` |
| XML | `.xml` | `xml` |
| Bash | `.sh` | `bash` |
| C/C++ | `.c`, `.cpp` | `c`, `cpp` |
| Java | `.java` | `java` |
| Go | `.go` | `go` |
| Rust | `.rs` | `rust` |
| PHP | `.php` | `php` |
| Ruby | `.rb` | `ruby` |

## 可用主題

從多種語法高亮主題中選擇：

### 深色主題
- `monokai` (預設) - 流行的深色主題，顏色鮮豔
- `github-dark` - GitHub 的深色主題
- `one-dark` - Atom 的 One Dark 主題
- `material` - Material 設計深色主題
- `dracula` - 流行的吸血鬼主題深色配色
- `nord` - 北極風格的藍色調色板
- `solarized-dark` - 低對比度深色主題

### 淺色主題
- `github-light` - GitHub 的淺色主題
- `solarized-light` - 低對比度淺色主題

## 進階範例

### 多語言程式碼顯示

```python
def showcase_languages():
    """顯示多種語言的程式碼"""
    
    # Python 範例
    python_code = '''
class UserManager:
    def __init__(self, database):
        self.db = database
        
    async def create_user(self, user_data):
        """創建新的用戶帳戶"""
        user_id = await self.db.users.insert(user_data)
        return user_id
'''
    
    logger.code(python_code, language="python", title="Python 類別")
    
    # JavaScript 範例  
    js_code = '''
const userManager = {
    async createUser(userData) {
        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });
            return await response.json();
        } catch (error) {
            console.error('創建用戶失敗:', error);
            throw error;
        }
    }
};
'''
    
    logger.code(js_code, language="javascript", title="JavaScript 物件")
    
    # SQL 範例
    sql_code = '''
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
'''
    
    logger.code(sql_code, language="sql", title="資料庫架構")
```

### 文件內容顯示與行範圍

```python
def show_specific_functions():
    """顯示原始文件中的特定函數"""
    
    # 只顯示主函數
    logger.code_file(
        file_path="main.py",
        start_line=45,
        end_line=70,
        title="主函數實現"
    )
    
    # 顯示配置部分
    logger.code_file(
        file_path="config.py",
        start_line=1,
        end_line=25,
        title="配置設定"
    )
```

### 程式碼重構對比

```python
def show_refactoring_example():
    """展示程式碼改進的前後對比"""
    
    # 原始實現
    old_code = '''
def process_user_data(users):
    results = []
    for user in users:
        if user['active']:
            user_info = {}
            user_info['id'] = user['id']
            user_info['name'] = user['first_name'] + ' ' + user['last_name']
            user_info['email'] = user['email']
            if user['premium']:
                user_info['tier'] = 'premium'
            else:
                user_info['tier'] = 'standard'
            results.append(user_info)
    return results
'''
    
    # 重構後的實現
    new_code = '''
def process_user_data(users):
    """處理活躍用戶並格式化其數據"""
    return [
        {
            'id': user['id'],
            'name': f"{user['first_name']} {user['last_name']}",
            'email': user['email'],
            'tier': 'premium' if user.get('premium', False) else 'standard'
        }
        for user in users
        if user.get('active', False)
    ]
'''
    
    logger.diff(
        old_code=old_code,
        new_code=new_code,
        old_title="原始實現",
        new_title="重構後實現",
        language="python"
    )
```

### 主題對比

```python
def compare_themes():
    """以不同主題顯示相同程式碼"""
    
    sample_code = '''
import asyncio
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False

async def start_server(config: Config) -> None:
    """啟動應用程式伺服器"""
    print(f"在 {config.host}:{config.port} 啟動伺服器")
    if config.debug:
        print("已啟用調試模式")
'''
    
    themes = [
        ("monokai", "Monokai 主題"),
        ("github-dark", "GitHub 深色主題"),
        ("one-dark", "One Dark 主題"),
        ("material", "Material 主題")
    ]
    
    for theme_name, theme_title in themes:
        logger.code(
            code=sample_code,
            language="python",
            theme=theme_name,
            title=theme_title,
            to_console_only=True  # 只在控制台顯示以便對比
        )
```

## 輸出控制

### 目標特定顯示

```python
# 只在控制台顯示 (不在日誌文件中)
logger.code(
    code=debug_code,
    title="調試信息",
    to_console_only=True
)

# 只保存到日誌文件 (不在控制台顯示)
logger.code(
    code=config_dump,
    title="配置轉儲",
    to_log_file_only=True
)
```

## 最佳實踐

### 1. 選擇合適的主題
- 在開發環境使用 **深色主題** (`monokai`, `github-dark`)
- 在文檔中使用 **淺色主題** (`github-light`, `solarized-light`)

### 2. 使用描述性標題
```python
# 好：描述性標題
logger.code(code, title="用戶認證函數")

# 更好：包含上下文
logger.code(code, title="用戶認證函數 (v2.1 - OAuth2 支援)")
```

### 3. 對大文件使用行範圍
```python
# 只顯示相關部分
logger.code_file(
    file_path="large_module.py",
    start_line=150,
    end_line=180,
    title="錯誤處理部分"
)
```

### 4. 使用 Diff 進行程式碼審查
```python
# 適合程式碼審查日誌
logger.diff(
    old_code=before_fix,
    new_code=after_fix,
    old_title="存在錯誤",
    new_title="錯誤已修復",
    language="python"
)
```

### 5. 控制輸出目標
```python
# 開發期間調試程式碼只在控制台
logger.code(debug_snippet, to_console_only=True)

# 重要的程式碼快照保存到文件
logger.code(production_config, to_log_file_only=True)
```

## 與現有功能集成

程式碼高亮與 pretty-loguru 的現有功能無縫配合：

```python
# 與不同日誌級別配合
logger.info("顯示關鍵函數：")
logger.code(critical_code, language="python")

# 與目標特定日誌配合
logger.console.code(console_code, to_console_only=True)
logger.file.code(file_code, to_log_file_only=True)

# 與 Rich 組件集成
logger.code(api_code, language="python", title="API 處理器")
logger.table("API 端點", endpoint_data)  # 顯示相關表格
```

程式碼高亮功能使 pretty-loguru 成為開發日誌記錄、程式碼文檔、調試會話和技術文檔生成的絕佳選擇。