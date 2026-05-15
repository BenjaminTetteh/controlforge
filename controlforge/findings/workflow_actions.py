import json

from datetime import datetime


def assign_finding_owner(
    findings_path,
    finding_id: str,
    owner: str
):

    findings_file = (
        findings_path / "findings.json"
    )

    with open(findings_file, "r") as file:
        findings = json.load(file)

    updated = False

    for finding in findings:

        if finding["finding_id"] == finding_id:

            finding["remediation_owner"] = owner

            finding["status"] = "In Progress"

            updated = True

            break

    if not updated:

        print(
            f"\nFinding not found: {finding_id}"
        )

        return

    with open(findings_file, "w") as file:
        json.dump(
            findings,
            file,
            indent=4
        )

    print(
        f"\nAssigned {finding_id} to {owner}"
    )


def submit_remediation(
    findings_path,
    finding_id: str,
    remediation_evidence: str
):

    findings_file = (
        findings_path / "findings.json"
    )

    with open(findings_file, "r") as file:
        findings = json.load(file)

    updated = False

    for finding in findings:

        if finding["finding_id"] == finding_id:

            finding["remediation_evidence"] = (
                remediation_evidence
            )

            finding["remediation_submitted_at"] = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            finding["status"] = (
                "Evidence Submitted"
            )

            finding["remediation_status"] = (
                "Awaiting Auditor Review"
            )

            updated = True

            break

    if not updated:

        print(
            f"\nFinding not found: {finding_id}"
        )

        return

    with open(findings_file, "w") as file:
        json.dump(
            findings,
            file,
            indent=4
        )

    print(
        f"\nRemediation submitted for "
        f"{finding_id}"
    )


def validate_finding(
    findings_path,
    finding_id: str,
    validation_notes: str
):

    findings_file = (
        findings_path / "findings.json"
    )

    with open(findings_file, "r") as file:
        findings = json.load(file)

    updated = False

    for finding in findings:

        if finding["finding_id"] == finding_id:

            finding["validated_by_auditor"] = True

            finding["auditor_validation_notes"] = (
                validation_notes
            )

            finding["validated_at"] = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            finding["status"] = (
                "Under Auditor Review"
            )

            finding["remediation_status"] = (
                "Validated"
            )

            updated = True

            break

    if not updated:

        print(
            f"\nFinding not found: {finding_id}"
        )

        return

    with open(findings_file, "w") as file:
        json.dump(
            findings,
            file,
            indent=4
        )

    print(
        f"\nFinding validated: "
        f"{finding_id}"
    )


def close_finding(
    findings_path,
    finding_id: str
):

    findings_file = findings_path / "findings.json"

    with open(findings_file, "r") as file:
        findings = json.load(file)

    updated = False

    for finding in findings:

        if finding["finding_id"] == finding_id:

            finding["closure_approved"] = True
            finding["closed_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            finding["status"] = "Closed"
            finding["remediation_status"] = "Closed"

            updated = True
            break

    if not updated:
        print(f"\nFinding not found: {finding_id}")
        return

    with open(findings_file, "w") as file:
        json.dump(findings, file, indent=4)

    print(f"\nFinding closed: {finding_id}")