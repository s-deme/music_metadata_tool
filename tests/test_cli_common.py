from pathlib import Path
import wave

from typer.testing import CliRunner

from music_metadata_lib.interface.cli.logging import default_log_path
from music_metadata_tool.interface.cli.main import app


runner = CliRunner()


def _write_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(44100)
        handle.writeframes(b"\x00\x00" * 441)


def test_scan_success_writes_log_file(tmp_path: Path, monkeypatch) -> None:
    log_path = tmp_path / "cli.log"
    monkeypatch.setenv("MUSIC_METADATA_LOG_PATH", str(log_path))

    music_dir = tmp_path / "music"
    _write_wav(music_dir / "track.wav")

    result = runner.invoke(app, ["scan", str(music_dir)])

    assert result.exit_code == 0
    content = log_path.read_text(encoding="utf-8")
    assert "\tSTART\tscan\t" in content
    assert "\tEND\tscan\tcount=1\tscan completed" in content


def test_default_log_path_uses_project_location_when_env_missing(monkeypatch) -> None:
    monkeypatch.delenv("MUSIC_METADATA_LOG_PATH", raising=False)

    assert default_log_path() == Path("storage/logs/cli.log")
