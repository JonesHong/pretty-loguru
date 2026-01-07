# Snapshot

- Root: `C:/work/pretty-loguru`
- Generated: `2025-12-31 17:24:19`
- Max tree depth: `12`
- Include private symbols: `True`
- Include nested symbols: `False`
- Use .gitignore: `True`

## 專案目錄結構
```text
pretty-loguru/
├── .claude/
│   └── settings.local.json
├── .github/
│   └── workflows/
│       ├── docs.yml
│       └── tests.yml
├── assets/
│   └── logs/
│       ├── example_1_basic/
│       ├── example_2_services/
│       │   ├── api/
│       │   ├── auth/
│       │   └── db/
│       ├── example_3_formats/
│       ├── example_4_targets/
│       ├── example_5_integrations/
│       ├── example_6_advanced/
│       ├── example_6_advanced_new/
│       ├── logger_config.json
│       └── logger_config_example.json
├── configs/
│   ├── app.json
│   └── logging.json
├── docs/
│   ├── .vitepress/
│   ├── api/
│   │   ├── core.md
│   │   ├── formats.md
│   │   ├── index.md
│   │   └── integrations.md
│   ├── en/
│   │   ├── api/
│   │   │   ├── core.md
│   │   │   ├── formats.md
│   │   │   ├── index.md
│   │   │   └── integrations.md
│   │   ├── features/
│   │   │   ├── ascii-art.md
│   │   │   ├── ascii-blocks.md
│   │   │   ├── code-highlighting.md
│   │   │   ├── index.md
│   │   │   ├── native-format.md
│   │   │   ├── rich-blocks.md
│   │   │   └── rich-panel.md
│   │   ├── guide/
│   │   │   ├── basic-usage.md
│   │   │   ├── config-templates.md
│   │   │   ├── custom-config.md
│   │   │   ├── index.md
│   │   │   ├── installation.md
│   │   │   ├── log-rotation.md
│   │   │   ├── performance.md
│   │   │   ├── quick-start.md
│   │   │   └── visual-methods.md
│   │   ├── integrations/
│   │   │   ├── fastapi.md
│   │   │   ├── index.md
│   │   │   └── uvicorn.md
│   │   ├── event_system_examples.md
│   │   ├── index.md
│   │   └── README.md
│   ├── features/
│   │   ├── ascii-art.md
│   │   ├── ascii-blocks.md
│   │   ├── code-highlighting.md
│   │   ├── index.md
│   │   ├── native-format.md
│   │   ├── rich-blocks.md
│   │   └── rich-panel.md
│   ├── guide/
│   │   ├── basic-usage.md
│   │   ├── config-templates.md
│   │   ├── custom-config.md
│   │   ├── index.md
│   │   ├── installation.md
│   │   ├── log-rotation.md
│   │   ├── performance.md
│   │   ├── production.md
│   │   ├── quick-start.md
│   │   └── visual-methods.md
│   ├── integrations/
│   │   ├── fastapi.md
│   │   ├── index.md
│   │   └── uvicorn.md
│   ├── public/
│   │   ├── example_1_en_file_0.png
│   │   ├── example_1_en_file_1.png
│   │   ├── example_1_en_file_2.png
│   │   ├── example_1_en_terminal.png
│   │   ├── example_2_en_file_0.png
│   │   ├── example_2_en_file_1.png
│   │   ├── example_2_en_file_2.png
│   │   ├── example_2_en_file_3.png
│   │   ├── example_2_en_terminal.png
│   │   ├── example_3_en_file_0.png
│   │   ├── example_3_en_file_1.png
│   │   ├── example_3_en_terminal.png
│   │   ├── example_4_en_file_0.png
│   │   ├── example_4_en_file_1.png
│   │   ├── example_4_en_terminal.png
│   │   ├── example_5_en_file_0.png
│   │   ├── example_5_en_file_1.png
│   │   ├── example_5_en_terminal.png
│   │   ├── example_6_en_file_0.png
│   │   ├── example_6_en_file_1.png
│   │   ├── example_6_en_file_2.png
│   │   ├── example_6_en_terminal_1.png
│   │   ├── example_6_en_terminal_2.png
│   │   └── logo.png
│   ├── .env.local
│   ├── .env.production
│   ├── DOCUMENTATION_GUIDE.md
│   ├── event_system_examples.md
│   ├── index.md
│   ├── package.json
│   └── README.md
├── pretty_loguru/
│   ├── addons/
│   │   └── __init__.py
│   ├── advanced/
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cleaner.py
│   │   ├── config.py
│   │   ├── diagnostics.py
│   │   ├── event_system.py
│   │   ├── extension_system.py
│   │   ├── handlers.py
│   │   ├── presets.py
│   │   ├── pretty_event.py
│   │   ├── registry.py
│   │   ├── target_formatter.py
│   │   └── templates.py
│   ├── factory/
│   │   ├── __init__.py
│   │   ├── creator.py
│   │   ├── methods.py
│   │   └── updater.py
│   ├── formats/
│   │   ├── __init__.py
│   │   ├── ascii_art.py
│   │   ├── block.py
│   │   ├── figlet.py
│   │   └── rich_components.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── _errors.py
│   │   ├── fastapi.py
│   │   ├── loki.py
│   │   └── uvicorn.py
│   ├── types/
│   │   ├── __init__.py
│   │   └── protocols.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── validators.py
│   │   └── warn_once.py
│   └── __init__.py
├── test_logs/
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── GIT_CHANGE_REVIEW.md
├── LICENSE
├── LOGIC_REVIEW_v3.md
├── OBSERVABILITY_CHANNELS_AND_NOISE_CONTROL.md
├── PROJECT_SCOPE_AND_REPO_HYGIENE_AUDIT.md
├── pyproject.toml
├── README.md
├── README.zh.md
├── setup.py
├── snapshot.md
├── snapshot.py
└── uv.lock
```

## 函式/類別清單（AST）
### `pretty_loguru/__init__.py`
- **function** `__getattr__(name: ...) -> ...` — 延遲載入 `pretty_loguru.addons` / `pretty_loguru.integrations`。

### `pretty_loguru/advanced/__init__.py`
- **function** `_ensure_pretty_loguru_record_defaults(record: ...) -> ...` — Ensure pretty-loguru's handlers won't crash when formatting a loguru record.
- **function** `get_available_libraries()` — Get a list of available libraries for advanced usage.
- **function** `check_library(library_name: ...) -> ...` — Check if a specific library is available.

### `pretty_loguru/advanced/helpers.py`
- **function** `create_rich_table_log(logger_instance: ..., title: ..., data: ..., log_level: ...=..., table_kwargs: ...=...) -> ...` — Create a Rich table and log it using pretty-loguru logger.
- **function** `create_mixed_ascii_panel(logger_instance: ..., text: ..., panel_title: ...=..., ascii_font: ...=..., panel_style: ...=..., log_level: ...=...) -> ...` — Create ASCII art inside a Rich panel and log it.
- **function** `create_loguru_rich_sink(console: ...=...) -> ...` — Create a Rich Console configured as a Loguru sink.
- **function** `quick_figlet_log(logger_instance: ..., text: ..., font: ...=..., log_level: ...=...) -> ...` — Quick FIGlet text generation and logging.

