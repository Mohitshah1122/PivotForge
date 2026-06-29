from modules.db import get_connection, add_audit_log


# ======================================
# ADD RELATIONSHIP
# ======================================
def add_relationship(
    source_asset,
    destination_asset,
    relationship_type
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO relationships(
        source_asset,
        destination_asset,
        relationship_type
    )
    VALUES(?,?,?)
    """,
    (
        source_asset,
        destination_asset,
        relationship_type
    ))

    connection.commit()
    connection.close()

    # ============================
    # AUDIT LOG
    # ============================
    add_audit_log(
        "CREATE",
        "RELATIONSHIP",
        f"Relationship created: {source_asset} → {destination_asset} ({relationship_type})"
    )


# ======================================
# GET ALL RELATIONSHIPS
# ======================================
def get_all_relationships():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        r.id,
        a1.asset_name AS source_name,
        a2.asset_name AS destination_name,
        r.relationship_type
    FROM relationships r
    JOIN assets a1
        ON r.source_asset = a1.id
    JOIN assets a2
        ON r.destination_asset = a2.id
    ORDER BY r.id DESC
    """)

    data = cursor.fetchall()
    connection.close()

    return data


# ======================================
# DELETE RELATIONSHIP
# ======================================
def delete_relationship(relationship_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM relationships WHERE id=?",
        (relationship_id,)
    )

    connection.commit()
    connection.close()

    # ============================
    # AUDIT LOG
    # ============================
    add_audit_log(
        "DELETE",
        "RELATIONSHIP",
        f"Relationship deleted ID {relationship_id}"
    )