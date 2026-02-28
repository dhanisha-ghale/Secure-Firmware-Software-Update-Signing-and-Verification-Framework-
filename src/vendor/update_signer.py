import json
import hashlib
from src.core.signature_manager import SignatureManager

class UpdateSigner:
    def __init__(self, private_key, certificate):
        self.private_key = private_key
        self.certificate = certificate

    def sign_firmware(self, firmware_path, version):
        with open(firmware_path, "rb") as f:
            data = f.read()
        digest = hashlib.sha256(data).digest()
        signature = SignatureManager.sign_data(self.private_key, digest)
        metadata = {"version": version, "signature": signature.hex()}
        metadata_path = firmware_path + ".metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)
        return metadata_path