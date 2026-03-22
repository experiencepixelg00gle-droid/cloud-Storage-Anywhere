import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

DB_FILE = "db.json"

# Load DB
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    import json
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Save DB
def save_db(data):
    import json
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Upload to Telegram
def upload_to_telegram(file, folder):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    caption = f"[{folder}] {file.filename}"
    
    files = {"document": file}
    data = {"chat_id": CHANNEL_ID, "caption": caption}
    
    res = requests.post(url, files=files, data=data)
    return res.json()

@app.route("/")
def home():
    return "My Cloud Running 🚀"

# Upload API
@app.route("/upload/<folder>", methods=["POST"])
def upload(folder):
    file = request.files['file']
    
    result = upload_to_telegram(file, folder)

    if not result.get("ok"):
        return result

    file_id = result["result"]["document"]["file_id"]

    db = load_db()
    if folder not in db:
        db[folder] = []

    db[folder].append({
        "name": file.filename,
        "file_id": file_id
    })

    save_db(db)

    return {"status": "uploaded", "folder": folder}

# List files
@app.route("/list/<folder>")
def list_files(folder):
    db = load_db()
    return jsonify(db.get(folder, []))

app.run(host="0.0.0.0", port=5000)
