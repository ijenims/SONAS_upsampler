# Context Log

## セッション概要

- 目的: 既存の `Streamlit` ベース実装を確認し、`HTML` ベースへの移植可否を判断・試作する。
- 結論: `core/*` の処理ロジックは UI 非依存のため、`FastAPI + HTML` への移植は可能。

## 実施内容（時系列）

### 1) 既存コード理解

- `app.py` を読み、処理フローを確認。
- 処理は以下の順で実行されることを確認:
  - CSVアップロード
  - `load_accel_xyz_from_csv()` でXYZ読込
  - `upsample_xyz_linear()` で 400Hz -> 1000Hz
  - `build_output_dataframe()` で出力整形
  - `build_output_filename()` で出力名生成
  - 可視化（入力/出力）とCSVダウンロード

### 2) HTML版の試作追加

- `webapp.py` を追加し、`FastAPI` エンドポイントを実装。
- `templates/index.html` を追加し、以下を実装:
  - CSVアップロードフォーム
  - 変換実行
  - 入力/出力グラフ表示（Plotly）
  - CSVダウンロード
  - 注意書き表示
- `requirements.txt` に `FastAPI` 系依存を追加:
  - `fastapi`
  - `uvicorn`
  - `jinja2`
  - `python-multipart`

### 3) 一時的なFastAPI一本化

- ユーザー要望により一度 `Streamlit` 版削除方針に変更。
- `app.py` を削除し、`README.md` を FastAPI 前提に更新。
- 変更履歴に日付付き記録（2026-04-24）を追加。

### 4) 方針修正（最終）

- ユーザー要望により「`Streamlit` 版は残す」方針へ再変更。
- `app.py` を復元。
- `requirements.txt` に `streamlit` を再追加。
- `run_web.bat` を追加（HTML版起動専用）。
- `README.md` を以下に更新:
  - Streamlit版とFastAPI版の共存運用を明記
  - 起動方法を併記
  - `.bat` はFastAPI版のみであることを明記
  - 変更履歴（2026-04-24）を反映

## 最終状態

- 両UIを利用可能:
  - `Streamlit`: `app.py`
  - `FastAPI + HTML`: `webapp.py` + `templates/index.html`
- HTML版起動用バッチ:
  - `run_web.bat`
- 依存関係:
  - `streamlit`, `pandas`, `numpy`, `plotly`, `fastapi`, `uvicorn`, `jinja2`, `python-multipart`

## 補足

- 実行環境上の制約で CLI からの `python` / `py` 実行確認が難しいタイミングがあったため、
  構文・静的チェックはエディタ診断中心で確認。
