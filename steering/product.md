# Product Context

**Project**: music-metadata-tool
**Last Updated**: 2025-12-15
**Version**: 1.0

---

## Product Vision

**Vision Statement**: ローカルにある大量の音楽ファイルのメタデータを一貫したルールで整理し、どの配信先やプレイヤーでも正しく表示される状態を最短時間で作れること。

**Mission**: CLI で完結するバルク編集ツールを提供し、タグの読み取り・検証・一括書き込み・CSV/TSV との往復を安全かつ再現性高く実行できるようにする。

---

## Product Overview

### What is music-metadata-tool?

music-metadata-tool は、MP3/FLAC/WAV などの音楽ファイルに対して、タグ読み取り・検証・一括更新・ファイル名整形を行う CLI ツールです。ローカルファイルを走査して現在のメタデータを CSV/TSV に書き出し、スプレッドシートで修正した結果をそのまま取り込み、同じルールでファイルに書き戻せます。

GUI への依存を避け、Git 管理や CI でも再現可能なスクリプトベースの運用を前提にしています。将来的には MusicBrainz/Discogs などのオンライン DB からの自動補完も追加し、マニュアル作業の削減を目指します。

### Problem Statement

**Problem**: 大量の音楽ファイルに分散したメタデータを手作業で揃えるのが煩雑で、プレイヤーや配信先ごとに表示崩れやタグ欠落が発生しやすい。

### Solution

**Solution**: ルールベースでバリデーションしながら CSV/TSV とタグを往復できる CLI を提供し、タグ編集・ファイル名整形・アルバムアート差し替えを一括で自動化する。プラグインでオンライン DB 補完を追加できる構造にする。

---

## Target Users

### Primary Users

#### User Persona 1: インディーズ/同人音楽制作者

**Demographics**:

- **Role**: 制作・配信担当を兼ねる個人
- **Organization Size**: 1-5 名
- **Technical Level**: CLI に抵抗はないがスクリプトは未経験

**Goals**:

- 配信前にタグとファイル名を一括で揃えたい
- 配信先ごとの差異に耐える正規化ルールを用意したい
- スプレッドシートで確認しながら安全に書き込みたい

**Pain Points**:

- GUI ツールだと履歴管理やバッチ処理が難しい
- タグ欠落やエンコード崩れを事前に検知できない
- ジャケット差し替えやトラック番号付与を毎回手作業で行っている

**Use Cases**:

- 新譜の一括タグ付けとファイル名整形
- 既存ライブラリの重複/欠落タグ検出と修正
- 配信先ごとの必須タグセットへの準拠チェック

---

#### User Persona 2: 配信運用/アーカイブ担当

**Demographics**:

- **Role**: カタログ運用・品質管理
- **Organization Size**: 10-50 名の小規模レーベル
- **Technical Level**: CLI/スクリプト利用可

**Goals**:

- 配信カタログのタグ品質を保ちたい
- スプレッドシート運用とファイルの実態を同期したい

**Pain Points**:

- ファイルと台帳の差分把握が手作業
- フォーマットごとのタグ差異を吸収できていない

**Use Cases**:

- 台帳更新後の差分タグ書き戻し
- 配信前チェックリストとしてのバリデーション出力

---

### Secondary Users

- **パワーユーザー**: ライブラリ整理や自動化を好む個人ユーザー
- **QA/サポート担当**: タグ品質検証とレポート作成を行う担当者

---

## Market & Business Context

### Market Opportunity

**Market Size**: ニッチ（個人制作者/小規模レーベル中心）

**Target Market**: GUI 依存からスクリプト化に移行したい音楽制作者・運用担当

MusicBrainz Picard や Mp3tag が GUI で強いが、再現性と CI 連携に強い CLI ツールは少ない。CSV/TSV 連携と検証レポートを強みに差別化する。

### Business Model

**Revenue Model**: OSS（無償）。将来的に商用サポート/プリセット提供を検討余地あり。

**Pricing Tiers** (if applicable):

- **Free Tier**: OSS コア機能（タグ入出力、バリデーション、ファイル名整形）
- **Pro/Enterprise**: 今は未設定

### Competitive Landscape

