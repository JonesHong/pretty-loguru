# 預設配置範例

pretty-loguru 提供了多種預設配置，讓你能快速在不同場景下使用最佳的日誌配置。本頁面展示各種預設配置的使用方法和自定義技巧。

## 🚀 快速開始

### 基本預設配置

```python
from pretty_loguru import create_logger

# 使用預設配置
logger = create_logger(
    name="demo",
    log_path="logs/demo.log"
)

# 使用開發環境預設配置
logger = create_logger(
    name="development_demo",
    preset="development",
    log_path="development_logs/dev.log"
)

# 使用生產環境預設配置
logger = create_logger(
    name="production_demo",
    preset="production",
    log_path="production_logs/prod.log"
)

# 使用除錯預設配置
logger = create_logger(
    name="debug_demo",
    preset="debug",
    log_path="debug_logs/debug.log"
)
```

## 🎯 預設配置類型

### 1. 開發環境配置 (development)

適合本地開發使用，包含豐富的視覺效果和詳細的日誌資訊：

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# 啟用開發環境預設配置
logger = create_logger(
    name="development_demo",
    log_path="dev_logs",
    level="INFO"
)

def development_demo():
    """開發環境配置展示"""
    
    logger.ascii_header("DEV MODE", font="slant", border_style="cyan")
    
    logger.debug("除錯資訊：變數 x = 42")
    logger.info("啟動開發伺服器...")
    logger.success("伺服器啟動成功，監聽 localhost:8000")
    
    # 詳細的除錯區塊
    logger.block(
        "開發環境狀態",
        [
            "🔧 除錯模式: 啟用",
            "🌐 環境: Development", 
            "📝 日誌級別: DEBUG",
            "🎨 視覺化: 完整啟用",
            "📊 效能監控: 啟用"
        ],
        border_style="cyan"
    )
    
    logger.warning("這是開發環境的警告訊息")
    logger.error("這是開發環境的錯誤訊息")

development_demo()
```

**開發環境配置特點：**
- 完整的視覺化效果 (ASCII 藝術、Rich 區塊)
- 詳細的除錯資訊
- 彩色輸出
- 檔案和控制台雙重輸出
- 較低的效能考量

### 2. 生產環境配置 (production)

適合生產環境使用，強調效能和簡潔性：

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# 啟用生產環境預設配置
logger = create_logger(
    name="production_demo",
    log_path="prod_logs",
    level="INFO"
)

def production_demo():
    """生產環境配置展示"""
    
    logger.info("應用程式啟動")
    logger.info("載入配置檔...")
    logger.success("服務啟動完成")
    
    # 簡潔的狀態報告
    logger.block(
        "服務狀態",
        [
            "狀態: 正常運行",
            "版本: v2.1.0",
            "實例: prod-server-01",
            "啟動時間: 2.3 秒"
        ],
        border_style="green"
    )
    
    logger.warning("記憶體使用率達到 75%")
    logger.error("資料庫連接逾時")

production_demo()
```

**生產環境配置特點：**
- 簡化的視覺效果
- 重要資訊的結構化輸出
- 最佳化的效能
- 重點關注錯誤和警告
- 支援日誌輪換

### 3. 除錯配置 (debug)

適合問題排查和深度除錯：

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# 啟用除錯預設配置
logger = create_logger(
    name="debug_demo",
    log_path="debug_logs",
    level="INFO"
)

def debug_demo():
    """除錯配置展示"""
    
    logger.ascii_header("DEBUG", font="doom", border_style="yellow")
    
    # 詳細的函數追蹤
    logger.debug("進入函數: debug_demo()")
    logger.debug("初始化變數...")
    
    data = {"user_id": 123, "action": "login", "timestamp": "2024-06-30"}
    logger.debug(f"處理資料: {data}")
    
    # 詳細的除錯區塊
    logger.block(
        "除錯資訊",
        [
            f"🔍 函數: {debug_demo.__name__}",
            f"📂 模組: {__name__}",
            f"💾 記憶體使用: 45MB",
            f"⏱️  執行時間: 0.002s",
            f"🔢 處理記錄數: {len(data)}"
        ],
        border_style="yellow"
    )
    
    logger.debug("函數執行完成")

debug_demo()
```

**除錯配置特點：**
- 最詳細的日誌輸出
- 函數追蹤和效能監控
- 變數狀態記錄
- 執行路徑追蹤
- 完整的錯誤堆疊

### 4. 測試配置 (testing)

適合單元測試和整合測試：

```python
from pretty_loguru import create_logger

# Create logger instance
logger = create_logger(
    name="demo",
    log_path="logs",
    level="INFO"
)

# 啟用測試預設配置
logger = create_logger(
    name="testing_demo",
    log_path="test_logs",
    level="INFO"
)

