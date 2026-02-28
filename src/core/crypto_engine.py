from cryptography.hazmat.primitives import hashes

def hash_data(data: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()