### `pretty_loguru/core/base.py`
- **function** `get_console() -> ...` — 獲取 Rich Console 實例
- **function** `_get_or_create_pretty_extra_defaults(logger_instance: ...) -> ...` — 取得（或建立）pretty-loguru 需要的 `record['extra']` 預設欄位容器。
- **function** `configure_logger(logger_instance: ..., config: ..., *, reset_handlers: ...=...) -> ...` — 根據 LoggerConfig 配置日誌實例。

### `pretty_loguru/core/cleaner.py`
- **class** `LoggerCleaner` — 日誌清理器類別
- **method** `LoggerCleaner.__init__(self, log_retention: ...=..., log_dir: ...=..., check_interval: ...=..., logger_instance: ...=..., recursive: ...=..., include_patterns: ...=..., exclude_patterns: ...=..., verbose: ...=...) -> ...` — 初始化日誌清理器
- **method** `LoggerCleaner._parse_retention(self, retention: ...) -> ...` — 解析保留時間參數，轉換為 timedelta 物件
- **method** `LoggerCleaner.start(self) -> ...` — 啟動日誌清理線程
- **method** `LoggerCleaner.stop(self) -> ...` — 優雅地停止清理線程
- **method** `LoggerCleaner._log_message(self, message: ..., level: ...=...) -> ...` — 記錄日誌消息
- **method** `LoggerCleaner._should_consider_file(self, file_path: ...) -> ...` — 依 include/exclude 規則判斷是否處理該檔案
- **method** `LoggerCleaner._clean_logs_loop(self) -> ...` — 清理日誌的循環執行函數
- **method** `LoggerCleaner._clean_old_logs(self) -> ...` — 執行實際的日誌清理操作

### `pretty_loguru/core/config.py`
- **class** `UnsetType` — 表示「未設定」的哨兵物件（sentinel）。
- **method** `UnsetType.__repr__(self) -> ...` — 回傳穩定的除錯表示字串（避免印出記憶體位址）。
- **class** `LoggerConfig` — 統一的日誌配置類，支持可重用配置模板和多logger管理
- **method** `LoggerConfig.__post_init__(self)` — 初始化後處理
- **method** `LoggerConfig.validate(self) -> ...` — 輕量配置驗證，避免錯誤延後爆出
- **method** `LoggerConfig.validate_strict(self) -> ...` — 更嚴格的配置驗證，包含常見格式檢查
- **method** `LoggerConfig.apply_to(self, *logger_names: ..., create_if_missing: ...=...)` — 將配置套用到 logger(s)
- **method** `LoggerConfig.update(self, *, restart_cleaner: ...=..., level: ...=..., log_dir: ...=..., rotation: ...=..., retention: ...=..., compression: ...=..., compression_format: ...=..., format: ...=..., component_name: ...=..., subdirectory: ...=..., start_cleaner: ...=..., use_native_format: ...=..., use_proxy: ...=..., preset: ...=..., verbose: ...=..., strict_validation: ...=..., cleaner_include_patterns: ...=..., cleaner_exclude_patterns: ...=..., serialize: ...=..., loki_enabled: ...=..., loki_base_url: ...=..., loki_labels: ...=..., loki_batch_size: ...=..., loki_flush_interval_seconds: ...=..., loki_timeout_seconds: ...=..., loki_tenant_id: ...=..., loki_username: ...=..., loki_password: ...=...) -> ...` — 更新配置並自動套用到所有附加的 logger
- **method** `LoggerConfig._update_attached_loggers(self, restart_cleaner: ...=...)` — 更新所有附加的 logger
- **method** `LoggerConfig.detach(self, *logger_names: ...) -> ...` — 從配置中分離指定的 logger
- **method** `LoggerConfig.update_from_dict(self, overrides: ..., *, restart_cleaner: ...=...) -> ...` — 以 dict 形式更新配置並自動套用到所有附加的 logger。
- **method** `LoggerConfig.detach_all(self) -> ...` — 分離所有附加的 logger
- **method** `LoggerConfig.get_attached_loggers(self) -> ...` — 獲取所有附加的 logger 名稱
- **method** `LoggerConfig.clone(self, **overrides) -> ...` — 克隆配置並可選擇性覆蓋參數
- **method** `LoggerConfig.inherit_from(self, parent_config: ..., **overrides) -> ...` — 從父配置繼承並可選擇性覆蓋參數
- **method** `LoggerConfig.to_dict(self) -> ...` — 將配置轉換為字典，方便序列化。
- **method** `LoggerConfig.from_dict(cls, config_dict: ...) -> ...` — 從字典創建配置實例。
- **method** `LoggerConfig.save_to_file(self, file_path: ...) -> ...` — 將配置保存到 JSON 文件。
- **method** `LoggerConfig.from_file(cls, file_path: ...) -> ...` — 從 JSON 文件載入配置。
- **method** `LoggerConfig.save(self, file_path: ...) -> ...` — 保存配置到文件
- **method** `LoggerConfig.load(cls, file_path: ...) -> ...` — 從文件載入配置
- **method** `LoggerConfig.logger_exists(name: ...) -> ...` — 檢查指定名稱的 logger 是否存在
- **method** `LoggerConfig.__repr__(self) -> ...` — 字符串表示

### `pretty_loguru/core/diagnostics.py`
- **function** `get_cleaner_status() -> ...` — 列出目前活躍的 cleaner 路徑。
- **function** `get_handler_status() -> ...` — 回傳各 logger 的 managed/user handler ids 以便排障。
- **function** `get_default_logger_state() -> ...` — 回報 default_logger 是否已建立。

### `pretty_loguru/core/event_system.py`
- **function** `subscribe(event_name: ..., callback: ...) -> ...` — Subscribes a callback to a specific event. Thread-safe.
- **function** `unsubscribe(event_name: ..., callback: ...) -> ...` — Unsubscribes a callback from a specific event. Thread-safe.
- **function** `post_event(event_name: ..., *args: ..., **kwargs: ...) -> ...` — Posts an event, triggering all subscribed callbacks. Thread-safe.
- **function** `list_events() -> ...` — Lists all registered event names. Thread-safe.
- **function** `clear_events() -> ...` — Clears all event listeners. Thread-safe.
- **function** `list_listeners(event_name: ...) -> ...` — Lists all listeners for a specific event. Thread-safe.
- **function** `event_count() -> ...` — Returns the total number of registered events. Thread-safe.
- **function** `listener_count(event_name: ...) -> ...` — Returns the number of listeners for a specific event. Thread-safe.

