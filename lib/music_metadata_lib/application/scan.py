"""scan ユースケースと入出力モデル。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Protocol


@dataclass(frozen=True)
class TagSet:
    """読み取ったタグ集合。"""

    title: str
    artist: str
    album: str
    album_artist: str
    track_number: str
    disc_number: str
    year: str
    genre: str


@dataclass(frozen=True)
class ScanRow:
    """CSV/TSV 出力用の 1 行データ。"""

    file_path: str
    format: str
    title: str
    artist: str
    album: str
    album_artist: str
    track_number: str
    disc_number: str
    year: str
    genre: str


@dataclass(frozen=True)
class ScanRequest:
    """scan 実行時の入力パラメータ。"""

    root_dir: Path
    output_path: Optional[Path] = None


class ScanError(RuntimeError):
    """scan 実行中のエラー。"""

    pass


class AudioScannerPort(Protocol):
    """音楽ファイル列挙ポート。"""

    def scan(self, root_dir: Path) -> Iterable[Path]:
        ...


class MetadataReaderPort(Protocol):
    """タグ読み取りポート。"""

    def read(self, file_path: Path) -> TagSet:
        ...


class DelimitedWriterPort(Protocol):
    """CSV/TSV 出力ポート。"""

    def write(self, rows: Iterable[ScanRow], output_path: Optional[Path], delimiter: str) -> None:
        ...


class ScanDirectoryUseCase:
    """ディレクトリ走査とメタデータ出力のユースケース。"""

    def __init__(
        self,
        scanner: AudioScannerPort,
        reader: MetadataReaderPort,
        writer: DelimitedWriterPort,
    ) -> None:
        self._scanner = scanner
        self._reader = reader
        self._writer = writer

    def execute(self, request: ScanRequest) -> int:
        root_dir = request.root_dir
        if not root_dir.exists() or not root_dir.is_dir():
            raise ScanError(f"Directory not found or not accessible: {root_dir}")

        output_path = request.output_path
        delimiter = "\t" if output_path and output_path.suffix.lower() == ".tsv" else ","

        count = 0

        def iter_rows() -> Iterable[ScanRow]:
            nonlocal count
            for file_path in self._scanner.scan(root_dir):
                count += 1
                yield self._build_row(file_path, self._reader.read(file_path))

        rows = iter_rows()
        self._writer.write(rows, output_path, delimiter)
        return count

    @staticmethod
    def _build_row(file_path: Path, tags: TagSet) -> ScanRow:
        file_path_abs = file_path.resolve()
        extension = file_path.suffix.lower().lstrip(".")
        return ScanRow(
            file_path=str(file_path_abs),
            format=extension,
            title=tags.title,
            artist=tags.artist,
            album=tags.album,
            album_artist=tags.album_artist,
            track_number=tags.track_number,
            disc_number=tags.disc_number,
            year=tags.year,
            genre=tags.genre,
        )
