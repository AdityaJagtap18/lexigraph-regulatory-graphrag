"""Cloud Security: AWS KMS Envelope Encryption Service (AES-256-GCM)."""

import base64
import os
from typing import Dict, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class KMSEnvelopeEncryptionService:
    """Envelope encryption provider leveraging AES-256-GCM data keys wrapped by KMS CMK."""

    DEFAULT_KMS_KEY_ARN = "arn:aws:kms:us-east-1:123456789012:key/lexigraph-compliance-cmk"

    def __init__(self, kms_key_arn: str = DEFAULT_KMS_KEY_ARN):
        self.kms_key_arn = kms_key_arn
        # Deterministic 256-bit Customer Master Key (CMK)
        self._cmk = AESGCM.generate_key(bit_length=256)

    def generate_data_key(self) -> Tuple[bytes, bytes]:
        """Simulates kms:GenerateDataKey — returns (plaintext_dek, ciphertext_dek)."""
        plaintext_dek = AESGCM.generate_key(bit_length=256)

        # Encrypt DEK with CMK
        aesgcm = AESGCM(self._cmk)
        nonce = os.urandom(12)
        encrypted_dek = nonce + aesgcm.encrypt(nonce, plaintext_dek, None)

        return plaintext_dek, encrypted_dek

    def encrypt_payload(self, plaintext: str) -> Dict[str, str]:
        """Encrypts data using envelope encryption: generates DEK, encrypts payload, wraps DEK."""
        plaintext_dek, encrypted_dek = self.generate_data_key()

        # Encrypt payload with DEK using AES-GCM
        aesgcm = AESGCM(plaintext_dek)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

        # Package into secure envelope
        return {
            "algorithm": "AES-256-GCM",
            "kms_key_arn": self.kms_key_arn,
            "encrypted_data_key": base64.b64encode(encrypted_dek).decode("utf-8"),
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8")
        }

    def decrypt_payload(self, envelope: Dict[str, str]) -> str:
        """Unwraps DEK using CMK and decrypts the ciphertext payload."""
        encrypted_dek = base64.b64decode(envelope["encrypted_data_key"])
        nonce = base64.b64decode(envelope["nonce"])
        ciphertext = base64.b64decode(envelope["ciphertext"])

        # Decrypt DEK with CMK
        cmk_aes = AESGCM(self._cmk)
        dek_nonce = encrypted_dek[:12]
        dek_cipher = encrypted_dek[12:]
        plaintext_dek = cmk_aes.decrypt(dek_nonce, dek_cipher, None)

        # Decrypt payload with plaintext DEK
        payload_aes = AESGCM(plaintext_dek)
        plaintext_bytes = payload_aes.decrypt(nonce, ciphertext, None)

        return plaintext_bytes.decode("utf-8")
