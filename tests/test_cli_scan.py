from typer.testing import CliRunner

from music_metadata_tool.interface.cli.main import app


runner = CliRunner()


def test_scan_invalid_directory_exits_non_zero() -> None:
    # REQ-SCAN-008
    result = runner.invoke(app, ["scan", "does-not-exist"])
    assert result.exit_code != 0
    stderr = getattr(result, "stderr", "")
    assert "does-not-exist" in result.output or "does-not-exist" in stderr


def test_scan_invalid_config_exits_non_zero(tmp_path, monkeypatch) -> None:
    music_dir = tmp_path / "music"
    music_dir.mkdir()
    (tmp_path / "config.json").write_text("{", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["scan", str(music_dir)])

    assert result.exit_code != 0
    stderr = getattr(result, "stderr", "")
    assert "Failed to load config" in result.output or "Failed to load config" in stderr
