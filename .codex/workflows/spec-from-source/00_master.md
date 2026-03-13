# Reverse Spec Workflow

ソースコードから利用者向け仕様をリバースで作成するための入口ファイル。

## 目的

- 既存コードを根拠に、機能一覧と利用者向け仕様書を段階的に作成する
- 推測や補完を避け、コード上で確認できた事実だけを記述する
- 仕様の根拠を対象ファイルへトレースできる状態を保つ

## 実行手順

次のファイルを上から順に読み、各フェーズを完了させること。

1. `.codex/workflows/spec-from-source/01_rules.md`
2. `.codex/workflows/spec-from-source/02_planning.md`
3. `.codex/workflows/spec-from-source/03_code-analysis.md`
4. `.codex/workflows/spec-from-source/04_csv-writing.md`
5. `.codex/workflows/spec-from-source/05_verification.md`
6. `.codex/workflows/spec-from-source/06_checklist.md`

## このリポジトリ向けの前提

- 対象は Web 画面ではなく CLI コマンドと機能仕様
- 主要な対象は `scan` と `apply`
- 根拠ファイルは `src/` と `tests/`、必要に応じて `README.md` と `config.json`
- 出力先の初期値は `docs/reverse-spec/`

## 成果物

- 機能一覧 CSV: `docs/reverse-spec/feature-inventory.csv`
- 利用者向け仕様書 Markdown: `docs/reverse-spec/user-spec.md`
- 必要に応じて HTML: `docs/reverse-spec/user-spec.html`