### `pretty_loguru/core/extension_system.py`
- **function** `register_extension_method(logger_instance: ..., name: ..., method: ..., overwrite: ...=...) -> ...` — 註冊擴展方法並直接綁定到 Logger 實例
- **function** `get_extension_method(name: ...) -> ...` — 獲取已註冊的擴展方法
- **function** `apply_extensions(logger_instance: ...) -> ...` — 將所有已註冊的擴展方法應用到 Logger 實例
- **function** `list_extensions() -> ...` — 列出所有已註冊的擴展方法
- **function** `clear_extensions() -> ...` — 清除所有已註冊的擴展方法

### `pretty_loguru/core/handlers.py`
- **function** `create_destination_filters() -> ...` — 創建基於目標的過濾器函數，用於控制日誌輸出目標
- **function** `format_filename(component_name: ..., log_name_format: ...=..., name: ...=...) -> ...` — 根據提供的格式生成日誌檔案名，並處理不合法的文件名字符
- **function** `create_formatter(fmt: ...=...) -> ...` — 創建日誌格式化函數
- **function** `adapt_rotation_value(rotation: ...) -> ...` — 調整輪換值的格式，確保正確設置

### `pretty_loguru/core/presets.py`
- **function** `_subtract_one_month(dt: ...) -> ...` — 在不依賴 python-dateutil 的情況下，將日期往前推一個月。
- **function** `_create_rename_function(pattern: ..., custom_format: ...=..., time_source: ...=...) -> ...` — 創建日誌重命名函數
- **function** `create_custom_compression_function(compression_format: ...) -> ...` — 創建自定義壓縮函數
- **function** `get_preset_config(preset_type: ...) -> ...` — 獲取預設配置
- **function** `list_available_presets() -> ...` — 列出所有可用的預設類型
- **function** `register_custom_preset(name: ..., config: ...) -> ...` — 註冊自定義預設
- **class** `PresetFactory` — 簡化的預設工廠類
- **method** `PresetFactory.get_preset(preset_type: ...) -> ...` — 獲取預設配置
- **method** `PresetFactory.list_presets() -> ...` — 列出可用預設

### `pretty_loguru/core/pretty_event.py`
- **class** `PrettyBlockPayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="block"`（v1）。
- **class** `PrettyPanelPayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="panel"`（v1）。
- **class** `PrettyTablePayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="table"`（v1）。
- **class** `PrettyTreePayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="tree"`（v1）。
- **class** `PrettyColumnsPayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="columns"`（v1）。
- **class** `PrettyCodePayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="code"`（v1）。
- **class** `PrettyDiffPayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="diff"`（v1）。
- **class** `PrettyAsciiHeaderPayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="ascii_header"`（v1）。
- **class** `PrettyFigletHeaderPayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="figlet_header"`（v1）。
- **class** `PrettyRenderablePayloadV1(TypedDict)` — `pretty_payload` schema for `pretty_kind="renderable"`（v1）。
- **function** `validate_pretty_payload(kind: ..., payload: ...) -> ...` — 最小化 payload 檢核（避免 renderer/sink 因缺欄位炸掉）。
- **function** `_get_box(box_style: ...) -> ...` — 將使用者輸入的 box style（字串/None）映射為 Rich box 物件。
- **function** `_tree_add(node: ..., value: ...) -> ...` — 遞迴把任意結構（dict/list/primitive）加入 Rich Tree。
- **function** `build_renderable(kind: ..., payload: ...) -> ...` — 由 `pretty_kind` + `pretty_payload` 重建 Rich renderable。
- **function** `render_renderable_to_text(renderable: ..., *, width: ...=...) -> ...` — 將 Rich renderable 渲染為純文字（用於檔案輸出）。

### `pretty_loguru/core/registry.py`
- **function** `register_logger(name: ..., logger: ...) -> ...` — Registers a logger instance by name. Thread-safe.
- **function** `get_logger(name: ...) -> ...` — Retrieves a logger instance by name. Thread-safe.
- **function** `unregister_logger(name: ...) -> ...` — Unregisters a logger instance by name. Thread-safe.
- **function** `list_loggers() -> ...` — Lists the names of all registered loggers. Thread-safe.
- **function** `update_logger(name: ..., logger: ...) -> ...` — Updates an existing logger instance by name. Thread-safe.
- **function** `clear_registry() -> ...` — Clears all registered loggers. Returns the number of loggers cleared. Thread-safe.
- **function** `get_registry_size() -> ...` — Returns the number of registered loggers. Thread-safe.
- **function** `cleanup_unused_loggers() -> ...` — Cleans up loggers that appear to be unused.

### `pretty_loguru/core/target_formatter.py`
- **function** `log_to_targets(logger_instance: ..., message: ..., level: ...=..., console_only: ...=..., file_only: ...=...) -> ...` — 目標日誌函數，支援分離的控制台和檔案輸出
- **function** `mark_file_handler(logger_instance: ..., enabled: ...=...) -> ...` — 標記 logger 是否有檔案輸出 handler，供目標輸出判斷使用
- **function** `ensure_target_parameters(method: ...) -> ...` — 確保格式化方法接受目標導向參數（最新版本：不提供向後相容模式）

### `pretty_loguru/core/templates.py`
- **class** `ConfigTemplates` — 配置模板管理系統
- **method** `ConfigTemplates.development() -> ...` — 開發環境配置
- **method** `ConfigTemplates.production() -> ...` — 生產環境配置
- **method** `ConfigTemplates.testing() -> ...` — 測試環境配置
- **method** `ConfigTemplates.debug() -> ...` — 調試配置
- **method** `ConfigTemplates.performance() -> ...` — 高效能配置
- **method** `ConfigTemplates.minimal() -> ...` — 最小配置
- **method** `ConfigTemplates.detailed() -> ...` — 詳細模式配置
- **method** `ConfigTemplates.simple() -> ...` — 簡單模式配置
- **method** `ConfigTemplates.daily() -> ...` — 每日轮换配置
- **method** `ConfigTemplates.hourly() -> ...` — 每小時轮换配置
- **method** `ConfigTemplates.minute() -> ...` — 每分鐘轮换配置
- **method** `ConfigTemplates.weekly() -> ...` — 每週轮换配置
- **method** `ConfigTemplates.monthly() -> ...` — 每月轮换配置
- **method** `ConfigTemplates.register(cls, name: ..., config: ...) -> ...` — 註冊自定義模板
- **method** `ConfigTemplates.get(cls, name: ...) -> ...` — 獲取模板
- **method** `ConfigTemplates.list_all(cls) -> ...` — 列出所有可用的模板
- **method** `ConfigTemplates.unregister(cls, name: ...) -> ...` — 取消註冊自定義模板
- **method** `ConfigTemplates.clear(cls) -> ...` — 清除所有自定義模板
- **function** `create_config(*, level: ...=..., log_dir: ...=..., rotation: ...=..., retention: ...=..., compression: ...=..., compression_format: ...=..., format: ...=..., component_name: ...=..., subdirectory: ...=..., start_cleaner: ...=..., use_native_format: ...=..., use_proxy: ...=..., preset: ...=..., verbose: ...=..., strict_validation: ...=..., cleaner_include_patterns: ...=..., cleaner_exclude_patterns: ...=..., serialize: ...=..., loki_enabled: ...=..., loki_base_url: ...=..., loki_labels: ...=..., loki_batch_size: ...=..., loki_flush_interval_seconds: ...=..., loki_timeout_seconds: ...=..., loki_tenant_id: ...=..., loki_username: ...=..., loki_password: ...=..., name: ...=...) -> ...` — 創建配置的便利函數（顯式欄位，避免黑盒 `**kwargs`）。
- **function** `config_from_template(template_name: ..., overrides: ...=...) -> ...` — 從模板創建配置（可選 overrides dict）。

