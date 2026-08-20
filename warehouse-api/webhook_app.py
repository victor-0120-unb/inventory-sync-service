"""
Webhook receiver + query endpoint for the stock cache (Day 4 pivot).

This replaces polling_service.py in the data flow:

    Old (killed Day 4):
        polling_service.py --GET(every 5 min)--> warehouse_api.py

    New:
        warehouse_api.py --POST /webhook/stock-update--> this service
                                                              |
                                                              v
                                                   stock_cache (MySQL, cache.py)
                                                              |
                                                              v
                                                   GET /stock, GET /stock/<sku>

Run standalone, separate from warehouse-api/app.py (which still serves the
original /warehouses and /inventory read-only endpoints against the
source-of-truth tables - untouched by this pivot):

    python webhook_app.py

Runs on port 5002 by default so it doesn't collide with warehouse_api.py
(5001) or app.py (5000).
"""

from flask import Flask, jsonify, request
from cache import update_stock, get_stock, get_all_stock

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Stock cache / webhook service is running"})


@app.route("/webhook/stock-update", methods=["POST"])
def stock_update():
    """
    Receives a push event from the warehouse whenever a stock level changes.

    Expected JSON body:
        {
            "sku": "SKU001",
            "warehouse_code": "WH-NRB",
            "quantity": 15
        }
    """
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "Missing or invalid JSON body"}), 400

    sku = payload.get("sku")
    warehouse_code = payload.get("warehouse_code")
    quantity = payload.get("quantity")

    if sku is None or warehouse_code is None or quantity is None:
        return jsonify({
            "error": "sku, warehouse_code and quantity are all required"
        }), 400

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify({"error": "quantity must be an integer"}), 400

    if quantity < 0:
        return jsonify({"error": "quantity cannot be negative"}), 400

    update_stock(sku, warehouse_code, quantity)

    return jsonify({
        "status": "cached",
        "sku": sku,
        "warehouse_code": warehouse_code,
        "quantity": quantity
    }), 200


@app.route("/stock/<sku>", methods=["GET"])
def stock_lookup(sku):
    """Latest cached stock for one sku, across all warehouses that reported it."""
    rows = get_stock(sku)

    if not rows:
        return jsonify({"error": f"No cached stock found for sku '{sku}'"}), 404

    return jsonify(rows)


@app.route("/stock", methods=["GET"])
def stock_all():
    """Latest cached stock for every sku/warehouse combination seen so far."""
    return jsonify(get_all_stock())


if __name__ == "__main__":
    app.run(port=5002, debug=True)
