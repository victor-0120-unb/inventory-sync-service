"""
Quick manual test for GET /inventory/<product_id>.
Run the Flask app first (python app.py), then run this script.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def test_existing_product():
    # Replace NS-1001 with a real product_id from your inventory table
    resp = requests.get(f"{BASE_URL}/inventory/NS-1001")
    print("Existing product ->", resp.status_code, resp.json())


def test_missing_product():
    resp = requests.get(f"{BASE_URL}/inventory/DOES-NOT-EXIST")
    print("Missing product ->", resp.status_code, resp.json())


if __name__ == "__main__":
    test_existing_product()
    test_missing_product()
