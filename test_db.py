from modules.db import get_connection

connection = get_connection()

cursor = connection.cursor()

print("========== ASSETS ==========")

cursor.execute("SELECT * FROM assets")

for row in cursor.fetchall():
    print(dict(row))

print("\n========== SERVICES ==========")

cursor.execute("SELECT * FROM services")

for row in cursor.fetchall():
    print(dict(row))

print("\n========== VULNERABILITIES ==========")

cursor.execute("SELECT * FROM vulnerabilities")

for row in cursor.fetchall():
    print(dict(row))

print("\n========== RELATIONSHIPS ==========")

cursor.execute("SELECT * FROM relationships")

for row in cursor.fetchall():
    print(dict(row))

connection.close()