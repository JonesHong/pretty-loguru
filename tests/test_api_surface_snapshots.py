from __future__ import annotations


def test_prettyloggerprotocol_method_names_snapshot():
    from pretty_loguru.types.protocols import PrettyLoggerProtocol

    methods = sorted(
        name
        for name, value in PrettyLoggerProtocol.__dict__.items()
        if callable(value) and not name.startswith("_")
    )
    expected = [
        "add",
        "ascii_block",
        "ascii_header",
        "bind",
        "block",
        "code",
        "code_file",
        "columns",
        "critical",
        "debug",
        "diff",
        "error",
        "figlet_block",
        "figlet_header",
        "info",
        "opt",
        "panel",
        "remove",
        "render",
        "success",
        "table",
        "tree",
        "warning",
    ]
    assert methods == expected

    annotations = getattr(PrettyLoggerProtocol, "__annotations__", {})
    assert sorted(annotations.keys()) == ["progress"]


def test_addons_public_exports_snapshot():
    from pretty_loguru import addons
    from pretty_loguru.formats import has_figlet

    expected = [
        "ConfigTemplates",
        "LoggerProgress",
        "PresetFactory",
        "PresetType",
        "config_from_preset",
        "config_from_template",
        "create_config",
        "log_to_targets",
        "mark_file_handler",
        "print_ascii_block",
        "print_ascii_header",
        "print_block",
        "print_columns",
        "print_table",
        "print_tree",
    ]

    if has_figlet():
        expected.extend(["get_figlet_fonts", "print_figlet_block", "print_figlet_header"])

    assert sorted(addons.__all__) == sorted(expected)
