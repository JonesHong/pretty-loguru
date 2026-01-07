# ASCII 藝術範例

ASCII 藝術是 pretty-loguru 的招牌功能，能夠建立令人印象深刻的文字藝術標題。本頁面展示各種 ASCII 藝術的實際應用。

## 🎯 基本 ASCII 標題

### 應用程式啟動標題

```python
from pretty_loguru import create_logger

# 初始化日誌系統
logger = create_logger(
    name="ascii-art_demo",
    log_dir="ascii_demo",
    level="INFO"
)

# 應用程式啟動
logger.ascii_header("APP START", font="slant", border_style="blue")
logger.info("正在載入配置...")
logger.success("應用程式啟動完成")
```

### 不同字體展示

```python
def font_showcase():
    """展示所有可用的字體"""
    
    # Standard 字體 - 經典樣式
    logger.ascii_header("STANDARD", font="standard", border_style="blue")
    
    # Slant 字體 - 斜體效果
    logger.ascii_header("SLANT", font="slant", border_style="green")
    
    # Doom 字體 - 粗體效果
    logger.ascii_header("DOOM", font="doom", border_style="red")
    
    # Small 字體 - 緊湊樣式
    logger.ascii_header("SMALL", font="small", border_style="yellow")
    
    # Block 字體 - 方塊樣式
    logger.ascii_header("BLOCK", font="block", border_style="magenta")
    
    # Digital 字體 - 數位樣式
    logger.ascii_header("DIGITAL", font="digital", border_style="cyan")

font_showcase()
```

## 🌈 顏色主題展示

### 狀態指示顏色

```python
def status_colors_demo():
    """使用不同顏色表示不同狀態"""
    
    # 成功狀態 - 綠色
    logger.ascii_header("SUCCESS", font="block", border_style="green")
    logger.success("操作成功完成")
    
    # 警告狀態 - 黃色
    logger.ascii_header("WARNING", font="doom", border_style="yellow")
    logger.warning("發現潛在問題")
    
    # 錯誤狀態 - 紅色
    logger.ascii_header("ERROR", font="doom", border_style="red")
    logger.error("發生嚴重錯誤")
    
    # 資訊狀態 - 藍色
    logger.ascii_header("INFO", font="slant", border_style="blue")
    logger.info("提供重要資訊")
    
    # 特殊狀態 - 紫色
    logger.ascii_header("SPECIAL", font="standard", border_style="magenta")
    logger.info("特殊事件發生")
    
    # 開發狀態 - 青色
    logger.ascii_header("DEBUG", font="small", border_style="cyan")
    logger.debug("除錯資訊")

status_colors_demo()
```

## 🚀 實際應用場景

### 系統啟動序列

```python
def system_startup_sequence():
    """模擬系統啟動過程"""
    import time
    
    # 啟動標題
    logger.ascii_header("SYSTEM BOOT", font="slant", border_style="blue")
    
    logger.info("正在初始化系統...")
    time.sleep(1)
    
    # 載入階段
    logger.ascii_header("LOADING", font="small", border_style="cyan")
    logger.info("載入核心模組...")
    logger.info("載入設備驅動...")
    logger.info("載入網路堆疊...")
    time.sleep(2)
    
    # 檢查階段
    logger.ascii_header("CHECKING", font="small", border_style="yellow")
    logger.info("檢查硬體狀態...")
    logger.success("CPU: 正常")
    logger.success("記憶體: 正常")
    logger.success("磁碟: 正常")
    time.sleep(1)
    
    # 完成標題
    logger.ascii_header("READY", font="block", border_style="green")
    logger.success("系統啟動完成")
    logger.info("準備接受用戶請求")

system_startup_sequence()
```

### 部署流程標示

