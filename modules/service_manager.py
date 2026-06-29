from modules.db import get_connection


# =====================================
# ADD SERVICE
# =====================================

def add_service(

    asset_id,

    port,

    protocol,

    service_name,

    version

):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    INSERT INTO services(

        asset_id,

        port,

        protocol,

        service_name,

        version

    )

    VALUES(?,?,?,?,?)

    """,

    (

        asset_id,

        port,

        protocol,

        service_name,

        version

    )

    )

    connection.commit()

    connection.close()


# =====================================
# GET ALL SERVICES
# =====================================

def get_all_services():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    SELECT

        services.*,

        assets.asset_name

    FROM services

    JOIN assets

    ON assets.id = services.asset_id

    ORDER BY services.id DESC

    """)

    data = cursor.fetchall()

    connection.close()

    return data


# =====================================
# DELETE SERVICE
# =====================================

def delete_service(service_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        "DELETE FROM services WHERE id=?",

        (service_id,)

    )

    connection.commit()

    connection.close()