import json
from pathlib import Path

import pytest

from music_metadata_lib.domain.config import ConfigError, load_column_config
from music_metadata_lib.domain.constants import CSV_HEADERS


def test_load_column_config_uses_default_headers_when_config_missing(tmp_path: Path) -> None:
    config = load_column_config(tmp_path / "config.json")

    assert config.columns == list(CSV_HEADERS)


def test_load_column_config_uses_configured_columns(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"columns": ["file_path", "title", "artist"]}),
        encoding="utf-8",
    )

    config = load_column_config(config_path)

    assert config.columns == ["file_path", "title", "artist"]


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({}, "non-empty list"),
        ({"columns": []}, "non-empty list"),
        ({"columns": ["file_path", "title", "title"]}, "duplicates"),
        ({"columns": ["title"]}, "must include 'file_path'"),
        ({"columns": ["file_path", "unknown"]}, "Unsupported columns"),
    ],
)
def test_load_column_config_rejects_invalid_payloads(
    tmp_path: Path,
    payload: dict[str, object],
    message: str,
) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ConfigError, match=message):
        load_column_config(config_path)


def test_load_column_config_rejects_invalid_json(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("{", encoding="utf-8")

    with pytest.raises(ConfigError, match="Failed to load config"):
        load_column_config(config_path)
