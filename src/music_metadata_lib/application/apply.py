"""apply ユースケースと入出力モデル。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Protocol

from music_metadata_lib.domain.config import TAG_COLUMNS
from music_metadata_lib.domain.constants import CSV_HEADERS, SUPPORTED_EXTENSIONS


@dataclass(frozen=True)
class ApplyRowData:
    """CSV/TSV の 1 行を表すデータ。"""

    file_path: str
    values: dict[str, str]


@dataclass(frozen=True)
class ApplyRequest:
    """apply 実行時の入力パラメータ。"""

    input_path: Path
    write: bool = False
    columns: Optional[list[str]] = None


class ApplyError(RuntimeError):
    """apply 実行中のエラー。"""

    pass


class DelimitedReaderPort(Protocol):
    """CSV/TSV 読み取りポート。"""

    def read(
        self,
        input_path: Path,
        delimiter: str,
        required_headers: list[str],
    ) -> Iterable[ApplyRowData]:
        ...


class MetadataWriterPort(Protocol):
    """タグ書き込みポート。"""

    def write(self, file_path: Path, tags: dict[str, str]) -> None:
        ...


class ApplyMetadataUseCase:
    """CSV/TSV からタグを書き戻すユースケース。"""

    def __init__(self, reader: DelimitedReaderPort, writer: MetadataWriterPort) -> None:
        self._reader = reader
        self._writer = writer

    def execute(self, request: ApplyRequest) -> int:
        input_path = request.input_path
        if not input_path.exists() or not input_path.is_file():
            raise ApplyError(f"Input file not found or not accessible: {input_path}")

        delimiter = "\t" if input_path.suffix.lower() == ".tsv" else ","
        base_dir = input_path.parent
        columns = request.columns or list(CSV_HEADERS)
        tag_columns = [column for column in columns if column in TAG_COLUMNS]

        processed = 0
        for row in self._reader.read(input_path, delimiter, columns):
            processed += 1
            if not row.file_path:
                raise ApplyError("Missing file_path value.")
            resolved_path = self._resolve_path(base_dir, row.file_path)
            self._validate_audio_path(resolved_path)

            tags = {column: row.values.get(column, "") for column in tag_columns}

            if request.write:
                self._writer.write(resolved_path, tags)

        return processed

    @staticmethod
    def _resolve_path(base_dir: Path, file_path: str) -> Path:
        candidate = Path(file_path)
        if not candidate.is_absolute():
            candidate = base_dir / candidate
        return candidate.resolve()

    @staticmethod
    def _validate_audio_path(file_path: Path) -> None:
        if not file_path.exists() or not file_path.is_file():
            raise ApplyError(f"File not found or not accessible: {file_path}")
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ApplyError(f"Unsupported audio extension: {file_path}")

    @staticmethod
    def required_headers() -> list[str]:
        return list(CSV_HEADERS)
