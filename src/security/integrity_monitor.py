import hashlib

class IntegrityMonitor:
    def __init__(self):
        self.hash_store = {}

    def record_hash(self, firmware_path):
        with open(firmware_path, "rb") as f:
            data = f.read()
        h = hashlib.sha256(data).hexdigest()
        self.hash_store[firmware_path] = h

    def is_tampered(self, firmware_path):
        with open(firmware_path, "rb") as f:
            current = hashlib.sha256(f.read()).hexdigest()
        return current != self.hash_store.get(firmware_path, current)