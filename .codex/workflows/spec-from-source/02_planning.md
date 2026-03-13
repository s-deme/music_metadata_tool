# Reverse Spec Planning

## 目的

解析対象を確定し、どの単位で CSV に落とすか決める。

## 手順

1. 解析対象を列挙する
   - `src/music_metadata_lib/interface/cli/main.py`
   - `src/music_metadata_lib/application/`
   - `src/music_metadata_lib/infrastructure/`
   - `tests/`
   - `README.md`
2. コマンド一覧を洗い出す
   - エントリーポイント
   - サブコマンド
   - オプション
3. 機能カテゴリを仮決めする
   - 例: `scan`, `apply`, `config`, `common error handling`
4. CSV の単位を決める
   - 1行 = 利用者が識別できる1つの仕様
   - 例: `scan の出力先未指定時は STDOUT に CSV を出す`
5. ドキュメント出力先を確認する
   - `docs/reverse-spec/feature-inventory.csv`
   - `docs/reverse-spec/user-spec.md`

## このプロジェクトでの推奨観点

- コマンドの入力: 引数、オプション、必須/任意
- 正常系: 何を読み、何を出力するか
- 異常系: 非ゼロ終了、エラーメッセージ、書き込み抑止
- 設定: `config.json` の有無で変わる挙動
- ファイル形式: CSV/TSV、対応拡張子、パス解決
