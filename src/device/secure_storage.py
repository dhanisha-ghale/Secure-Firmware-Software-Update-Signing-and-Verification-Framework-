import os
import json

class SecureStorage:
    def __init__(self, storage_dir="keystore/device"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_key(self, key_name, key_data):
        path = os.path.join(self.storage_dir, key_name)
        with open(path, "wb") as f:
            f.write(key_data)

    def load_key(self, key_name):
        path = os.path.join(self.storage_dir, key_name)
        with open(path, "rb") as f:
            return f.read()