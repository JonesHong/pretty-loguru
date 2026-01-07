from __future__ import annotations


def test_destination_filters_respect_target_flags():
    from pretty_loguru.core.handlers import create_destination_filters

    filters = create_destination_filters()
    console_filter = filters["console"]
    file_filter = filters["file"]

    assert console_filter({"extra": {}}) is True
    assert console_filter({"extra": {"to_file_only": True}}) is False
    assert console_filter({"extra": {"to_file_only": False}}) is True

    assert file_filter({"extra": {}}) is True
    assert file_filter({"extra": {"to_console_only": True}}) is False
    assert file_filter({"extra": {"to_console_only": False}}) is True

