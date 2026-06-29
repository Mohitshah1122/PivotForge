import sqlite3
from modules.db import add_audit_log


DATABASE = "database/pivotforge.db"


def load_demo_data():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # ===================================================
    # Clear Existing Data
    # ===================================================

    cursor.execute("DELETE FROM relationships")
    cursor.execute("DELETE FROM vulnerabilities")
    cursor.execute("DELETE FROM assets")

# RESET AUTO INCREMENT COUNTERS
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='relationships'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='vulnerabilities'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='assets'")
    conn.commit()

    add_audit_log(
        "RESET",
        "DEMO_DATA",
        "Existing enterprise data cleared"
    )

    # ===================================================
    # Assets
    # ===================================================

    assets = [

        ("Internet", "0.0.0.0", "External", "Low"),
        ("Firewall", "192.168.1.1", "Security Device", "High"),
        ("VPN Gateway", "192.168.1.2", "Security Device", "High"),
        ("Web Server", "192.168.1.10", "Server", "High"),
        ("Application Server", "192.168.1.20", "Server", "High"),
        ("Database Server", "192.168.1.30", "Database", "Critical"),
        ("Domain Controller", "192.168.1.40", "Identity Server", "Critical"),
        ("File Server", "192.168.1.50", "File Server", "Medium"),
        ("Administrator Workstation", "192.168.1.60", "Workstation", "High"),
        ("Employee Workstation", "192.168.1.70", "Workstation", "Medium")

    ]

    cursor.executemany("""

        INSERT INTO assets
        (
            asset_name,
            ip_address,
            asset_type,
            criticality
        )
        VALUES (?, ?, ?, ?)

    """, assets)

    conn.commit()

    add_audit_log(
        "IMPORT",
        "DEMO_DATA",
        "10 enterprise assets inserted"
    )

    # ===================================================
    # Asset IDs Mapping
    # ===================================================

    cursor.execute("SELECT id, asset_name FROM assets")
    rows = cursor.fetchall()

    asset_map = {row[1]: row[0] for row in rows}

    # ===================================================
    # Vulnerabilities
    # ===================================================

    vulnerabilities = [

        (asset_map["Web Server"], "CVE-2025-1001", "Apache RCE", "Critical", "Remote Code Execution vulnerability."),
        (asset_map["VPN Gateway"], "CVE-2025-1002", "VPN Bypass", "Critical", "Authentication bypass."),
        (asset_map["Database Server"], "CVE-2025-1003", "SQL Injection", "High", "SQL Injection vulnerability."),
        (asset_map["Domain Controller"], "CVE-2025-1004", "Kerberos Escalation", "Critical", "Privilege escalation."),
        (asset_map["Employee Workstation"], "CVE-2025-1005", "Browser RCE", "Medium", "Browser vulnerability.")

    ]

    cursor.executemany("""

        INSERT INTO vulnerabilities
        (
            asset_id,
            cve_id,
            vulnerability_name,
            severity,
            description
        )
        VALUES (?, ?, ?, ?, ?)

    """, vulnerabilities)

    conn.commit()

    add_audit_log(
        "IMPORT",
        "DEMO_DATA",
        "5 vulnerabilities inserted"
    )

    # ===================================================
    # Relationships
    # ===================================================

    relationships = [

        (asset_map["Internet"], asset_map["Firewall"], "Network"),
        (asset_map["Firewall"], asset_map["VPN Gateway"], "Network"),
        (asset_map["Firewall"], asset_map["Web Server"], "Network"),
        (asset_map["VPN Gateway"], asset_map["Application Server"], "Trust"),
        (asset_map["Web Server"], asset_map["Application Server"], "Network"),
        (asset_map["Application Server"], asset_map["Database Server"], "Database Connection"),
        (asset_map["Application Server"], asset_map["Domain Controller"], "Trust"),
        (asset_map["Domain Controller"], asset_map["File Server"], "Trust"),
        (asset_map["Administrator Workstation"], asset_map["Domain Controller"], "Admin Access"),
        (asset_map["Employee Workstation"], asset_map["Web Server"], "Network")

    ]

    cursor.executemany("""

        INSERT INTO relationships
        (
            source_asset,
            destination_asset,
            relationship_type
        )
        VALUES (?, ?, ?)

    """, relationships)

    conn.commit()

    add_audit_log(
        "IMPORT",
        "DEMO_DATA",
        "10 relationships inserted"
    )

    # ===================================================
    # FINAL LOG
    # ===================================================

    add_audit_log(
        "IMPORT",
        "DEMO_DATA",
        "Enterprise demo dataset fully loaded"
    )

    conn.close()

    print("Demo Enterprise Data Loaded Successfully")