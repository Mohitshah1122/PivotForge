import sqlite3

DB = "database/pivotforge.db"

def add_log(action, module, details):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (action, module, details)
        VALUES (?, ?, ?)
    """, (action, module, details))

    conn.commit()
    conn.close()