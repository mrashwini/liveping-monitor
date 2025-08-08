import requests
import time
import sqlite3
from datetime import datetime, timezone

# SQLite DB file
DB_FILE = "uptime.db"

# Log file
LOG_FILE = "uptime_log.txt"

# URLs to monitor
URLS = [
    "https://www.google.com",
    "https://www.github.com",
    "https://nonexistent.example.com"
]

# ✅ Initialize SQLite DB
def init_db():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response_time REAL,
                    timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("✅ Database initialized.")
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")

# ✅ Log to SQLite
def log_to_db(url, status, response_time):
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO logs (url, status, response_time, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (url, status, response_time, timestamp))
            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Failed to log to DB: {e}")

# ✅ Log to text file
def log_to_file(url, status, response_time):
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} | {url} | {status} | {response_time}ms\n")
    except Exception as e:
        print(f"❌ Failed to write to log file: {e}")

# ✅ Check single URL
def check_url(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        duration = round((time.time() - start) * 1000, 2)
        status = "UP" if response.status_code == 200 else f"DOWN ({response.status_code})"
    except requests.RequestException as e:
        status = f"DOWN ({str(e)})"
        duration = -1

    print(f"{url} - {status} - {duration}ms")
    log_to_db(url, status, duration)
    log_to_file(url, status, duration)

# ✅ Query and print logs
def show_logs(limit=10):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute('''
                SELECT timestamp, url, status, response_time
                FROM logs
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            rows = c.fetchall()

        print(f"\n📊 Last {limit} Logs:")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}ms")
    except sqlite3.Error as e:
        print(f"❌ Failed to fetch logs: {e}")

# ✅ Main loop
if __name__ == "__main__":
    init_db()
    try:
        while True:
            for url in URLS:
                check_url(url)
            show_logs(limit=5)
            time.sleep(60)  # Wait 60 seconds before next round
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
