from datetime import datetime, timedelta


def initialize_remediation_fields(
    findings: list
) -> list:

    for finding in findings:

        finding["status"] = "Open"
        finding["remediation_owner"] = "Unassigned"

        finding["remediation_due_date"] = (
            datetime.now() + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        finding["remediation_notes"] = ""
        finding["remediation_status"] = "Pending"

        finding["remediation_evidence"] = ""
        finding["remediation_submitted_at"] = ""

        finding["validated_by_auditor"] = False
        finding["auditor_validation_notes"] = ""
        finding["validated_at"] = ""

        finding["closure_approved"] = False
        finding["closed_at"] = ""

    return findings