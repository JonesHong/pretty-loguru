# Changelog

本檔案以「使用者行為」為主紀錄變更；內部重構若不影響使用者，請避免寫成主要條目。
發版規則見 `RELEASE_STRATEGY.md`。

## [Unreleased]

### Breaking
- `pretty_loguru` 頂層改為只匯出 core API；addons/integrations 改為顯式 import（`pretty_loguru.addons` / `pretty_loguru.integrations`）
- `log_dir` 改為「必須是目錄」，檔案路徑（例如 `app.log`）會直接丟錯（見 `MIGRATION_1_TO_2.md`）

### Fixed
- `reinit_logger()`/`LoggerConfig.update()` 不再清除使用者自行 `logger.add()` 的 sinks（除非顯式 `reset_handlers=True`）

## [1.1.3] - 2025-07-22

### Fixed
- Fixed dynamic config update not working properly - `config.update()` now correctly updates all attached loggers without creating new instances
- Added missing `use_proxy` attribute to `LoggerConfig` class
- Fixed import path for `_update_attached_loggers` method

### Added
- New `updater.py` module with proper logger update functionality
- `update_logger_config()` function for updating existing logger instances

### Changed
- Modified `_update_attached_loggers` to update existing loggers instead of creating new instances
- Improved logger name handling during config updates

## [1.1.2] - Previous version
- Previous release details...
