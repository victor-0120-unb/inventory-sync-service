from flask import Flask, jsonify
from db import get_warehouses, get_inventory

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Warehouse API is running"
    })


@app.route("/warehouses")
def warehouses():
    return jsonify(get_warehouses())


@app.route("/inventory")
def inventory():
    return jsonify(get_inventory())


if __name__ == "__main__":
    app.run(debug=True)