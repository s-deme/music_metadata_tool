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
        json.dumps(
            {
                "columns": ["file_path", "title", "artist"],
                "scan_directory": "/workspace/music",
                "scan_output": "/workspace/storage/scan.tsv",
                "apply_input": "/workspace/storage/scan.tsv",
            }
        ),
        encoding="utf-8",
    )

    config = load_column_config(config_path)

    assert config.columns == ["file_path", "title", "artist"]
    assert config.scan_directory == "/workspace/music"
    assert config.scan_output == "/workspace/storage/scan.tsv"
    assert config.apply_input == "/workspace/storage/scan.tsv"


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({}, "non-empty list"),
        ({"columns": []}, "non-empty list"),
        ({"columns": ["file_path", "title", "title"]}, "duplicates"),
        ({"columns": ["title"]}, "must include 'file_path'"),
        ({"columns": ["file_path", "unknown"]}, "Unsupported columns"),
        ({"columns": ["file_path"], "scan_directory": 1}, "scan_directory"),
        ({"columns": ["file_path"], "scan_output": ""}, "scan_output"),
        ({"columns": ["file_path"], "apply_input": []}, "apply_input"),
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
