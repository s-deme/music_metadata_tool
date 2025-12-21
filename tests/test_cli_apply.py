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