```python
def deployment_workflow():
    """部署流程的各個階段標示"""
    import time
    
    # 開始部署
    logger.ascii_header("DEPLOY", font="slant", border_style="blue")
    logger.info("開始部署流程...")
    
    # 構建階段
    logger.ascii_header("BUILD", font="small", border_style="cyan")
    logger.info("正在編譯程式碼...")
    logger.info("正在打包應用...")
    logger.success("構建完成")
    time.sleep(1)
    
    # 測試階段
    logger.ascii_header("TEST", font="small", border_style="yellow")
    logger.info("執行單元測試...")
    logger.info("執行整合測試...")
    logger.success("所有測試通過")
    time.sleep(1)
    
    # 部署階段
    logger.ascii_header("DEPLOY", font="small", border_style="magenta")
    logger.info("上傳到伺服器...")
    logger.info("更新服務...")
    logger.info("重啟應用...")
    time.sleep(1)
    
    # 驗證階段
    logger.ascii_header("VERIFY", font="small", border_style="green")
    logger.info("健康檢查...")
    logger.success("服務運行正常")
    
    # 完成
    logger.ascii_header("COMPLETE", font="block", border_style="green")
    logger.success("部署成功完成")

deployment_workflow()
```

### 錯誤處理流程

```python
def error_handling_demo():
    """錯誤處理的視覺化展示"""
    
    try:
        # 模擬一些操作
        logger.ascii_header("PROCESS", font="slant", border_style="blue")
        logger.info("開始處理重要任務...")
        
        # 模擬錯誤
        raise Exception("模擬的系統錯誤")
        
    except Exception as e:
        # 錯誤標題
        logger.ascii_header("ERROR", font="doom", border_style="red")
        logger.error(f"發生錯誤: {e}")
        
        # 錯誤分析
        logger.ascii_header("ANALYZE", font="small", border_style="yellow")
        logger.warning("正在分析錯誤原因...")
        logger.info("檢查系統狀態...")
        logger.info("檢查網路連接...")
        
        # 恢復嘗試
        logger.ascii_header("RECOVER", font="small", border_style="cyan")
        logger.info("嘗試自動恢復...")
        logger.info("重新初始化連接...")
        
        # 恢復成功
        logger.ascii_header("RECOVERED", font="slant", border_style="green")
        logger.success("系統已恢復正常")

error_handling_demo()
```

### 數據處理管道

```python
def data_pipeline_demo():
    """數據處理管道的階段標示"""
    import time
    
    # 開始處理
    logger.ascii_header("PIPELINE", font="slant", border_style="blue")
    logger.info("啟動數據處理管道...")
    
    # 第一階段：提取
    logger.ascii_header("EXTRACT", font="small", border_style="cyan")
    logger.info("從數據源提取數據...")
    logger.info("讀取 CSV 檔案...")
    logger.info("連接 API 端點...")
    logger.success("數據提取完成: 10,000 筆記錄")
    time.sleep(1)
    
    # 第二階段：轉換
    logger.ascii_header("TRANSFORM", font="small", border_style="yellow")
    logger.info("清理數據...")
    logger.info("標準化格式...")
    logger.info("驗證數據質量...")
    logger.success("數據轉換完成: 9,856 筆有效記錄")
    time.sleep(1)
    
    # 第三階段：載入
    logger.ascii_header("LOAD", font="small", border_style="magenta")
    logger.info("寫入目標資料庫...")
    logger.info("更新索引...")
    logger.info("更新統計資訊...")
    logger.success("數據載入完成")
    time.sleep(1)
    
    # 完成
    logger.ascii_header("COMPLETE", font="block", border_style="green")
    logger.success("數據管道執行成功")
    logger.info("處理了 10,000 筆記錄")
    logger.info("成功載入 9,856 筆記錄")

data_pipeline_demo()
```

### 監控和警報

```python
def monitoring_alerts_demo():
    """監控系統的警報展示"""
    
    # 正常監控
    logger.ascii_header("MONITOR", font="digital", border_style="green")
    logger.info("系統監控正常運行...")
    
    # 檢測到異常
    logger.ascii_header("ALERT", font="doom", border_style="red")
    logger.warning("檢測到異常活動")
    logger.error("CPU 使用率超過 90%")
    logger.error("記憶體使用率超過 95%")
    
    # 緊急響應
    logger.ascii_header("EMERGENCY", font="doom", border_style="red")
    logger.critical("啟動緊急響應程序")
    logger.info("通知系統管理員...")
    logger.info("啟動自動擴展...")
    
    # 問題解決
    logger.ascii_header("RESOLVED", font="slant", border_style="green")
    logger.success("問題已解決")
    logger.info("系統恢復正常運行")

monitoring_alerts_demo()
```

