
import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "warehouse_db"),
    )


def update_stock(sku, warehouse_code, quantity):

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO stock_cache (sku, warehouse_code, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            quantity = VALUES(quantity),
            last_updated = CURRENT_TIMESTAMP
        """,
        (sku, warehouse_code, quantity),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_stock(sku):
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT sku, warehouse_code, quantity, last_updated
        FROM stock_cache
        WHERE sku = %s
        ORDER BY warehouse_code
        """,
        (sku,),
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def get_all_stock():
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT sku, warehouse_code, quantity, last_updated
        FROM stock_cache
        ORDER BY sku, warehouse_code
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows