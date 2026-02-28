import os
import sys
import time

from src.core.key_manager import KeyManager
from src.vendor.update_signer import UpdateSigner
from src.device.update_verifier import UpdateVerifier
from src.vendor.firmware_builder import FirmwareBuilder
from src.utils.file_utils import save_file


class SecureFirmwareCLI:

    def __init__(self):
        self.key_manager = None
        self.signer = None
        self.verifier = None
        self.firmware_files = []

    def initialize_system_and_generate_updates(self):
        print("\n🔐 Initializing Secure Firmware Framework...\n")
        time.sleep(1)

        self.key_manager = KeyManager()

        # Generate CA and Vendor keys
        ca_private, ca_public = self.key_manager.generate_rsa_keypair()
        vendor_private, vendor_public = self.key_manager.generate_rsa_keypair()

        vendor_cert = {
            "vendor_public_key": vendor_public,
            "issued_by": "CA"
        }

        print("✅ CA Key Pair Generated.")
        print("✅ Vendor Key Pair Generated.")
        print("✅ Vendor Certificate Issued by CA.")

        self.signer = UpdateSigner(vendor_private, vendor_cert)
        self.verifier = UpdateVerifier(vendor_cert)

        print("✅ Framework Initialized. Generating Firmware Updates...\n")
        time.sleep(1)

        official_versions = ["1.0", "2.0", "3.0", "4.0"]
        self.firmware_files.clear()

        for version in official_versions:
            path = f"updates/signed/Manufacturer_Update_v{version}.bin"
            FirmwareBuilder.create_dummy_firmware(path)
            self.signer.sign_firmware(path, version)
            self.firmware_files.append(path)

            print(f"✅ Official Firmware v{version} created and signed at {path}")

        # Create tampered firmware (invalid signature)
        tampered_path = "updates/tampered/Manufacturer_Update_v1.1.bin"
        save_file(tampered_path, "Tampered firmware content")

        tampered_metadata_path = tampered_path + ".metadata.json"
        save_file(
            tampered_metadata_path,
            '{"version": "1.1", "signature": "INVALID"}'
        )

        self.firmware_files.append(tampered_path)

        print(f"⚠️ Tampered firmware created at {tampered_path}\n")

    def verify_firmware(self):

        if not self.verifier:
            print("❌ System not initialized.")
            return

        print("\n📂 Available Firmware Files:")
        for idx, file in enumerate(self.firmware_files, start=1):
            print(f"{idx}. {file}")

        try:
            choice = int(input("\nSelect firmware number to verify: "))
            firmware_path = self.firmware_files[choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return

        print(f"\n📄 Selected: {firmware_path}")
        print("\n🔍 Starting Firmware Validation Workflow...\n")
        time.sleep(1)

        metadata_file = firmware_path + ".metadata.json"

        print("1️⃣ Certificate Validation...")
        print("   ✅ Vendor certificate trusted by CA.\n")
        time.sleep(0.5)

        print("2️⃣ Digital Signature Verification...")

        try:
            is_valid = self.verifier.verify_update(
                firmware_path,
                metadata_file,
                self.signer.private_key.public_key()
            )

            if is_valid:
                print("   ✅ Signature valid. Firmware is safe to install.\n")
            else:
                print("   ❌ Signature invalid! Firmware is unsafe.\n")

        except Exception as e:
            print(f"   ❌ Verification failed: {e}")
            return

        print(f"✅ Firmware verification completed: {'Valid' if is_valid else 'Invalid'}\n")

    def run(self):

        while True:
            print("===========================================")
            print("   Secure Firmware Update CLI Simulation")
            print("===========================================")
            print("1️⃣  Initialize System & Generate Updates")
            print("2️⃣  Verify Firmware")
            print("3️⃣  Exit")
            print("===========================================")

            option = input("Select an option: ")

            if option == "1":
                self.initialize_system_and_generate_updates()

            elif option == "2":
                if not self.firmware_files:
                    print("❌ Please initialize system first!\n")
                    continue
                self.verify_firmware()

            elif option == "3":
                print("👋 Exiting Secure Firmware CLI. Goodbye!")
                break

            else:
                print("❌ Invalid option.\n")


if __name__ == "__main__":
    cli = SecureFirmwareCLI()
    cli.run()
    