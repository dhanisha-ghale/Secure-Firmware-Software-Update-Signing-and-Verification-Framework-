import os

class FirmwareBuilder:
    @staticmethod
    def create_dummy_firmware(path, content="Default firmware content"):
        """
        Creates a dummy firmware file at the given path with the specified content.
        """
        # Ensure parent directory exists
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Write content
        with open(path, "w") as f:
            f.write(content)