from music_metadata_lib.domain.constants import SUPPORTED_EXTENSIONS


def test_supported_extensions_match_documented_set() -> None:
    assert SUPPORTED_EXTENSIONS == {
        ".mp3",
        ".flac",
        ".wav",
        ".aiff",
        ".aif",
        ".ogg",
        ".m4a",
    }
