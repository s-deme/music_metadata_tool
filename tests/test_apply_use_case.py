import csv
from pathlib import Path

import pytest

from music_metadata_lib.application.apply import ApplyError, ApplyMetadataUseCase, ApplyRequest, ApplyRowData
from music_metadata_lib.domain.constants import CSV_HEADERS


class FakeReader:
    def __init__(self, rows: list[ApplyRowData]) -> None:
        self._rows = rows

    def read(self, input_path: Path, delimiter: str, required_headers: list[str]) -> list[ApplyRowData]:
        return self._rows


class FakeWriter:
    def __init__(self) -> None:
        self.called_with: list[tuple[Path, dict[str, str]]] = []

    def write(self, file_path: Path, tags: dict[str, str]) -> None:
        self.called_with.append((file_path, tags))


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def test_apply_dry_run_does_not_write(tmp_path: Path) -> None:
    # REQ-APPLY-003
    audio_path = tmp_path / "track.mp3"
    audio_path.write_bytes(b"")
    (tmp_path / "scan.csv").write_text("", encoding="utf-8")

    reader = FakeReader(
        [
            ApplyRowData(
                file_path=str(audio_path),
                values={},
            )
        ]
    )
    writer = FakeWriter()
    use_case = ApplyMetadataUseCase(reader=reader, writer=writer)
    use_case.execute(
        ApplyRequest(input_path=tmp_path / "scan.csv", write=False, columns=list(CSV_HEADERS))
    )
    assert writer.called_with == []


def test_apply_write_resolves_relative_path(tmp_path: Path) -> None:
    # REQ-APPLY-004, REQ-APPLY-007
    audio_path = tmp_path / "music" / "track.mp3"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    audio_path.write_bytes(b"")
    (tmp_path / "scan.csv").write_text("", encoding="utf-8")

    reader = FakeReader(
        [
            ApplyRowData(
                file_path="music/track.mp3",
                values={
                    "title": "Title",
                    "artist": "Artist",
                    "album": "Album",
                    "album_artist": "Album Artist",
                    "track_number": "1",
                    "disc_number": "1",
                    "year": "2024",
                    "genre": "Pop",
                },
            )
        ]
    )
    writer = FakeWriter()
    use_case = ApplyMetadataUseCase(reader=reader, writer=writer)
    use_case.execute(
        ApplyRequest(input_path=tmp_path / "scan.csv", write=True, columns=list(CSV_HEADERS))
    )

    assert writer.called_with
    called_path, _ = writer.called_with[0]
    assert called_path == audio_path.resolve()


def test_apply_invalid_extension_raises(tmp_path: Path) -> None:
    # REQ-APPLY-006
    audio_path = tmp_path / "track.txt"
    audio_path.write_bytes(b"")

    reader = FakeReader(
        [
            ApplyRowData(
                file_path=str(audio_path),
                values={},
            )
        ]
    )
    writer = FakeWriter()
    use_case = ApplyMetadataUseCase(reader=reader, writer=writer)
    with pytest.raises(ApplyError):
        use_case.execute(
            ApplyRequest(input_path=tmp_path / "scan.csv", write=True, columns=list(CSV_HEADERS))
        )


def test_apply_missing_file_raises(tmp_path: Path) -> None:
    # REQ-APPLY-005
    reader = FakeReader(
        [
            ApplyRowData(
                file_path="missing.mp3",
                values={},
            )
        ]
    )
    writer = FakeWriter()
    use_case = ApplyMetadataUseCase(reader=reader, writer=writer)
    with pytest.raises(ApplyError):
        use_case.execute(
            ApplyRequest(input_path=tmp_path / "scan.csv", write=True, columns=list(CSV_HEADERS))
        )


def test_apply_omits_unconfigured_columns(tmp_path: Path) -> None:
    audio_path = tmp_path / "track.mp3"
    audio_path.write_bytes(b"")
    (tmp_path / "scan.csv").write_text("", encoding="utf-8")

    reader = FakeReader(
        [
            ApplyRowData(
                file_path=str(audio_path),
                values={
                    "title": "Title",
                    "genre": "Pop",
                },
            )
        ]
    )
    writer = FakeWriter()
    use_case = ApplyMetadataUseCase(reader=reader, writer=writer)
    use_case.execute(
        ApplyRequest(input_path=tmp_path / "scan.csv", write=True, columns=["file_path", "title"])
    )

    assert writer.called_with
    _, tags = writer.called_with[0]
    assert tags == {"title": "Title"}


def test_apply_missing_file_path_raises(tmp_path: Path) -> None:
    (tmp_path / "scan.csv").write_text("", encoding="utf-8")

    reader = FakeReader([ApplyRowData(file_path="", values={})])
    writer = FakeWriter()
    use_case = ApplyMetadataUseCase(reader=reader, writer=writer)

    with pytest.raises(ApplyError, match="Missing file_path value"):
        use_case.execute(
            ApplyRequest(input_path=tmp_path / "scan.csv", write=True, columns=list(CSV_HEADERS))
        )