## 🔧 進階技巧

### 動態字體選擇

```python
import random

def random_header_demo():
    """隨機選擇字體和顏色"""
    
    fonts = ["standard", "slant", "doom", "small", "block", "digital"]
    colors = ["blue", "green", "red", "yellow", "magenta", "cyan"]
    
    for i in range(5):
        font = random.choice(fonts)
        color = random.choice(colors)
        
        logger.ascii_header(
            f"RANDOM {i+1}",
            font=font,
            border_style=color
        )
        logger.info(f"使用字體: {font}, 顏色: {color}")

random_header_demo()
```

### 條件式標題

```python
def conditional_headers_demo(status, operation):
    """根據條件顯示不同的標題"""
    
    if status == "success":
        logger.ascii_header(
            f"{operation} OK",
            font="block",
            border_style="green"
        )
    elif status == "warning":
        logger.ascii_header(
            f"{operation} WARN",
            font="standard",
            border_style="yellow"
        )
    elif status == "error":
        logger.ascii_header(
            f"{operation} FAIL",
            font="doom",
            border_style="red"
        )
    else:
        logger.ascii_header(
            f"{operation} INFO",
            font="slant",
            border_style="blue"
        )

# 使用範例
conditional_headers_demo("success", "BACKUP")
conditional_headers_demo("error", "RESTORE")
conditional_headers_demo("warning", "UPDATE")
```

### 階段進度指示

```python
def progress_stages_demo():
    """使用 ASCII 標題顯示進度階段"""
    
    stages = [
        ("STAGE 1", "small", "cyan"),
        ("STAGE 2", "small", "cyan"), 
        ("STAGE 3", "small", "cyan"),
        ("COMPLETE", "block", "green")
    ]
    
    for i, (stage, font, color) in enumerate(stages):
        logger.ascii_header(stage, font=font, border_style=color)
        
        if i < len(stages) - 1:
            logger.info(f"執行階段 {i+1} 的任務...")
            logger.success(f"階段 {i+1} 完成")
        else:
            logger.success("所有階段完成!")

progress_stages_demo()
```

### 字體組合效果

```python
def font_combination_demo():
    """展示不同場景下的字體選擇"""
    
    # 系統相關 - 使用 standard 字體
    logger.ascii_header("SYSTEM", font="standard", border_style="blue")
    logger.info("系統級操作使用標準字體")
    
    # 成功消息 - 使用 slant 字體
    logger.ascii_header("SUCCESS", font="slant", border_style="green")
    logger.success("成功消息使用斜體字體")
    
    # 錯誤警告 - 使用 doom 字體
    logger.ascii_header("ERROR", font="doom", border_style="red")
    logger.error("錯誤警告使用粗體字體")
    
    # 快速狀態 - 使用 small 字體
    logger.ascii_header("STATUS", font="small", border_style="cyan")
    logger.info("狀態更新使用小型字體")
    
    # 重要里程碑 - 使用 block 字體
    logger.ascii_header("MILESTONE", font="block", border_style="magenta")
    logger.success("重要里程碑使用方塊字體")

font_combination_demo()
```

## ⚠️ 使用注意事項

### ASCII 字符限制

```python
from pretty_loguru import is_ascii_only

def ascii_validation_demo():
    """展示 ASCII 字符驗證"""
    
    test_strings = [
        "HELLO WORLD",    # 正確
        "TEST 123",       # 正確  
        "HELLO 世界",      # 錯誤 - 包含中文
        "CAFÉ",           # 錯誤 - 包含重音符號
        "ASCII ONLY"      # 正確
    ]
    
    for text in test_strings:
        if is_ascii_only(text):
            logger.ascii_header(text, font="standard", border_style="green")
            logger.success(f"'{text}' 可以使用 ASCII 藝術")
        else:
            logger.warning(f"'{text}' 包含非 ASCII 字符，無法使用 ASCII 藝術")
            logger.info(f"=== {text} ===")  # 使用普通標題

ascii_validation_demo()
```

