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

            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)

            data = response.json()

            if not data.get("success"):
                print("❌ INIT FAILED:", data)
                return None

            handshake_token = data["data"]["handshake_token"]
            expires_in = data["data"]["expires_in_seconds"]

            self.token_manager.set_handshake_token(handshake_token, expires_in)

            print("✅ Handshake initiated")
            return data

        except Exception as e:
            print("❌ INIT ERROR:", str(e))
            return None

    # -------------------------
    # COMPLETE HANDSHAKE
    # -------------------------
    def complete_handshake(self):
        url = f"{BASE_URL}/complete-handshake"

        handshake_token = self.token_manager.get_handshake_token()

        if not handshake_token:
            print("❌ No handshake token found")
            return None

        if not self.token_manager.is_handshake_valid():
            print("❌ Handshake expired")
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

            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)

            data = response.json()

            if not data.get("success"):
                print("❌ COMPLETE FAILED:", data)
                return None

            access_token = data["data"]["access_token"]
            refresh_token = data["data"]["refresh_token"]
            expires_in = data["data"]["expires_in_seconds"]

            self.token_manager.set_access_token(access_token, expires_in)

            return data

        except Exception as e:
            print("❌ COMPLETE ERROR:", str(e))
            return None

    # -------------------------
    # FULL FLOW
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

        complete_result = self.complete_handshake()
        if not complete_result:
            return {
                "success": False,
                "message": "Complete handshake failed"
            }

        print("\n🎉 FULL AUTH SUCCESS\n")

        return {
            "success": True,
            "message": "Handshake completed successfully",
            "data": complete_result
        }