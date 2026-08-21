
import sys
import os
import time

import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "stock-cache"))
from stock_cache import update_stock  # noqa: E402

WAREHOUSE_URL = "http://127.0.0.1:5000/inventory"
POLL_INTERVAL = 300


def poll_warehouse():
    try:
        response = requests.get(WAREHOUSE_URL)
        response.raise_for_status()
        body = response.json()
    except requests.RequestException as err:
        print("Error contacting warehouse:", err)
        return
    except ValueError as err:
        print("Warehouse API did not return valid JSON:", err)
        return

    if body.get("status") != "success":
        print("Warehouse API returned an error:", body.get("message"))
        return

    rows = body.get("data", [])
    synced = 0
    for row in rows:
        try:
            update_stock(row["sku"], row["warehouse_code"], row["quantity"])
            synced += 1
        except KeyError as err:
            print("Skipping malformed row, missing field:", err, row)

    print(f"Synced {synced}/{len(rows)} rows to stock_cache.")


if __name__ == "__main__":
    while True:
        print("\nPolling warehouse...")
        poll_warehouse()
        print(f"Waiting {POLL_INTERVAL} seconds until the next poll...")
        time.sleep(POLL_INTERVAL)