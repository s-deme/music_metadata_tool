from typer.testing import CliRunner

from music_metadata_lib.interface.cli.main import app as library_app
from music_metadata_tool.interface.cli.main import app

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "music-metadata-tool" in result.stdout
    # サブコマンド名がヘルプに含まれていること
    for cmd in ["scan", "apply", "rename", "validate", "config"]:
        assert cmd in result.stdout


def test_library_cli_keeps_shared_commands() -> None:
    result = runner.invoke(library_app, ["--help"])

    assert result.exit_code == 0
    assert "music-metadata-lib" in result.stdout
    for cmd in ["scan", "apply"]:
        assert cmd in result.stdout
