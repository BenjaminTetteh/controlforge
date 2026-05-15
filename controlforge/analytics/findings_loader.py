import json


def load_saved_findings(findings_path) -> list:
    findings_file = findings_path / "findings.json"

    if not findings_file.exists():
        return []

    with open(findings_file, "r") as file:
        return json.load(file)