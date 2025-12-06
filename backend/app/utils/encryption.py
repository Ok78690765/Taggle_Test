"""Encryption utilities for sensitive data"""
import base64
from cryptography.fernet import Fernet

from app.config import settings


class TokenEncryption:
    """Handles encryption and decryption of tokens"""

    def __init__(self):
        """Initialize encryption with secret key"""
        if not settings.secret_key or len(settings.secret_key) < 32:
            raise ValueError(
                "SECRET_KEY must be set and at least 32 characters long"
            )
        key = base64.urlsafe_b64encode(
            settings.secret_key[:32].encode().ljust(32, b"\0")
        )
        self.cipher = Fernet(key)

    def encrypt(self, token: str) -> str:
        """Encrypt a token"""
        encrypted = self.cipher.encrypt(token.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_token: str) -> str:
        """Decrypt an encrypted token"""
        decrypted = self.cipher.decrypt(encrypted_token.encode())
        return decrypted.decode()


token_encryption = TokenEncryption()
