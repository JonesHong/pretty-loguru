#!/usr/bin/env python3
"""
Direct Library Access - 底層庫直接存取演示

這個範例展示：
1. 使用 Advanced API 直接存取底層庫
2. 庫可用性檢查和條件使用
3. 混合使用 pretty-loguru 和原生庫
4. 高性能和靈活性的平衡

運行方式：
    python direct_library_access.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
from pretty_loguru.advanced import get_available_libraries, check_library
import time

def check_available_libraries():
    """檢查可用的底層庫"""
    print("=== 檢查可用的底層庫 ===\n")
    
    available = get_available_libraries()
    
    for lib_name, is_available in available.items():
        status = "✅ 可用" if is_available else "❌ 不可用"
        print(f"{lib_name:10}: {status}")
        
        if not is_available:
            install_cmd = {
                'rich': 'pip install rich',
                'art': 'pip install art', 
                'pyfiglet': 'pip install pyfiglet'
            }.get(lib_name, f'請檢查 {lib_name} 安裝')
            print(f"           安裝命令: {install_cmd}")
    
    print()
    return available

def direct_loguru_usage():
    """直接使用 loguru 的進階功能"""
    print("=== 直接使用 Loguru 進階功能 ===\n")
    
    if not check_library('loguru'):
        print("❌ Loguru 不可用")
        return
    
    from pretty_loguru.advanced import loguru_logger
    
    # 1. 添加自訂 sink
    print("1. 添加自訂日誌輸出")
    
    # 自訂格式化器
    custom_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # 添加檔案日誌
    loguru_logger.add(
        "./logs/advanced_loguru_{time}.log",
        format=custom_format,
        level="DEBUG",
        rotation="1 MB",
        retention="7 days",
        compression="zip",
        enqueue=True,  # 異步處理，提高性能
        backtrace=True,
        diagnose=True
    )
    
    # 2. 使用 bind 添加上下文
    print("2. 添加上下文資訊")
    contextual_logger = loguru_logger.bind(user_id="12345", session="abc-123")
    contextual_logger.info("這是帶有上下文的日誌")
    
    # 3. 使用 patch 動態添加資訊
    print("3. 動態添加資訊")
    def add_hostname(record):
        record["extra"]["hostname"] = "server-01"
        record["extra"]["app_version"] = "2.1.0"
    
    # 使用 patch() 會回傳「新的 logger」，不會就地修改原本的 logger
    patched_logger = loguru_logger.patch(add_hostname)
    patched_logger.info("這是帶有動態資訊的日誌")
    
    print("✅ Loguru 進階功能演示完成\n")

def direct_rich_usage():
    """直接使用 Rich 的進階功能"""
    print("=== 直接使用 Rich 進階功能 ===\n")
    
    if not check_library('rich'):
        print("❌ Rich 不可用，請安裝: pip install rich")
        return
    
    from pretty_loguru.advanced import Console, Table, Panel, Progress, Layout, Live
    from pretty_loguru.advanced import Text, Syntax, Tree
    
    console = Console()
    
    # 1. 複雜表格展示
    print("1. 複雜表格展示")
    table = Table(title="🚀 系統監控儀表板", show_header=True, header_style="bold magenta")
    table.add_column("服務", style="cyan", no_wrap=True)
    table.add_column("狀態", style="green")
    table.add_column("CPU", justify="right", style="yellow")
    table.add_column("記憶體", justify="right", style="blue")
    table.add_column("響應時間", justify="right", style="red")
    
    table.add_row("Web Server", "🟢 運行中", "45%", "2.1GB", "245ms")
    table.add_row("Database", "🟢 運行中", "62%", "4.8GB", "12ms")
    table.add_row("Redis Cache", "🟡 警告", "78%", "1.2GB", "8ms")
    table.add_row("API Gateway", "🟢 運行中", "35%", "892MB", "156ms")
    
    console.print(table)
    
    # 2. 語法高亮
    print("\\n2. 程式碼語法高亮")
    code = '''
def hello_world():
    """A simple function."""
    return "Hello, World!"
    
result = hello_world()
print(result)
'''
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="Python 程式碼", border_style="green"))
    
    # 3. 樹狀結構
    print("\\n3. 檔案樹狀結構")
    tree = Tree("📁 專案結構")
    python_tree = tree.add("🐍 Python 專案")
    python_tree.add("📄 main.py")
    python_tree.add("📄 config.py")
    src_tree = python_tree.add("📁 src/")
    src_tree.add("📄 app.py")
    src_tree.add("📄 utils.py")
    tests_tree = python_tree.add("📁 tests/")
    tests_tree.add("📄 test_app.py")
    
    console.print(tree)
    
    # 4. 進度條演示
    print("\\n4. 進度條演示")
    with Progress() as progress:
        task = progress.add_task("[cyan]處理數據...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)
    
    print("✅ Rich 進階功能演示完成\\n")

def direct_art_usage():
    """直接使用 Art 庫功能"""
    print("=== 直接使用 Art 庫功能 ===\\n")
    
    if not check_library('art'):
        print("❌ Art 不可用，請安裝: pip install art")
        return
    
    from pretty_loguru.advanced import text2art, tprint, FONT_NAMES
    
    # 1. 文字轉 ASCII 藝術
    print("1. 文字轉 ASCII 藝術")
    ascii_art = text2art("HELLO", font="slant")
    print(ascii_art)
    
    # 2. 直接列印 ASCII 藝術
    print("2. 直接列印模式")
    tprint("WORLD", font="block")
    
    # 3. 顯示可用字體 (部分)
    print("3. 可用字體範例 (前10個):")
    if FONT_NAMES:
        for font in list(FONT_NAMES)[:5]:  # 只顯示前5個避免輸出過多
            try:
                art_text = text2art("Art", font=font)
                print(f"字體: {font}")
                print(art_text)
                print("-" * 40)
            except:
                print(f"字體 {font} 無法使用")
    
    print("✅ Art 庫功能演示完成\\n")

def direct_pyfiglet_usage():
    """直接使用 PyFiglet 功能"""
    print("=== 直接使用 PyFiglet 功能 ===\\n")
    
    if not check_library('pyfiglet'):
        print("❌ PyFiglet 不可用，請安裝: pip install pyfiglet")
        return
    
    from pretty_loguru.advanced import Figlet, FigletFont
    
    # 1. 基本 FIGlet 使用
    print("1. 基本 FIGlet 使用")
    f = Figlet(font='slant')
    print(f.renderText('PyFiglet'))
    
    # 2. 不同字體展示
    print("2. 不同字體展示")
    fonts = ['small', 'mini', 'digital']
    for font in fonts:
        try:
            f = Figlet(font=font)
            print(f"字體: {font}")
            print(f.renderText('Demo'))
            print("-" * 30)
        except:
            print(f"字體 {font} 不可用")
    
    # 3. 自訂寬度
    print("3. 自訂寬度設定")
    f = Figlet(font='slant', width=100)
    print(f.renderText('Wide Text'))
    
    print("✅ PyFiglet 功能演示完成\\n")

def hybrid_usage_example():
    """混合使用範例 - 結合 pretty-loguru 和底層庫"""
    print("=== 混合使用範例 ===\\n")
    
    # 使用 pretty-loguru 的簡便性
    logger = create_logger("hybrid_demo", log_dir="./logs")
    
    logger.info("開始混合使用演示")
    
    # 使用 Rich 進行複雜顯示
    if check_library('rich'):
        from pretty_loguru.advanced import Console, Panel, Table
        
        console = Console()
        
        # 創建複雜的狀態面板
        status_table = Table(show_header=False, box=None)
        status_table.add_column("項目", style="cyan")
        status_table.add_column("值", style="green")
        
        status_table.add_row("系統狀態", "🟢 正常")
        status_table.add_row("CPU 使用率", "45%")
        status_table.add_row("記憶體使用", "2.1GB / 8GB")
        status_table.add_row("活躍連接", "1,247")
        
        panel = Panel(
            status_table,
            title="[bold blue]系統監控面板[/bold blue]",
            border_style="blue"
        )
        console.print(panel)
        
        # 在 pretty-loguru 中記錄這個操作
        logger.success("系統監控面板已顯示")
    
    # 使用 loguru 的進階日誌功能
    if check_library('loguru'):
        from pretty_loguru.advanced import loguru_logger
        
        # 添加結構化日誌
        structured_data = {
            "event": "system_check",
            "cpu_usage": 45,
            "memory_usage": 2.1,
            "active_connections": 1247,
            "status": "healthy"
        }
        
        loguru_logger.bind(**structured_data).info("系統檢查完成")
        logger.info("結構化日誌已記錄")
    
    # 使用 Art 創建視覺分隔
    if check_library('art'):
        from pretty_loguru.advanced import text2art
        separator = text2art("---", font="small")
        print(separator)
        logger.info("視覺分隔符已添加")
    
    logger.success("混合使用演示完成")

def performance_comparison():
    """性能對比演示"""
    print("=== 性能對比演示 ===\\n")
    
    logger = create_logger("performance_test", log_dir="./logs")
    
    # 1. pretty-loguru 標準用法
    print("1. pretty-loguru 標準用法測試")
    start_time = time.time()
    for i in range(100):
        logger.info(f"標準日誌訊息 {i}")
    standard_time = time.time() - start_time
    print(f"標準用法耗時: {standard_time:.4f} 秒")
    
    # 2. 直接使用 loguru (如果可用)
    if check_library('loguru'):
        from pretty_loguru.advanced import loguru_logger
        
        print("2. 直接使用 loguru 測試")
        start_time = time.time()
        for i in range(100):
            loguru_logger.info(f"直接 loguru 訊息 {i}")
        direct_time = time.time() - start_time
        print(f"直接用法耗時: {direct_time:.4f} 秒")
        
        performance_ratio = standard_time / direct_time if direct_time > 0 else 0
        print(f"性能比率: {performance_ratio:.2f}x")
    
    logger.info("性能對比測試完成")

def main():
    """主函數"""
    print("=== Pretty Loguru Advanced API 完整演示 ===\\n")
    
    # 1. 檢查庫可用性
    available_libs = check_available_libraries()
    
    # 2. 底層庫直接使用演示
    direct_loguru_usage()
    direct_rich_usage()
    direct_art_usage()
    direct_pyfiglet_usage()
    
    # 3. 混合使用演示
    hybrid_usage_example()
    
    # 4. 性能對比
    performance_comparison()
    
    print("\\n" + "="*60)
    print("Advanced API 演示完成!")
    print("\\n💡 重點回顧:")
    print("• Advanced API 提供底層庫的完整功能")
    print("• 可以混合使用簡化 API 和原生功能")
    print("• 庫可用性檢查確保代碼的穩定性")
    print("• 性能關鍵場景可以直接使用底層庫")
    print("\\n📁 檢查 ./logs/ 目錄查看生成的日誌檔案")

if __name__ == "__main__":
    main()
