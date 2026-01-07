from __future__ import annotations


def test_bind_preserves_user_extra_and_protects_reserved_keys(tmp_path):
    from pretty_loguru import create_logger

    logger = create_logger("bindopt", log_dir=str(tmp_path / "logs"), level="DEBUG")

    records: list[dict] = []

    def sink(message):
        records.append(message.record)

    handler_id = logger.add(
        sink,
        level="DEBUG",
        filter=lambda record: record["extra"].get("logger_id") == "bindopt",
    )
    try:
        logger.bind(user_id="u1").info("hello")
        logger.bind(logger_id="evil").info("should not override")
    finally:
        logger.remove(handler_id)

    assert len(records) == 2
    assert records[0]["extra"]["user_id"] == "u1"
    assert records[0]["extra"]["logger_id"] == "bindopt"
    assert records[1]["extra"]["logger_id"] == "bindopt"


def test_opt_lazy_semantics_are_not_broken(tmp_path):
    from pretty_loguru import create_logger

    logger = create_logger("lazyopt", log_dir=str(tmp_path / "logs"), level="DEBUG")

    records: list[dict] = []

    def sink(message):
        records.append(message.record)

    handler_id = logger.add(
        sink,
        level="DEBUG",
        filter=lambda record: record["extra"].get("logger_id") == "lazyopt",
    )
    try:
        logger.opt(lazy=True).debug("{}", lambda: "computed")
    finally:
        logger.remove(handler_id)

    assert len(records) == 1
    assert records[0]["message"] == "computed"


def test_serialize_writes_json_lines(tmp_path):
    import json

    from pretty_loguru import create_logger

    log_dir = tmp_path / "logs"
    logger = create_logger("serialize", log_dir=str(log_dir), level="INFO", serialize=True)
    logger.info("serialized-message")

    log_files = list(log_dir.glob("*.log"))
    assert log_files, "Expected at least one .log file to be created"

    payload = json.loads(log_files[0].read_text(encoding="utf-8").splitlines()[0])
    assert payload["record"]["message"] == "serialized-message"
