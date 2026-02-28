from src.core.certificate_manager import CertificateManager

class CertificateIssuer:
    @staticmethod
    def issue_certificate(private_key, vendor_public_key, vendor_name, valid_days=365):
        # Simulate CA issuing certificate to vendor
        cert = CertificateManager.create_self_signed_cert(private_key, vendor_name, valid_days)
        return cert