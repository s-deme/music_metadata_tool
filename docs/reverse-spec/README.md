# Reverse Spec

このディレクトリは、既存ソースコードから利用者向け仕様を逆生成するための成果物置き場です。

## 生成物

- `feature-inventory.csv`: 仕様の一次ソース
- `user-spec.md`: CSV から自動生成する Markdown 仕様書
- `user-spec.html`: 必要に応じて HTML 化した版

## 使い方

1. `.codex/workflows/spec-from-source/00_master.md` を入口としてワークフローを実行する
2. `feature-inventory.csv` を埋める
3. `./bin/reverse-spec-md` で `user-spec.md` を再生成する
4. `./bin/reverse-spec-html` で `user-spec.html` を再生成する
5. `./bin/test` で関連テストを実行する

## 運用ルール

- `feature-inventory.csv` を唯一の一次ソースとして扱う
- `user-spec.md` は手編集しない
- 実装変更時は CSV を更新してから Markdown/HTML を再生成する

## このリポジトリでの対象

- `scan` コマンド
- `apply` コマンド
- `config.json` による列制御
- CLI の正常系と異常系
- `rename`, `validate`, `config` の未実装プレースホルダ

## 公開向け補足

- `config.json` はローカル設定として扱い、リポジトリには含めない
- 共有用の例は `config.example.json` を使う
