# music-metadata-tool

音楽ファイルのメタデータを一覧出力し、CSV/TSV から更新する CLI。

## 概要

- scan: 指定ディレクトリ配下を再帰的に走査し、タグを CSV/TSV に出力
- apply: CSV/TSV を読み込み、タグ更新（`--write` で書き込み）

## Docker での実行

前提: Docker と Docker Compose が利用できること。

### ビルド

```bash
docker compose build
```

### コンテナ起動（開発用）

```bash
docker compose run --rm app
```

`/workspace/music` には既定でリポジトリ内の `./music` をマウントします。別の音楽フォルダを使う場合は、実行前に `MUSIC_SOURCE_DIR` を指定します。

```bash
MUSIC_SOURCE_DIR=/absolute/path/to/music docker compose run --rm app
```

ローカル固定で使う場合は、プロジェクト直下に `.env` を置いて `MUSIC_SOURCE_DIR` を設定します。`.env` は Git 管理しません。公開用には [\.env.example](/mnt/e/script/music_metadata_tool/.env.example) を置いてあります。

`.env` では必要に応じて `MUSIC_METADATA_LOG_PATH` も設定できます。

### テスト実行

```bash
docker compose run --rm app python -m pytest -q
```

### CLI ヘルプ

```bash
docker compose run --rm app python -m music_metadata_tool.interface.cli.main --help
```

### scan（基本）

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

### scan の詳細

`scan` は指定ディレクトリ配下を再帰的に走査し、音楽ファイルのタグを CSV/TSV に出力します。

主なポイント:

- 対象拡張子: `.mp3`, `.flac`, `.wav`, `.aiff`, `.aif`, `.ogg`, `.m4a`
- 出力順: `file_path` 昇順（再現性のため固定）
- 出力パス:
  - `--output` 省略時は STDOUT に CSV を出力
  - `.tsv` 拡張子なら TSV、その他は CSV
- `file_path` は絶対パスで出力
- 欠落タグは空文字として出力

ヘッダーは次の順序で出力されます。

```
file_path,format,title,artist,album,album_artist,track_number,disc_number,year,genre
```

### 設定ファイル（列の表示・順序）

プロジェクト直下の `config.json` で出力列の表示/順序を変更できます。
`apply` も同じ設定に従い、設定に含まれる列のみを更新対象とします。

公開用リポジトリには [config.example.json](/mnt/e/script/music_metadata_tool/config.example.json) を置いてあります。必要に応じてこれを `config.json` としてコピーして使います。

```json
{
  "columns": [
    "file_path",
    "title",
    "artist",
    "album"
  ]
}
```

注意点:

- `file_path` は必須
- 設定に含めない列は出力/更新対象から除外される
  - 省略した列は `apply` 実行時に変更しない

STDOUT へ出力する例:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music > /workspace/storage/scan.csv
```

TSV で出力する例:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

サブディレクトリだけを対象にする例:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music/albums --output /workspace/storage/albums.tsv
```

参照フォルダを変える方法（PowerShell 例）:

```powershell
$env:MUSIC_SOURCE_DIR="E:\music\albums"
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

ホスト側の任意パスに保存したい場合（Windows PowerShell）:

```powershell
docker compose run --rm app music-metadata-tool scan /workspace/storage > E:\script\music_metadata_tool\scan.csv
```

出力結果を確認する例（先頭 5 行）:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/storage | head -n 5
```

### apply（ドライラン）

```bash
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv
```

### apply（書き込み）

```bash
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv --write
```

### ログファイル

CLI 実行ログは `storage/logs/cli.log` に追記されます（開始/終了/エラー/対象件数）。  
出力先は環境変数 `MUSIC_METADATA_LOG_PATH` で変更できます。

## 開発・検証方針

- Python 実行、テスト、CLI 検証は Docker コンテナ内で行う
- ホスト側の Python 環境には依存しない
- テストの標準コマンドは `docker compose run --rm app python -m pytest -q`

## リバース仕様書

既存実装から逆生成した利用者向け仕様は `docs/reverse-spec/` に配置しています。

- 一次ソース: [docs/reverse-spec/feature-inventory.csv](/mnt/e/script/music_metadata_tool/docs/reverse-spec/feature-inventory.csv)
- 利用者向け文書: [docs/reverse-spec/user-spec.md](/mnt/e/script/music_metadata_tool/docs/reverse-spec/user-spec.md)
- HTML 版: `docs/reverse-spec/user-spec.html` を必要時にローカル生成

更新手順:

1. `docs/reverse-spec/feature-inventory.csv` を更新する
2. `./bin/reverse-spec-md` で Markdown を再生成する
3. `./bin/reverse-spec-html` で HTML を再生成する
4. `./bin/test` でテストを確認する

Markdown を再生成する場合:

```bash
./bin/reverse-spec-md
```

HTML を再生成する場合:

```bash
./bin/reverse-spec-html
```

## 未実装コマンド

- `rename`
- `validate`
- `config`

これらは現時点ではプレースホルダです。ヘルプには表示されますが、実処理は持たず `not yet implemented` を返します。

ソースは `.` を `/workspace` にマウントしているため、ホストの変更がコンテナに反映されます。
