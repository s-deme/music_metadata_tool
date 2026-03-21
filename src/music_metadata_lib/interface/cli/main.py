"""music_metadata_lib の CLI エントリポイント。"""

from pathlib import Path
from typing import Optional

import typer

from music_metadata_lib.application.apply import ApplyError, ApplyMetadataUseCase, ApplyRequest
from music_metadata_lib.application.scan import ScanDirectoryUseCase, ScanError, ScanRequest
from music_metadata_lib.domain.config import ConfigError, load_column_config
from music_metadata_lib.infrastructure.apply_adapters import DelimitedReaderAdapter, MetadataWriterAdapter
from music_metadata_lib.infrastructure.scan_adapters import (
    AudioScannerAdapter,
    DelimitedWriterAdapter,
    MetadataReaderAdapter,
)
from music_metadata_lib.interface.cli.logging import LogContext, default_log_path, log_event


app = typer.Typer(help="music-metadata-lib CLI")


@app.command(help="音楽ファイルを走査しタグを CSV/TSV へ出力")
def scan(
    directory: Optional[Path] = typer.Argument(None, exists=False, file_okay=False, dir_okay=True),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="出力先 (省略時は STDOUT、.tsv は TSV で出力)",
    ),
) -> None:
    """ディレクトリ配下を走査し CSV/TSV を出力する。"""

    log_ctx = LogContext(command="scan", log_path=default_log_path())
    log_event(log_ctx, "START", f"directory={directory}")
    try:
        column_config = load_column_config()
    except ConfigError as exc:
        log_event(log_ctx, "ERROR", str(exc))
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    resolved_directory = directory or _config_path(column_config.scan_directory)
    resolved_output = output or _config_path(column_config.scan_output)
    if resolved_directory is None:
        message = "scan directory is required. Pass DIRECTORY or set 'scan_directory' in config.json."
        log_event(log_ctx, "ERROR", message)
        typer.echo(message, err=True)
        raise typer.Exit(code=1)
    use_case = ScanDirectoryUseCase(
        scanner=AudioScannerAdapter(),
        reader=MetadataReaderAdapter(),
        writer=DelimitedWriterAdapter(),
    )
    try:
        count = use_case.execute(
            ScanRequest(
                root_dir=resolved_directory,
                output_path=resolved_output,
                columns=column_config.columns,
            )
        )
        log_event(log_ctx, "END", "scan completed", count=count)
    except ScanError as exc:
        log_event(log_ctx, "ERROR", str(exc))
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc


@app.command(help="CSV/TSV からタグを書き戻し")
def apply(
    input_path: Optional[Path] = typer.Argument(None, exists=False, dir_okay=False, file_okay=True),
    write: bool = typer.Option(False, "--write", help="実ファイルへ書き込み"),
) -> None:
    """CSV/TSV からタグを書き戻す。"""

    log_ctx = LogContext(command="apply", log_path=default_log_path())
    log_event(log_ctx, "START", f"input={input_path} write={write}")
    try:
        column_config = load_column_config()
    except ConfigError as exc:
        log_event(log_ctx, "ERROR", str(exc))
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    resolved_input = input_path or _config_path(column_config.apply_input)
    if resolved_input is None:
        message = "apply input is required. Pass INPUT_PATH or set 'apply_input' in config.json."
        log_event(log_ctx, "ERROR", message)
        typer.echo(message, err=True)
        raise typer.Exit(code=1)
    use_case = ApplyMetadataUseCase(
        reader=DelimitedReaderAdapter(),
        writer=MetadataWriterAdapter(),
    )
    try:
        count = use_case.execute(
            ApplyRequest(input_path=resolved_input, write=write, columns=column_config.columns)
        )
        written = count if write else 0
        log_event(log_ctx, "END", f"apply completed written={written}", count=count)
    except ApplyError as exc:
        log_event(log_ctx, "ERROR", str(exc))
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc


def run() -> None:
    """CLI を起動する。"""

    app()


def _config_path(value: str | None) -> Path | None:
    if value is None:
        return None
    return Path(value)


if __name__ == "__main__":
    run()
