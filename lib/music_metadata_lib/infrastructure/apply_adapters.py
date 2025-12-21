"""apply 向けのインフラアダプタ群。"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Iterator

import mutagen

from music_metadata_lib.application.apply import ApplyError, ApplyRowData, DelimitedReaderPort, MetadataWriterPort, TagSet
from music_metadata_lib.domain.constants import CSV_HEADERS


class DelimitedReaderAdapter(DelimitedReaderPort):
    """CSV/TSV 読み取りとヘッダー検証を行うアダプタ。"""

    def read(self, input_path: Path, delimiter: str) -> Iterable[ApplyRowData]:
        with input_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            headers = reader.fieldnames or []
            missing = [header for header in CSV_HEADERS if header not in headers]
            if missing:
                raise ApplyError(f"Missing required headers: {', '.join(missing)}")

            for row in reader:
                yield ApplyRowData(
                    file_path=row.get("file_path", ""),
                    format=row.get("format", ""),
                    title=row.get("title", ""),
                    artist=row.get("artist", ""),
                    album=row.get("album", ""),
                    album_artist=row.get("album_artist", ""),
                    track_number=row.get("track_number", ""),
                    disc_number=row.get("disc_number", ""),
                    year=row.get("year", ""),
                    genre=row.get("genre", ""),
                )


class MetadataWriterAdapter(MetadataWriterPort):
    """Mutagen を使ったタグ書き込みアダプタ。"""

    def write(self, file_path: Path, tags: TagSet) -> None:
        audio = mutagen.File(file_path, easy=True)
        if audio is None:
            raise ApplyError(f"Unsupported or unreadable audio file: {file_path}")
        if audio.tags is None:
            try:
                audio.add_tags()
            except Exception:
                raise ApplyError(f"Unable to add tags to audio file: {file_path}")

        tag_map = {
            "title": tags.title,
            "artist": tags.artist,
            "album": tags.album,
            "albumartist": tags.album_artist,
            "tracknumber": tags.track_number,
            "discnumber": tags.disc_number,
            "date": tags.year,
            "genre": tags.genre,
        }

        for key, value in tag_map.items():
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
