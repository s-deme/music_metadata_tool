# Scan Design (C4 + ADR)

**Feature**: scan (metadata export)
**System**: music-metadata-tool CLI
**Scope**: ディレクトリ配下の音楽ファイルを走査し、メタデータを CSV/TSV で出力する。

## Architecture Overview

Library-first を前提に、`scan` は Application 層のユースケースとして実装し、CLI は薄い I/O 層に留める。
列設定は `config.json` を CLI で読み込み、ユースケースへ渡す。

## C4 Context (Level 1)

- **User**: ローカル音楽ファイルのメタデータを一覧で取得したいユーザー
- **System**: music-metadata-tool (CLI + library)
- **External Systems**: ファイルシステム (入力)、CSV/TSV ファイルまたは STDOUT (出力)

## C4 Container (Level 2)

- **CLI Container** (Typer)
  - 役割: 引数解析、ヘルプ、エラーメッセージ
  - 役割: `config.json` の読み込みと列設定の検証
  - 呼び出し先: Application の `ScanDirectory` ユースケース
- **Application Container**
  - 役割: 走査のオーケストレーション、出力形式選択
  - 依存: Domain (タグモデル)、Infrastructure (I/O 実装)
- **Infrastructure Container**
  - 役割: ファイル走査、メタデータ読み取り (Mutagen)、CSV/TSV 出力

## C4 Component (Level 3)

### Application Components

- **ScanDirectoryUseCase**
  - 入力: ルートディレクトリ、出力先パス(任意)
  - 入力: 列順序/表示のリスト
  - 出力: CSV/TSV のストリームまたはファイル書き込み
  - 依存: `AudioScannerPort`, `MetadataReaderPort`, `DelimitedWriterPort`

### Infrastructure Components

- **AudioScannerAdapter**
  - 役割: 対象拡張子のファイルを再帰的に列挙し、パス昇順で返す
- **MetadataReaderAdapter (Mutagen)**
  - 役割: タグ読み取り。欠落タグは空文字で返す
- **DelimitedWriterAdapter**
  - 役割: CSV/TSV のヘッダーと行を逐次書き込み

## Data Model (Logical)

`ScanRow`:
- file_path (absolute)
- format (extension without dot, lowercase)
- title, artist, album, album_artist, track_number, disc_number, year, genre

## ADR (Architecture Decision Records)

### ADR-001: CSV/TSV は拡張子で判定しファイル出力は UTF-8 とする

- **Status**: Accepted
- **Context**: Excel 連携を想定し、CSV と TSV を同一コマンドで扱いたい
- **Decision**: 出力パスの拡張子が `.tsv` の場合のみ TSV を出力し、それ以外は CSV を出力する。ファイル出力のエンコーディングは UTF-8 (BOM なし) を採用し、STDOUT は環境依存とする。
- **Consequences**: 取り回しが簡単。ファイル名の拡張子ミスによる出力形式違いに注意が必要。STDOUT の文字化けは実行環境に依存する。

### ADR-002: 出力順序は file_path 昇順で固定する

- **Status**: Accepted
- **Context**: 再現性のある差分管理と安定した比較が必要
- **Decision**: 走査結果は `file_path` 昇順で出力する
- **Consequences**: スキャン時にソートコストが発生する

### ADR-003: 欠落タグは空文字で出力しスキャンを継続する

- **Status**: Accepted
- **Context**: 欠落タグがあっても一覧出力を止めずに編集対象にしたい
- **Decision**: 欠落/読み取り不可のタグは空文字とし、例外はログに集約しつつ処理を継続する
- **Consequences**: 一部タグ欠落があっても CSV 出力は完了する

### ADR-006: 列の表示/順序は `config.json` で制御する

- **Status**: Accepted
- **Context**: 利用者が Excel で扱う列を最小化したい
- **Decision**: `config.json` の `columns` に列の順序/表示を定義し、scan 出力はその列だけを出力する
- **Consequences**: 設定と CSV の整合性が重要になる

## Traceability Matrix

- REQ-SCAN-001 -> AudioScannerAdapter, ScanDirectoryUseCase
- REQ-SCAN-002 -> ScanDirectoryUseCase, DelimitedWriterAdapter
- REQ-SCAN-003 -> ScanDirectoryUseCase, DelimitedWriterAdapter
- REQ-SCAN-004 -> ScanDirectoryUseCase, DelimitedWriterAdapter
- REQ-SCAN-005 -> DelimitedWriterAdapter, ScanRow schema
- REQ-SCAN-006 -> AudioScannerAdapter, MetadataReaderAdapter, ScanRow schema
- REQ-SCAN-007 -> MetadataReaderAdapter
- REQ-SCAN-008 -> ScanDirectoryUseCase (CLI error mapping)
- REQ-SCAN-009 -> AudioScannerAdapter (sorting)
- REQ-SCAN-011 -> CLI config loader, DelimitedWriterAdapter
- REQ-SCAN-012 -> CLI error mapping
