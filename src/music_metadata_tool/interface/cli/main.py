"""music_metadata_tool の CLI エントリポイント。"""

from pathlib import Path
from typing import Optional

import typer

from music_metadata_tool import __version__
from music_metadata_lib.application.apply import ApplyError, ApplyMetadataUseCase, ApplyRequest
from music_metadata_lib.application.scan import ScanDirectoryUseCase, ScanError, ScanRequest
from music_metadata_lib.infrastructure.apply_adapters import DelimitedReaderAdapter, MetadataWriterAdapter
from music_metadata_lib.infrastructure.scan_adapters import (
    AudioScannerAdapter,
    DelimitedWriterAdapter,
    MetadataReaderAdapter,
)
from music_metadata_lib.interface.cli.logging import LogContext, default_log_path, log_event


app = typer.Typer(help="music-metadata-tool CLI")


def version_callback(value: bool) -> None:
    """--version が指定されたらバージョンを出力して終了する。"""

    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="バージョンを表示して終了",
    ),
) -> None:
    """グローバルオプションの初期化を行う。"""
    ctx.ensure_object(dict)


@app.command(help="音楽ファイルを走査しタグを CSV/TSV へ出力")
def scan(
    directory: Path = typer.Argument(..., exists=False, file_okay=False, dir_okay=True),
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
    use_case = ScanDirectoryUseCase(
        scanner=AudioScannerAdapter(),
        reader=MetadataReaderAdapter(),
        writer=DelimitedWriterAdapter(),
    )
    try:
        count = use_case.execute(ScanRequest(root_dir=directory, output_path=output))
        log_event(log_ctx, "END", "scan completed", count=count)
    except ScanError as exc:
        log_event(log_ctx, "ERROR", str(exc))
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc


@app.command(help="CSV/TSV からタグを書き戻し")
def apply(
    input_path: Path = typer.Argument(..., exists=False, dir_okay=False, file_okay=True),
    write: bool = typer.Option(False, "--write", help="実ファイルへ書き込み"),
) -> None:
    """CSV/TSV からタグを書き戻す。"""

    log_ctx = LogContext(command="apply", log_path=default_log_path())
    log_event(log_ctx, "START", f"input={input_path} write={write}")
    use_case = ApplyMetadataUseCase(
        reader=DelimitedReaderAdapter(),
        writer=MetadataWriterAdapter(),
    )
    try:
        count = use_case.execute(ApplyRequest(input_path=input_path, write=write))
        written = count if write else 0
        log_event(log_ctx, "END", f"apply completed written={written}", count=count)
    except ApplyError as exc:
        log_event(log_ctx, "ERROR", str(exc))
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc


@app.command(help="タグに基づくファイル名/ディレクトリ整形（雛形）")
def rename() -> None:
    """タグに基づくファイル名/ディレクトリ整形（雛形）。"""

    typer.echo("rename: not yet implemented")


@app.command(help="必須タグ/エンコードチェックのレポート（雛形）")
def validate() -> None:
    """必須タグ/エンコードチェックのレポート（雛形）。"""

    typer.echo("validate: not yet implemented")


@app.command(help="設定/テンプレート管理（雛形）")
def config() -> None:
    """設定/テンプレート管理（雛形）。"""

    typer.echo("config: not yet implemented")


def run() -> None:
    """CLI を起動する。"""

    app()


if __name__ == "__main__":
    run()
