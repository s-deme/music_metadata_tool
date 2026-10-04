import csv
from dataclasses import fields

import pytest

from music_metadata_lib.application.apply import ApplyError
from music_metadata_lib.application.scan import ScanRow
from music_metadata_lib.infrastructure.apply_adapters import DelimitedReaderAdapter
from music_metadata_lib.infrastructure.delimited_format import (
    SPREADSHEET_SAFE_MARKER, formula_candidate, spreadsheet_value,
)
from music_metadata_lib.infrastructure.scan_adapters import DelimitedWriterAdapter


@pytest.mark.parametrize("value", [
    "=1+1", "+SUM(A1)", "-1+2", "@SUM(A1)", "  =1", "\t+1", "\r\n@x",
    "\x00-1", "\ufeff=1", "\u200b=1",
])
def test_formula_candidates_are_text(value):
    assert formula_candidate(value)
    assert spreadsheet_value(value) == "'" + value


@pytest.mark.parametrize("value", ["", "normal", "artist@example.com", "A+B", "  title"])
def test_normal_values_are_unchanged(value):
    assert not formula_candidate(value)
    assert spreadsheet_value(value) == value


def row(title):
    values = {field.name: "" for field in fields(ScanRow)}
    values.update(file_path="song.mp3", title=title)
    return ScanRow(**values)


def test_normal_csv_preserves_values_for_roundtrip(tmp_path):
    path = tmp_path / "edit.csv"
    with pytest.warns(UserWarning, match="Formula-like"):
        DelimitedWriterAdapter().write([row(" =1")], path, ",", ["file_path", "title"])
    result = list(DelimitedReaderAdapter().read(path, ",", ["file_path", "title"]))
    assert result[0].values["title"] == " =1"


@pytest.mark.parametrize("delimiter,suffix", [(",", ".csv"), ("\t", ".tsv")])
def test_safe_export_identifies_format_and_refuses_apply(tmp_path, delimiter, suffix):
    path = tmp_path / ("view" + suffix)
    DelimitedWriterAdapter(True).write([row("\t=1")], path, delimiter, ["file_path", "title"])
    with path.open(encoding="utf-8", newline="") as handle:
        result = list(csv.reader(handle, delimiter=delimiter))
    assert result[0] == [SPREADSHEET_SAFE_MARKER]
    assert result[2][1] == "'\t=1"
    with pytest.raises(ApplyError, match="view only"):
        list(DelimitedReaderAdapter().read(path, delimiter, ["file_path", "title"]))
