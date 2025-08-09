import requests
import time
import json

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

INTERVAL = config.get("interval_seconds", 60)
URLS = config.get("urls", [])

# Telegram Bot Config
BOT_TOKEN = "8211506382:AAFCaiER16SAA_QTPKhDIeHP0kgdPeG3UjA"
CHAT_ID = "5792094086"

# Store previous status
status_map = {url: None for url in URLS}


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Error sending Telegram message:", e)


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def monitor():
    while True:
        for url in URLS:
            is_up = check_site(url)
            prev_status = status_map[url]

            if prev_status is None:
                status_map[url] = is_up
                continue

            if prev_status and not is_up:
                send_telegram_message(f"🚨 *ALERT*: {url} is DOWN!")

            if not prev_status and is_up:
                send_telegram_message(f"✅ *RECOVERED*: {url} is back UP!")

            status_map[url] = is_up

        time.sleep(INTERVAL)


if __name__ == "__main__":
    monitor()
