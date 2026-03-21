# music-metadata-tool

音楽ファイルのメタデータを一覧出力し、CSV/TSV から更新する CLI。

## 入力フォルダの設定（.env）

音楽ファイルの実フォルダは `.env` で指定します。

`scan_directory` にはコンテナ内のパスを書き、ホスト側の実パスは `.env` の `MUSIC_SOURCE_DIR` で指定します。

Windows の例:

```env
MUSIC_SOURCE_DIR=E:\iTunes\iTunes Media\Music
```

`.env` はプロジェクト直下に置きます。.env は Git 管理しません。公開用には [\.env.example](/mnt/e/script/music_metadata_tool/.env.example) を置いてあります。

必要に応じて `MUSIC_METADATA_LOG_PATH` も `.env` で設定できます。

## 設定ファイルの作成（config.json）

プロジェクト直下の `config.json` に対象パスと列設定を書きます。

まず [config.example.json](/mnt/e/script/music_metadata_tool/config.example.json) を `config.json` としてコピーして、必要なパスに書き換えます。

```json
{
  "scan_directory": "/workspace/music",
  "scan_output": "/workspace/storage/scan.tsv",
  "apply_input": "/workspace/storage/scan.tsv",
  "columns": [
    "file_path",
    "title",
    "artist",
    "album"
  ]
}
```

設定手順:

1. `config.example.json` を `config.json` としてコピーする
2. `scan_directory` を対象の音楽フォルダに合わせる
3. `scan_output` と `apply_input` を出力先ファイルに合わせる
4. 必要なら `columns` を調整する

設定項目:

- `scan_directory`: `scan` 対象ディレクトリ（コンテナ内パス）
- `scan_output`: `scan` 出力先
- `apply_input`: `apply` 入力ファイル
- `columns`: 出力列と更新対象列

注意点:

- `file_path` は必須
- 設定に含めない列は出力対象・更新対象から除外される
- 省略した列は `apply` 実行時に変更しない
- コマンドライン引数を渡した場合は、設定ファイルよりコマンドライン引数を優先する
- `.env` で `MUSIC_SOURCE_DIR` を設定した場合、通常 `scan_directory` は `/workspace/music` を使う

## 使い方

初回のみ、先にイメージを作成します。

```bash
docker compose build
```

その後は、通常この 2 コマンドを使います。

```bash
docker compose run --rm app music-metadata-tool scan
docker compose run --rm app music-metadata-tool apply --write
```

1. `config.json` を作成する
2. `docker compose build`
3. `scan` で TSV/CSV を出力する
4. Excel などで編集する
5. `apply --write` で書き戻す

## コマンド

### scan

指定ディレクトリ配下を再帰的に走査し、タグを CSV/TSV に出力します。

```bash
docker compose run --rm app music-metadata-tool scan
```

主な仕様:

- 対象拡張子: `.mp3`, `.flac`, `.wav`, `.aiff`, `.aif`, `.ogg`, `.m4a`
- 出力順: `file_path` 昇順
- `file_path` は絶対パスで出力
- 欠落タグは空文字で出力
- `scan_output` が `.tsv` なら TSV、それ以外は CSV
- `--output` を省略し、`scan_output` も未設定なら STDOUT に CSV 出力

出力ヘッダー:

```
file_path,format,title,artist,album,album_artist,track_number,disc_number,year,genre
```

設定を一時的に上書きしたい場合:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

### apply

編集済み CSV/TSV を読み込み、音楽ファイルへ書き戻します。

```bash
docker compose run --rm app music-metadata-tool apply --write
```

書き込み前に確認したい場合:

```bash
docker compose run --rm app music-metadata-tool apply
```

入力ファイルを一時的に上書きしたい場合:

```bash
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv --write
```

### CLI ヘルプ

```bash
docker compose run --rm app python -m music_metadata_tool.interface.cli.main --help
```

### ログファイル

CLI 実行ログは `storage/logs/cli.log` に追記されます（開始/終了/エラー/対象件数）。
出力先は環境変数 `MUSIC_METADATA_LOG_PATH` で変更できます。
