import requests
import time

WAREHOUSE_URL = "http://127.0.0.1:5001/inventory"

POLL_INTERVAL = 300


def poll_warehouse():
    try:
        response = requests.get(WAREHOUSE_URL)

        print("Warehouse response:")
        print(response.json())

    except requests.RequestException as error:
        print("Error contacting warehouse:", error)


while True:
    print("\nPolling warehouse...")
    poll_warehouse()

    print(f"Waiting {POLL_INTERVAL} seconds until the next poll...")
    time.sleep(POLL_INTERVAL)