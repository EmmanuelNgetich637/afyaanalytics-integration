"""
Service layer handling external API handshake with Afyanalytics.
Manages initiation, completion, and token lifecycle.
"""

import requests
import time

from config import (
    BASE_URL,
    PLATFORM_NAME,
    PLATFORM_KEY,
    PLATFORM_SECRET,
    REQUEST_TIMEOUT
)

from utils.token_manager import TokenManager


class AfyaService:
    def __init__(self):
        self.token_manager = TokenManager()

    # -------------------------
    # INITIATE HANDSHAKE
    # -------------------------
    def initiate_handshake(self):
        url = f"{BASE_URL}/initiate-handshake"

        payload = {
            "platform_name": PLATFORM_NAME,
            "platform_key": PLATFORM_KEY,
            "platform_secret": PLATFORM_SECRET,
            "callback_url": "http://localhost:5000/callback"
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            print("\n➡️ INITIATING HANDSHAKE...")

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

            data = response.json()

            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)

            if not data.get("success"):
                print("❌ INIT FAILED:", data)
                return None

            handshake_token = data.get("data", {}).get("handshake_token")
            expires_in = data.get("data", {}).get("expires_in_seconds")

            if not handshake_token:
                print("❌ Missing handshake token")
                return None

            self.token_manager.set_handshake_token(handshake_token, expires_in)

            print("✅ Handshake initiated")
            return data

        except Exception as e:
            print("❌ INIT ERROR:", str(e))
            return None

    # -------------------------
    # COMPLETE HANDSHAKE (FIXED)
    # -------------------------
    def complete_handshake(self, handshake_token):
        """
        FIX: now accepts handshake_token from Flask route
        """

        url = f"{BASE_URL}/complete-handshake"

        if not handshake_token:
            print("❌ No handshake token provided")
            return None

        payload = {
            "handshake_token": handshake_token,
            "platform_key": PLATFORM_KEY
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            print("\n➡️ COMPLETING HANDSHAKE...")

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

            data = response.json()

            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)

            if not data.get("success"):
                print("❌ COMPLETE FAILED:", data)
                return None

            access_data = data.get("data", {})

            access_token = access_data.get("access_token")
            refresh_token = access_data.get("refresh_token")
            expires_in = access_data.get("expires_in_seconds")

            if not access_token:
                print("❌ Missing access token")
                return None

            self.token_manager.set_access_token(access_token, expires_in)

            print("✅ Handshake completed")
            return data

        except Exception as e:
            print("❌ COMPLETE ERROR:", str(e))
            return None

    # -------------------------
    # FULL FLOW (OPTIONAL UTILITY)
    # -------------------------
    def run_full_handshake_flow(self):
        print("\n🚀 STARTING FULL HANDSHAKE FLOW...\n")

        init_result = self.initiate_handshake()
        if not init_result:
            return {
                "success": False,
                "message": "Initiate handshake failed"
            }

        time.sleep(1)

        handshake_token = self.token_manager.get_handshake_token()

        complete_result = self.complete_handshake(handshake_token)
        if not complete_result:
            return {
                "success": False,
                "message": "Complete handshake failed"
            }

        print("\n FULL AUTH SUCCESS\n")

        return {
            "success": True,
            "message": "Handshake completed successfully",
            "data": complete_result
        }