def testing_demo():
    """測試配置展示"""
    
    logger.ascii_header("TESTING", font="standard", border_style="magenta")
    
    # 測試開始
    logger.info("開始執行測試套件...")
    
    test_results = {
        "test_login": "PASS",
        "test_logout": "PASS", 
        "test_register": "FAIL",
        "test_password_reset": "PASS"
    }
    
    # 測試結果報告
    passed_tests = []
    failed_tests = []
    
    for test_name, result in test_results.items():
        if result == "PASS":
            passed_tests.append(f"✅ {test_name}")
        else:
            failed_tests.append(f"❌ {test_name}")
    
    if passed_tests:
        logger.block(
            "通過的測試",
            passed_tests,
            border_style="green"
        )
    
    if failed_tests:
        logger.block(
            "失敗的測試", 
            failed_tests,
            border_style="red",
            log_level="ERROR"
        )
    
    # 測試摘要
    total_tests = len(test_results)
    passed_count = len(passed_tests)
    
    logger.block(
        "測試摘要",
        [
            f"📊 總測試數: {total_tests}",
            f"✅ 通過: {passed_count}",
            f"❌ 失敗: {total_tests - passed_count}",
            f"📈 成功率: {(passed_count/total_tests)*100:.1f}%"
        ],
        border_style="blue"
    )

testing_demo()
```

## 🔧 自定義預設配置

### 創建自己的預設配置

```python
from pretty_loguru import create_logger

def create_custom_preset():
    """創建自定義預設配置"""
    
    # 自定義 API 服務配置
    api_preset = {
        "folder": "api_logs",
        "file_name": "api_{time}.log",
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        "rotation": "500 MB",
        "retention": "30 days",
        "compression": "zip",
        "visual_mode": "minimal"  # 簡化視覺效果
    }
    
    # 使用自定義配置
    logger = create_logger(**api_preset)
    
    logger.ascii_header("API SERVICE", font="small", border_style="blue")
    logger.info("API 服務已啟動")
    
    # API 狀態區塊
    logger.block(
        "API 服務狀態",
        [
            "🌐 端點: https://api.example.com",
            "🔐 認證: JWT",
            "📊 限流: 1000 req/min",
            "⚡ 響應時間: < 100ms"
        ],
        border_style="blue"
    )

create_custom_preset()
```

### 環境特定配置

```python
import os
from pretty_loguru import create_logger

def environment_specific_config():
    """根據環境變數選擇配置"""
    
    env = os.getenv("ENVIRONMENT", "development")
    
    config_map = {
        "development": {
            "preset": "development",
            "folder": "dev_logs",
            "level": "DEBUG"
        },
        "staging": {
            "preset": "production", 
            "folder": "staging_logs",
            "level": "INFO"
        },
        "production": {
            "preset": "production",
            "folder": "prod_logs", 
            "level": "WARNING"
        }
    }
    
    config = config_map.get(env, config_map["development"])
    create_logger(**config)
    
    logger.ascii_block(
        f"環境配置已載入",
        [
            f"🌍 環境: {env.upper()}",
            f"📁 日誌目錄: {config['folder']}", 
            f"📊 日誌級別: {config['level']}",
            f"⚙️  預設: {config['preset']}"
        ],
        ascii_header="CONFIG",
        ascii_font="standard",
        border_style="cyan"
    )

environment_specific_config()
```

## 📊 配置比較

### 各預設配置特性對比

```python
def compare_presets():
    """比較不同預設配置的特性"""
    
    from rich.table import Table
    from rich.console import Console
    
    console = Console()
    
    table = Table(title="預設配置特性比較", show_header=True, header_style="bold magenta")
    table.add_column("特性", style="cyan", width=15)
    table.add_column("Development", style="green", width=12)
    table.add_column("Production", style="yellow", width=12) 
    table.add_column("Debug", style="red", width=12)
    table.add_column("Testing", style="blue", width=12)
    
    features = [
        ("ASCII 藝術", "✅ 完整", "⚠️ 簡化", "✅ 完整", "✅ 完整"),
        ("Rich 區塊", "✅ 完整", "⚠️ 簡化", "✅ 完整", "✅ 完整"),
        ("日誌級別", "DEBUG", "INFO", "DEBUG", "INFO"),
        ("效能優化", "❌ 否", "✅ 是", "❌ 否", "⚠️ 部分"),
        ("檔案輪換", "⚠️ 基本", "✅ 完整", "❌ 否", "⚠️ 基本"),
        ("視覺效果", "✅ 豐富", "⚠️ 簡潔", "✅ 詳細", "✅ 清晰"),
        ("錯誤追蹤", "⚠️ 標準", "✅ 重點", "✅ 詳細", "✅ 完整")
    ]
    
    for feature in features:
        table.add_row(*feature)
    
    console.print(table)

