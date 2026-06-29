import sqlite3
import os

DATABASE_PATH = os.path.join("database", "pivotforge.db")


def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # =============================
    # Assets Table
    # =============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS assets(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        asset_name TEXT NOT NULL,

        ip_address TEXT NOT NULL,

        asset_type TEXT NOT NULL,

        criticality TEXT NOT NULL

    )

    """)

    # =============================
    # Vulnerabilities Table
    # =============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS vulnerabilities(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        asset_id INTEGER NOT NULL,

        cve_id TEXT NOT NULL,

        vulnerability_name TEXT NOT NULL,

        severity TEXT NOT NULL,

        description TEXT,

        FOREIGN KEY(asset_id)

        REFERENCES assets(id)

    )

    """)

    # =============================
    # Relationships Table
    # =============================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS relationships(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        source_asset INTEGER NOT NULL,

        destination_asset INTEGER NOT NULL,

        relationship_type TEXT NOT NULL,

        FOREIGN KEY(source_asset)

        REFERENCES assets(id),

        FOREIGN KEY(destination_asset)

        REFERENCES assets(id)

    )

    """)

    # =============================
    # Services Table
    # =============================

    cursor.execute("""

CREATE TABLE IF NOT EXISTS services(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_id INTEGER NOT NULL,

    port INTEGER NOT NULL,

    protocol TEXT NOT NULL,

    service_name TEXT NOT NULL,

    version TEXT,

    FOREIGN KEY(asset_id)

    REFERENCES assets(id)

)

""")
    # =============================
    # Audit Logs Table
    # =============================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    module TEXT NOT NULL,
    details TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

    connection.commit()

    connection.close()

print("Database Initialized Successfully")
def add_audit_log(action, module, details):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (action, module, details)
        VALUES (?, ?, ?)
    """, (action, module, details))

    connection.commit()
    connection.close()