"""
Reference app.py for Northstar Support Deflection MVP.

IMPORTANT: If backend/app.py already exists in the repo (built by your
teammates), do NOT overwrite it wholesale. Just merge in:
  1. The import:      from routes.inventory import inventory_bp
  2. The registration: app.register_blueprint(inventory_bp)

Everything else here (chat route, health check) is a reasonable guess at
what the rest of the app looks like based on the README's tech stack
(Flask + MySQL, chat interface for order-status/stock-availability).
Swap in the real routes your teammates already wrote.
"""

from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import os

# --- Load environment variables from .env ---
load_dotenv()

app = Flask(__name__)

# --- Register blueprints ---
from routes.inventory import inventory_bp
app.register_blueprint(inventory_bp)

# Add other teammates' blueprints here as they're built, e.g.:
# from routes.order_status import order_status_bp
# app.register_blueprint(order_status_bp)


@app.route("/")
def index():
    """Serves the chat interface."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Simple health check to confirm the app is running."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
