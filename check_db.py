import sqlite3
conn = sqlite3.connect("fashion.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print("Tables:", tables)
for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"  {t}: {cursor.fetchone()[0]} rows")
conn.close()
