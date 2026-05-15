from pathlib import Path
import json


def load_previous_findings(
    findings_path
):

    findings_file = (
        findings_path / "findings.json"
    )

    if not findings_file.exists():
        return []

    with open(findings_file, "r") as file:
        return json.load(file)


def detect_recurring_findings(
    current_findings: list,
    previous_findings: list
) -> list:

    recurring = []

    previous_keys = set()

    for finding in previous_findings:

        key = (
            finding.get("affected_user"),
            finding.get("control_id")
        )

        previous_keys.add(key)

    for finding in current_findings:

        current_key = (
            finding.get("affected_user"),
            finding.get("control_id")
        )

        if current_key in previous_keys:

            recurring.append({
                "finding_id": finding["finding_id"],
                "affected_user": (
                    finding["affected_user"]
                ),
                "control_id": (
                    finding["control_id"]
                ),
                "control_name": (
                    finding["control_name"]
                ),
                "severity": (
                    finding["severity"]
                )
            })

    return recurring