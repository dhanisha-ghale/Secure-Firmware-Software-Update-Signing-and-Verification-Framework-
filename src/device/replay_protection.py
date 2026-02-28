class ReplayProtection:
    def __init__(self):
        self.installed_versions = set()

    def is_new_version(self, version):
        if version in self.installed_versions:
            return False
        self.installed_versions.add(version)
        return True