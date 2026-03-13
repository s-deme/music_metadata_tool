#!/usr/bin/env python3
"""Render reverse-spec CSV into a grouped Markdown user specification."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path


CATEGORY_TITLES = {
    "common": "Common",
    "config": "Config",
    "scan": "Scan",
    "apply": "Apply",
    "stub": "Stub Commands",
}


def read_rows(input_path: Path) -> list[dict[str, str]]:
    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def render_markdown(rows: list[dict[str, str]], csv_path: str) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)

    lines = [
        "# User Specification",
        "",
        f"この文書は `{csv_path}` を一次ソースとして自動生成したものです。",
        "",
        "## Summary",
        "",
        "- 対象: `common`, `config`, `scan`, `apply`, `stub`",
        f"- 一次ソース: `{csv_path}`",
        "- 運用: 実装変更時は CSV を先に更新し、この文書と HTML を再生成する",
        "",
    ]

    for category in ["common", "config", "scan", "apply", "stub"]:
        category_rows = grouped.get(category, [])
        if not category_rows:
            continue

        lines.append(f"## {CATEGORY_TITLES[category]}")
        lines.append("")
        for row in category_rows:
            lines.append(f"### {row['id']} {row['feature']}")
            lines.append("")
            lines.append(row["behavior"])
            if row.get("conditions"):
                lines.append("")
                lines.append(f"- 条件: {row['conditions']}")
            if row.get("notes"):
                lines.append(f"- 補足: {row['notes']}")
            if row.get("status"):
                lines.append(f"- 状態: {row['status']}")
            if row.get("evidence"):
                lines.append(f"- 根拠: {row['evidence']}")
            lines.append("")

    lines.extend(
        [
            "## Maintenance",
            "",
            "更新手順:",
            "",
            "1. `docs/reverse-spec/feature-inventory.csv` を更新する",
            "2. `./bin/reverse-spec-md` で Markdown を再生成する",
            "3. `./bin/reverse-spec-html` で HTML を再生成する",
            "4. `./bin/test` で関連テストを確認する",
            "",
            "## Placeholder Policy",
            "",
            "`rename`, `validate`, `config` は現時点ではプレースホルダです。ヘルプには表示されますが、実処理は持たず `not yet implemented` を返します。",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "Usage: python tools/csv_to_user_spec_md.py <input.csv> <output.md>",
            file=sys.stderr,
        )
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    rows = read_rows(input_path)
    content = render_markdown(rows, str(input_path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
