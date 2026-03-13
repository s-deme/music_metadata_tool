# Apply Requirements (EARS)

**Feature**: apply (metadata import)
**System**: music-metadata-tool CLI
**Scope**: CSV/TSV を読み込み、音楽ファイルのメタデータを更新する。

## Assumptions

- 入力ファイルは scan 出力と同じヘッダーを持つ
- CSV/TSV は UTF-8 (BOM なし) で読み込む
- file_path が相対パスの場合は、CSV/TSV のあるディレクトリを基準に解決する
- `config.json` が存在する場合は `columns` に列順序/表示が定義され、`file_path` は必須とする

## Requirements

### REQ-APPLY-001 (Ubiquitous)
The music-metadata-tool apply command SHALL read a CSV/TSV file containing metadata rows with the required header columns.

**Acceptance Criteria**
- ヘッダーに `file_path`, `format`, `title`, `artist`, `album`, `album_artist`,
  `track_number`, `disc_number`, `year`, `genre` が含まれる
- 欠落ヘッダーがある場合はエラーで終了する

### REQ-APPLY-002 (State-driven)
WHILE the input file path ends with `.tsv`, the system SHALL parse tab-separated values; OTHERWISE it SHALL parse comma-separated values.

**Acceptance Criteria**
- `.tsv` は TSV として解釈される
- それ以外は CSV として解釈される

### REQ-APPLY-003 (Event-driven)
WHEN the apply command is invoked without `--write`, the system SHALL perform a dry-run without modifying files.

**Acceptance Criteria**
- `--write` がない場合、ファイルは更新されない
- 解析とバリデーションは行われる

### REQ-APPLY-004 (Event-driven)
WHEN the apply command is invoked with `--write`, the system SHALL write tags to the referenced audio files.

**Acceptance Criteria**
- 対象ファイルのタグが CSV/TSV の値で更新される

### REQ-APPLY-005 (Unwanted behavior)
IF a referenced file does not exist or is not accessible, THEN the system SHALL exit with a non-zero status and report the path.

**Acceptance Criteria**
- 終了コードが 0 以外
- エラーメッセージにパスが含まれる

### REQ-APPLY-006 (Ubiquitous)
The system SHALL only attempt to update files with supported audio extensions.

**Acceptance Criteria**
- サポート外拡張子はエラーとして扱う

### REQ-APPLY-007 (Ubiquitous)
The system SHALL resolve each `file_path` entry to an absolute path before processing.

**Acceptance Criteria**
- 相対パスは CSV/TSV のディレクトリを基準に解決される
- すべての処理対象パスが絶対パスになる

### REQ-APPLY-008 (Event-driven)
WHEN `config.json` is present, the system SHALL require only the configured columns and update only those columns.

**Acceptance Criteria**
- 入力に必須となる列は `config.json` の `columns` に一致する
- 設定に含まれない列は更新対象にならない

### REQ-APPLY-009 (Unwanted behavior)
IF `config.json` is invalid, THEN the system SHALL exit with a non-zero status and report the error.

**Acceptance Criteria**
- 終了コードが 0 以外
- エラーメッセージが設定ファイル起因であることが分かる
