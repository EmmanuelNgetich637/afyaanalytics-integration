"""
Main Flask application for AfyaAnalytics integration service.
Handles handshake API endpoint execution.
"""

from flask import Flask, jsonify
from flask_cors import CORS

from services.afya_service import AfyaService

app = Flask(__name__)
CORS(app)

afya_service = AfyaService()


@app.route("/")
def home():
    return jsonify({
        "message": "AfyaAnalytics Integration API is running"
    })


@app.route("/start-handshake", methods=["GET"])
def start_handshake():
    result = afya_service.run_full_handshake_flow()

    if not result or result.get("success") is not True:
        return jsonify({
            "success": False,
            "message": result.get("message", "Handshake failed"),
            "data": result
        }), 500

    return jsonify({
        "success": True,
        "message": result.get("message"),
        "data": result.get("data")
    }), 200


@app.route("/callback", methods=["POST"])
def callback():
    return jsonify({"message": "Callback received"}), 200


if __name__ == "__main__":
    app.run(debug=True)