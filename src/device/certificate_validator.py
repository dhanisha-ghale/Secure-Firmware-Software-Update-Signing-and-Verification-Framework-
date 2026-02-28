class CertificateValidator:
    def __init__(self, trusted_certs):
        self.trusted_certs = trusted_certs

    def is_valid(self, cert):
        # Simple check: in trusted store
        return cert in self.trusted_certs