
import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "warehouse_db"),
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
            p.sku,
            p.product_name,
            w.warehouse_code,
            i.quantity,
            i.last_updated
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN warehouses w ON i.warehouse_id = w.warehouse_id
    """)
    inventory = cursor.fetchall()
    cursor.close()
    connection.close()
    return inventory


def get_inventory_by_sku(sku):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            p.sku,
            p.product_name,
            w.warehouse_code,
            i.quantity,
            i.last_updated
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN warehouses w ON i.warehouse_id = w.warehouse_id
        WHERE p.sku = %s
    """, (sku,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows