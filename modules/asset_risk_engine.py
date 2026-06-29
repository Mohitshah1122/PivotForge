from modules.db import get_connection


class AssetRiskEngine:

    def calculate(self, asset_id):

        connection = get_connection()

        cursor = connection.cursor()

        score = 0

        # -------------------------
        # Asset Criticality
        # -------------------------

        cursor.execute(

            "SELECT criticality FROM assets WHERE id=?",

            (asset_id,)

        )

        asset = cursor.fetchone()

        if asset:

            criticality = asset["criticality"].lower()

            if criticality == "critical":
                score += 30

            elif criticality == "high":
                score += 25

            elif criticality == "medium":
                score += 15

            else:
                score += 5

        # -------------------------
        # Vulnerabilities
        # -------------------------

        cursor.execute(

            "SELECT severity FROM vulnerabilities WHERE asset_id=?",

            (asset_id,)

        )

        vulnerabilities = cursor.fetchall()

        for vulnerability in vulnerabilities:

            severity = vulnerability["severity"].lower()

            if severity == "critical":
                score += 10

            elif severity == "high":
                score += 7

            elif severity == "medium":
                score += 4

            else:
                score += 1

        # -------------------------
        # Services
        # -------------------------

        cursor.execute(

            "SELECT COUNT(*) AS total FROM services WHERE asset_id=?",

            (asset_id,)

        )

        service_count = cursor.fetchone()["total"]

        score += min(service_count, 5)

        # -------------------------
        # Relationships
        # -------------------------

        cursor.execute(

            """

            SELECT COUNT(*) AS total

            FROM relationships

            WHERE source_asset=?

            OR destination_asset=?

            """,

            (

                asset_id,

                asset_id

            )

        )

        relationship_count = cursor.fetchone()["total"]

        score += min(relationship_count, 5)

        connection.close()

        if score > 100:
            score = 100

        return score

    # ----------------------------------

    def get_level(self, score):

        if score <= 25:
            return "Low"

        elif score <= 50:
            return "Medium"

        elif score <= 75:
            return "High"

        else:
            return "Critical"