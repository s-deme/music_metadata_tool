"""music_metadata_lib の CLI エントリポイント。"""

from pathlib import Path
from typing import Optional

import typer

from music_metadata_lib.interface.cli.commands import run_apply, run_scan

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
    spreadsheet_safe: bool = typer.Option(
        False, "--spreadsheet-safe",
        help="表計算ソフト用に数式候補を文字列化（閲覧専用、apply不可）",
    ),
) -> None:
    run_scan(directory, output, spreadsheet_safe)


@app.command(help="CSV/TSV からタグを書き戻し")
def apply(
    input_path: Optional[Path] = typer.Argument(None, exists=False, dir_okay=False, file_okay=True),
    write: bool = typer.Option(False, "--write", help="実ファイルへ書き込み"),
) -> None:
    run_apply(input_path, write)


def run() -> None:
    """CLI を起動する。"""

    app()
if __name__ == "__main__":
    run()
