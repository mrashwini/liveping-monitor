import os
import json
import time
import requests

# Load config
if os.getenv("GITHUB_ACTIONS"):  # running in GitHub Actions
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
else:  # running locally
    with open("config.json", "r") as f:
        config = json.load(f)
    TELEGRAM_BOT_TOKEN = config.get("telegram_bot_token")
    TELEGRAM_CHAT_ID = config.get("telegram_chat_id")

# Websites to monitor
SITES = [
    "https://google.com",
    "https://github.com",
    "https://youtube.com"
]

# Track status to only alert on changes
status_history = {site: True for site in SITES}  # Assume UP initially

def send_telegram_message(message):
    """Send a message to Telegram Bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def check_sites():
    """Check each site and send alert if status changes."""
    global status_history
    for site in SITES:
        try:
            r = requests.get(site, timeout=5)
            is_up = r.status_code == 200
        except requests.RequestException:
            is_up = False

        # Detect change in status
        if is_up != status_history[site]:
            status_history[site] = is_up
            if is_up:
                send_telegram_message(f"✅ {site} is back UP!")
            else:
                send_telegram_message(f"⚠️ {site} is DOWN!")

        print(f"{site} - {'UP' if is_up else 'DOWN'}")

if __name__ == "__main__":
    while True:
        check_sites()
        time.sleep(60)  # check every minute
