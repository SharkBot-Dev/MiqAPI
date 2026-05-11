from utility.miq import create_quote_image

from flask import Flask, request, send_file
import requests
import io

from urllib.parse import urlparse

import dotenv
import os

dotenv.load_dotenv()

USE_TOR = os.getenv('USE_TOR') == "1"

if USE_TOR:
    proxies = {
        'http': "socks5://127.0.0.1:9050",
        'https': "socks5://127.0.0.1:9050"
    }

app = Flask(__name__)

def hex_to_rgb(hex_code: str):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

@app.get('/')
def miqServer():
    args = request.args
    author = args.get('author', "Discord")
    text = args.get('text', "テストメッセージです")[:2000]
    avatar_url = args.get('avatar_url', "https://cdn.discordapp.com/embed/avatars/0.png")
    if USE_TOR:
        domain = urlparse(avatar_url).netloc
        if "cdn.discordapp.com" == domain:
            avatar = requests.get(avatar_url).content
        else:
            avatar = requests.get(avatar_url, proxies=proxies).content
    else:
        avatar = requests.get(avatar_url).content
    backgrond = hex_to_rgb(args.get('backgroud', "#000000"))
    textcolor = hex_to_rgb(args.get('textcolor', "#ffffff"))
    color = args.get('color', "True") == "True"
    negapoji = args.get('negapoji', "False") == "True"
    fake = args.get('fake', "False") == "True"
    image = create_quote_image(author, text, avatar, backgrond, textcolor, color, negapoji, fake, True)
    image_io = io.BytesIO()
    image.save(image_io, "png")
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')

@app.errorhandler(404)
def error_handler(e):
    return "そのパスは存在しません。"

@app.errorhandler(500)
def error_handler(e):
    print(f"Error: {e}")
    return "画像生成に失敗しました。"

if __name__ == '__main__':
    app.run("0.0.0.0", port=8002)