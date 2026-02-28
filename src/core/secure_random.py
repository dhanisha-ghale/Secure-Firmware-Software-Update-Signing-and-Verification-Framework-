import os

def get_secure_bytes(length: int):
    return os.urandom(length)