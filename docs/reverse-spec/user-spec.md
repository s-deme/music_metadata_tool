# User Specification

この文書は `docs/reverse-spec/feature-inventory.csv` を一次ソースとして自動生成したものです。

## Summary

- 対象: `common`, `config`, `scan`, `apply`, `stub`
- 一次ソース: `docs/reverse-spec/feature-inventory.csv`
- 運用: 実装変更時は CSV を先に更新し、この文書と HTML を再生成する

## Common

### RS-001 CLI help

CLI は `--help` でコマンド一覧を表示する

- 条件: ヘルプを要求した場合
- 補足: `scan`,`apply`,`rename`,`validate`,`config` が表示される
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; tests/test_cli_help.py

### RS-002 CLI version

CLI は `--version` でバージョン文字列を表示して終了する

- 条件: `--version` 指定時
- 補足: バージョン値はパッケージ定数から取得する
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_tool/__init__.py; tests/test_cli_common.py

### RS-003 CLI logging

CLI は開始・終了・エラーのイベントをログファイルへ追記する

- 条件: `scan` または `apply` 実行時
- 補足: ログ書き込み失敗は処理を停止しない
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_lib/interface/cli/logging.py; tests/test_cli_common.py

### RS-004 Default log path

CLI ログの既定出力先は `storage/logs/cli.log` である

- 条件: 環境変数未設定時
- 補足: 環境変数 `MUSIC_METADATA_LOG_PATH` で変更できる
- 状態: tested
- 根拠: src/music_metadata_lib/interface/cli/logging.py; README.md; tests/test_cli_common.py

## Config

### RS-005 Missing config fallback

`config.json` が存在しない場合は既定の全列構成を使用する

- 条件: プロジェクト直下に `config.json` がない場合
- 補足: 既定列は `file_path` から `genre` までの 10 列
- 状態: tested
- 根拠: src/music_metadata_lib/domain/config.py; src/music_metadata_lib/domain/constants.py; tests/test_config.py

### RS-006 Configured columns

`config.json` の `columns` が有効な場合はその列順だけを使用する

- 条件: `config.json` が存在し `columns` が妥当な場合
- 補足: `scan` の出力列と `apply` の更新対象の両方に影響する
- 状態: tested
- 根拠: src/music_metadata_lib/domain/config.py; src/music_metadata_tool/interface/cli/main.py; README.md; tests/test_config.py

### RS-007 Config validation

`config.json` の `columns` は非空の文字列リストで重複なく `file_path` を含まなければならない

- 条件: 設定読み込み時
- 補足: 未対応列や重複や空文字はエラーになる
- 状態: tested
- 根拠: src/music_metadata_lib/domain/config.py; tests/test_config.py

### RS-008 Invalid config exit

`config.json` が読めないか不正な場合は CLI は標準エラーへメッセージを出して非ゼロ終了する

- 条件: `scan` または `apply` 実行時に設定エラーが発生した場合
- 補足: エラーメッセージは設定ファイル由来であることを含む
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_lib/domain/config.py; tests/test_cli_scan.py; tests/test_cli_apply.py

## Scan

### RS-009 Recursive audio scan

`scan` は指定ディレクトリ配下を再帰的に走査し対応拡張子の音楽ファイルだけを対象にする

- 条件: 対象ディレクトリが存在しアクセス可能な場合
- 補足: 拡張子比較は大文字小文字を区別しない
- 状態: tested
- 根拠: src/music_metadata_lib/application/scan.py; src/music_metadata_lib/infrastructure/scan_adapters.py; tests/test_scan_use_case.py; tests/test_scan_adapters.py

### RS-010 Supported extensions

`scan` の対象拡張子は `.mp3`, `.flac`, `.wav`, `.aiff`, `.aif`, `.ogg`, `.m4a` である

- 条件: 再帰走査時
- 補足: 他拡張子は出力対象外
- 状態: tested
- 根拠: src/music_metadata_lib/domain/constants.py; README.md; tests/test_constants.py

