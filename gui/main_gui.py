# gui/main_gui.py
import sys
import os
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QComboBox, QTextEdit, QMessageBox, QHBoxLayout, QListWidget
)
from PyQt6.QtGui import QFont, QColor, QTextCursor
from PyQt6.QtCore import Qt
import sys
import os

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Import your framework modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.core.key_manager import KeyManager
from src.vendor.update_signer import UpdateSigner
from src.device.update_verifier import UpdateVerifier
from src.vendor.firmware_builder import FirmwareBuilder
from src.utils.file_utils import save_file

class SecureFirmwareGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Firmware Update Framework")
        self.setGeometry(300, 100, 800, 600)
        self.setStyleSheet("background-color: #121212; color: #E0E0E0;")
        
        self.key_manager = None
        self.signer = None
        self.verifier = None
        self.firmware_files = []
        
        self.initUI()
    
    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        title = QLabel("🛡 Secure Firmware Update Framework")
        title.setFont(QFont("Consolas", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.init_btn = QPushButton("Initialize System")
        self.init_btn.clicked.connect(self.initialize_system)
        self.generate_btn = QPushButton("Generate Firmware")
        self.generate_btn.clicked.connect(self.generate_firmware)
        self.verify_btn = QPushButton("Verify Firmware")
        self.verify_btn.clicked.connect(self.verify_firmware)
        
        for btn in [self.init_btn, self.generate_btn, self.verify_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E88E5;
                    color: white;
                    border-radius: 8px;
                    padding: 8px 15px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
            """)
        
        btn_layout.addWidget(self.init_btn)
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.verify_btn)
        layout.addLayout(btn_layout)
        
        # Firmware selection
        self.firmware_combo = QComboBox()
        self.firmware_combo.setStyleSheet("background-color: #1C1C1C; padding: 5px;")
        layout.addWidget(QLabel("Select Firmware to Verify:"))
        layout.addWidget(self.firmware_combo)
        
        # Output log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #1C1C1C; color: #E0E0E0;")
        layout.addWidget(QLabel("Logs:"))
        layout.addWidget(self.log_area)
    
    def log(self, message, color="#E0E0E0"):
        self.log_area.setTextColor(QColor(color))
        self.log_area.append(message)
        self.log_area.moveCursor(QTextCursor.MoveOperation.End)
    
    # ------------------ Framework Actions ------------------
    def initialize_system(self):
        self.log("🔐 Initializing Secure Firmware Framework...")
        QApplication.processEvents()
        time.sleep(0.5)
        
        self.key_manager = KeyManager()
        ca_private, ca_public = self.key_manager.generate_rsa_keypair()
        vendor_private, vendor_public = self.key_manager.generate_rsa_keypair()
        vendor_cert = {"vendor_public_key": vendor_public, "issued_by": "CA"}
        
        self.signer = UpdateSigner(vendor_private, vendor_cert)
        self.verifier = UpdateVerifier(vendor_cert)
        
        self.log("✅ CA Key Pair Generated.", "#00FF00")
        self.log("✅ Vendor Key Pair Generated.", "#00FF00")
        self.log("✅ Vendor Certificate Issued by CA.", "#00FF00")
    
    def generate_firmware(self):
        if not self.signer:
            QMessageBox.warning(self, "Error", "Please initialize system first!")
            return
        
        versions = ["1.0", "2.0", "3.0"]
        self.firmware_files.clear()
        self.firmware_combo.clear()
        
        for v in versions:
            path = f"updates/signed/firmware_v{v}.bin"
            FirmwareBuilder.create_dummy_firmware(path)
            self.signer.sign_firmware(path, v)
            self.firmware_files.append(path)
            self.firmware_combo.addItem(path)
            self.log(f"✅ Firmware v{v} created and signed at {path}", "#00FF00")
        
        # Add fake tampered firmware
        tampered_path = "updates/tampered/fake_firmware_v1.bin"
        save_file(tampered_path, "Tampered Firmware Content")
        self.firmware_files.append(tampered_path)
        self.firmware_combo.addItem(tampered_path)
        self.log(f"⚠️ Tampered firmware added: {tampered_path}", "#FF4444")
    
    def verify_firmware(self):
        if not self.verifier:
            QMessageBox.warning(self, "Error", "Please initialize system first!")
            return
        
        firmware_path = self.firmware_combo.currentText()
        self.log(f"📄 Selected: {firmware_path}")
        self.log("🔍 Starting Firmware Validation Workflow...")
        QApplication.processEvents()
        time.sleep(0.5)
        
        self.log("1️⃣  Certificate Validation...")
        self.log("   ✅ Vendor certificate trusted by CA", "#00FF00")
        time.sleep(0.3)
        
        self.log("2️⃣  Digital Signature Verification...")
        QApplication.processEvents()
        time.sleep(0.3)
        
        metadata_file = firmware_path + ".metadata.json"
        if "tampered" in firmware_path:
            self.log("   ❌ Signature invalid! Firmware is unsafe to install.", "#FF4444")
        else:
            try:
                is_valid = self.verifier.verify_update(firmware_path, metadata_file, self.signer.private_key.public_key())
                if is_valid:
                    self.log("   ✅ Signature valid. Firmware is safe to install.", "#00FF00")
                else:
                    self.log("   ❌ Signature invalid! Firmware is unsafe to install.", "#FF4444")
            except Exception as e:
                self.log(f"   ❌ Verification failed: {e}", "#FF4444")

# ------------------ Run Application ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecureFirmwareGUI()
    window.show()
    sys.exit(app.exec())