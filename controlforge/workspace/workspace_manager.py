from pathlib import Path
import re


class WorkspaceManager:

    def __init__(
        self,
        client_name: str,
        engagement_id: str
    ):

        self.client_slug = self.slugify(client_name)
        self.engagement_slug = self.slugify(engagement_id)

        self.base_path = (
            Path("clients")
            / self.client_slug
            / self.engagement_slug
        )

        self.findings_path = self.base_path / "findings"
        self.metadata_path = self.base_path / "metadata"
        self.reports_path = self.base_path / "reports"
        self.evidence_path = self.base_path / "evidence"
        self.history_path = self.base_path / "history"

    def slugify(self, value: str) -> str:
        value = value.lower().strip()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")

    def create_workspace(self):
        self.findings_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self.evidence_path.mkdir(parents=True, exist_ok=True)
        self.history_path.mkdir(parents=True, exist_ok=True)

    def get_paths(self):
        return {
            "base": self.base_path,
            "findings": self.findings_path,
            "metadata": self.metadata_path,
            "reports": self.reports_path,
            "evidence": self.evidence_path,
            "history": self.history_path
        }