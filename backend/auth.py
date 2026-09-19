"""
CODE COMBAT - Simple Offline Authentication Module
"""

import hmac
import hashlib
from typing import Dict, Any


class Auth:
    """Provides password checks for local admin panel."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.admin_password = self.config.get("admin_password", "admin123")

    def verify_admin_password(self, password_attempt: str) -> bool:
        """Compares provided password with configured admin password in constant time."""
        if not password_attempt:
            return False
        return hmac.compare_digest(
            password_attempt.strip().encode("utf-8"),
            self.admin_password.encode("utf-8")
        )
