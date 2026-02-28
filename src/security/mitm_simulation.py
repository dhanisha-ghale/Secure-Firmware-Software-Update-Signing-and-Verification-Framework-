class MITMSimulator:
    def check(self, firmware_path):
        # In simulation, always return False (no MITM)
        return False