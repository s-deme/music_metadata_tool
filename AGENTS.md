# Music Metadata Tool

- 機能範囲は音楽メタデータの scan（CSV/TSV出力）と apply（CSV/TSV取込）だけで、CSV編集機能は追加しない。
- 実装は src/music_metadata_lib/ と src/music_metadata_tool/、テストは tests/ を正本にする。
- 仕様は追跡対象の specs/<feature>-*.md を使い、storage/specs/ は更新しないレガシー領域とする。
- 検証は README の Docker または bin/test を優先する。
