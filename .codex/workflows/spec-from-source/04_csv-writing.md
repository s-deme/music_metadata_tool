# Reverse Spec CSV Writing

## 目的

抽出した事実を CSV に正規化して、後続の Markdown/HTML 化へ渡す。

## 出力ファイル

- `docs/reverse-spec/feature-inventory.csv`

## CSV ヘッダー

以下のヘッダーを使用する。

```csv
id,category,feature,behavior,conditions,notes,evidence,status
```

## 列定義

- `id`: `RS-001` のような通し番号
- `category`: `scan`, `apply`, `common` など
- `feature`: 機能名
- `behavior`: 利用者視点の事実
- `conditions`: 発動条件、前提、例外条件
- `notes`: 補足、実装差分、未確認事項
- `evidence`: 根拠ファイル。複数可
- `status`: `tested`, `implemented`, `needs-review`

## 記入ルール

1. 1行につき1仕様
2. `behavior` は断定形で書く
3. 条件がある場合のみ `conditions` に分離する
4. 根拠は最低1つ、可能なら実装とテストの両方を書く
5. 迷う行は `status=needs-review` にする

## CLI 向けの具体例

```csv
RS-001,scan,標準出力への出力,scan コマンドは output 未指定時に CSV を標準出力へ出力する,output が未指定,ヘッダー行を含む,"src/music_metadata_lib/interface/cli/main.py; tests/test_cli_scan.py",tested
RS-002,apply,ドライラン,apply コマンドは --write がない場合にファイルを書き換えない,--write 未指定,入力検証は実行する,"src/music_metadata_lib/application/apply.py; tests/test_cli_apply.py",tested
```
