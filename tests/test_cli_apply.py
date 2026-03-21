import csv
from pathlib import Path

from typer.testing import CliRunner

from music_metadata_tool.interface.cli.main import app


runner = CliRunner()


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def test_apply_missing_file_exits_non_zero(tmp_path: Path) -> None:
    # REQ-APPLY-005
    input_path = tmp_path / "scan.csv"
    _write_csv(
        input_path,
        [
            [
                "file_path",
                "format",
                "title",
                "artist",
                "album",
                "album_artist",
                "track_number",
                "disc_number",
                "year",
                "genre",
            ],
            ["missing.mp3", "mp3", "", "", "", "", "", "", "", ""],
        ],
    )

    result = runner.invoke(app, ["apply", str(input_path), "--write"])
    assert result.exit_code != 0


def test_apply_missing_input_exits_non_zero() -> None:
    result = runner.invoke(app, ["apply", "missing.csv"])

    assert result.exit_code != 0


def test_apply_invalid_config_exits_non_zero(tmp_path: Path, monkeypatch) -> None:
    input_path = tmp_path / "scan.csv"
    _write_csv(
        input_path,
        [
            [
                "file_path",
                "format",
                "title",
                "artist",
                "album",
                "album_artist",
                "track_number",
                "disc_number",
                "year",
                "genre",
            ],
        ],
    )
    (tmp_path / "config.json").write_text("{", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["apply", str(input_path)])

    assert result.exit_code != 0
    stderr = getattr(result, "stderr", "")
    assert "Failed to load config" in result.output or "Failed to load config" in stderr


def test_apply_uses_configured_input(tmp_path: Path, monkeypatch) -> None:
    audio_path = tmp_path / "track.wav"
    audio_path.write_bytes(b"")
    input_path = tmp_path / "scan.csv"
    _write_csv(
        input_path,
        [
            [
                "file_path",
                "format",
                "title",
                "artist",
                "album",
                "album_artist",
                "track_number",
                "disc_number",
                "year",
                "genre",
            ],
            [str(audio_path), "wav", "", "", "", "", "", "", "", ""],
        ],
    )
    (tmp_path / "config.json").write_text(
        (
            "{\n"
            '  "columns": ["file_path", "format", "title", "artist", "album", "album_artist", "track_number", "disc_number", "year", "genre"],\n'
            f'  "apply_input": "{input_path}"\n'
            "}\n"
        ),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["apply"])

    assert result.exit_code == 0


def test_apply_requires_input_when_not_in_config(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "config.json").write_text(
        '{"columns": ["file_path", "format", "title", "artist", "album", "album_artist", "track_number", "disc_number", "year", "genre"]}',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["apply"])

    assert result.exit_code != 0
    stderr = getattr(result, "stderr", "")
    assert "apply input is required" in result.output or "apply input is required" in stderr
