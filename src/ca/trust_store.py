class TrustStore:
    def __init__(self):
        self.trusted_certs = []

    def add_cert(self, cert):
        self.trusted_certs.append(cert)

    def is_trusted(self, cert):
        return cert in self.trusted_certs