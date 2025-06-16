# AI News App

## 概要

このプロジェクトは、AI関連のニュースを自動で収集し、ウェブページに表示するアプリケーションです。1週間の期間で、Webアプリケーション開発の基本的な流れ（データベース設計、バックエンド、フロントエンド、スクレイピング、AI機能の実装）を学ぶために作成しました。

## 主な機能

* **ニュース記事の自動収集:** 指定したニュースサイトからWebスクレイピングで定期的に記事情報を取得し、データベースに保存します。
* **記事一覧表示:** 収集した記事を時系列で一覧表示します。
* **ページネーション:** 記事が多数になっても見やすいように、ページ送り機能を実装しています。
* **検索機能:** キーワードで記事のタイトルや概要を検索できます。
* **AIによる関連記事推薦:** 記事詳細ページで、AI（TF-IDFとコサイン類似度）を使って内容が似ている他の記事を推薦します。
* **管理者サイト:** Djangoの管理サイトから直接データを管理できます。

## 使用技術

* **バックエンド:** Python, Django
* **データベース:** PostgreSQL
* **Webスクレイピング:** Requests, BeautifulSoup4
* **AI・機械学習:** Scikit-learn
* **その他:** python-dotenv, python-dateutil, Conda, Git, GitHub

## セットアップと実行方法（ローカル開発環境）

1.  **リポジトリのクローン:**
    ```bash
    git clone [https://github.com/Ogawatatsuya41/ai_news_app.git](https://github.com/Ogawatatsuya41/ai_news_app.git)
    cd ai_news_app
    ```

2.  **Conda環境の構築:**
    `environment.yml` からConda環境を構築します。（もし `requirements.txt` を使っている場合は、その旨を記述）
    ```bash
    conda env create -f environment.yml
    conda activate ai_news_env 
    ```

3.  **データベースのセットアップ:**
    PostgreSQLで、アプリケーション用のデータベースとユーザーを作成します。
    ```sql
    CREATE DATABASE ai_news_db;
    CREATE USER ai_news_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE ai_news_db TO ai_news_user;
    ```

4.  **.envファイルの作成:**
    プロジェクトルートに `.env` ファイルを作成し、データベースのパスワードを設定します。
    ```
    DB_PASSWORD="your_password"
    ```

5.  **データベースマイグレーション:**
    ```bash
    python manage.py migrate
    ```

6.  **管理者ユーザーの作成:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **初期データの投入:**
    まずニュース記事を収集し、次に関連記事の類似度データを計算します。
    ```bash
    python manage.py scrape_news
    python manage.py build_similarity
    ```

8.  **開発サーバーの起動:**
    ```bash
    python manage.py runserver
    ```
    ブラウザで `http://127.0.0.1:8000/news/` にアクセスしてください。