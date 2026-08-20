from flask import Flask, jsonify

app = Flask(__name__)

inventory = [
    {
        "product_id": "SKU001",
        "product_name": "Nike Air Force 1",
        "quantity": 15
    },
    {
        "product_id": "SKU002",
        "product_name": "Adidas Campus",
        "quantity": 8
    },
    {
        "product_id": "SKU003",
        "product_name": "New Balance 550",
        "quantity": 0
    }
]


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


if __name__ == "__main__":
    app.run(port=5001, debug=True)