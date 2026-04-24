"""
Main Flask application for AfyaAnalytics integration service.
Exposes API endpoints for handshake authentication flow.
"""

from flask import Flask, jsonify
from flask_cors import CORS

from services.afya_service import AfyaService

app = Flask(__name__)
CORS(app)

# Create service instance
afya_service = AfyaService()


# HEALTH CHECK ENDPOINT

@app.route("/")
def home():
    return jsonify({
        "message": "AfyaAnalytics Integration API is running"
    })


# START HANDSHAKE FLOW

@app.route("/start-handshake", methods=["GET"])
def start_handshake():
    result = afya_service.run_full_handshake_flow()

    if not result:
        return jsonify({
            "success": False,
            "message": "Handshake flow failed"
        }), 500

    return jsonify({
        "success": True,
        "message": "Handshake completed successfully",
        "data": result
    })


# RUN SERVER

if __name__ == "__main__":
    app.run(debug=True)