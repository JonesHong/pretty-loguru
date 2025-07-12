#!/usr/bin/env python3
"""
FIGlet Demo - FIGlet 文字藝術演示

這個範例展示：
1. FIGlet 文字藝術標題
2. 不同字體效果
3. 應用啟動畫面設計
4. 品牌視覺效果

運行方式：
    pip install pyfiglet  # 需要安裝 pyfiglet
    python figlet_demo.py

注意：需要先安裝 pyfiglet: pip install pyfiglet
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
from pretty_loguru.formats import has_figlet
import time

def check_figlet_availability():
    """檢查 FIGlet 是否可用"""
    if not has_figlet():
        print("❌ FIGlet 功能不可用")
        print("請安裝 pyfiglet: pip install pyfiglet")
        return False
    
    print("✅ FIGlet 功能已啟用")
    return True

def basic_figlet_demo():
    """基本 FIGlet 演示"""
    logger = create_logger("figlet_demo", log_path="./logs")
    
    print("=== 基本 FIGlet 文字藝術演示 ===\n")
    
    try:
        # 1. 歡迎標題 - 使用基本字體
        logger.figlet_header("WELCOME")
        logger.info("歡迎使用 FIGlet 文字藝術功能!")
        
        # 2. 成功訊息
        logger.figlet_header("SUCCESS", border_style="green")
        logger.success("操作成功完成!")
        
        # 3. 警告訊息  
        logger.figlet_header("WARNING", border_style="yellow")
        logger.warning("注意：發現潛在問題")
        
    except Exception as e:
        logger.error(f"FIGlet 演示失敗: {e}")
        logger.info("FIGlet 功能可能需要兼容性調整")
        # 降級到 ASCII 藝術
        logger.ascii_header("WELCOME", font="slant", border_style="blue")
        logger.info("使用 ASCII 藝術作為替代方案")

def font_showcase():
    """字體展示"""
    logger = create_logger("font_showcase", log_path="./logs")
    
    print("\n=== FIGlet 字體展示 ===\n")
    
    fonts = ["slant", "small", "mini", "digital", "big"]
    
    for font in fonts:
        try:
            logger.info(f"展示字體: {font}")
            logger.figlet_header("DEMO", font=font, border_style="blue")
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"字體 {font} 不可用: {e}")

def application_branding():
    """應用品牌化演示"""
    logger = create_logger("brand_app", log_path="./logs")
    
    print("\n=== 應用品牌化演示 ===\n")
    
    # 公司品牌標題
    logger.figlet_header("MyCompany", font="slant", border_style="blue")
    
    # 產品資訊
    brand_info = [
        "產品: LogSystem Pro",
        "版本: v3.0.0", 
        "作者: Development Team",
        "網站: https://mycompany.com",
        "啟動時間: " + time.strftime("%Y-%m-%d %H:%M:%S")
    ]
    logger.block("品牌資訊", brand_info, border_style="blue")
    
    # 產品標題
    logger.figlet_header("LogSys", font="small", border_style="green")
    logger.console_success("LogSystem Pro 已成功啟動!")

def status_displays():
    """狀態顯示演示"""
    logger = create_logger("status_display", log_path="./logs")
    
    print("\n=== 狀態顯示演示 ===\n")
    
    # 1. 初始化
    logger.figlet_header("INIT", font="mini", border_style="blue")
    logger.info("系統初始化中...")
    time.sleep(1)
    
    # 2. 載入中
    logger.figlet_header("LOAD", font="mini", border_style="yellow")
    logger.info("正在載入模組...")
    time.sleep(1)
    
    # 3. 就緒狀態
    logger.figlet_header("READY", font="small", border_style="green")
    logger.success("系統準備就緒!")
    
    # 4. 錯誤狀態
    time.sleep(1)
    logger.figlet_header("ERROR", font="small", border_style="red")
    logger.error("發生系統錯誤!")

def creative_usage():
    """創意使用演示"""
    logger = create_logger("creative_demo", log_path="./logs")
    
    print("\n=== 創意使用演示 ===\n")
    
    # 1. 日期標題
    today = time.strftime("%m-%d")
    logger.figlet_header(today, font="digital", border_style="blue")
    logger.info(f"今日日期: {time.strftime('%Y年%m月%d日')}")
    
    # 2. 數字顯示
    logger.info("顯示重要數字")
    logger.figlet_header("2024", font="big", border_style="green")
    
    # 3. 狀態碼
    logger.info("系統狀態碼")
    logger.figlet_header("200", font="small", border_style="green")
    logger.success("HTTP 200 - 一切正常")
    
    # 4. 版本號
    logger.info("軟體版本")
    logger.figlet_header("v3.0", font="slant", border_style="blue")

def deployment_workflow():
    """部署工作流程 FIGlet 演示"""
    logger = create_logger("deploy_figlet", log_path="./logs")
    
    print("\n=== 部署工作流程 FIGlet 演示 ===\n")
    
    # 1. 部署開始
    logger.figlet_header("DEPLOY", font="slant", border_style="blue")
    deploy_info = [
        "環境: Production",
        "分支: main",
        "版本: v2.1.0 → v2.2.0", 
        "部署者: DevOps Team"
    ]
    logger.block("部署資訊", deploy_info, border_style="blue")
    time.sleep(2)
    
    # 2. 建置階段
    logger.figlet_header("BUILD", font="small", border_style="yellow")
    logger.info("正在編譯程式碼...")
    time.sleep(1)
    
    # 3. 測試階段
    logger.figlet_header("TEST", font="small", border_style="yellow")
    logger.info("執行自動化測試...")
    time.sleep(1)
    
    # 4. 完成
    logger.figlet_header("DONE", font="slant", border_style="green")
    success_info = [
        "✅ 部署成功完成!",
        "耗時: 3分25秒",
        "服務狀態: 健康運行",
        "可用性: 99.9%"
    ]
    logger.block("部署結果", success_info, border_style="green")

def main():
    """主函數"""
    print("=== Pretty Loguru FIGlet 文字藝術完整演示 ===")
    
    # 檢查 FIGlet 可用性
    if not check_figlet_availability():
        return
    
    try:
        # 1. 基本功能
        basic_figlet_demo()
        
        # 2. 字體展示
        font_showcase()
        
        # 3. 應用品牌化
        application_branding()
        
        # 4. 狀態顯示
        status_displays()
        
        # 5. 創意使用
        creative_usage()
        
        # 6. 部署工作流程
        deployment_workflow()
        
        print("\n" + "="*50)
        print("FIGlet 演示完成!")
        print("查看 ./logs/ 目錄中的日誌檔案")
        print("FIGlet 讓您的應用標題更具視覺衝擊力!")
        
    except Exception as e:
        print(f"❌ 演示過程中發生錯誤: {e}")
        print("請確認已正確安裝 pyfiglet: pip install pyfiglet")

if __name__ == "__main__":
    main()