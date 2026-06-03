from database.db import conn, cursor

cursor.execute("""
ALTER TABLE companies
ADD COLUMN sent_at TEXT
""")

conn.commit()

print("✅ Spalte sent_at erstellt")