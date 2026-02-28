import os, json
from datetime import datetime

class AuditTrail:
    def __init__(self, log_file="logs/audit/audit_trail.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                json.dump([], f)

    def record_event(self, event_type, description):
        with open(self.log_file, "r") as f:
            logs = json.load(f)
        logs.append({"timestamp": datetime.utcnow().isoformat(),
                     "event": event_type,
                     "description": description})
        with open(self.log_file, "w") as f:
            json.dump(logs, f, indent=4)