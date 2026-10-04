"""scan 向けのインフラアダプタ群。"""

from __future__ import annotations

import csv
import sys
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator, Optional, TextIO

import mutagen

from music_metadata_lib.application.scan import (
    AudioScannerPort,
    DelimitedWriterPort,
    MetadataReaderPort,
    ScanRow,
    TagSet,
)
from music_metadata_lib.domain.constants import CSV_HEADERS, SUPPORTED_EXTENSIONS
from music_metadata_lib.infrastructure.delimited_format import (
    SPREADSHEET_SAFE_MARKER, formula_candidate, spreadsheet_value,
)


class AudioScannerAdapter(AudioScannerPort):
    """拡張子フィルタ付きのファイル走査アダプタ。"""

    def scan(self, root_dir: Path) -> Iterable[Path]:
        candidates = (
            path
            for path in root_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        )
        return sorted(candidates, key=str)


class MetadataReaderAdapter(MetadataReaderPort):
    """Mutagen を使ったタグ読み取りアダプタ。"""

    def read(self, file_path: Path) -> TagSet:
        tags = {}
        try:
            audio = mutagen.File(file_path, easy=True)
            if audio and audio.tags:
                tags = audio.tags
        except Exception:
            tags = {}

        return TagSet(
            title=_pick_tag(tags, ["title"]),
            artist=_pick_tag(tags, ["artist"]),
            album=_pick_tag(tags, ["album"]),
            album_artist=_pick_tag(tags, ["albumartist", "album_artist"]),
            track_number=_pick_tag(tags, ["tracknumber", "track"]),
            disc_number=_pick_tag(tags, ["discnumber", "disc"]),
            year=_pick_tag(tags, ["date", "year"]),
            genre=_pick_tag(tags, ["genre"]),
        )


class DelimitedWriterAdapter(DelimitedWriterPort):
    """CSV/TSV の逐次書き込みアダプタ。"""

    def __init__(self, spreadsheet_safe: bool = False) -> None:
        self.spreadsheet_safe = spreadsheet_safe

    def write(
        self,
        rows: Iterable[ScanRow],
        output_path: Optional[Path],
        delimiter: str,
        headers: list[str],
    ) -> None:
        with _open_output(output_path) as handle:
            writer = csv.writer(handle, delimiter=delimiter)
            if self.spreadsheet_safe:
                writer.writerow([SPREADSHEET_SAFE_MARKER])
            writer.writerow(headers)
            warned = False
            for row in rows:
                values = _row_values(row, headers)
                if self.spreadsheet_safe:
                    values = [spreadsheet_value(value) for value in values]
                elif not warned and any(formula_candidate(value) for value in values):
                    warnings.warn(
                        "Formula-like values found. Use scan --spreadsheet-safe for spreadsheet "
                        "viewing; normal output preserves tags for apply.",
                        UserWarning,
                        stacklevel=2,
                    )
                    warned = True
                writer.writerow(values)


def _row_values(row: ScanRow, headers: list[str]) -> list[str]:
    return [str(getattr(row, header)) for header in headers]


def _pick_tag(tags: dict, keys: Iterable[str]) -> str:
    """候補キーから最初に見つかったタグ値を返す。"""

    for key in keys:
        if key in tags:
            value = tags.get(key)
            if isinstance(value, list):
                return str(value[0]) if value else ""
            return str(value)
    return ""


@contextmanager
def _open_output(output_path: Optional[Path]) -> Iterator[TextIO]:
    """STDOUT またはファイルへ出力するハンドルを返す。"""

    if output_path is None:
        yield sys.stdout
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        yield handle
