import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, disable_preview=True):
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": disable_preview,
        },
        timeout=10,
    )

@app.get("/")
def home():
    return "Bot is running", 200

@app.post("/webhook")
def webhook():
    data = request.get_json(silent=True) or {}

    message = data.get("message") or data.get("channel_post")
    if not message:
        return "OK", 200

    text = (message.get("text") or "").strip()
    chat_id = message.get("chat", {}).get("id")

    if not chat_id or not text:
        return "OK", 200

    if text.startswith("/start"):
        send_message(chat_id, "키워드를 입력하세요. 예: CHUC-106", True)
        return "OK", 200

    if text.startswith("/") or "http://" in text or "https://" in text:
        return "OK", 200

    keyword_upper = text.upper()
    keyword_lower = text.lower()

    search_url = f"https://missav.ws/ko/search/{keyword_upper}"
    detail_url = f"https://missav.ws/ko/{keyword_lower}-uncensored-leak"

    result = f"{search_url}\n\n{detail_url}"
    send_message(chat_id, result, True)

    return "OK", 200
