"""Session-based encryption for API keys using Fernet (AES-256)."""
from __future__ import annotations

import base64
import logging
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger(__name__)


class EncryptionError(RuntimeError):
    """Raised when encryption/decryption fails."""


class SessionEncryption:
    """Session-based encryption for API keys.

    Uses Fernet (AES-256 symmetric encryption) to encrypt API keys
    for storage in session cookies. Keys are never persisted to database.
    """

    def __init__(self, secret_key: str):
        """Initialize encryption with a secret key.

        Args:
            secret_key: A string at least 32 characters long.
                       Will be hashed to create a Fernet key.

        Raises:
            EncryptionError: If secret_key is too short or invalid.
        """
        if not secret_key or len(secret_key) < 32:
            raise EncryptionError(
                "secret_key must be at least 32 characters long"
            )

        # Derive a Fernet key from the secret key
        # Fernet requires a 32-byte URL-safe base64-encoded key
        key_bytes = secret_key[:32].encode("utf-8")
        # Pad or truncate to exactly 32 bytes
        key_bytes = (key_bytes + b"\x00" * 32)[:32]
        # Encode as URL-safe base64 for Fernet
        fernet_key = base64.urlsafe_b64encode(key_bytes)
        self.cipher = Fernet(fernet_key)

    def encrypt(self, data: str) -> str:
        """Encrypt a string (e.g., API key).

        Args:
            data: The plaintext to encrypt (e.g., API key)

        Returns:
            URL-safe encrypted string that can be stored in a cookie

        Raises:
            EncryptionError: If encryption fails
        """
        try:
            if not data:
                raise EncryptionError("Cannot encrypt empty data")
            encrypted = self.cipher.encrypt(data.encode("utf-8"))
            # Return as URL-safe string for cookie storage
            return encrypted.decode("utf-8")
        except Exception as exc:
            logger.error("Encryption failed", exc_info=True)
            raise EncryptionError(f"Encryption failed: {exc}") from exc

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt an encrypted string.

        Args:
            encrypted_data: The encrypted string (from a cookie)

        Returns:
            The decrypted plaintext (e.g., API key)

        Raises:
            EncryptionError: If decryption fails or data is tampered
        """
        try:
            if not encrypted_data:
                raise EncryptionError("Cannot decrypt empty data")
            decrypted = self.cipher.decrypt(encrypted_data.encode("utf-8"))
            return decrypted.decode("utf-8")
        except InvalidToken as exc:
            logger.error(
                "Decryption failed: invalid token (possible tampering)",
                exc_info=True,
            )
            raise EncryptionError("Decryption failed: invalid or tampered token") from exc
        except Exception as exc:
            logger.error("Decryption failed", exc_info=True)
            raise EncryptionError(f"Decryption failed: {exc}") from exc
