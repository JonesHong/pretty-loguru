from __future__ import annotations


def test_create_logger_does_not_remove_user_configured_loguru_sinks(tmp_path):
    import os
    import subprocess
    import sys

    log_file = tmp_path / "loguru_user_sink.log"
    env = os.environ.copy()
    env["PRETTY_LOGURU_TEST_LOGURU_SINK_FILE"] = str(log_file)

    code = (
        "import os\n"
        "from loguru import logger\n"
        "from pretty_loguru import create_logger\n"
        "logger.add(os.environ['PRETTY_LOGURU_TEST_LOGURU_SINK_FILE'], format='{message}')\n"
        "create_logger('pl_base_prepare')\n"
        "logger.info('HELLO_FROM_LOGURU')\n"
    )
    subprocess.run([sys.executable, "-c", code], check=True, env=env)

    assert log_file.exists()
    assert "HELLO_FROM_LOGURU" in log_file.read_text(encoding='utf-8')


def test_log_to_targets_both_does_not_duplicate_file_output(tmp_path):
    from pretty_loguru import create_logger
    from pretty_loguru.addons import log_to_targets

    log_dir = tmp_path / "logs"
    logger = create_logger("targets_dedup", log_dir=str(log_dir))

    log_to_targets(logger, "HELLO_BOTH", level="INFO")
    logger.complete()

    files = list(log_dir.glob("*.log"))
    assert files, "Expected a .log file to be created"
    text = files[0].read_text(encoding="utf-8")
    assert text.count("HELLO_BOTH") == 1


def test_pretty_block_emits_single_event():
    from pretty_loguru import create_logger

    logger = create_logger("pretty_event_block")
    events: list[dict] = []

    handler_id = logger.add(
        lambda msg: events.append(msg.record),
        level="INFO",
        filter=lambda r: r["extra"].get("logger_id") == "pretty_event_block",
    )

    logger.block("TITLE", ["line1", "line2"])
    logger.remove(handler_id)

    pretty_events = [e for e in events if e["extra"].get("pretty_kind") == "block"]
    assert len(pretty_events) == 1

    event = pretty_events[0]
    assert isinstance(event["extra"].get("pretty_payload"), dict)
    assert event["extra"]["pretty_payload"]["title"] == "TITLE"
    assert event["extra"].get("pretty_text"), "expected pretty_text to be generated"


def test_pretty_table_emits_single_event():
    from pretty_loguru import create_logger

    logger = create_logger("pretty_event_table")
    events: list[dict] = []

    handler_id = logger.add(
        lambda msg: events.append(msg.record),
        level="INFO",
        filter=lambda r: r["extra"].get("logger_id") == "pretty_event_table",
    )

    logger.table("USERS", [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
    logger.remove(handler_id)

    pretty_events = [e for e in events if e["extra"].get("pretty_kind") == "table"]
    assert len(pretty_events) == 1

    event = pretty_events[0]
    assert isinstance(event["extra"].get("pretty_payload"), dict)
    assert event["extra"]["pretty_payload"]["title"] == "USERS"
    assert event["extra"].get("pretty_text"), "expected pretty_text to be generated"


def test_pretty_event_appends_pretty_text_to_file(tmp_path):
    from pretty_loguru import create_logger

    log_dir = tmp_path / "pretty"
    logger = create_logger("pretty_file_event", log_dir=str(log_dir))

    logger.block("FILE_TITLE", ["file_line1", "file_line2"])
    logger.complete()

    files = list(log_dir.glob("*.log"))
    assert files, "Expected a .log file to be created"

    text = files[0].read_text(encoding="utf-8")
    assert "CustomBlock: FILE_TITLE" in text
    assert "file_line1" in text
    assert "file_line2" in text


def test_reinit_preserves_user_added_handlers(tmp_path):
    from pretty_loguru import create_logger, reinit_logger

    logger = create_logger("contract_preserve", log_dir=str(tmp_path / "logs"))

    user_events: list[str] = []
    user_handler_id = logger.add(lambda msg: user_events.append(str(msg)), level="INFO")
    assert user_handler_id in logger._core.handlers

    reinit_logger("contract_preserve", level="DEBUG")
    assert user_handler_id in logger._core.handlers


def test_loggerconfig_update_preserves_user_added_handlers(tmp_path):
    from pretty_loguru import LoggerConfig, create_logger

    config = LoggerConfig(level="INFO", log_dir=str(tmp_path / "cfg"))
    logger = create_logger("contract_cfg", config=config)
    config.apply_to("contract_cfg")

    user_events: list[str] = []
    user_handler_id = logger.add(lambda msg: user_events.append(str(msg)), level="INFO")
    assert user_handler_id in logger._core.handlers

    config.update(level="DEBUG")
    assert user_handler_id in logger._core.handlers


def test_log_dir_must_be_directory(tmp_path):
    from pretty_loguru import LoggerConfig

    bad_path = str(tmp_path / "app.log")
    config = LoggerConfig(log_dir=bad_path)
    try:
        config.validate()
    except ValueError as e:
        assert "log_dir must be a directory" in str(e)
    else:
        raise AssertionError("Expected ValueError for file-like log_dir")


def test_handlers_are_scoped_by_logger_id(tmp_path):
    from pretty_loguru import create_logger

    logger_a = create_logger("scope_a", log_dir=str(tmp_path / "a"))
    logger_b = create_logger("scope_b", log_dir=str(tmp_path / "b"))

    ids_a = getattr(logger_a, "_pretty_loguru_managed_handler_ids", [])
    ids_b = getattr(logger_b, "_pretty_loguru_managed_handler_ids", [])
    assert ids_a and ids_b

    handler_a = logger_a._core.handlers[ids_a[0]]
    handler_b = logger_b._core.handlers[ids_b[0]]

    record_a = {"extra": {"logger_id": "scope_a"}}
    record_b = {"extra": {"logger_id": "scope_b"}}

    assert handler_a._filter(record_a) is True
    assert handler_a._filter(record_b) is False
    assert handler_b._filter(record_b) is True
    assert handler_b._filter(record_a) is False


def test_reinit_reset_handlers_removes_user_added_handlers(tmp_path):
    from pretty_loguru import create_logger, reinit_logger

    logger = create_logger("reset_handlers", log_dir=str(tmp_path / "logs"))
    user_handler_id = logger.add(lambda msg: None, level="INFO")
    assert user_handler_id in logger._core.handlers

    reinit_logger("reset_handlers", reset_handlers=True)
    assert user_handler_id not in logger._core.handlers


def test_loggerconfig_apply_to_can_create_missing(tmp_path):
    from pretty_loguru import LoggerConfig, get_logger

    config = LoggerConfig(level="INFO", log_dir=str(tmp_path / "logs"))
    logger = config.apply_to("apply_create")
    assert logger is not None
    assert get_logger("apply_create") is logger


def test_loggerconfig_detach_stops_auto_updates(tmp_path):
    from pretty_loguru import LoggerConfig, create_logger

    config = LoggerConfig(level="INFO", log_dir=str(tmp_path / "logs"))
    logger = create_logger("detach_logger", config=config)
    config.apply_to("detach_logger")

    assert getattr(logger, "_pretty_loguru_config").level == "INFO"
    config.update(level="DEBUG")
    assert getattr(logger, "_pretty_loguru_config").level == "DEBUG"

    config.detach("detach_logger")
    config.update(level="ERROR")
    assert getattr(logger, "_pretty_loguru_config").level == "DEBUG"
