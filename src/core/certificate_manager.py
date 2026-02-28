from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization

class CertificateManager:
    @staticmethod
    def create_self_signed_cert(private_key, common_name, valid_days=365):
        subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=valid_days)
        ).sign(private_key, hashes.SHA256())
        return cert

    @staticmethod
    def save_cert(cert, filepath):
        with open(filepath, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))