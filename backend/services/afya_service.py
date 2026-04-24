"""
Service layer handling external API handshake with Afyanalytics.
Manages initiation, completion, and token lifecycle.
"""

import requests
from config import (
    BASE_URL,
    PLATFORM_NAME,
    PLATFORM_KEY,
    PLATFORM_SECRET,
    HANDSHAKE_EXPIRY_SECONDS,
    REQUEST_TIMEOUT
)

from utils.token_manager import TokenManager


class AfyaService:
    def __init__(self):
        self.token_manager = TokenManager()

    #INITIATE HANDSHAKE
    
    def initiate_handshake(self):
        url = f"{BASE_URL}/initiate-handshake"

        payload = {
            "platform_name": PLATFORM_NAME,
            "platform_key": PLATFORM_KEY,
            "platform_secret": PLATFORM_SECRET,
            "callback_url": "http://localhost:5000/callback"
        }

        try:
            response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            data = response.json()

            if not data.get("success"):
                raise Exception(data.get("message", "Handshake initiation failed"))

            handshake_token = data["data"]["handshake_token"]
            expires_in = data["data"]["expires_in_seconds"]

            # store token
            self.token_manager.set_handshake_token(handshake_token, expires_in)

            print("✅ Handshake initiated")
            print("Token:", handshake_token)
            print("Expires in:", expires_in, "seconds")

            return data

        except Exception as e:
            print("❌ Error initiating handshake:", str(e))
            return None


    #COMPLETE HANDSHAKE
    
    def complete_handshake(self):
        url = f"{BASE_URL}/complete-handshake"

        handshake_token = self.token_manager.get_handshake_token()

        if not handshake_token:
            print("❌ No handshake token found")
            return None

        payload = {
            "handshake_token": handshake_token,
            "platform_key": PLATFORM_KEY
        }

        try:
            response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            data = response.json()

            if not data.get("success"):
                raise Exception(data.get("message", "Handshake completion failed"))

            access_token = data["data"]["access_token"]
            refresh_token = data["data"]["refresh_token"]
            expires_in = data["data"]["expires_in_seconds"]

            # store access token
            self.token_manager.set_access_token(access_token, expires_in)

            print("✅ Handshake completed")
            print("Access Token:", access_token)

            return data

        except Exception as e:
            print("❌ Error completing handshake:", str(e))
            return None

    # STEP 3: FULL FLOW (AUTO)

    def run_full_handshake_flow(self):
        """
        Executes full authentication flow:
        1. Initiate handshake
        2. Complete handshake
        """

        print("🚀 Starting Afyanalytics handshake flow...")

        init_result = self.initiate_handshake()
        if not init_result:
            return None

        complete_result = self.complete_handshake()
        if not complete_result:
            return None

        print("🎉 Full authentication successful")
        return complete_result