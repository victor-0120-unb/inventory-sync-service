import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vack0120.",
        database="warehouse_api_db"
    )


def get_warehouses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM warehouses")
    warehouses = cursor.fetchall()

    cursor.close()
    connection.close()

    return warehouses


def get_inventory():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            inventory_id,
            warehouse_id,
            product_name,
            category,
            quantity,
            reorder_level,
            unit_price
        FROM inventory
    """)

    inventory = cursor.fetchall()

    cursor.close()
    connection.close()

    return inventory