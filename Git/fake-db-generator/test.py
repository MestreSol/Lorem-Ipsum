import sqlite3
def read_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"Table: {table[1]}")
        cursor.execute(f"SELECT * FROM {table[1]}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