### RS-011 Sorted output

`scan` の出力行は `file_path` 昇順で安定化される

- 条件: 対象ファイルが複数ある場合
- 補足: 再現性確保のためソートする
- 状態: tested
- 根拠: src/music_metadata_lib/infrastructure/scan_adapters.py; tests/test_scan_use_case.py; tests/test_scan_adapters.py

### RS-012 Default stdout CSV

`scan` は `--output` 未指定時にヘッダー付き CSV を標準出力へ書き出す

- 条件: `--output` が未指定の場合
- 補足: 区切り文字はカンマを使う
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_lib/application/scan.py; src/music_metadata_lib/infrastructure/scan_adapters.py; tests/test_scan_use_case.py

### RS-013 File output creation

`scan` は出力先指定時に親ディレクトリを作成してファイルへ上書き出力する

- 条件: `--output` が指定された場合
- 補足: ファイル出力は UTF-8 で行う
- 状態: tested
- 根拠: src/music_metadata_lib/infrastructure/scan_adapters.py; tests/test_scan_use_case.py

### RS-014 TSV selection

`scan` は出力先拡張子が `.tsv` のときだけ TSV を出力しそれ以外は CSV を出力する

- 条件: `--output` 指定時
- 補足: 標準出力時は CSV になる
- 状態: tested
- 根拠: src/music_metadata_lib/application/scan.py; tests/test_scan_use_case.py

### RS-015 Scan row schema

`scan` は `file_path`,`format`,`title`,`artist`,`album`,`album_artist`,`track_number`,`disc_number`,`year`,`genre` を出力する

- 条件: 既定列構成を使う場合
- 補足: `file_path` は絶対パスで `format` は拡張子の小文字からドットを除いた値
- 状態: tested
- 根拠: src/music_metadata_lib/application/scan.py; src/music_metadata_lib/domain/constants.py; tests/test_scan_use_case.py

### RS-016 Missing tags

`scan` は欠落タグまたは読み取り失敗を空文字として出力し処理を継続する

- 条件: タグが存在しないか Mutagen 読み取りで例外が出た場合
- 補足: 一部ファイルのタグ欠落で全体は失敗しない
- 状態: tested
- 根拠: src/music_metadata_lib/infrastructure/scan_adapters.py; tests/test_scan_adapters.py

### RS-017 Invalid directory error

`scan` は入力ディレクトリが存在しないかディレクトリでない場合にエラーメッセージを出して非ゼロ終了する

- 条件: 対象パス不正時
- 補足: メッセージには指定パスを含む
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_lib/application/scan.py; tests/test_cli_scan.py; tests/test_scan_use_case.py

### RS-018 Configured scan columns

`scan` は有効な `config.json` がある場合に設定された列だけを設定順で出力する

- 条件: `config.json` が有効な場合
- 補足: 未設定列は出力しない
- 状態: tested
- 根拠: src/music_metadata_lib/application/scan.py; src/music_metadata_lib/infrastructure/scan_adapters.py; src/music_metadata_lib/domain/config.py; README.md; tests/test_scan_use_case.py

## Apply

### RS-019 Input file validation

`apply` は指定入力が存在するファイルでない場合にエラーメッセージを出して非ゼロ終了する

- 条件: 入力パス不正時
- 補足: ユースケースは処理開始前に失敗する
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_lib/application/apply.py; tests/test_cli_apply.py

### RS-020 Required headers

`apply` は入力 CSV または TSV に必須ヘッダーが揃っていることを要求する

- 条件: 読み込み開始時
- 補足: 不足ヘッダーがあるとエラーにする
- 状態: tested
- 根拠: src/music_metadata_lib/infrastructure/apply_adapters.py; tests/test_apply_adapters.py

### RS-021 TSV parsing

`apply` は入力ファイル拡張子が `.tsv` のときタブ区切りで読み込みそれ以外はカンマ区切りで読む

