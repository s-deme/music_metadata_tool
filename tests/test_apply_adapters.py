import csv
from pathlib import Path

import pytest
import mutagen

from music_metadata_lib.application.apply import ApplyError
from music_metadata_lib.infrastructure.apply_adapters import DelimitedReaderAdapter, MetadataWriterAdapter
from music_metadata_lib.domain.constants import CSV_HEADERS


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
        list(reader.read(input_path, ",", list(CSV_HEADERS)))


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
    rows = list(reader.read(input_path, "\t", list(CSV_HEADERS)))
    assert len(rows) == 1


def test_metadata_writer_raises_for_unreadable_audio(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    audio_path = tmp_path / "track.mp3"
    audio_path.write_bytes(b"")

    monkeypatch.setattr(mutagen, "File", lambda *args, **kwargs: None)

    writer = MetadataWriterAdapter()
    with pytest.raises(ApplyError, match="Unsupported or unreadable audio file"):
        writer.write(audio_path, {"title": "Title"})


def test_metadata_writer_skips_save_when_tags_are_unchanged(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audio_path = tmp_path / "track.mp3"
    audio_path.write_bytes(b"")

    class FakeAudio:
        def __init__(self) -> None:
            self.tags = {"title": ["Title"]}
            self.saved = False

        def add_tags(self) -> None:
            raise AssertionError("add_tags should not be called")

        def save(self) -> None:
            self.saved = True

    fake_audio = FakeAudio()
    monkeypatch.setattr(mutagen, "File", lambda *args, **kwargs: fake_audio)

    writer = MetadataWriterAdapter()
    writer.write(audio_path, {"title": "Title"})

    assert fake_audio.saved is False


def test_metadata_writer_saves_when_tags_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audio_path = tmp_path / "track.mp3"
    audio_path.write_bytes(b"")

    class FakeAudio:
        def __init__(self) -> None:
            self.tags = {"title": ["Old Title"]}
            self.saved = False

        def add_tags(self) -> None:
            raise AssertionError("add_tags should not be called")

        def save(self) -> None:
            self.saved = True

    fake_audio = FakeAudio()
    monkeypatch.setattr(mutagen, "File", lambda *args, **kwargs: fake_audio)

    writer = MetadataWriterAdapter()
    writer.write(audio_path, {"title": "New Title"})

    assert fake_audio.tags["title"] == ["New Title"]
    assert fake_audio.saved is True
