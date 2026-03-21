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


def test_scan_uses_configured_directory_and_output(tmp_path, monkeypatch) -> None:
    music_dir = tmp_path / "music"
    music_dir.mkdir()
    output_path = tmp_path / "storage" / "scan.csv"
    (tmp_path / "config.json").write_text(
        (
            "{\n"
            '  "columns": ["file_path", "format"],\n'
            f'  "scan_directory": "{music_dir}",\n'
            f'  "scan_output": "{output_path}"\n'
            "}\n"
        ),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["scan"])

    assert result.exit_code == 0
    assert output_path.exists()


def test_scan_requires_directory_when_not_in_config(tmp_path, monkeypatch) -> None:
    (tmp_path / "config.json").write_text('{"columns": ["file_path", "format"]}', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["scan"])

    assert result.exit_code != 0
    stderr = getattr(result, "stderr", "")
    assert "scan directory is required" in result.output or "scan directory is required" in stderr