| Competitor              | Strengths                  | Weaknesses                    | Our Differentiation                      |
| ----------------------- | -------------------------- | ----------------------------- | ---------------------------------------- |
| MusicBrainz Picard      | 豊富なオンライン DB 連携    | GUI 前提、再現性のあるバッチが弱い | CLI/CSV ワークフローで再現性を担保      |
| Mp3tag                  | 直感的 GUI、Windows ユーザー多 | スクリプト連携が限定的            | CI でも動く Python ベースの CLI          |
| beets                   | プラグイン豊富、Python 製   | 設定学習コストが高い            | CSV/TSV を第一級に扱い、導入容易         |

---

## Core Product Capabilities

### Must-Have Features (MVP)

1. **タグ読み取りと CSV/TSV 出力**
   - **Description**: ディレクトリを走査し、主要タグとファイルパスを表形式で出力
   - **User Value**: 既存ライブラリの現状把握と編集の起点になる
   - **Priority**: P0 (Critical)

2. **CSV/TSV からのタグ書き戻し**
   - **Description**: 編集済み CSV/TSV をバリデーション後にファイルへ一括書き込み
   - **User Value**: スプレッドシートでの編集内容を安全に反映できる
   - **Priority**: P0 (Critical)

3. **ファイル名・ディレクトリ整形**
   - **Description**: タグに基づきファイル名/ディレクトリをリネームするテンプレート適用
   - **User Value**: 配信/再生環境での表示崩れを防ぎ、整理されたライブラリを保つ
   - **Priority**: P0 (Critical)

### High-Priority Features (Post-MVP)

4. **アルバムアート差し替え**
   - **Description**: 画像ファイルを指定して一括埋め込み・上書き
   - **User Value**: 配信前に統一解像度/ファイルサイズへ揃えられる
   - **Priority**: P1 (High)

5. **バリデーションレポート**
   - **Description**: 必須タグ欠落やエンコード問題をレポート出力
   - **User Value**: 出荷前チェックリストとして活用できる
   - **Priority**: P1 (High)

### Future Features (Roadmap)

6. **MusicBrainz/Discogs 連携**
   - **Description**: オンライン DB からタグ候補を取得し、マージオプションを提供
   - **User Value**: 手入力を削減し整合性を高める
   - **Priority**: P2 (Medium)

7. **プラグイン API**
   - **Description**: カスタムバリデーション/変換を外部モジュールとして追加可能にする
   - **User Value**: チーム固有の運用ルールを簡単に適用できる
   - **Priority**: P3 (Low)

---

## Product Principles

### Design Principles

1. **再現性優先**: 同じ入力に対し同じ出力が得られるバッチ実行を重視
2. **安全な書き込み**: バリデーションとドライランを必須パスに含め、破壊的変更を防ぐ
3. **拡張性**: フォーマット/タグ/変換ルールを後から追加しやすい構造にする

### User Experience Principles

1. **CLI で完結**: 必要なオプションは短い名前で、説明は `--help` で完備
2. **フェイルファスト**: 早期に入力エラーを示し、修正方法を明示
3. **可視化された差分**: 変更前後を表やサマリで確認できる出力を提供

---

## Success Metrics

### Key Performance Indicators (KPIs)

#### Business Metrics

| Metric                              | Target             | Measurement              |
| ----------------------------------- | ------------------ | ------------------------ |
| **Monthly Active Users (MAU)**      | 100 CLI 実行/月    | ダウンロード/実行数      |
| **Monthly Recurring Revenue (MRR)** | N/A (OSS)          | -                        |
| **Community Contribution**          | 3 PR/四半期        | GitHub PR 数             |

#### Product Metrics

| Metric                       | Target                | Measurement                |
| ---------------------------- | --------------------- | -------------------------- |
| **CLI 成功率**               | > 98%                 | 成功/失敗の実行ログ比率    |
| **バリデーション検出率**     | 必須欠落を 95% 以上検出 | テストデータでの検出率     |
| **処理時間**                 | 1,000 ファイルを 60s 以内 | ローカルベンチマーク       |

#### Technical Metrics

| Metric                      | Target               | Measurement                     |
| --------------------------- | -------------------- | ------------------------------- |
| **CLI 実行時間 (p95)**      | < 60s / 1,000 files  | ローカル計測                    |
| **メモリ使用量 (p95)**      | < 400MB              | ローカル計測                    |
| **エラー率**                | < 1%                 | テスト/実行ログ                 |

