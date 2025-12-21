"""CLI ログ出力ユーティリティ。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import os


@dataclass(frozen=True)
class LogContext:
    command: str
    log_path: Path


def default_log_path() -> Path:
    """既定のログ出力先を返す。"""

    env_path = os.environ.get("MUSIC_METADATA_LOG_PATH")
    if env_path:
        return Path(env_path)
    return Path("storage/logs/cli.log")


def log_event(
    ctx: LogContext,
    status: str,
    message: str,
    count: Optional[int] = None,
) -> None:
    """ログを 1 行追記する。"""

    timestamp = datetime.now().isoformat(timespec="seconds")
    count_text = str(count) if count is not None else "-"
    line = f"{timestamp}\t{status}\t{ctx.command}\tcount={count_text}\t{message}\n"

    try:
        ctx.log_path.parent.mkdir(parents=True, exist_ok=True)
        ctx.log_path.open("a", encoding="utf-8").write(line)
    except Exception:
        # ログ失敗は処理を止めない
        return
