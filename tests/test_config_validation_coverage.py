from __future__ import annotations

import pytest

from pretty_loguru import LoggerConfig


def test_logger_config_post_init_repairs_attached_loggers():
    cfg = LoggerConfig()
    # 模擬使用者/反序列化破壞了內部欄位
    delattr(cfg, "_attached_loggers")
    cfg.__post_init__()
    assert hasattr(cfg, "_attached_loggers")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"log_dir": 123},
        {"rotation": object()},
        {"retention": object()},
        {"compression": object()},
        {"start_cleaner": "yes"},
        {"use_native_format": "yes"},
        {"verbose": "yes"},
        {"strict_validation": "yes"},
        {"cleaner_include_patterns": "not-a-list"},
        {"cleaner_exclude_patterns": ["ok", 1]},
        {"serialize": "yes"},
        {"loki_enabled": "yes"},
        {"loki_base_url": 123},
        {"loki_labels": {"k": 1}},
        {"loki_batch_size": 0},
        {"loki_flush_interval_seconds": -1},
        {"loki_timeout_seconds": 0},
        {"loki_tenant_id": 123},
        {"loki_username": 123},
        {"loki_password": 123},
    ],
)
def test_logger_config_validate_type_errors(kwargs):
    cfg = LoggerConfig(**kwargs)
    with pytest.raises(TypeError):
        cfg.validate()

