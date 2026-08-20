"""
Manual/smoke test for the webhook + stock cache pivot.

Requires warehouse-api/webhook_app.py to be running on port 5002
(and MySQL up with schema.sql + cache_schema.sql applied).

Run:
    python test_stock_cache.py
"""

import requests

BASE = "http://127.0.0.1:5002"


def check(label, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")


def main():
    # 1. Insert stock for a new product
    r = requests.post(f"{BASE}/webhook/stock-update", json={
        "sku": "SKU001", "warehouse_code": "WH-NRB", "quantity": 15
    })
    check("insert new sku -> 200", r.status_code == 200)

    # 2. Update existing stock (same sku/warehouse, new quantity)
    r = requests.post(f"{BASE}/webhook/stock-update", json={
        "sku": "SKU001", "warehouse_code": "WH-NRB", "quantity": 12
    })
    check("update existing sku -> 200", r.status_code == 200)

    # 3. Retrieve latest stock and confirm it reflects the update, not the insert
    r = requests.get(f"{BASE}/stock/SKU001")
    check("get_stock returns 200", r.status_code == 200)
    rows = r.json()
    check("get_stock reflects latest quantity (12, not 15)",
          any(row["quantity"] == 12 for row in rows))

    # 4. Handle quantity 0 explicitly (must not be treated as missing/falsy)
    r = requests.post(f"{BASE}/webhook/stock-update", json={
        "sku": "SKU003", "warehouse_code": "WH-NRB", "quantity": 0
    })
    check("quantity 0 accepted -> 200", r.status_code == 200)
    r = requests.get(f"{BASE}/stock/SKU003")
    check("quantity 0 stored and retrievable",
          r.status_code == 200 and r.json()[0]["quantity"] == 0)

    # 5. Reject negative quantity
    r = requests.post(f"{BASE}/webhook/stock-update", json={
        "sku": "SKU001", "warehouse_code": "WH-NRB", "quantity": -5
    })
    check("negative quantity rejected -> 400", r.status_code == 400)

    # 6. Unknown sku lookup -> 404
    r = requests.get(f"{BASE}/stock/SKU-DOES-NOT-EXIST")
    check("unknown sku -> 404", r.status_code == 404)

    # 7. last_updated is present on cached rows
    r = requests.get(f"{BASE}/stock/SKU001")
    check("last_updated present", "last_updated" in r.json()[0])

    # 8. get_all_stock returns everything cached so far
    r = requests.get(f"{BASE}/stock")
    check("get_all_stock -> 200 and non-empty", r.status_code == 200 and len(r.json()) > 0)


if __name__ == "__main__":
    main()
