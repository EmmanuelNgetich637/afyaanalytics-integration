from flask import Flask, jsonify
from flask_cors import CORS

from services.afya_service import AfyaService
from sessions.session_store import SessionStore

app = Flask(__name__)

# --------------------
# FIXED CORS CONFIG (IMPORTANT)
# --------------------
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"]
)

afya_service = AfyaService()
store = SessionStore()


# --------------------
# HEALTH CHECK
# --------------------
@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "AfyaAnalytics Integration API is running"
    })


# --------------------
# CREATE SESSION
# --------------------
@app.route("/session/create", methods=["POST"])
def create_session():
    session_id = store.create_session()

    return jsonify({
        "success": True,
        "session_id": session_id
    })


# --------------------
# INITIATE HANDSHAKE
# --------------------
@app.route("/session/<session_id>/initiate", methods=["POST"])
def initiate(session_id):

    session = store.get(session_id)
    if not session:
        return jsonify({
            "success": False,
            "message": "Invalid session"
        }), 404

    result = afya_service.initiate_handshake()

    if not result or not result.get("success"):
        return jsonify({
            "success": False,
            "message": "Handshake initiation failed",
            "raw": result
        }), 500

    data = result.get("data", {})
    handshake_token = data.get("handshake_token")

    if not handshake_token:
        return jsonify({
            "success": False,
            "message": "Handshake token missing",
            "raw": result
        }), 500

    store.update(session_id, {
        "handshake_token": handshake_token
    })

    return jsonify({
        "success": True,
        "data": data
    })


# --------------------
# COMPLETE HANDSHAKE
# --------------------
@app.route("/session/<session_id>/complete", methods=["POST"])
def complete(session_id):

    session = store.get(session_id)
    if not session:
        return jsonify({
            "success": False,
            "message": "Invalid session"
        }), 404

    handshake_token = session.get("handshake_token")

    if not handshake_token:
        return jsonify({
            "success": False,
            "message": "No handshake token found"
        }), 400

    result = afya_service.complete_handshake(handshake_token)

    if not result or not result.get("success"):
        return jsonify({
            "success": False,
            "message": "Handshake completion failed",
            "raw": result
        }), 500

    data = result.get("data", {})

    store.update(session_id, {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token")
    })

    return jsonify({
        "success": True,
        "data": data
    })


# --------------------
# GET SESSION STATUS
# --------------------
@app.route("/session/<session_id>", methods=["GET"])
def get_session(session_id):

    session = store.get(session_id)

    if not session:
        return jsonify({
            "success": False,
            "message": "Session not found"
        }), 404

    return jsonify({
        "success": True,
        "data": session
    })


if __name__ == "__main__":
    app.run(debug=True)