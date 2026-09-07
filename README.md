# music-metadata-tool

音楽ファイルのメタデータをCSV／TSVへ一覧出力し、編集した内容を同じファイルへ書き戻すCLIです。CSV自体の編集機能は含みません。

## 先に確認すること

`apply --write` は音楽ファイルをその場で更新します。自動バックアップ、ロールバック、全行を一括で取り消すtransactionはありません。途中の行で失敗した場合、それ以前の更新が残ることがあります。最初はバックアップした小さなコピーで試し、`--write` なしの検証を通してから本番データへ適用してください。

`--write` なしの `apply` は入力形式と対象pathを検証しますが、変更差分のpreviewは表示しません。空のセルは対応するtagを消去する指定です。

## 入力フォルダの設定（`.env`）

ホスト側の音楽フォルダを `.env` の `MUSIC_SOURCE_DIR` で指定し、`config.json` ではDockerコンテナ内のmount先を使います。

Windowsの例:

```env
MUSIC_SOURCE_DIR=E:\iTunes\iTunes Media\Music
```

`.env` はプロジェクト直下に置き、Gitへ登録しません。雛形は [`.env.example`](.env.example) です。必要に応じて `MUSIC_METADATA_LOG_PATH` も設定できます。

`scan` が出力する `file_path` はコンテナ内の絶対pathです。後で `apply` するときも同じホストフォルダを同じ `/workspace/music` へmountしてください。別のmount先で実行すると、CSV／TSV内のpathから元ファイルを見つけられません。

## 設定ファイルの作成（`config.json`）

プロジェクト直下に [`config.example.json`](config.example.json) を `config.json` としてコピーし、必要なpathと列へ変更します。

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

設定項目:

- `scan_directory`: `scan` 対象ディレクトリ（コンテナ内path）
- `scan_output`: `scan` 出力先。`.tsv` ならTSV、それ以外はCSV
- `apply_input`: `apply` 入力ファイル
- `columns`: 出力列と更新対象列。`file_path` は必須

`columns` を設定すると、その列と順序が `scan` 出力および `apply` 対象になります。設定に含めないtag列は出力せず、更新もしません。`columns` を設定しない場合の既定列は次の10列です。

```text
file_path,format,title,artist,album,album_artist,track_number,disc_number,year,genre
```

`file_path` は対象を特定する列、`format` はscan専用です。更新できる列は `title`、`artist`、`album`、`album_artist`、`track_number`、`disc_number`、`year`、`genre` です。コマンドライン引数は設定ファイルより優先されます。

## 基本的な使い方

初回にイメージを作成します。

```bash
docker compose build
```

1. `config.json` と `.env` を作成する
2. `scan` でCSV／TSVを出力する
3. Excelなどで編集し、`file_path` を変えない
4. `--write` なしで入力と対象pathを検証する
5. バックアップを確認してから `--write` で更新する

```bash
docker compose run --rm app music-metadata-tool scan
docker compose run --rm app music-metadata-tool apply
docker compose run --rm app music-metadata-tool apply --write
```

### `scan`

指定ディレクトリ配下を再帰的に走査し、tagをCSV／TSVへ出力します。

- 対象拡張子: `.mp3`, `.flac`, `.wav`, `.aiff`, `.aif`, `.ogg`, `.m4a`
- 出力順: `file_path` 昇順
- 欠落tag: 空文字
- `--output` と `scan_output` の両方を省略: STDOUTへCSV出力

設定を一時的に上書きする例:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

### `apply`

入力ファイルを一時的に上書きする例:

```bash
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv --write
```

### CLIヘルプ

```bash
docker compose run --rm app python -m music_metadata_tool.interface.cli.main --help
```

## ログ

CLI実行ログは既定で `storage/logs/cli.log` に追記されます。出力先は環境変数 `MUSIC_METADATA_LOG_PATH` で変更できます。
