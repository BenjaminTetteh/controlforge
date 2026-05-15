from datetime import datetime


def initialize_remediation_fields(
    findings: list
):
    from datetime import datetime, timedelta
    
    for finding in findings:

        if "status" not in finding:
            finding["status"] = "Open"

        if "remediation_owner" not in finding:
            finding["remediation_owner"] = (
                "Unassigned"
            )

        if "remediation_status" not in finding:
            finding["remediation_status"] = (
                "Not Started"
            )

        if "remediation_evidence" not in finding:
            finding["remediation_evidence"] = None

        if "remediation_submitted_at" not in finding:
            finding["remediation_submitted_at"] = None

        if "validated_by_auditor" not in finding:
            finding["validated_by_auditor"] = False

        if "auditor_validation_notes" not in finding:
            finding["auditor_validation_notes"] = None

        if "validated_at" not in finding:
            finding["validated_at"] = None

        if "closure_approved" not in finding:
            finding["closure_approved"] = False

        if "closed_at" not in finding:
            finding["closed_at"] = None

        if "remediation_due_date" not in finding:
            finding["remediation_due_date"] = (
                datetime.now() + timedelta(days=30)
            ).strftime("%Y-%m-%d")

        if "created_at" not in finding:
            finding["created_at"] = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

    return findings