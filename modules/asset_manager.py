from modules.db import get_connection, add_audit_log


# ===========================
# GET ALL ASSETS
# ===========================
def get_all_assets():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM assets
        ORDER BY id DESC
    """)

    assets = cursor.fetchall()
    connection.close()

    return assets


# ===========================
# ADD NEW ASSET
# ===========================
def add_asset(
    asset_name,
    ip_address,
    asset_type,
    criticality
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO assets
        (
            asset_name,
            ip_address,
            asset_type,
            criticality
        )
        VALUES (?, ?, ?, ?)
    """,
    (
        asset_name,
        ip_address,
        asset_type,
        criticality
    ))

    connection.commit()
    connection.close()

    # ===========================
    # AUDIT LOG
    # ===========================
    add_audit_log(
        "CREATE",
        "ASSET",
        f"Asset added: {asset_name} ({ip_address})"
    )


# ===========================
# DELETE ASSET
# ===========================
def delete_asset(asset_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM assets WHERE id=?",
        (asset_id,)
    )

    connection.commit()
    connection.close()

    # ===========================
    # AUDIT LOG
    # ===========================
    add_audit_log(
        "DELETE",
        "ASSET",
        f"Asset deleted with ID: {asset_id}"
    )