from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/logs")
def get_logs(limit: int = 20):
    conn = sqlite3.connect("uptime.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT url, status, response_time, timestamp
        FROM logs
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {"url": row[0], "status": row[1], "response_time": row[2], "timestamp": row[3]}
        for row in rows
    ]
