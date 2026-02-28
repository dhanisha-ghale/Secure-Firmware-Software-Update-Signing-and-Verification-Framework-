import json
import hashlib
# src/device/update_verifier.py
from src.core.signature_manager import SignatureManager
class UpdateVerifier:
    def __init__(self, trusted_cert):
        self.trusted_cert = trusted_cert

    def verify_update(self, firmware_path, metadata_path, vendor_public_key):
        with open(firmware_path, "rb") as f:
            data = f.read()

        digest = hashlib.sha256(data).digest()

        # Load metadata
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        signature = bytes.fromhex(metadata["signature"])

        # Verify signature
        return SignatureManager.verify_signature(vendor_public_key, digest, signature)