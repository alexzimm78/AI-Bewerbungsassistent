import sqlite3

# Verbindung
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# Tabelle
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    skills TEXT,
    experience TEXT,
    address TEXT
)
""")

conn.commit()