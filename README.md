# 100knock-data-analytics

『Python実践データ分析100本ノック 第2版』の練習用リポジトリ

## Usage

朝練用のノートを起動する場合は

```bash
uv run marimo edit --headless --host 0.0.0.0 --no-token --watch notebooks/chp00.py
```

## Build Book

ノートを HTML Book 化する場合は

1. `uv run task export-html`
1. 必要な HTML ファイルを `site` 直下に配置する
1. `uv run task build-book`
