# 公開API列表 - 這些應該包含在文檔中

## 核心公開API
# 這些是主要的用戶接口，應詳細記錄

# 工廠函數與管理
create_logger       # 創建日誌實例
default_logger      # 獲取默認日誌實例
get_logger          # 根據名稱獲取日誌實例
set_logger          # 手動註冊日誌實例
unregister_logger   # 取消註冊日誌實例
list_loggers        # 列出所有已註冊的日誌實例

# 日誌格式化函數
print_block         # 打印區塊日誌
print_ascii_header  # 打印ASCII藝術標題
print_ascii_block   # 打印帶有ASCII標題的區塊
is_ascii_only       # 檢查是否僅包含ASCII字符
print_figlet_header # 打印FIGlet藝術標題
print_figlet_block  # 打印帶有FIGlet標題的區塊
get_figlet_fonts    # 獲取所有可用的FIGlet字體

# 配置相關
LOG_LEVEL           # 預設日誌級別
LOG_ROTATION        # 預設日誌輪換大小
LOG_PATH            # 預設日誌儲存路徑
LOG_NAME_FORMATS    # 預定義的日誌檔案名格式
OUTPUT_DESTINATIONS # 輸出目標類型
LogLevelEnum        # 日誌級別枚舉類別
LoggerConfig        # 日誌配置類

# 核心功能
configure_logger    # 配置日誌系統

# 集成功能
InterceptHandler    # 攔截標準日誌庫的日誌並轉發給 Loguru
configure_uvicorn   # 配置Uvicorn使用Loguru格式化輸出
setup_fastapi_logging # 為FastAPI設置日誌功能
get_logger_dependency # 創建返回logger實例的依賴函數

# 清理功能
LoggerCleaner       # 日誌清理器類別

# 日誌實例已擴展的方法
EnhancedLogger:
  - block             # 輸出帶有邊框的日誌區塊
  - console_block     # 輸出帶有邊框的日誌區塊，僅輸出到控制台
  - file_block        # 輸出帶有邊框的日誌區塊，僅輸出到日誌文件
  - ascii_header      # 輸出ASCII藝術標題
  - console_ascii_header # 輸出ASCII藝術標題，僅輸出到控制台
  - file_ascii_header # 輸出ASCII藝術標題，僅輸出到日誌文件
  - ascii_block       # 輸出帶有ASCII標題的日誌區塊
  - console_ascii_block # 輸出帶有ASCII標題的日誌區塊，僅輸出到控制台
  - file_ascii_block  # 輸出帶有ASCII標題的日誌區塊，僅輸出到日誌文件
  - figlet_header     # 輸出FIGlet藝術標題（如果有安裝pyfiglet）
  - console_figlet_header # 輸出FIGlet藝術標題，僅輸出到控制台
  - file_figlet_header # 輸出FIGlet藝術標題，僅輸出到日誌文件
  - figlet_block      # 輸出帶有FIGlet標題的日誌區塊
  - console_figlet_block # 輸出帶有FIGlet標題的日誌區塊，僅輸出到控制台
  - file_figlet_block # 輸出帶有FIGlet標題的日誌區塊，僅輸出到日誌文件
  - get_figlet_fonts  # 獲取所有可用的FIGlet字體
  - console           # 僅在控制台顯示的日誌記錄方法
  - console_debug     # 僅在控制台顯示的調試級別日誌
  - console_info      # 僅在控制台顯示的資訊級別日誌
  - console_success   # 僅在控制台顯示的成功級別日誌
  - console_warning   # 僅在控制台顯示的警告級別日誌
  - console_error     # 僅在控制台顯示的錯誤級別日誌
  - console_critical  # 僅在控制台顯示的嚴重錯誤級別日誌
  - file              # 僅寫入文件的日誌記錄方法
  - file_debug        # 僅寫入文件的調試級別日誌
  - file_info         # 僅寫入文件的資訊級別日誌
  - file_success      # 僅寫入文件的成功級別日誌
  - file_warning      # 僅寫入文件的警告級別日誌
  - file_error        # 僅寫入文件的錯誤級別日誌
  - file_critical     # 僅寫入文件的嚴重錯誤級別日誌
  - dev               # 開發模式日誌記錄方法（console的別名）
  - dev_debug         # 開發模式調試級別日誌（console_debug的別名）
  - dev_info          # 開發模式資訊級別日誌（console_info的別名）
  - dev_success       # 開發模式成功級別日誌（console_success的別名）
  - dev_warning       # 開發模式警告級別日誌（console_warning的別名）
  - dev_error         # 開發模式錯誤級別日誌（console_error的別名）
  - dev_critical      # 開發模式嚴重錯誤級別日誌（console_critical的別名）

# 私有/內部API列表 - 這些不應包含在公開文檔中

## 核心私有API和輔助函數
# 這些主要是內部實現細節，不應公開給最終用戶

# 格式化工具
create_target_method     # 創建目標導向格式化方法
add_target_methods       # 為logger實例添加目標導向格式化方法
ensure_target_parameters # 確保方法接受目標導向參數
_console_only            # 僅在控制台顯示的日誌記錄內部方法
_file_only               # 僅寫入文件的日誌記錄內部方法
add_custom_output_methods # 為日誌實例添加自定義輸出方法
get_console              # 獲取Rich Console實例

# 處理器與格式化器
create_destination_filters # 創建基於目標的過濾器函數
format_filename         # 根據提供的格式生成日誌檔案名
create_formatter        # 創建日誌格式化函數
adapt_rotation_value    # 調整輪換值的格式，確保正確設置

# 內部工廠和方法擴展
add_custom_methods      # 為logger實例添加所有自定義方法
add_output_methods      # 為logger實例添加輸出目標相關方法
add_format_methods      # 為logger實例添加格式化相關方法
register_extension_method # 註冊自定義擴展方法到logger實例
create_block_method     # 為logger實例創建block方法
create_ascii_methods    # 為logger實例創建ASCII藝術相關方法
create_figlet_methods   # 為logger實例創建FIGlet藝術相關方法
format_block_message    # 格式化區塊消息為單一字符串

# 內部類型與輔助函數
_has_figlet             # FIGlet功能是否可用
_has_uvicorn            # Uvicorn整合是否可用
_has_fastapi            # FastAPI整合是否可用
has_figlet              # 檢查FIGlet功能是否可用 
has_uvicorn             # 檢查Uvicorn整合是否可用
default_config          # 創建默認配置實例
_logger_registry        # 全局logger實例註冊表
_logger_file_paths      # 保存logger實例的文件路徑
log_path_global         # 全域變數，用於儲存日誌路徑