from .tamper_detection import TamperDetection
from .replay_attack_simulation import ReplayAttackSimulator
from .mitm_simulation import MITMSimulator

class AttackSimulator:
    def __init__(self):
        self.tamper = TamperDetection()
        self.replay = ReplayAttackSimulator()
        self.mitm = MITMSimulator()

    def run_all(self, firmware_path):
        return {
            "tamper_detected": self.tamper.check(firmware_path),
            "replay_detected": self.replay.check(firmware_path),
            "mitm_detected": self.mitm.check(firmware_path)
        }