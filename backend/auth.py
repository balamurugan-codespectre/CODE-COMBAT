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
        self.admin_id = str(self.config.get("admin_id", "admin"))
        self.admin_password = str(self.config.get("admin_password", "admin123"))
        self.secret_key = str(self.config.get("secret_key", "code_combat_ultra_secret_hmac_key_2026")).encode("utf-8")

    def verify_admin_id(self, id_attempt: str) -> bool:
        """Compares provided admin ID with configured admin ID."""
        if not id_attempt:
            return False
        return hmac.compare_digest(
            id_attempt.strip().lower().encode("utf-8"),
            self.admin_id.strip().lower().encode("utf-8")
        )

    def verify_admin_password(self, password_attempt: str) -> bool:
        """Compares provided password with configured admin password in constant time."""
        if not password_attempt:
            return False
        return hmac.compare_digest(
            password_attempt.strip().encode("utf-8"),
            self.admin_password.encode("utf-8")
        )

    def verify_admin_credentials(self, id_attempt: Optional[str], password_attempt: str) -> bool:
        """Verifies both admin ID (if provided) and admin password."""
        if not password_attempt:
            return False
        if id_attempt:
            if not self.verify_admin_id(id_attempt):
                return False
        return self.verify_admin_password(password_attempt)

    def update_admin_credentials(self, new_id: Optional[str] = None, new_password: Optional[str] = None):
        """Updates runtime admin credentials."""
        if new_id and str(new_id).strip():
            self.admin_id = str(new_id).strip()
            self.config["admin_id"] = self.admin_id
        if new_password and str(new_password).strip():
            self.admin_password = str(new_password).strip()
            self.config["admin_password"] = self.admin_password

    def update_admin_password(self, new_password: str):
        """Updates runtime admin password."""
        self.update_admin_credentials(new_password=new_password)

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