- 条件: 入力ファイル読込時
- 補足: 拡張子判定で区切り文字を選ぶ
- 状態: tested
- 根拠: src/music_metadata_lib/application/apply.py; tests/test_apply_adapters.py

### RS-022 Dry run default

`apply` は `--write` が無い場合に入力の解析と検証だけを行い音楽ファイルを書き換えない

- 条件: `--write` 未指定時
- 補足: 処理件数は数えるが書き込み件数は 0 としてログされる
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; src/music_metadata_lib/application/apply.py; tests/test_apply_use_case.py

### RS-023 Write on demand

`apply` は `--write` 指定時に各行のタグ値を対象ファイルへ書き込む

- 条件: `--write` 指定時
- 補足: 空文字のタグ値は削除として扱う
- 状態: tested
- 根拠: src/music_metadata_lib/application/apply.py; src/music_metadata_lib/infrastructure/apply_adapters.py; tests/test_apply_use_case.py

### RS-024 Relative path resolution

`apply` は相対 `file_path` を入力 CSV または TSV の配置ディレクトリ基準で絶対パスに解決する

- 条件: 入力行の `file_path` が相対パスの場合
- 補足: 絶対パスは `resolve()` で正規化される
- 状態: tested
- 根拠: src/music_metadata_lib/application/apply.py; tests/test_apply_use_case.py

### RS-025 Missing file_path value

`apply` は入力行の `file_path` が空ならエラーにする

- 条件: 行処理時
- 補足: 空文字は許可しない
- 状態: tested
- 根拠: src/music_metadata_lib/application/apply.py; tests/test_apply_use_case.py

### RS-026 Audio file validation

`apply` は存在しないファイルや未対応拡張子のファイルを更新対象にできない

- 条件: 各行処理時
- 補足: 未対応拡張子はエラーにする
- 状態: tested
- 根拠: src/music_metadata_lib/application/apply.py; tests/test_apply_use_case.py; tests/test_cli_apply.py

### RS-027 Configured apply columns

`apply` は有効な `config.json` の列だけを必須入力かつ更新対象として扱う

- 条件: `config.json` が有効な場合
- 補足: 設定にない列は書き込まない
- 状態: tested
- 根拠: src/music_metadata_lib/application/apply.py; src/music_metadata_lib/domain/config.py; tests/test_apply_use_case.py; README.md

### RS-028 Unreadable audio handling

`apply` は Mutagen が開けない音声ファイルをエラーにする

- 条件: `--write` で書き込み時に音声ファイルが未対応または読めない場合
- 補足: タグ追加に失敗した場合もエラーにする
- 状態: tested
- 根拠: src/music_metadata_lib/infrastructure/apply_adapters.py; tests/test_apply_adapters.py

## Stub Commands

### RS-029 Rename stub

`rename` コマンドは現時点で未実装メッセージ `rename: not yet implemented` を出力する

- 条件: `rename` 実行時
- 補足: 実処理は持たない
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; tests/test_cli_common.py

### RS-030 Validate stub

`validate` コマンドは現時点で未実装メッセージ `validate: not yet implemented` を出力する

- 条件: `validate` 実行時
- 補足: 実処理は持たない
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; tests/test_cli_common.py

### RS-031 Config stub

`config` コマンドは現時点で未実装メッセージ `config: not yet implemented` を出力する

- 条件: `config` 実行時
- 補足: 実処理は持たない
- 状態: tested
- 根拠: src/music_metadata_tool/interface/cli/main.py; tests/test_cli_common.py

## Maintenance

更新手順:

1. `docs/reverse-spec/feature-inventory.csv` を更新する
2. `./bin/reverse-spec-md` で Markdown を再生成する
3. `./bin/reverse-spec-html` で HTML を再生成する
4. `./bin/test` で関連テストを確認する

## Placeholder Policy

`rename`, `validate`, `config` は現時点ではプレースホルダです。ヘルプには表示されますが、実処理は持たず `not yet implemented` を返します。

