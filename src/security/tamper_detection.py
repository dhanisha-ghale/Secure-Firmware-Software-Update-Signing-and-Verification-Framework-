from .integrity_monitor import IntegrityMonitor

class TamperDetection:
    def __init__(self):
        self.monitor = IntegrityMonitor()

    def record(self, firmware_path):
        self.monitor.record_hash(firmware_path)

    def check(self, firmware_path):
        return self.monitor.is_tampered(firmware_path)