### `pretty_loguru/factory/creator.py`
- **function** `_ensure_base_logger_prepared() -> ...` — 使用 loguru public API 時，所有 Pretty-Loguru logger 會共享同一個 core。
- **function** `_install_user_handler_tracking(logger_instance: ...) -> ...` — 追蹤「使用者透過此 logger 實例 add()」建立的 handler ids。
- **function** `_emit_cleaner_message(logger_instance: ..., message: ..., level: ...=..., verbose: ...=...) -> ...` — 統一輸出 cleaner 的提示訊息。
- **function** `_start_cleaner_for_path(log_dir: ..., logger_instance: ...=..., verbose: ...=..., include_patterns: ...=..., exclude_patterns: ...=..., log_retention: ...=...) -> ...` — 為指定路徑啟動清理器，如果該路徑已有清理器則重複使用
- **function** `_stop_all_cleaners() -> ...` — 停止所有活躍的清理器
- **function** `_stop_cleaner_for_path(log_dir: ..., logger_instance: ...=..., verbose: ...=...) -> ...` — 停止指定路徑的清理器（若存在）
- **function** `_restart_cleaner_for_path(log_dir: ..., logger_instance: ...=..., verbose: ...=..., include_patterns: ...=..., exclude_patterns: ...=..., log_retention: ...=...) -> ...` — 重啟指定路徑的清理器，確保設定生效
- **function** `_create_logger_from_config(config: ..., *, enable_addons: ...=...) -> ...` — 根據標準化的 LoggerConfig 物件創建 logger 實例。
- **function** `_resolve_enable_addons(flag: ...) -> ...` — 根據傳入值或環境變數決定是否啟用 addons。
- **function** `create_logger(name: ...=..., config: ...=..., use_native_format: ...=..., log_dir: ...=..., rotation: ...=..., retention: ...=..., compression: ...=..., compression_format: ...=..., level: ...=..., format: ...=..., component_name: ...=..., subdirectory: ...=..., start_cleaner: ...=..., verbose: ...=..., cleaner_include_patterns: ...=..., cleaner_exclude_patterns: ...=..., strict_validation: ...=..., serialize: ...=..., loki_enabled: ...=..., loki_base_url: ...=..., loki_labels: ...=..., loki_batch_size: ...=..., loki_flush_interval_seconds: ...=..., loki_timeout_seconds: ...=..., loki_tenant_id: ...=..., loki_username: ...=..., loki_password: ...=..., preset: ...=..., force_new_instance: ...=..., enable_addons: ...=..., clear_fields: ...=...) -> ...` — 創建或獲取一個 logger 實例。
- **function** `get_logger(name: ...) -> ...` — 根據名稱獲取已註冊的 logger 實例
- **function** `set_logger(name: ..., logger_instance: ...) -> ...` — 手動註冊 logger 實例
- **function** `list_loggers() -> ...` — 列出所有已註冊的 logger 名稱
- **function** `unregister_logger(name: ...) -> ...` — 取消註冊 logger 實例
- **function** `reinit_logger(name: ..., use_native_format: ...=..., log_dir: ...=..., rotation: ...=..., retention: ...=..., compression: ...=..., compression_format: ...=..., level: ...=..., format: ...=..., component_name: ...=..., subdirectory: ...=..., start_cleaner: ...=..., verbose: ...=..., cleaner_include_patterns: ...=..., cleaner_exclude_patterns: ...=..., strict_validation: ...=..., serialize: ...=..., loki_enabled: ...=..., loki_base_url: ...=..., loki_labels: ...=..., loki_batch_size: ...=..., loki_flush_interval_seconds: ...=..., loki_timeout_seconds: ...=..., loki_tenant_id: ...=..., loki_username: ...=..., loki_password: ...=..., preset: ...=..., reset_handlers: ...=..., clear_fields: ...=...) -> ...` — 重新初始化已存在的 logger。
- **function** `default_logger() -> ...` — 獲取默認 logger 實例 - 延遲初始化
- **function** `_warn_unknown_preset(preset_name: ...) -> ...`
- **function** `_get_preset(preset_name: ...)` — 簡化的預設獲取函數
- **function** `cleanup_loggers(names: ...=...) -> ...` — 清理所有註冊的 logger 和清理器。

### `pretty_loguru/factory/methods.py`
- **function** `add_format_methods(logger_instance: ..., console: ...=...) -> ...` — 為 logger 實例添加格式化相關方法
- **function** `add_custom_methods(logger_instance: ..., console: ...=...) -> ...` — 為 logger 實例添加所有自定義方法
- **function** `_install_bind_addons_injection(logger_instance: ..., console: ...) -> ...` — 讓 `logger.bind(...)` 回傳的 logger 也具備 formats 方法。

### `pretty_loguru/factory/updater.py`
- **function** `update_logger_level(name: ..., level: ...) -> ...` — 動態更新 logger 的日誌級別
- **function** `update_logger_config(name: ..., config: ..., restart_cleaner: ...=..., reset_handlers: ...=...) -> ...` — 使用 LoggerConfig 更新現有 logger

### `pretty_loguru/formats/__init__.py`
- **function** `has_figlet() -> ...` — 檢查 FIGlet 功能是否可用

### `pretty_loguru/formats/ascii_art.py`
- **function** `text2art(text, **kwargs)` — `art.text2art` 的 fallback：在未安裝 `art` 時回傳提示字串。
- **function** `_cached_text2art(text: ..., font: ...) -> ...`
- **function** `print_ascii_header(text: ..., font: ...=..., level: ...=..., border_style: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=..., strict: ...=...) -> ...` — 打印 ASCII 藝術標題
- **function** `print_ascii_block(title: ..., lines: ..., header_text: ...=..., font: ...=..., border_style: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=..., strict: ...=...) -> ...` — 打印帶有 ASCII 藝術標題的區塊樣式日誌
- **function** `create_ascii_methods(logger_instance: ..., console: ...=...) -> ...` — 為 logger 實例創建 ASCII 藝術相關方法

