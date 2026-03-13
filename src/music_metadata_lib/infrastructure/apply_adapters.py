"""apply 向けのインフラアダプタ群。"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Iterator

import mutagen

from music_metadata_lib.application.apply import ApplyError, ApplyRowData, DelimitedReaderPort, MetadataWriterPort


class DelimitedReaderAdapter(DelimitedReaderPort):
    """CSV/TSV 読み取りとヘッダー検証を行うアダプタ。"""

    def read(
        self,
        input_path: Path,
        delimiter: str,
        required_headers: list[str],
    ) -> Iterable[ApplyRowData]:
        with input_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            headers = reader.fieldnames or []
            missing = [header for header in required_headers if header not in headers]
            if missing:
                raise ApplyError(f"Missing required headers: {', '.join(missing)}")

            for row in reader:
                file_path = row.get("file_path") or ""
                values = {
                    header: (row.get(header) or "")
                    for header in required_headers
                    if header != "file_path"
                }
                yield ApplyRowData(
                    file_path=file_path,
                    values=values,
                )


class MetadataWriterAdapter(MetadataWriterPort):
    """Mutagen を使ったタグ書き込みアダプタ。"""

    def write(self, file_path: Path, tags: dict[str, str]) -> None:
        audio = mutagen.File(file_path, easy=True)
        if audio is None:
            raise ApplyError(f"Unsupported or unreadable audio file: {file_path}")
        if audio.tags is None:
            try:
                audio.add_tags()
            except Exception:
                raise ApplyError(f"Unable to add tags to audio file: {file_path}")

        tag_map = {
            "title": "title",
            "artist": "artist",
            "album": "album",
            "album_artist": "albumartist",
            "track_number": "tracknumber",
            "disc_number": "discnumber",
            "year": "date",
            "genre": "genre",
        }

        for column, value in tags.items():
            key = tag_map.get(column)
            if key is None:
                continue
            _set_or_clear(audio.tags, key, value)

        audio.save()


def _set_or_clear(tags: mutagen.Tags, key: str, value: str) -> None:
    """タグ値を設定し、空なら削除する。"""

    if value:
        tags[key] = [value]
    else:
        try:
            del tags[key]
        except KeyError:
            pass
