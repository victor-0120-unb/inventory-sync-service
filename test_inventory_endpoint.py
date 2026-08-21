
import requests

BASE_URL = "http://127.0.0.1:5000"


def check(label, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")


def test_existing_product():
    resp = requests.get(f"{BASE_URL}/inventory/SKU-1001")
    check("existing sku -> 200", resp.status_code == 200)
    check("existing sku -> success envelope", resp.json().get("status") == "success")
    print("Existing product ->", resp.status_code, resp.json())


def test_missing_product():
    resp = requests.get(f"{BASE_URL}/inventory/DOES-NOT-EXIST")
    check("missing sku -> 404", resp.status_code == 404)
    check("missing sku -> error envelope", resp.json().get("status") == "error")
    print("Missing product ->", resp.status_code, resp.json())


if __name__ == "__main__":
    test_existing_product()
    test_missing_product()