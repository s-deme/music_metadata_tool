import csv
import io
import sys
from pathlib import Path

import pytest

from music_metadata_lib.application.scan import ScanDirectoryUseCase, ScanError, ScanRequest, TagSet
from music_metadata_lib.infrastructure.scan_adapters import AudioScannerAdapter, DelimitedWriterAdapter


class FakeMetadataReader:
    def read(self, file_path: Path) -> TagSet:
        return TagSet(
            title="",
            artist="",
            album="",
            album_artist="",
            track_number="",
            disc_number="",
            year="",
            genre="",
        )


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")


def test_scan_writes_stdout_csv(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # REQ-SCAN-001, REQ-SCAN-002, REQ-SCAN-005, REQ-SCAN-006, REQ-SCAN-009
    _touch(tmp_path / "b_track.MP3")
    _touch(tmp_path / "a_track.flac")
    _touch(tmp_path / "note.txt")

    buffer = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buffer)

    use_case = ScanDirectoryUseCase(
        scanner=AudioScannerAdapter(),
        reader=FakeMetadataReader(),
        writer=DelimitedWriterAdapter(),
    )
    use_case.execute(ScanRequest(root_dir=tmp_path))

    buffer.seek(0)
    rows = list(csv.reader(buffer))
    assert rows[0][0] == "file_path"
    file_paths = [row[0] for row in rows[1:]]
    expected = sorted(
        [str((tmp_path / "a_track.flac").resolve()), str((tmp_path / "b_track.MP3").resolve())]
    )
    assert file_paths == expected


def test_scan_writes_tsv_file(tmp_path: Path) -> None:
    # REQ-SCAN-003, REQ-SCAN-004, REQ-SCAN-005
    _touch(tmp_path / "music" / "track.wav")

    output_path = tmp_path / "out" / "scan.tsv"
    use_case = ScanDirectoryUseCase(
        scanner=AudioScannerAdapter(),
        reader=FakeMetadataReader(),
        writer=DelimitedWriterAdapter(),
    )
    use_case.execute(ScanRequest(root_dir=tmp_path, output_path=output_path))

    with output_path.open("r", encoding="utf-8") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    assert rows[0] == [
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
    ]
    assert len(rows) == 2


def test_scan_invalid_directory_raises() -> None:
    # REQ-SCAN-008
    use_case = ScanDirectoryUseCase(
        scanner=AudioScannerAdapter(),
        reader=FakeMetadataReader(),
        writer=DelimitedWriterAdapter(),
    )
    with pytest.raises(ScanError):
        use_case.execute(ScanRequest(root_dir=Path("does-not-exist")))