### `pretty_loguru/formats/block.py`
- **function** `get_box_style(box_name: ...=...)` — 獲取 box 樣式對象
- **function** `format_block_message(title: ..., lines: ..., separator: ...=..., separator_length: ...=...) -> ...` — 格式化區塊消息為單一字符串
- **function** `print_block(title: ..., lines: ..., border_style: ...=..., box: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 打印區塊樣式的日誌，並寫入到日誌文件
- **function** `create_block_method(logger_instance: ..., console: ...=...) -> ...` — 為 logger 實例創建 block 方法

### `pretty_loguru/formats/figlet.py`
- **function** `print_figlet_header(text: ..., font: ...=..., level: ...=..., border_style: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=..., strict: ...=...) -> ...` — 打印 FIGlet 藝術標題
- **function** `print_figlet_block(title: ..., lines: ..., figlet_header: ...=..., figlet_font: ...=..., border_style: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=..., strict: ...=...) -> ...` — 打印帶有 FIGlet 藝術標題的區塊樣式日誌
- **function** `get_figlet_fonts() -> ...` — 獲取所有可用的 FIGlet 字體
- **function** `create_figlet_methods(logger_instance: ..., console: ...=...) -> ...` — 為 logger 實例創建 FIGlet 藝術相關方法
- **function** `_lazy_pyfiglet()`
- **function** `_cached_figlet_format(text: ..., font: ...) -> ...`
- **function** `_require_pyfiglet(logger_instance: ...=...) -> ...`

### `pretty_loguru/formats/rich_components.py`
- **function** `print_renderable(renderable: ..., title: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 顯示任意 Rich renderable，並以「單 event」方式記錄到 console/file。
- **function** `print_table(title: ..., data: ..., headers: ...=..., show_header: ...=..., show_lines: ...=..., style: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 創建並顯示 Rich 表格，同時記錄到日誌
- **function** `print_tree(title: ..., tree_data: ..., style: ...=..., guide_style: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 創建並顯示 Rich 樹狀結構
- **function** `print_columns(title: ..., items: ..., padding: ...=..., width: ...=..., expand: ...=..., equal: ...=..., column_first: ...=..., right_to_left: ...=..., align: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 以分欄格式顯示項目列表
- **class** `LoggerProgress` — 與 logger 集成的進度條類
- **method** `LoggerProgress.__init__(self, logger_instance: ..., console: ...=..., log_start: ...=..., log_complete: ...=...)` — 建立與 logger 綁定的 progress helper。
- **method** `LoggerProgress.progress_context(self, description: ...=..., total: ...=...)` — 進度條上下文管理器
- **method** `LoggerProgress.track_list(self, items: ..., description: ...=...) -> ...` — 跟蹤列表處理進度
- **function** `print_code(code: ..., language: ...=..., theme: ...=..., line_numbers: ...=..., word_wrap: ...=..., indent_guides: ...=..., title: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 顯示語法高亮的程式碼
- **function** `print_code_from_file(file_path: ..., language: ...=..., theme: ...=..., line_numbers: ...=..., word_wrap: ...=..., indent_guides: ...=..., start_line: ...=..., end_line: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 從文件讀取並顯示語法高亮的程式碼
- **function** `print_diff(old_code: ..., new_code: ..., old_title: ...=..., new_title: ...=..., language: ...=..., theme: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 並排顯示程式碼差異對比，使用紅色（舊版本）和綠色（新版本）視覺區分
- **function** `print_panel(content: ..., title: ...=..., subtitle: ...=..., border_style: ...=..., box_style: ...=..., title_align: ...=..., subtitle_align: ...=..., width: ...=..., height: ...=..., padding: ...=..., expand: ...=..., level: ...=..., logger_instance: ...=..., console: ...=..., to_console_only: ...=..., to_file_only: ...=..., _target_depth: ...=...) -> ...` — 顯示 Rich Panel（面板），這是 block 方法的原生 Rich 版本
- **function** `create_rich_methods(logger_instance: ..., console: ...=...) -> ...` — 為 logger 實例創建 Rich 組件方法

### `pretty_loguru/integrations/__init__.py`
- **function** `has_uvicorn() -> ...` — 檢查 Uvicorn 整合是否可用
- **function** `has_fastapi() -> ...` — 檢查 FastAPI 整合是否可用

### `pretty_loguru/integrations/_errors.py`
- **function** `missing_dependency(dep_name: ..., *, extra: ...=...) -> ...` — 統一 integrations 的缺依賴錯誤訊息（避免 import-time warning）。

### `pretty_loguru/integrations/fastapi.py`
- **function** `_peek_request_body(request: ..., max_bytes: ...) -> ...` — 讀取最多 max_bytes 的 request body 預覽，並保留原始資料供後續處理。
- **class** `LoggingMiddleware(BaseHTTPMiddleware)` — FastAPI 日誌中間件，記錄請求和響應的詳細信息
- **method** `LoggingMiddleware.__init__(self, app: ..., logger_instance: ...=..., exclude_paths: ...=..., exclude_methods: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_headers: ...=..., sensitive_headers: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=...)` — 初始化日誌中間件
- **method** `LoggingMiddleware.dispatch(self, request: ..., call_next: ...) -> ...` — 處理請求和響應，記錄相關日誌
- **method** `LoggingMiddleware._sanitize_headers(self, headers: ...) -> ...` — 處理請求/響應頭，遮蔽敏感信息
- **class** `LoggingRoute(APIRoute)` — 帶有日誌功能的 FastAPI 路由
- **method** `LoggingRoute.__init__(self, *args: ..., logger_instance: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=..., **kwargs: ...)` — 建立帶有日誌功能的 route。
- **method** `LoggingRoute.get_route_handler(self) -> ...` — 回傳 FastAPI 用來處理 request 的 handler（帶有日誌紀錄）。
- **method** `LoggingRoute._receive_factory(body: ...)` — 創建一個能夠重複讀取請求體的函數
- **function** `get_logger_dependency(logger_instance: ...) -> ...` — 創建一個返回 logger 實例的依賴函數。
- **function** `install_fastapi_middleware(app: ..., *, logger_instance: ...=..., exclude_paths: ...=..., exclude_methods: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_headers: ...=..., sensitive_headers: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=...) -> ...` — 安裝 FastAPI LoggingMiddleware（較低階 building block）。
- **function** `install_fastapi_route_class(app: ..., *, logger_instance: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=...) -> ...` — 安裝 FastAPI LoggingRoute route_class（較低階 building block）。
- **function** `setup_fastapi_logging(app: ..., logger_instance: ...=..., middleware: ...=..., custom_routes: ...=..., exclude_paths: ...=..., exclude_methods: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_headers: ...=..., sensitive_headers: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=...) -> ...` — 為 FastAPI 應用設置日誌功能
- **function** `integrate_fastapi(app: ..., logger: ..., enable_uvicorn: ...=..., exclude_health_checks: ...=..., exclude_paths: ...=..., exclude_methods: ...=..., middleware: ...=..., custom_routes: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_headers: ...=..., sensitive_headers: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=...) -> ...` — 將 FastAPI 應用與 Pretty Loguru logger 進行完整集成
- **function** `build_fastapi_logging_options(logger_instance: ...=..., *, exclude_paths: ...=..., exclude_methods: ...=..., log_request_body: ...=..., log_response_body: ...=..., log_headers: ...=..., sensitive_headers: ...=..., log_request_body_if_unknown_length: ...=..., max_body_bytes: ...=...) -> ...` — 提供 FastAPI 日誌中間件與 route_class 的「非直接安裝」選項。
- **function** `restore_fastapi_logging(app: ...) -> ...` — 嘗試還原 integrate_fastapi/setup_fastapi_logging 對 app 的變更。
- **function** `_require_fastapi() -> ...` — 當 `fastapi` 未安裝時，統一拋出缺少依賴的錯誤。
- **function** `setup_fastapi_logging(*args: ..., **kwargs: ...) -> ...` — `setup_fastapi_logging` 的 stub（缺少 `fastapi` 時會拋錯）。
- **function** `integrate_fastapi(*args: ..., **kwargs: ...) -> ...` — `integrate_fastapi` 的 stub（缺少 `fastapi` 時會拋錯）。
- **function** `get_logger_dependency(*args: ..., **kwargs: ...) -> ...` — `get_logger_dependency` 的 stub（缺少 `fastapi` 時會拋錯）。
- **function** `install_fastapi_middleware(*args: ..., **kwargs: ...) -> ...` — `install_fastapi_middleware` 的 stub（缺少 `fastapi` 時會拋錯）。
- **function** `install_fastapi_route_class(*args: ..., **kwargs: ...) -> ...` — `install_fastapi_route_class` 的 stub（缺少 `fastapi` 時會拋錯）。
- **function** `build_fastapi_logging_options(*args: ..., **kwargs: ...) -> ...` — `build_fastapi_logging_options` 的 stub（缺少 `fastapi` 時會拋錯）。
- **class** `LoggingMiddleware` — `LoggingMiddleware` 的 stub（缺少 `fastapi` 時會拋錯）。
- **method** `LoggingMiddleware.__init__(self, *args: ..., **kwargs: ...) -> ...` — 建立 stub；任何呼叫都會拋出缺少依賴錯誤。
- **class** `LoggingRoute` — `LoggingRoute` 的 stub（缺少 `fastapi` 時會拋錯）。
- **method** `LoggingRoute.__init__(self, *args: ..., **kwargs: ...) -> ...` — 建立 stub；任何呼叫都會拋出缺少依賴錯誤。

### `pretty_loguru/integrations/loki.py`
- **function** `_normalize_loki_push_url(url: ...) -> ...` — 將 base URL 正規化成 Loki push endpoint（`/loki/api/v1/push`）。
- **class** `LokiSinkConfig` — Loki sink 設定（直推 / best-effort）。
- **class** `LokiSink` — Loguru sink：將 log line 推送到 Loki。
- **method** `LokiSink.__init__(self, config: ...) -> ...` — 建立 Loki sink。
- **method** `LokiSink.__call__(self, message: ...) -> ...` — Loguru sink entrypoint：接收一筆 message 並加入緩衝，必要時觸發 flush。
- **method** `LokiSink.flush(self) -> ...` — 立即送出目前緩衝的 log lines。
- **method** `LokiSink.close(self) -> ...` — 關閉 sink 並嘗試做最後一次 flush。
- **function** `create_loki_sink(url: ..., labels: ...=..., batch_size: ...=..., flush_interval_seconds: ...=..., timeout_seconds: ...=..., tenant_id: ...=..., username: ...=..., password: ...=..., headers: ...=...) -> ...` — 建立可直接傳給 `logger.add(...)` 的 Loki sink。

### `pretty_loguru/integrations/uvicorn.py`
- **class** `InterceptHandler(logging.Handler)` — 攔截標準日誌庫的日誌並轉發給 Loguru
- **method** `InterceptHandler.__init__(self, logger_instance: ...=...)` — 初始化攔截處理器
- **method** `InterceptHandler.emit(self, record: ...) -> ...` — 處理日誌記錄，將其轉發給 Loguru。
- **function** `build_uvicorn_log_config(logger_instance: ...=..., log_level: ...=..., logger_names: ...=...) -> ...` — 建立可直接傳入 `uvicorn.run(..., log_config=...)` 的 logging config dict（non-monkeypatch）。
- **function** `_configure_uvicorn_logging(logger_instance: ...=..., log_level: ...=..., logger_names: ...=...) -> ...` — 配置 Uvicorn 日誌以使用 Loguru 格式化輸出
- **function** `setup_uvicorn_logging(logger_instance: ...=..., log_level: ...=...)` — 在 uvicorn.run 之前調用此函數來設置日誌攔截（monkeypatch）。
- **function** `integrate_uvicorn(logger: ...=..., log_level: ...=..., logger_names: ...=..., *, monkeypatch: ...=..., snapshot_all_loggers: ...=...) -> ...` — 將 Uvicorn 與 Pretty Loguru logger 進行集成
- **function** `restore_uvicorn_logging() -> ...` — 還原被 monkeypatch 的 uvicorn logging 行為（若曾呼叫 integrate_uvicorn(monkeypatch=True)）。

### `pretty_loguru/types/protocols.py`
- **class** `PrettyLoggerProtocol(Protocol)` — 簡化的 Pretty Logger 協議
- **method** `PrettyLoggerProtocol.debug(self, message: ..., *args: ..., **kwargs: ...) -> ...` — 記錄 `DEBUG` 級別訊息（對齊 `loguru.logger.debug`）。
- **method** `PrettyLoggerProtocol.info(self, message: ..., *args: ..., **kwargs: ...) -> ...` — 記錄 `INFO` 級別訊息（對齊 `loguru.logger.info`）。
- **method** `PrettyLoggerProtocol.success(self, message: ..., *args: ..., **kwargs: ...) -> ...` — 記錄 `SUCCESS` 級別訊息（對齊 `loguru.logger.success`）。
- **method** `PrettyLoggerProtocol.warning(self, message: ..., *args: ..., **kwargs: ...) -> ...` — 記錄 `WARNING` 級別訊息（對齊 `loguru.logger.warning`）。
- **method** `PrettyLoggerProtocol.error(self, message: ..., *args: ..., **kwargs: ...) -> ...` — 記錄 `ERROR` 級別訊息（對齊 `loguru.logger.error`）。
- **method** `PrettyLoggerProtocol.critical(self, message: ..., *args: ..., **kwargs: ...) -> ...` — 記錄 `CRITICAL` 級別訊息（對齊 `loguru.logger.critical`）。
- **method** `PrettyLoggerProtocol.block(self, title: ..., lines: ..., **kwargs: ...) -> ...` — 以 Rich Panel 印出區塊（console/file 語意一致）。
- **method** `PrettyLoggerProtocol.ascii_header(self, text: ..., **kwargs: ...) -> ...` — 印出 ASCII Art 標題（需要 `art`）。
- **method** `PrettyLoggerProtocol.ascii_block(self, title: ..., lines: ..., **kwargs: ...) -> ...` — 印出 ASCII Art 區塊（需要 `art`）。
- **method** `PrettyLoggerProtocol.figlet_header(self, text: ..., **kwargs: ...) -> ...` — 印出 FIGlet 標題（需要 `pyfiglet`）。
- **method** `PrettyLoggerProtocol.figlet_block(self, title: ..., lines: ..., **kwargs: ...) -> ...` — 印出 FIGlet 區塊（需要 `pyfiglet`）。
- **method** `PrettyLoggerProtocol.table(self, title: ..., data: ..., headers: ...=..., show_header: ...=..., show_lines: ...=..., style: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 以 Rich Table 顯示結構化資料。
- **method** `PrettyLoggerProtocol.tree(self, title: ..., tree_data: ..., style: ...=..., guide_style: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 以 Rich Tree 顯示樹狀結構資料。
- **method** `PrettyLoggerProtocol.columns(self, title: ..., items: ..., padding: ...=..., width: ...=..., expand: ...=..., equal: ...=..., column_first: ...=..., right_to_left: ...=..., align: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 以 Rich Columns 以多欄方式排列字串項目。
- **method** `PrettyLoggerProtocol.code(self, code: ..., language: ...=..., theme: ...=..., line_numbers: ...=..., word_wrap: ...=..., indent_guides: ...=..., title: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 以 Rich Syntax 顯示程式碼區塊（語法高亮）。
- **method** `PrettyLoggerProtocol.code_file(self, file_path: ..., language: ...=..., theme: ...=..., line_numbers: ...=..., word_wrap: ...=..., indent_guides: ...=..., start_line: ...=..., end_line: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 讀取檔案並以 Rich Syntax 顯示（支援行號/範圍）。
- **method** `PrettyLoggerProtocol.diff(self, old_code: ..., new_code: ..., old_title: ...=..., new_title: ...=..., language: ...=..., theme: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 以 side-by-side 的方式顯示程式碼差異（舊/新）。
- **method** `PrettyLoggerProtocol.panel(self, content: ..., title: ...=..., subtitle: ...=..., border_style: ...=..., box_style: ...=..., title_align: ...=..., subtitle_align: ...=..., width: ...=..., height: ...=..., padding: ...=..., expand: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 以 Rich Panel 顯示文字或任意可渲染物件。
- **method** `PrettyLoggerProtocol.render(self, renderable: ..., title: ...=..., level: ...=..., to_console_only: ...=..., to_file_only: ...=...) -> ...` — 直接渲染任意 Rich renderable（並保證 file/console 語意一致）。
- **method** `PrettyLoggerProtocol.bind(self, **kwargs: ...) -> ...` — 回傳帶有額外 `record['extra']` 的 logger（對齊 `loguru.logger.bind`）。
- **method** `PrettyLoggerProtocol.opt(self, **kwargs: ...) -> ...` — 調整 event 參數（depth/colors/capture...；對齊 `loguru.logger.opt`）。
- **method** `PrettyLoggerProtocol.add(self, sink: ..., **kwargs: ...) -> ...` — 新增 sink（file/stdout/自定義 callable；對齊 `loguru.logger.add`）。
- **method** `PrettyLoggerProtocol.remove(self, handler_id: ...=...) -> ...` — 移除 sink（對齊 `loguru.logger.remove`）。

### `pretty_loguru/utils/dependencies.py`
- **function** `art()` — 延遲導入 art（方便測試 patch 與避免硬依賴）
- **function** `pyfiglet()` — 延遲導入 pyfiglet（方便測試 patch 與避免硬依賴）
- **function** `ensure_art_dependency(logger_instance: ...=...) -> ...` — 確保 art 庫已安裝
- **function** `ensure_pyfiglet_dependency(logger_instance: ...=...) -> ...` — 確保 pyfiglet 庫已安裝
- **function** `check_art_availability() -> ...` — 檢查 art 庫是否可用
- **function** `check_pyfiglet_availability() -> ...` — 檢查 pyfiglet 庫是否可用
- **function** `warn_missing_dependency(dependency_name: ..., logger_instance: ...=..., return_value: ...=...) -> ...` — 對缺失的依賴發出警告
- **function** `has_art() -> ...` — 返回 art 庫是否可用
- **function** `has_pyfiglet() -> ...` — 返回 pyfiglet 庫是否可用

### `pretty_loguru/utils/validators.py`
- **function** `is_ascii_only(text: ...) -> ...` — 檢查文本是否只包含 ASCII 字符
- **function** `validate_ascii_text(text: ..., text_type: ...=..., logger_instance: ...=...) -> ...` — 驗證並清理 ASCII 文本
- **function** `validate_ascii_header(header_text: ..., logger_instance: ...=...) -> ...` — 專門用於驗證 ASCII 標題文本的便捷函數
- **function** `validate_ascii_art_text(art_text: ..., logger_instance: ...=...) -> ...` — 專門用於驗證 ASCII 藝術文本的便捷函數

### `pretty_loguru/utils/warn_once.py`
- **function** `warn_once(message: ..., category: ...=..., *, key: ...=...) -> ...` — 發出一次性的警告，同一 key 僅警告一次。

### `snapshot.py`
- **class** `SymbolSnapshot` — 單一 Python 符號快照（class/function/method 或 error）。
- **class** `FileSnapshot` — 單一檔案的符號清單快照。
- **class** `ProjectDeps` — 單一依賴清單檔案（pyproject/requirements...）解析結果。
- **class** `Config` — Snapshot 工具設定。
- **class** `_GitIgnoreRule` — 一條 .gitignore 規則（簡化實作）。
- **class** `GitIgnore` — 讀取並套用 .gitignore 規則。
- **method** `GitIgnore.__init__(self, root: ..., *, follow_symlinks: ...) -> ...` — 建立 .gitignore 規則集合（需呼叫 `load()` 才會讀取檔案）。
- **method** `GitIgnore.load(self) -> ...` — 走訪專案並讀取所有 `.gitignore`，建構規則清單。
- **method** `GitIgnore.is_ignored(self, path: ...) -> ...` — 判斷給定路徑是否被 .gitignore 規則排除。
- **method** `GitIgnore._iter_gitignore_files(self) -> ...` — 列出專案內所有 `.gitignore` 檔案（依 os.walk 掃描）。
- **method** `GitIgnore._parse_gitignore_file(self, path: ..., *, base_dir: ...) -> ...` — 解析單一 `.gitignore` 檔案為規則清單。
- **method** `GitIgnore._rule_matches(self, rule: ..., rel_posix: ...) -> ...` — 判斷某條規則是否命中 `rel_posix`（posix 相對路徑）。
- **method** `GitIgnore._to_posix_rel(self, path: ...) -> ...` — 將任意路徑轉換為相對於 root 的 posix path（用於比對）。
- **class** `ProjectScanner` — 專案掃描器：負責
- **method** `ProjectScanner.__init__(self, config: ...) -> ...` — 建立掃描器並初始化排除規則（含 .gitignore）。
- **method** `ProjectScanner.iter_included_files(self) -> ...` — 走訪 root 並回傳「未被排除」的檔案路徑。
- **method** `ProjectScanner.iter_python_files(self) -> ...` — 列出要進行 AST 解析的 Python 檔案（依 `target_exts`）。
- **method** `ProjectScanner.iter_dependency_manifests(self) -> ...` — 列出依賴檔案（pyproject/requirements...）供後續解析。
- **method** `ProjectScanner.build_tree(self) -> ...` — 產出專案目錄樹（ASCII tree）。
- **method** `ProjectScanner._build_tree_lines(self, dir_path: ..., *, prefix: ..., depth: ...) -> ...` — 遞迴生成目錄樹的每一行（內部用）。
- **method** `ProjectScanner._is_excluded(self, path: ..., *, is_dir: ...) -> ...` — 判斷路徑是否應被排除（.gitignore + excludes）。
- **class** `CodeAnalyzer(ast.NodeVisitor)` — Python AST 分析器：蒐集 function/class/method（含巢狀）。
- **method** `CodeAnalyzer.__init__(self, *, include_private: ..., include_nested: ...) -> ...` — 建立 AST analyzer。
- **method** `CodeAnalyzer.visit_ClassDef(self, node: ...) -> ...` — 拜訪 class 節點並記錄 SymbolSnapshot（符合篩選條件時）。
- **method** `CodeAnalyzer.visit_FunctionDef(self, node: ...) -> ...` — 拜訪同步 function 節點。
- **method** `CodeAnalyzer.visit_AsyncFunctionDef(self, node: ...) -> ...` — 拜訪 async function 節點。
- **method** `CodeAnalyzer._handle_function_like(self, node: ...) -> ...` — 處理 function/method 節點並記錄 SymbolSnapshot（符合篩選條件時）。
- **method** `CodeAnalyzer._should_keep(self, name: ...) -> ...` — 依 include_private 設定決定是否保留該 symbol。
- **method** `CodeAnalyzer._in_function_scope(self) -> ...` — 是否目前位於 function scope（用於判斷 nested）。
- **method** `CodeAnalyzer._qualified(self, name: ...) -> ...` — 產生 qualified name（依目前 scope 堆疊）。
- **method** `CodeAnalyzer._format_class_signature(self, node: ...) -> ...` — 輸出 class bases 的簡化表示（避免噴出完整 AST）。
- **method** `CodeAnalyzer._format_function_signature(self, node: ...) -> ...` — 輸出 function signature 的簡化表示（以 `...` 取代型別/預設值）。
- **function** `_first_doc_line(doc: ...) -> ...` — 取 docstring 的第一行（用於 snapshot.md 摘要）。
- **function** `_safe_expr_placeholder(expr: ...) -> ...` — 將 AST 表達式轉成可讀的簡化佔位字串（失敗則回傳 `...`）。
- **class** `PythonFileParser` — 解析單一 Python 檔案並產生 `FileSnapshot`（AST symbols）。
- **method** `PythonFileParser.__init__(self, config: ...) -> ...` — 建立 parser。
- **method** `PythonFileParser.parse(self, path: ...) -> ...` — 解析指定 Python 檔案（包含容錯讀檔/容錯解析）。
- **class** `DependencyParser` — 解析依賴清單檔案（pyproject/Pipfile/requirements）。
- **method** `DependencyParser.parse_manifest(self, path: ..., *, root: ...) -> ...` — 解析單一 manifest 檔案並回傳 `ProjectDeps`（無法解析則回傳 None）。
- **method** `DependencyParser._parse_requirements(self, text: ...) -> ...` — 解析 requirements.txt 形式的依賴清單。
- **method** `DependencyParser._parse_pyproject(self, text: ..., *, fallback_name: ...) -> ...` — 解析 pyproject.toml（優先用 tomllib，失敗則用弱解析）。
- **method** `DependencyParser._parse_pipfile_section(self, text: ..., *, section: ...) -> ...` — 解析 Pipfile 的指定 section（packages / dev-packages）。
- **function** `_split_dep_name_spec(entry: ...) -> ...` — 將依賴項目字串切成（name, spec）兩段（spec 可為空）。
- **function** `_parse_pyproject_from_toml_dict(data: ..., *, fallback_name: ...) -> ...` — 從 `tomllib.loads()` 的結果中萃取 dependencies / dev deps / project name。
- **function** `_weak_extract_toml_table(text: ..., table: ...) -> ...` — 弱解析：擷取 `[table]` 區塊（不完整 TOML 支援，但夠用）。
- **function** `_weak_toml_get_scalar(text: ..., table: ..., key: ...) -> ...` — 弱解析：從 `[table]` 中抓取 scalar 值（字串/數字都以字串回傳）。
- **function** `_weak_toml_get_array(text: ..., table: ..., key: ...) -> ...` — 弱解析：從 `[table]` 中抓取 string array（`key = ['a','b']`）。
- **function** `_weak_toml_get_table_of_arrays(text: ..., table: ...) -> ...` — 弱解析：從 `[table]` 中抓取 `key = [..]` 的 table-of-arrays。
- **class** `ReportGenerator` — 將掃描結果轉成 Markdown 報告。
- **method** `ReportGenerator.to_markdown(self, *, config: ..., tree: ..., file_snaps: ..., deps: ...) -> ...` — 產出 snapshot.md 內容。
- **function** `_to_pretty_json_block(d: ...) -> ...` — 將 dict 依賴清單輸出成 Markdown code block。
- **function** `_select_dependency_manifests(manifests: ...) -> ...` — 將同一個資料夾內「多個依賴描述檔」去重，只保留一份最具代表性的來源。
- **function** `_build_arg_parser() -> ...` — 建立 snapshot CLI 的 argument parser。
- **function** `main(argv: ...) -> ...` — CLI entrypoint：產生 `snapshot.md` 並寫入檔案。

## 依賴清單
### pretty-loguru
- Path: `.`
- Source: `pyproject.toml`

#### devDependencies
```json
{
    "httpx": ">=0.24.0",
    "pytest": ">=7.0.0",
    "pytest-asyncio": ">=0.23.0"
}
```

#### dependencies
```json
{
    "art": ">=5.0.0",
    "fastapi": ">=0.100.0",
    "loguru": ">=0.6.0",
    "psutil": ">=5.9.0",
    "rich": ">=12.0.0",
    "uvicorn": ">=0.20.0"
}
```
