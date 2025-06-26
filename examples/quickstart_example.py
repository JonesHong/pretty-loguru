"""
Pretty Loguru 快速開始範例

展示95%用戶最常用的基本功能 - 3分鐘上手指南
"""

from pretty_loguru import create_logger

# === 1. 最簡單的使用方式 ===
print("=== 1. 極簡使用（僅控制台輸出）===")
logger = create_logger("my_app")
logger.info("Hello, Pretty Loguru!")
logger.warning("This is a warning")
logger.error("This is an error")

# === 2. 添加檔案輸出 ===
print("\n=== 2. 添加檔案輸出 ===")
file_logger = create_logger("my_app_with_files", log_path="./logs")
file_logger.info("This appears in both console and file")
file_logger.success("操作成功！")

# === 3. 使用預設配置 ===
print("\n=== 3. 使用預設配置 ===")
# 每日輪轉日誌
daily_logger = create_logger("daily_app", log_path="./logs", preset="daily")
daily_logger.info("Daily rotating logs")

# 每小時輪轉日誌
hourly_logger = create_logger("hourly_app", log_path="./logs", preset="hourly")
hourly_logger.info("Hourly rotating logs")

# === 4. 分別輸出到控制台和檔案 ===
print("\n=== 4. 控制輸出目標 ===")
logger.console_info("僅顯示在控制台")  # 只在控制台顯示
logger.file_error("僅寫入檔案")        # 只寫入檔案

# === 5. 漂亮的區塊輸出 ===
print("\n=== 5. 區塊格式輸出 ===")
logger.block(
    "系統狀態",
    [
        "CPU: 45%",
        "記憶體: 60%", 
        "磁碟: 120GB 可用",
        "狀態: 正常運行"
    ],
    border_style="green"
)

# === 6. ASCII 藝術標題 ===
print("\n=== 6. ASCII 藝術標題 ===")
logger.ascii_header("SUCCESS", font="slant", border_style="green")

print("\n=== 快速開始完成！===")
print("查看 ./logs 目錄中的日誌檔案")