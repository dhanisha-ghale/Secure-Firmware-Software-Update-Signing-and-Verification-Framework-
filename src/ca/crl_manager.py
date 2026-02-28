class CRLManager:
    def __init__(self):
        self.revoked_certs = []

    def revoke_cert(self, cert_serial):
        self.revoked_certs.append(cert_serial)

    def is_revoked(self, cert_serial):
        return cert_serial in self.revoked_certs