---

## Product Roadmap

### Phase 1: MVP (Months 1-3)

**Goal**: Launch minimum viable product

**Features**:

- タグ読み取り/CSV 出力
- CSV からのタグ書き戻し（ドライラン付き）
- ファイル名整形のテンプレート適用

**Success Criteria**:

- 主要タグ欠落の検出/報告が可能
- 1,000 ファイルを 1 分以内に処理

---

### Phase 2: Growth (Months 4-6)

**Goal**: Achieve product-market fit

**Features**:

- アルバムアート一括差し替え
- バリデーションレポート（CSV/HTML）
- プロファイル別の必須タグプリセット

**Success Criteria**:

- 配信前チェックの工数を 50% 削減
- テンプレート/プリセットの導入が 30 分以内で完了

---

### Phase 3: Scale (Months 7-12)

**Goal**: 外部連携と拡張性の拡大

**Features**:

- MusicBrainz/Discogs 連携
- プラグイン API
- CI 用の検証コマンドとレポート連携

**Success Criteria**:

- 自動補完で入力工数を 70% 削減
- コア機能のプラグイン化が可能

---

## User Workflows

### Primary Workflow 1: 既存ファイルのタグ抽出と編集

**User Goal**: ライブラリのタグを CSV/TSV で編集可能な形に出力する

**Steps**:

1. `scan` コマンドでディレクトリを走査
2. システムがタグを抽出し CSV/TSV を生成
3. ユーザーがスプレッドシートで編集
4. 編集結果を保存して次のワークフローで取り込む
5. 編集漏れがない状態で完了

**Success Criteria**:

- 1,000 ファイルでも 5 分以内に抽出完了
- 抽出結果に必須タグが含まれている

---

### Primary Workflow 2: CSV/TSV からタグ書き戻し

**User Goal**: 編集済み CSV/TSV を元にタグとファイル名を更新する

**Steps**:

1. `apply` コマンドで CSV/TSV を読み込み
2. システムがバリデーションし差分を表示（ドライラン）
3. `--write` オプションで実書き込みを実行

**Success Criteria**:

- ドライランで欠落/矛盾が検出される
- 書き込み後に再スキャンして差分ゼロを確認できる

---

## Business Domain

### Domain Concepts

Key concepts and terminology used in this domain:

1. **タグ (Metadata Tags)**: 曲情報（タイトル、アーティスト、アルバム、トラック番号、ジャンル、年など）
2. **カバーアート**: アルバムジャケット画像。解像度/サイズ制約に注意
3. **リネームテンプレート**: タグを元にファイル名/ディレクトリを生成する書式

### Business Rules

1. **必須タグ**: タイトル/アーティスト/アルバム/トラック番号/年は欠落不可
   - **Example**: トラック番号が欠落している場合はエラーとし、書き込みを拒否
2. **ファイル名テンプレート**: `<disc>-<track> <title>` のようにチームで合意した形式でリネーム
   - **Example**: `01-03 Song.mp3` など

---

## Constraints & Requirements

### Business Constraints

- **Budget**: OSS 前提のため金銭コストなし
- **Timeline**: MVP を 3 ヶ月以内に公開
- **Team Size**: 1-2 名
- **Launch Date**: 2026-Q1 目標

### Compliance Requirements

- **ライセンス**: OSS 依存ライブラリのライセンス適合（MIT/BSD/Apache を優先）
- **個人情報**: ローカルファイルのみを扱うためクラウド送信は行わない
- **Data Residency**: データはローカルのみ。オンライン API 連携時は明示的に opt-in

### Non-Functional Requirements

- **Performance**: 1,000 ファイルを 60 秒以内で処理
- **Availability**: CLI のため該当なし
- **Scalability**: ローカル環境で 10,000 ファイルまで安定処理
- **Security**: オンライン連携時は API トークンを平文保存しない
- **Portability**: Windows/macOS/Linux で動作

---

## Stakeholders

### Internal Stakeholders

| Role                    | Name         | Responsibilities                  |
| ----------------------- | ------------ | --------------------------------- |
| **Product Owner**       | （未定）     | Vision, roadmap, priorities       |
| **Tech Lead**           | （未定）     | Architecture, technical decisions |
| **Engineering Manager** | （未定）     | Team management, delivery         |
| **QA Lead**             | （未定）     | Quality assurance, testing        |
| **Design Lead**         | （不要/CLI） | CLI UX                            |

