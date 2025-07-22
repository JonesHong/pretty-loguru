# Changelog

All notable changes to this project will be documented in this file.

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