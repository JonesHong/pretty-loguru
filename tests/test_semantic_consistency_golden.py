from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor


def _scoped_destination_filter(logger_id: str, destination: str):
    from pretty_loguru.core.handlers import create_destination_filters

    base = create_destination_filters()[destination]

    def _filter(record):
        return record["extra"].get("logger_id") == logger_id and base(record)

    return _filter


def test_golden_pretty_event_payload_is_visible_to_console_and_file(tmp_path):
    from pretty_loguru import create_logger
    from pretty_loguru.core.pretty_event import build_renderable, validate_pretty_payload

    logger_id = "golden_payload"
    logger = create_logger(logger_id, log_dir=str(tmp_path / "logs"), level="WARNING")

    console_records: list[dict] = []
    file_records: list[dict] = []
    lock = threading.Lock()

    def capture_console(msg):
        with lock:
            console_records.append(msg.record)

    def capture_file(msg):
        with lock:
            file_records.append(msg.record)

    console_handler_id = logger.add(
        capture_console,
        level="INFO",
        filter=_scoped_destination_filter(logger_id, "console"),
    )
    file_handler_id = logger.add(
        capture_file,
        level="INFO",
        filter=_scoped_destination_filter(logger_id, "file"),
    )
    try:
        logger.block("TITLE", ["line1", "line2"])
    finally:
        logger.remove(console_handler_id)
        logger.remove(file_handler_id)

    assert len(console_records) == 1
    assert len(file_records) == 1

    a = console_records[0]["extra"]
    b = file_records[0]["extra"]

    assert a["pretty_kind"] == "block"
    assert a["pretty_kind"] == b["pretty_kind"]
    assert a["pretty_payload"] == b["pretty_payload"]
    assert isinstance(a["pretty_payload"], dict)
    assert isinstance(a["pretty_text"], str) and a["pretty_text"].strip()

    validate_pretty_payload(a["pretty_kind"], a["pretty_payload"])
    renderable = build_renderable(a["pretty_kind"], a["pretty_payload"])
    assert renderable is not None

    json.dumps(a["pretty_payload"], ensure_ascii=False)


def test_golden_pretty_event_respects_to_console_only_and_to_file_only(tmp_path):
    from pretty_loguru import create_logger

    logger_id = "golden_targets"
    logger = create_logger(logger_id, log_dir=str(tmp_path / "logs"), level="WARNING")

    console_records: list[dict] = []
    file_records: list[dict] = []
    lock = threading.Lock()

    def capture_console(msg):
        with lock:
            console_records.append(msg.record)

    def capture_file(msg):
        with lock:
            file_records.append(msg.record)

    console_handler_id = logger.add(
        capture_console,
        level="INFO",
        filter=_scoped_destination_filter(logger_id, "console"),
    )
    file_handler_id = logger.add(
        capture_file,
        level="INFO",
        filter=_scoped_destination_filter(logger_id, "file"),
    )
    try:
        logger.bind(to_console_only=True).block("C_ONLY", ["x"])
        logger.bind(to_file_only=True).block("F_ONLY", ["y"])
    finally:
        logger.remove(console_handler_id)
        logger.remove(file_handler_id)

    assert [r["extra"]["pretty_payload"]["title"] for r in console_records] == ["C_ONLY"]
    assert [r["extra"]["pretty_payload"]["title"] for r in file_records] == ["F_ONLY"]


def test_golden_pretty_event_multithreaded_no_duplicate_and_same_routing(tmp_path):
    from pretty_loguru import create_logger

    logger_id = "golden_stress"
    logger = create_logger(logger_id, log_dir=str(tmp_path / "logs"), level="WARNING")

    console_records: list[dict] = []
    file_records: list[dict] = []
    lock = threading.Lock()

    def capture_console(msg):
        with lock:
            console_records.append(msg.record)

    def capture_file(msg):
        with lock:
            file_records.append(msg.record)

    console_handler_id = logger.add(
        capture_console,
        level="INFO",
        filter=_scoped_destination_filter(logger_id, "console"),
    )
    file_handler_id = logger.add(
        capture_file,
        level="INFO",
        filter=_scoped_destination_filter(logger_id, "file"),
    )
    try:
        n = 200

        def work(i: int) -> None:
            logger.bind(seq=i).block("STRESS", [str(i)])

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(work, range(n)))
    finally:
        logger.remove(console_handler_id)
        logger.remove(file_handler_id)

    assert len(console_records) == 200
    assert len(file_records) == 200

    console_seq = {r["extra"]["seq"] for r in console_records}
    file_seq = {r["extra"]["seq"] for r in file_records}
    assert console_seq == file_seq == set(range(200))

    assert all(r["extra"].get("pretty_kind") == "block" for r in console_records)
    assert all(r["extra"].get("pretty_kind") == "block" for r in file_records)
