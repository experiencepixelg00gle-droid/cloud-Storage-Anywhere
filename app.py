import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

@app.route("/")
def home():
    return "Server chal raha hai 🚀"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    files = {"document": file}
    data = {"chat_id": CHANNEL_ID}

    res = requests.post(url, files=files, data=data)
    return res.text

app.run(host="0.0.0.0", port=5000)