compare_presets()
```

## 💡 最佳實踐

### 1. 根據環境選擇配置

```python
# 推薦 - 環境感知配置
def smart_logger_init():
    import os
    
    if os.getenv("DEBUG"):
        logger = create_logger(
    name="debug_demo",
    log_path="debug_logs",
    level="INFO"
)
    elif os.getenv("TESTING"):
        logger = create_logger(
    name="testing_demo",
    log_path="testing_logs",
    level="INFO"
)
    elif os.getenv("PROD"):
        logger = create_logger(
    name="production_demo",
    log_path="production_logs",
    level="INFO"
)
    else:
        logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)

smart_logger_init()
```

### 2. 配置檔案管理

```python
# 使用設定檔
import json

def load_config_from_file(config_path="logger_config.json"):
    """從檔案載入日誌配置"""
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        create_logger(**config)
        
        logger.success(f"已載入配置檔: {config_path}")
        logger.block(
            "載入的配置",
            [f"{key}: {value}" for key, value in config.items()],
            border_style="green"
        )
        
    except FileNotFoundError:
        logger.warning(f"配置檔 {config_path} 不存在，使用預設配置")
        logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)
    except json.JSONDecodeError:
        logger.error(f"配置檔 {config_path} 格式錯誤")
        logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)

load_config_from_file()
```

### 3. 動態配置切換

```python
def dynamic_config_switching():
    """動態切換配置"""
    
    # 初始配置
    logger = create_logger(
    name="development_demo",
    log_path="development_logs",
    level="INFO"
)
    logger.info("使用開發配置啟動")
    
    # 模擬切換到生產模式
    def switch_to_production():
        logger.ascii_header("SWITCHING", font="small", border_style="yellow")
        logger.warning("切換到生產環境配置...")
        
        # 重新初始化為生產配置
        logger = create_logger(
    name="production_demo",
    log_path="prod_logs",
    level="INFO"
)
        
        logger.ascii_block(
            "配置切換完成",
            [
                "🔄 模式: 生產環境",
                "📁 日誌: prod_logs/",
                "🎯 級別: INFO",
                "⚡ 效能: 最佳化"
            ],
            ascii_header="SWITCHED",
            ascii_font="standard",
            border_style="green"
        )
    
    # 執行切換
    switch_to_production()

dynamic_config_switching()
```

## 🚀 完整範例

結合所有預設配置的綜合範例：

```python
def comprehensive_preset_demo():
    """預設配置綜合展示"""
    
    import time
    
    presets = ["development", "production", "debug", "testing"]
    
    for preset in presets:
        print(f"\n{'='*50}")
        print(f"展示 {preset.upper()} 預設配置")
        print(f"{'='*50}")
        
        # 初始化配置
        create_logger(preset=preset, folder=f"{preset}_demo_logs")
        
        # 配置標題
        logger.ascii_header(preset.upper(), font="slant", border_style="blue")
        
        # 基本日誌展示
        logger.info(f"正在展示 {preset} 配置")
        logger.success("配置載入成功")
        logger.warning("這是警告訊息")
        logger.error("這是錯誤訊息")
        
        # 配置特性區塊
        logger.block(
            f"{preset.title()} 配置特性",
            [
                f"🎯 適用場景: {get_preset_scenario(preset)}",
                f"📊 日誌級別: {get_preset_level(preset)}",
                f"🎨 視覺效果: {get_preset_visual(preset)}",
                f"⚡ 效能優化: {get_preset_performance(preset)}"
            ],
            border_style="cyan"
        )
        
        time.sleep(2)  # 暫停以便觀察
    
    logger.ascii_header("COMPLETE", font="block", border_style="green")
    logger.success("所有預設配置展示完成！")

def get_preset_scenario(preset):
    scenarios = {
        "development": "本地開發、功能測試",
        "production": "線上服務、正式環境", 
        "debug": "問題排查、效能分析",
        "testing": "自動測試、CI/CD"
    }
    return scenarios.get(preset, "通用")

def get_preset_level(preset):
    levels = {
        "development": "DEBUG",
        "production": "INFO",
        "debug": "DEBUG", 
        "testing": "INFO"
    }
    return levels.get(preset, "INFO")

def get_preset_visual(preset):
    visuals = {
        "development": "完整豐富",
        "production": "簡潔高效",
        "debug": "詳細完整",
        "testing": "清晰明確"
    }
    return visuals.get(preset, "標準")

def get_preset_performance(preset):
    performance = {
        "development": "功能優先",
        "production": "效能最佳化",
        "debug": "詳細優先", 
        "testing": "平衡模式"
    }
    return performance.get(preset, "平衡")

if __name__ == "__main__":
    comprehensive_preset_demo()
```

預設配置讓 pretty-loguru 能快速適應不同的使用場景，選擇合適的預設配置是成功使用日誌系統的關鍵！