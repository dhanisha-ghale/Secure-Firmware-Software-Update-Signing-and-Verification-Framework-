class ReplayAttackSimulator:
    def __init__(self):
        self.installed_versions = set()

    def check(self, version):
        if version in self.installed_versions:
            return True
        self.installed_versions.add(version)
        return False