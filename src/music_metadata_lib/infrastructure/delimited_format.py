"""File-level identification and escaping for spreadsheet-only exports."""

import unicodedata

SPREADSHEET_SAFE_MARKER = "# music_metadata_tool spreadsheet-safe v1 (view only)"


def formula_candidate(value: str) -> bool:
    # Spreadsheet importers can discard leading whitespace and control characters.
    index = 0
    while index < len(value) and (
        value[index].isspace() or unicodedata.category(value[index]) in {"Cc", "Cf"}
    ):
        index += 1
    return bool(value[index:]) and value[index] in "=+-@"


def spreadsheet_value(value: str) -> str:
    return "'" + value if formula_candidate(value) else value
