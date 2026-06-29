from modules.db import get_connection


class SearchManager:

    def search(self, keyword):

        connection = get_connection()

        cursor = connection.cursor()

        like = f"%{keyword}%"

        # Assets
        cursor.execute("""

        SELECT *

        FROM assets

        WHERE

        asset_name LIKE ?

        OR ip_address LIKE ?

        OR asset_type LIKE ?

        """,

        (like, like, like))

        assets = cursor.fetchall()

        # Vulnerabilities
        cursor.execute("""

        SELECT *

        FROM vulnerabilities

        WHERE

        cve_id LIKE ?

        OR vulnerability_name LIKE ?

        OR severity LIKE ?

        """,

        (like, like, like))

        vulnerabilities = cursor.fetchall()

        # Services
        cursor.execute("""

        SELECT *

        FROM services

        WHERE

        service_name LIKE ?

        OR protocol LIKE ?

        OR version LIKE ?

        """,

        (like, like, like))

        services = cursor.fetchall()

        connection.close()

        return {

            "assets": assets,

            "vulnerabilities": vulnerabilities,

            "services": services

        }