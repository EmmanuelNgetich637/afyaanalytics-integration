# backend/sessions/session_store.py

import time
import uuid

SESSIONS = {}


class SessionStore:
    def create_session(self):
        session_id = str(uuid.uuid4())

        SESSIONS[session_id] = {
            "handshake_token": None,
            "access_token": None,
            "refresh_token": None,
            "created_at": time.time()
        }

        return session_id

    def get(self, session_id):
        return SESSIONS.get(session_id)

    def update(self, session_id, data):
        if session_id in SESSIONS:
            SESSIONS[session_id].update(data)

    def delete(self, session_id):
        if session_id in SESSIONS:
            del SESSIONS[session_id]