#!/usr/bin/env python3
"""
ASCII Art Demo - ASCII 藝術標題演示

這個範例展示：
1. ASCII 藝術標題
2. 不同字體效果  
3. 品牌化和視覺標識
4. 應用啟動畫面

運行方式：
    python ascii_art.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets
import time

def basic_ascii_demo():
    """基本 ASCII 藝術演示"""
    logger = create_logger("ascii_demo", log_dir="./logs")
    
    print("=== 基本 ASCII 藝術演示 ===\n")
    
    # 1. 簡單的 ASCII 標題
    logger.ascii_header("WELCOME", font="slant")
    logger.info("歡迎使用 ASCII 藝術功能!")
    
    # 2. 成功訊息
    logger.ascii_header("SUCCESS", font="slant", border_style="green")
    logger.success("操作成功完成!")
    
    # 3. 警告訊息
    logger.ascii_header("WARNING", font="slant", border_style="yellow")
    logger.warning("注意：發現潛在問題")

def application_branding():
    """應用品牌化演示"""
    logger = create_logger("my_app", log_dir="./logs")
    
    print("\n=== 應用品牌化演示 ===\n")
    
    # 應用啟動畫面
    logger.ascii_header("MyApp", font="slant", border_style="blue")
    
    startup_info = [
        "版本: v2.1.0",
        "作者: Your Company", 
        "網站: https://myapp.com",
        "啟動時間: " + time.strftime("%Y-%m-%d %H:%M:%S")
    ]
    logger.block("應用資訊", startup_info, border_style="blue")
    
    log_to_targets(logger, "MyApp 已成功啟動!", level="SUCCESS", console_only=True)

def status_headers():
    """狀態標題演示"""
    logger = create_logger("status_app", log_dir="./logs")
    logger.ascii_header("WELCOME")
    print("\n=== 狀態標題演示 ===\n")
    
    # 1. 初始化階段
    logger.ascii_header("INIT", font="slant", border_style="blue")
    logger.info("正在初始化系統...")
    time.sleep(1)
    
    # 2. 載入階段  
    logger.ascii_header("LOADING", font="slant", border_style="yellow")
    logger.info("正在載入配置檔案...")
    time.sleep(1)
    
    # 3. 準備就緒
    logger.ascii_header("READY", font="slant", border_style="green")
    logger.success("系統準備就緒!")
    
    # 4. 錯誤狀態
    time.sleep(1)
    logger.ascii_header("ERROR", font="slant", border_style="red") 
    logger.error("發生嚴重錯誤!")

def deployment_workflow():
    """部署工作流程演示"""
    logger = create_logger("deploy_app", log_dir="./logs")
    
    print("\n=== 部署工作流程演示 ===\n")
    
    # 1. 部署開始
    logger.ascii_header("DEPLOY", font="slant", border_style="blue")
    deploy_steps = [
        "環境: Production",
        "分支: main", 
        "提交: abc123def",
        "部署者: DevOps Team"
    ]
    logger.block("部署資訊", deploy_steps, border_style="blue")
    logger.info("開始部署流程...")
    
    time.sleep(2)
    
    # 2. 測試階段
    logger.ascii_header("TESTING", font="slant", border_style="yellow")
    test_results = [
        "單元測試: ✓ 通過 (124/124)",
        "整合測試: ✓ 通過 (45/45)",
        "性能測試: ✓ 通過",
        "安全掃描: ✓ 通過"
    ]
    logger.block("測試結果", test_results, border_style="green")
    
    time.sleep(2)
    
    # 3. 部署成功
    logger.ascii_header("SUCCESS", font="slant", border_style="green")
    success_info = [
        "✅ 部署成功完成!",
        "版本: v2.1.0 → v2.2.0", 
        "部署時間: 3分15秒",
        "服務狀態: 健康運行",
        "可用性: 99.9%"
    ]
    logger.block("部署結果", success_info, border_style="green")
    logger.success("🎉 部署流程全部完成!")

def monitoring_dashboard():
    """監控儀表板演示"""
    logger = create_logger("monitor", log_dir="./logs")
    
    print("\n=== 監控儀表板演示 ===\n")
    
    # 系統監控標題
    logger.ascii_header("MONITOR", font="slant", border_style="blue")
    
    # 系統健康狀態
    health_data = [
        "🟢 Web 服務: 正常 (99.9% 正常運行時間)",
        "🟢 資料庫: 正常 (連接池: 85/100)",
        "🟢 快取: 正常 (Redis 記憶體: 2.1GB/8GB)",
        "🟡 磁碟空間: 警告 (使用率: 78%)",
        "🔴 外部 API: 異常 (3rd-party service 離線)"
    ]
    logger.block("📊 系統健康狀態", health_data, border_style="blue")
    
    # 實時統計
    stats_data = [
        "當前用戶: 1,247 人在線",
        "每秒請求: 89 req/s",
        "平均響應時間: 245ms",
        "錯誤率: 0.02%",
        "資料傳輸: 15.2MB/s"
    ]
    logger.block("📈 實時統計", stats_data, border_style="green")

def main():
    """主函數"""
    print("=== Pretty Loguru ASCII 藝術完整演示 ===")
    
    # 1. 基本功能
    basic_ascii_demo()
    
    # 2. 應用品牌化
    application_branding()
    
    # 3. 狀態標題
    status_headers()
    
    # 4. 部署流程
    deployment_workflow()
    
    # 5. 監控儀表板  
    monitoring_dashboard()
    
    print("\n" + "="*50)
    print("ASCII 藝術演示完成!")
    print("查看 ./logs/ 目錄中的日誌檔案")
    print("ASCII 藝術讓您的應用更具視覺衝擊力!")

if __name__ == "__main__":
    main()
