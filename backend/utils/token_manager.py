"""
In-memory token manager for handshake and access tokens.
Handles expiry tracking and lifecycle management.
"""

import time


class TokenManager:
    def __init__(self):
        self.tokens = {
            "handshake_token": None,
            "access_token": None,
            "handshake_expiry": None,
            "access_expiry": None
        }

    # -------------------------
    # STORE TOKENS
    # -------------------------
    def set_handshake_token(self, token, expires_in_seconds):
        self.tokens["handshake_token"] = token
        self.tokens["handshake_expiry"] = time.time() + expires_in_seconds

    def set_access_token(self, token, expires_in_seconds):
        self.tokens["access_token"] = token
        self.tokens["access_expiry"] = time.time() + expires_in_seconds

    # -------------------------
    # GET TOKENS
    # -------------------------
    def get_handshake_token(self):
        return self.tokens["handshake_token"]

    def get_access_token(self):
        return self.tokens["access_token"]

    # -------------------------
    # VALIDATION
    # -------------------------
    def is_handshake_valid(self):
        expiry = self.tokens["handshake_expiry"]
        return expiry and time.time() < expiry

    def is_access_valid(self):
        expiry = self.tokens["access_expiry"]
        return expiry and time.time() < expiry

    # -------------------------
    # RESET
    # -------------------------
    def clear_all(self):
        self.tokens = {
            "handshake_token": None,
            "access_token": None,
            "handshake_expiry": None,
            "access_expiry": None
        }