from src.core.key_manager import KeyManager
from src.core.certificate_manager import CertificateManager

class CAService:
    def __init__(self, ca_name="TestCA"):
        self.private_key, self.public_key = KeyManager.generate_rsa_keypair()
        self.cert = CertificateManager.create_self_signed_cert(self.private_key, ca_name)

    def issue_certificate(self, vendor_public_key, vendor_name):
        # In real life, CA signs vendor certificate; here we simulate with self-signed
        return CertificateManager.create_self_signed_cert(self.private_key, vendor_name)