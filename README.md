# MiqAPI
Make it a Quoteの生成API

# 自分でホストする方法
1. このレポジトリをローカルにクローンする
2. 以下のコマンドでライブラリを仮想環境にインストールする
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. 以下のコマンドで起動する
```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```