### External Stakeholders

| Role                        | Name        | Responsibilities            |
| --------------------------- | ----------- | --------------------------- |
| **Community Contributors**  | OSS ユーザー | Bug/feature feedback        |

---

## Go-to-Market Strategy

### Launch Strategy

**Target Launch Date**: 2026-Q1

**Launch Phases**:

1. **Private Beta** (2025-Q4)
   - 限定配布でフィードバック収集
   - Focus: 基本コマンドの安定化

2. **Public Beta** (2026-Q1)
   - OSS 公開
   - Focus: CSV/TSV ワークフローの検証

3. **General Availability** (2026-Q2)
   - プラグイン/オンライン補完を含む安定版
   - Focus: 拡張性と互換性

### Marketing Channels

- **GitHub**: OSS 公開とリリース管理
- **ブログ/技術記事**: 使い方とレシピの公開
- **SNS (X/Discord)**: ユーザーサポートとフィードバック収集

---

## Risk Assessment

### Product Risks

| Risk                                    | Probability | Impact | Mitigation                              |
| --------------------------------------- | ----------- | ------ | --------------------------------------- |
| 音楽フォーマット/タグ仕様の多様性        | Medium      | High   | 抽象化したタグモデルと拡張ポイントを用意 |
| CSV 編集時の人為ミス                    | High        | Medium | 厳格なバリデーションとドライランを実装   |
| オンライン DB 依存による API 変更       | Medium      | Medium | プラグイン化とバージョンピン             |

---

## Customer Support

### Support Channels

- **Issues**: GitHub Issues
- **Community**: Discord/Slack（検討）
- **Docs**: README とサンプルワークフロー

### Support SLA

| Tier              | Response Time | Resolution Time |
| ----------------- | ------------- | --------------- |
| **Critical (P0)** | ベストエフォート | ベストエフォート |
| **High (P1)**     | ベストエフォート | ベストエフォート |
| **Medium (P2)**   | ベストエフォート | ベストエフォート |
| **Low (P3)**      | ベストエフォート | ベストエフォート |

---

## Product Analytics

### Analytics Tools

- **CLI 実行ログ**: ローカルでの実行統計/失敗理由を収集（オプトイン）

### Events to Track

| Event               | Description                         | Purpose                   |
| ------------------- | ----------------------------------- | ------------------------- |
| `scan_completed`    | スキャン完了                         | パフォーマンス把握        |
| `validation_failed` | バリデーション失敗                   | 品質課題の傾向把握       |
| `apply_executed`    | タグ書き戻しの実行                   | 機能利用状況の把握       |

---

## Localization & Internationalization

### Supported Languages

- **Primary**: Japanese (ja-JP)
- **Secondary**: English (en-US) を順次整備

### Localization Strategy

- CLI メッセージの多言語対応（日本語/英語）
- 日付/数値表記はロケール依存箇所を限定
- ドキュメントは ja/En 併記を目指す

---

## Data & Privacy

### Data Collection

**What data we collect**:

- ローカルファイルのメタデータ（オフライン処理のみ）
- オプトイン時の実行ログ（匿名化）

**What data we DON'T collect**:

- パスワード/個人情報/音声コンテンツ本体の外部送信

### Privacy Policy

- ローカル処理を基本とし、オンライン連携時は明示的に opt-in
- ログ送信はデフォルトオフ、送信時は匿名化し保存期間を最小化

---

## Integrations

### Existing Integrations

| Integration       | Purpose                      | Priority |
| ----------------- | ---------------------------- | -------- |
| Mutagen           | オーディオタグ読み書き       | P0       |

### Planned Integrations

| Integration       | Purpose                      | Timeline |
| ----------------- | ---------------------------- | -------- |
| MusicBrainz API   | オンラインタグ補完           | 2026-Q2  |
| Discogs API       | オンラインタグ補完           | 2026-Q3  |

---

## Changelog

### Version 1.1 (Planned)

- バリデーションレポート強化とオンライン補完追加

---

**Last Updated**: 2025-12-15
**Maintained By**: コアチーム（未定）
