"""設定ファイルの読み取りとバリデーション。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from music_metadata_lib.domain.constants import CSV_HEADERS


class ConfigError(RuntimeError):
    """設定ファイルのエラー。"""


@dataclass(frozen=True)
class ColumnConfig:
    """CLI 設定。"""

    columns: list[str]
    scan_directory: str | None = None
    scan_output: str | None = None
    apply_input: str | None = None

    def tag_columns(self) -> list[str]:
        return [column for column in self.columns if column in TAG_COLUMNS]


TAG_COLUMNS = [
    "title",
    "artist",
    "album",
    "album_artist",
    "track_number",
    "disc_number",
    "year",
    "genre",
]


def load_column_config(config_path: Path | None = None) -> ColumnConfig:
    """config.json から CLI 設定を読み込む。"""

    path = config_path or Path("config.json")
    if not path.exists():
        return ColumnConfig(columns=list(CSV_HEADERS))

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Failed to load config: {path}") from exc

    columns = payload.get("columns")
    if not isinstance(columns, list) or not columns:
        raise ConfigError("Config 'columns' must be a non-empty list.")

    normalized = _normalize_columns(columns)
    _validate_columns(normalized)
    return ColumnConfig(
        columns=normalized,
        scan_directory=_normalize_optional_path(payload.get("scan_directory"), "scan_directory"),
        scan_output=_normalize_optional_path(payload.get("scan_output"), "scan_output"),
        apply_input=_normalize_optional_path(payload.get("apply_input"), "apply_input"),
    )


def _normalize_columns(columns: Iterable[object]) -> list[str]:
    normalized: list[str] = []
    for column in columns:
        if not isinstance(column, str):
            raise ConfigError("Config 'columns' must contain strings only.")
        value = column.strip()
        if not value:
            raise ConfigError("Config 'columns' must not contain empty strings.")
        normalized.append(value)
    return normalized


def _validate_columns(columns: list[str]) -> None:
    if len(columns) != len(set(columns)):
        raise ConfigError("Config 'columns' must not contain duplicates.")
    invalid = [column for column in columns if column not in CSV_HEADERS]
    if invalid:
        raise ConfigError(f"Unsupported columns in config: {', '.join(invalid)}")
    if "file_path" not in columns:
        raise ConfigError("Config 'columns' must include 'file_path'.")


def _normalize_optional_path(value: object, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ConfigError(f"Config '{field_name}' must be a string.")

    normalized = value.strip()
    if not normalized:
        raise ConfigError(f"Config '{field_name}' must not be empty.")
    return normalized
