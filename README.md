# 日本の人口推計データ分析アプリ

このアプリケーションは、e-Stat APIを使用して日本の人口推計データを取得し、視覚的に分析するStreamlitアプリケーションです。

## 機能

- e-Stat APIから人口推計データを取得
- 都道府県別、年齢層別、性別ごとのデータ分析
- 時系列での人口推移グラフ
- 地域間の人口比較
- 年齢層別の人口分布
- データのCSVダウンロード

## セットアップ

### 前提条件

- Python 3.8以上
- e-Stat API キー（[e-Stat](https://www.e-stat.go.jp/)から取得可能）

### インストール方法

1. リポジトリをクローン:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

3. `.env`ファイルを作成し、APIキーを設定:
```
ESTAT_API_KEY=your_api_key_here
```

### 実行方法

```bash
streamlit run main.py
```

ブラウザで`http://localhost:8501`を開くとアプリケーションにアクセスできます。

## Dockerでの実行

Dockerを使用して実行する場合:

```bash
# イメージのビルド
docker build -t estat-population-app .

# コンテナの実行
docker run -p 8501:8501 -v $(pwd):/app --env-file .env estat-population-app
```

または、docker-composeを使用:

```bash
docker-compose up
```

## 使い方

1. サイドバーから検索条件（統計データ、年範囲、都道府県、年齢層、性別）を選択
2. 「データを取得」ボタンをクリック
3. 取得したデータとグラフが表示されます
4. 必要に応じてCSVファイルとしてダウンロード可能

## 注意事項

- 現在のバージョンでは、APIから実際のデータを取得する代わりにサンプルデータを生成しています
- 実際のAPIデータを使用する場合は、`fetch_estat_data`関数のコメントを解除してください

## ライセンス

MIT

## 謝辞

- [e-Stat](https://www.e-stat.go.jp/) - 日本の政府統計ポータルサイト
- [Streamlit](https://streamlit.io/) - Pythonウェブアプリケーションフレームワーク
