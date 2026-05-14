from pathlib import Path
import json


class AuditHistoryManager:

    def __init__(
        self,
        history_path
    ):

        self.history_file = (
            history_path / "audit_history.json"
        )

    def load_history(self):

        if not self.history_file.exists():
            return []

        with open(self.history_file, "r") as file:
            return json.load(file)

    def append_audit_run(
        self,
        audit_summary: dict
    ):

        history = self.load_history()

        history.append(audit_summary)

        with open(self.history_file, "w") as file:
            json.dump(
                history,
                file,
                indent=4
            )