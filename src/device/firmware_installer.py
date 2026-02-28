import shutil, os

class FirmwareInstaller:
    @staticmethod
    def install(firmware_path, install_dir="device_storage/"):
        os.makedirs(install_dir, exist_ok=True)
        shutil.copy(firmware_path, install_dir)
        return True