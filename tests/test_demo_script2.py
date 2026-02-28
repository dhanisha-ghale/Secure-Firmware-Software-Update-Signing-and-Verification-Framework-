import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from demo.demo_script2 import SecureFirmwareCLI


class TestSecureFirmwareCLI(unittest.TestCase):

    def setUp(self):
        """Create a fresh CLI instance for each test"""
        self.cli = SecureFirmwareCLI()

    @patch("demo.demo_script2.FirmwareBuilder.create_dummy_firmware")
    @patch("demo.demo_script2.save_file")
    @patch("demo.demo_script2.UpdateVerifier")
    @patch("demo.demo_script2.UpdateSigner")
    @patch("demo.demo_script2.KeyManager")
    def test_initialize_system_generates_firmware(
        self, mock_key_manager, mock_signer_class, mock_verifier_class,
        mock_save_file, mock_create_fw
    ):
        # Mock key generation
        mock_key_manager.return_value.generate_rsa_keypair.side_effect = [
            ("ca_private", "ca_public"),
            ("vendor_private", "vendor_public")
        ]

        # Run initialization
        self.cli.initialize_system_and_generate_updates()

        # Firmware list should have entries
        self.assertGreater(len(self.cli.firmware_files), 0)
        # Tampered firmware should exist
        self.assertIn(
            "updates/tampered/Manufacturer_Update_v1.1.bin",
            self.cli.firmware_files
        )

    @patch("demo.demo_script2.input", return_value="1")
    def test_verify_tampered_firmware_detected(self, mock_input):
        self.cli.firmware_files = ["updates/tampered/Manufacturer_Update_v1.1.bin"]
        self.cli.verifier = MagicMock()
        self.cli.signer = MagicMock()
        # Simulate verification failure
        self.cli.verifier.verify_update.return_value = False

        with patch("builtins.print") as mock_print:
            self.cli.verify_firmware()
            mock_print.assert_any_call(
                "   ❌ Signature invalid! Firmware is unsafe.\n"
            )

    @patch("demo.demo_script2.input", return_value="1")
    def test_verify_valid_firmware(self, mock_input):
        self.cli.firmware_files = ["updates/signed/Manufacturer_Update_v1.0.bin"]
        self.cli.signer = MagicMock()
        self.cli.signer.private_key.public_key.return_value = "public_key"

        self.cli.verifier = MagicMock()
        self.cli.verifier.verify_update.return_value = True

        with patch("builtins.print") as mock_print:
            self.cli.verify_firmware()
            mock_print.assert_any_call(
                "   ✅ Signature valid. Firmware is safe to install.\n"
            )

    @patch("demo.demo_script2.input", return_value="invalid")
    def test_invalid_user_selection(self, mock_input):
        self.cli.firmware_files = ["file1.bin"]
        self.cli.verifier = MagicMock()
        self.cli.signer = MagicMock()

        with patch("builtins.print") as mock_print:
            self.cli.verify_firmware()
            mock_print.assert_any_call("❌ Invalid selection!")

    @patch("demo.demo_script2.input", side_effect=["3"])
    def test_main_exit(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.run()
            mock_print.assert_any_call(
                "👋 Exiting Secure Firmware CLI. Goodbye!"
            )


if __name__ == "__main__":
    unittest.main()