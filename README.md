# music-metadata-tool

音楽ファイルのメタデータを一覧出力・CSV から更新するための CLI（雛形）。

## Docker での環境構築

前提: Docker と Docker Compose が利用できること。

### ビルド

```bash
docker compose build
```

### コンテナ起動（開発用）

```bash
docker compose run --rm app
```

### 例: テスト実行

```bash
docker compose run --rm app pytest -q
```

### 例: CLI 起動

```bash
docker compose run --rm app python -m music_metadata_tool.interface.cli.main --help
```

### 例: scan 実行（基本）

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

### scan 実行の詳細

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

STDOUT へ出力する例（`scan.tsv` を作らず、画面に出す）:

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

Windows の音楽フォルダを読む例:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

参照フォルダを変える方法（PowerShell 例）:

```powershell
docker compose run --rm `
  -v E:\music\albums:/workspace/music `
  app music-metadata-tool scan /workspace/music --output /workspace/storage/scan.tsv
```

ホスト側の任意パスに保存したい場合（Windows PowerShell）:

```powershell
docker compose run --rm app music-metadata-tool scan /workspace/storage > E:\script\music_metadata_tool\scan.csv
```

出力結果を確認する例（先頭 5 行）:

```bash
docker compose run --rm app music-metadata-tool scan /workspace/storage | head -n 5
```

### 例: apply 実行（ドライラン）

```bash
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv
```

### 例: apply 実行（書き込み）

```bash
docker compose run --rm app music-metadata-tool apply /workspace/storage/scan.tsv --write
```

### ログファイル

CLI 実行ログは `storage/logs/cli.log` に追記されます（開始/終了/エラー/対象件数）。  
出力先は環境変数 `MUSIC_METADATA_LOG_PATH` で変更できます。

ソースは `.` を `/workspace` にマウントしているため、ホストの変更がコンテナに反映されます。
