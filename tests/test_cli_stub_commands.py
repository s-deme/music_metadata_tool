from typer.testing import CliRunner

from music_metadata_tool.interface.cli.main import app


runner = CliRunner()


def test_stub_commands_report_not_implemented() -> None:
    for command in ["rename", "validate", "config"]:
        result = runner.invoke(app, [command])
        assert result.exit_code == 0
        assert f"{command}: not yet implemented" in result.stdout
