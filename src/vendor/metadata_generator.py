import json

class MetadataGenerator:
    @staticmethod
    def save_metadata(firmware_path, signature, version="1.0"):
        metadata = {"version": version, "signature": signature.hex()}
        metadata_path = firmware_path + ".metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)
        return metadata_path