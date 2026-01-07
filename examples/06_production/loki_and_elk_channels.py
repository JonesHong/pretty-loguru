#!/usr/bin/env python3
"""
Loki + ELK Channels (minimal, low-noise)

目標：
1) 展示「不需要做複雜 routing API」的做法：用不同 logger 代表不同管道
   - app_logger：一般 console / file（開發與排查用）
   - elk_logger：只寫入專用檔案（供 Filebeat 收集 → Elasticsearch）
   - loki_logger：直推到 Loki（供 Grafana 查詢）

2) 回答常見疑問：為什麼 serialize=True 的內容看起來很複雜？
   - 這是 loguru 的 serialize schema：每行 JSON 會包含 record/time/level/extra 等完整結構
   - 真正「你要看的訊息」通常在 `record["message"]`

執行方式：
    python examples/06_production/loki_and_elk_channels.py

搭配 Loki/Grafana（可選）：
    docker compose -f examples/observability/docker-compose.yml up -d
    # 預設 Loki URL http://localhost:3100

搭配 ELK/Filebeat（可選）：
    - 讓 Filebeat 只收集 logs/elk-events/**/*.log（避免全量 logs/ 造成雜訊）
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from pretty_loguru import create_logger


def _env_flag(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")


def _extract_loguru_serialize_message(line: str) -> Optional[Dict[str, Any]]:
    """
    解析 loguru serialize=True 的單行 JSON，並回傳你通常真正要看的欄位。

    loguru 的 serialize 不是只存 message，而是存完整 record。
    這裡做「示意性的抽取」，避免使用者以為資料不可用或太雜。
    """
    try:
        obj = json.loads(line)
        if not isinstance(obj, dict):
            return None

        record = obj.get("record")
        if not isinstance(record, dict):
            # 非 loguru serialize schema（例如 ELK_PURE_JSON=1 的純 JSON line）
            return None

        extra = record.get("extra")
        if not isinstance(extra, dict):
            extra = {}

        # 兼容：某些舊版/錯誤用法可能把額外資料塞到 extra["extra"]（dict）裡
        nested_extra = extra.get("extra")
        if isinstance(nested_extra, dict):
            extra = {**nested_extra, **{k: v for k, v in extra.items() if k != "extra"}}

        logger_name = extra.get("name")

        extra = {
            k: v
            for k, v in extra.items()
            if k
            not in (
                # pretty-loguru internal routing / rendering keys
                "logger_id",
                "name",
                "to_console_only",
                "to_file_only",
                "pretty_text",
            )
        }
        return {
            "message": record.get("message"),
            "level": (record.get("level") or {}).get("name"),
            "logger_name": logger_name,
            "time": record.get("time"),
            "extra": extra,
        }
    except Exception:
        return None


def _write_serialize_view_file(source_log: Path) -> Optional[Path]:
    """
    將 loguru serialize=True 的檔案轉成「較可讀的 view 檔」（JSON lines）。

    目的：保留原始機器友善的完整 record（source_log），同時提供人類好讀版（*.view.jsonl）。
    """
    try:
        lines = source_log.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None

    # 避免 daily_latest.temp.log 累積太多內容，view 檔只取最後 N 行（足夠 debug / demo）
    tail_n = 200
    if len(lines) > tail_n:
        lines = lines[-tail_n:]

    extracted: list[Dict[str, Any]] = []
    for line in lines:
        payload = _extract_loguru_serialize_message(line)
        if isinstance(payload, dict):
            extracted.append(payload)

    view_path = source_log.with_suffix(".view.jsonl")
    try:
        view_path.write_text(
            "\n".join(json.dumps(x, ensure_ascii=False) for x in extracted) + ("\n" if extracted else ""),
            encoding="utf-8",
        )
    except Exception:
        return None
    return view_path


def _pick_latest_existing_log_file(log_dir: Path) -> Optional[Path]:
    """
    從目錄挑出「目前存在」且 mtime 最新的 *.log。

    Windows + loguru rotation/enqueue 的組合下，檔案可能在列舉與 stat/read 之間被輪換/更名，
    範例程式應該要容忍這種競態條件，避免 demo 直接炸掉。
    """
    candidates: list[tuple[float, Path]] = []
    for p in log_dir.glob("**/*.log"):
        try:
            candidates.append((p.stat().st_mtime, p))
        except FileNotFoundError:
            continue
        except OSError:
            continue
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def main() -> None:
    root = Path.cwd()
    # 輸出策略：
    # - ELK events：預設不印到終端（避免刷屏）
    # - Loki events：預設印到終端（方便你確認「真的有送」）
    #
    # 也提供 SHOW_CHANNEL_EVENTS_IN_CONSOLE 作為一鍵全開。
    show_all = _env_flag("SHOW_CHANNEL_EVENTS_IN_CONSOLE", default=False)
    show_elk_events_in_console = _env_flag("SHOW_ELK_EVENTS_IN_CONSOLE", default=False) or show_all
    show_loki_events_in_console = _env_flag("SHOW_LOKI_EVENTS_IN_CONSOLE", default=True) or show_all

    # 1) 一般用途：你的程式日常 log（console + file）
    app_logger = create_logger(
        "app",
        log_dir=root / "logs" / "app",
        preset="daily",
    )

    # 2) ELK：建立「專用檔案管道」→ 讓 Filebeat 只收這個資料夾（降低雜訊）
    elk_dir = root / "logs" / "elk-events"
    elk_pure_json = os.getenv("ELK_PURE_JSON", "").lower() in ("1", "true", "yes")
    elk_logger = create_logger(
        "elk_events",
        log_dir=elk_dir,
        # 預設：用 loguru serialize schema（方便保留完整 record）
        # 若你只想要「純 JSON line」給 Filebeat，設 ELK_PURE_JSON=1，並以 message 自行輸出 JSON 字串
        serialize=not elk_pure_json,
        format="{message}" if elk_pure_json else None,
        preset="daily",
    )

    # 3) Loki：建立「專用直推管道」
    # 注意：pretty-loguru 的 Loki 直推是 best-effort（不重試/無離線緩衝/無 backpressure）
    # 若 Loki 沒開，程式仍會正常跑完，只是 Loki 看不到資料。
    loki_base_url = os.getenv("LOKI_BASE_URL", "http://localhost:3100")
    loki_log_dir_env = os.getenv("LOKI_LOG_DIR")
    loki_log_dir: Optional[Path] = None
    if loki_log_dir_env:
        p = Path(loki_log_dir_env)
        loki_log_dir = p if p.is_absolute() else (root / p)
    loki_logger = create_logger(
        "loki_events",
        loki_enabled=True,
        loki_base_url=loki_base_url,
        loki_labels={"app": "pretty-loguru", "channel": "loki-events", "env": os.getenv("APP_ENV", "local")},
        loki_batch_size=1,
        loki_timeout_seconds=0.5,
        # Loki sink 會使用 serialize=True（在 core/base.py 內部 add sink 時固定）
        # 這裡也開啟 serialize=True 讓你本地 file（若你之後加 log_dir）也能一致。
        serialize=True,
        # 預設不落檔；若你也想在本機留「可回放」的檔案，設定 LOKI_LOG_DIR（例如 logs/loki-events）
        log_dir=loki_log_dir,
    )

    app_logger.info("app logger: 這是一般日誌（console + file）")
    app_logger.info(
        "提示：ELK events 預設不顯示在終端（避免刷屏）；Loki events 預設會顯示。"
        " 你也可以用 SHOW_CHANNEL_EVENTS_IN_CONSOLE=1 全部顯示，或用"
        " SHOW_ELK_EVENTS_IN_CONSOLE / SHOW_LOKI_EVENTS_IN_CONSOLE 分別控制。"
    )

    # 對於「事件流」logger：用 bind() 注入 routing flag，避免 console 被事件刷屏
    #
    # 注意：不要用 logger.info(..., extra={...})
    # - 在 loguru 裡，kwargs 主要用於 message format，並不會自動進到 record["extra"]
    # - 正確做法是 logger.bind(...) 或 logger.opt(...).bind(...)
    elk_route_kw = {} if show_elk_events_in_console else {"to_file_only": True}
    loki_route_kw = {} if show_loki_events_in_console else {"to_file_only": True}

    if elk_pure_json:
        elk_logger.bind(**elk_route_kw).info(
            json.dumps({"event": "user_signup", "user_id": 123, "plan": "pro"}, ensure_ascii=False)
        )
        elk_logger.bind(**elk_route_kw).info(
            json.dumps({"event": "payment_retry", "order_id": "A-001", "attempt": 2, "level": "WARNING"}, ensure_ascii=False)
        )
    else:
        elk_logger.bind(**elk_route_kw, user_id=123, plan="pro").info("elk event: user_signup")
        elk_logger.bind(**elk_route_kw, order_id="A-001", attempt=2).warning("elk event: payment_retry")

    # Loki 事件：同樣用 to_file_only 來避免 console 雜訊（Loki sink 仍會吃到這筆）
    loki_logger.bind(**loki_route_kw, version="1.2.0").info("loki event: deployment_started")
    loki_logger.bind(**loki_route_kw, duration_ms=1532).success("loki event: deployment_succeeded")

    # 4) 示範：從 ELK 檔案（serialize JSON）抽出「你要看的純內容」
    last_file = _pick_latest_existing_log_file(elk_dir)
    if not last_file:
        app_logger.warning("找不到 ELK log 檔案，請確認是否有寫入權限")
    else:
        try:
            lines = last_file.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            # 可能剛好被 rotation 更名了，這裡不要讓 demo 直接炸掉
            app_logger.warning("ELK log 檔案在讀取時被輪換/更名，請再執行一次範例")
            lines = []
        except Exception:
            lines = []

        if not lines:
            app_logger.warning(f"ELK 專用檔案存在但內容為空或讀取失敗: {last_file}")
        else:
            last_line = lines[-1]
            extracted = None if elk_pure_json else _extract_loguru_serialize_message(last_line)
            app_logger.info(f"ELK 專用檔案: {last_file}")
            app_logger.info(f"ELK 檔案最後一行（原始 JSON）長度: {len(last_line)}")
            if elk_pure_json:
                app_logger.info("ELK_PURE_JSON=1：檔案每行就是你自己輸出的 JSON（無 loguru record 包裝）")
                try:
                    app_logger.info(f"ELK 純 JSON（解析後）: {json.loads(last_line)}")
                except Exception:
                    app_logger.info(f"ELK 純 JSON line（未能解析）: {last_line}")
            else:
                app_logger.info(f"ELK 抽取後（你通常關心的欄位）: {extracted}")
                view_path = _write_serialize_view_file(last_file)
                if view_path:
                    app_logger.info(f"ELK view 檔（較可讀的 JSONL）: {view_path}")

    # 5) （可選）若你有設定 LOKI_LOG_DIR，則同樣生成本機的 view 檔
    if loki_log_dir:
        loki_logs = sorted(loki_log_dir.glob("**/*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
        if loki_logs:
            loki_view = _write_serialize_view_file(loki_logs[0])
            if loki_view:
                app_logger.info(f"Loki view 檔（較可讀的 JSONL）: {loki_view}")

    app_logger.info("完成：已各送出 2 筆 ELK 事件 + 2 筆 Loki 事件（Loki 需服務存在才會看到）")


if __name__ == "__main__":
    main()
