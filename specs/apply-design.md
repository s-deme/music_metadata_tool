# Apply Design (C4 + ADR)

**Feature**: apply (metadata import)
**System**: music-metadata-tool CLI
**Scope**: CSV/TSV を読み込み、音楽ファイルのメタデータを更新する。

## Architecture Overview

Library-first を前提に、`apply` は Application 層のユースケースとして実装し、CLI は薄い I/O 層に留める。

## C4 Context (Level 1)

- **User**: CSV/TSV で編集したタグをファイルへ反映したいユーザー
- **System**: music-metadata-tool (CLI + library)
- **External Systems**: ファイルシステム (音楽ファイル)、CSV/TSV ファイル (入力)

## C4 Container (Level 2)

- **CLI Container** (Typer)
  - 役割: 引数解析、`--write` の有無判定、エラーメッセージ
  - 呼び出し先: Application の `ApplyMetadataUseCase`
- **Application Container**
  - 役割: CSV/TSV 読み取り、パス解決、バリデーション、書き込み指示
  - 依存: Infrastructure (DelimitedReader, MetadataWriter)
- **Infrastructure Container**
  - 役割: CSV/TSV 解析、Mutagen でタグ書き込み

## C4 Component (Level 3)

### Application Components

- **ApplyMetadataUseCase**
  - 入力: CSV/TSV パス、`--write` フラグ
  - 出力: 例外/終了コードのみ（通常は STDOUT 出力なし）
  - 依存: `DelimitedReaderPort`, `MetadataWriterPort`

### Infrastructure Components

- **DelimitedReaderAdapter**
  - 役割: CSV/TSV を読み取り、ヘッダー検証を行う
- **MetadataWriterAdapter**
  - 役割: Mutagen を使ってタグを書き込む

## ADR (Architecture Decision Records)

### ADR-004: `--write` なしはドライラン

- **Status**: Accepted
- **Context**: 誤更新を防ぐため、デフォルトは安全側に倒す必要がある
- **Decision**: `--write` 指定がない場合は書き込みを行わず、入力の検証のみ行う
- **Consequences**: 実更新には必ず `--write` が必要

### ADR-005: 入力拡張子で CSV/TSV を判別する

- **Status**: Accepted
- **Context**: ユーザーが拡張子でファイル種別を直感的に扱える
- **Decision**: `.tsv` は TSV、それ以外は CSV として扱う
- **Consequences**: 誤った拡張子は出力形式の誤解釈につながる

## Traceability Matrix

- REQ-APPLY-001 -> DelimitedReaderAdapter
- REQ-APPLY-002 -> ApplyMetadataUseCase, DelimitedReaderAdapter
- REQ-APPLY-003 -> ApplyMetadataUseCase, CLI apply
- REQ-APPLY-004 -> ApplyMetadataUseCase, MetadataWriterAdapter
- REQ-APPLY-005 -> ApplyMetadataUseCase, CLI apply
- REQ-APPLY-006 -> ApplyMetadataUseCase
- REQ-APPLY-007 -> ApplyMetadataUseCase
