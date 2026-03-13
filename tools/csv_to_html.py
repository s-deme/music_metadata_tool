#!/usr/bin/env python3
"""Render reverse-spec CSV into a simple HTML table."""

from __future__ import annotations

import csv
import html
import sys
from pathlib import Path


def render_table(rows: list[dict[str, str]], headers: list[str]) -> str:
    header_html = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body_parts: list[str] = []
    for row in rows:
        cells = "".join(
            f"<td>{html.escape((row.get(header) or '').replace(';', '; '))}</td>"
            for header in headers
        )
        body_parts.append(f"<tr>{cells}</tr>")
    return (
        "<table>\n"
        f"<thead><tr>{header_html}</tr></thead>\n"
        "<tbody>\n"
        + "\n".join(body_parts)
        + "\n</tbody>\n"
        "</table>"
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python tools/csv_to_html.py <input.csv> <output.html>", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)

    table_html = render_table(rows, headers)
    document = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reverse Spec</title>
  <style>
    body {{
      font-family: sans-serif;
      margin: 24px;
      line-height: 1.5;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #999;
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f0f0f0;
    }}
    tr:nth-child(even) {{
      background: #fafafa;
    }}
  </style>
</head>
<body>
  <h1>Reverse Spec</h1>
  {table_html}
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
