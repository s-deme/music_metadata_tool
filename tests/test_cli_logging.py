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


def test_apply_dry_run_writes_log_file(tmp_path: Path, monkeypatch) -> None:
    log_path = tmp_path / "cli.log"
    monkeypatch.setenv("MUSIC_METADATA_LOG_PATH", str(log_path))

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

    result = runner.invoke(app, ["apply", str(input_path)])

    assert result.exit_code == 0
    content = log_path.read_text(encoding="utf-8")
    assert "\tSTART\tapply\t" in content
    assert "\tEND\tapply\tcount=1\tapply completed written=0" in content
