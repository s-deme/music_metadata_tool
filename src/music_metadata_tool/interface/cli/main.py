"""music_metadata_tool の CLI エントリポイント。"""

from pathlib import Path
from typing import Optional

import typer

from music_metadata_lib.interface.cli.commands import run_apply, run_scan
from music_metadata_tool import __version__

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
    directory: Optional[Path] = typer.Argument(None, exists=False, file_okay=False, dir_okay=True),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="出力先 (省略時は STDOUT、.tsv は TSV で出力)",
    ),
) -> None:
    run_scan(directory, output)


@app.command(help="CSV/TSV からタグを書き戻し")
def apply(
    input_path: Optional[Path] = typer.Argument(None, exists=False, dir_okay=False, file_okay=True),
    write: bool = typer.Option(False, "--write", help="実ファイルへ書き込み"),
) -> None:
    run_apply(input_path, write)


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
