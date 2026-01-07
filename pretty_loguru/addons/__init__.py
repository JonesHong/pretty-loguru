"""
addons 模組入口（加值功能）

此模組聚合 Pretty Loguru 的「加值能力」：
- 視覺化輸出（Rich/ASCII/FIGlet）
- targets（console/file 導向輸出）
- templates/presets（配置模板與預設策略）
- advanced（底層直接存取）

注意：core 合約只保證 `pretty_loguru` 頂層匯出的 API；addons 屬於可演進範圍。
"""

from __future__ import annotations

from ..core.presets import PresetType, PresetFactory
from ..core.templates import (
    ConfigTemplates,
    create_config,
    config_from_template,
    config_from_preset,
)
from ..core.target_formatter import (
    log_to_targets,
    mark_file_handler,
)

from ..formats.block import print_block
from ..formats.ascii_art import print_ascii_header, print_ascii_block
from ..formats.rich_components import print_table, print_tree, print_columns, LoggerProgress

from ..formats import has_figlet

if has_figlet():
    from ..formats import print_figlet_header, print_figlet_block, get_figlet_fonts

__all__ = [
    "PresetType",
    "PresetFactory",
    "ConfigTemplates",
    "create_config",
    "config_from_template",
    "config_from_preset",
    "log_to_targets",
    "mark_file_handler",
    "print_block",
    "print_ascii_header",
    "print_ascii_block",
    "print_table",
    "print_tree",
    "print_columns",
    "LoggerProgress",
]

if has_figlet():
    __all__.extend(["print_figlet_header", "print_figlet_block", "get_figlet_fonts"])
