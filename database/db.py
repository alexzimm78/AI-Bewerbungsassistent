import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


# users Tabelle
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    skills TEXT,
    experience TEXT,
    address TEXT
)
""")

conn.commit()


# applications Tabelle
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    email TEXT,
    bewerbung_typ TEXT,
    sent_at TEXT
)
""")

conn.commit()

# companies Tabelle
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    email TEXT,
    status TEXT
)
""")

conn.commit()

# interviews Tabelle
cursor.execute("""
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    company TEXT,
    interview_date TEXT,
    note TEXT
)
""")

conn.commit()