from typer.testing import CliRunner

from music_metadata_tool.interface.cli.main import app


runner = CliRunner()


def test_scan_invalid_directory_exits_non_zero() -> None:
    # REQ-SCAN-008
    result = runner.invoke(app, ["scan", "does-not-exist"])
    assert result.exit_code != 0
    stderr = getattr(result, "stderr", "")
    assert "does-not-exist" in result.output or "does-not-exist" in stderr
