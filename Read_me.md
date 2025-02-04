# Django To-Do List App 📝

このプロジェクトは Django を使用したシンプルな To-Do リストアプリです。  
ユーザーはタスクを追加、編集、削除、完了マークすることができます。

## 🚀 機能
- タスクの追加 ✍️
- タスクの編集 ✏️
- タスクの削除 🗑️
- タスクの完了マーク ✅
- データベースに保存 🗄️
- Django Admin でタスク管理 📊

- コミットするときは✍️ (編集内容）みたいな感じでいこう

## 🛠️ 使用技術
- Python 3.x
- Django 4.x
- SQLite3（デフォルトのDB）
- HTML, CSS (Bootstrap)
- JavaScript (オプション)

## 📦 インストール方法

1. **リポジトリをクローン**
    ```sh
    git clone https://github.com/your-username/todolist.git
    cd todolist
    ```
2. **仮想環境を作成 & 有効化**
    ```sh
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **依存関係をインストール**
    ```sh
    pip install -r requirements.txt
    ```
4. **マイグレーションを実行**
    ```sh
    python manage.py migrate
    ```
5. **管理ユーザーを作成 (オプション)**
    ```sh
    python manage.py createsuperuser
    ```
6. **サーバーを起動**
    ```sh
    python manage.py runserver
    ```
    サーバーが起動したら、ブラウザで以下の URL にアクセスしてください：
    ```
    http://127.0.0.1:8000/
    ```

## 📂 プロジェクト構成

- [wiki]https://github.com/Takasin0141/To_Do_list/wiki)


## 📝 使い方
1. **新しいタスクを追加**
2. **タスクを編集 / 削除**
3. **完了したタスクにチェック**
4. **Django Admin で管理** (`/admin/` にアクセス)

## 🎯 今後の改善予定
- ユーザー認証（ログイン / ログアウト）
- タスクの優先度設定
- モバイル対応 UI

## 🛠️ 開発者向け情報
**デバッグモードで実行**
```sh
python manage.py runserver --settings=todolist.settings_dev
