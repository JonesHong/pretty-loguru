from __future__ import annotations


def test_enable_addons_true_injects_rich_and_art_methods(tmp_path):
    from pretty_loguru import create_logger
    from pretty_loguru.formats import has_figlet

    logger = create_logger("addons_on", log_dir=str(tmp_path / "logs"), enable_addons=True)

    for name in (
        "block",
        "ascii_header",
        "ascii_block",
        "table",
        "tree",
        "columns",
        "code",
        "code_file",
        "diff",
        "panel",
        "progress",
    ):
        assert hasattr(logger, name), f"Expected logger to have injected method/attr: {name}"

    if has_figlet():
        assert hasattr(logger, "figlet_header")
        assert hasattr(logger, "figlet_block")


def test_enable_addons_false_does_not_inject_formats(tmp_path):
    from pretty_loguru import create_logger

    logger = create_logger("addons_off", log_dir=str(tmp_path / "logs"), enable_addons=False)

    for name in (
        "block",
        "ascii_header",
        "ascii_block",
        "table",
        "tree",
        "columns",
        "code",
        "code_file",
        "diff",
        "panel",
        "progress",
        "figlet_header",
        "figlet_block",
    ):
        assert not hasattr(logger, name), f"Did not expect logger to have injected method/attr: {name}"

