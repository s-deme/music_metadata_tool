from pathlib import Path
import wave

from music_metadata_lib.infrastructure.scan_adapters import AudioScannerAdapter, MetadataReaderAdapter


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")


def _write_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(44100)
        handle.writeframes(b"\x00\x00" * 441)


def test_audio_scanner_filters_and_sorts(tmp_path: Path) -> None:
    # REQ-SCAN-001, REQ-SCAN-009
    _touch(tmp_path / "b_song.MP3")
    _touch(tmp_path / "a_song.flac")
    _touch(tmp_path / "other.txt")
    _touch(tmp_path / "nested" / "c_song.wav")

    scanner = AudioScannerAdapter()
    results = list(scanner.scan(tmp_path))
    expected = [
        tmp_path / "a_song.flac",
        tmp_path / "b_song.MP3",
        tmp_path / "nested" / "c_song.wav",
    ]
    assert results == expected


def test_metadata_reader_missing_tags_returns_empty(tmp_path: Path) -> None:
    # REQ-SCAN-007
    audio_path = tmp_path / "track.wav"
    _write_wav(audio_path)

    reader = MetadataReaderAdapter()
    tags = reader.read(audio_path)
    assert tags.title == ""
    assert tags.artist == ""
    assert tags.album == ""
    assert tags.album_artist == ""
    assert tags.track_number == ""
    assert tags.disc_number == ""
    assert tags.year == ""
    assert tags.genre == ""