### 長度建議

```python
def length_guidelines_demo():
    """長度使用建議"""
    
    # 推薦長度 - 效果良好
    short_titles = ["START", "OK", "ERROR", "DONE", "READY"]
    
    for title in short_titles:
        logger.ascii_header(title, font="slant", border_style="green")
    
    # 中等長度 - 可接受
    medium_titles = ["STARTUP", "SUCCESS", "WARNING", "COMPLETE"]
    
    for title in medium_titles:
        logger.ascii_header(title, font="standard", border_style="blue")
    
    # 較長文字 - 需要注意效果
    logger.ascii_header("DEPLOYMENT", font="small", border_style="yellow")
    logger.warning("較長的文字建議使用小型字體")

length_guidelines_demo()
```

## 🎨 創意應用

### 動畫效果模擬

```python
def animation_effect_demo():
    """模擬動畫效果"""
    import time
    
    # 倒數計時效果
    for i in range(3, 0, -1):
        logger.ascii_header(str(i), font="doom", border_style="yellow")
        time.sleep(1)
    
    logger.ascii_header("GO", font="doom", border_style="green")
    logger.success("倒數計時完成!")

animation_effect_demo()
```

### 品牌標識

```python
def branding_demo():
    """品牌標識展示"""
    
    # 公司標識
    logger.ascii_header("COMPANY", font="block", border_style="blue")
    logger.info("這是公司的品牌標識")
    
    # 產品標識
    logger.ascii_header("PRODUCT", font="slant", border_style="magenta")
    logger.info("這是產品的品牌標識")
    
    # 版本標識
    logger.ascii_header("V2.0", font="digital", border_style="cyan")
    logger.info("版本資訊標識")

branding_demo()
```

## 🚀 完整範例

綜合所有技巧的完整範例：

```python
def complete_ascii_demo():
    """ASCII 藝術功能完整展示"""
    import time
    
    logger = create_logger(
    name="ascii-art_demo",
    log_dir="complete_ascii_demo",
    level="INFO"
)
    
    # 1. 歡迎標題
    logger.ascii_header("WELCOME", font="slant", border_style="blue")
    logger.info("歡迎使用 ASCII 藝術展示")
    
    # 2. 字體展示
    logger.ascii_header("FONTS", font="standard", border_style="cyan")
    fonts = ["standard", "slant", "doom", "small", "block"]
    
    for font in fonts:
        logger.ascii_header("DEMO", font=font, border_style="green")
        logger.info(f"字體: {font}")
        time.sleep(0.5)
    
    # 3. 顏色展示
    logger.ascii_header("COLORS", font="standard", border_style="cyan")
    colors = ["red", "green", "blue", "yellow", "magenta"]
    
    for color in colors:
        logger.ascii_header("COLOR", font="slant", border_style=color)
        logger.info(f"顏色: {color}")
        time.sleep(0.5)
    
    # 4. 應用場景
    logger.ascii_header("APPS", font="standard", border_style="cyan")
    
    # 模擬啟動
    logger.ascii_header("START", font="slant", border_style="blue")
    logger.info("模擬應用啟動...")
    
    # 模擬處理
    logger.ascii_header("WORK", font="small", border_style="yellow")
    logger.info("模擬工作處理...")
    
    # 模擬完成
    logger.ascii_header("DONE", font="block", border_style="green")
    logger.success("展示完成!")
    
    # 5. 結束標題
    logger.ascii_header("GOODBYE", font="slant", border_style="magenta")
    logger.info("感謝觀看 ASCII 藝術展示")

if __name__ == "__main__":
    complete_ascii_demo()
```

這個完整的範例展示了 ASCII 藝術的所有主要功能和創意應用。運行這些程式碼，你會看到令人印象深刻的視覺效果！