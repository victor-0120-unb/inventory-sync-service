"""
Stock cache storage layer (Day 4 pivot deliverable).

This module owns the `stock_cache` table: the latest known stock level per
(sku, warehouse_code), written by the webhook receiver in webhook_app.py
and read by the query endpoints in the same file.

Deliberately kept separate from db.py (which belongs to the read-only
`warehouses` / `inventory` source-of-truth API your teammates built) so
this task doesn't touch or risk breaking their code.

Connection settings are read from environment variables so no password
ever needs to live in the repo. Set them before running, e.g.:

    export DB_HOST=localhost
    export DB_USER=root
    export DB_PASSWORD=your_password_here
    export DB_NAME=warehouse_db

NOTE: schema.sql creates a database called `warehouse_db`, but the
existing warehouse-api/db.py connects to `warehouse_api_db`. That
mismatch predates this task and is called out in SCOPE_DELTA_ANALYSIS.md
for the team to resolve. This cache layer targets `warehouse_db`, the
database schema.sql actually creates.
"""

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
    """
    Write (or refresh) the latest stock level for a sku at a warehouse.

    Uses INSERT ... ON DUPLICATE KEY UPDATE against the
    (sku, warehouse_code) unique key, so a webhook event for a sku/warehouse
    we've already seen updates the existing row (and bumps last_updated)
    instead of creating a duplicate.
    """
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
    """Return cached stock rows (one per warehouse) for a single sku."""
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
    """Return every cached stock row, across all skus and warehouses."""
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
