#!/usr/bin/env python3
"""
Blocks Demo - 區塊格式化展示

這個範例展示：
1. 基本區塊格式化
2. 不同邊框樣式
3. 實際應用場景
4. 系統狀態報告

運行方式：
    python blocks.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pretty_loguru import create_logger
from pretty_loguru.addons import log_to_targets
import time

def basic_blocks_demo():
    """基本區塊格式化演示"""
    logger = create_logger("blocks_demo", log_dir="./logs")
    
    print("=== 基本區塊格式化 ===\n")
    
    # 1. 最簡單的區塊
    logger.info("開始演示區塊功能")
    logger.block("歡迎訊息", ["歡迎使用 Pretty Loguru!", "這是一個區塊格式化演示"])
    
    # 2. 帶有多行內容的區塊
    system_info = [
        "系統: Linux Ubuntu 20.04",
        "Python: 3.9.0",
        "記憶體: 8GB",
        "CPU: Intel i7-8565U"
    ]
    logger.block("系統資訊", system_info)

def colored_blocks_demo():
    """彩色區塊演示"""
    logger = create_logger("colored_blocks", log_dir="./logs")
    
    print("\n=== 彩色區塊演示 ===\n")
    
    # 不同顏色的區塊
    logger.block("成功訊息", ["操作完成!", "所有檔案處理成功"], border_style="green")
    
    logger.block("警告訊息", ["記憶體使用率過高", "建議關閉不必要的程序"], border_style="yellow")
    
    logger.block("錯誤報告", ["連接失敗", "無法連接到資料庫"], border_style="red")
    
    logger.block("資訊提示", ["處理中...", "請稍等片刻"], border_style="blue")

def real_world_scenarios():
    """真實應用場景演示"""
    logger = create_logger("app_status", log_dir="./logs")
    
    print("\n=== 真實應用場景 ===\n")
    
    # 1. 應用啟動報告
    log_to_targets(logger, "正在啟動應用...", level="INFO", console_only=True)
    startup_info = [
        "應用名稱: MyWebApp",
        "版本: v2.1.0",
        "環境: Production",
        "端口: 8080",
        "啟動時間: " + time.strftime("%Y-%m-%d %H:%M:%S")
    ]
    logger.block("🚀 應用啟動", startup_info, border_style="green")
    
    # 2. 錯誤處理報告
    time.sleep(1)
    logger.warning("檢測到異常狀況")
    error_details = [
        "錯誤類型: DatabaseConnectionError",
        "錯誤代碼: DB001",
        "發生時間: " + time.strftime("%H:%M:%S"),
        "影響範圍: 用戶登入功能",
        "預估修復時間: 5分鐘"
    ]
    logger.block("⚠️ 錯誤報告", error_details, border_style="red")
    
    # 3. 性能監控報告
    time.sleep(1)
    logger.info("生成性能報告")
    performance_data = [
        "CPU 使用率: 45%",
        "記憶體使用: 2.1GB / 8GB (26%)",
        "磁碟 I/O: 正常",
        "網路延遲: 23ms",
        "活躍連接: 1,247",
        "每秒請求: 89 req/s"
    ]
    logger.block("📊 性能監控", performance_data, border_style="blue")

def deployment_status():
    """部署狀態報告"""
    logger = create_logger("deployment", log_dir="./logs")
    
    print("\n=== 部署狀態報告 ===\n")
    
    logger.info("開始部署流程")
    
    # 1. 部署準備階段
    prep_steps = [
        "✓ 代碼編譯完成",
        "✓ 測試全部通過", 
        "✓ 安全掃描通過",
        "✓ 備份資料庫完成",
        "→ 準備部署到生產環境"
    ]
    logger.block("🔧 部署準備", prep_steps, border_style="blue")
    
    time.sleep(1)
    
    # 2. 部署進行中
    deploy_progress = [
        "正在停止舊版本服務...",
        "正在部署新版本代碼...",
        "正在更新資料庫 schema...",
        "正在重啟服務...",
        "正在進行健康檢查..."
    ]
    logger.block("⚡ 部署進行中", deploy_progress, border_style="yellow")
    
    time.sleep(2)
    
    # 3. 部署完成
    deploy_result = [
        "✅ 部署成功完成!",
        "版本: v2.1.0 → v2.2.0",
        "部署時間: 2分30秒",
        "停機時間: 45秒",
        "健康檢查: 通過",
        "服務狀態: 正常運行"
    ]
    logger.block("🎉 部署完成", deploy_result, border_style="green")
    
    logger.success("部署流程全部完成")

def main():
    """主函數"""
    print("=== Pretty Loguru 區塊格式化完整演示 ===")
    
    # 1. 基本功能
    basic_blocks_demo()
    
    # 2. 彩色區塊
    colored_blocks_demo()
    
    # 3. 真實場景
    real_world_scenarios()
    
    # 4. 部署報告
    deployment_status()
    
    print("\n" + "="*50)
    print("演示完成！")
    print("查看 ./logs/ 目錄中的日誌檔案")
    print("您會發現區塊格式化讓日誌更加清晰易讀！")

if __name__ == "__main__":
    main()
