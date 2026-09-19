"""
CODE COMBAT Pro - Cryptographic Session & Admin Authentication Module
Uses HMAC-SHA256 tokens and constant-time password verification.
"""

import hmac
import hashlib
import time
import base64
import json
from typing import Dict, Any, Optional


class Auth:
    """Manages constant-time password verification and signed session tokens."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.admin_password = str(self.config.get("admin_password", "admin123"))
        self.secret_key = str(self.config.get("secret_key", "code_combat_ultra_secret_hmac_key_2026")).encode("utf-8")

    def verify_admin_password(self, password_attempt: str) -> bool:
        """Compares provided password with configured admin password in constant time."""
        if not password_attempt:
            return False
        return hmac.compare_digest(
            password_attempt.strip().encode("utf-8"),
            self.admin_password.encode("utf-8")
        )

    def update_admin_password(self, new_password: str):
        """Updates runtime admin password."""
        self.admin_password = str(new_password).strip()
        self.config["admin_password"] = self.admin_password

    def create_session_token(self, participant_id: str, participant_name: str, expiry_hours: int = 12) -> str:
        """Creates a tamper-proof HMAC-signed session token."""
        payload = {
            "pid": participant_id,
            "name": participant_name,
            "exp": int(time.time()) + (expiry_hours * 3600)
        }
        raw_payload = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        signature = hmac.new(self.secret_key, raw_payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{raw_payload}.{signature}"

    def verify_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifies HMAC signature and expiration of session token."""
        if not token or "." not in token:
            return None
        parts = token.split(".")
        if len(parts) != 2:
            return None

        raw_payload, received_sig = parts
        expected_sig = hmac.new(self.secret_key, raw_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(received_sig, expected_sig):
            return None

        try:
            payload = json.loads(base64.urlsafe_b64decode(raw_payload.encode("utf-8")).decode("utf-8"))
            if payload.get("exp", 0) < time.time():
                return None  # Expired
            return payload
        except Exception:
            return None
