# Scan Requirements (EARS)

**Feature**: scan (metadata export)
**System**: music-metadata-tool CLI
**Scope**: ディレクトリ配下の音楽ファイルを走査し、メタデータを CSV/TSV で出力する。

## Assumptions

- 対象フォーマットは拡張子で判定する: `.mp3`, `.flac`, `.wav`, `.aiff`, `.aif`, `.ogg`, `.m4a`
- CSV/TSV は UTF-8 (BOM なし) で出力する
- 出力は再現性のためパス昇順で整列する

## Requirements

### REQ-SCAN-001 (Ubiquitous)
The music-metadata-tool scan command SHALL recursively scan the provided directory and include only files with supported audio extensions.

**Acceptance Criteria**
- 指定したディレクトリ配下を再帰的に走査する
- 対象拡張子のみを抽出する（大文字小文字は区別しない）

### REQ-SCAN-002 (Event-driven)
WHEN the scan command is invoked without an explicit output path, the system SHALL write the metadata list to STDOUT in CSV format.

**Acceptance Criteria**
- 出力先未指定時は STDOUT に CSV を出力する
- CSV はヘッダー行を含む

### REQ-SCAN-003 (Event-driven)
WHEN an output path is provided, the system SHALL write the metadata list to that path and create parent directories if needed.

**Acceptance Criteria**
- 出力先ディレクトリが無い場合は作成する
- 出力先は上書きする

### REQ-SCAN-004 (State-driven)
WHILE the output path ends with `.tsv`, the system SHALL emit tab-separated values; OTHERWISE it SHALL emit comma-separated values.

**Acceptance Criteria**
- `.tsv` は TSV で出力される
- それ以外は CSV で出力される

### REQ-SCAN-005 (Ubiquitous)
The system SHALL output a header row with the following columns in this order:
`file_path`, `format`, `title`, `artist`, `album`, `album_artist`, `track_number`, `disc_number`, `year`, `genre`.

**Acceptance Criteria**
- ヘッダーの列名と順序が一致する
- すべての行で列数が一致する

### REQ-SCAN-006 (Ubiquitous)
The system SHALL include one row per scanned audio file with `file_path` as an absolute path and `format` as the lowercase file extension without a dot.

**Acceptance Criteria**
- `file_path` は絶対パスである
- `format` は拡張子からドットを除き小文字化する

### REQ-SCAN-007 (Unwanted behavior)
IF a tag is missing or unreadable, THEN the system SHALL emit an empty field for that tag and continue scanning.

**Acceptance Criteria**
- 欠落/読み取り不可のタグは空文字になる
- 他のファイルの処理に影響しない

### REQ-SCAN-008 (Event-driven)
WHEN the provided directory does not exist or is not accessible, the system SHALL exit with a non-zero status and print a human-readable error message.

**Acceptance Criteria**
- 終了コードが 0 以外
- エラーメッセージにパスが含まれる

### REQ-SCAN-009 (Ubiquitous)
The system SHALL sort output rows by `file_path` in ascending order to ensure reproducible output.

**Acceptance Criteria**
- 同一入力で同一順序になる

### REQ-SCAN-010 (Ubiquitous)
The system SHALL complete scanning 1,000 files within 60 seconds on a typical developer machine.

**Acceptance Criteria**
- 1,000 ファイルのサンプルで 60 秒以内に完了する
