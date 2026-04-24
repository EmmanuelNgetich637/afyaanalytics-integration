"""
In-memory token manager for storing and validating handshake and access tokens.
Handles expiry tracking and token lifecycle management.
"""

import time 

class TokenManager:
    def _init_(self):
        self.tokens = {
            "handshake_token": None,
            "access_token": None,
            "handshake_expiry": None,
            "access_expiry": None
        }

    #STORE TOKENS

    def set_handshake_token(self, token, expires_in_seconds):
        self.tokens["handshake_token"] = token
        self.tokens["handshake_expiry"] = time.time() + expires_in_seconds
    
    def set_access_token(self, token, expires_in_seconds):
        self.tokens["access_token"] = token
        self.tokens["access_expiry"] = time.time() + expires_in_seconds

    #GET TOKENS

    def get_handshake_toke(self):
        return self.tokens["handshake_token"]
    
    def get_access_toke(self):
        return self.tokens["access_token"]
    
    #EXPIRY CHECKERS

    def is_handshake_valid(self):
        expiry = self.tokens["handshake_expiry"]
        if not expiry:
            return False
        return time.time() < expiry
    
    #RESET / CLEANUP

    def clear_handshake(self):
        self.tokens["handshake_token"] = None

    def clear_all(self):
        self.tokens = {
            "handshake_token": None,
            "access_token": None,
            "handshake_expiry": None,
            "access_expiry": None,
        }