import csv
from pathlib import Path

import pytest

from music_metadata_lib.application.apply import ApplyError
from music_metadata_lib.infrastructure.apply_adapters import DelimitedReaderAdapter


def _write_csv(path: Path, rows: list[list[str]], delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter=delimiter)
        writer.writerows(rows)


def test_delimited_reader_missing_header_raises(tmp_path: Path) -> None:
    # REQ-APPLY-001
    input_path = tmp_path / "scan.csv"
    _write_csv(input_path, [["file_path", "format"], ["song.mp3", "mp3"]])

    reader = DelimitedReaderAdapter()
    with pytest.raises(ApplyError):
        list(reader.read(input_path, ","))


def test_delimited_reader_reads_tsv(tmp_path: Path) -> None:
    # REQ-APPLY-002
    input_path = tmp_path / "scan.tsv"
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
            ["song.mp3", "mp3", "", "", "", "", "", "", "", ""],
        ],
        delimiter="\t",
    )

    reader = DelimitedReaderAdapter()
    rows = list(reader.read(input_path, "\t"))
    assert len(rows) == 1
