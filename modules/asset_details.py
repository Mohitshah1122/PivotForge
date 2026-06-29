from modules.db import get_connection
from modules.asset_risk_engine import AssetRiskEngine

class AssetDetails:

    def get_asset(self, asset_id):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT *

        FROM assets

        WHERE id=?

        """,

        (asset_id,))

        asset = cursor.fetchone()

        connection.close()

        return asset


    def get_services(self, asset_id):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT *

        FROM services

        WHERE asset_id=?

        ORDER BY port

        """,

        (asset_id,))

        data = cursor.fetchall()

        connection.close()

        return data


    def get_vulnerabilities(self, asset_id):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT *

        FROM vulnerabilities

        WHERE asset_id=?

        """,

        (asset_id,))

        data = cursor.fetchall()

        connection.close()

        return data


    def get_relationships(self, asset_id):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            r.*,

            a.asset_name

        FROM relationships r

        JOIN assets a

        ON a.id=r.destination_asset

        WHERE r.source_asset=?

        """,

        

        (asset_id,))

        data = cursor.fetchall()

        connection.close()

        return data
        # =====================================
    # Asset Risk
    # =====================================

    def get_risk(self, asset_id):

        engine = AssetRiskEngine()

        score = engine.calculate(asset_id)

        level = engine.get_level(score)

        return {

            "score": score,

            "level": level

        }